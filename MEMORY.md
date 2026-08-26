# MEMORY.md — Memoria de largo plazo

*Se actualiza cada vez que aprendemos algo importante. Lo más reciente arriba. Este archivo manda sobre `IDENTITY/SOUL/USER/BRAIN/MENTORS` cuando hay conflicto.*

> **Fuente única: `memoria/`, no este archivo.** Desde D-011 (20-ago-2026) la memoria vive en notas atómicas —`memoria/*.md` más `memoria/indice.json`— que llevan tipo, estado, autoridad y enlaces. **Este archivo es la vista narrativa de esas notas.** Si los dos difieren, manda la nota atómica, porque es la que consultan el agente y el briefing.
>
> Sincronizado con `memoria/` el **23-ago-2026**: entraron H-019 (dos credenciales expuestas, ambas rotadas), H-020 (el micrófono fijo del cerebro bloquea el despertar por aplausos), L-006 (la primera línea del error manda), S-017 (cerebro servido por localhost con puente), S-018 (el panel deja de mostrar las conversaciones de Ricardo) y P-011 (separar físicamente el historial privado). P-008 dejó de ser teórico: se cobró dos horas de webhook caído.
>
> Antes, el **22-ago-2026**: entraron D-011, H-017, H-018, L-005, P-007 a P-010, R-001 y R-002, y quedaron separados los tres roles contables (N-002 Carla Montoya → remuneraciones; N-006 Carlos Jirón → IVA y renta, es quien lleva el RCV; N-003 Cristian Vidal → solo vende la licencia anual del software de liquidaciones).
>
> Antecedente: consolidado el 20-ago-2026 desde una versión paralela que vivía en `~/Downloads/`. Si aparece otra copia en otra carpeta, está obsoleta por definición. Ver L-004.

**Cómo regenerar el índice después de editar `memoria/`:**

```bash
python3 ~/harvey/brain/grafo.py
```

---

## Decisiones

### D-011 · Migración a memoria atómica: aprobada para texto, bloqueada para voz — 20-ago-2026
Banco de 25 preguntas contra las dos memorias, mismo modelo y mismas instrucciones (`brain/evaluacion.json`), con el criterio fijado de antemano (D-007):

| Criterio | Resultado | |
|---|---|---|
| Cero pérdidas de información | 0 detectadas | ✅ |
| Primer token bajo 800 ms | 1.558 ms (mediana) | ❌ |
| Visto bueno de Ricardo | otorgado | ✅ |

Tokens de entrada: 20.284 → **7.535 (−63%)**. Primer token: 1.126 ms → 1.558 ms (+38%).

**La memoria nueva no empató, ganó en dos casos concretos:**
1. **La memoria vieja miente.** Seguía diciendo que Cristian Vidal era el contador. Es programador (N-003); la contadora es **Carla Montoya** (N-002).
2. **Manejo de contradicciones.** Ante "¿es creíble el 26% de margen?", la vieja eligió un lado en silencio; la nueva declaró el conflicto entre H-012 y H-017 con sus autoridades. Eso solo es posible con notas tipadas y `estado: conflicto`.

**Decisión:** texto (WhatsApp/Telegram) **migrado**; voz **bloqueada** hasta bajar la latencia. Causa pendiente: el prompt caching no está acertando (0 tokens leídos en las 25 pruebas) — defecto de implementación, no de diseño.

**Salvaguarda:** `agent/maximus.py` usa la memoria atómica solo si encuentra `memoria/indice.json` y `core/SOUL.md`. Si falta cualquiera, vuelve a los seis archivos completos. Falla cerrado.

### D-010 · Maximus se construye sobre el agente de WhatsApp que ya existe — 20-ago-2026
Ricardo decide priorizar el "gerente virtual" (antes punto B, parqueado por Maximus el 20-ago). **Objeción original planteada dos veces y retirada** al descubrir que el canal ya está construido: no abre un proyecto nuevo, cierra uno a medias, y en WhatsApp sí pasa el filtro obligatorio porque permite capturar la bitácora de escalamientos sin que Ricardo anote nada.

**Lo que ya existe en `~/whatsapp-agentkit` (HECHO, leído del repo):**
- Proveedores: `meta.py` (el que usa hoy — número **local chileno**, no Twilio), más `twilio.py`, `messenger.py`, `instagram.py`.
- `transcripcion.py`: **voz→texto ya funciona** (Groq Whisper large-v3-turbo, español).
- `brain.py`, `memory.py`, `main.py`, `tools.py`, `admin.py`.
- Precedente de tareas programadas: `subir_venta_mall.py` corre 22:30 en ServidorPlaya.

**El hallazgo que corrige el plan:** el agente actual es **de cara al cliente** (reservas, pedidos, leads, tickets, cotizaciones). Maximus es **de cara a Ricardo**. Mismo canal, rol distinto. Falta: (1) reconocer a Ricardo por número y enrutarlo a un cerebro propio con los seis archivos de memoria, (2) herramientas de gestión en vez de herramientas de atención, (3) **texto→voz, que NO existe** — solo hay entrada de audio, (4) tareas programadas para saludo y recordatorios.

**FASE 1 — construida y probada en el Mac el 20-ago-2026:**
- `agent/maximus.py` (nuevo): detecta el número de Ricardo, carga los seis archivos desde `MAXIMUS_MEMORY_DIR`, responde con prompt cacheado y formato WhatsApp. Cache invalidado por mtime: al editar la memoria, Maximus la relee solo.
- `agent/main.py`: 11 líneas insertadas **antes** de colación y de atención al cliente. **Falla cerrado**: si `MAXIMUS_OWNER_PHONES` está vacío, el bloque no existe para nadie y el agente se comporta igual que siempre.
- Prueba ejecutada (D-007): número reconocido con y sin `+`, otro número rechazado, 50.071 caracteres de memoria cargados, y respuesta correcta a "costo laboral de julio y prime cost" — incluyendo el caveat de que el 29% es estimado. **Aprobada.**
- **FASE 1 APROBADA el 20-ago-2026.** Desplegada en ServidorPlaya y verificada con el criterio fijado de antemano (D-007): Ricardo preguntó por WhatsApp desde su celular "¿cuánto fue el costo laboral de julio?" y Maximus respondió $30.271.531 / 45 personas / $36-42M cargado, **etiquetando el estimado como estimado**. No inventó.

**Estado de la instalación (20-ago-2026):**
- Código de producción: `C:\dimango-agent` (clon de `titicheo65/dimango-agent`, deploy key de solo lectura).
- Memoria: `C:\maximus` (clon de `titicheo65/maximus`).
- Se abandonó `C:\Users\usuario\Desktop\dimango-app`, que era la copia viva y **no era un repositorio git**. Quedan 5 copias muertas del proyecto en el servidor, pendientes de archivar.
- Arranque: `python -m uvicorn agent.main:app --host 0.0.0.0 --port 8000` desde `C:\dimango-agent`.

**P-008 · Tres pendientes de infraestructura, todos con costo si no se hacen:**
1. **Nada arranca solo.** Si se reinicia ese Windows, ni el agente ni ngrok vuelven. Se resuelve con tarea programada al inicio (ya hay precedente: `subir_venta_mall`).
2. **La memoria del servidor no se actualiza sola.** `C:\maximus` es un clon: cuando Maximus aprende algo en la sesión de Claude Code, el servidor sigue con la versión vieja hasta que alguien haga `git pull`. Necesita tarea programada cada 15 min.
3. **Telegram sin token válido.** El webhook devolvió 404 — el `.env` tiene el token revocado, no el nuevo.

