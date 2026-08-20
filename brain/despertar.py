#!/usr/bin/env python3
"""
Secuencia de arranque de Maximus.

  riff de entrada  →  saludo hablado

Uso:
    python3 brain/despertar.py                    # saludo por defecto
    python3 brain/despertar.py "texto a decir"    # saludo propio
    python3 brain/despertar.py --mudo             # solo el riff

El audio de arranque vive en ~/harvey/audio/ y está fuera del repositorio:
son derechos de terceros y no corresponde versionarlos.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RIFF = BASE / "audio" / "arranque.mp3"

SEGUNDOS_RIFF = 5
VOLUMEN_RIFF = 0.55
VOZ = "es-CL-LorenzoNeural"

SALUDO_DEFECTO = "Maximus en línea. Dime qué necesitas."


def sonar_riff(segundos=SEGUNDOS_RIFF, volumen=VOLUMEN_RIFF, bloquear=True):
    """Reproduce la entrada. Si no existe el archivo, sigue sin quejarse."""
    if not RIFF.exists():
        return None
    cmd = ["afplay", "-t", str(segundos), "-v", str(volumen), str(RIFF)]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if bloquear:
        p.wait()
    return p


async def hablar(texto: str):
    """Sintetiza con edge-tts (gratis, voz chilena) y reproduce."""
    try:
        import edge_tts
    except ImportError:
        print("edge-tts no instalado:  pip3 install edge-tts")
        return
    salida = BASE / "audio" / ".saludo.mp3"
    await edge_tts.Communicate(texto, VOZ).save(str(salida))
    subprocess.run(["afplay", str(salida)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    salida.unlink(missing_ok=True)


async def despertar(texto: str = SALUDO_DEFECTO, mudo: bool = False):
    # El riff suena mientras la voz se sintetiza: cero espera muerta.
    proceso = sonar_riff(bloquear=False)
    if not mudo:
        try:
            import edge_tts
            salida = BASE / "audio" / ".saludo.mp3"
            await edge_tts.Communicate(texto, VOZ).save(str(salida))
        except ImportError:
            salida = None
    if proceso:
        proceso.wait()
    if not mudo and salida and salida.exists():
        subprocess.run(["afplay", str(salida)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        salida.unlink(missing_ok=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--mudo"]
    mudo = "--mudo" in sys.argv
    texto = args[0] if args else SALUDO_DEFECTO
    asyncio.run(despertar(texto, mudo))
