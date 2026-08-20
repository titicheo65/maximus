#!/usr/bin/env python3
"""
Convierte la memoria monolítica de ~/harvey en notas atómicas.

No borra nada: lee de archivo/ (congelado) y escribe en memoria/.
Cada nota es un .md con frontmatter YAML según el esquema aprobado el 20-ago-2026.

Autoridad de fuente (condición 1 de Ricardo):
  1 sistema oficial · 2 exportación directa · 3 planilla interna
  4 informado por persona · 5 estimación de Maximus
"""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEST = BASE / "memoria"
DEST.mkdir(exist_ok=True)

# (id, tipo, titulo, meta, cuerpo)
NOTAS = [

# ─────────────────────────── DECISIONES ───────────────────────────
("D-001", "decision", "Aurexgroup queda parqueado", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="decisión de Ricardo, entrevista 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19", valido_hasta="2026-11-17",
    enlaces=dict(relacionado=["D-002"], evidencia_de=["H-004"]),
    tags=["aurexgroup", "foco", "parqueado"]),
"""Ricardo decide enfocar 100% en DiMango.

**Maximus está de acuerdo, y se lo gana así:** DiMango es el 100% de la caja y
necesita sumar $430M/año. Aurexgroup no puede financiar eso en 12 meses ni en el
mejor escenario.

**Condición:** parqueado ≠ abandonado. Fecha de revisión obligatoria:
**17 de noviembre de 2026.** Un proyecto sin fecha de revisión está abandonado
con culpa, no parqueado."""),

("D-002", "decision", "Criterio de comercializabilidad de Aurexgroup", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="formulado por Ricardo, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    enlaces=dict(relacionado=["D-001"], aplica_a=["L-002"]),
    tags=["aurexgroup", "producto", "validacion"]),
"""> Problema real detectado en DiMango → solución → validación interna →
> simplificación → **instalación en un negocio externo sin intervención de
> Ricardo** → medición → recién entonces producto validado.

**Regla dura:** una solución solo es producto si un tercero puede instalarla,
operarla y mantenerla **sin depender de Ricardo**. DiMango es laboratorio de
descubrimiento y primera validación, nunca la prueba final."""),

("D-003", "decision", "Meta DiMango: $2.400M anuales", dict(
    estado="en_revision", fuente="HECHO", autoridad=4,
    origen="confirmada por Ricardo, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    enlaces=dict(cuestionada_por=["H-015"], relacionado=["M-005"]),
    tags=["meta", "crecimiento", "facturacion"]),
"""$2.400 millones CLP anuales = **$200 millones/mes**.
Brecha vs. run rate: +$35,87M/mes (+21,9%). Anual: +$430M.

Con dos locales en una ciudad de mercado finito, ese delta solo puede salir de
tres lugares: más transacciones, ticket más alto, o un canal/local nuevo.

**EN REVISIÓN desde el 20-ago-2026 (H-015):** es una meta de *facturación*. Si el
Mall pierde plata y aporta el 25,35% de la venta, crecer en facturación total
empeora el resultado. Debería ser una meta de **margen**."""),

("D-004", "decision", "Orden de las tres decisiones pospuestas", dict(
    estado="vigente", fuente="HECHO", autoridad=5,
    origen="reordenamiento propuesto por Maximus, aceptado 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    enlaces=dict(relacionado=["T-001", "D-005"], superado_parcialmente_por=["D-008"]),
    tags=["prioridades", "delegacion", "tablero"]),
"""Ricardo las listó: 1) salir del centro, 2) arquitectura tecnológica, 3) tablero.

**Maximus las reordena:** el tablero no es tercero, es **condición del primero**.
No se puede delegar lo que no se puede medir; delegar sin métricas es abdicar.

| Decisión | Quién ejecuta | Lead time |
|---|---|---|
| Segundo al mando | Ricardo | 3-6 meses |
| Tablero de gestión | Maximus | 3-4 semanas |
| Arquitectura definitiva | Ricardo + proveedor | 2-3 meses |

**Nota 20-ago:** la arquitectura quedó resuelta de hecho por D-008. Lo que queda
abierto no es *cuál sistema*, sino *cómo no depender de uno solo*."""),

