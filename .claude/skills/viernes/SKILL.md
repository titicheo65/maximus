---
name: viernes
description: Clasificación semanal de la bitácora de escalamientos de DiMango. Úsala cuando Ricardo diga "el viernes", "clasifiquemos la bitácora", "revisemos los escalamientos", "cierre de semana", "cuántas veces me interrumpieron esta semana", "cómo vamos con la dependencia", o cuando pregunte por el veredicto de T-001 (segundo al mando vs cerrar proyectos). Registra cada escalamiento como nodo E-00X en memoria/, recalcula el porcentaje que decide T-001 y entrega el informe corto.
---

# Ritual del viernes — clasificación de escalamientos

Este es el instrumento de medición del objetivo #1: que DiMango opere sin Ricardo
(D-005). Sin este ritual, "reducir la dependencia" es una intención sin número.

**Fecha de veredicto de T-001: 14 de septiembre de 2026.** Cada viernes hasta esa
fecha acerca o aleja el diagnóstico.

---

## 1 · Reunir la semana

Fuentes, en orden de autoridad:

1. **La planilla** `Bitacora_Escalamientos_DiMango.xlsx`, si Ricardo la entrega o
   indica dónde está. Al 22-ago-2026 **no está en el Mac** — no la busques en
   `~/harvey`, pídesela.
2. **Mensajes de la semana** en el canal de Maximus (Telegram/WhatsApp), donde
   Ricardo va anotando al vuelo.
3. **Entrevista corta**, si no hay ninguna de las dos.

Por cada escalamiento hacen falta seis datos, y solo seis:

| Dato | Ejemplo |
|---|---|
| Quién escaló y desde qué local | Noemi · Playa Chinchorro |
| Qué pedía | autorizar egreso de caja para una encomienda |
| Cuántos minutos le costó a Ricardo | 1 |
| Monto, si había | $10.550 |
| ¿Podía resolverlo otro? | sí, con autoridad |
| Origen | operación normal / proyecto iniciado por Ricardo / falla técnica / cliente |

**Si un dato no está, queda vacío. No lo estimes** — los minutos inventados
contaminan el porcentaje que decide T-001, que es justamente lo único que este
ritual existe para medir.

## 2 · Registrar cada escalamiento en la memoria

Un archivo por escalamiento en `memoria/E-00X.md`, numerando desde el último que
exista. Formato exacto, copiado de `memoria/E-001.md`:

```markdown
---
id: E-00X
tipo: escalamiento
titulo: <Persona> — <qué pedía, en seis palabras>
estado: vigente
fuente: HECHO
autoridad: 4
origen: bitácora de escalamientos
fecha_hecho: AAAA-MM-DD
fecha_registro: AAAA-MM-DD
enlaces:
  evidencia_de: [T-001, D-005]
tags: [bitacora, <categoría>, <local>]
local: Playa Chinchorro | Mall
minutos: <número>
categoria: Finanzas/Pagos | Operación | Personal | Técnico | Proveedores | Cliente
nivel_propuesto: 1 | 2 | 3 | 4
---

<Qué pasó, dos líneas.>

Origen: <origen> · ¿Podía resolverlo otro? <sí/no> ·
Nivel propuesto: <n> (<nombre del nivel>) · Responsable: <cargo>

**Contexto:** <el monto traducido a minutos de venta, si hay monto.>
```

Los cuatro niveles salen de R-002 (marco M5):

1. **Decide y actúa** — no informa
2. **Decide e informa** — actúa y deja registro
3. **Consulta antes** — no actúa sin respuesta
4. **Escala siempre** — nunca decide

Referencia para traducir montos: la venta de DiMango es **~$5,47M al día**,
≈ $7.600 por minuto (ARITMÉTICA, BRAIN.md §1).

Terminado el registro, regenerar índice y visualizador:

```bash
python3 ~/harvey/brain/grafo.py
```

Revisa su salida: si aparecen **enlaces rotos**, apuntaste a una nota que no
existe. Arréglalo antes de seguir.

## 3 · Calcular — los tres números de la semana

1. **Minutos totales** que Ricardo gastó resolviendo cosas de otros.
2. **Reparto por origen**, en % de los minutos. El que importa:
   **"proyecto iniciado por Ricardo"**.
3. **Reparto por nivel propuesto.** Todo lo que caiga en nivel 1 o 2 es trabajo
   que ya podría no estar llegándole.

**Veredicto de T-001, criterio fijado el 19-ago-2026 y no negociable:**

> Si "proyecto iniciado por Ricardo" supera el **40% de los minutos**, gana la
> tesis rival: el problema no es la falta de un segundo al mando, es el exceso de
> proyectos abiertos. La prioridad pasa a cerrar proyectos, y la búsqueda del #2
> se pospone.

Acumula el porcentaje **desde el inicio del registro**, no solo la semana. Una
semana suelta no decide nada; cuatro sí.

## 4 · Proponer regla cuando algo se repite

Si el mismo tipo de escalamiento aparece **dos veces o más**, no se comenta: se
propone una regla. Nota nueva `memoria/R-00X.md`, `tipo: regla`,
`estado: propuesto`, con el umbral concreto y quién queda autorizado. Modelo:
`memoria/R-001.md` (caja chica por local).

Una regla propuesta que Ricardo no aprueba en dos semanas se le vuelve a poner
al frente. No se deja morir en silencio.

## 5 · Entregar el informe

Máximo **seis líneas**, formato de `SOUL.md` — conclusión primero:

```
Semana del <fecha> al <fecha>: <N> escalamientos, <M> minutos.
<El hallazgo que importa, en una línea.>
Origen: <x>% proyectos tuyos · <y>% operación · <z>% técnico.
T-001 acumulado: <p>% (umbral 40%). <Qué significa hoy.>
Regla propuesta: <una, o "ninguna esta semana">.
Lo que haría: <una sola cosa concreta>.
```

## 6 · Cerrar

- Actualiza `MEMORY.md` **solo** si hubo decisión tomada, regla aprobada o
  cambio de prioridad. Un escalamiento registrado no es una decisión.
- Si el veredicto de T-001 se inclinó, dilo aunque falte tiempo para el 14-sep.
  Una tendencia clara vista en agosto vale más que la confirmación en septiembre.

---

## Reglas de este ritual

**Una semana sin datos se reporta como "sin registro", nunca como "cero
escalamientos".** No son lo mismo, y confundirlos es el modo más fácil de que
esta medición diga que todo va bien mientras nadie anota nada. Si pasan dos
semanas sin registro, el problema a levantar no son los escalamientos: es que la
bitácora murió.

**No juzgues a quien escala.** Que Noemi pregunte por $10.550 no es un problema
de Noemi: es que nadie le dijo hasta dónde puede decidir. El objeto de análisis
es la autoridad que falta, no la persona.

**Los minutos son de Ricardo, no del que llamó.** Se mide la interrupción, no la
tarea.
