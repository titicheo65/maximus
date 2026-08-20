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

| Indicador | Estado | Por qué bloquea |
|---|---|---|
| Margen bruto | **DESCONOCIDO** | Sin esto no se sabe si crecer es rentable |
| Margen neto | **DESCONOCIDO** | Sin esto no se sabe si el negocio gana plata |
| Costo laboral como % de venta | **DESCONOCIDO** | Con 45 personas, es la variable que decide todo |
| Ticket promedio por local | **DESCONOCIDO** | Sin esto no hay palanca de ticket |
| N° de transacciones por local | **DESCONOCIDO** | Sin esto no hay palanca de volumen |
| Facturación y margen por local | **DESCONOCIDO** | No se sabe si un local subsidia al otro |
| % de venta por delivery y comisión efectiva | **DESCONOCIDO** | El margen real puede ser muy distinto al aparente |
| CAC / ROAS | **DESCONOCIDO** | No hay atribución |

**Rango de exposición del costo laboral (ARITMÉTICA, no dato):**

| Costo cargado promedio/trabajador | Costo laboral mensual | % de la venta |
|---|---|---|
| $700.000 | $31,5M | 19,2% |
| $900.000 | $40,5M | 24,7% |
| $1.100.000 | $49,5M | 30,2% |

La banda vale **$18 millones/mes = $216 millones/año.** Ricardo no sabe en qué punto está.

*Referencia de industria (a verificar contra sus datos, no asumir): en restaurante full-service el "prime cost" — insumos + mano de obra — suele manejarse bajo 60-65% de la venta. Si DiMango está sobre eso, crecer volumen empeora el resultado.*

## 4. Marketing (HECHO)

**$238.000 CLP/mes** = **0,145% de la venta** (ARITMÉTICA).

Fuentes de clientes, cualitativas, sin atribución: tránsito y ubicación · reconocimiento de marca · clientes recurrentes · recomendaciones · redes sociales · turistas · Playa Chinchorro · flujo propio del Mall Plaza.

**Lectura de Harvey:** no es un presupuesto de marketing, es un error de redondeo. La facturación la genera la ubicación, no la estrategia. Eso significa cero palancas propias de demanda: si el mall cambia el layout o abre un competidor cerca, no hay nada que accionar.

**Duda abierta:** los $238.000 probablemente están incompletos. Faltan por verificar: gestión de redes, diseño, y sobre todo **promociones y descuentos**, que en gastronomía suelen ser el mayor gasto real de marketing y nunca aparecen en esa línea.

## 5. Stack tecnológico (HECHO, con vacíos)

**POS y operación**
- **Toteat** — POS del restaurante
- **DiMangoToGo** — plataforma propia en desarrollo: pedidos, atención, caja, pagos, autoservicio
- **Base44** — plataforma sobre la que se desarrollan las apps y automatizaciones internas

**Pagos**
- Transbank (POS físicos, equipos nuevos en implementación) · Flow / Webpay · Onepay · Edenred Ticket Restaurant

**Pedidos / autoservicio**
- DiMangoToGo · tótem asociado a **Wibo**, soporte técnico derivado a **Remote Media**

**Impresión**
- Infraestructura propia local: servidor de impresión y dispositivos dentro de la red del restaurante, conectados a DiMangoToGo

**Marketing / web**
- dimango.cl · dimangotogo.com · Base44 SignBoard TV (**con fallas pendientes de corrección**)

**PENDIENTES CRÍTICOS — Ricardo debe confirmar los nombres:**
- Software contable → **PENDIENTE**
- Sistema de inventario (fuente única del dato) → **PENDIENTE**
- Sistema de RRHH / asistencia → **PENDIENTE**

Sin estos tres no se puede construir el tablero de gestión. Son la primera cosa a cerrar.

### Riesgos técnicos identificados

1. **Dos fuentes de verdad.** Toteat y DiMangoToGo conviven. Mientras eso siga, cualquier número de ventas es discutible y las integraciones seguirán frágiles por diseño, no por accidente.
2. **Punto único de falla humano.** Pagos, caja, comandas e impresión corren sobre software propio en desarrollo activo, sin segundo desarrollador y sin documentación de traspaso. Un día caído en ambos locales ≈ **$5,5 millones**. Una semana ≈ **$38 millones**. El plan de contingencia actual es Ricardo con el teléfono.
3. **Proveedores encadenados.** Tótem Wibo → soporte derivado a Remote Media. Cadena de soporte indirecta sobre un componente de venta.

## 6. Competencia (DÉBIL — declarado de memoria, sin datos)

- **Milkhouse** — competidor fuerte en heladería, propuesta concentrada en el producto helado, posicionamiento de categoría reconocido.
- **Helados La Fontana** — competidor histórico en heladería: tradición, reconocimiento, cliente local.
- **Patio gastronómico de Mall Plaza Arica** — en el local del mall el competidor no es un restaurante sino toda la oferta del espacio.

**Marco correcto que aportó Ricardo:** la competencia debe analizarse **por ocasión de consumo**, no por empresas que vendan lo mismo.

**PENDIENTE:** mapa competitivo real de Arica con precios, ticket, tráfico, Google, redes, producto y experiencia. Hoy este apartado es memoria, no inteligencia.

## 7. Números que Harvey debe vigilar

Ninguno está instrumentado todavía. Esta es la lista objetivo del tablero:

**Semanal:** venta por local · transacciones por local · ticket promedio por local · costo de insumos % · costo laboral % · **escalamientos a Ricardo (N° y tipo)**

**Mensual:** margen bruto por local · margen neto por local · prime cost % · mix por categoría · % y margen por canal (salón / retiro / delivery) · gasto de marketing real incluyendo descuentos · rotación de personal

**Trimestral:** avance de dependencia (¿cuántas decisiones dejaron de escalar?) · revisión de Aurexgroup