("D-005", "decision", "El objetivo de 90 días necesita ser falsable", dict(
    estado="abierto", fuente="HIPOTESIS", autoridad=5,
    origen="propuesta de Maximus, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    enlaces=dict(medido_por=["E-001"], relacionado=["T-001", "R-002"]),
    tags=["objetivo-90-dias", "dependencia", "bitacora"]),
""""Reducir la dependencia operativa" con ocho subcomponentes es un programa, no
un objetivo. No tiene métrica ni fecha de verificación.

**Propuesta:**
> Del 9 al 15 de noviembre de 2026, DiMango opera 7 días corridos sin que
> Ricardo resuelva una sola decisión operacional.

**Estado:** la bitácora fue ACEPTADA y entregada el 19-ago
(`Bitacora_Escalamientos_DiMango.xlsx`). Primer diagnóstico completo: semana del
14-sep-2026. **La meta de 7 días sigue pendiente de aceptación formal.**"""),

("D-006", "decision", "Tótems bloqueados con Fully Kiosk Browser", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="implementado por Ricardo, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    reverificar_en="2026-08-22",
    enlaces=dict(regulado_por=["D-007"], menciona=["S-001"]),
    tags=["totem", "autoservicio", "kiosko", "sin-verificar"]),
"""**Problema:** niños salían de la app en los tótems. Un tótem fuera de la app
vende cero.
**Diagnóstico:** no se arregla en la app — una PWA no puede impedir la salida.
Es bloqueo a nivel de sistema operativo.
**Solución:** Fully Kiosk Browser sobre Android.

**Estado: implementado, NO verificado bajo carga real.** "Sin errores" no es lo
mismo que probado. Verificar el sábado 22-ago con flujo de niños.

**Pendientes:** confirmar que el auto-reload deja el carrito vacío · el
auto-reload es ciego a los pagos (mitigado con umbral de 120 s; el reset por
código en /Kioskos es la solución correcta) · registro de sesiones abandonadas
no implementado."""),

("D-007", "decision", "Regla de despliegue: sin prueba no hay cierre", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="acordada con Ricardo, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    deriva_de_principio="P5 de MENTORS.md (capa 1, no es nota atómica)",
    enlaces=dict(aplica_a=["D-006", "D-010"], relacionado=["L-005"]),
    tags=["metodo", "despliegue", "verificacion"]),
""""No tuvimos errores" no cuenta como verificación.

Todo cambio en producción necesita una prueba explícita con **criterio de
aprobación fijado de antemano** y una fecha de verificación bajo carga real.
Maximus no cierra un pendiente sin eso."""),

("D-008", "decision", "Migración a DiMangoToGo — Toteat termina el 30-jun-2026", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo",
    fecha_hecho="2026-06-30", valido_desde="2026-07-01",
    enlaces=dict(deriva_en=["P-001", "H-002"], menciona=["S-001", "S-006"], agrava=["L-002"]),
    tags=["toteat", "dimangotogo", "pos", "migracion"]),
"""Desde el 1-jul-2026 DiMango opera 100% sobre DiMangoToGo. Aurexgroup —también
de Ricardo— le factura el servicio: **$1.000.000 en julio**.

**Motivo real (informado por Ricardo, 20-ago):** Toteat era un sistema plano y
**cobraba por ventas**. Ricardo prefiere pagarse a sí mismo y tener un sistema
sólido que controla.

**Lo bueno:** desaparece el problema de dos fuentes de verdad.
**Lo malo:** desaparece la red. Ya no hay sistema alternativo si falla."""),

("D-009", "decision", "Harvey pasa a llamarse Maximus", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="decisión de Ricardo",
    fecha_hecho="2026-08-20", valido_desde="2026-08-20",
    enlaces=dict(relacionado=["D-010"]),
    tags=["maximus", "identidad"]),
"""Cambio aplicado en los siete archivos. La carpeta sigue siendo `~/harvey/`;
renombrarla es opcional."""),

("D-010", "decision", "Maximus se construye sobre el agente de WhatsApp existente", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="repo ~/whatsapp-agentkit + despliegue verificado en ServidorPlaya",
    fecha_hecho="2026-08-20", valido_desde="2026-08-20",
    enlaces=dict(menciona=["S-007", "S-008"], relacionado=["P-008"], regulado_por=["D-007"]),
    tags=["maximus", "whatsapp", "telegram", "fase-1"]),
