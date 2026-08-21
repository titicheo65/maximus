#!/usr/bin/env python3
"""
Briefing matutino de Maximus.

Junta lo de afuera (clima, indicadores) con lo de adentro (pendientes abiertos de
la memoria) y le pide a Maximus que arme el saludo del día. Distinto cada mañana,
porque el contenido cambia — no por variar la fórmula.

Calendario y correos NO se piden acá: llegan como parámetro (--contexto) desde
quien los tenga autenticados. Ver la nota de arquitectura al final del archivo.

Uso:
    python3 brain/briefing.py                 # imprime el briefing
    python3 brain/briefing.py --hablar        # lo dice en voz alta
    python3 brain/briefing.py --contexto "3 correos nuevos; sin reuniones"
"""

import asyncio
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

BASE = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("America/Santiago")
ARICA = (-18.4783, -70.3126)

_DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
_MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
          "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _json(url: str, timeout: int = 15):
    """
    httpx primero: trae su propio bundle de certificados. El urllib de Python en
    macOS falla con CERTIFICATE_VERIFY_FAILED si nadie corrió
    'Install Certificates.command', y ese fallo es silencioso en un briefing.
    """
    try:
        import httpx
        r = httpx.get(url, timeout=timeout)
        return r.json() if r.status_code == 200 else None
    except ImportError:
        pass
    except Exception:
        return None
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None


def indicadores() -> str:
    d = _json("https://mindicador.cl/api")
    if not d:
        return "Indicadores: no disponibles."
    partes = []
    for k, etq in [("dolar", "dólar"), ("euro", "euro"), ("uf", "UF")]:
        if k in d:
            partes.append(f"{etq} ${d[k]['valor']:,.2f}".replace(",", "."))
    return " · ".join(partes)


def clima() -> str:
    lat, lon = ARICA
    d = _json(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
              "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
              "&current=temperature_2m&timezone=America/Santiago&forecast_days=1")
    if not d:
        return "Clima: no disponible."
    c, dia = d["current"], d["daily"]
    lluvia = dia["precipitation_probability_max"][0]
    txt = (f"{c['temperature_2m']:.0f}°C ahora, "
           f"máxima {dia['temperature_2m_max'][0]:.0f}°, "
           f"mínima {dia['temperature_2m_min'][0]:.0f}°")
    return txt + (f", {lluvia}% de lluvia" if lluvia and lluvia > 20 else "")


def pendientes(maximo: int = 8) -> str:
    """Lo que la memoria tiene abierto, con su valor en juego si está declarado."""
    idx = BASE / "memoria" / "indice.json"
    if not idx.exists():
        return "Sin memoria atómica disponible."
    data = json.loads(idx.read_text(encoding="utf-8"))
    abiertos = [n for n in data["nodos"]
                if n["tipo"] in ("pendiente", "tesis")
                and n["estado"] in ("abierto", "propuesto", "conflicto")]
    abiertos.sort(key=lambda n: -n["grado"])
    hoy = datetime.now(TZ).date()
    lineas = []
    for n in abiertos[:maximo]:
        edad = ""
        if n.get("fecha"):
            try:
                dias = (hoy - datetime.fromisoformat(n["fecha"]).date()).days
                edad = f", abierto hace {dias} día{'s' if dias != 1 else ''}"
            except ValueError:
                edad = ""
        lineas.append(f"- {n['id']}: {n['titulo']} [{n['estado']}{edad}]")
    conflictos = [n["id"] for n in data["nodos"] if n["estado"] == "conflicto"]
    if conflictos:
        lineas.append(f"- CONFLICTOS SIN RESOLVER: {', '.join(conflictos)}")
    return "\n".join(lineas) or "Nada abierto."


async def armar(contexto_extra: str = "") -> str:
    from anthropic import AsyncAnthropic
    from dotenv import load_dotenv
    load_dotenv(Path.home() / "whatsapp-agentkit" / ".env")
    from recuperar import Cerebro

    ahora = datetime.now(TZ)
    fecha = f"{_DIAS[ahora.weekday()]} {ahora.day} de {_MESES[ahora.month-1]}"

    datos = f"""FECHA: {fecha}, {ahora.strftime('%H:%M')} hrs, Arica.
CLIMA: {clima()}
INDICADORES: {indicadores()}

PENDIENTES ABIERTOS EN TU MEMORIA:
{pendientes()}
"""
    if contexto_extra:
        datos += f"\nAGENDA Y CORREO:\n{contexto_extra}\n"

    cerebro = Cerebro()
    fija = cerebro.core()

    instruccion = """Arma el briefing matutino de Ricardo. Reglas:

- Máximo 8 líneas. Se escucha en voz alta mientras se viste o maneja.
- Primera línea: saludo corto y LO MÁS IMPORTANTE del día. Nada de "espero que
  tengas un buen día".
- Clima e indicadores en UNA línea, juntos, sin ceremonia.
- De los pendientes elige a lo más TRES: los que de verdad mueven la aguja hoy.
  No leas la lista completa.
- Si hay conflictos sin resolver en la memoria, dilo.
- Cierra proponiendo UNA cosa concreta para hoy. No preguntes "¿qué quieres hacer?".
- Texto plano, sin markdown ni asteriscos: esto se convierte en voz.
- Los montos escríbelos como se leen ("novecientos veinte pesos", "treinta millones").

PROHIBIDO INVENTAR. Solo puedes usar los datos que vienen abajo. Si algo no está
—cuántos días lleva algo abierto, una cifra, una fecha— NO lo estimes ni lo
rellenes: omítelo. Un briefing con un dato inventado vale menos que uno corto.
Si el clima o los indicadores no llegaron, no los menciones.
"""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    r = await client.messages.create(
        model=os.getenv("MAXIMUS_MODEL", "claude-opus-4-5"),
        max_tokens=600,
        system=[{"type": "text", "text": fija + "\n\n" + instruccion,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": datos}],
    )
    return r.content[0].text.strip()


async def main():
    extra = ""
    if "--contexto" in sys.argv:
        i = sys.argv.index("--contexto")
        if i + 1 < len(sys.argv):
            extra = sys.argv[i + 1]

    texto = await armar(extra)
    print(texto)

    if "--hablar" in sys.argv:
        from despertar import despertar
        await despertar(texto)


# ── Nota de arquitectura ──────────────────────────────────────────────
# Clima e indicadores no piden autenticación: los saca cualquiera, incluido
# ServidorPlaya. Calendario y Gmail sí, y hoy están autenticados solo en el Mac
# de Ricardo (vía los conectores de Claude Code). Por eso entran por --contexto
# en vez de consultarse acá: así este script corre igual en los dos lados, y
# quien tenga las llaves le pasa el pedazo que le falta.
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(main())