**Decisión de canal (20-ago):** Maximus habla con Ricardo por **Telegram**, no por WhatsApp. Razón técnica, no de gusto: Meta no permite iniciar conversación fuera de la ventana de 24h sin plantilla aprobada, lo que hace **imposible el saludo matutino y las alertas proactivas** de la fase 2. Telegram permite escribir primero, gratis y sin aprobación. Los mensajes a **trabajadores y clientes siguen en WhatsApp** — ahí es donde ellos están. Implementado en `agent/telegram_maximus.py` + endpoint `/telegram/webhook`, aislado del webhook de WhatsApp.

**H-014 · Credenciales de Twilio expuestas en `.claude/settings.local.json` (HECHO, 20-ago-2026).** El push protection de GitHub bloqueó la subida: Account SID y API Key de Twilio en texto plano dentro del archivo de configuración local de Claude Code, líneas 37-39. **Siguen en el disco del Mac.** Riesgo bajo hoy porque el agente migró a Meta y Twilio ya no se usa — pero las credenciales deben **rotarse o eliminarse en el panel de Twilio**, no solo borrarse del archivo. El archivo quedó en `.gitignore` y fuera del repositorio.

**H-013 · El código de producción no tiene repositorio propio — RESUELTO el 20-ago-2026.** Creados `titicheo65/maximus` (memoria) y `titicheo65/dimango-agent` (código), ambos privados. Verificado que no se subió ningún `.env`, `.db`, cuadrante de personal ni RCV del SII. Detalle del hallazgo original: El remote de `~/whatsapp-agentkit` es `github.com/Hainrixz/whatsapp-agentkit` — el repo del autor del AgentKit, no de Ricardo. Estado: **ahead 3, behind 2**. Los tres commits propios (agente DiMango, automatización de venta al Mallplaza, control de colación) existen solo en el Mac y en ServidorPlaya, **sin respaldo en ningún repositorio de Ricardo**. Es el mismo agujero de L-004 pero en producción. Acción: crear `dimango-agent` privado y cambiar el remote.

**Riesgo asumido, declarado:** el agente corre en **ServidorPlaya**. Si cae la luz o internet en Playa Chinchorro, Maximus muere. Es L-002 otra vez — pieza nueva que solo Ricardo mantiene. Se acepta para las fases 1-2; antes de la fase 4 hay que decidir si migra a un servidor fuera del local.

### D-009 · Harvey pasa a llamarse Maximus — 20-ago-2026
Decisión de Ricardo. Cambio aplicado en los siete archivos (`CLAUDE.md`, `IDENTITY.md`, `SOUL.md`, `USER.md`, `BRAIN.md`, `MEMORY.md`, `MENTORS.md`). La carpeta sigue siendo `~/harvey/` — renombrarla es opcional y obliga a actualizar L-004.

### D-008 · Migración a DiMangoToGo completada — Toteat termina el 30-jun-2026
Desde el 1-jul-2026 DiMango opera 100% sobre DiMangoToGo (app propia, Base44). Aurexgroup —también de Ricardo— le factura el servicio a DiMango: **$1.000.000 en julio**.
**Lo bueno:** desaparece el problema de dos fuentes de verdad. DiMangoToGo es la fuente única y el tablero se vuelve posible.
**Lo malo:** desaparece la red. Ya no hay sistema alternativo si DiMangoToGo falla. Esta decisión es la que convierte P-001 (DTE) en el riesgo número uno del negocio.

### D-007 · Regla de despliegue reforzada — 19-ago-2026
"No tuvimos errores" no cuenta como verificación. Todo cambio en producción necesita una prueba explícita con criterio de aprobación y una fecha de verificación bajo carga real. Maximus no cierra un pendiente sin eso.

### D-006 · Tótems bloqueados con Fully Kiosk Browser — 19-ago-2026
**Problema:** niños salían de la app en los tótems de autoatención. Un tótem fuera de la app vende cero.
**Diagnóstico:** no se arregla en la app — una PWA no puede impedir la salida. Es bloqueo a nivel de sistema operativo.
**Solución implementada:** Fully Kiosk Browser sobre Android. Ricardo controla los dispositivos directamente.
**Estado: implementado, NO verificado bajo carga real.** Ricardo reporta "sin errores", que no es lo mismo que probado. **Verificar el sábado 22-ago con flujo de niños.**
**Pendientes de esta decisión:**
- Confirmar que el auto-reload deja el carrito vacío (si vuelve el pedido anterior, hace falta el reset por código).
- Riesgo vivo: el auto-reload de Fully es ciego a los pagos. Si recarga sobre una transacción en curso, se pierde la venta. Mitigado con umbral de 120 s; el reset por código en /Kioskos sigue siendo la solución correcta a mediano plazo.
- Registro de sesiones abandonadas: no implementado. Sigue sin saberse cuánta venta se cae por tótem.

### D-004 · Orden de las tres decisiones pospuestas — 19-ago-2026
Ricardo las listó: 1) salir del centro, 2) arquitectura tecnológica, 3) tablero de gestión.
**Maximus las reordena:** el tablero no es tercero, es **condición del primero**. No se puede delegar lo que no se puede medir; delegar sin métricas es abdicar, y en 60 días Ricardo vuelve al centro apagando el incendio que causó su propia delegación a ciegas.

Pero no van en fila india — tienen lead times distintos y arrancan **en paralelo**:

| Decisión | Quién ejecuta | Lead time |
|---|---|---|
| Segundo al mando | Ricardo, exclusivamente | 3-6 meses |
| Tablero de gestión | Maximus, mayormente | 3-4 semanas |
| Arquitectura definitiva | Ricardo + proveedor | 2-3 meses |

La búsqueda del #2 empieza primero porque tarda más. Cuando llegue, el tablero ya existe y es el instrumento con el que se le hace responsable desde el día uno.
**Nota 20-ago:** la "arquitectura definitiva" quedó resuelta de hecho por D-008 — DiMangoToGo es la fuente única desde el 1-jul. Lo que queda abierto no es *cuál sistema*, sino *cómo no depender de uno solo* (P-001).

### D-003 · Meta DiMango confirmada — 19-ago-2026
$2.400 millones CLP anuales ($200M/mes). +21,9% sobre run rate. La meta original escrita ("2.400.000 anual") era un error de unidades y quedó corregida.

### D-002 · Tesis de Aurexgroup corregida — 19-ago-2026
Ricardo mejoró la tesis original y esta es la versión vigente:

> Problema real detectado en DiMango → solución → validación interna → simplificación/estandarización → **instalación en un negocio externo sin intervención de Ricardo** → medición → recién entonces producto validado.

**Criterio de comercializabilidad (regla dura):** una solución solo es producto si un tercero puede instalarla, operarla y mantenerla **sin depender de Ricardo** para configurarla, corregirla o mantenerla viva. DiMango es laboratorio de descubrimiento y primera validación, nunca la prueba final.

### D-001 · Aurexgroup queda parqueado — 19-ago-2026
Ricardo decide enfocar 100% en DiMango. **Maximus está de acuerdo, y se lo gana así:** DiMango es el 100% de la caja y necesita sumar $430M/año; Aurexgroup no puede financiar eso en 12 meses ni en el mejor escenario.
**Condición:** parqueado ≠ abandonado. **Fecha de revisión obligatoria: 17 de noviembre de 2026.** Un proyecto sin fecha de revisión está abandonado con culpa, no parqueado.

---

## Hallazgos financieros (19-ago-2026, desde el RCV del SII, may-jul 2026)

### H-001 · Costo de mercadería SANO — 28,7% de la venta neta
Promedio 3 meses: $39,5M/mes en alimentos + bebidas. Dentro del rango normal (28-35%). **Ricardo compra bien.** Se usa el promedio a propósito: el RCV va por fecha de recepción y el mes a mes oscila artificialmente. Mayo parece anómalamente bajo — confirmar con agosto.