"""**Objeción original de Maximus, planteada dos veces y retirada** al descubrir
que el canal ya estaba construido: no abre un proyecto nuevo, cierra uno a
medias, y permite capturar la bitácora de escalamientos sin que Ricardo anote.

**FASE 1 APROBADA el 20-ago-2026** con el criterio de D-007: Ricardo preguntó
por WhatsApp desde su celular por el costo laboral de julio y Maximus respondió
$30.271.531 / 45 personas / $36-42M cargado, **etiquetando el estimado como
estimado**. No inventó.

**Canal:** Telegram para Ricardo (Meta no permite iniciar conversación fuera de
la ventana de 24h sin plantilla aprobada, lo que haría imposible el saludo
matutino). WhatsApp para clientes y trabajadores."""),

# ─────────────────────────── HALLAZGOS ───────────────────────────
("H-001", "hallazgo", "Costo de mercadería en 28,7% de la venta neta", dict(
    estado="vigente", fuente="ARITMETICA", autoridad=2,
    origen="RCV de compras del SII, may-jul 2026",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-19",
    valido_desde="2026-05-01", valido_hasta="2026-07-31", reverificar_en="2026-09-15",
    enlaces=dict(limitado_por=["P-005"], relacionado=["M-001", "M-004"]),
    tags=["costo-mercaderia", "prime-cost", "margen"]),
"""Promedio 3 meses: **$39,5M/mes** en alimentos y bebidas = **28,7% de la venta
neta**. Dentro del rango normal de la industria (28-35%). **Ricardo compra bien.**

Se usa el promedio a propósito: el RCV va por fecha de recepción y el mes a mes
oscila artificialmente. Mayo aparece anómalamente bajo.

**Limitación (P-005):** es costo de **compra**, no de **consumo**. Sin inventario
la merma es inmedible, así que el costo real puede ser peor."""),

("H-002", "hallazgo", "El costo de medios de pago saltó con la migración", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="RCV del SII, may-jul 2026",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-19",
    valido_desde="2026-05-01", valido_hasta="2026-07-31", reverificar_en="2026-09-15",
    enlaces=dict(deriva_de=["D-008"], deriva_en=["P-002"], menciona=["S-004", "S-005"]),
    tags=["medios-de-pago", "mercado-pago", "transbank", "costo"]),
"""| | Costo | % venta |
|---|---|---|
| Mayo (Toteat) | $3.347.135 | 1,89% |
| Junio (Toteat) | $1.743.016 | 1,15% |
| **Julio (solo DiMangoToGo)** | **$4.236.597** | **2,59%** |

Pre-migración 1,55% → post 2,59%. **+1,04 puntos = ~$20,5M/año.**
Motor: Mercado Pago $1,73M → $2,40M (+39%) con la venta cayendo 7%.

**HIPÓTESIS:** DiMangoToGo enruta volumen hacia Mercado Pago, que cobra más que
Transbank. La automatización propia estaría subiendo el costo por transacción.

**Caveat:** un solo mes; junio distorsionado porque Transbank no facturó."""),

("H-004", "hallazgo", "Aurexgroup no tiene ingresos externos", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="RCV del SII, julio 2026",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-19",
    enlaces=dict(evidencia_de=["D-002"], relacionado=["D-001"]),
    tags=["aurexgroup", "validacion-externa"]),
"""Su primera y única factura ($1M, julio) es a DiMango.
**Validación externa: cero.** Confirma el criterio de D-002: el único cliente
es Ricardo."""),

("H-008", "hallazgo", "El traspaso entre locales bloquea el margen por local", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_hecho="2026-08-20", fecha_registro="2026-08-20",
    enlaces=dict(bloquea=["H-015"], relacionado=["H-011", "P-007"], menciona=["N-004"]),
    tags=["traspaso", "reposicion", "margen-por-local", "control"]),
