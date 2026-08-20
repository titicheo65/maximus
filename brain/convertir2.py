#!/usr/bin/env python3
"""Segunda tanda: pendientes, sistemas, métricas, reglas y escalamientos."""

from convertir import escribir

NOTAS = [

# ─────────────────────────── PENDIENTES ───────────────────────────
("P-001", "pendiente", "Contingencia de emisión de DTE", dict(
    estado="cerrado", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-19", cerrado_en="2026-08-20",
    enlaces=dict(agravado_por=["D-008"], menciona=["S-001", "S-003"],
                 deriva_en=["P-009", "L-005"]),
    tags=["dte", "sii", "contingencia", "riesgo", "cerrado"]),
"""**Respuestas de Ricardo:**
- DiMangoToGo **no emite**: emite **SimpleFactura**, proveedor certificado.
- Contingencia: emisión manual desde la web del proveedor.
- Folios CAF al día. **Cero fallas de emisión en julio.**
- **Los encargados de ambos locales saben emitir manual** → cumple P3.

**Error de Maximus, conservado a propósito:** se clasificó como riesgo #1 del
negocio a $5,5M/día, y se repitió cinco veces. Ese número asumía que DiMangoToGo
emitía por sí misma y que no había alternativa. Era una construcción propia
(autoridad 5) presentada con el peso de un hecho. Ver L-005."""),

("P-002", "pendiente", "Comparar comisión efectiva Mercado Pago vs Transbank", dict(
    estado="abierto", fuente="ARITMETICA", autoridad=2,
    origen="derivado de H-002", fecha_registro="2026-08-19",
    valor_en_juego="$20.500.000 al año", esfuerzo="una tarde",
    enlaces=dict(deriva_de=["H-002"], menciona=["S-004", "S-005"]),
    tags=["medios-de-pago", "costo", "quick-win"]),
"""Vale ~$20,5M al año. Una tarde de trabajo.

La hipótesis de H-002 es que DiMangoToGo enruta volumen hacia Mercado Pago, que
cobra más que Transbank. Si se confirma, se corrige cambiando el orden de
preferencia de medios de pago en la app."""),

("P-003", "pendiente", "Venta de julio por local", dict(
    estado="cerrado", fuente="HECHO", autoridad=2,
    origen="DiMangoToGo /AdminVentas", fecha_registro="2026-08-19",
    cerrado_en="2026-08-20", cerrado_por=["H-015"],
    enlaces=dict(cerrado_por=["H-015"], se_consulta_en=["S-001"]),
    tags=["venta-por-local", "cerrado"]),
"""Cerrado el 20-ago-2026 con H-015.

**Lección de proceso:** el dato estuvo disponible en `/AdminVentas` todo el
tiempo. Fue prioridad #1 durante tres días mientras estaba a un clic. Nadie
preguntó dónde vivía el dato antes de declararlo desconocido."""),

("P-004", "pendiente", "Costo laboral de julio", dict(
    estado="cerrado", fuente="HECHO", autoridad=3,
    origen="planilla de Ricardo", fecha_registro="2026-08-19",
    cerrado_en="2026-08-20",
    enlaces=dict(cerrado_por=["H-011"]),
    tags=["costo-laboral", "cerrado"]),
"""Cerrado con H-011. Era el indicador más caro de la lista: una banda de
incertidumbre de $18M/mes.

**Sigue mejorable:** el dato es de autoridad 3 (planilla interna, pago líquido).
Previred daría autoridad 1 y el costo cargado real."""),

("P-005", "pendiente", "Inventario — decidir si se instala", dict(
    estado="abierto", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026", fecha_registro="2026-08-20",
    enlaces=dict(bloquea=["M-001"], limita=["H-001"], relacionado=["H-016", "P-007"]),
    tags=["inventario", "merma", "margen-bruto"]),
"""**No existe sistema central de inventario.** Consecuencia directa: compras ≠
consumo, la merma es inmedible, y el 28,7% de H-001 es costo de *compra*, no de
*consumo*.

**Alternativa más barata (H-016):** cargar `Product.cost` en DiMangoToGo da
margen bruto por producto sin instalar inventario. No mide merma, pero responde
la pregunta más útil primero."""),

("P-006", "pendiente", "Arriendo de Playa Chinchorro", dict(
    estado="cerrado", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    fecha_registro="2026-08-20", cerrado_en="2026-08-20",
    enlaces=dict(deriva_de=["H-012"], relacionado=["H-015", "M-003"]),
    tags=["arriendo", "playa", "cerrado"]),
"""**Playa Chinchorro es propiedad de Ricardo, ya pagada. No paga arriendo.**

Descarta el candidato #1 para explicar el residual de H-012, y obliga a corregir
el benchmark: el margen típico de 3-8% en gastronomía asume que el operador
arrienda **ambos** locales. Sin arriendo en el local principal, el margen
legítimo de DiMango es estructuralmente más alto.

**Efecto colateral sobre H-015:** al comparar Playa con el Mall hay que imputar
un arriendo de mercado a Playa. Si no, Playa gana por estar mejor dotado, no por
estar mejor operado."""),

("P-007", "pendiente", "Control de reposiciones: cruzar pedido con venta", dict(
    estado="abierto", fuente="HECHO", autoridad=2,
    origen="pedido explícito de Ricardo + auditoría del código",
    fecha_registro="2026-08-20", prioridad="alta",
    enlaces=dict(deriva_de=["H-008"], menciona=["S-001", "S-002", "N-004", "N-005"],
                 desbloquearia=["M-001"]),
    tags=["reposicion", "control", "merma", "traspaso"]),
"""**El caso que planteó Ricardo:** se venden 10 Coca-Colas, reponen 12 → alerta.

**Lo que ya existe:**
- Venta del día anterior: correo automático a la 1:30 AM
- `ChecklistPedido`: cantidad solicitada vs entregada, por local y área
- `ReglaInsumo`: convierte producto vendido → insumo

**Lo único que falta:** que al cargar el pedido aparezca al lado lo que se vendió.
Los dos datos están sobre la mesa a la misma hora y nadie los junta.

**Riesgo previo a medir:** el puente venta↔bodega es matching por **nombre de
texto**. Antes de construir cualquier alerta hay que medir qué % de los productos
vendidos tiene una `ReglaInsumo` que los cubra. Si es 60%, la alerta miente en el
40% restante y se ignora en dos semanas.

**Control de personas (N-004):** Verónica pide y despacha. Sin separación de
funciones, el control técnico no cambia nada."""),

("P-008", "pendiente", "Infraestructura de Maximus en ServidorPlaya", dict(
    estado="abierto", fuente="OBSERVADO", autoridad=2,
    origen="despliegue del 20-ago-2026", fecha_registro="2026-08-20",
    enlaces=dict(deriva_de=["D-010"], menciona=["S-008"], relacionado=["L-002"]),
    tags=["infraestructura", "servidorplaya", "riesgo"]),
"""1. **Nada arranca solo.** Si se reinicia ese Windows, ni el agente ni ngrok
   vuelven. Se resuelve con tarea programada al inicio.
2. **La memoria del servidor no se actualiza sola.** `C:\\maximus` es un clon:
   sin `git pull` periódico, Maximus se congela en el 20 de agosto y responde
   datos viejos con seguridad — peor que no tenerlo.
3. **Telegram sin token válido.** El webhook devolvió 404.
4. **Cinco copias muertas** del proyecto en el servidor, pendientes de archivar.
5. **Todo pasa por un túnel ngrok gratuito.** Si cae, el webhook de WhatsApp deja
   de recibir mensajes de clientes y nadie se entera."""),

("P-009", "pendiente", "Riesgo residual de emisión: internet", dict(
    estado="abierto", fuente="ARITMETICA", autoridad=4,
    origen="derivado de P-001", fecha_registro="2026-08-20",
    enlaces=dict(deriva_de=["P-001"], menciona=["S-003"]),
    tags=["dte", "internet", "contingencia"]),
"""El punto único ya no es DiMangoToGo: son **SimpleFactura e internet**.

Las dos vías de emisión —la app y la web del proveedor— requieren conexión. En
Chile la boleta es 100% electrónica: el talonario timbrado ya no existe como
contingencia.

**Pregunta abierta para el proveedor, sin urgencia:** ¿SimpleFactura **encola**
las boletas si cae internet y las timbra al recuperar conexión? El SII contempla
ese modo, pero hay que confirmar si el software lo implementa o simplemente
falla."""),

# ─────────────────────────── SISTEMAS ───────────────────────────
("S-004", "sistema", "Mercado Pago", dict(
    estado="vigente", fuente="HECHO", autoridad=2, origen="RCV del SII",
    enlaces=dict(relacionado=["H-002", "P-002"]),
    tags=["medios-de-pago", "comision"]),
"""Medio de pago. **Julio: $2,40M de comisión, +39% vs junio con la venta
cayendo 7%.** Es el motor del alza de H-002.

Hipótesis abierta: DiMangoToGo enruta volumen hacia acá y cobra más que
Transbank."""),

("S-005", "sistema", "Transbank", dict(
    estado="vigente", fuente="HECHO", autoridad=2, origen="RCV del SII",
    enlaces=dict(relacionado=["H-002", "P-002"]),
    tags=["medios-de-pago", "pos-fisico"]),
"""POS físicos, equipos nuevos en implementación durante agosto 2026.
En junio no facturó, lo que distorsiona la comparación de H-002."""),

("S-006", "sistema", "Toteat", dict(
    estado="superado", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo",
    valido_desde="?", valido_hasta="2026-06-30",
    enlaces=dict(reemplazado_por=["S-001"], relacionado=["D-008"]),
    tags=["pos", "historico", "terminado"]),
"""POS anterior. **Terminado el 30-jun-2026.**

Costaba ~$148.031/mes. **Cobraba por ventas**, que fue el motivo real de la
salida según Ricardo: prefiere pagarse a sí mismo y controlar el sistema.

Su desaparición es lo que dejó al negocio sin red de respaldo (D-008)."""),

("S-007", "sistema", "Agente de WhatsApp / Telegram", dict(
    estado="vigente", fuente="HECHO", autoridad=2,
    origen="repo titicheo65/dimango-agent", valido_desde="2026-08-20",
    responsable="N-001",
    enlaces=dict(relacionado=["D-010", "P-008"], corre_en=["S-008"]),
    tags=["maximus", "whatsapp", "telegram", "agente"]),
"""FastAPI en Python. Proveedor Meta (número local chileno). Transcribe notas de
voz con Groq Whisper. Corre en `C:\\dimango-agent`, puerto 8000.

**Dos roles sobre el mismo canal:** atención al cliente (reservas, pedidos,
tickets) y Maximus (gestión, memoria completa, solo para el número de Ricardo).
Ambos fallan cerrado: sin variables configuradas, se comporta como siempre.

**Módulos:** `maximus.py`, `telegram_maximus.py`, `voz.py` (edge-tts con voz
chilena, ElevenLabs opcional), `colacion.py`."""),

("S-008", "sistema", "ServidorPlaya", dict(
    estado="vigente", fuente="OBSERVADO", autoridad=2,
    origen="inspección directa, 20-ago-2026", responsable="N-001",
    enlaces=dict(relacionado=["P-008", "L-002"]),
    tags=["infraestructura", "windows", "ngrok", "riesgo"]),
"""Windows en el local de Playa Chinchorro. Se accede por AnyDesk/Splashtop.

**Tres servicios y tres túneles ngrok** (tope del plan Hobbyist):

| Puerto | Servicio | Túnel |
|---|---|---|
| 8000 | agente WhatsApp | oak-cornea-marlin.ngrok-free.dev |
| 8001 | `functions.main` (voiceagentkit) | voiceagentkit.ngrok.app |
| 3003 | — | dimango.ngrok.app |

**Riesgo estructural:** si se corta la luz o internet en Playa, se caen el agente
de clientes y Maximus. Nada arranca solo."""),

("S-009", "sistema", "Software de remuneraciones", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026",
    enlaces=dict(responsable=["N-003"], relacionado=["H-011"]),
    tags=["remuneraciones", "rrhh", "externo"]),
"""Software contable que genera las remuneraciones, creado por Cristian Vidal
(N-003).

Ricardo planteó reemplazarlo con desarrollo propio. **Clasificado como idea, no
prioridad:** L-002 puro — otro sistema que solo él mantendría, para reemplazar
algo que funciona, con cuatro frentes abiertos."""),

