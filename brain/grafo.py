#!/usr/bin/env python3
"""
Lee las notas atómicas de memoria/ y genera:
  - memoria/indice.json  → nodos y aristas, para búsqueda y recuperación
  - brain/cerebro.html   → visualizador autocontenido (se abre sin servidor)

No depende de nada externo: ni librerías, ni CDN, ni internet.
Los datos van embebidos en el HTML, así que el archivo no sale de tu disco.
"""

import base64
import json
import re
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MEM = BASE / "memoria"
CARA = BASE / "brain" / "cara.jpg"

COLORES = {
    "decision": "#f5a623",   # ámbar
    "hallazgo": "#4a9eff",   # azul
    "pendiente": "#ff5f56",  # rojo
    "leccion": "#27c93f",    # verde
    "tesis": "#bd93f9",      # violeta
    "escalamiento": "#ff79c6",
    "persona": "#ffffff",    # blanco
    "sistema": "#ff8c42",    # naranjo
    "metrica": "#50e3c2",    # turquesa
    "regla": "#8be9fd",
    "personal": "#f1fa8c",
}


def parse_nota(ruta: Path) -> dict | None:
    txt = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m:
        return None
    front, cuerpo = m.group(1), m.group(2).strip()

    meta, clave_actual = {}, None
    for linea in front.split("\n"):
        if not linea.strip():
            continue
        if linea.startswith("  "):                       # sub-clave de enlaces
            sm = re.match(r"\s+(\w+):\s*(.*)", linea)
            if sm and clave_actual == "enlaces":
                destinos = [d.strip() for d in sm.group(2).strip("[]").split(",") if d.strip()]
                meta.setdefault("enlaces", {})[sm.group(1)] = destinos
            continue
        km = re.match(r"(\w+):\s*(.*)", linea)
        if not km:
            continue
        clave, valor = km.group(1), km.group(2).strip()
        clave_actual = clave
        if clave == "enlaces":
            meta["enlaces"] = {}
        elif valor.startswith("[") and valor.endswith("]"):
            meta[clave] = [v.strip() for v in valor[1:-1].split(",") if v.strip()]
        else:
            meta[clave] = valor.strip('"')
    meta["cuerpo"] = cuerpo
    return meta


