#!/usr/bin/env python3
"""
Lee las notas atómicas de memoria/ y genera:
  - memoria/indice.json  → nodos y aristas, para búsqueda y recuperación
  - brain/cerebro.html   → visualizador autocontenido (se abre sin servidor)

No depende de nada externo: ni librerías, ni CDN, ni internet.
Los datos van embebidos en el HTML, así que el archivo no sale de tu disco.
"""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MEM = BASE / "memoria"

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

    indice = {"nodos": nodos, "aristas": aristas,
              "generado": "2026-08-20",
              "huerfanos": huerfanos, "enlaces_rotos": rotos}
    (MEM / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")

    html = PLANTILLA.replace("__DATOS__", json.dumps(indice, ensure_ascii=False))
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
#rta{position:fixed;bottom:104px;left:50%;transform:translateX(-50%);z-index:15;
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
  <button id="btnvoz" onclick="alternarVoz()" title="Que Maximus conteste hablando">🔊</button>
  <span id="estado"></span>
</div>
<div id="rta"></div>

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
  const dispW=Math.max(W-izq-der-mg*2, 220), dispH=Math.max(H-hud-mg*2-110, 220);
  cam.z=Math.max(0.12, Math.min(dispW/Math.max(x1-x0,1), dispH/Math.max(y1-y0,1), 1.7));
  cam.x=izq+mg+(dispW-(x1-x0)*cam.z)/2-x0*cam.z;
  cam.y=hud+mg+(dispH-(y1-y0)*cam.z)/2-y0*cam.z;
}

for(let i=0;i<400;i++) paso();   // estabilizar antes de mostrar
ajustar();

function bucle(){ paso(); pintar(); requestAnimationFrame(bucle) } bucle();

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
const DEFECTO = 'https://oak-cornea-marlin.ngrok-free.dev';
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

    if(d.audio){
      try{
        const a = new Audio('data:audio/mpeg;base64,' + d.audio);
        a.volume = 0.9; a.play();
      }catch(e){ /* si el navegador bloquea el autoplay, el texto ya está */ }
    }

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

window.configurar=configurar; window.guardarCfg=guardarCfg; marcarCfg(); marcarVoz();

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

</script></body></html>"""


if __name__ == "__main__":
    main()