# ─────────────────────────── HALLAZGOS QUE FALTABAN ───────────────────────────
("H-003", "hallazgo", "Arriendo Plaza Oeste — el mayor costo después de la comida", dict(
    estado="vigente", fuente="HECHO", autoridad=2, origen="RCV del SII",
    fecha_hecho="2026-07-31", valido_desde="2026-05-01", valido_hasta="2026-07-31",
    enlaces=dict(resuelto_por=["H-015"], relacionado=["M-003", "P-006"]),
    tags=["arriendo", "mall", "costo-fijo"]),
"""Mayo $11.874.572 · Junio $11.842.204 · **Julio $12.721.588 (+7,1%)** — sube
mientras la venta cae 7,4%.

**Resuelto por H-015:** el Mall hace el 25,35% de la venta, no la mitad. El
arriendo es el **37,4% de su venta neta**, casi el doble del umbral viable.

**Pendiente:** leer el contrato — reajuste, componente variable, vencimiento y
multa por salida anticipada."""),

("H-006", "hallazgo", "Estructura de costos conocidos", dict(
    estado="vigente", fuente="ARITMETICA", autoridad=2, origen="RCV del SII",
    fecha_hecho="2026-07-31",
    enlaces=dict(deriva_en=["H-012"], relacionado=["H-001", "H-003"]),
    tags=["costos", "estado-de-resultados"]),
"""Costos conocidos ≈ **$62M/mes** contra venta neta de julio.

Incluye: mercadería (~$39,5M), arriendo del Mall ($12,7M), medios de pago
($4,2M), delivery (~$1,5M), tabaco, servicios y seguros (~11% de la venta
incluyendo arriendo).

**No incluye:** costo laboral (no llega con factura, no está en el RCV),
honorarios, contribuciones ni impuestos."""),

