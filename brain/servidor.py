#!/usr/bin/env python3
"""
Sirve el cerebro por http://localhost y le hace de puente al agente.

Por qué existe, en una línea: Chrome no recuerda el permiso del micrófono en
file://, así que hay que abrir el cerebro por http — y en cuanto cambia el
origen, el agente rechaza la llamada por CORS. Este servidor resuelve las dos
cosas a la vez: entrega la página Y reenvía las llamadas al agente, así que
para el navegador todo ocurre en el mismo origen y no hay CORS que valga.

    python3 brain/servidor.py               # puerto 8899
    MAXIMUS_PUERTO=9000 python3 brain/servidor.py

El agente se toma de MAXIMUS_AGENTE si está en el entorno; si no, del túnel
de siempre. El token NO vive acá: lo manda el navegador desde ⚙ conexión y
este servidor solo lo reenvía tal cual.
"""

import json
import os
import ssl
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# El Python de python.org no usa el llavero de macOS y viene sin certificados
# raíz: sin esto, toda llamada https falla con CERTIFICATE_VERIFY_FAILED.
# Se usan los de certifi. Nunca se desactiva la verificación: el túnel lleva
# el token del agente y va por internet.
try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

BASE = Path(__file__).resolve().parent
AGENTE = os.getenv("MAXIMUS_AGENTE", "https://maximus.ngrok.app").rstrip("/")
PUERTO = int(os.getenv("MAXIMUS_PUERTO", "8899"))

# Solo se reenvía lo del cerebro. El panel /admin y el webhook no se exponen
# acá ni por error: este puente es para hablar con Maximus, nada más.
PERMITIDAS = ("/maximus/chat", "/maximus/ver")


class Puente(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)

    def do_POST(self):
        ruta = self.path.split("?")[0]
        if ruta not in PERMITIDAS:
            self.send_error(404, "No encontrado")
            return

        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(largo) if largo else b""

        pedido = urllib.request.Request(
            AGENTE + ruta,
            data=cuerpo,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-maximus-token": self.headers.get("x-maximus-token", ""),
                "ngrok-skip-browser-warning": "1",
            },
        )

        try:
            with urllib.request.urlopen(pedido, timeout=180, context=SSL_CTX) as r:
                datos, codigo = r.read(), r.status
        except urllib.error.HTTPError as e:
            datos, codigo = e.read(), e.code
        except Exception as e:
            # El cerebro espera JSON siempre: un error de red no debe llegarle
            # como una página de error que no sabe leer.
            datos = json.dumps({"respuesta": f"No pude alcanzar al agente: {e}"}).encode()
            codigo = 502

        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def log_message(self, *args):
        pass          # sin ruido en la consola


if __name__ == "__main__":
    print(f"Cerebro en  http://localhost:{PUERTO}/cerebro.html")
    print(f"Puente a    {AGENTE}")
    ThreadingHTTPServer(("127.0.0.1", PUERTO), Puente).serve_forever()
