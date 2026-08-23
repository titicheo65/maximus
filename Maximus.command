#!/bin/bash
# Despertar a Maximus — doble clic desde el Finder.
#   riff de entrada → saludo hablado → cerebro visual
#
# Dos guardas, porque el disparador puede ser un aplauso mal detectado:
#   1. una sola instancia a la vez  → no se solapan música ni saludo
#   2. una sola pestaña del cerebro → si ya está abierta, se trae al frente

cd "$(dirname "$0")" || exit 1

SALUDO="${1:-Maximus en línea.}"

# ── Guarda 1 · instancia única ────────────────────────────────────────
# mkdir es atómico: o lo crea este proceso o ya existe. El lock huérfano
# (kill -9, corte de luz) se limpia solo a los 5 minutos — el despertar
# completo dura ~40 s, así que nunca hay un lock legítimo tan viejo.
LOCK="/tmp/maximus.despertar.lock"
find /tmp -maxdepth 1 -name "maximus.despertar.lock" -mmin +5 -exec rmdir {} \; 2>/dev/null
if ! mkdir "$LOCK" 2>/dev/null; then
    exit 0          # ya hay un despertar en curso: este se va en silencio
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

python3 brain/despertar.py "$SALUDO"

# Refresca el grafo por si la memoria cambió
python3 brain/grafo.py >/dev/null 2>&1

# ── Cómo se abre el cerebro ───────────────────────────────────────────
# En file:// Chrome trata la página como origen opaco y NO recuerda el permiso
# del micrófono: lo vuelve a pedir en cada turno y no se puede conversar de
# corrido. Servirlo por http://localhost lo arregla… pero el agente solo acepta
# los orígenes "null" (file://) y la app Base44, así que hasta que el servidor
# no autorice localhost, cambiar de origen rompe el chat con "Failed to fetch".
#
# brain/servidor.py sirve la página Y hace de puente al agente, así que todo
# ocurre en el mismo origen: sin CORS, y sin depender de desplegar nada en
# ServidorPlaya. Ponlo en 0 solo para volver al comportamiento viejo.
USAR_LOCALHOST=1
PUERTO=8899

URL="brain/cerebro.html"
if [ "$USAR_LOCALHOST" = "1" ]; then
    LOCAL="http://localhost:$PUERTO/cerebro.html"
    if ! curl -s -o /dev/null --max-time 1 "$LOCAL"; then
        # Un http.server pelado de una sesión anterior sirve la página pero no
        # hace de puente: hay que sacarlo o el chat falla por CORS.
        lsof -ti tcp:"$PUERTO" | xargs kill 2>/dev/null
        nohup python3 brain/servidor.py >/dev/null 2>&1 &
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            curl -s -o /dev/null --max-time 1 "$LOCAL" && break
            sleep 0.3
        done
    fi
    curl -s -o /dev/null --max-time 1 "$LOCAL" && URL="$LOCAL"
fi

# ── Guarda 2 · una sola pestaña ───────────────────────────────────────
# Si el cerebro ya está abierto en Chrome, se enfoca y no se abre otro.
# No se recarga a propósito: si estás dictándole, recargar te corta.
# La aguja es la URL exacta, no solo "cerebro.html": una pestaña vieja servida
# por localhost también contiene ese nombre y se confundiría con la buena.
if [ "$URL" = "brain/cerebro.html" ]; then
    AGUJA="file://$(pwd)/brain/cerebro.html"
else
    AGUJA="$URL"
fi

YA_ABIERTA=$(osascript - "$AGUJA" <<'FIN' 2>/dev/null
on run argv
	set aguja to item 1 of argv
	if application "Google Chrome" is running then
		tell application "Google Chrome"
			repeat with w in windows
				set i to 0
				repeat with t in tabs of w
					set i to i + 1
					if URL of t starts with aguja then
						set active tab index of w to i
						try
							set index of w to 1
						end try
						activate
						return "si"
					end if
				end repeat
			end repeat
		end tell
	end if
	return "no"
end run
FIN
)

if [ "$YA_ABIERTA" != "si" ]; then
    # Chrome explicito: Safari no reconoce voz y los visores embebidos bloquean el microfono
    open -a "Google Chrome" "$URL" 2>/dev/null || open "$URL"
fi

# La ventana de Terminal se cierra sola
osascript -e 'tell application "Terminal" to close (every window whose name contains "Maximus")' >/dev/null 2>&1 &
exit 0