("H-012", "hallazgo", "El residual del estado de resultados no cuadra", dict(
    estado="conflicto", fuente="ARITMETICA", autoridad=5,
    origen="cálculo de Maximus sobre H-006 + H-011",
    fecha_hecho="2026-07-31", fecha_registro="2026-08-20",
    enlaces=dict(deriva_de=["H-006", "H-011"], contradice=["H-017"],
                 relacionado=["P-006", "M-005"]),
    tags=["margen-neto", "residual", "conflicto", "sin-resolver"]),
"""| Concepto | Monto/mes |
|---|---|
| Venta neta (julio) | $134,0M |
| Costos conocidos (H-006) | −$62M |
| Costo laboral cargado | −$37M |
| **Residual sin identificar** | **≈$35M — 26% de la venta** |

**CONFLICTO ABIERTO.** Ricardo afirma (autoridad 4) que ese 26% es utilidad real.
Maximus estimó (autoridad 5) que falta costo por capturar. Por la regla de
prioridad de fuentes gana Ricardo — pero la regla de conflictos exige no
resolverlo en silencio.

**Se cierra con autoridad 1:** el saldo bancario al 1 y al 31 de julio. Si la
caja creció ~$35M, es utilidad. Si no creció, hay costo que no estamos viendo.

**Matiz de P-006:** con Playa sin arriendo, el margen legítimo de DiMango es más
alto que el benchmark de la industria. Eso achica la anomalía, no la elimina.

**Estado: Ricardo decidió no priorizar los saldos bancarios el 20-ago.**"""),