def main():
    notas = {}
    for f in sorted(MEM.glob("*.md")):
        d = parse_nota(f)
        if d:
            notas[f.stem] = d

    nodos, aristas = [], []
    grados = {k: 0 for k in notas}

    for nid, n in notas.items():
        for rel, destinos in (n.get("enlaces") or {}).items():
            for dst in destinos:
                if dst in notas:                          # solo aristas resueltas
                    aristas.append({"de": nid, "a": dst, "rel": rel})
                    grados[nid] += 1
                    grados[dst] += 1

    for nid, n in notas.items():
        tipo = n.get("tipo", "otro")
        nodos.append({
            "id": nid,
            "tipo": tipo,
            "titulo": n.get("titulo", nid),
            "estado": n.get("estado", ""),
            "autoridad": int(n.get("autoridad", 5) or 5),
            "fuente": n.get("fuente", ""),
            "fecha": n.get("fecha_hecho", n.get("fecha_registro", "")),
            "tags": n.get("tags", []),
            "cuerpo": n.get("cuerpo", ""),
            "origen": n.get("origen", ""),
            "grado": grados[nid],
            "color": COLORES.get(tipo, "#888"),
        })

    huerfanos = [n["id"] for n in nodos if n["grado"] == 0]
    rotos = []
    for nid, n in notas.items():
        for rel, destinos in (n.get("enlaces") or {}).items():
            for dst in destinos:
                if dst not in notas:
                    rotos.append(f"{nid} --{rel}--> {dst}")

    # La fecha se toma del reloj: escrita a mano miente en cuanto alguien
    # regenera el índice sin acordarse de cambiarla.
    indice = {"nodos": nodos, "aristas": aristas,
              "generado": date.today().isoformat(),
              "huerfanos": huerfanos, "enlaces_rotos": rotos}
    (MEM / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")

    # La cara va embebida como el resto: el HTML tiene que seguir abriéndose
    # con doble clic, sin servidor y sin archivos sueltos al lado.
    # Si no está el archivo, el avatar simplemente no aparece.
    cara = base64.b64encode(CARA.read_bytes()).decode() if CARA.exists() else ""

    html = (PLANTILLA
            .replace("__DATOS__", json.dumps(indice, ensure_ascii=False))
            .replace("__CARA__", cara))
    (BASE / "brain" / "cerebro.html").write_text(html, encoding="utf-8")

    print(f"{len(nodos)} nodos · {len(aristas)} conexiones")
    print(f"huérfanos (sin ninguna conexión): {len(huerfanos)} {huerfanos if huerfanos else ''}")
    print(f"enlaces a notas que aún no existen: {len(rotos)}")
    for r in rotos[:12]:
        print(f"   {r}")
    top = sorted(nodos, key=lambda n: -n["grado"])[:6]
    print("\nlos más conectados:")
    for n in top:
        print(f"   {n['id']:7} {n['grado']:2} conexiones — {n['titulo'][:52]}")


PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Cerebro de Maximus</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#07080c;color:#dfe3ea;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden}
#lienzo{position:fixed;inset:0;cursor:grab}#lienzo:active{cursor:grabbing}
.panel{position:fixed;top:64px;bottom:0;width:330px;background:rgba(12,14,20,.93);backdrop-filter:blur(14px);
 border-right:1px solid #1c2030;padding:20px;overflow-y:auto;z-index:10}

/* ── HUD superior ── */
#hud{position:fixed;top:0;left:0;right:0;height:64px;z-index:22;display:flex;align-items:stretch;
 background:linear-gradient(180deg,rgba(10,12,18,.98),rgba(10,12,18,.92));
 border-bottom:1px solid #1c2030;backdrop-filter:blur(16px);font-variant-numeric:tabular-nums}
.reloj{flex:0 0 auto;padding:9px 20px;border-right:1px solid #14171f;display:flex;flex-direction:column;
 justify-content:center;min-width:132px}
.reloj .ciu{font-size:9px;letter-spacing:.16em;color:#4d5566;font-weight:600;margin-bottom:1px}
.reloj .hr{font-size:19px;color:#dfe3ea;font-family:ui-monospace,Menlo,monospace;line-height:1.15}
.reloj .hr .seg{font-size:11px;color:#4d5566}
.reloj .tmp{font-size:10.5px;color:#7d8698;margin-top:1px}
.reloj.local{background:rgba(245,166,35,.05)}
.reloj.local .ciu{color:#f5a623}
.reloj.noche .hr{color:#8b93a3}
#ind{flex:1;padding:9px 22px;display:flex;flex-direction:column;justify-content:center;gap:3px;min-width:0}
#ind .fila1,#ind .fila2{display:flex;gap:20px;flex-wrap:wrap;font-size:11px;white-space:nowrap}
#ind b{color:#dfe3ea;font-family:ui-monospace,Menlo,monospace;font-weight:500}
#ind .k{color:#4d5566}
#ind .alerta{color:#ff8fa3}
#ind .ok{color:#4a9e6f}
#hud{overflow-x:auto;scrollbar-width:none}
#hud::-webkit-scrollbar{display:none}
@media(max-width:1250px){
  .reloj{min-width:108px;padding:9px 13px}
  .reloj .hr{font-size:17px} .reloj .hr .seg{display:none}
  #ind{padding:9px 14px;min-width:280px}
  #ind .fila1,#ind .fila2{gap:13px;font-size:10.5px}
}
.panel.der{right:0;left:auto;border-right:0;border-left:1px solid #1c2030;width:220px}
h1{font-size:15px;letter-spacing:.14em;color:#f5a623;margin-bottom:2px;font-weight:600}
.sub{font-size:11px;color:#5c6478;margin-bottom:18px}
input{width:100%;background:#12151f;border:1px solid #232838;border-radius:9px;padding:9px 12px;
 color:#dfe3ea;font-size:13px;margin-bottom:16px;outline:none}
input:focus{border-color:#f5a623}
.tit{font-size:10px;letter-spacing:.13em;color:#4d5566;margin:18px 0 9px;font-weight:600}
.fila{display:flex;justify-content:space-between;align-items:center;padding:5px 8px;border-radius:6px;
 cursor:pointer;font-size:12px}
.fila:hover{background:#171b26}
.punto{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:8px;flex:none}
.n{color:#4d5566;font-size:11px}
#insp{background:#0e1118;border:1px solid #1c2030;border-radius:11px;padding:14px;font-size:12.5px}
#insp h3{font-size:13.5px;color:#fff;margin-bottom:7px;line-height:1.35}
#insp .meta{font-size:10.5px;color:#5c6478;margin-bottom:10px;line-height:1.7}
#insp .cuerpo{color:#aab2c0;font-size:12px;line-height:1.65;max-height:340px;overflow-y:auto;
 white-space:pre-wrap;border-top:1px solid #1c2030;padding-top:10px;margin-top:4px}
#insp table{font-size:11px;border-collapse:collapse;margin:6px 0}
#insp td,#insp th{border:1px solid #232838;padding:3px 6px}
.chip{display:inline-block;background:#171b26;border-radius:4px;padding:1px 6px;font-size:10px;
 color:#7d8698;margin:2px 3px 0 0}
.enl{cursor:pointer;color:#4a9eff}.enl:hover{text-decoration:underline}
.aut{display:inline-block;padding:1px 6px;border-radius:4px;font-size:10px;font-weight:600}
.a1{background:#0d4f2c;color:#5ef58f}.a2{background:#0d3a5f;color:#6cc4ff}
.a3{background:#5f4a0d;color:#ffd166}.a4{background:#5f2f0d;color:#ffa06c}
.a5{background:#4a1420;color:#ff8fa3}
#pie{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);font-size:11px;color:#3d4454;z-index:10}
#barra{position:fixed;bottom:46px;left:50%;transform:translateX(-50%);z-index:15;
 width:min(620px,72vw);display:flex;align-items:center;gap:10px}
#chat{flex:1;background:rgba(14,17,24,.94);border:1px solid #232838;border-radius:22px;
 padding:12px 20px;color:#dfe3ea;font-size:13.5px;outline:none;backdrop-filter:blur(10px)}
#chat:focus{border-color:#f5a623}
#estado{font-size:11px;color:#f5a623;white-space:nowrap;min-width:60px}
#btnvoz{background:rgba(14,17,24,.94);border:1px solid #232838;border-radius:50%;width:40px;height:40px;
 font-size:16px;cursor:pointer;color:#4d5566;flex:none;opacity:.45}
#btnvoz.on{border-color:#f5a623;color:#f5a623;opacity:1}
#btnmic,#btnojo{background:rgba(14,17,24,.94);border:1px solid #232838;border-radius:50%;width:40px;height:40px;
 font-size:16px;cursor:pointer;color:#4d5566;flex:none;opacity:.45}
#btnojo:hover{border-color:#50e3c2;color:#50e3c2;opacity:1}
#btnojo.on{border-color:#50e3c2;color:#50e3c2;opacity:1}
#btnmic.on{border-color:#ff5f56;color:#ff5f56;opacity:1;animation:lat 1.4s ease-in-out infinite}
@keyframes lat{0%,100%{box-shadow:0 0 0 0 rgba(255,95,86,.5)}50%{box-shadow:0 0 0 9px rgba(255,95,86,0)}}
#cfg{position:fixed;top:78px;right:14px;z-index:20;background:#171b26;border:1px solid #f5a623;
 color:#f5a623;border-radius:8px;padding:7px 14px;font-size:12px;cursor:pointer;font-weight:600}
#cfg:hover{background:#f5a623;color:#07080c}
#cfg.ok{border-color:#2a4a3a;color:#4a9e6f;font-weight:400}
#cfgpanel{display:none;position:fixed;top:56px;right:14px;z-index:25;width:min(400px,88vw);
 background:rgba(14,17,24,.98);border:1px solid #f5a623;border-radius:12px;padding:18px;
 backdrop-filter:blur(14px)}
#cfgpanel .ct{font-size:10px;letter-spacing:.13em;color:#f5a623;font-weight:600;margin-bottom:14px}
#cfgpanel label{display:block;font-size:11px;color:#7d8698;margin-bottom:5px}
#cfgpanel input{width:100%;margin-bottom:14px;font-family:ui-monospace,Menlo,monospace;font-size:12px}
#cfgpanel button{background:#f5a623;color:#07080c;border:0;border-radius:7px;padding:8px 18px;
 font-size:12.5px;font-weight:600;cursor:pointer;margin-right:8px}
#cfgpanel button.sec{background:#232838;color:#9aa3b2;font-weight:400}
#cfgmsg{font-size:11.5px;color:#ff8fa3;margin-bottom:12px;line-height:1.5}
/* ── el perro ── */
#cara{position:fixed;bottom:100px;left:50%;transform:translateX(-50%);z-index:17;
 width:136px;height:136px;cursor:pointer;filter:drop-shadow(0 10px 26px rgba(0,0,0,.65))}
#cara canvas{display:block;width:136px;height:136px}
#cara:hover{filter:drop-shadow(0 10px 26px rgba(245,166,35,.4))}
@media(max-width:900px){#cara{width:104px;height:104px;bottom:96px}
 #cara canvas{width:104px;height:104px}}
@media(max-width:760px){#cara{display:none}}

#rta{position:fixed;bottom:250px;left:50%;transform:translateX(-50%);z-index:15;
 width:min(620px,72vw);background:rgba(14,17,24,.96);border:1px solid #2a4a3a;border-radius:12px;
 padding:16px 20px;font-size:13px;line-height:1.65;color:#c3cad6;white-space:pre-wrap;
 max-height:38vh;overflow-y:auto;display:none;backdrop-filter:blur(14px)}
#ocultar{position:fixed;top:14px;left:14px;z-index:20;background:#171b26;border:1px solid #232838;
 color:#7d8698;border-radius:7px;padding:5px 10px;font-size:12px;cursor:pointer;display:none}
body.sinpaneles .panel{display:none} body.sinpaneles #ocultar{background:#f5a623;color:#07080c}
@media(max-width:900px){.panel{width:260px;padding:14px} .panel.der{display:none} #ocultar{display:block}}
@media(max-width:760px){.panel{width:100%;height:52vh;bottom:auto;top:auto;bottom:0;border-top:1px solid #1c2030}}
</style></head><body>
<div id="hud">
  <div class="reloj local" data-tz="America/Santiago"><div class="ciu">ARICA</div><div class="hr">—</div><div class="tmp">—</div></div>
  <div class="reloj" data-tz="America/New_York"><div class="ciu">WASHINGTON</div><div class="hr">—</div><div class="tmp">—</div></div>
  <div class="reloj" data-tz="Europe/Madrid"><div class="ciu">MADRID</div><div class="hr">—</div><div class="tmp">—</div></div>
  <div class="reloj" data-tz="Europe/Rome"><div class="ciu">MILANO</div><div class="hr">—</div><div class="tmp">—</div></div>
  <div id="ind">
    <div class="fila1"><span class="k">cargando indicadores…</span></div>
    <div class="fila2"></div>
  </div>
</div>

<canvas id="lienzo"></canvas>
<button id="ocultar" onclick="document.body.classList.toggle('sinpaneles');setTimeout(ajustar,60)">☰ paneles</button>

<div class="panel">
  <h1>CEREBRO DE MAXIMUS</h1>
  <div class="sub" id="cuenta"></div>
  <input id="buscar" placeholder="Buscar en el cerebro…" autocomplete="off">
  <div id="resultados"></div>
  <div class="tit">INSPECTOR</div>
  <div id="insp"><div style="color:#4d5566;font-size:12px">Haz clic en un nodo para leerlo.
  Solo ese nodo y sus conexiones quedan iluminados.</div></div>
  <div class="tit">MÁS CONECTADOS</div>
  <div id="hubs"></div>
</div>

<div class="panel der">
  <div class="tit">TIPOS</div><div id="tipos"></div>
  <div class="tit">AUTORIDAD DE FUENTE</div>
  <div style="font-size:10.5px;color:#5c6478;line-height:1.9">
    <span class="aut a1">1</span> sistema oficial<br>
    <span class="aut a2">2</span> exportación directa<br>
    <span class="aut a3">3</span> planilla interna<br>
    <span class="aut a4">4</span> informado<br>
    <span class="aut a5">5</span> estimación
  </div>
</div>

<div id="barra">
  <input id="chat" placeholder="Pregúntale a Maximus…  (Enter para enviar)" autocomplete="off">
  <button id="btnojo" onclick="mirarPantalla()" title="Que Maximus mire tu pantalla">👁</button>
  <button id="btnmic" onclick="alternarMic()" title="Hablarle a Maximus">🎤</button>
  <button id="btnvoz" onclick="alternarVoz()" title="Que Maximus conteste hablando">🔊</button>
  <span id="estado"></span>
</div>
<div id="rta"></div>
<div id="cara" title="Háblale a Maximus"><canvas id="caralienzo"></canvas></div>

<button id="cfg" onclick="configurar()">⚙ conexión</button>
<div id="cfgpanel">
  <div class="ct">CONEXIÓN CON MAXIMUS</div>
  <label>URL del agente</label>
  <input id="cfgurl" spellcheck="false">
  <label>Token de chat — solo la línea verde que imprime el servidor</label>
  <input id="cfgtok" spellcheck="false" placeholder="k7Rm2xQp9nT4wZ8vB3jL6dH5sA2e">
  <div id="cfgmsg"></div>
  <button onclick="guardarCfg()">Guardar</button>
  <button class="sec" onclick="document.getElementById('cfgpanel').style.display='none'">Cancelar</button>
</div>
<div id="pie">arrastra para mover · rueda para acercar · clic en un nodo para leerlo ·
 <span onclick="ajustar()" style="color:#f5a623;cursor:pointer">⊙ ajustar (F)</span></div>

<script>
const D = __DATOS__;
const c = document.getElementById('lienzo'), x = c.getContext('2d');
let W, H; function medir(){W=c.width=innerWidth;H=c.height=innerHeight} medir(); onresize=medir;

const N = D.nodos, A = D.aristas;
const idx = {}; N.forEach((n,i)=>{idx[n.id]=i; n.x=W/2+(Math.random()-.5)*420; n.y=H/2+(Math.random()-.5)*420; n.vx=0; n.vy=0;});
const vecinos = {}; N.forEach(n=>vecinos[n.id]=new Set());
A.forEach(a=>{vecinos[a.de].add(a.a); vecinos[a.a].add(a.de)});

let cam={x:0,y:0,z:1}, sel=null, oculto=new Set(), resaltados=null;

// ── layout: repulsión + resortes ──
function paso(){
  for(let i=0;i<N.length;i++){
    const a=N[i]; if(oculto.has(a.tipo))continue;
    for(let j=i+1;j<N.length;j++){
      const b=N[j]; if(oculto.has(b.tipo))continue;
      let dx=b.x-a.x, dy=b.y-a.y, d2=dx*dx+dy*dy||1, d=Math.sqrt(d2);
      if(d>420)continue;
      const f=2400/d2, fx=dx/d*f, fy=dy/d*f;
      a.vx-=fx; a.vy-=fy; b.vx+=fx; b.vy+=fy;
    }
    a.vx += (W/2-a.x)*0.0007; a.vy += (H/2-a.y)*0.0007;
  }
  A.forEach(e=>{
    const a=N[idx[e.de]], b=N[idx[e.a]];
    if(!a||!b||oculto.has(a.tipo)||oculto.has(b.tipo))return;
    let dx=b.x-a.x, dy=b.y-a.y, d=Math.hypot(dx,dy)||1;
    const f=(d-125)*0.010, fx=dx/d*f, fy=dy/d*f;
    a.vx+=fx; a.vy+=fy; b.vx-=fx; b.vy-=fy;
  });
  N.forEach(n=>{n.vx*=0.85; n.vy*=0.85; n.x+=n.vx; n.y+=n.vy});
}

const radio = n => 5 + Math.min(n.grado,12)*1.5;

function pintar(){
  x.clearRect(0,0,W,H);
  x.save(); x.translate(cam.x,cam.y); x.scale(cam.z,cam.z);

  A.forEach(e=>{
    const a=N[idx[e.de]], b=N[idx[e.a]];
    if(!a||!b||oculto.has(a.tipo)||oculto.has(b.tipo))return;
    const act = !resaltados || (resaltados.has(e.de)&&resaltados.has(e.a));
    x.strokeStyle = act ? 'rgba(90,150,120,.42)' : 'rgba(60,66,80,.08)';
    x.lineWidth = act ? 1 : .5;
    x.beginPath(); x.moveTo(a.x,a.y); x.lineTo(b.x,b.y); x.stroke();
  });

  N.forEach(n=>{
    if(oculto.has(n.tipo))return;
    const act = !resaltados || resaltados.has(n.id), r=radio(n);
    x.globalAlpha = act ? 1 : .13;
    x.beginPath(); x.arc(n.x,n.y,r,0,7); x.fillStyle=n.color; x.fill();
    if(n.id===sel){x.strokeStyle='#fff'; x.lineWidth=2; x.stroke()}
    if(cam.z>0.62 && (act||!resaltados)){
      x.fillStyle = act?'#c9d1de':'#3d4454';
      x.font = (n.grado>4?'600 ':'')+ (10/Math.max(cam.z,.75)*cam.z+2) +'px -apple-system,sans-serif';
      x.textAlign='center'; x.fillText(n.id, n.x, n.y-r-5);
    }
    x.globalAlpha=1;
  });
  x.restore();
}

// encuadra todo lo visible en el área libre entre los dos paneles
function ajustar(){
  const vis = N.filter(n=>!oculto.has(n.tipo));
  if(!vis.length) return;
  const xs=vis.map(n=>n.x), ys=vis.map(n=>n.y);
  const x0=Math.min(...xs), x1=Math.max(...xs), y0=Math.min(...ys), y1=Math.max(...ys);
  // los paneles se encogen en ventanas angostas; el área libre nunca es negativa
  const izq = W<900 ? 0 : 345, der = W<760 ? 0 : (W<900 ? 150 : 235), mg=50, hud=64;
  // 250 abajo: barra de chat + la cara del perro. Los nodos no se esconden detrás.
  const dispW=Math.max(W-izq-der-mg*2, 220), dispH=Math.max(H-hud-mg*2-250, 200);
  cam.z=Math.max(0.12, Math.min(dispW/Math.max(x1-x0,1), dispH/Math.max(y1-y0,1), 1.7));
  cam.x=izq+mg+(dispW-(x1-x0)*cam.z)/2-x0*cam.z;
  cam.y=hud+mg+(dispH-(y1-y0)*cam.z)/2-y0*cam.z;
}

for(let i=0;i<400;i++) paso();   // estabilizar antes de mostrar
ajustar();

// El bucle se ARRANCA al final del archivo, no aquí: pintarCara() usa
// constantes declaradas más abajo, y tocarlas antes de tiempo lanza una
// excepción que corta el requestAnimationFrame y congela el grafo entero.
function bucle(){ paso(); pintar(); pintarCara(); requestAnimationFrame(bucle) }

// ── interacción ──
let arrastre=false, px=0, py=0, movido=0;
c.onmousedown=e=>{arrastre=true;px=e.clientX;py=e.clientY;movido=0};
onmouseup=()=>arrastre=false;
onmousemove=e=>{ if(!arrastre)return; const dx=e.clientX-px, dy=e.clientY-py;
  movido+=Math.abs(dx)+Math.abs(dy); cam.x+=dx; cam.y+=dy; px=e.clientX; py=e.clientY };
c.onwheel=e=>{e.preventDefault(); const f=e.deltaY<0?1.11:0.9;
  cam.x=e.clientX-(e.clientX-cam.x)*f; cam.y=e.clientY-(e.clientY-cam.y)*f; cam.z*=f};
c.onclick=e=>{
  if(movido>6)return;
  const mx=(e.clientX-cam.x)/cam.z, my=(e.clientY-cam.y)/cam.z;
  let mejor=null, dm=1e9;
  N.forEach(n=>{ if(oculto.has(n.tipo))return;
    const d=Math.hypot(n.x-mx,n.y-my); if(d<radio(n)+9 && d<dm){dm=d;mejor=n} });
  mejor ? abrir(mejor.id) : (sel=null, resaltados=null, mostrar(null));
};

function abrir(id){
  sel=id; resaltados=new Set([id,...vecinos[id]]); mostrar(N[idx[id]]);
  const n=N[idx[id]]; cam.x=W/2-n.x*cam.z; cam.y=H/2-n.y*cam.z;
}

function mostrar(n){
  const el=document.getElementById('insp');
  if(!n){el.innerHTML='<div style="color:#4d5566;font-size:12px">Haz clic en un nodo para leerlo.</div>';return}
  const conex=[...vecinos[n.id]];
  el.innerHTML=`<h3>${n.id} · ${n.titulo}</h3>
   <div class="meta">
     <span class="aut a${n.autoridad}">autoridad ${n.autoridad}</span>
     &nbsp;${n.fuente} &nbsp;·&nbsp; ${n.estado} &nbsp;·&nbsp; ${n.fecha}<br>
     ${n.origen?'<span style="color:#454c5e">'+n.origen+'</span><br>':''}
     ${n.tags.map(t=>'<span class="chip">'+t+'</span>').join('')}
   </div>
   <div class="cuerpo">${n.cuerpo.replace(/[&<>]/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[s]))}</div>
   <div class="tit" style="margin-top:12px">CONECTA CON ${conex.length}</div>
   ${conex.map(id=>{const v=N[idx[id]]; return v?`<div class="fila" onclick="abrir('${id}')">
     <span><span class="punto" style="background:${v.color}"></span>${id}</span>
     <span class="n">${v.titulo.slice(0,26)}</span></div>`:''}).join('')}`;
}

// ── paneles ──
const tipos={}; N.forEach(n=>tipos[n.tipo]=(tipos[n.tipo]||0)+1);
document.getElementById('cuenta').textContent=`${N.length} notas · ${A.length} conexiones`;
document.getElementById('tipos').innerHTML=Object.entries(tipos).sort((a,b)=>b[1]-a[1])
 .map(([t,n])=>`<div class="fila" onclick="alternar('${t}',this)">
   <span><span class="punto" style="background:${N.find(x=>x.tipo===t).color}"></span>${t}</span>
   <span class="n">${n}</span></div>`).join('');
document.getElementById('hubs').innerHTML=[...N].sort((a,b)=>b.grado-a.grado).slice(0,8)
 .map(n=>`<div class="fila" onclick="abrir('${n.id}')">
   <span><span class="punto" style="background:${n.color}"></span>${n.id}</span>
   <span class="n">${n.grado}</span></div>`).join('');

function alternar(t,el){ oculto.has(t)?oculto.delete(t):oculto.add(t);
  el.style.opacity = oculto.has(t)?.32:1; setTimeout(ajustar,120) }
window.ajustar=ajustar;
addEventListener('keydown',e=>{ if(e.key==='f'||e.key==='F') ajustar();
  if(e.key==='Escape'){sel=null;resaltados=null;mostrar(null)} });

document.getElementById('buscar').oninput=e=>{
  const q=e.target.value.toLowerCase().trim();
  const r=document.getElementById('resultados');
  if(q.length<2){r.innerHTML='';return}
  const hits=N.filter(n=>(n.id+' '+n.titulo+' '+n.tags.join(' ')+' '+n.cuerpo).toLowerCase().includes(q)).slice(0,14);
  r.innerHTML=hits.length?hits.map(n=>`<div class="fila" onclick="abrir('${n.id}')">
    <span><span class="punto" style="background:${n.color}"></span>${n.id}</span>
    <span class="n">${n.titulo.slice(0,28)}</span></div>`).join('')
   :'<div style="color:#4d5566;font-size:12px;padding:6px">Sin resultados.</div>';
};
window.abrir=abrir; window.alternar=alternar;

// ── chat con Maximus ──────────────────────────────────────────────
// El token no viaja dentro del archivo: se pide una vez y queda en este
// navegador. Así el .html se puede copiar o mandar sin llevar la llave.
// Si el cerebro se sirve por http (servidor.py en localhost), se le habla al
// agente por el MISMO origen: ese servidor hace de puente. Así no hay CORS, y
// sobre todo Chrome recuerda el permiso del micrófono — en file:// lo pide en
// cada turno y no se puede conversar de corrido. Abierto como archivo, se va
// directo al túnel, como siempre.
const DEFECTO = location.protocol.startsWith('http')
  ? location.origin
  : 'https://oak-cornea-marlin.ngrok-free.dev';
// localStorage también está bloqueado en algunos visores embebidos. Si falla,
// la configuración vive en memoria: sirve para esta sesión y no rompe nada.
const _mem = {};
const g = k => { try { return localStorage.getItem(k) || _mem[k] || ''; }
                 catch(e){ return _mem[k] || ''; } };
const s = (k,v) => { _mem[k]=v; try { localStorage.setItem(k,v); } catch(e){} };

function marcarCfg(){
  const b = document.getElementById('cfg');
  if(!b) return;
  if(g('mx_tok')){ b.classList.add('ok'); b.textContent = '⚙ conectado'; }
  else { b.classList.remove('ok'); b.textContent = '⚙ conexión'; }
}

// Panel dentro de la página, no prompt(): los visores embebidos y algunos
// navegadores bloquean prompt() en file:// y el clic no hacía nada.
function configurar(){
  const p = document.getElementById('cfgpanel');
  p.style.display = (p.style.display === 'block') ? 'none' : 'block';
  if(p.style.display === 'block'){
    document.getElementById('cfgurl').value = g('mx_url') || DEFECTO;
    document.getElementById('cfgtok').value = g('mx_tok');
    document.getElementById('cfgtok').focus();
    document.getElementById('cfgmsg').textContent = '';
  }
}

function guardarCfg(){
  const url = document.getElementById('cfgurl').value.trim().replace(/\/$/,'');
  const tok = document.getElementById('cfgtok').value.trim();
  const msg = document.getElementById('cfgmsg');

  // Un token es una sola palabra corta. Si llega un comando pegado entero,
  // hay que decirlo acá y no mandarlo al servidor.
  if(!tok){ msg.textContent = 'Falta el token.'; return; }
  if(/\s/.test(tok) || tok.length > 120){
    msg.textContent = 'Eso no parece un token: son ~28 caracteres seguidos, sin espacios. ' +
                      'Lo que pegaste tiene ' + tok.length + '. Copia solo la línea verde del servidor.';
    return;
  }
  s('mx_url', url); s('mx_tok', tok);
  msg.textContent = '';
  document.getElementById('cfgpanel').style.display = 'none';
  marcarCfg();
  estado('conectado', 2500);
}

function estado(t, ms){
  const e = document.getElementById('estado');
  e.textContent = t;
  if(ms) setTimeout(()=>{ if(e.textContent===t) e.textContent=''; }, ms);
}

async function preguntar(texto){
  const url = g('mx_url') || DEFECTO;
  if(!g('mx_tok')){ configurar(); if(!g('mx_tok')) return; }

  const caja = document.getElementById('rta');
  caja.style.display='block';
  caja.textContent='…';
  estado('pensando');

  try{
    const r = await fetch(url + '/maximus/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json',
               'x-maximus-token': g('mx_tok'),
               'ngrok-skip-browser-warning':'1'},
      body: JSON.stringify({mensaje: texto, sesion:'cerebro', voz: g('mx_voz')==='1'})
    });
    if(r.status === 401){ caja.textContent='Token inválido. Toca ⚙ conexión abajo.'; estado(''); return; }
    if(r.status === 503){ caja.textContent='El chat no está habilitado en el servidor: falta MAXIMUS_CHAT_TOKEN en el .env.'; estado(''); return; }
    if(!r.ok){ caja.textContent='El agente respondió ' + r.status; estado(''); return; }

    const d = await r.json();
    caja.textContent = d.respuesta;
    estado('');

    if(d.audio) sonar(d.audio, 0.9);   // cierra el mic mientras habla: ver sonar()

    // lo mejor del grafo: iluminar exactamente lo que Maximus usó para responder
    const usadas = (d.notas || []).filter(n => idx[n] !== undefined);
    if(usadas.length){
      resaltados = new Set(usadas);
      sel = usadas[0];
      caja.textContent += '\n\n— usó ' + usadas.length + ' notas: ' + usadas.join(', ');
      ajustarA(usadas);
    }
  }catch(e){
    caja.textContent = 'No pude hablar con el agente.\n\n' + e.message +
      '\n\nRevisa que el servidor esté arriba y que la URL sea la correcta (⚙ conexión).';
    estado('');
  }
}

function ajustarA(ids){
  const vis = ids.map(i=>N[idx[i]]).filter(Boolean);
  if(!vis.length) return;
  const xs=vis.map(n=>n.x), ys=vis.map(n=>n.y);
  const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
  const izq = W<900?0:345, der = W<760?0:(W<900?150:235), mg=90;
  const dw=Math.max(W-izq-der-mg*2,220), dh=Math.max(H-mg*2-180,200);
  cam.z=Math.max(0.15, Math.min(dw/Math.max(x1-x0,1), dh/Math.max(y1-y0,1), 1.5));
  cam.x=izq+mg+(dw-(x1-x0)*cam.z)/2-x0*cam.z;
  cam.y=mg+(dh-(y1-y0)*cam.z)/2-y0*cam.z;
}

document.getElementById('chat').addEventListener('keydown', e=>{
  if(e.key==='Enter' && e.target.value.trim()){
    const t=e.target.value.trim(); e.target.value=''; preguntar(t);
  }
  if(e.key==='Escape'){ document.getElementById('rta').style.display='none'; }
});
// ── que Maximus mire la pantalla ──────────────────────────────────
// Con esto lee DiMangoToGo o DiMangoWorking sin integrar nada: le muestras
// /AdminVentas y saca los números. La imagen no se guarda en ninguna parte.
async function mirarPantalla(){
  if(!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia){
    mostrarRta('Este navegador no puede compartir pantalla. Ábrelo en Chrome.');
    return;
  }
  if(!g('mx_tok')){ configurar(); return; }

  const btn = document.getElementById('btnojo');
  let stream;
  try{
    stream = await navigator.mediaDevices.getDisplayMedia({video:{frameRate:1}, audio:false});
  }catch(e){
    mostrarRta('No compartiste ninguna pantalla.'); return;
  }

  btn.classList.add('on'); estado('mirando');
  try{
    const track = stream.getVideoTracks()[0];
    // Un instante para que la imagen llegue completa antes de capturarla
    await new Promise(r=>setTimeout(r, 400));

    const video = document.createElement('video');
    video.srcObject = stream; video.muted = true;
    await video.play();
    await new Promise(r=>setTimeout(r, 250));

    const c = document.createElement('canvas');
    c.width = video.videoWidth; c.height = video.videoHeight;
    c.getContext('2d').drawImage(video, 0, 0);
    track.stop(); stream.getTracks().forEach(t=>t.stop());

    // JPEG al 82%: una captura en PNG puede pesar varios MB y no aporta nitidez
    const dataUrl = c.toDataURL('image/jpeg', 0.82);

    const pregunta = document.getElementById('chat').value.trim();
    document.getElementById('chat').value = '';
    mostrarRta('mirando…');
    estado('analizando');

    const r = await fetch((g('mx_url')||DEFECTO) + '/maximus/ver', {
      method:'POST',
      headers:{'Content-Type':'application/json','x-maximus-token':g('mx_tok'),
               'ngrok-skip-browser-warning':'1'},
      body: JSON.stringify({imagen:dataUrl, mime:'image/jpeg', pregunta})
    });
    if(!r.ok){ mostrarRta('El agente respondió ' + r.status); estado(''); btn.classList.remove('on'); return; }
    const d = await r.json();
    mostrarRta(d.respuesta);
    estado('');
    if(g('mx_voz')==='1') hablarRespuesta(d.respuesta);
  }catch(e){
    mostrarRta('No pude capturar la pantalla: ' + e.message);
    estado('');
  }
  btn.classList.remove('on');
}

// Pide solo el audio de un texto ya generado (para lo que ve, no para el chat)
async function hablarRespuesta(texto){
  try{
    const r = await fetch((g('mx_url')||DEFECTO) + '/maximus/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json','x-maximus-token':g('mx_tok'),
               'ngrok-skip-browser-warning':'1'},
      body: JSON.stringify({mensaje:'Repite exactamente esto, sin agregar nada: ' + texto,
                            sesion:'voz-solo', voz:true})
    });
    const d = await r.json();
    if(d.audio) sonar(d.audio, 1.0);   // cierra el mic mientras habla: ver sonar()
  }catch(e){}
}
window.mirarPantalla = mirarPantalla;

// ── hablarle a Maximus ────────────────────────────────────────────
// Reconocimiento del propio navegador: gratis, sin servidor, sin API key.
// Solo Chrome y Edge lo implementan; Safari no.
let rec = null, escuchando = false, audioActual = null;

// El micrófono tiene DOS estados y confundirlos era el bug:
//   micAbierto  → el pestillo. Lo pones tú y solo tú lo sacas.
//   escuchando  → si el motor del navegador está activo en este instante.
// Chrome corta el reconocimiento cada vez que te callas. Eso baja 'escuchando',
// no el pestillo — y mientras el pestillo esté puesto, se vuelve a levantar solo.
let micAbierto = false, fallosSeguidos = 0;

// ¿Está sonando la respuesta? Mientras habla no se escucha: por los parlantes se
// oiría a sí mismo, se transcribiría y se contestaría solo, en bucle.
function hablando(){
  return !!(audioActual && !audioActual.paused && !audioActual.ended);
}

function sonar(b64, volumen){
  try{
    if(audioActual){ audioActual.pause(); }
    if(escuchando){ try{ rec && rec.abort(); }catch(e){} }   // cierra el mic antes de hablar
    audioActual = new Audio('data:audio/mpeg;base64,' + b64);
    audioActual.volume = volumen;
    engancharAudio(audioActual);      // para que la cara se mueva con la voz
    audioActual.play().catch(()=>{});
  }catch(e){ /* si el navegador bloquea el autoplay, el texto ya está */ }
}

// ── la cara ───────────────────────────────────────────────────────
// El avatar se mueve con la ONDA REAL de la voz, no con un temporizador:
// si la respuesta dura 3 s el hocico se mueve 3 s, y calla cuando calla.
//
// Un perro de una foto no tiene boca animable. El truco es estirar hacia
// abajo la franja inferior de la imagen —hocico, mandíbula y lengua— en
// proporción al volumen. Como el recorte está en un círculo, lo que sobra
// se corta solo y el ojo lo lee como la boca abriéndose.
const CORTE = 0.70;   // dónde empieza la mandíbula, medido en la foto

const cara = document.getElementById('cara');
const cl = document.getElementById('caralienzo');
const cx = cl ? cl.getContext('2d') : null;
const fotoCara = new Image();
let caraLista = false;
fotoCara.onload = ()=>{ caraLista = true; };
fotoCara.onerror = ()=>{ if(cara) cara.style.display='none'; };
fotoCara.src = 'data:image/jpeg;base64,__CARA__';
// sin foto el src queda en el prefijo pelado: se esconde y no estorba
if(cara && fotoCara.src.length < 40) cara.style.display = 'none';
if(cara) cara.onclick = ()=>alternarMic();

// Audio → número. Se intenta el analizador real; si el navegador lo niega
// se cae a una onda sintética. Nunca se toca la reproducción: si algo falla
// aquí, el sonido sigue saliendo igual y solo se pierde la sincronía fina.
let ac=null, analiz=null, muestras=null, modoSint=false, mudos=0, vioSenal=false;

function engancharAudio(el){
  if(modoSint) return;
  try{
    if(!ac) ac = new (window.AudioContext||window.webkitAudioContext)();
    const src = ac.createMediaElementSource(el);
    analiz = ac.createAnalyser(); analiz.fftSize = 256;
    muestras = new Uint8Array(analiz.fftSize);
    src.connect(analiz); analiz.connect(ac.destination);
    mudos = 0;

    // Enrutar por un contexto dormido deja la respuesta MUDA, y quedarse
    // callado es mucho peor que no animar. resume() es asíncrono, así que
    // no sirve mirar el estado en la línea siguiente: hay que volver a mirar.
    if(ac.state !== 'running'){
      ac.resume().catch(()=>{});
      setTimeout(()=>{
        if(ac.state === 'running' || el !== audioActual) return;
        modoSint = true; analiz = null;          // se rinde el analizador
        const t = el.currentTime, fuente = el.src, vol = el.volume;
        el.pause();
        const bis = new Audio(fuente);            // este NO pasa por el contexto
        bis.volume = vol;
        try{ bis.currentTime = t; }catch(e){}
        audioActual = bis; bis.play().catch(()=>{});
      }, 350);
    }
  }catch(e){ modoSint = true; analiz = null; }
}

function nivelVoz(){
  if(!hablando()) return 0;
  if(analiz && !modoSint){
    analiz.getByteTimeDomainData(muestras);
    let pico = 0;
    for(let i=0;i<muestras.length;i++){ const v = Math.abs(muestras[i]-128); if(v>pico) pico = v; }
    if(pico > 1){ vioSenal = true; mudos = 0; return Math.min(1, pico/64); }
    // Silencio. Si el analizador YA entregó señal alguna vez, esto es una
    // pausa del habla y la boca se cierra — que es justo lo que debe pasar.
    // Solo si nunca entregó nada se concluye que no sirve y se cambia de modo.
    if(vioSenal || ++mudos <= 45) return 0;
    modoSint = true;
  }
  const t = performance.now()/1000;
  return 0.30 + 0.34*Math.abs(Math.sin(t*7.7)) * (0.55 + 0.45*Math.abs(Math.sin(t*2.9)));
}

let ampSuave = 0;

function pintarCara(){
  if(!cx || !caraLista) return;
  const S = 136, DPR = Math.min(devicePixelRatio||1, 2);
  if(cl.width !== S*DPR){ cl.width = cl.height = S*DPR; }
  cx.setTransform(DPR,0,0,DPR,0,0);
  cx.clearRect(0,0,S,S);

  const objetivo = nivelVoz();
  // Sube rápido y baja lento: una boca no se cierra de golpe entre sílabas.
  ampSuave += (objetivo - ampSuave) * (objetivo > ampSuave ? 0.55 : 0.16);
  const a = ampSuave, t = performance.now()/1000;

  const R = S/2 - 5;
  const respira = 1 + Math.sin(t*1.6)*0.012 + a*0.045;   // late al hablar
  const cxc = S/2, cyc = S/2 - a*2.5;                     // y cabecea un poco

  // halo: ámbar al hablar, rojo si el micrófono está abierto
  const rojo = micAbierto && !hablando();
  const col = rojo ? '255,95,86' : '245,166,35';
  const fuerza = rojo ? 0.35 + 0.25*Math.abs(Math.sin(t*3.4)) : a;
  if(fuerza > 0.02){
    const g = cx.createRadialGradient(cxc,cyc,R*0.85, cxc,cyc,R+16*fuerza+6);
    g.addColorStop(0, 'rgba('+col+',' + (0.30*fuerza).toFixed(3) + ')');
    g.addColorStop(1, 'rgba('+col+',0)');
    cx.fillStyle = g;
    cx.beginPath(); cx.arc(cxc,cyc,R+22,0,7); cx.fill();
  }

  cx.save();
  cx.beginPath(); cx.arc(cxc,cyc,R,0,7); cx.clip();

  const w = fotoCara.naturalWidth, h = fotoCara.naturalHeight;
  const D = R*2*respira, x0 = cxc-D/2, y0 = cyc-D/2;
  const quijada = a*D*0.11;

  // arriba: ojos y frente, quietos
  cx.drawImage(fotoCara, 0, 0, w, h*CORTE,
                         x0, y0, D, D*CORTE);
  // abajo: hocico y lengua, estirados hacia abajo con la voz
  cx.drawImage(fotoCara, 0, h*CORTE, w, h*(1-CORTE),
                         x0, y0+D*CORTE, D, D*(1-CORTE)+quijada);
  cx.restore();

  cx.strokeStyle = 'rgba('+col+',' + (0.34 + 0.5*fuerza).toFixed(3) + ')';
  cx.lineWidth = 1.6 + fuerza*2.6;
  cx.beginPath(); cx.arc(cxc,cyc,R,0,7); cx.stroke();
}

function alternarMic(){
  if(micAbierto){ pararMic(); return; }        // apagar es explícito: lo pediste tú

  // Si estaba hablando, se calla: le estás interrumpiendo.
  if(audioActual){ try{ audioActual.pause(); }catch(e){} audioActual = null; }

  // Quien habla espera que le contesten hablando: la voz se enciende sola.
  if(g('mx_voz') !== '1'){ s('mx_voz','1'); marcarVoz(); }

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){
    mostrarRta('Este navegador no reconoce voz.\n\nÁbrelo en Chrome: Safari no implementa el reconocimiento de voz.');
    return;
  }

  micAbierto = true; fallosSeguidos = 0;
  marcarMic(); estado('escuchando');
  arrancarMic();
}

function arrancarMic(){
  if(!micAbierto || escuchando || hablando()) return;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR) return;

  rec = new SR();
  rec.lang = 'es-CL';
  rec.continuous = false;      // el turno lo corta el navegador; el pestillo lo reabre
  rec.interimResults = true;

  const caja = document.getElementById('chat');
  let final = '';              // local a cada turno: no arrastra lo ya enviado

  rec.onstart = () => { escuchando = true; fallosSeguidos = 0; marcarMic(); estado('escuchando'); };

  rec.onresult = e => {
    let interino = '';
    for(let i = e.resultIndex; i < e.results.length; i++){
      const t = e.results[i][0].transcript;
      if(e.results[i].isFinal) final += t; else interino += t;
    }
    caja.value = (final + interino).trim();     // se ve lo que va entendiendo
  };

  rec.onerror = ev => {
    escuchando = false;
    // Con el pestillo puesto estos dos son normales, no fallas: te quedaste
    // callado, o el turno se cortó para reabrirse. No deben apagar el micrófono.
    if(ev.error === 'no-speech' || ev.error === 'aborted') return;

    // Sin permiso o sin micrófono no sirve reintentar: se suelta el pestillo.
    micAbierto = false; marcarMic(); estado('');
    mostrarRta({
      'not-allowed':'Falta permiso del micrófono. Dáselo en el candado de la barra de direcciones.',
      'service-not-allowed':'El navegador bloqueó el micrófono. Prueba abriendo el archivo en Chrome.',
      'audio-capture':'No encuentro micrófono.'
    }[ev.error] || ('Error de reconocimiento: ' + ev.error));
  };

  rec.onend = () => {
    escuchando = false;
    const t = caja.value.trim();
    if(t){ caja.value=''; preguntar(t); }        // al callarte, se envía solo
    if(micAbierto){ estado('escuchando'); setTimeout(arrancarMic, 300); }
    else { marcarMic(); estado(''); }
  };

  try { rec.start(); }
  catch(e){
    escuchando = false;
    if(++fallosSeguidos >= 3){
      micAbierto = false; marcarMic(); estado('');
      mostrarRta('No pude abrir el micrófono: ' + e.message);
    }else{
      setTimeout(arrancarMic, 500);
    }
  }
}

// Red de seguridad. Si el pestillo está puesto y el reconocimiento quedó abajo
// por cualquier camino —un error de red, una salida temprana, el navegador en
// segundo plano— esto lo levanta. Vale más un vigilante de tres líneas que
// perseguir cada punto de salida a mano.
setInterval(() => {
  if(micAbierto && !escuchando && !hablando()) arrancarMic();
}, 1500);

function pararMic(){
  micAbierto = false;                      // primero suelta el pestillo…
  try{ rec && rec.stop(); }catch(e){}      // …o el onend lo volvería a abrir
  marcarMic(); estado('');
}
function marcarMic(){
  const b = document.getElementById('btnmic');
  if(b) b.classList.toggle('on', micAbierto);   // el botón muestra TU decisión
}
function mostrarRta(t){
  const c = document.getElementById('rta');
  c.style.display='block'; c.textContent = t;
}
window.alternarMic = alternarMic;

function alternarVoz(){
  const on = g('mx_voz') === '1';
  s('mx_voz', on ? '0' : '1');
  marcarVoz();
  estado(on ? 'voz apagada' : 'voz encendida', 2000);
}
function marcarVoz(){
  const b = document.getElementById('btnvoz');
  if(b) b.classList.toggle('on', g('mx_voz') === '1');
}
window.alternarVoz = alternarVoz;

window.configurar=configurar; window.guardarCfg=guardarCfg; marcarCfg(); marcarVoz(); marcarMic();

// ── HUD: relojes, clima e indicadores ─────────────────────────────
const CIUDADES = [
  {tz:'America/Santiago', lat:-18.4783, lon:-70.3126},
  {tz:'America/New_York', lat: 38.9072, lon:-77.0369},
  {tz:'Europe/Madrid',    lat: 40.4168, lon: -3.7038},
  {tz:'Europe/Rome',      lat: 45.4642, lon:  9.1900},
];

// códigos WMO de open-meteo → un símbolo que se entienda de un vistazo
const CIELO = c =>
  c===0?'☀' : c<=2?'⛅' : c===3?'☁' : c<=48?'🌫' :
  c<=57?'🌦' : c<=67?'🌧' : c<=77?'❄' : c<=82?'🌧' : c<=86?'❄' : '⛈';

function tictac(){
  document.querySelectorAll('.reloj').forEach(el=>{
    const tz = el.dataset.tz;
    const p = new Intl.DateTimeFormat('es-CL',{timeZone:tz,hour:'2-digit',minute:'2-digit',
      second:'2-digit',hour12:false}).formatToParts(new Date());
    const v = Object.fromEntries(p.filter(x=>x.type!=='literal').map(x=>[x.type,x.value]));
    el.querySelector('.hr').innerHTML = `${v.hour}:${v.minute}<span class="seg">:${v.second}</span>`;
    const h = parseInt(v.hour,10);
    el.classList.toggle('noche', h < 7 || h >= 21);   // ciudades dormidas, más apagadas
  });
}
tictac(); setInterval(tictac, 1000);

async function traerClima(){
  const lats = CIUDADES.map(c=>c.lat).join(','), lons = CIUDADES.map(c=>c.lon).join(',');
  try{
    const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lats}&longitude=${lons}`+
      `&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=1`);
    const d = await r.json();
    const arr = Array.isArray(d) ? d : [d];
    document.querySelectorAll('.reloj').forEach((el,i)=>{
      const c = arr[i]; if(!c) return;
      const t = Math.round(c.current.temperature_2m);
      const mn = Math.round(c.daily.temperature_2m_min[0]), mx = Math.round(c.daily.temperature_2m_max[0]);
      el.querySelector('.tmp').textContent = `${CIELO(c.current.weather_code)} ${t}°  ${mn}/${mx}`;
    });
  }catch(e){
    document.querySelectorAll('.reloj .tmp').forEach(t=>t.textContent='clima n/d');
  }
}

async function traerIndicadores(){
  const f1 = document.querySelector('#ind .fila1');
  const f2 = document.querySelector('#ind .fila2');

  // lo que sale del propio cerebro no depende de internet: se pinta primero
  const abiertos = N.filter(n=>['abierto','propuesto','conflicto'].includes(n.estado)).length;
  const conf = N.filter(n=>n.estado==='conflicto');
  f2.innerHTML =
    `<span><span class="k">notas</span> <b>${N.length}</b></span>`+
    `<span><span class="k">conexiones</span> <b>${A.length}</b></span>`+
    `<span><span class="k">abiertos</span> <b>${abiertos}</b></span>`+
    (conf.length
      ? `<span class="alerta">▲ ${conf.length} en conflicto: ${conf.map(c=>c.id).join(' ')}</span>`
      : `<span class="ok">sin conflictos</span>`);

  try{
    const d = await (await fetch('https://mindicador.cl/api')).json();
    const n = v => v.toLocaleString('es-CL',{maximumFractionDigits:2});
    f1.innerHTML =
      `<span><span class="k">dólar</span> <b>$${n(d.dolar.valor)}</b></span>`+
      `<span><span class="k">euro</span> <b>$${n(d.euro.valor)}</b></span>`+
      `<span><span class="k">UF</span> <b>$${n(d.uf.valor)}</b></span>`+
      `<span><span class="k">UTM</span> <b>$${n(d.utm.valor)}</b></span>`+
      `<span class="k">al ${d.dolar.fecha.slice(0,10)}</span>`;
  }catch(e){
    f1.innerHTML = '<span class="k">indicadores no disponibles (sin conexión)</span>';
  }
}

traerClima(); traerIndicadores();
setInterval(traerClima, 15*60*1000);        // el clima no cambia cada minuto
setInterval(traerIndicadores, 60*60*1000);

bucle();   // todo declarado: recién ahora se puede pintar
</script></body></html>"""


if __name__ == "__main__":
    main()