"""**Flujo confirmado:** los pedidos se envían todos los días — se despacha desde
**Playa Chinchorro** y se entrega en el **Mall**. El Mall no produce nada.

**Consecuencia:** si el traspaso no se registra valorizado, el costo de
mercadería por local no existe — solo existe la venta por local.

**Son dos controles distintos, no uno:**
1. Pedido del Mall vs venta del Mall — ¿piden de más?
2. Despachado en Playa vs recibido en el Mall — ¿llega todo?

El segundo es el punto de fuga clásico en operaciones de dos locales, y es el
que nadie mira porque "es de la casa"."""),

("H-011", "hallazgo", "Costo laboral de julio 2026 — $30,27M líquido, 45 personas", dict(
    estado="vigente", fuente="HECHO", autoridad=3,
    origen="suelgo_working.xlsx, hojas mar-26 a ago-26, entregado por Ricardo",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-20",
    valido_desde="2026-07-01", valido_hasta="2026-07-31", confianza="media",
    limitacion="pago líquido, sin leyes sociales. Notas 'cash' sugieren pagos fuera de planilla",
    mejorable_con="certificado de cotizaciones Previred julio 2026 (autoridad 1)",
    enlaces=dict(cierra=["P-004"], deriva_en=["H-012"], no_asignable_por=["H-008"],
                 se_consulta_en=["S-002"], relacionado=["M-002", "M-004"]),
    tags=["costo-laboral", "julio-2026", "por-local", "dotacion"]),
"""**Julio 2026: $30.271.531 líquido · 45 personas.**

| Local | Personas | Líquido | % |
|---|---|---|---|
| Playa Chinchorro | 30 | $21.411.531 | 70,7% |
| Mall | 11 | $6.600.000 | 21,8% |
| Ambos | 3 | $2.260.000 | 7,5% |

Por puesto: garzones $7,62M · cocina $6,80M · heladeros $4,69M ·
administración $3,75M · aseo $3,21M · producción $1,95M.

**Verificación:** `quincena + extras + fin de mes = TOTAL2` cuadra en el 100%
de las filas de los tres meses revisados.

**Serie:** junio $25,93M (37) → julio $30,27M (45) → agosto $28,91M (43).

**Alerta:** de junio a julio entraron 8 personas (+21,6%), el costo subió 16,8%
y la venta solo 7,5%. Como % de la venta: 17,0% → **18,5%**.

**Cargado:** Ricardo informó **$37M con imposiciones** (autoridad 4), dentro de
la banda estimada de $36-42M.

**No asignable por local (H-008):** Playa tiene 30 de 45 porque produce para los
dos locales."""),

("H-015", "hallazgo", "Venta de julio por local — el Mall no se sostiene", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="DiMangoToGo /AdminVentas, resumen contable julio filtrado por local",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-20",
    valido_desde="2026-07-01", valido_hasta="2026-07-31",
    verificacion="Playa + Mall cuadra al peso con el consolidado en bruta, c/IVA y neta",
    enlaces=dict(cierra=["P-003"], resuelve=["H-003"], cuestiona=["D-003"],
                 bloqueado_por=["H-008"], se_consulta_en=["S-001"], relacionado=["M-003", "M-006"]),
    tags=["venta-por-local", "mall", "arriendo", "viabilidad", "julio-2026"]),
"""| | Playa | Mall | Total |
|---|---|---|---|
| Venta bruta | $119.455.935 | $40.464.040 | $159.919.975 |
| Venta c/IVA | $119.044.684 | $40.433.220 | $159.477.904 |
| **Venta neta** | **$100.037.550** | **$33.977.496** | $134.015.045 |
| Propinas (aparte) | $7.260.449 | $3.455.478 | $10.715.927 |
| **% del total** | **74,65%** | **25,35%** | 100% |

**Estado de resultados por local (ARITMÉTICA; supone mercadería 28,7% pareja):**

| | Mall | Playa |
|---|---|---|
| Arriendo | **37,4%** | 0% (propio) |
| Mercadería | 28,7% | 28,7% |
| Laboral directo | 19,4% | 21,4% |
| Medios de pago | 2,6% | 2,6% |
| **Queda** | **11,8%** | **47,3%** |

**El arriendo del Mall es 37,4% de su venta neta. El umbral de viabilidad es 20%.**

Y ese 11,8% no descuenta todavía: la mano de obra de Playa que produce para el
Mall (H-008), los 3 empleados "ambos", servicios, gastos comunes ni
administración. **El Mall está en el borde o bajo el agua.**

**Playa subsidia al Mall.** Ya no es hipótesis.

**Para llegar a un arriendo del 20%:** vender $63,6M netos (crecer **87%**) o
renegociar el arriendo a $6,8M (**bajar 47%**). La tercera opción es cerrar.

**Antes de decidir:** leer el contrato de Plaza Oeste — reajuste, componente
variable, vencimiento y multa por salida anticipada."""),