("H-013", "hallazgo", "El código de producción no tenía repositorio propio", dict(
    estado="cerrado", fuente="OBSERVADO", autoridad=2,
    origen="inspección de ~/whatsapp-agentkit", fecha_hecho="2026-08-20",
    cerrado_en="2026-08-20",
    enlaces=dict(relacionado=["L-002", "L-004", "S-007"]),
    tags=["respaldo", "git", "riesgo", "cerrado"]),
"""El remote apuntaba a `github.com/Hainrixz/whatsapp-agentkit` — el repo del autor
del AgentKit, no de Ricardo. Estado: **ahead 3, behind 2**.

Los tres commits propios —agente DiMango, automatización de venta al Mallplaza,
control de colación— existían **solo en el Mac y en ServidorPlaya**.

**Resuelto:** creados `titicheo65/maximus` (memoria) y `titicheo65/dimango-agent`
(código), ambos privados. Verificado que no se subió ningún `.env`, `.db`,
cuadrante de personal ni RCV del SII."""),

("H-014", "hallazgo", "Credenciales de Twilio expuestas en un archivo local", dict(
    estado="abierto", fuente="HECHO", autoridad=1,
    origen="push protection de GitHub", fecha_hecho="2026-08-20",
    enlaces=dict(relacionado=["H-013", "S-007"]),
    tags=["seguridad", "credenciales", "twilio", "pendiente"]),
"""GitHub bloqueó un push: Account SID y API Key de Twilio en texto plano dentro
de `.claude/settings.local.json`.

**No llegaron al repositorio.** El archivo quedó en `.gitignore`.

**Pendiente:** las credenciales **siguen en el disco del Mac**. Riesgo bajo hoy
porque el agente migró a Meta y Twilio ya no se usa, pero deben **rotarse o
eliminarse en el panel de Twilio** — borrarlas del archivo no las desactiva."""),