### H-002 · El costo de medios de pago saltó justo con la migración
| | Costo | % venta |
|---|---|---|
| Mayo (con Toteat) | $3.347.135 | 1,89% |
| Junio (con Toteat) | $1.743.016 | 1,15% |
| **Julio (solo DiMangoToGo)** | **$4.236.597** | **2,59%** |

Pre-migración 1,55% → post 2,59%. **+1,04 puntos = ~$20,5M/año.** Motor: Mercado Pago $1,73M → $2,40M (+39%) con la venta cayendo 7%.
**HIPÓTESIS PRINCIPAL:** DiMangoToGo enruta volumen hacia Mercado Pago, que cobra más que Transbank. La automatización propia estaría subiendo el costo por transacción.
**Caveat:** un solo mes; junio distorsionado porque Transbank no facturó. Confirmar con agosto.
**Acción pendiente:** ver P-002.
**Comparación cruda:** Toteat costaba ~$148.031/mes. Aurexgroup cobra $1.000.000/mes = **6,8x**. La transferencia interna no es fuga real; el delta de Mercado Pago sí.

### H-003 · Arriendo Plaza Oeste (Mall) — el mayor costo después de la comida
Mayo $11.874.572 · Junio $11.842.204 · **Julio $12.721.588 (+7,1%)** — sube mientras la venta cae 7,4%.
Si el local del Mall hace la mitad de la venta, el arriendo se come el **18,5% de su venta neta**. Sobre 20% el local no es viable.
**Acción:** leer el contrato (reajuste IPC, componente variable, gastos comunes) y obtener venta por local (P-003).

### H-004 · Aurexgroup no tiene ingresos externos — tiene una transferencia interna
Su primera y única factura ($1M, julio) es a DiMango. **Validación externa: cero.** Confirma el criterio de D-002: el único cliente es Ricardo.

### H-005 · Otros
- **Tabaco (BAT Chile):** ~$2,7M/mes promedio, ~$32M/año, con IVA no recuperable. Margen regulado casi nulo. Nadie ha calculado si conviene.
- **Capex mayo:** $7,6M (Marsol $6,6M). Explicaba la falsa alarma inicial de "compras disparadas".
- **Costos fijos** (arriendo + servicios + seguros): estables en ~11% de la venta.
- **Delivery:** comisiones ~$1,5M/mes = 1,0% de la venta. Canal pequeño.
- **Marketing real:** ~$83.696 en junio. Prácticamente cero, confirmado desde el SII.

### H-006 · Lo que sigue faltando
**Costo laboral.** No llega con factura, no está en el RCV. Costos conocidos ≈ $62M/mes contra venta neta de $137,9M → quedan ~$76M para sueldos, honorarios, impuestos y utilidad. Es el último número para cerrar el estado de resultados. Ver P-004.

### H-007 · El residual no cuadra — hay costo que no estamos viendo (ARITMÉTICA + HIPÓTESIS, 20-ago-2026)
Con el residual de H-006 ($76M) y la banda de costo laboral de `BRAIN.md` §3 ($31,5M–$49,5M/mes):

| Costo laboral | Queda para honorarios, impuestos y utilidad | % de la venta neta |
|---|---|---|
| $31,5M | $44,5M | 32,3% |
| $40,5M | $35,5M | 25,7% |
| $49,5M | $26,5M | 19,2% |

**El escenario más pesimista da 19% de margen antes de impuestos.** En gastronomía full-service el margen neto típico es 3-8%. Ningún punto de la banda es plausible.

**Conclusión: falta costo por identificar, o la venta neta está sobreatribuida.** No es una buena noticia disfrazada — es una señal de que el estado de resultados está incompleto.
**Candidatos a revisar, en orden:** ¿aparece el **arriendo de Playa Chinchorro**? (H-003 solo captura Plaza Oeste) · honorarios y boletas de terceros (no van al RCV de compras) · gastos comunes y contribuciones · proveedores que boletean · retiros del dueño · pérdida y merma no contabilizada (no hay inventario, ver P-005).
**Estado: hipótesis abierta.** Se resuelve con P-003 + P-004.

### H-008 · El traspaso entre locales bloquea el margen por local — 20-ago-2026
**Flujo confirmado por Ricardo (HECHO):** los pedidos se envían todos los días — se despacha desde **Playa Chinchorro** y se entrega en el **Mall**. Hay traspaso interno de mercadería entre locales, diario.

**Consecuencia que nadie había visto:** las compras entran por un solo RUT y (probablemente) por un solo local. Si el traspaso Playa→Mall no se registra valorizado, **el costo de mercadería por local no existe** — solo existe la venta por local.

Eso significa que **P-003 no alcanza para responder H-003.** Saber que el Mall vende X no dice si el Mall es viable: falta su costo. El arriendo de $12,7M/mes solo se puede juzgar contra el margen del local, no contra su venta.

**Por lo tanto el módulo de reposición no es solo control de merma — es el instrumento que hace posible el margen por local.** Eleva su prioridad de forma legítima.

**Son dos controles distintos, no uno:**
1. **Pedido del Mall vs venta del Mall** — ¿piden de más? (el caso que planteó Ricardo)
2. **Despachado en Playa vs recibido en el Mall** — ¿llega todo? (el que nadie mira, porque "es de la casa")

El segundo es el punto de fuga clásico en operaciones de dos locales.

### H-009 · Base44 sin créditos y código espejado en GitHub — 20-ago-2026 (observado en pantalla)
- **0 créditos restantes**, renovación en ~2 días (≈22-ago). **Ricardo no puede editar DiMangoToGo hasta entonces.** Si aparece una falla en producción hoy, no tiene herramienta para corregirla. Se cruza directo con P-001.
- Plan ofrecido: Elite $100 el primer mes, luego **$200/mes**. El plan actual no está confirmado.
- **El código está sincronizado con GitHub** ("Code synced successfully"). Es la primera pieza real de contingencia contra L-002: existe una copia del código fuera de Base44. **Pendiente: el nombre del repo.**

### H-010 · Auditoría del código de las dos apps — 20-ago-2026 (HECHO, leído del repo)
Repos privados clonados en `~/dimango-repos/` (`titicheo65/dimangotogo`, `titicheo65/dimangoworking`), acceso por llave SSH dedicada `id_ed25519_github`. ToGo: 519 archivos. Working: 283.

**Lo que YA existe — el control está construido al ~70%, no al 0%:**
- `ChecklistPedido` (Working): fecha · local (MALL/PLAYA) · área · producto · **cantidad_solicitada** · **cantidad_entregada** · responsable · estado. El control despachado-vs-recibido de H-008 **ya está modelado**.
- `ReglaInsumo` (ToGo): convierte producto vendido → insumo, con multiplicadores. Es el puente venta↔bodega.
- `TabVincularChecklist` (Working): vincula ítem de checklist ↔ ítem de bodega con `factor_descuento`.
- `MermaChecklist`: merma **valorizada en $**. `MovimientoStock`: entradas/salidas con destino (incluye MERMA y COLACION).
- `PlanillaSueldo`: mes · nombre · puesto · **local (playa/mall/ambos)** · sueldo_base · total_mes.

