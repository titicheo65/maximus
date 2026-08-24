#!/usr/bin/env python3
"""
Mide el umbral real de aplauso para escuchar.py.

El --calibrar que trae escuchar.py mide 5 segundos de silencio y sugiere
pico*3. Eso da el piso del ambiente, no el número que discrimina: lo que
decide si un aplauso se distingue de un portazo es la distancia entre TU
aplauso y TU ruido cotidiano, y ninguno de los dos se mide callado.

Esto mide las dos cosas por separado y busca el hueco entre ellas:

  fase 1 · ambiente  → sigue haciendo lo de siempre, no te quedes callado
  fase 2 · aplausos  → ocho aplausos sueltos, uno por segundo

Si no hay hueco, lo dice en vez de inventar un número: significa que en ese
ambiente el aplauso no es distinguible y hay que disparar Maximus de otra
forma.

    python3 brain/calibrar.py

Antes de correrlo, apaga el micrófono del cerebro (el botón del mic): si
Chrome tiene el micrófono tomado, las mediciones salen bajas.
"""

import sys
import time

import numpy as np
import sounddevice as sd

FS = 16000
BLOQUE = 512              # ~32 ms, el mismo que usa escuchar.py
SEG_AMBIENTE = 20
SEG_APLAUSOS = 12
N_APLAUSOS = 8


def picos(grabacion):
    """Pico de energía por bloque, igual que lo mide escuchar.py."""
    g = np.abs(grabacion).ravel()
    n = len(g) // BLOQUE
    return np.array([g[i * BLOQUE:(i + 1) * BLOQUE].max() for i in range(n)])


def cuenta(mensaje, segundos):
    print(f"\n{mensaje}")
    for i in range(3, 0, -1):
        print(f"   {i}…", end="", flush=True)
        time.sleep(1)
    print(f"  ¡ya!  ({segundos} s)")


def golpes_reales(p, cuantos, separacion, relativo=0.3):
    """
    Los golpes que de verdad son golpes.

    Pedir "los 8 picos más altos" a secas siempre devuelve 8, aunque hayas
    aplaudido tres veces: rellena con los ruidos más altos que encuentre. Y si
    después uno toma el más flojo de esa lista, está midiendo ruido y creyendo
    que mide un aplauso.

    Por eso se exige que cada golpe llegue al menos al `relativo` del más
    fuerte. Lo que no llega, no era un aplauso, y se descarta en vez de
    contaminar el cálculo.
    """
    if len(p) == 0:
        return np.array([])
    corte = p.max() * relativo
    elegidos = []
    for i in np.argsort(p)[::-1]:
        if p[i] < corte:
            break
        if all(abs(int(i) - j) >= separacion for j in elegidos):
            elegidos.append(int(i))
        if len(elegidos) >= cuantos:
            break
    return np.array([p[i] for i in elegidos])


def sordo():
    """
    ¿El micrófono está llegando de verdad?

    Un aplauso cerca del micrófono satura: da valores sobre 0,3 y a menudo
    cerca de 1,0. Si un aplauso de prueba apenas se mueve, el micrófono está
    tomado por otra app —Chrome, típicamente— o la entrada está muy baja.
    Sin esta prueba, las dos fases igual devuelven números y uno concluye
    cualquier cosa a partir de un instrumento que no estaba midiendo.
    """
    print("\nPRUEBA DEL MICRÓFONO. Da UN aplauso fuerte cuando diga ya.")
    for i in range(3, 0, -1):
        print(f"   {i}…", end="", flush=True)
        time.sleep(1)
    print("  ¡ya!")
    g = sd.rec(int(3 * FS), samplerate=FS, channels=1, dtype="float32")
    sd.wait()
    pico = float(np.abs(g).max())
    print(f"   pico medido: {pico:.3f}")

    if pico >= 0.25:
        return False

    print("\n" + "─" * 58)
    print("  El micrófono no está capturando bien. No sigo: cualquier número")
    print("  que saliera de acá sería basura con formato de dato.")
    print("\n  Revisa, en este orden:")
    print("   1. El cerebro: apaga el botón del micrófono, o cierra la pestaña.")
    print("      Mientras Chrome lo tenga tomado, acá llega casi nada.")
    print("   2. Ajustes → Sonido → Entrada: que sea el micrófono del MacBook")
    print("      y que el volumen de entrada no esté abajo.")
    print("   3. Que no haya un Teams, Meet o Zoom abierto usándolo.")
    print("─" * 58)
    return True