("H-016", "hallazgo", "El campo de costo por producto existe y está vacío", dict(
    estado="vigente", fuente="OBSERVADO", autoridad=2,
    origen="DiMangoToGo /AdminVentas + esquema Product.cost del repo",
    fecha_hecho="2026-08-20", fecha_registro="2026-08-20",
    enlaces=dict(desbloquearia=["M-001"], se_consulta_en=["S-001"], relacionado=["P-005"]),
    tags=["margen", "costo-producto", "quick-win"]),
"""`/AdminVentas` muestra **COSTO NETO: $0**. En el esquema, `Product.cost` existe
y está descrito como *"costo neto unitario del producto (para cálculo de
margen)"*.

**Está construido y nadie lo llenó.**

Cargar los costos daría **margen bruto por producto y por categoría**, calculado
solo, sin inventario y sin contador. Responde la pregunta que nunca se pudo
plantear: cuáles productos ganan plata y cuáles no.

Máximo valor por mínimo esfuerzo de todo lo identificado el 20-ago."""),

# ─────────────────────────── LECCIONES ───────────────────────────
("L-002", "leccion", "La automatización está profundizando el cuello de botella", dict(
    estado="vigente", fuente="HIPOTESIS", autoridad=5,
    origen="lectura de Maximus, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    enlaces=dict(agravado_por=["D-008", "D-010"], relacionado=["D-002", "T-001"]),
    tags=["dependencia", "automatizacion", "cuello-de-botella"]),
"""Cada componente que Ricardo agrega —Base44, DiMangoToGo, DiMangoWorking,
servidor de impresión, tótem, cuatro medios de pago— es una pieza más que
**solo él entiende**. Está reemplazando dependencia de personas por dependencia
de sistemas que dependen de una sola persona.

**Regla derivada:** automatización que solo Ricardo puede mantener no es
automatización, es una dependencia nueva con mejor interfaz. Toda iniciativa
técnica debe pasar el test de D-002."""),

("L-004", "leccion", "La memoria de Maximus tuvo dos fuentes de verdad", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="observado directamente el 20-ago-2026",
    fecha_hecho="2026-08-20", valido_desde="2026-08-20",
    enlaces=dict(relacionado=["D-008", "L-002"]),
    tags=["memoria", "fuente-unica", "git"]),
"""Existían dos `MEMORY.md` divergentes: uno en `~/harvey/` y otro en
`~/Downloads/` (más avanzado). Trabajar sobre el equivocado habría significado
repetir decisiones ya tomadas y perder los hallazgos financieros.

**Es el mismo error que D-008 acaba de eliminar en el POS**, replicado en el
sistema que existe para evitar ese error.

**Regla derivada:** la memoria vive en `~/harvey/`, versionada en git. Los
archivos que salen a otra carpeta son exportaciones de solo lectura y mueren
ahí. Toda sesión arranca con `cd ~/harvey`."""),

("L-005", "leccion", "Un riesgo estimado sin verificar la arquitectura vale tan poco como un número inventado", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="error propio de Maximus, corregido el 20-ago-2026",
    fecha_hecho="2026-08-20", valido_desde="2026-08-20",
    enlaces=dict(deriva_de=["P-001"], relacionado=["D-007"]),
    tags=["error-de-maximus", "metodo", "dte"]),
"""Maximus clasificó la emisión de DTE como **riesgo #1 del negocio a $5,5M/día**,
por encima de todo lo demás, y lo repitió cinco veces.

El número era una construcción propia: asumía que DiMangoToGo emitía por sí
misma y que no había alternativa. La realidad —proveedor certificado, emisión
manual que los encargados saben usar, folios al día, cero fallas en julio— lo
desmintió.

**La estimación tenía autoridad 5 y se presentó con el peso de un hecho.**
Regla: todo riesgo cuantificado debe declarar de qué arquitectura depende, y
verificarla antes de priorizar sobre ella."""),