**Los cuatro huecos reales, en orden de gravedad:**
1. **Todo el puente venta↔bodega es matching por NOMBRE DE TEXTO.** No hay ID compartido entre `Product` (ToGo) y `CatalogoProducto`/`ProductoPedidoDiario` (Working). El propio esquema lo dice: `ReglaInsumo.nombre_en_venta` = *"Nombre del producto tal como aparece en la venta (POS). Fuente de matching."* Y `TabVincularChecklist` compara con `normalizar(nombre)`. **Consecuencia: renombrar un producto en la carta rompe la conversión en silencio.** No tira error, deja de contar. Es el peor tipo de falla en un control.
2. **La comparación que Ricardo pidió NO existe.** `ChecklistPedido` compara solicitado vs entregado, pero **no tiene campo de "sugerido según venta"**. Nadie cruza pedido contra venta del día. Esa es exactamente la pieza que falta.
3. **Dos formatos de vínculo conviviendo:** `vinculos_bodega` (nuevo) y `bodega_item_id` (legacy). Deuda que duplica los caminos de lectura.
4. **El enum `accion` de `ReglaInsumo`** (`oz2`, `limones2`, `x4`, `350gr`… "migrado del sistema viejo") es un lenguaje ad-hoc heredado. Producto nuevo que no calce con esos valores queda fuera de la conversión, en silencio.

**El número que decide todo, y es una consulta, no un proyecto:**
> ¿Qué % de los productos vendidos el último mes tiene una `ReglaInsumo` que los cubra?

Si la cobertura es 60%, la alerta miente en el 40% restante y no sirve como control. **Medir esto ANTES de construir cualquier alerta.**

**P-004 puede cerrarse desde `PlanillaSueldo`** — y además **por local**, que es justo lo que H-008 necesitaba para H-003. Caveat: `total_mes` es **neto**; falta leyes sociales para llegar al costo cargado. El factor se saca de Previred, no se estima.

### H-011 · COSTO LABORAL DE JULIO — P-004 CERRADO (HECHO, planilla `suelgo_working.xlsx`, 20-ago-2026)
Fuente: Excel de Ricardo, hojas mar-26 a ago-26. Verificación de integridad: `QUINCENA + extras + fin de mes = TOTAL2` cuadra en **el 100% de las filas** de los tres meses revisados. La planilla es internamente consistente.

**Julio 2026 — pago líquido: $30.271.531 · 45 personas** (coincide con las ~45 de `USER.md`).

| Local | Personas | Líquido | % del total |
|---|---|---|---|
| Playa Chinchorro | 30 | $21.411.531 | 70,7% |
| Mall | 11 | $6.600.000 | 21,8% |
| Ambos | 3 | $2.260.000 | 7,5% |

Por puesto: garzones $7,62M · cocina $6,80M · heladeros $4,69M · administración $3,75M · aseo $3,21M · producción $1,95M.

**Serie:** junio $25,93M (37 personas) → julio $30,27M (45) → agosto $28,91M (43).
**Alerta:** de junio a julio entraron **8 personas (+21,6%)** y el costo laboral subió **+16,8%**, con la venta subiendo solo **+7,5%**. Como % de la venta neta: junio 17,0% → **julio 18,5%** (+1,5 pts). Nadie decidió eso mirando un número.

**Costo cargado (ARITMÉTICA, no dato):** la planilla es de pago líquido; no incluye leyes sociales del empleador ni AFP/salud del trabajador. Aplicando un factor líquido→costo empresa de 1,20–1,38: **$36M–$42M/mes**. El factor exacto sale de Previred, no se estima.

**Efecto sobre `BRAIN.md` §3:** la banda de incertidumbre de $18M/mes se reduce a ~$6M. El punto medio (~$39M) cae en el centro de la banda original.

**Prime cost (ARITMÉTICA):** mercadería 28,7% + laboral cargado ~29% = **≈57,7% de la venta neta.** Bajo el umbral de 60-65% de la industria. **El prime cost de DiMango está sano.** Es la primera buena noticia con datos detrás.

**El costo laboral NO es asignable por local tal como está.** Playa concentra 30 de 45 personas porque **produce para los dos locales** (H-008). Si el Mall hiciera la mitad de la venta, su laboral sería 9,6% de su venta y el de Playa 31% — ninguno de los dos es creíble. Igual que con la mercadería, el costo de producción hay que repartirlo. Sin esa repartición no hay margen por local.

### H-012 · H-007 SE CONFIRMA — siguen faltando ~$36M/mes (ARITMÉTICA, 20-ago-2026)
Con el costo laboral ya conocido:

| Concepto | Monto/mes |
|---|---|
| Venta neta (julio) | $137,9M |
| Costos conocidos (RCV, H-006) | −$62M |
| Costo laboral cargado (H-011, punto medio) | −$39M |
| **Residual sin identificar** | **≈$36M — 26% de la venta neta** |

**P-004 estrechó el problema pero no lo cerró.** Un 26% antes de impuestos sigue siendo implausible en gastronomía full-service (3-8% típico). Son ~$430M al año sin explicación.

**Dos lecturas posibles, y hay que decidir cuál con evidencia, no con optimismo:**
1. Falta costo por capturar — el candidato #1 sigue siendo el **arriendo de Playa Chinchorro** (H-003 solo capturó Plaza Oeste), más honorarios, contribuciones, gastos comunes, PPM/renta, pagos en efectivo (la planilla tiene notas "cash") y retiros del dueño.
2. La venta neta de $137,9M está sobreatribuida.

**Siguiente paso concreto:** confirmar si existe arriendo de Playa Chinchorro y por cuánto. Si es local propio, la explicación hay que buscarla en el resto de la lista.

### H-015 · P-003 CERRADO — venta de julio por local, y el Mall no se sostiene (HECHO + ARITMÉTICA, 20-ago-2026)
Fuente: DiMangoToGo `/AdminVentas`, resumen contable de julio filtrado por local (autoridad 2).
**Verificación:** Playa + Mall cuadra al peso con el consolidado en las tres líneas (bruta, c/IVA, neta). Sin conflicto interno.

| | Playa | Mall | Total |
|---|---|---|---|
| Venta bruta | $119.455.935 | $40.464.040 | $159.919.975 |
| Venta c/IVA | $119.044.684 | $40.433.220 | $159.477.904 |
| **Venta neta** | **$100.037.550** | **$33.977.496** | $134.015.045 |
| Propinas | $7.260.449 | $3.455.478 | $10.715.927 |
| **% del total** | **74,65%** | **25,35%** | 100% |

**Estado de resultados por local (ARITMÉTICA; supone mercadería 28,7% igual en ambos):**

| | Mall | Playa |
|---|---|---|
| Arriendo | **37,4%** | 0% (local propio) |
| Mercadería | 28,7% | 28,7% |
| Laboral directo | 19,4% | 21,4% |
| Medios de pago | 2,6% | 2,6% |
| **Queda** | **11,8%** | **47,3%** |

**El arriendo del Mall es 37,4% de su venta neta. El umbral de viabilidad de la industria es 20%.** Casi el doble.

Y ese 11,8% residual todavía no descuenta: la mano de obra de producción de Playa que trabaja para el Mall (H-008 — el Mall no produce nada, todo llega elaborado), los 3 empleados "ambos", servicios, gastos comunes ni administración. **El Mall está en el borde o bajo el agua.**

**Playa subsidia al Mall.** Ya no es hipótesis: Playa deja 47,3% antes de gastos generales, y no paga arriendo.

**Qué necesitaría el Mall para llegar a un arriendo del 20%:**
- Vender **$63,6M netos** contra los $33,98M de hoy → **crecer 87%**, o
- Renegociar el arriendo a **$6,8M** → **bajar 47%**

Ninguna de las dos es menor. La tercera opción es cerrar.

**Efecto sobre D-003 (meta de $2.400M/año):** el Mall aporta el 25,35% de la venta. Si es deficitario, **crecer en venta total empeora el resultado** — que es exactamente la advertencia de M4. La meta puede estar mal planteada: debería ser de margen, no de facturación.