def main():
    print("Calibración del aplauso — dispositivo:", sd.query_devices(kind="input")["name"])

    if sordo():
        return 3

    cuenta("FASE 1 · ambiente. Sigue con tu ruido normal, NO te quedes callado.",
           SEG_AMBIENTE)
    grab = sd.rec(int(SEG_AMBIENTE * FS), samplerate=FS, channels=1, dtype="float32")
    sd.wait()                      # sin esto se analiza una grabación a medias
    amb = picos(grab)

    # El máximo de 20 s es un dato frágil: UN golpe accidental cerca del
    # micrófono lo dispara y vetaría cualquier umbral. Lo que importa es el
    # nivel que el ambiente sostiene, y aparte, cuántas veces lo cruza.
    p50, p99, alto, top = (np.percentile(amb, 50), np.percentile(amb, 99),
                           np.percentile(amb, 99.9), amb.max())
    print(f"\n  ambiente:  típico {p50:.3f}   ruidoso {p99:.3f}"
          f"   casi el techo {alto:.3f}   pico suelto {top:.3f}")

    cuenta(f"FASE 2 · {N_APLAUSOS} aplausos SUELTOS, uno por segundo.", SEG_APLAUSOS)
    ap = sd.rec(int(SEG_APLAUSOS * FS), samplerate=FS, channels=1, dtype="float32")
    sd.wait()
    golpes = golpes_reales(picos(ap), N_APLAUSOS, separacion=15)   # ~0,5 s entre golpes

    if len(golpes) < 4:
        print(f"\n  Detecté solo {len(golpes)} aplauso(s) claro(s) de {N_APLAUSOS}.")
        print("  Con tan pocos no hay con qué calcular. Repite dando los ocho,")
        print("  bien separados, uno por segundo.")
        return 1

    if len(golpes) < N_APLAUSOS:
        print(f"\n  (detecté {len(golpes)} de {N_APLAUSOS} aplausos — alcanza para calcular)")

    flojo, fuerte = golpes.min(), golpes.max()
    print(f"\n  aplausos:  el más flojo {flojo:.3f}   el más fuerte {fuerte:.3f}")

    # Controles del instrumento, en orden. Cada uno es una causa distinta y
    # necesita una acción distinta: confundirlas hace descartar el aplauso por
    # una medición mala en vez de arreglar la medición.

    # 1. Entrada saturada. En esta escala 1,0 es el techo: si el AMBIENTE ya
    #    llega ahí, macOS está amplificando y todo satura por igual. Con la
    #    entrada así no hay umbral posible, pero el problema es el volumen,
    #    no el aplauso.
    if top > 0.9:
        print("\n" + "─" * 58)
        print("  ENTRADA SATURADA — hay que bajar el volumen del micrófono.")
        print(f"  El ruido de fondo llega a {top:.2f} y el techo de la escala es 1,00.")
        print("  Con la entrada tan alta, un portazo y un aplauso marcan lo mismo:")
        print("  los dos llegan al tope. Ningún umbral los separa.")
        print("\n  Ajustes → Sonido → Entrada: baja el volumen de entrada hasta")
        print("  que hablando normal la barra quede por la mitad, y repite.")
        print("─" * 58)
        return 4

    # 2. Micrófono sordo: no llegó señal de aplauso.
    if fuerte < 0.25:
        print("\n" + "─" * 58)
        print("  MEDICIÓN INVÁLIDA — no un veredicto.")
        print(f"  El aplauso más fuerte marcó {fuerte:.3f}; uno real satura cerca de 1,0.")
        print("  Algo tomó el micrófono, o dejaste de aplaudir. Repite.")
        print("─" * 58)
        return 3

    # 3. Ahora sí: señal sana, pero el aplauso no despega del ruido.
    if fuerte < top * 1.5:
        print("\n" + "─" * 58)
        print("  MEDICIÓN INVÁLIDA — no un veredicto.")
        print(f"  Tus aplausos ({fuerte:.3f}) apenas superan al ruido ({top:.3f}).")
        print("  Aplaude más cerca del micrófono y repite.")
        print("─" * 58)
        return 3

    # El umbral vive en el hueco: sobre lo que el ambiente sostiene, bajo el
    # aplauso más flojo. El pico suelto no manda — se reporta como riesgo.
    piso = alto
    techo = flojo * 0.7

    print("\n" + "─" * 58)
    if techo <= piso:
        print("  NO hay separación entre tu ruido y tus aplausos.")
        print(f"  El ambiente sostiene {piso:.3f} y el aplauso más flojo da {flojo:.3f}.")
        print("\n  Ningún umbral distingue los dos. Subirlo te deja sin despertar;")
        print("  bajarlo lo dispara solo. En este ambiente el aplauso no sirve")
        print("  como disparador: mejor un atajo de teclado o el ícono del Dock.")
        return 2

    umbral = round(min(max((piso + techo) / 2, 0.15), 0.9), 2)

    # Lo único que de verdad predice si esto va a molestar: cuántas veces el
    # ambiente medido habría cruzado el umbral elegido.
    cruces = int((amb > umbral).sum())
    por_hora = cruces * (3600 / SEG_AMBIENTE)

    print(f"  UMBRAL RECOMENDADO:  {umbral:.2f}")
    print(f"  Tu aplauso más flojo lo supera {flojo/umbral:.1f} veces.")
    if cruces == 0:
        print(f"  En {SEG_AMBIENTE} s de tu ambiente, cero cruces. Limpio.")
    else:
        print(f"  Ojo: tu ambiente lo cruzó {cruces} vez(ces) en {SEG_AMBIENTE} s")
        print(f"  — del orden de {por_hora:.0f} por hora. Hacen falta DOS seguidos")
        print("  para disparar, pero con esa tasa vas a tener despertares solos.")
    print("\n  Para usarlo:")
    print(f"    python3 brain/escuchar.py --umbral {umbral:.2f}")
    print("─" * 58)
    return 0


if __name__ == "__main__":
    sys.exit(main())
