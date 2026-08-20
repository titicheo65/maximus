#!/usr/bin/env python3
"""
Banco de pruebas de la migración.

Corre las 25 preguntas congeladas contra las DOS memorias y compara:
  A) memoria vieja  — los seis archivos completos en el system prompt
  B) memoria nueva  — core + índice + recuperación selectiva

Mide para cada una: tiempo al primer token, tokens de entrada, y guarda las dos
respuestas lado a lado para revisión humana.

Criterio de aprobación fijado ANTES de correr (D-007):
  · 0 pérdidas de información en las 25
  · primer token bajo 800 ms en la memoria nueva
  · Ricardo revisa al menos 5 comparaciones y da el visto bueno
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recuperar import Cerebro                                   # noqa: E402

from anthropic import AsyncAnthropic                            # noqa: E402
from dotenv import load_dotenv                                  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
load_dotenv(Path.home() / "whatsapp-agentkit" / ".env")

MODELO = os.getenv("MAXIMUS_MODEL", "claude-opus-4-5")
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

ARCHIVOS_VIEJOS = ["IDENTITY.md", "SOUL.md", "USER.md", "BRAIN.md", "MEMORY.md", "MENTORS.md"]

INSTRUCCION = """
Responde como Maximus, en español, breve y directo. Conclusión primero.
Si el dato no está en tu memoria, dilo y señala dónde debería consultarse.
Si hay una contradicción entre notas, decláralo en vez de elegir en silencio.
Nunca inventes un número.
""".strip()

# ── LAS 25 PREGUNTAS CONGELADAS ──
# 15 de Maximus (prueba sistemática) + 10 de Ricardo (uso real)
PREGUNTAS = [
    # -- recuperación directa --
    ("M01", "recuperacion", "¿Cuánto fue el costo laboral de julio y cómo se reparte por local?"),
    ("M02", "recuperacion", "¿Cuál es el prime cost y qué significa que esté donde está?"),
    ("M03", "recuperacion", "¿Qué pasó con Toteat y desde cuándo?"),
    # -- conectar varias notas --
    ("M04", "conexion", "¿Por qué no podemos saber si el local del Mall es rentable?"),
    ("M05", "conexion", "¿Qué relación hay entre la migración a DiMangoToGo y el aumento del costo de medios de pago?"),
    ("M06", "conexion", "Si cerráramos el Mall, ¿qué pasaría con el costo laboral de Playa?"),
    ("M07", "conexion", "¿Qué tendría que pasar para que Aurexgroup deje de estar parqueado?"),
    # -- contradicción o límite --
    ("M08", "contradiccion", "El residual del estado de resultados da 26% de margen. ¿Es creíble? ¿Por qué?"),
    ("M09", "contradiccion", "¿En qué se equivocó Maximus sobre el riesgo del DTE y por qué?"),
    ("M10", "contradiccion", "¿El costo de mercadería de 28,7% es el costo real de lo que se consume?"),
    # -- histórico vs vivo, fuentes --
    ("M11", "fuente", "¿Cuánto vendimos hoy?"),
    ("M12", "fuente", "¿Cuál es el dato más confiable que tenemos del costo laboral y cuál sería mejor?"),
    ("M13", "fuente", "¿La venta de julio fue $163.552.687? ¿Ese número cambia con el tiempo?"),
    # -- personas --
    ("M14", "persona", "¿Quién es Cristian Vidal, qué hace y qué pendiente se relaciona con él?"),
    # -- reconocer que no sabe --
    ("M15", "no_sabe", "¿Cuál es el margen bruto real por producto?"),

    # ── las 10 de Ricardo, tal como las diría ──
    ("R01", "ricardo", "¿Cuántos km de trote o bicicleta debo hacer hoy?"),
    ("R02", "ricardo", "¿Qué pagos de proveedores tengo esta semana?"),
    ("R03", "ricardo", "¿Cómo está el stock de PF y Biofood?"),
    ("R04", "ricardo", "¿Qué pasó anoche en el Mall y quién estaba al tanto?"),
    ("R05", "ricardo", "¿Me consultaron antes de tomar esa decisión?"),
    ("R06", "ricardo", "¿Cuánto vendió el Mall en julio y cuál es su ticket promedio?"),
    ("R07", "ricardo", "¿El Mall conviene o lo cierro?"),
    ("R08", "ricardo", "¿Quién hace la reposición del Mall y quién la recibe?"),
    ("R09", "ricardo", "¿Cuánto me cuesta tener 45 personas y cuánto subió respecto a junio?"),
    ("R10", "ricardo", "¿Qué es lo más urgente que tengo pendiente hoy?"),
]


def memoria_vieja() -> str:
    partes = []
    for f in ARCHIVOS_VIEJOS:
        p = BASE / f
        if p.exists():
            partes.append(f"===== {f} =====\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(partes)


async def preguntar(fija: str, pregunta: str, variable: str = ""):
    """
    `fija` va con cache_control: es el prefijo estable y se cachea.
    `variable` va después, sin cache: cambia con cada pregunta.
    """
    bloques = [{"type": "text", "text": fija + "\n\n" + INSTRUCCION,
                "cache_control": {"type": "ephemeral"}}]
    if variable:
        bloques.append({"type": "text", "text": variable})

    t0 = time.time()
    primer = None
    texto = []
    async with client.messages.stream(model=MODELO, max_tokens=700, system=bloques,
                                      messages=[{"role": "user", "content": pregunta}]) as s:
        async for chunk in s.text_stream:
            if primer is None:
                primer = time.time() - t0
            texto.append(chunk)
        msg = await s.get_final_message()
    u = msg.usage
    leido = getattr(u, "cache_read_input_tokens", 0) or 0
    creado = getattr(u, "cache_creation_input_tokens", 0) or 0
    return {
        "respuesta": "".join(texto).strip(),
        "ttft_ms": round((primer or 0) * 1000),
        "total_ms": round((time.time() - t0) * 1000),
        "tokens_in": u.input_tokens + leido + creado,
        "cache_leido": leido,
        "sin_cache": u.input_tokens,
        "tokens_out": u.output_tokens,
    }


async def main():
    cerebro = Cerebro()
    viejo = memoria_vieja()
    print(f"modelo: {MODELO}")
    print(f"memoria vieja: {len(viejo):,} caracteres\n")

    # calentar los dos caches para que ninguna memoria salga castigada
    fija0, var0, _ = cerebro.contexto("hola")
    await preguntar(viejo, "hola")
    await preguntar(fija0, "hola", var0)

    resultados = []
    for pid, cat, q in PREGUNTAS:
        fija, variable, ids = cerebro.contexto(q)
        a, b = await asyncio.gather(preguntar(viejo, q), preguntar(fija, q, variable))
        resultados.append({"id": pid, "categoria": cat, "pregunta": q,
                           "notas_recuperadas": ids, "vieja": a, "nueva": b})
        print(f"{pid} [{cat:13}] vieja {a['ttft_ms']:5}ms {a['tokens_in']:6,}tok  "
              f"nueva {b['ttft_ms']:5}ms {b['tokens_in']:6,}tok "
              f"(cache {b['cache_leido']:,}) {len(ids)}n")

    (BASE / "brain" / "evaluacion.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=1), encoding="utf-8")

    v = [r["vieja"] for r in resultados]
    n = [r["nueva"] for r in resultados]
    print("\n" + "=" * 68)
    print(f"{'':22}{'VIEJA':>14}{'NUEVA':>14}{'':>10}")
    for etq, k in [("primer token (ms)", "ttft_ms"), ("tokens de entrada", "tokens_in")]:
        pv = sum(x[k] for x in v) / len(v)
        pn = sum(x[k] for x in n) / len(n)
        print(f"{etq:22}{pv:>14,.0f}{pn:>14,.0f}{(pn/pv-1)*100:>9.0f}%")
    bajo800 = sum(1 for x in n if x["ttft_ms"] < 800)
    print(f"\nrespuestas nuevas bajo 800 ms: {bajo800}/{len(n)}")
    print("comparación completa en brain/evaluacion.json")


if __name__ == "__main__":
    asyncio.run(main())