# ─────────────────────────── TESIS ───────────────────────────
("T-001", "tesis", "No necesita un segundo al mando, necesita cerrar proyectos", dict(
    estado="abierto", fuente="HIPOTESIS", autoridad=5,
    origen="tesis rival planteada por Maximus, 19-ago-2026",
    fecha_hecho="2026-08-19", valido_desde="2026-08-19",
    veredicto_en="2026-09-14",
    criterio="si 'proyecto iniciado por Ricardo' supera el 40% de los minutos de la bitácora, gana la tesis rival",
    enlaces=dict(se_resuelve_con=["E-001", "D-005"], relacionado=["L-002"]),
    tags=["segundo-al-mando", "foco", "wip", "sin-resolver"]),
"""Un observador competente diría que el problema de Ricardo no es falta de
estructura sino exceso de iniciativas simultáneas — él mismo escribió
"probablemente tengo más proyectos de los que debería ejecutar".

Un #2 cuesta $2-3M/mes y tarda 6 meses en ser útil. Cortar la cartera de
proyectos a la mitad es gratis y funciona el lunes siguiente.

**Criterio de veredicto fijado el 19-ago:** si en la bitácora "Proyecto iniciado
por Ricardo" supera el **40% de los minutos**, gana la tesis rival y la prioridad
pasa a cerrar proyectos antes que a buscar un #2."""),

# ─────────────────────────── PERSONAS ───────────────────────────
("N-001", "persona", "Ricardo Vinet", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="entrevista 19-ago-2026",
    valido_desde="2026-08-19",
    roles=[dict(rol="dueño y gerente", empresa="DiMango", desde="?", hasta=None)],
    enlaces=dict(responsable_de=["D-005", "T-001"]),
    tags=["ricardo", "dueño", "cuello-de-botella"]),
"""Empresario, operador y creador de productos tecnológicos. Arica, Chile.
Tres dimensiones simultáneas que exige que Maximus considere siempre.

**Es el cuello de botella identificado de DiMango.** Objetivo #1: que DiMango
opere sin él.

Piensa hablando: sus audios traen más contexto que sus mensajes escritos."""),

("N-002", "persona", "Carla Montoya — contadora externa", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-20", valido_desde="2026-08-20",
    roles=[dict(rol="contadora", empresa="externa", desde="?", hasta=None)],
    enlaces=dict(responsable_de=["P-005"]),
    tags=["contabilidad", "sii", "externo"]),
"""Lleva la contabilidad de DiMango. Servicio externo, se le paga.

**Corrección del 20-ago:** Maximus tenía registrado a Cristian Vidal como el
contador. Era falso — Cristian es programador (N-003). El error contaminó el
análisis durante un día completo.

**Pendiente:** si Ricardo tiene acceso de consulta, y si la contabilidad va
separada por local o consolidada."""),

("N-003", "persona", "Cristian Vidal — programador", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-20", valido_desde="2026-08-20",
    roles=[dict(rol="programador externo", desde="?", hasta=None)],
    enlaces=dict(menciona=["S-009"]),
    tags=["programador", "remuneraciones", "externo"]),
"""Creó el software contable que genera las remuneraciones.

Ricardo planteó reemplazarlo con desarrollo propio. **Clasificado como idea, no
prioridad:** sería otro sistema que solo él mantiene (L-002), para reemplazar
algo que funciona, con cuatro frentes abiertos."""),

("N-004", "persona", "Verónica — reposición y despacho", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-20", valido_desde="2026-08-20",
    roles=[dict(rol="pide reposición del Mall", horario="10:00-11:45 diario", desde="?", hasta=None),
           dict(rol="despacha en Playa", desde="?", hasta=None)],
    enlaces=dict(relacionado=["H-008", "P-007"]),
    tags=["reposicion", "despacho", "control", "separacion-de-funciones"]),
