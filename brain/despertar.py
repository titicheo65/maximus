#!/usr/bin/env python3
"""
Secuencia de arranque de Maximus.

  intro de música (25 s)  →  la música baja  →  saludo hablado encima  →  cierre

La música no se corta cuando entra la voz: baja a volumen de fondo y sigue
corriendo hasta que Maximus termina de hablar.

Uso:
    python3 brain/despertar.py                    # saludo por defecto
    python3 brain/despertar.py "texto a decir"    # saludo propio
    python3 brain/despertar.py --mudo             # solo la música

El audio de arranque vive en ~/harvey/audio/ y está fuera del repositorio:
son derechos de terceros y no corresponde versionarlos.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RIFF = BASE / "audio" / "arranque.mp3"

SEGUNDOS_INTRO = 25      # música sola antes de que hable
VOLUMEN_RIFF = 0.55      # volumen de la intro
VOLUMEN_FONDO = 0.10     # volumen mientras Maximus habla
SEGUNDOS_BAJADA = 2.5    # cuánto tarda en bajar
SEGUNDOS_CIERRE = 4.0    # sigue sonando al final y se apaga fundiendo
VOZ = "es-CL-LorenzoNeural"

SALUDO_DEFECTO = "Maximus en línea. Dime qué necesitas."


# ── Reproductor con volumen en vivo ───────────────────────────────────
# afplay fija el volumen al lanzarse y no lo suelta más: sirve para la intro,
# no para bajarla. AVAudioPlayer (AVFoundation, vía pyobjc) sí permite mover
# el volumen del mismo proceso, que es lo que hace posible el fondo.
#   pip3 install pyobjc-framework-AVFoundation
# Si no está, se degrada a afplay y la música termina donde entra la voz.

def _reproductor(path: Path, volumen: float):
    try:
        from AVFoundation import AVAudioPlayer
        from Foundation import NSURL
    except ImportError:
        return None
    url = NSURL.fileURLWithPath_(str(path))
    player, _ = AVAudioPlayer.alloc().initWithContentsOfURL_error_(url, None)
    if player is None:
        return None
    player.setVolume_(volumen)
    player.prepareToPlay()
    player.play()
    return player


async def _fundir(player, desde: float, hasta: float, segundos: float, pasos: int = 30):
    """Fundido hecho a mano. setVolume:fadeDuration: depende del runloop de Cocoa,
    que acá no corre; un bucle propio es más aburrido y no falla."""
    for i in range(1, pasos + 1):
        player.setVolume_(desde + (hasta - desde) * i / pasos)
        await asyncio.sleep(segundos / pasos)


def sonar_riff(segundos=SEGUNDOS_INTRO, volumen=VOLUMEN_RIFF, bloquear=True):
    """Reproduce la entrada con afplay. Si no existe el archivo, sigue sin quejarse."""
    if not RIFF.exists():
        return None
    cmd = ["afplay", "-t", str(segundos), "-v", str(volumen), str(RIFF)]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if bloquear:
        p.wait()
    return p


async def _sintetizar(texto: str):
    """Devuelve la ruta del mp3 de la voz, o None si edge-tts no está."""
    try:
        import edge_tts
    except ImportError:
        print("edge-tts no instalado:  pip3 install edge-tts")
        return None
    salida = BASE / "audio" / ".saludo.mp3"
    await edge_tts.Communicate(texto, VOZ).save(str(salida))
    return salida if salida.exists() else None


async def _decir(salida: Path):
    p = await asyncio.create_subprocess_exec(
        "afplay", str(salida),
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
    await p.wait()


async def hablar(texto: str):
    """Sintetiza con edge-tts (gratis, voz chilena) y reproduce. Sin música."""
    salida = await _sintetizar(texto)
    if salida:
        await _decir(salida)
        salida.unlink(missing_ok=True)


async def despertar(texto: str = SALUDO_DEFECTO, mudo: bool = False):
    musica = _reproductor(RIFF, VOLUMEN_RIFF) if RIFF.exists() else None
    proceso = None
    if musica is None and RIFF.exists():
        # Sin AVFoundation: la música alcanza solo para la intro.
        proceso = sonar_riff(bloquear=False)

    inicio = asyncio.get_running_loop().time()

    # La voz se sintetiza mientras suena la intro: cero espera muerta.
    salida = None if mudo else await _sintetizar(texto)

    # Que la intro dure lo suyo aunque la síntesis haya sido rápida.
    resto = SEGUNDOS_INTRO - (asyncio.get_running_loop().time() - inicio)
    if resto > 0:
        await asyncio.sleep(resto)

    if mudo or not salida:
        if musica:
            await _fundir(musica, VOLUMEN_RIFF, 0.0, SEGUNDOS_CIERRE)
            musica.stop()
        elif proceso:
            proceso.wait()
        return

    if musica:
        await _fundir(musica, VOLUMEN_RIFF, VOLUMEN_FONDO, SEGUNDOS_BAJADA)
    elif proceso:
        proceso.wait()

    await _decir(salida)
    salida.unlink(missing_ok=True)

    if musica:
        await _fundir(musica, VOLUMEN_FONDO, 0.0, SEGUNDOS_CIERRE)
        musica.stop()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--mudo"]
    mudo = "--mudo" in sys.argv
    texto = args[0] if args else SALUDO_DEFECTO
    asyncio.run(despertar(texto, mudo))
