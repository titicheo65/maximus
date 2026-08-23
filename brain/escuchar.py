#!/usr/bin/env python3
"""
Despertar a Maximus con dos aplausos.

Escucha el micrófono y busca dos golpes secos y cercanos. Cuando los oye,
ejecuta lo que le digas — por defecto, Maximus.command: música, briefing y
cerebro.

    python3 brain/escuchar.py                    # dos aplausos → Maximus.command
    python3 brain/escuchar.py --calibrar         # mide tu ambiente y sugiere umbral
    python3 brain/escuchar.py --umbral 0.35      # más alto = menos falsos positivos
    python3 brain/escuchar.py --cmd "..."        # ejecuta otra cosa

Qué distingue un aplauso de un portazo o de una voz: un aplauso es un pico de
energía muy corto y con mucha diferencia contra el ruido de fondo. Se exige que
haya DOS dentro de una ventana breve, y que entre medio el sonido baje. Eso
descarta casi todo lo que no es un aplauso — pero nada lo descarta todo, por eso
existe --umbral.

Requiere: pip3 install sounddevice
Y permiso de micrófono para la Terminal (macOS lo pide la primera vez).
"""

import argparse
import subprocess
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent.parent

FS = 16000            # frecuencia de muestreo
BLOQUE = 512          # ~32 ms por bloque
UMBRAL = 0.28         # energía mínima para considerar un golpe
MIN_ENTRE = 0.09      # segundos mínimos entre los dos aplausos
MAX_ENTRE = 0.65      # y máximos: más lento que esto no es un doble aplauso
FACTOR_FONDO = 6.0    # el golpe debe superar el ruido de fondo por este factor
PAUSA_TRAS_DISPARO = 6.0   # no volver a disparar de inmediato


def calibrar(segundos=5):
    import sounddevice as sd
    print(f"Midiendo tu ambiente {segundos} segundos. Quédate en silencio…")
    grabacion = sd.rec(int(segundos * FS), samplerate=FS, channels=1, dtype="float32")
    sd.wait()
    fondo = float(np.abs(grabacion).mean())
    pico = float(np.abs(grabacion).max())
    print(f"\n  ruido de fondo: {fondo:.4f}")
    print(f"  pico más alto:  {pico:.4f}")
    sugerido = max(0.15, min(0.6, pico * 3))
    print(f"\n  umbral sugerido: {sugerido:.2f}")
    print(f"  úsalo así:  python3 brain/escuchar.py --umbral {sugerido:.2f}")


def escuchar(umbral: float, comando: str):
    import sounddevice as sd

    fondo = deque(maxlen=60)          # ~2 s de ruido reciente
    golpes = deque(maxlen=4)
    ultimo_disparo = 0.0

    print(f"Escuchando. Da dos aplausos.   (umbral {umbral}, Ctrl+C para salir)\n")

    def bloque(datos, frames, tiempo, estado):
        nonlocal ultimo_disparo
        ahora = time.time()
        energia = float(np.abs(datos).max())
        media = float(np.abs(datos).mean())
        fondo.append(media)
        piso = float(np.mean(fondo)) if fondo else 0.001

        es_golpe = energia > umbral and energia > piso * FACTOR_FONDO
        if not es_golpe:
            return
        if golpes and ahora - golpes[-1] < MIN_ENTRE:
            return                      # el mismo aplauso repartido en dos bloques
        golpes.append(ahora)

        if len(golpes) >= 2:
            delta = golpes[-1] - golpes[-2]
            if MIN_ENTRE <= delta <= MAX_ENTRE and ahora - ultimo_disparo > PAUSA_TRAS_DISPARO:
                ultimo_disparo = ahora
                golpes.clear()
                print(f"  ✱ dos aplausos ({delta*1000:.0f} ms) — despertando a Maximus")
                subprocess.Popen(comando, shell=True, cwd=str(BASE),
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOQUE,
                            dtype="float32", callback=bloque):
            while True:
                time.sleep(0.4)
    except KeyboardInterrupt:
        print("\nListo.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrar", action="store_true")
    ap.add_argument("--umbral", type=float, default=UMBRAL)
    ap.add_argument("--cmd", default=str(BASE / "Maximus.command"))
    a = ap.parse_args()

    if a.calibrar:
        calibrar()
    else:
        escuchar(a.umbral, a.cmd)
