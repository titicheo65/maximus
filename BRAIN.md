# BRAIN.md — Conocimiento operativo de DiMango

*Actualizado: 19 de agosto de 2026. Regla de este archivo: nada entra sin etiqueta de origen.*

---

## 1. Facturación (HECHO)

| Mes | Facturación CLP |
|---|---|
| Mayo 2026 | $176.633.829 |
| Junio 2026 | $152.203.686 |
| Julio 2026 | $163.552.687 |

- Promedio 3 meses: **$164.130.067/mes** (ARITMÉTICA)
- Run rate anualizado: **~$1.970 millones CLP/año** (ARITMÉTICA)
- Venta diaria promedio: **~$5.471.000 CLP/día**, ambos locales (ARITMÉTICA)

**Variaciones:** mayo→junio **−13,8%** · junio→julio **+7,5%** · julio sigue **−7,4%** bajo mayo.
**Causa de la caída de junio: NO VALIDADA.** Hipótesis abierta: estacionalidad de invierno y menor flujo turístico. Sin evidencia. Para cerrarla hay que comparar mismos meses 2024/2025, ventas por local, transacciones, ticket, días efectivos de operación, promociones extraordinarias.

## 2. Meta (HECHO, confirmada por Ricardo)

**$2.400 millones CLP anuales** = **$200 millones/mes**.

- Brecha vs. run rate actual: **+$35,87 millones/mes**, **+21,9%** (ARITMÉTICA)
- Brecha anual: **+$430 millones** (ARITMÉTICA)

Con dos locales en una ciudad de mercado finito, ese delta solo puede salir de tres lugares: **más transacciones**, **ticket más alto**, o **un canal/local nuevo**. No hay un cuarto. Ninguno está cuantificado hoy.

## 3. Lo que NO sabemos — la lista que bloquea todo

Ricardo no pudo responder ninguno de estos, y tuvo la disciplina de no inventarlos. Cada uno es prerrequisito de una decisión real:

*Actualizado 20-ago-2026 con los hallazgos del RCV del SII (ver `MEMORY.md` H-001 a H-007).*

| Indicador | Estado | Por qué bloquea |
|---|---|---|
| Costo de mercadería | **28,7% de la venta neta** (HECHO, RCV may-jul) — H-001. Es costo de **compra**, no de consumo: sin inventario no se conoce la merma | — |
| % de venta por delivery y comisión efectiva | **~1,0% de la venta** (HECHO, RCV) — H-005. Canal pequeño | — |
| Costo de medios de pago | **2,59% post-migración** (HECHO, julio) — H-002. Subió 1,04 pts = $20,5M/año | — |
| Costo laboral | **$30,27M líquido en julio, 45 personas** (HECHO, planilla) — H-011. Cargado estimado $36-42M = **~22-26% de la venta** | — |
| Prime cost | **≈57,7% de la venta neta** (ARITMÉTICA, H-011). **Bajo el umbral de 60-65%: está sano** | — |
| Margen bruto | **DESCONOCIDO** | Falta el consumo real (merma). El costo laboral ya está |
| Margen neto | **DESCONOCIDO, y faltan ~$36M/mes** — H-012 | Con el laboral ya restado, el residual sigue en 26% de la venta: implausible. ~$430M/año sin explicación |
| Facturación y margen por local | **DESCONOCIDO** — P-003 | No se sabe si un local subsidia al otro. Decide la viabilidad del Mall (H-003) |
| Ticket promedio por local | **DESCONOCIDO** — sale de P-003 | Sin esto no hay palanca de ticket |
| N° de transacciones por local | **DESCONOCIDO** — sale de P-003 | Sin esto no hay palanca de volumen |
| CAC / ROAS | **DESCONOCIDO** | No hay atribución. Con marketing en ~0,05% de la venta, es irrelevante hoy |

~~**Rango de exposición del costo laboral**~~ — **RESUELTO el 20-ago-2026.** La banda estimada era $31,5M–$49,5M. El dato real (julio, líquido) es **$30,27M**; cargado, **$36-42M**. La incertidumbre bajó de $18M/mes a ~$6M. Detalle por local y por puesto en `MEMORY.md` H-011.

*Referencia de industria (a verificar contra sus datos, no asumir): en restaurante full-service el "prime cost" — insumos + mano de obra — suele manejarse bajo 60-65% de la venta. Si DiMango está sobre eso, crecer volumen empeora el resultado.*

## 4. Marketing (HECHO)

**$238.000 CLP/mes** = **0,145% de la venta** (ARITMÉTICA).

Fuentes de clientes, cualitativas, sin atribución: tránsito y ubicación · reconocimiento de marca · clientes recurrentes · recomendaciones · redes sociales · turistas · Playa Chinchorro · flujo propio del Mall Plaza.

**Lectura de Maximus:** no es un presupuesto de marketing, es un error de redondeo. La facturación la genera la ubicación, no la estrategia. Eso significa cero palancas propias de demanda: si el mall cambia el layout o abre un competidor cerca, no hay nada que accionar.