**Antes de decidir hay que:** leer el contrato de Plaza Oeste (reajuste, componente variable, vencimiento, multa por salida anticipada) y confirmar el supuesto de mercadería por local.

### H-016 · Dos hallazgos menores de `/AdminVentas` (20-ago-2026)
- **`COSTO NETO: $0`.** El campo existe en la pantalla y `Product.cost` existe en el esquema ("costo neto unitario para cálculo de margen"). **Está construido y nadie lo llenó.** Cargar los costos daría margen bruto por producto y por categoría sin necesidad de inventario ni contador. Máximo valor por mínimo esfuerzo.
- **Propinas $10,7M/mes (6,7% de la venta).** Pendiente confirmar si están dentro o fuera de la venta bruta: si están dentro, todos los porcentajes calculados sobre venta están sobreestimados.

### H-017 · Ricardo afirma que el margen de 26% es real — CONFLICTO ABIERTO (20-ago-2026)
Ante la pregunta de si el residual de 26% (H-012) era creíble, Ricardo respondió: *"sí es creíble, es un poco lo que estamos manejando de ganancia"*.

**Autoridad 4** (informado por persona) contra la estimación de Maximus (**autoridad 5**). Por la regla de prioridad de fuentes, esta nota gana.

**Pero no cierra el conflicto:** hace falta **autoridad 1 — movimiento bancario de julio**. Mientras tanto H-012, H-017 y la métrica M-005 (margen neto) quedan en `conflicto`, y Maximus debe declararlo cada vez que el tema aparezca, en vez de elegir un lado en silencio.

### H-018 · Los trabajos de impresión no se marcan como impresos — riesgo de reimpresión masiva (21-ago-2026)
Fuente: `C:\Users\usuario\.pm2\logs\impresion-playa-error.log`. El log repite quince veces:

> `[COLA] Job <id> ya se imprimio en esta sesion (Base44 lo sigue marcando pendiente) - se omite para no duplicar`

**Qué pasa:** el servidor imprime, pero **DiMangoToGo nunca marca el trabajo como impreso**. La cola queda llena de trabajos fantasma en estado pendiente.

**Qué evita el desastre hoy:** una lista anti-duplicados que vive **en la RAM** del servidor de impresión.

**Por qué es frágil:** si el proceso se reinicia —corte de luz, reinicio de Windows, o el arranque automático de P-008— esa lista se pierde, Base44 sigue diciendo "pendiente" y **se reimprimen de golpe todos los trabajos acumulados**: boletas y precuentas viejas saliendo en cadena, probablemente en medio del servicio.

**Agravante:** el arranque automático que resuelve P-008 hace este escenario *más* probable, no menos. Antes alguien levantaba el servidor a mano y estaba mirando; ahora arranca solo. **Y el Mall tiene su propio PC con servidor local y arranque automático ya configurado (S-012): si corre el mismo código, el riesgo ya está activo allá, hoy.**

**Dónde se arregla:** en DiMangoToGo, no en el servidor de impresión. El job debe marcarse como impreso cuando el servidor confirma.

**Evidencia a buscar, barata:** preguntar en el Mall si alguna vez salieron boletas o precuentas viejas de golpe después de un corte de luz. Si ocurrió, esto deja de ser hipótesis.

**Segundo hallazgo del mismo log:** PM2 tiene registrada la **v6** del servidor de impresión en estado `stopped`, pero en el repositorio existe una **v7**. Pendiente confirmar qué proceso imprime hoy en Playa.

### H-019 · Dos credenciales expuestas en producción — ambas rotadas el 23-ago-2026
El panel `/admin` —que lista **todas** las conversaciones y se publica por ngrok— corría con la contraseña escrita en el código: `admin` / `dimango2026`, valores por defecto que el `.env` no sobreescribía. Cualquiera con la URL y esa clave, publicada en el repositorio, leía los chats de clientes y las conversaciones de Ricardo con Maximus.

El mismo día, el **token de `/maximus/chat`** quedó visible en una captura de pantalla mandada para diagnosticar otra cosa.

**Ambas rotadas y verificadas**, no dadas por buenas: clave vieja → **401**, token viejo → **401**, agente operativo → 200.

**Es el tercer caso del mismo patrón** tras H-014 (Twilio). La constante no es el descuido: es que **el sistema trae valores por defecto que funcionan**, y un default que funciona nunca se cambia. **Regla derivada:** ningún componente debe arrancar con credencial por defecto — si falta la variable, que no arranque.

**Sigue abierto:** el panel no debería estar expuesto a internet. La contraseña tapa el agujero; sacarlo del túnel lo cierra.

### H-020 · El micrófono fijo del cerebro y el despertar por aplausos no conviven — 23-ago-2026
Solo un proceso a la vez escucha bien el micrófono del Mac. Con el cerebro abierto y el micrófono en modo fijo, `escuchar.py` mide **0.0000**. Es consecuencia directa del arreglo del mismo día (S-017): antes el micrófono se apagaba entre turnos y dejaba huecos; ahora el pestillo queda puesto y el conflicto es permanente.

**`escuchar.py` quedó detenido.** Corría con `--umbral 0.15` —la mitad del que trae por defecto— y por eso cualquier par de ruidos secos despertaba a Maximus solo. Para relanzarlo hay que calibrar, y para calibrar hay que soltar el micrófono.

**Duda de fondo:** el aplauso es frágil por diseño — umbral fijo sobre una entrada que macOS amplifica sola, compitiendo por el micrófono con el propio cerebro. Un atajo de teclado hace lo mismo y es determinista.

---

## Bitácora de escalamientos — entradas

### E-001 · 19-ago-2026 · Noemi · Playa Chinchorro
Autorizar egreso de caja para pago de encomienda. **$10.550. 1 minuto** (entrar al sistema y poner clave).
Categoría: Finanzas/Pagos · Origen: Operación normal · Podía resolverlo otro: sí, con autoridad · Nivel: 1 (decide y actúa) · Responsable: encargado de local.
**Contexto:** $10.550 = 1,4 minutos de venta de DiMango; 0,006% de la facturación mensual.
**Regla propuesta (pendiente de aprobación):** caja chica por local hasta $50.000 por egreso y $200.000 diarios acumulados; el encargado autoriza, registra con su usuario y adjunta respaldo. Sobre $50.000, consulta. Rendición semanal.

---

## Abierto — requiere decisión de Ricardo

### P-001 · Contingencia de emisión de DTE — RESPONDIDO Y DESESCALADO el 20-ago-2026

**Respuestas de Ricardo (HECHO):**
- DiMangoToGo **no emite**: emite **SimpleFactura**, proveedor externo certificado.
- **Contingencia existente:** emisión manual desde la web de SimpleFactura si DiMangoToGo falla.
- Folios CAF **al día**. **Cero fallas de emisión en julio.**
- **Los encargados de ambos locales saben emitir manual.** La contingencia funciona sin Ricardo — cumple P3.

**Maximus se equivocó en el tamaño del riesgo, y lo reconoce.** Se clasificó como riesgo #1 a $5,5M/día asumiendo que DiMangoToGo emitía por sí misma y que no había alternativa. Con proveedor certificado, emisión manual documentada, folios al día y un mes sin fallas, **ese número era una construcción de Maximus, no un hecho del negocio.** Lección: un riesgo estimado sin verificar la arquitectura real vale tan poco como un número inventado.

**Riesgo residual, real pero menor:** el punto único ya no es DiMangoToGo — es **SimpleFactura e internet**. Ambas vías (app y web del proveedor) requieren conexión. No existe respaldo en papel porque en Chile la boleta es 100% electrónica (verificado en sii.cl, 20-ago-2026); el talonario timbrado ya no aplica.

