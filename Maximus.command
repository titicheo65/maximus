#!/bin/bash
# Despertar a Maximus — doble clic desde el Finder.
#   riff de entrada → saludo hablado → cerebro visual

cd "$(dirname "$0")" || exit 1

SALUDO="${1:-Maximus en línea.}"

python3 brain/despertar.py "$SALUDO"

# Refresca el grafo por si la memoria cambió, y lo abre
python3 brain/grafo.py >/dev/null 2>&1
# Chrome explicito: Safari no reconoce voz y los visores embebidos bloquean el microfono
open -a "Google Chrome" brain/cerebro.html 2>/dev/null || open brain/cerebro.html

# La ventana de Terminal se cierra sola
osascript -e 'tell application "Terminal" to close (every window whose name contains "Maximus")' >/dev/null 2>&1 &
exit 0