("H-017", "hallazgo", "Ricardo afirma que el margen de 26% es real", dict(
    estado="conflicto", fuente="HECHO", autoridad=4,
    origen="informado por Ricardo, 20-ago-2026", fecha_registro="2026-08-20",
    enlaces=dict(contradice=["H-012"], se_resuelve_con=["M-005"]),
    tags=["margen-neto", "conflicto", "utilidad"]),
"""Ante la pregunta de si el residual de 26% era creíble, Ricardo respondió:
*"sí es creíble, es un poco lo que estamos manejando de ganancia"*.

**Autoridad 4** (informado por persona) contra la estimación de Maximus
(autoridad 5). Por la regla de prioridad de fuentes, esta nota gana.

**Pero no cierra el conflicto:** se necesita autoridad 1 (movimiento bancario de
julio) para confirmarlo. Mientras tanto, ambas notas quedan en `conflicto` y
Maximus debe declararlo cuando el tema aparezca."""),

# ─────────────────────────── LECCIONES ───────────────────────────
("L-001", "leccion", "DiMango no estaba instrumentado — parcialmente refutada", dict(
    estado="superado", fuente="HECHO", autoridad=2,
    origen="diagnóstico 19-ago, corregido 20-ago",
    fecha_hecho="2026-08-19", valido_hasta="2026-08-20",
    enlaces=dict(relacionado=["H-001", "P-003"]),
    tags=["ceguera", "instrumentacion", "refutada"]),
"""Cinco de seis preguntas financieras fundamentales sobre un negocio de ~$2.000
millones/año: "no lo sé". El diagnóstico fue **ceguera**, no falta de datos.

**Refutada en su parte pesimista el 20-ago:** el RCV del SII entregó seis
hallazgos en un día, y la venta por local estaba en `/AdminVentas` todo el
tiempo. **El dato no faltaba: nadie había preguntado dónde vivía.**

**Regla derivada:** antes de declarar un indicador desconocido, preguntar qué
sistema debería tenerlo."""),

("L-003", "leccion", "No se puede justificar automatización sin conocer el costo que ahorra", dict(
    estado="vigente", fuente="HIPOTESIS", autoridad=5,
    origen="lectura de Maximus, 19-ago-2026", fecha_hecho="2026-08-19",
    enlaces=dict(relacionado=["D-006", "L-002", "M-002"]),
    tags=["automatizacion", "roi", "totem"]),
"""Tótems, autoservicio y reducción de cajas se justifican con un ahorro de costo
laboral que era inmedible.

**Parcialmente resuelto:** con H-011 ya existe el costo laboral por local y por
puesto. Ahora sí se puede medir si un tótem ahorró o costó.

Y sin ese número, Aurexgroup tampoco tiene caso de venta: no se puede vender un
ROI que no se midió en el propio laboratorio."""),

# ─────────────────────────── MÉTRICAS ───────────────────────────
("M-002", "metrica", "Costo laboral sobre venta neta", dict(
    estado="vigente", fuente="ARITMETICA", autoridad=3,
    fecha_hecho="2026-07-31", umbral="referencia: 25-35% en full-service",
    enlaces=dict(deriva_de=["H-011"], relacionado=["M-004", "L-003"]),
    tags=["costo-laboral", "dotacion"]),
"""**Definición:** costo laboral cargado / venta neta.

| Mes | Personas | Líquido / venta |
|---|---|---|
| Junio | 37 | 17,0% |
| Julio | 45 | **18,5%** |

**Alerta vigente:** +8 personas en un mes (+21,6%) con la venta subiendo 7,5%.
Nadie tomó esa decisión mirando este número."""),