**Única pregunta abierta, para el proveedor y sin urgencia:** ¿DiMangoToGo/SimpleFactura **encolan** las boletas si cae internet y las timbran al recuperar conexión? El SII contempla ese modo —emisión sin timbre electrónico y timbrado posterior visible en el Resumen de Ventas Diarias—, pero hay que confirmar si el software lo implementa o simplemente falla.

*(Nota normativa, cumplida: desde el 1-mar-2026 rige la entrega obligatoria de la boleta impresa o en digital en venta presencial. DiMango tiene impresoras en ambos locales.)*

### ~~P-001 original~~ · Enunciado previo, conservado para trazabilidad
Desde el 1-jul-2026 no existe sistema alternativo. Si DiMangoToGo no emite, DiMango no vende legalmente: ~$5,5M/día. **Es el riesgo número uno del negocio, por encima del tablero y de todo lo demás.**
Preguntas abiertas: ¿DiMangoToGo está certificada ante el SII como sistema propio o emite vía proveedor por API? ¿Hay talonario de contingencia autorizado o el sistema gratuito del SII configurado y probado? ¿Los folios/CAF están al día? **¿Hubo fallas de emisión en julio?**
**Nota Maximus 20-ago:** cuatro preguntas sin respuesta no es un pendiente, es evitación (`SOUL.md` — "está evitando una decisión importante"). Este ítem bloquea el resto de la agenda hasta que tenga respuesta.
**20-ago, quinta vez:** Ricardo decide conscientemente posponerlo — *"sobre el DTE lo respondo después de esto, para mí es prioridad esto último"* (control de reposiciones). Queda registrado como decisión suya, con la objeción de Maximus ya planteada cinco veces. Agravante del mismo día: H-009 — Base44 sin créditos hasta ~22-ago, o sea que si la emisión falla esta semana tampoco puede tocar el código.
*(Trazabilidad: el número P-001 se reusó. El P-001 original — "confirmar software contable, inventario y RRHH" — es ahora P-005.)*

### P-002 · Comparar tasa de comisión Mercado Pago vs Transbank
Vale ~$20,5M al año. Una tarde de trabajo. Ver H-002.

### P-003 · Venta de julio por local (desde DiMangoToGo)
Cierra el estado de resultados por local y resuelve la pregunta del arriendo del Mall (H-003) y el residual de H-007.

### P-004 · Costo laboral de julio
Remuneraciones + imposiciones. El último número del estado de resultados. Cierra el indicador más caro de `BRAIN.md` §3: una banda de $18M/mes de incertidumbre.

### P-005 · Contabilidad, inventario y RRHH — resuelto parcialmente
*(Antes P-001.)*
- **Contable:** no existe software. **Son tres personas con tres funciones separadas** (HECHO, informado por Ricardo el 22-ago-2026):
  - **Carlos Jirón V.** — Soc. Ardiles & Jirón Cía Ltda, Arica. Lleva **IVA y renta** (N-006). Es quien trabaja sobre el **RCV del SII**, la fuente de H-001 a H-006. Honorarios de julio 2026 **sin pagar** al 22-ago.
  - **Carla Montoya** — **remuneraciones y liquidaciones** (N-002). Fuente humana de la planilla que cerró H-011.
  - **Cristian Vidal** — **no es contador ni programador de DiMango**: vende una licencia, **una vez al año**, del software con que se generan las liquidaciones (N-003).

  Consecuencia: contabilidad tributaria y laboral, **no de gestión**. Ninguno de los tres entrega margen por local ni prime cost semanal. **Pendiente:** si Ricardo tiene acceso de consulta y si la contabilidad va separada por local o consolidada — eso último define si el margen por local sale de contabilidad o hay que construirlo desde DiMangoToGo.
  **Historial de correcciones — dos errores encadenados, ambos por modelo incompleto:** el 20-ago figuraba **Cristian Vidal** como contador (falso, y contaminó el análisis un día completo). El 21-ago, corregido a **Carla Montoya llevando el RCV** — también falso: el RCV es de Carlos Jirón. La lección de N-002 se confirma: cuando dos fuentes se contradicen, lo más probable no es que una mienta, sino que falte una pieza del modelo.
- **Alternativa barata al inventario (H-016):** cargar `Product.cost` en DiMangoToGo entrega margen bruto por producto sin instalar nada. No mide merma, pero responde la pregunta más útil primero.
- **RRHH / control de gestión:** **DiMangoWorking** (Base44, de Ricardo). Cae bajo L-002: otro sistema que solo Ricardo mantiene.
- **Inventario:** **NO EXISTE sistema central.** Por eso compras ≠ consumo y **la merma es inmedible**. Es la causa raíz de que H-001 (28,7%) sea un costo de *compra*, no de *consumo* — el margen bruto real puede ser peor.

### P-007 · Control de reposiciones: cruzar pedido con venta — PEDIDO EXPLÍCITO DE RICARDO
**El caso que planteó:** se venden 10 Coca-Colas, reponen 12 → alerta.

**Lo que ya existe (H-010):** la venta del día anterior llega por correo automático a la 1:30 AM · `ChecklistPedido` tiene cantidad solicitada vs entregada por local y área · `ReglaInsumo` convierte producto vendido → insumo.

**Lo único que falta:** que al cargar el pedido aparezca al lado lo que se vendió. Los dos datos están sobre la mesa a la misma hora y nadie los junta.

**Riesgo previo a medir, no negociable:** el puente venta↔bodega es matching por **nombre de texto**. Antes de construir la alerta hay que medir **qué % de los productos vendidos tiene una `ReglaInsumo` que los cubra**. Si es 60%, la alerta miente en el 40% restante y se ignora en dos semanas.

**Control de personas (N-004):** **Verónica pide y despacha** — pide la reposición del Mall (10:00-11:45 diario) y despacha en Playa. La misma persona que decide cuánto se manda confirma cuánto salió. Recibiendo en el Mall hay cuatro personas según el día (N-005: Vivianda de lunes a viernes; Alejandra o Angélica el fin de semana; siempre el cocinero del turno AM). **Sin separación de funciones, el control técnico no cambia nada.** No es acusación: es el punto de fuga clásico en operaciones de dos locales.

### P-008 · Infraestructura de Maximus en ServidorPlaya
1. **Nada arranca solo.** Si se reinicia ese Windows, ni el agente ni ngrok vuelven. Tarea programada al inicio (hay precedente: `subir_venta_mall`). **Ojo: resolver esto agrava H-018** — ver ahí antes de activarlo.
2. **La memoria del servidor no se actualiza sola.** `C:\maximus` es un clon: sin `git pull` periódico, Maximus se congela en el 20 de agosto y responde datos viejos con seguridad — peor que no tenerlo.
3. **Telegram sin token válido.** El webhook devolvió 404.
4. **Cinco copias muertas** del proyecto en el servidor, pendientes de archivar.
5. **Todo pasa por un túnel ngrok gratuito.** Si cae, el webhook de WhatsApp deja de recibir mensajes de clientes **y nadie se entera**.

### P-009 · Riesgo residual de emisión: internet
El punto único ya no es DiMangoToGo: son **SimpleFactura e internet**. Las dos vías —la app y la web del proveedor— requieren conexión, y en Chile la boleta es 100% electrónica: el talonario timbrado ya no existe como contingencia.
**Pregunta para el proveedor, sin urgencia:** ¿SimpleFactura **encola** las boletas si cae internet y las timbra al recuperar conexión? El SII contempla ese modo; falta confirmar si el software lo implementa o simplemente falla.

### P-010 · Filtración de aguas lluvias en el local del Mall — 20-ago-2026
Mallplaza informa **por escrito** una filtración de aguas lluvias en el local del mall y adjunta **carta de activación de seguro**. Firma Yanira Tara, con copia a Marcela Cerda y Diego Silva: la comunicación es formal. Ricardo la reenvió a TRABAJOARICACHILE@gmail.com esa misma noche.

