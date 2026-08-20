# MEMORY.md — Memoria de largo plazo

*Se actualiza cada vez que aprendemos algo importante. Lo más reciente arriba. Este archivo manda sobre los demás cuando hay conflicto.*

---

## Decisiones

### D-001 · Aurexgroup queda parqueado — 19-ago-2026
Ricardo decide enfocar 100% en DiMango. **Harvey está de acuerdo, y se lo gana así:** DiMango es el 100% de la caja y necesita sumar $430M/año; Aurexgroup no puede financiar eso en 12 meses ni en el mejor escenario.
**Condición:** parqueado ≠ abandonado. **Fecha de revisión obligatoria: 17 de noviembre de 2026.** Un proyecto sin fecha de revisión está abandonado con culpa, no parqueado.

### D-002 · Tesis de Aurexgroup corregida — 19-ago-2026
Ricardo mejoró la tesis original y esta es la versión vigente:

> Problema real detectado en DiMango → solución → validación interna → simplificación/estandarización → **instalación en un negocio externo sin intervención de Ricardo** → medición → recién entonces producto validado.

**Criterio de comercializabilidad (regla dura):** una solución solo es producto si un tercero puede instalarla, operarla y mantenerla **sin depender de Ricardo** para configurarla, corregirla o mantenerla viva. DiMango es laboratorio de descubrimiento y primera validación, nunca la prueba final.

### D-003 · Meta DiMango confirmada — 19-ago-2026
$2.400 millones CLP anuales ($200M/mes). +21,9% sobre run rate. La meta original escrita ("2.400.000 anual") era un error de unidades y quedó corregida.

### D-004 · Orden de las tres decisiones pospuestas — 19-ago-2026
Ricardo las listó: 1) salir del centro, 2) arquitectura tecnológica, 3) tablero de gestión.
**Harvey las reordena:** el tablero no es tercero, es **condición del primero**. No se puede delegar lo que no se puede medir; delegar sin métricas es abdicar, y en 60 días Ricardo vuelve al centro apagando el incendio que causó su propia delegación a ciegas.

Pero no van en fila india — tienen lead times distintos y arrancan **en paralelo**:

| Decisión | Quién ejecuta | Lead time |
|---|---|---|
| Segundo al mando | Ricardo, exclusivamente | 3-6 meses |
| Tablero de gestión | Harvey, mayormente | 3-4 semanas |
| Arquitectura definitiva | Ricardo + proveedor | 2-3 meses |

La búsqueda del #2 empieza primero porque tarda más. Cuando llegue, el tablero ya existe y es el instrumento con el que se le hace responsable desde el día uno.

---

## Abierto — requiere decisión de Ricardo

### D-005 · El objetivo de 90 días no es un objetivo todavía
"Reducir la dependencia operativa" con ocho subcomponentes es un programa, no un objetivo. No tiene métrica ni fecha de verificación.
**Propuesta de Harvey:** convertirlo en un compromiso fechado y falsable —
> **Del 9 al 15 de noviembre de 2026, DiMango opera 7 días corridos sin que Ricardo resuelva una sola decisión operacional.**

Y desde esta semana, el instrumento que lo hace medible: **bitácora de escalamientos.** Cada vez que algo llega a Ricardo se registra fecha, quién, qué decisión, por qué llegó a él. No se puede reducir lo que no se cuenta — y esa bitácora, sola, es el mapa exacto de qué delegar y a quién.
**Estado: pendiente de aceptación.**

### T-001 · Tesis rival: no necesita un #2, necesita cerrar proyectos
Un observador competente diría que el problema de Ricardo no es falta de estructura sino exceso de iniciativas simultáneas — él mismo escribió "probablemente tengo más proyectos de los que debería ejecutar".
Un #2 cuesta $2-3M/mes y tarda 6 meses en ser útil. Cortar la cartera de proyectos a la mitad es gratis y funciona el lunes siguiente.
**Es más barata de probar y podría ser la correcta.** No se descarta. Se resuelve con la evidencia de la bitácora de escalamientos: si la mayoría de los escalamientos son proyectos que Ricardo mismo inició, la tesis rival gana.
**Estado: sin resolver.**

### P-001 · Confirmar software contable, de inventario y de RRHH
Bloquea la construcción del tablero. Es lo primero.

---

## Lecciones

### L-001 · DiMango no está instrumentado — 19-ago-2026
Cinco de seis preguntas financieras fundamentales sobre un negocio de ~$2.000 millones/año y 45 personas: "no lo sé". Ricardo tuvo la disciplina de no inventar los números, y eso vale. Pero el diagnóstico no es "falta de crecimiento", es **ceguera**. El dato no falta: está desconsolidado, repartido entre POS, Previred, el contador y las liquidaciones de apps. Es un problema de semanas, no de trimestres.

### L-002 · La automatización está profundizando el cuello de botella que dice resolver — 19-ago-2026
Cada componente que Ricardo agrega —Base44, DiMangoToGo, servidor de impresión propio, tótem, cuatro medios de pago, Toteat en paralelo— es una pieza más que **solo él entiende**. Está reemplazando dependencia de personas por dependencia de sistemas que dependen de una sola persona.
**Regla derivada:** automatización que solo Ricardo puede mantener no es automatización, es una dependencia nueva con mejor interfaz. Toda iniciativa técnica debe pasar el test de D-002.

### L-003 · No se puede justificar automatización sin conocer el costo que ahorra — 19-ago-2026
Tótems, autoservicio y reducción de cajas se justifican con un ahorro de costo laboral que hoy es **inmedible**, porque no existe el costo laboral %. Cuando el tótem funcione no habrá forma de decir si ahorró $4M o costó $2M. Y sin ese número, Aurexgroup tampoco tiene caso de venta: no se puede vender un ROI que no se midió en el propio laboratorio.

---

## Prioridades vigentes (19-ago-2026 → 17-nov-2026)

1. **Cerrar los pendientes de sistemas** (contable, inventario, RRHH) — días
2. **Bitácora de escalamientos** — arranca esta semana, costo cero
3. **Tablero de gestión con los 8 indicadores ciegos** — 3-4 semanas
4. **Búsqueda/desarrollo del segundo al mando** — arranca ya, madura en meses
5. **Decidir arquitectura: Toteat o DiMangoToGo como fuente única** — 2-3 meses
6. **Plan de contingencia técnica** (documentación + segundo par de manos) — riesgo vivo de $5,5M/día
7. **Congelar proyectos nuevos** hasta que 1-4 estén en marcha

**Lo que NO es prioridad ahora:** Aurexgroup, marketing pagado (no se escala gasto sin conocer margen), tercer local, nuevas funcionalidades de DiMangoToGo que no sean corrección de fallas.