"""**Hace las dos puntas del traspaso:** pide el reabastecimiento del Mall
(10:00-11:45 todos los días) y despacha en Playa.

**Riesgo de control, no acusación:** la misma persona que decide cuánto se manda
confirma cuánto salió. No hay control cruzado. Es el punto de fuga clásico en
operaciones de dos locales."""),

("N-005", "persona", "Quienes reciben en el Mall", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-20", valido_desde="2026-08-20",
    enlaces=dict(relacionado=["H-008", "N-004", "P-007"]),
    tags=["recepcion", "mall", "turnos"]),
"""- **Vivianda** — lunes a viernes
- **Alejandra** o **Angélica** — sábado y domingo
- **Cocinero a cargo del turno AM** — siempre

**Cuatro personas recibiendo, una sola despachando.** La recepción cambia según
el día, lo que dificulta fijar responsabilidad sobre faltantes."""),

# ─────────────────────────── SISTEMAS ───────────────────────────
("S-001", "sistema", "DiMangoToGo", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="repo titicheo65/dimangotogo + uso directo",
    valido_desde="2026-07-01",
    responsable="N-001",
    enlaces=dict(reemplaza=["S-006"], menciona=["S-003"], relacionado=["D-008", "L-002"]),
    tags=["pos", "base44", "fuente-unica", "ventas"]),
"""Plataforma propia sobre Base44: pedidos, atención, caja, pagos, autoservicio.
**Fuente única de venta desde el 1-jul-2026.** 519 archivos.

**Pantallas clave:** `/AdminVentas` (venta por local, medio de pago,
conciliación SII) · `/Caja` · `/Checklist` · `/Kioskos` · `/CierreTurno`.

**Emisión de DTE:** no emite; delega en SimpleFactura (S-003).

**Deuda técnica:** el puente venta↔bodega es matching por **nombre de texto**
(`ReglaInsumo.nombre_en_venta`). Renombrar un producto rompe la conversión en
silencio."""),

("S-002", "sistema", "DiMangoWorking", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="repo titicheo65/dimangoworking",
    responsable="N-001",
    enlaces=dict(relacionado=["L-002", "H-011", "P-007"]),
    tags=["base44", "bodega", "rrhh", "gestion"]),
"""Base44, de Ricardo. 283 archivos. Cuadratura de caja, bodega, remuneraciones,
utilidad.

**Pantallas clave:** `/ChecklistInsumos` (pedido diario, insumos por venta,
vincular bodega, reglas) · `/PlanillaSueldos` · `/GestionFinanciera` (pagos a
proveedores) · `/PedidoProveedor` (stock de proveedores) · `/Inventario`.

**Entidades relevantes:** `ChecklistPedido` (solicitado vs entregado por local y
área), `MermaChecklist` (merma valorizada), `MovimientoStock`, `PlanillaSueldo`
(con campo local: playa/mall/ambos)."""),

("S-003", "sistema", "SimpleFactura", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    valido_desde="2026-07-01",
    enlaces=dict(relacionado=["P-001", "P-009"]),
    tags=["dte", "sii", "boletas", "proveedor-externo"]),
"""Proveedor externo certificado que emite los DTE de DiMango. DiMangoToGo no
emite por sí misma.

**Contingencia:** emisión manual desde la web del proveedor. Los encargados de
ambos locales saben hacerlo — cumple P3 (funciona sin Ricardo).

Folios CAF al día. Cero fallas de emisión en julio."""),

# ─────────────────────────── MÉTRICAS ───────────────────────────
("M-001", "metrica", "Margen bruto", dict(
    estado="desconocido", fuente="HIPOTESIS", autoridad=5,
    enlaces=dict(bloqueado_por=["P-005", "H-016"], relacionado=["H-001"]),
    tags=["margen", "desconocido"]),
"""**Definición:** (venta neta − costo de mercadería consumida) / venta neta.

**Estado: DESCONOCIDO.** Falta el consumo real, no el de compra.

**Se desbloquea con:** cargar `Product.cost` en DiMangoToGo (H-016) o instalar
inventario (P-005). El primero es mucho más barato."""),