**Pendiente de verificar:** alguien en terreno que constate el daño y lo fotografíe · si hubo pérdida de mercadería u horas de operación · qué cubre el seguro y quién lo tramita.

**Lectura de Maximus — esto no es solo un siniestro:** el arriendo del Mall es el **37,4% de su venta neta** (H-015), casi el doble del umbral viable, y hay que renegociarlo o salir. Un defecto de infraestructura documentado **por el propio arrendador** es material para esa conversación. **Guardar todo por escrito** —cartas, fotos, fechas, pérdidas—: hoy es un siniestro, en la renegociación es un argumento.

### P-011 · Separar físicamente el historial privado de Maximus — 23-ago-2026
Hoy las conversaciones de Ricardo con Maximus están **ocultas** del panel, no separadas (S-018): siguen en el mismo archivo de base de datos que los chats de clientes. Quien tenga acceso al `.db` del servidor las lee.

**La versión buena ya está escrita** —base aparte, imposible de exponer por olvido— en el commit `4eea4a1` de `titicheo65/dimango-agent`. Se descartó porque el agente no levantó tras desplegarla, y **después se comprobó que la caída era por un puerto tomado (L-006), no por ese código.**

**Cómo retomarlo:** un día de semana, probando el arranque en el servidor (Windows, Python 3.14) antes de dejarlo corriendo, con el puerto verificado libre, y recuperando `migrar_privado.py` del mismo commit para mover lo ya guardado.

**Prioridad honesta: baja.** El riesgo real —panel abierto a internet con contraseña por defecto— ya se cerró con H-019.

### D-005 · El objetivo de 90 días no es un objetivo todavía
"Reducir la dependencia operativa" con ocho subcomponentes es un programa, no un objetivo. No tiene métrica ni fecha de verificación.
**Propuesta de Maximus:** convertirlo en un compromiso fechado y falsable —
> **Del 9 al 15 de noviembre de 2026, DiMango opera 7 días corridos sin que Ricardo resuelva una sola decisión operacional.**

**Estado: bitácora ACEPTADA y entregada el 19-ago-2026** (`Bitacora_Escalamientos_DiMango.xlsx`). Captura diaria por WhatsApp/nota, clasificación semanal por Maximus los viernes. **Primer diagnóstico completo: semana del 14-sep-2026.** La meta de 7 días (9-15 nov) sigue pendiente de aceptación formal.

### T-001 · Tesis rival: no necesita un #2, necesita cerrar proyectos
Un observador competente diría que el problema de Ricardo no es falta de estructura sino exceso de iniciativas simultáneas — él mismo escribió "probablemente tengo más proyectos de los que debería ejecutar".
Un #2 cuesta $2-3M/mes y tarda 6 meses en ser útil. Cortar la cartera de proyectos a la mitad es gratis y funciona el lunes siguiente.
**Estado: sin resolver. Criterio de veredicto fijado el 19-ago-2026:** si en la bitácora "Proyecto iniciado por Ricardo" supera el **40% de los minutos**, gana la tesis rival y la prioridad pasa a cerrar proyectos antes que a buscar un #2. La hoja Resumen calcula ese porcentaje solo.
**Cómo se ejecuta la medición (22-ago-2026):** skill `viernes` en `.claude/skills/viernes/SKILL.md`. Registra cada escalamiento como nodo `E-00X`, recalcula el porcentaje acumulado y propone reglas cuando un tipo se repite. Una semana sin datos se reporta como *"sin registro"*, nunca como *"cero escalamientos"*.

---

## Reglas propuestas — pendientes de aprobación de Ricardo

### R-001 · Caja chica por local
El encargado autoriza egresos hasta **$50.000 por egreso** y **$200.000 diarios acumulados**, registra con su usuario y adjunta respaldo. Sobre $50.000, consulta. Rendición semanal.
**Origen:** E-001 — un egreso de **$10.550** escaló hasta Ricardo. Eso es 1,4 minutos de venta de DiMango.

### R-002 · Niveles de autoridad para delegar
Cuatro niveles, por área y por monto (marco M5 de `MENTORS.md`):

1. **Decide y actúa** — no informa
2. **Decide e informa** — actúa y deja registro
3. **Consulta antes** — no actúa sin respuesta
4. **Escala siempre** — nunca decide

**El problema de Ricardo no es que nadie decida: es que nadie sabe hasta dónde puede decidir.** Cada entrada de la bitácora se clasifica en un nivel y se asigna a un responsable. Esa clasificación acumulada **es** el procedimiento de delegación — no hay que escribirlo aparte.

---

## Lecciones

### L-006 · Cuando un proceso no arranca, manda la primera línea del error — 23-ago-2026
El agente no levantaba. El traceback visible mostraba `SystemExit: 1`, un `CancelledError` de SQLAlchemy y un error del loop de colación. Maximus concluyó que la causa era un cambio propio —una segunda base de datos— e hizo revertir el despliegue.

No era eso. La causa estaba en la primera línea, cortada por el scroll: `OSError [Errno 10048]: solo se permite un uso de cada dirección de socket`. **El puerto 8000 estaba tomado por un proceso zombi.** Todo lo demás era la cascada de apagado.

**Costo: cerca de dos horas con el webhook de WhatsApp caído, un domingo con los dos locales operando**, más un rollback innecesario.

**Regla derivada, que se lee al revés de como aparece:** la primera línea es la causa y el resto es consecuencia · si el error llega cortado, capturarlo entero **antes** de teorizar · verificar que el puerto está libre antes de arrancar, y que quedó libre después de matar — no asumirlo · nunca lanzar un segundo intento sobre uno que parece colgado, que es como se crea el zombi.

**Misma familia que L-005:** allá se cuantificó un riesgo sin verificar la arquitectura, acá se atribuyó una falla sin leer el error completo. En los dos casos la hipótesis se presentó con el peso de un hecho.

### L-005 · Un riesgo estimado sin verificar la arquitectura vale tan poco como un número inventado — 20-ago-2026
Maximus clasificó la emisión de DTE como **riesgo #1 del negocio a $5,5M/día**, por encima de todo lo demás, y lo repitió cinco veces.

El número era una construcción propia: asumía que DiMangoToGo emitía por sí misma y que no había alternativa. La realidad —proveedor certificado, emisión manual que los encargados saben usar, folios al día, cero fallas en julio— lo desmintió.

**La estimación tenía autoridad 5 y se presentó con el peso de un hecho.**
**Regla derivada:** todo riesgo cuantificado debe declarar **de qué arquitectura depende**, y esa arquitectura se verifica antes de priorizar sobre ella.

### L-004 · La memoria de Maximus tuvo dos fuentes de verdad — 20-ago-2026
Existían dos `MEMORY.md` divergentes: uno en `~/harvey/` (versión del 19-ago, con D-001 a D-005) y otro en `~/Downloads/` (más avanzado: D-006 a D-008, hallazgos H-001 a H-006, bitácora E-001). Trabajar sobre el equivocado habría significado repetir decisiones ya tomadas y perder los hallazgos financieros.
**Es el mismo error que D-008 acaba de eliminar en el POS**, replicado en el sistema que existe para evitar ese error.
**Regla derivada:** la memoria vive en `~/harvey/`, versionada en git. Los archivos que salen a otra carpeta son exportaciones de solo lectura y mueren ahí. Toda sesión arranca con `cd ~/harvey`.