**Duda abierta:** los $238.000 probablemente están incompletos. Faltan por verificar: gestión de redes, diseño, y sobre todo **promociones y descuentos**, que en gastronomía suelen ser el mayor gasto real de marketing y nunca aparecen en esa línea.

## 5. Stack tecnológico (HECHO, con vacíos)

**POS y operación**
- **DiMangoToGo** — plataforma propia: pedidos, atención, caja, pagos, autoservicio. **Fuente única desde el 1-jul-2026** (ver `MEMORY.md` D-008)
- **DiMangoWorking** (Base44, de Ricardo) — control de gestión y RRHH
- **Base44** — plataforma sobre la que se desarrollan las apps y automatizaciones internas
- ~~**Toteat**~~ — POS anterior, **terminado el 30-jun-2026**

**Pagos**
- Transbank (POS físicos, equipos nuevos en implementación) · Flow / Webpay · Onepay · Edenred Ticket Restaurant

**Pedidos / autoservicio**
- DiMangoToGo · tótem asociado a **Wibo**, soporte técnico derivado a **Remote Media**

**Impresión**
- Infraestructura propia local: servidor de impresión y dispositivos dentro de la red del restaurante, conectados a DiMangoToGo

**Marketing / web**
- dimango.cl · dimangotogo.com · Base44 SignBoard TV (**con fallas pendientes de corrección**)

**Los tres sistemas de gestión — resueltos el 20-ago-2026 (ver `MEMORY.md` P-005):**
- **Contable → no existe software. Son tres personas con tres funciones separadas** (HECHO, informado por Ricardo el 22-ago-2026):
  - **Carlos Jirón V.** (Soc. Ardiles & Jirón, Arica) — **IVA y renta**, N-006. Es quien trabaja sobre el **RCV del SII**, la fuente de H-001 a H-006.
  - **Carla Montoya** — **remuneraciones y liquidaciones**, N-002. Fuente humana de la planilla que cerró H-011.
  - **Cristian Vidal** — **no es contador**: vende una licencia, una vez al año, del software con que se generan las liquidaciones, N-003.

  **Los tres hacen contabilidad tributaria y laboral. Ninguno hace contabilidad de gestión:** nadie entrega margen por local ni prime cost semanal. Pendiente: acceso de consulta para Ricardo, y si la contabilidad va separada por local o consolidada. *(Corregido dos veces: el 20-ago decía que Cristian Vidal era el contador; el 21-ago que Carla llevaba el RCV. Las dos eran falsas.)*
- **RRHH / control de gestión → DiMangoWorking** (Base44, de Ricardo). Cae bajo L-002.
- **Inventario → NO EXISTE.** Consecuencia directa: compras ≠ consumo, **la merma es inmedible**, y el 28,7% de H-001 es costo de compra, no de consumo. El margen bruto real puede ser peor.

### Riesgos técnicos identificados

1. **Emisión de DTE sin contingencia — RIESGO N°1 (actualizado 20-ago-2026).** Desde el 1-jul no hay sistema alternativo. Si DiMangoToGo no emite, DiMango no vende legalmente: **~$5,5M/día**. Sin respuesta tras cuatro preguntas. Ver `MEMORY.md` P-001.
2. **Punto único de falla humano.** Pagos, caja, comandas e impresión corren sobre software propio en desarrollo activo, sin segundo desarrollador y sin documentación de traspaso. Una semana caído ≈ **$38 millones**. El plan de contingencia actual es Ricardo con el teléfono.
3. **Proveedores encadenados.** Tótem Wibo → soporte derivado a Remote Media. Cadena de soporte indirecta sobre un componente de venta.
4. ~~**Dos fuentes de verdad.**~~ **Resuelto por D-008** (Toteat terminó el 30-jun-2026). El costo de resolverlo fue quedarse sin red — de ahí el riesgo 1.

## 6. Competencia (DÉBIL — declarado de memoria, sin datos)

- **Milkhouse** — competidor fuerte en heladería, propuesta concentrada en el producto helado, posicionamiento de categoría reconocido.
- **Helados La Fontana** — competidor histórico en heladería: tradición, reconocimiento, cliente local.
- **Patio gastronómico de Mall Plaza Arica** — en el local del mall el competidor no es un restaurante sino toda la oferta del espacio.

**Marco correcto que aportó Ricardo:** la competencia debe analizarse **por ocasión de consumo**, no por empresas que vendan lo mismo.

**PENDIENTE:** mapa competitivo real de Arica con precios, ticket, tráfico, Google, redes, producto y experiencia. Hoy este apartado es memoria, no inteligencia.

## 7. Números que Maximus debe vigilar

Ninguno está instrumentado todavía. Esta es la lista objetivo del tablero:

**Semanal:** venta por local · transacciones por local · ticket promedio por local · costo de insumos % · costo laboral % · **escalamientos a Ricardo (N° y tipo)**

**Mensual:** margen bruto por local · margen neto por local · prime cost % · mix por categoría · % y margen por canal (salón / retiro / delivery) · gasto de marketing real incluyendo descuentos · rotación de personal

**Trimestral:** avance de dependencia (¿cuántas decisiones dejaron de escalar?) · revisión de Aurexgroup
