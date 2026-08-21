#!/bin/bash
# Despertar a Maximus — doble clic desde el Finder.
#   riff de entrada → saludo hablado → cerebro visual

cd "$(dirname "$0")" || exit 1

SALUDO="${1:-Maximus en línea.}"

python3 brain/despertar.py "$SALUDO"

# Refresca el grafo por si la memoria cambió, y lo abre
python3 brain/grafo.py >/dev/null 2>&1
open brain/cerebro.html

# La ventana de Terminal se cierra sola
osascript -e 'tell application "Terminal" to close (every window whose name contains "Maximus")' >/dev/null 2>&1 &
exit 0