### L-003 · No se puede justificar automatización sin conocer el costo que ahorra — 19-ago-2026
Tótems, autoservicio y reducción de cajas se justifican con un ahorro de costo laboral que hoy es **inmedible**, porque no existe el costo laboral %. Cuando el tótem funcione no habrá forma de decir si ahorró $4M o costó $2M. Y sin ese número, Aurexgroup tampoco tiene caso de venta: no se puede vender un ROI que no se midió en el propio laboratorio.

### L-002 · La automatización está profundizando el cuello de botella que dice resolver — 19-ago-2026
Cada componente que Ricardo agrega —Base44, DiMangoToGo, DiMangoWorking, servidor de impresión propio, tótem, cuatro medios de pago— es una pieza más que **solo él entiende**. Está reemplazando dependencia de personas por dependencia de sistemas que dependen de una sola persona.
**Regla derivada:** automatización que solo Ricardo puede mantener no es automatización, es una dependencia nueva con mejor interfaz. Toda iniciativa técnica debe pasar el test de D-002.
**Agravante 20-ago:** D-008 eliminó Toteat. La dependencia ya no tiene alternativa. Ver P-001.

### L-001 · DiMango no está instrumentado — 19-ago-2026
Cinco de seis preguntas financieras fundamentales sobre un negocio de ~$2.000 millones/año y 45 personas: "no lo sé". Ricardo tuvo la disciplina de no inventar los números, y eso vale. Pero el diagnóstico no es "falta de crecimiento", es **ceguera**. El dato no falta: está desconsolidado, repartido entre POS, Previred, el contador y las liquidaciones de apps. Es un problema de semanas, no de trimestres.
**Actualización 20-ago:** parcialmente refutada en su parte pesimista. El RCV del SII entregó en un día seis hallazgos (H-001 a H-005) que llevaban meses "desconocidos". El dato estaba a una descarga de distancia. Lo que falta ahora es específico y corto: P-003 y P-004.

---

## Prioridades vigentes (actualizadas 22-ago-2026 → 17-nov-2026)

Ordenadas por **valor en riesgo**, no por orden de aparición.

*Reordenadas el 23-ago-2026.*

| # | Qué | Por qué acá | Plazo |
|---|---|---|---|
| 3 | **H-018 — reimpresión masiva por cola fantasma** | La lista anti-duplicados vive en RAM. Un corte de luz reimprime boletas viejas en pleno servicio, y el Mall ya tiene el arranque automático puesto (S-012). **No activar más automatización de impresión hasta ver a `maximus-agent` sobrevivir un corte de luz real bajo PM2 (ver H-021)** | **Días** |
| 6 | **P-007 — control de reposiciones** | Pedido explícito de Ricardo. Primero medir la cobertura de `ReglaInsumo`; sin eso la alerta miente | 1-2 semanas |
| 7 | **P-002 — comisiones MP vs Transbank** | $20,5M/año. Una tarde | 1-2 semanas |
| 8 | **Bitácora de escalamientos (skill `viernes`)** | Corriendo. Clasificación los viernes. Veredicto de T-001 el 14-sep | Corriendo |
| 9 | **Tablero de gestión** | Ya no arranca de cero: H-001…H-005 y H-015 son la primera fila | 3-4 semanas |
| 10 | **Inventario — decidir si se instala (P-005)** | Sin esto la merma es inmedible. Antes probar la vía barata: cargar `Product.cost` (H-016) | 4-6 semanas |
| 11 | **P-011 — separar físicamente el historial privado** | El riesgo real ya se cerró con H-019. Esto endurece algo que hoy funciona. **Nunca un domingo con los locales abiertos** | Baja |
| 12 | **Segundo al mando** | Lead time largo, condicionado al veredicto de T-001 | Meses |
| 13 | **Congelar proyectos nuevos** | Hasta que 1-7 estén cerrados | Permanente |

**Nota 24-ago:** P-006 ya no debió figurar en esta tabla — cerrado desde el 20-ago
(ver `P-006.md` y la fila de cerrados más abajo). Quedó vivo por un desfase entre
la nota atómica y esta vista narrativa. Corregido acá; Ricardo lo reconfirmó hoy
sin que yo se lo pidiera, sin que aportara nada nuevo.

**Observación de Maximus sobre el 23-ago (domingo):** el día completo se fue en infraestructura del propio Maximus — despertar duplicado, micrófono, privacidad del panel, dos credenciales rotadas, dos horas de webhook caído. Se resolvieron cosas reales, incluidas dos exposiciones de credenciales. **Pero ninguna movió venta, margen ni dependencia**, y las tres prioridades de arriba de la lista siguen exactamente donde estaban el sábado. Es el patrón de T-001 —proyecto iniciado por Ricardo desplazando la prioridad declarada— y queda registrado para el veredicto del 14-sep.

**Cerrado el 26-ago-2026 — causa raíz encontrada tras tres repeticiones:**

- **P-008 punto 1 — "nada arranca solo".** Migrado a PM2 el 24-ago
  (`maximus-agent`, mismo mecanismo que `server6` y `voiceagentkit`). El
  zombi del puerto 8000 se repitió tres veces (24-ago con corte de luz,
  25-ago sin corte de luz) antes de encontrar la causa real: un
  `iniciar-agente.bat` **en la carpeta de Inicio de Windows** —no en las
  tareas programadas, por eso costó tanto verlo— que quedó de la carpeta
  abandonada `C:\Users\usuario\Desktop\dimango-app` (H-013) y lanzaba su
  propio Python en el puerto 8000 en cada arranque, por fuera de PM2.
  Movido a respaldo junto con dos scripts más redundantes. Detalle
  completo en `H-021.md` y `P-008.md`. **Único pendiente:** confirmarlo en
  el próximo reinicio real. **Telegram sigue sin responder**, sin
  investigar todavía.

**Cerrados el 23-ago-2026 (informado por Ricardo, autoridad 4):**

- **P-010 — filtración del Mall.** No hubo daño: el siniestro no se materializó. **Pero el valor de esa nota nunca fue el daño, era el documento**: Mallplaza dejó constancia por escrito de un defecto de aguas lluvias en el local que arrienda al 37,4% de su venta neta. Queda por confirmar si se respondió por escrito a Yanira Tara y si la carta está guardada donde se encuentre en noviembre.
- **D-006 — tótems.** Funcionando, los niños ya no salen de la app, y ahora envían respaldo por Telegram (pendiente registrar qué envían exactamente). **Sigue sin medirse la venta que se cae por sesiones abandonadas** — sin ese número no se puede justificar comprar más tótems ni retirarlos (L-003).

**Cerrados antes, se conservan por trazabilidad:**

| | Qué | Cómo cerró |
|---|---|---|
| ~~P-001~~ | contingencia de emisión DTE | 20-ago. SimpleFactura + emisión manual que los encargados saben usar. **El riesgo estaba sobreestimado por Maximus** (L-005). Queda el residual P-009 |
| ~~P-003~~ | venta de julio por local | 20-ago por **H-015**: Playa $100,04M / Mall $33,98M netos. Reveló que el arriendo del Mall es el 37,4% de su venta |
| ~~P-004~~ | costo laboral de julio | 20-ago por **H-011**: $30,27M líquido, 45 personas, $36-42M cargado |
| ~~P-006~~ | arriendo de Playa Chinchorro | 20-ago: Playa es propiedad de Ricardo, sin arriendo. Descarta el candidato #1 del residual de H-012 (ver `P-006.md`) |

**Fuera de la lista (resuelto):** "decidir arquitectura Toteat vs DiMangoToGo" — cerrado por D-008 el 30-jun-2026.

**Lo que NO es prioridad ahora:** Aurexgroup, marketing pagado (no se escala gasto sin conocer margen), tercer local, nuevas funcionalidades de DiMangoToGo que no sean corrección de fallas o el reset por código de /Kioskos.