("M-003", "metrica", "Arriendo sobre venta neta por local", dict(
    estado="vigente", fuente="ARITMETICA", autoridad=2,
    fecha_hecho="2026-07-31", umbral="20% máximo viable",
    enlaces=dict(deriva_de=["H-015", "H-003"]),
    tags=["arriendo", "viabilidad", "mall"]),
"""**Definición:** arriendo mensual / venta neta del local.
**Umbral de la industria: 20%.** Sobre eso, el local no se sostiene.

| Local | Julio 2026 |
|---|---|
| Mall | **37,4%** |
| Playa | 0% (propio) |"""),

("M-004", "metrica", "Prime cost", dict(
    estado="vigente", fuente="ARITMETICA", autoridad=3,
    fecha_hecho="2026-07-31", umbral="60-65% máximo",
    enlaces=dict(deriva_de=["H-001", "H-011"]),
    tags=["prime-cost", "margen", "industria"]),
"""**Definición:** (insumos + mano de obra) / venta neta. Es *el* número con el
que se administra un restaurante. Sobre 60-65%, crecer en volumen empeora el
resultado.

**Julio 2026: ≈57,7%** — mercadería 28,7% + laboral cargado ~29%.
**Está sano.**

*Nota: Ricardo no conocía el término al 20-ago-2026, aunque está en MENTORS.md
como marco aprobado (M4). Maximus lo usó sin explicarlo.*"""),

("M-006", "metrica", "Ticket promedio por local", dict(
    estado="parcial", fuente="ARITMETICA", autoridad=3,
    fecha_hecho="2026-07-31",
    enlaces=dict(deriva_de=["H-015"], se_consulta_en=["S-001"]),
    tags=["ticket", "por-local", "palanca"]),
"""Estimado desde la conciliación parcial de julio:
- **Playa: ~$14.845**
- **Mall: ~$19.491** (Ricardo estimó ~$18.000 de memoria — coherente)

**El Mall tiene mejor ticket que Playa (+31%).** Su problema no es el ticket:
es el volumen contra un arriendo desproporcionado.

**Pendiente:** número exacto de transacciones por local desde `/AdminVentas`."""),
]


FRONT_ORDEN = ["tipo", "titulo", "estado", "fuente", "autoridad", "origen",
               "fecha_hecho", "fecha_registro", "valido_desde", "valido_hasta",
               "confianza", "limitacion", "mejorable_con", "reverificar_en",
               "umbral", "criterio", "veredicto_en", "verificacion",
               "responsable", "roles", "enlaces", "tags"]


def yaml_valor(v, indent=0):
    sp = "  " * indent
    if isinstance(v, dict):
        return "\n" + "\n".join(f"{sp}  {k}: {yaml_valor(x, indent + 1).lstrip()}"
                                for k, x in v.items())
    if isinstance(v, list):
        if v and isinstance(v[0], dict):
            return "\n" + "\n".join(
                f"{sp}  - " + ", ".join(f"{k}: {x}" for k, x in d.items()) for d in v)
        return "[" + ", ".join(str(x) for x in v) + "]"
    if v is None:
        return "null"
    return f'"{v}"' if isinstance(v, str) and (":" in v or "," in v) else str(v)


def escribir(nid, tipo, titulo, meta, cuerpo):
    m = dict(meta)
    m["tipo"] = tipo
    m["titulo"] = titulo
    m.setdefault("fecha_registro", "2026-08-20")

    lineas = [f"id: {nid}"]
    for k in FRONT_ORDEN:
        if k in m:
            lineas.append(f"{k}: {yaml_valor(m[k])}")
    for k in m:
        if k not in FRONT_ORDEN:
            lineas.append(f"{k}: {yaml_valor(m[k])}")

    texto = "---\n" + "\n".join(lineas) + "\n---\n\n" + cuerpo.strip() + "\n"
    (DEST / f"{nid}.md").write_text(texto, encoding="utf-8")
    return len(texto)


if __name__ == "__main__":
    total = 0
    por_tipo = {}
    for nid, tipo, titulo, meta, cuerpo in NOTAS:
        total += escribir(nid, tipo, titulo, meta, cuerpo)
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    print(f"{len(NOTAS)} notas escritas en {DEST} ({total:,} caracteres)")
    for t, n in sorted(por_tipo.items(), key=lambda x: -x[1]):
        print(f"  {t:12} {n}")