("M-005", "metrica", "Margen neto", dict(
    estado="conflicto", fuente="ARITMETICA", autoridad=5,
    umbral="3-8% típico en full-service; más alto si no se arrienda",
    enlaces=dict(bloqueado_por=["H-012", "H-017"], relacionado=["D-003"]),
    tags=["margen-neto", "conflicto", "desconocido"]),
"""**Definición:** utilidad después de todos los costos / venta neta.

**Estado: EN CONFLICTO.** El residual da 26%; Ricardo afirma que es real;
Maximus estima que falta costo. Ver H-012 y H-017.

**Se resuelve con:** movimiento bancario de julio (autoridad 1).

**Por qué importa más que la venta:** D-003 es una meta de facturación. Si el
Mall pierde plata (H-015), crecer en venta total empeora el margen."""),

# ─────────────────────────── REGLAS ───────────────────────────
("R-001", "regla", "Caja chica por local — propuesta", dict(
    estado="propuesto", fuente="HIPOTESIS", autoridad=5,
    origen="propuesta de Maximus a partir de E-001", fecha_registro="2026-08-19",
    enlaces=dict(deriva_de=["E-001"], relacionado=["R-002", "D-005"]),
    tags=["delegacion", "caja", "autoridad", "pendiente-de-aprobacion"]),
"""**Propuesta, pendiente de aprobación:**
- El encargado autoriza egresos de caja hasta **$50.000 por egreso** y
  **$200.000 diarios acumulados**
- Registra con su usuario y adjunta respaldo
- Sobre $50.000, consulta
- Rendición semanal

**Origen:** E-001 — un egreso de $10.550 escaló hasta Ricardo. Eso es 1,4 minutos
de venta de DiMango."""),

("R-002", "regla", "Niveles de autoridad para delegar", dict(
    estado="propuesto", fuente="HIPOTESIS", autoridad=5,
    origen="marco M5 de MENTORS.md, pendiente de aprobación",
    enlaces=dict(relacionado=["D-005", "R-001", "T-001"]),
    tags=["delegacion", "autoridad", "objetivo-90-dias"]),
"""Cuatro niveles, por área y por monto:

1. **Decide y actúa** — no informa
2. **Decide e informa** — actúa y deja registro
3. **Consulta antes** — no actúa sin respuesta
4. **Escala siempre** — nunca decide

**El problema de Ricardo no es que nadie decida: es que nadie sabe hasta dónde
puede decidir.**

Cada entrada de la bitácora de escalamientos se clasifica en un nivel y se asigna
a un responsable. Esa clasificación acumulada *es* el procedimiento de delegación."""),

# ─────────────────────────── ESCALAMIENTOS ───────────────────────────
("E-001", "escalamiento", "Noemi — autorizar egreso de caja de $10.550", dict(
    estado="vigente", fuente="HECHO", autoridad=4,
    origen="bitácora de escalamientos", fecha_hecho="2026-08-19",
    local="Playa Chinchorro", minutos=1, categoria="Finanzas/Pagos",
    nivel_propuesto=1,
    enlaces=dict(evidencia_de=["T-001", "D-005"], deriva_en=["R-001"]),
    tags=["bitacora", "caja", "playa"]),
"""Autorizar egreso de caja para pago de encomienda. **$10.550. 1 minuto**
(entrar al sistema y poner clave).

Origen: operación normal · ¿Podía resolverlo otro? **Sí, con autoridad** ·
Nivel propuesto: 1 (decide y actúa) · Responsable: encargado de local.

**Contexto:** $10.550 = 1,4 minutos de venta de DiMango; 0,006% de la
facturación mensual."""),
]

if __name__ == "__main__":
    for nid, tipo, titulo, meta, cuerpo in NOTAS:
        escribir(nid, tipo, titulo, meta, cuerpo)
    print(f"{len(NOTAS)} notas adicionales escritas")
