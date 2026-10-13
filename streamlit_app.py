"""Digital Twin Spektrofotometer UV-Vis (Agilent Cary 100) - Analisis Thiamin
SATU FILE SAJA: seluruh model 3D (Three.js) sudah tertanam di dalam file ini.
Jalankan: streamlit run app.py
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Digital Twin Cary 100 UV-Vis", page_icon="🔬", layout="wide")

st.title("🔬 Digital Twin Spektrofotometer UV-Vis (Agilent Cary 100)")
st.caption(
    "Simulasi edukasi analisis thiamin (vitamin B1): urutan menyalakan alat, jalur berkas cahaya, "
    "kurva kalibrasi, dan penentuan konsentrasi. Data spektrum bersifat ilustratif, bukan data kalibrasi alat."
)

with st.sidebar:
    st.header("Cara memakai")
    st.markdown(
        """
1. Nyalakan berurutan: **UPS** → **instrumen** → **komputer** → **monitor** (klik tombolnya di model 3D).
2. Tunggu *warm-up* selesai (lihat checklist). Mode transparan aktif otomatis, berkas cahaya terlihat.
3. Klik layar monitor / **Buka Cary WinUV**.
4. Buka tutup, pasang kuvet (kuarsa), tutup, lalu **Baseline** (blanko HCl 0,1 M).
5. Tab **Scan** (200–400 nm) untuk mencari λmax thiamin (≈ 246 nm).
6. Tab **Concentration**: **Ukur semua standar** → **Hitung kurva** → **Ukur sampel**.
        """
    )
    height = st.slider("Tinggi tampilan (px)", 500, 1200, 860, 20)

HTML = r"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digital Twin Cary 100</title>
<style>
*{box-sizing:border-box}body{margin:0;font:13px system-ui,sans-serif;background:#1b2330;color:#e8edf3;overflow:hidden}
#c{position:fixed;inset:0;width:100%;height:100%;display:block}
.bar{position:fixed;top:6px;left:6px;right:6px;display:flex;flex-wrap:wrap;gap:5px;z-index:5}
button,select,input{font:inherit}
button{background:#2b3a50;color:#e8edf3;border:1px solid #4a5d7a;border-radius:6px;padding:5px 9px;cursor:pointer}
button:hover{background:#3a4f6d}button.on{background:#2d7dd2;border-color:#7fb8f5}button:disabled{opacity:.45;cursor:not-allowed}
.panel{position:fixed;background:rgba(20,28,40,.9);border:1px solid #3a4d68;border-radius:8px;padding:10px;z-index:4}
#left{left:6px;top:80px;width:225px;max-height:calc(100% - 200px);overflow:auto}
#info{right:6px;top:80px;width:240px;max-height:26%;overflow:auto}
#hud{left:6px;bottom:6px;font-family:monospace;line-height:1.5;white-space:pre}
#left h4,#info h4{margin:0 0 6px}#left ul{list-style:none;margin:0 0 10px;padding:0}#left li{padding:1px 0;color:#9fb0c6}#left li.ok{color:#7be08f}
#left li:before{content:"○ "}#left li.ok:before{content:"● "}
#left label{display:block;margin:6px 0 2px;color:#9fb0c6}#left select,#left input[type=range]{width:100%}
#toast{position:fixed;top:48px;left:50%;transform:translateX(-50%);background:#b3321f;color:#fff;padding:7px 14px;border-radius:6px;z-index:9;opacity:0;transition:opacity .3s;pointer-events:none;max-width:90%}
#app{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:min(640px,96vw);max-height:92vh;overflow:auto;background:#ece9d8;color:#111;border:2px solid #0a246a;border-radius:6px;z-index:8;box-shadow:0 10px 40px #000a}
#app[hidden]{display:none}.wt{background:linear-gradient(#2a62d0,#0a3fa8);color:#fff;padding:5px 8px;display:flex;justify-content:space-between;align-items:center}
.wt button{padding:0 7px;background:#c33;border-color:#fff}
#app .bd{padding:8px}#app button{background:#f3f3ee;color:#111;border:1px solid #777}#app button:hover{background:#fff}#app button.on{background:#cfe0ff}
#app input{width:70px}#app table{width:100%;border-collapse:collapse;font-size:12px}#app td,#app th{border:1px solid #aaa;padding:2px 5px;text-align:right}
#status{margin:6px 0;font-weight:600}canvas#chart{width:100%;background:#fff;border:1px solid #888}
#sch{right:6px;bottom:6px;width:310px}.lb{position:fixed;pointer-events:none;font-size:10px;background:#000a;color:#fff;padding:1px 4px;border-radius:3px;z-index:3;white-space:nowrap}
</style></head><body>
<canvas id="c"></canvas>
<div class="bar">
 <button data-v="front">Depan</button><button data-v="top">Atas</button><button data-v="back">Belakang</button><button data-v="side">Samping</button>
 <button data-v="inst">Instrumen</button><button data-v="cuv">Kuvet</button><button data-v="mon">Monitor</button>
 <button id="bX">Transparan</button><button id="bB" class="on">Berkas cahaya</button><button id="bL" class="on">Label</button><button id="bR">Auto-rotate</button>
 <button id="bA">Buka Cary WinUV</button><button id="bFS">Layar penuh</button><button id="bRe">Reset simulasi</button>
</div>
<div class="panel" id="left">
 <h4>Urutan menyalakan</h4>
 <ul id="chk"></ul>
 <h4>Sampel &amp; kuvet</h4>
 <label>Larutan</label><select id="smp"><option value="blank">Blanko (HCl 0,1 M)</option><option value="std">Standar thiamin</option><option value="unk">Sampel thiamin (tak diketahui)</option></select>
 <label>Konsentrasi: <b id="cv">6</b> ppm</label><input type="range" id="conc" min="0.5" max="15" step="0.5" value="6">
 <div style="margin-top:8px;display:flex;gap:5px;flex-wrap:wrap"><button id="bLid">Buka tutup</button><button id="bCuv">Pasang kuvet</button></div>
 <p style="color:#8ea0b8;font-size:11px">Klik langsung pada tombol UPS, saklar rocker instrumen, tombol power PC, monitor, tutup kompartemen, atau kuvet. Spektrum thiamin = data ilustratif (λmax ≈ 246 nm dalam HCl 0,1 M; verifikasi dengan SOP/manual). Daerah UV wajib kuvet kuarsa.</p>
</div>
<div class="panel" id="info"><h4 id="it">Klik bagian mana saja</h4><div id="ix">Klik objek 3D untuk melihat nama dan fungsinya.</div></div>
<div class="panel" id="hud"></div>
<div class="panel" id="sch"><b>Jalur cahaya (tampak atas)</b><canvas id="schc" width="290" height="190" style="width:100%;display:block;margin:4px 0"></canvas><div style="font-size:11px;color:#9fb0c6;line-height:1.35">1 Lampu → 2 Cermin M1 → 3 Celah masuk → 4 Kisi (memilih λ) → 5 Cermin M2 → 6 Chopper (membagi berkas) → 7 Kuvet sampel &amp; referensi → 8 Detektor PMT. Di tiap cermin sudut datang = sudut pantul. Berkas sampel meredup setelah kuvet.</div></div>
<div id="toast"></div>
<div id="app" hidden>
 <div class="wt"><span>Cary WinUV</span><button id="xapp">✕</button></div>
 <div class="bd">
  <div><button data-t="scan" class="on">Scan</button> <button data-t="simple">Simple Reads</button> <button data-t="conc">Concentration</button></div>
  <div id="status"></div>
  <div id="p-scan" style="margin:6px 0">Start <input id="s0" type="number" value="200"> nm &nbsp; Stop <input id="s1" type="number" value="400"> nm <small>(190–900)</small></div>
  <div id="p-simple" style="margin:6px 0" hidden>λ <input id="sl" type="number" value="246"> nm &nbsp; Replikat <input id="sn" type="number" value="3" min="1" max="10"></div>
  <div id="p-conc" hidden style="margin:6px 0">λ analisis <input id="cl" type="number" value="246"> nm <small>(thiamin ≈ 246 nm dalam HCl 0,1 M; cek dengan Scan)</small><div id="stdtab"></div><div style="margin-top:4px">Faktor pengenceran sampel <input id="df" type="number" value="1" min="1" step="0.5"></div><div style="margin-top:4px;display:flex;gap:5px;flex-wrap:wrap"><button id="cAll">Ukur semua standar</button><button id="cFit">Hitung kurva</button><button id="cUnk">Ukur sampel</button><button id="cClr">Hapus data</button></div></div><canvas id="chart" width="580" height="260"></canvas><div id="cres" style="margin-top:4px;font-size:12px"></div>
  <div id="tbl"></div>
  <div style="margin-top:6px;display:flex;gap:5px;flex-wrap:wrap"><button id="aBase">Baseline (Zero)</button><button id="aStart">Start</button><button id="aStop">Stop</button><button id="aCsv">Ekspor CSV</button></div>
 </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const $=id=>document.getElementById(id);
if(typeof THREE==='undefined'){document.body.innerHTML='<p style="padding:20px">Three.js gagal dimuat (cek koneksi internet / WebGL).</p>'}
else{
const BY=0.8, WARM=12;
const S={ups:0,inst:0,pc:0,mon:0,booted:0,bootT:0,warm:0,base:0,lid:0,cuv:0,app:0,xray:0,beam:1,job:null,lam:500,sample:'blank',conc:6,tab:'scan',res:null,lbl:1,autoX:0};
S.cal={l:246,std:[2,4,6,8,10,12].map(c=>({c,a:null,sd:null})),fit:null,unk:null};
// ---------- util
let toastT;function toast(t){const e=$('toast');e.textContent=t;e.style.opacity=1;clearTimeout(toastT);toastT=setTimeout(()=>e.style.opacity=0,2800)}
function W(l){let r=0,g=0,b=0;if(l<380)return[.55,.25,1];if(l<440){r=(440-l)/60;b=1}else if(l<490){g=(l-440)/50;b=1}else if(l<510){g=1;b=(510-l)/20}else if(l<580){r=(l-510)/70;g=1}else if(l<645){r=1;g=(645-l)/65}else if(l<=780)r=1;else return[.5,.1,.1];return[r,g,b]}
const G=(l,m,s)=>Math.exp(-.5*((l-m)/s)**2);
// Thiamin HCl dalam HCl 0,1 M (ILUSTRATIF): puncak ~246 nm, A1%1cm ~410 -> ~0,0395 Abs per ppm
const THI=(l,c)=>c*.0395*(G(l,246,12.5)+.10*G(l,272,16)+.9*G(l,205,11));
const UNK=7.35;
function specA(l){const s=S.sample;const c=s==='unk'?UNK:s==='std'?S.conc:0;return Math.min(3.5,THI(l,c))}
const noise=()=>(Math.random()-.5)*.004;
const readA=l=>Math.max(0,(S.cuv?specA(l):0)+noise());
// ---------- scene
const scene=new THREE.Scene();scene.background=new THREE.Color(0x1b2330);
const cam=new THREE.PerspectiveCamera(45,1,.1,100);cam.position.set(-1,5.5,12);
const ren=new THREE.WebGLRenderer({canvas:$('c'),antialias:true});ren.setPixelRatio(Math.min(Math.max(devicePixelRatio,1.5),2.5));ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;
ren.outputEncoding=THREE.sRGBEncoding;ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.05;
{const pm=new THREE.PMREMGenerator(ren),es=new THREE.Scene();es.background=new THREE.Color(0x7d8794);[[0,9,0,14,.5,14,1.8],[10,4,6,2,6,6,1.3],[-10,4,6,2,6,6,1.1],[0,3,-10,16,5,1,.8]].forEach(a=>{const m=new THREE.Mesh(new THREE.BoxGeometry(a[3],a[4],a[5]),new THREE.MeshBasicMaterial({color:new THREE.Color(a[6],a[6],a[6])}));m.position.set(a[0],a[1],a[2]);es.add(m)});scene.environment=pm.fromScene(es,.04).texture}
const ctl=new THREE.OrbitControls(cam,ren.domElement);ctl.target.set(1,.8,0);ctl.maxPolarAngle=Math.PI/2.05;ctl.minDistance=1.5;ctl.maxDistance=24;ctl.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xffffff,0x667788,.8));
const dl=new THREE.DirectionalLight(0xffffff,.9);dl.position.set(5,12,8);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);Object.assign(dl.shadow.camera,{left:-12,right:12,top:12,bottom:-12});scene.add(dl);
const std=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6,metalness:.05},o));
function bx(w,h,d,m,x,y,z,p){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),typeof m==='number'?std(m):m);o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;(p||scene).add(o);return o}
function cy(r,h,m,x,y,z,p,rx,rz){const o=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,24),typeof m==='number'?std(m):m);o.position.set(x,y,z);o.rotation.x=rx||0;o.rotation.z=rz||0;o.castShadow=true;(p||scene).add(o);return o}
function sp(r,m,x,y,z,p){const o=new THREE.Mesh(new THREE.SphereGeometry(r,12,12),m);o.position.set(x,y,z);(p||scene).add(o);return o}
const clickables=[];
function tag(m,k){m.traverse(o=>{if(o.isMesh){o.userData.key=k;clickables.push(o)}});return m}
function canvasTex(w,h,fn){const c=document.createElement('canvas');c.width=w;c.height=h;fn(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t}
function plane(pw,ph,tx,x,y,z,p,flat){const m=new THREE.Mesh(new THREE.PlaneGeometry(pw,ph),new THREE.MeshBasicMaterial({map:tx}));m.position.set(x,y,z);if(flat)m.rotation.x=-Math.PI/2;(p||scene).add(m);return m}
const txt=(lines,w,h,bg,fg,fs)=>canvasTex(w,h,(g)=>{g.fillStyle=bg;g.fillRect(0,0,w,h);g.fillStyle=fg;g.font='bold '+fs+'px sans-serif';g.textBaseline='middle';lines.forEach((t,i)=>g.fillText(t,10,h*(i+1)/(lines.length+1)))});
// lingkungan
const tile=canvasTex(256,256,(g)=>{g.fillStyle='#f2f2f0';g.fillRect(0,0,256,256);g.strokeStyle='#b9b9b4';g.lineWidth=5;g.strokeRect(0,0,256,256)});tile.wrapS=tile.wrapT=THREE.RepeatWrapping;tile.repeat.set(17,8);tile.anisotropy=8;
const tableM=bx(17,.3,8,new THREE.MeshStandardMaterial({map:tile,roughness:.4}),1.5,-.15,.3);
bx(30,8,.2,0xe8dcc0,0,3,-4.3);[-7,4].forEach(x=>bx(.8,8,.3,0xe8782a,x,3,-4.15));
const cab=bx(2.6,3,.5,0x8fa3b5,-3,1.5,-4);cab.material.transparent=true;cab.material.opacity=.6;
// ---------- Cary 100
const cary=new THREE.Group();cary.position.set(-3.2,0,0);scene.add(cary);
const shW=new THREE.MeshPhysicalMaterial({color:0xf1f1ec,roughness:.38,clearcoat:.5,clearcoatRoughness:.3,transparent:true});
const shD=new THREE.MeshPhysicalMaterial({color:0x34373b,roughness:.5,metalness:.1,clearcoat:.3,transparent:true});
const shells=[];
function rrs(w,d,r){const s=new THREE.Shape(),x=-w/2,y=-d/2;s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+d-r);s.quadraticCurveTo(x+w,y+d,x+w-r,y+d);s.lineTo(x+r,y+d);s.quadraticCurveTo(x,y+d,x,y+d-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);return s}
function slabG(w,d,h,r,hole){const s=rrs(w,d,r);if(hole){const a=hole,q=new THREE.Path();q.moveTo(a[0]-a[2]/2,-a[1]-a[3]/2);q.lineTo(a[0]+a[2]/2,-a[1]-a[3]/2);q.lineTo(a[0]+a[2]/2,-a[1]+a[3]/2);q.lineTo(a[0]-a[2]/2,-a[1]+a[3]/2);q.closePath();s.holes.push(q)}const b=Math.min(.03,h/3);const g=new THREE.ExtrudeGeometry(s,{depth:h-2*b,bevelEnabled:true,bevelThickness:b,bevelSize:b,bevelOffset:-b,bevelSegments:3,curveSegments:10});g.rotateX(-Math.PI/2);g.translate(0,b,0);return g}
function sg(g,m,x,y,z,p,keep){const o=new THREE.Mesh(g,m);o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;p.add(o);const e=new THREE.LineSegments(new THREE.EdgesGeometry(g,35),new THREE.LineBasicMaterial({color:0x3b8bff,transparent:true,opacity:0}));e.visible=false;o.add(e);shells.push({m:o,e,keep});return o}
function rm(g,c,x,y,z,p){const o=new THREE.Mesh(g,new THREE.MeshPhysicalMaterial({color:c,roughness:.35,clearcoat:.6}));o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;p.add(o);return o}
const HOLE=[0,.5,1.8,1.8];
tag(sg(slabG(5.6,4.4,.5,.15),shW,0,0,0,cary),'body');
tag(sg(slabG(5.6,4.4,.5,.15,HOLE),shW,0,.5,0,cary),'body');
tag(sg(slabG(2.6,2.5,.1,.08,[0,-.05,1.8,1.8]),shW,0,1,.55,cary),'body');
tag(sg(slabG(2.0,1.4,.35,.1),shW,-1.7,1,-1.4,cary),'body');
tag(sg(new THREE.BoxGeometry(1.6,.03,1.05),shD,-1.7,1.365,-1.4,cary),'lampcover');
for(let i=0;i<9;i++)bx(1.3,.012,.025,0x0b0b0b,-1.7,1.385,-1.83+i*.07,cary);
// tutup kompartemen sampel (engsel di belakang)
const lid=new THREE.Group();lid.position.set(0,1.1,-.7);cary.add(lid);
tag(sg(slabG(2.5,2.5,.08,.1),shD,0,0,1.25,lid,true),'lid');tag(bx(.8,.1,.1,0x0d0d0d,0,.1,2.4,lid),'lid');
// strip depan
bx(5.4,.22,.05,0x4a4d52,0,.12,2.21,cary);
const ledM=std(0x114411,{emissive:0x000000});sp(.05,ledM,-2.5,.12,2.25,cary);
const rocker=bx(.3,.18,.07,0x111111,-2.1,.12,2.26,cary);tag(rocker,'sw');
tag(bx(.6,.1,.05,0x222222,-.4,.12,2.25,cary),'port');
plane(2.6,.4,txt(['Agilent Technologies','Cary Series UV-Vis Spectrophotometer'],520,80,'#eeeeee','#222',22),-1.6,1.002,2.0,cary,1);
plane(1.1,.18,txt(['Cary 100 UV-Vis'],220,36,'#4a4d52','#ddd',22),1.9,.12,2.24,cary).position.z=2.241;
tag(plane(.8,.45,txt(['PT UNITAMA','Service label'],160,90,'#ccc','#222',20),-2.0,.25,2.21,cary),'label');
const qr=canvasTex(64,64,(g)=>{g.fillStyle='#fff';g.fillRect(0,0,64,64);g.fillStyle='#000';for(let i=0;i<16;i++)for(let j=0;j<16;j++)if(Math.random()>.5)g.fillRect(i*4,j*4,4,4)});
tag(plane(.5,.5,qr,-2.35,1.002,.3,cary,1),'qr');tag(plane(.5,.5,txt(['SCAN HERE'],180,180,'#9cc9c0','#124',26),-1.7,1.002,.3,cary,1),'qr');
plane(.35,.25,txt(['2'],70,50,'#fff','#000',40),-2.6,1.002,1.4,cary,1);
// interior
const tray=bx(1.8,.04,1.8,0x0b0b0b,0,.52,.5,cary);bx(5.2,.03,4,0x555a60,0,.505,0,cary);
const holdM=std(0x0e0e0e);[.95,.05].forEach((z,i)=>{const h=bx(.7,.1,.5,holdM,0,.57,z,cary);tag(h,i?'hold_r':'hold_s');[[-.3,-.2],[.3,.2]].forEach(p=>cy(.025,.12,0xc9a227,p[0],.64,z+p[1],cary))});
function cuvette(){const g=new THREE.Group();const gl=bx(.3,.36,.3,std(0xcfe8ff,{transparent:true,opacity:.28,roughness:.05}),0,0,0,g);gl.castShadow=false;const lq=bx(.26,.26,.26,std(0xcfe8ff,{transparent:true,opacity:.7}),0,-.04,0,g);g.userData.liq=lq;return g}
const cuvS=cuvette();cary.add(cuvS);tag(cuvS,'cuv');cuvS.position.set(1.6,.18,3);let cuvK=0;
const cuvR=cuvette();cuvR.position.set(0,.8,.05);cary.add(cuvR);tag(cuvR,'cuv_ref');
function setLiq(){const m=cuvS.userData.liq.material;m.color.setHex(S.sample==='blank'?0xd7ecff:0xc4e2ff);m.opacity=S.sample==='blank'?.45:.62}
// optik
const opt=new THREE.Group();cary.add(opt);
const silver=std(0xd8dde2,{metalness:.9,roughness:.1});
const common=[[-2.5,-1.7],[-1.9,-1.7],[-1.9,-1.2],[-1.9,-.6],[-1.1,-1.1],[-1.1,.5]];
const sampP=[[-1.1,.5],[-1.1,.95],[-.15,.95],[.15,.95],[1.5,.95],[2.3,.5]];
const refP=[[-1.1,.5],[-1.1,.05],[1.5,.05],[2.3,.5]];
const MIRS=[];function mirrors(p){for(let i=1;i<p.length-1;i++){if(i===3&&p===common)continue;const a=p[i-1],b=p[i],c=p[i+1];const d1=[b[0]-a[0],b[1]-a[1]],d2=[c[0]-b[0],c[1]-b[1]];const n1=Math.hypot(...d1),n2=Math.hypot(...d2);if(n1<.3||n2<.01||(i===2&&p===sampP)||(i===2&&p===refP&&false))continue;const nx=d2[0]/n2-d1[0]/n1,nz=d2[1]/n2-d1[1]/n1;if(Math.hypot(nx,nz)<.1)continue;const m=new THREE.Group();m.position.set(b[0],BY,b[1]);m.rotation.y=Math.atan2(nx,nz);MIRS.push([b[0],b[1],m.rotation.y]);bx(.32,.3,.04,silver,0,0,0,m);cy(.035,.12,0xc9a227,0,0,-.08,m,Math.PI/2);opt.add(tag(m,'mirror'))}}
mirrors(common);mirrors(sampP);mirrors(refP);
const lampV=cy(.14,.4,0xff9a3c,-2.5,BY,-1.7,opt,0,Math.PI/2);const lampVM=lampV.material;lampVM.emissive=new THREE.Color(0);tag(lampV,'lampV');
const lampD=cy(.12,.35,0x66d9ff,-2.5,BY,-1.3,opt,0,Math.PI/2);lampD.material.emissive=new THREE.Color(0);tag(lampD,'lampD');
[-1.2].forEach(z=>{const s=new THREE.Group();s.position.set(-1.9,BY,z);bx(.2,.2,.04,0x222222,-.16,0,0,s);bx(.2,.2,.04,0x222222,.16,0,0,s);opt.add(tag(s,'slit'))});
const grat=new THREE.Group();grat.position.set(-1.9,BY,-.6);bx(.34,.3,.05,0xb08d2a,0,0,0,grat);opt.add(tag(grat,'grat'));
const chop=new THREE.Group();chop.position.set(-1.1,BY,.5);[0,Math.PI].forEach(a=>{const s=new THREE.Mesh(new THREE.CylinderGeometry(.32,.32,.03,24,1,false,a,Math.PI/2),std(0x333333,{side:THREE.DoubleSide}));chop.add(s)});opt.add(tag(chop,'chop'));
const pmtM=std(0x888e96,{emissive:0x000000});const pmt=cy(.22,.6,pmtM,2.45,BY,.5,opt,0,Math.PI/2);tag(pmt,'pmt');
// berkas
const mk=()=>new THREE.MeshBasicMaterial({color:0xff0000,transparent:true,opacity:.85,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});
const mC=mk(),mS1=mk(),mS2=mk(),mR=mk();
function seg(a,b,m){const A=new THREE.Vector3(a[0],BY,a[1]),B=new THREE.Vector3(b[0],BY,b[1]);const L=A.distanceTo(B);const o=new THREE.Mesh(new THREE.CylinderGeometry(.03,.03,L,8),m);o.position.copy(A).add(B).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),B.clone().sub(A).normalize());o.renderOrder=10;opt.add(o)}
for(let i=0;i<common.length-1;i++)seg(common[i],common[i+1],mC);
for(let i=0;i<sampP.length-1;i++)seg(sampP[i],sampP[i+1],i<3?mS1:mS2);
for(let i=0;i<refP.length-1;i++)seg(refP[i],refP[i+1],mR);
function route(a){const p=common.concat(a.slice(1));const cum=[0];for(let i=1;i<p.length;i++)cum.push(cum[i-1]+Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]));return{p,cum,L:cum[cum.length-1]}}
const rS=route(sampP),rR=route(refP);const dCuv=rS.cum[common.length-1+3];
function posAt(r,u){u=u%r.L;let i=1;while(r.cum[i]<u)i++;const t=(u-r.cum[i-1])/(r.cum[i]-r.cum[i-1]);return[r.p[i-1][0]+(r.p[i][0]-r.p[i-1][0])*t,r.p[i-1][1]+(r.p[i][1]-r.p[i-1][1])*t]}
const pM=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});const pulses=[];
const glowT=canvasTex(64,64,(g)=>{const r=g.createRadialGradient(32,32,0,32,32,32);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.3,'rgba(255,255,255,.4)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,64,64)});
const halos=[];[[-2.5,-1.7,'c',.8],[-1.9,-1.7,'c',.55],[-1.9,-.6,'c',.6],[-1.1,-1.1,'c',.55],[-1.1,.5,'c',.6],[-1.1,.95,'s1',.5],[1.5,.95,'s2',.5],[-1.1,.05,'r',.5],[1.5,.05,'r',.5],[2.3,.5,'p',.9],[0,.95,'s1',.4]].forEach(a=>{const m=new THREE.SpriteMaterial({map:glowT,color:0xff0000,transparent:true,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});const s=new THREE.Sprite(m);s.scale.set(a[3],a[3],1);s.position.set(a[0],BY,a[1]);s.renderOrder=11;opt.add(s);halos.push({m,t:a[2]})});
[rS,rR].forEach((r,k)=>{for(let i=0;i<10;i++){const s=sp(.07,pM,0,BY,0,opt);s.renderOrder=12;pulses.push({s,r,u:i*r.L/10,k})}});
// ---------- UPS, PC, monitor, props
const ups=new THREE.Group();ups.position.set(.9,0,.2);scene.add(ups);
tag(rm(slabG(1.2,1.9,1.2,.12),0x16161a,0,.1,0,ups),'ups');bx(1.2,.14,1.9,0xc9a227,0,.07,0,ups);bx(1.2,.14,1.9,0xc9a227,0,1.37,0,ups);
const upsLed=[];for(let i=0;i<5;i++)upsLed.push(sp(.04,std(0x114411,{emissive:0}),-.2+i*.1,.6,.97,ups));
plane(.5,.2,txt(['ICA'],100,40,'#16161a','#c9a227',28),0,.85,.961,ups);
tag(cy(.09,.05,0xdddddd,.35,1.0,.97,ups,Math.PI/2),'upsbtn');
const folder=bx(1.1,.04,1.5,0x6fb3e0,0,1.46,0,ups);
const pcG=new THREE.Group();pcG.position.set(2.7,0,0);scene.add(pcG);
tag(rm(slabG(.95,2.1,1.9,.08),0x15151a,0,0,0,pcG),'pc');bx(.9,.75,.02,0x8e9298,0,.45,1.06,pcG);bx(.9,.22,.03,0x0a0a0a,0,1.55,1.06,pcG);
tag(cy(.06,.04,0xdddddd,-.25,1.2,1.07,pcG,Math.PI/2),'pcbtn');
for(let i=0;i<4;i++)bx(.07,.03,.03,0x555,.0+i*.1,1.2,1.07,pcG);
const pcLed=sp(.03,std(0x114411,{emissive:0}),-.1,1.2,1.07,pcG);plane(.3,.08,txt(['DELL'],90,24,'#8e9298','#222',18),0,.85,1.075,pcG);
bx(.9,.12,1.3,0xcc2b2b,0,1.96,0,pcG);
const mon=new THREE.Group();mon.position.set(5,0,-.6);scene.add(mon);
bx(.8,.06,.6,0x111111,0,.03,0,mon);bx(.15,.7,.12,0x111111,0,.4,0,mon);
tag(bx(2.7,1.55,.1,0x111111,0,1.3,0,mon),'monbody');
const scrC=document.createElement('canvas');scrC.width=512;scrC.height=300;const scrT=new THREE.CanvasTexture(scrC);scrT.encoding=THREE.sRGBEncoding;
const scr=plane(2.5,1.35,scrT,0,1.3,.055,mon);tag(scr,'screen');
tag(cy(.05,.03,0x333333,1.1,.58,.06,mon,Math.PI/2),'monbtn');const monLed=sp(.025,std(0x114411,{emissive:0}),.95,.58,.06,mon);
const kb=bx(1.7,.05,.6,0x1a1a1a,5,.025,1.1,scene);tag(kb,'kbd');plane(1.6,.5,canvasTex(256,80,(g,w,h)=>{g.fillStyle='#1a1a1a';g.fillRect(0,0,w,h);g.fillStyle='#444';for(let r=0;r<5;r++)for(let c=0;c<20;c++)g.fillRect(6+c*12.3,6+r*14,10,11)}),5,.052,1.1,scene,1);
bx(1.1,.01,.9,0xf2d36b,6.4,.005,1.1);tag(bx(.2,.08,.32,0x111111,6.4,.05,1.1),'mouse');
const kim=new THREE.Group();kim.position.set(-4.6,0,3.3);scene.add(kim);bx(1,.05,.7,0x1f4d3a,0,.03,0,kim);tag(bx(.7,.35,.45,0x3a8a8f,0,.22,0,kim),'kim');bx(.3,.2,.1,0xffffff,0,.45,0,kim);cy(.06,.28,0xf0f0f0,.4,.2,.15,kim);cy(.06,.28,0xf0f0f0,.4,.2,-.1,kim);
bx(.45,.12,.3,0xd9d2c0,-6.2,.06,3.2);bx(.9,.01,1.2,0xffffff,-2,.006,3.7).rotation.y=.2;bx(.7,.15,.4,0x2a62d0,-5.2,.08,-2.6);bx(.7,.08,.3,0xe8dcc0,3.8,.04,2.4);
function cable(pts,c,r){scene.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p))),30,r||.025,6),std(c)))}
cable([[-.4,.4,-1.5],[0,.05,-2.4],[1.5,.05,-2.2],[1.2,.1,-.8]],0x1d2fb0);
cable([[1.5,.3,-.9],[2.3,.03,-2],[3.4,.03,-1.5],[3.8,.05,2.4]],0x111111);cable([[2.8,.4,-1],[3.3,.03,-.6],[3.8,.05,2.2]],0x111111);cable([[4.9,.3,-.7],[4.4,.03,-.3],[3.9,.05,2.3]],0x111111);
// ---------- info
const INFO={body:['Cangkang Agilent Cary 100','Pelindung optik tertutup (sealed optics) yang menjaga komponen dari debu dan uap korosif. Aktifkan “Transparan” untuk melihat bagian dalam.'],
lampcover:['Panel kompartemen lampu','Menutup ruang lampu Visible (tungsten-halogen) dan UV (deuterium). Jenis lampu: perlu diverifikasi dengan manual alat.'],
lid:['Tutup kompartemen sampel','Klik untuk membuka/menutup. Harus tertutup saat pengukuran agar cahaya luar tidak masuk. Kompartemen besar memberi fleksibilitas ukuran sampel.'],
sw:['Saklar power instrumen','Klik untuk ON/OFF. Urutan: UPS → instrumen → komputer → monitor (sesuaikan SOP lab Anda).'],
port:['Konektor ACCESSORIES','Port kontrol aksesori terpusat untuk aksesori Agilent dan pihak ketiga.'],label:['Label servis','Berisi data model, tanggal perawatan, dan teknisi. Isi pada model ini hanya ilustrasi.'],qr:['Stiker QR','QR identitas alat dan kartu perawatan (“Scan Here”).'],
hold_s:['Holder kuvet sampel','Tempat kuvet sampel (jalur berkas depan). Pasang kuvet dengan sisi bening menghadap berkas.'],hold_r:['Holder kuvet referensi','Jalur berkas referensi. Pada simulasi berisi aquades.'],cuv:['Kuvet sampel (1 cm)','Klik untuk memasang/mengambil. Tutup kompartemen harus dibuka dulu. Untuk UV (<340 nm, termasuk thiamin 246 nm) WAJIB kuvet kuarsa, bukan kaca/plastik. Pegang sisi buram, bersihkan dengan Kimwipes.'],cuv_ref:['Kuvet referensi','Berisi blanko sebagai pembanding.'],
lampV:['Lampu Visible (tungsten-halogen)','Sumber cahaya untuk daerah tampak. Titik pindah lampu UV/Vis: perlu diverifikasi dengan manual alat.'],lampD:['Lampu UV (deuterium)','Sumber cahaya untuk daerah UV.'],
mirror:['Cermin','Mengarahkan berkas. Dilapisi kuarsa (quartz overcoated) agar kinerja optik terjaga.'],slit:['Celah variabel (variable slits)','Mengatur resolusi spektral. Celah sempit = resolusi lebih baik, energi lebih kecil.'],grat:['Kisi difraksi (grating)','Memisahkan cahaya putih menjadi panjang gelombang tunggal. Berputar sesuai nm yang dipilih (drive phase-locked mencegah pergeseran puncak).'],
chop:['Chopper ganda','Cakram berputar yang membagi berkas ke jalur sampel dan referensi secara bergantian. Pada animasi diperlambat untuk visualisasi.'],pmt:['Detektor PMT','Photomultiplier tube mengubah intensitas cahaya menjadi sinyal listrik. Absorbansi A = −log10(I/I0).'],
ups:['UPS (ICA)','Melindungi komputer dan instrumen dari mati listrik dan lonjakan tegangan. Nyalakan PERTAMA, matikan TERAKHIR.'],upsbtn:['Tombol power UPS','Klik untuk ON/OFF. LED hijau menyala bertahap menandakan UPS aktif.'],
pc:['Komputer Dell OptiPlex 7010','Menjalankan Cary WinUV dan mengontrol instrumen.'],pcbtn:['Tombol power komputer','Klik untuk ON/OFF. Nyalakan setelah UPS dan instrumen.'],monbody:['Monitor Dell','Menampilkan Windows 7 dan aplikasi Cary WinUV.'],monbtn:['Tombol power monitor','Nyalakan setelah komputer.'],screen:['Layar monitor','Saat desktop tampil, klik untuk membuka Cary WinUV.'],kbd:['Keyboard','Input aplikasi.'],mouse:['Mouse dan mousepad','Navigasi aplikasi.'],kim:['Kimtech Kimwipes','Tisu bebas serat untuk membersihkan sisi bening kuvet. Jangan menggosok keras.']};
function showInfo(k){const i=INFO[k];if(!i)return;$('it').textContent=i[0];$('ix').textContent=i[1]}
// ---------- daya
const ORDER=[['ups','UPS'],['inst','instrumen'],['pc','komputer'],['mon','monitor']];
function power(k){if(S.job){toast('Tunggu pengukuran selesai.');return}
 const i=ORDER.findIndex(o=>o[0]===k);
 if(!S[k]){for(let j=0;j<i;j++)if(!S[ORDER[j][0]]){toast('Nyalakan '+ORDER[j][1]+' terlebih dahulu.');return}S[k]=1;if(k==='inst'){S.warm=0}if(k==='pc'){S.bootT=0}}
 else{for(let j=ORDER.length-1;j>i;j--)if(S[ORDER[j][0]]){toast('Matikan '+ORDER[j][1]+' lebih dulu (urutan kebalikan).');return}
  if(S.app){toast('Tutup aplikasi Cary WinUV terlebih dahulu.');return}
  S[k]=0;if(k==='inst'){S.warm=0;S.base=0}if(k==='pc'){S.booted=0}}}
const desk=()=>S.mon&&S.pc&&S.booted;
function openApp(on){if(on&&!desk()){toast('Aplikasi hanya bisa dibuka setelah komputer dan monitor menyala & Windows siap.');return}if(!on&&S.job){toast('Tunggu pengukuran selesai.');return}S.app=on;$('app').hidden=!on}
function toggleLid(){if(S.job){toast('Tunggu pengukuran selesai.');return}S.lid=S.lid?0:1}
function toggleCuv(){if(S.job){toast('Tunggu pengukuran selesai.');return}if(!S.lid){toast('Buka tutup kompartemen sampel dulu.');return}S.cuv=S.cuv?0:1}
// ---------- layar monitor
let lastScr='';
function drawScreen(){const st=!S.mon?'off':!S.pc?'nosig':!S.booted?'boot':'desk'+S.app;if(st===lastScr)return;lastScr=st;const g=scrC.getContext('2d'),w=512,h=300;
 if(st==='off'){g.fillStyle='#050505';g.fillRect(0,0,w,h)}
 else if(st==='nosig'){g.fillStyle='#0a1a3a';g.fillRect(0,0,w,h);g.fillStyle='#fff';g.font='20px sans-serif';g.fillText('No Signal',200,150)}
 else if(st==='boot'){g.fillStyle='#000';g.fillRect(0,0,w,h);g.fillStyle='#fff';g.font='22px sans-serif';g.fillText('Starting Windows',160,150)}
 else{const gr=g.createRadialGradient(330,140,10,330,140,300);gr.addColorStop(0,'#ff7aa8');gr.addColorStop(1,'#f4d9e4');g.fillStyle=gr;g.fillRect(0,0,w,h);
  ['Adobe Reader XI','Recycle Bin','Cary WinUV','Simple Reads','Concentration','Scan','e1','e21','e22','e23','e24'].forEach((n,i)=>{const x=14+Math.floor(i/6)*66,y=10+(i%6)*44;g.fillStyle=i===2?'#e8c85a':'#fff';g.fillRect(x+14,y,26,24);g.strokeStyle='#2a2a9a';g.strokeRect(x+14,y,26,24);g.fillStyle='#000';g.font='9px sans-serif';g.fillText(n.slice(0,12),x,y+36)});
  g.fillStyle='#3a6fb0';g.fillRect(0,278,w,22);if(S.app){g.fillStyle='#fff';g.fillRect(150,50,300,180);g.fillStyle='#0a3fa8';g.fillRect(150,50,300,16);g.fillStyle='#fff';g.font='11px sans-serif';g.fillText('Cary WinUV – Scan',156,62)}}
 scrT.needsUpdate=true}
// ---------- pengukuran
function pre(){if(!desk())return'Komputer/monitor belum siap.';if(!S.inst)return'Instrumen belum menyala.';if(S.warm<WARM)return'Warm-up belum selesai.';if(S.lid)return'Tutup kompartemen sampel harus tertutup.';if(!S.cuv)return'Letakkan kuvet di holder sampel.';return''}
function range(){const a=+$('s0').value,b=+$('s1').value;if(!(a>=190&&b<=900&&a<b)){toast('Rentang tidak valid (190–900 nm, Start < Stop).');return null}return[a,b]}
function startBase(){const e=pre();if(e){toast(e);return}if(S.sample!=='blank'){setSample('blank');toast('Larutan di kuvet otomatis diganti blanko (HCl 0,1 M).')}const r=range();if(!r)return;S.job={type:'base',l:r[0],stop:r[1],rate:(r[1]-r[0])/1.5}}
function start(){if(S.tab==='conc'){toast('Gunakan tombol Ukur / Ukur semua standar / Ukur sampel.');return}if(S.tab==='scan'){const e=pre();if(e){toast(e);return}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return}const r=range();if(!r)return;S.res={type:'scan',pts:[]};S.job={type:'scan',l:r[0],start:r[0],stop:r[1],rate:(r[1]-r[0])/8,last:r[0]-1,pts:S.res.pts};S.xray=1}
 else{const e=pre();if(e){toast(e);return}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return}const l=+$('sl').value,n=Math.max(1,Math.min(10,+$('sn').value|0));if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return}S.lam=l;S.res={type:'simple',rows:[]};S.job={type:'simple',l,n,i:0,t:0};S.xray=1}
 syncX()}
function runJob(dt){const j=S.job;if(!j)return;
 if(j.type==='read'){j.t+=dt;if(j.t>=.8){j.t=0;j.vals.push(readA(j.l));if(j.vals.length>=j.n){S.job=null;j.cb(j.vals)}}}else if(j.type==='scan'||j.type==='base'){j.l=Math.min(j.stop,j.l+j.rate*dt);S.lam=j.l;if(j.type==='scan'&&j.l-j.last>=1){j.last=j.l;j.pts.push([j.l,readA(j.l)])}
  if(j.l>=j.stop){if(j.type==='base'){S.base=1;toast('Baseline selesai.')}else toast('Scan selesai.');S.job=null}}
 else{j.t+=dt;if(j.t>=1.2){j.t=0;const a=readA(j.l);S.res.rows.push([++j.i,j.l,a,100*Math.pow(10,-a)]);if(j.i>=j.n){S.job=null;toast('Simple Reads selesai.')}}}}
function drawChart(){if(S.tab==='conc')return drawCal();const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#fff';g.fillRect(0,0,w,h);g.strokeStyle='#999';g.fillStyle='#333';g.font='11px sans-serif';
 const r=S.res;if(!r||r.type!=='scan'||!r.pts.length){g.fillText(S.tab==='scan'?'Spektrum akan tampil di sini (Abs vs nm)':'Hasil Simple Reads di tabel',10,20);return}
 const a=+$('s0').value,b=+$('s1').value;const ym=Math.max(1,Math.max(...r.pts.map(p=>p[1]))*1.15);const X=l=>40+(l-a)/(b-a)*(w-50),Y=v=>h-25-v/ym*(h-40);
 g.strokeRect(40,15,w-50,h-40);g.fillText(a,36,h-8);g.fillText(b,w-30,h-8);g.fillText('nm',w/2,h-8);g.fillText(ym.toFixed(1),8,22);g.fillText('Abs',8,h/2);
 g.strokeStyle='#c00';g.lineWidth=1.5;g.beginPath();r.pts.forEach((p,i)=>i?g.lineTo(X(p[0]),Y(p[1])):g.moveTo(X(p[0]),Y(p[1])));g.stroke();g.lineWidth=1;let mx=r.pts[0];r.pts.forEach(q=>{if(q[1]>mx[1])mx=q});g.fillStyle='#d32f2f';g.beginPath();g.arc(X(mx[0]),Y(mx[1]),4,0,7);g.fill();g.fillStyle='#333';g.fillText('λmax '+mx[0].toFixed(0)+' nm, A='+mx[1].toFixed(3),Math.min(X(mx[0])+8,w-150),Y(mx[1])-6)}
function drawTable(){const r=S.res;if(!r||r.type!=='simple'){$('tbl').innerHTML='';return}let t='<table><tr><th>#</th><th>λ (nm)</th><th>Abs</th><th>%T</th></tr>';r.rows.forEach(x=>t+=`<tr><td>${x[0]}</td><td>${x[1]}</td><td>${x[2].toFixed(4)}</td><td>${x[3].toFixed(2)}</td></tr>`);if(r.rows.length>1){const m=r.rows.reduce((s,x)=>s+x[2],0)/r.rows.length;const sd=Math.sqrt(r.rows.reduce((s,x)=>s+(x[2]-m)**2,0)/(r.rows.length-1));t+=`<tr><td colspan=2>Rata-rata ± SD</td><td colspan=2>${m.toFixed(4)} ± ${sd.toFixed(4)}</td></tr>`}$('tbl').innerHTML=t+'</table>'}
function csv(){if(S.tab==='conc'){const C=S.cal,q=C.std.filter(s=>s.a!=null);if(!q.length){toast('Belum ada data.');return}const t='ppm,Abs,SD\n'+q.map(s=>s.c+','+s.a.toFixed(4)+','+s.sd.toFixed(4)).join('\n')+(C.fit?'\n\nslope,'+C.fit.a+'\nintercept,'+C.fit.b+'\nR2,'+C.fit.r2:'');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='kalibrasi_thiamin.csv';a.click();return}const r=S.res;if(!r){toast('Belum ada data.');return}let t=r.type==='scan'?'nm,Abs\n'+r.pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(4)).join('\n'):'n,nm,Abs,%T\n'+r.rows.map(x=>x.map(v=>+v.toFixed(4)).join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='cary100_'+r.type+'.csv';a.click()}
// ---------- kalibrasi thiamin
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const sdv=a=>{if(a.length<2)return 0;const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1))};
function setSample(s,c){S.sample=s;if(c!=null){S.conc=c;$('conc').value=c;$('cv').textContent=c}$('smp').value=s;$('conc').disabled=s!=='std';setLiq()}
function readOne(sample,c,cb){const e=pre();if(e){toast(e);return false}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return false}const l=+$('cl').value;if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return false}S.cal.l=l;setSample(sample,c);S.lam=l;S.xray=1;syncX();S.job={type:'read',l,n:3,t:0,vals:[],cb};return true}
function syncStd(){document.querySelectorAll('#stdtab input').forEach(e=>{const s=S.cal.std[+e.dataset.i];const v=parseFloat(e.value);if(v>=0&&s.c!==v){s.c=v;s.a=null}})}
function measStd(i,all){syncStd();const s=S.cal.std[i];readOne('std',s.c,v=>{s.a=mean(v);s.sd=sdv(v);S.cal.fit=null;S.cal.unk=null;if(all&&i+1<S.cal.std.length)setTimeout(()=>measStd(i+1,true),300);else calc();renderConc()})}
function calc(){syncStd();const p=S.cal.std.filter(s=>s.a!=null);if(p.length<3){S.cal.fit=null;toast('Minimal 3 standar terukur.');renderConc();return}
 const n=p.length,sx=p.reduce((s,q)=>s+q.c,0),sy=p.reduce((s,q)=>s+q.a,0),sxx=p.reduce((s,q)=>s+q.c*q.c,0),sxy=p.reduce((s,q)=>s+q.c*q.a,0);
 const a=(n*sxy-sx*sy)/(n*sxx-sx*sx),b=(sy-a*sx)/n,ym=sy/n;const sst=p.reduce((s,q)=>s+(q.a-ym)**2,0),ssr=p.reduce((s,q)=>s+(q.a-(a*q.c+b))**2,0);const syx=n>2?Math.sqrt(ssr/(n-2)):0;
 S.cal.fit={a,b,r2:1-ssr/sst,n,syx,lod:3.3*syx/a,loq:10*syx/a};renderConc()}
function measUnk(){if(!S.cal.fit){toast('Hitung kurva kalibrasi dulu.');return}const df=Math.max(1,+$('df').value||1);readOne('unk',null,v=>{const A=mean(v),f=S.cal.fit;S.cal.unk={A,sd:sdv(v),c:(A-f.b)/f.a,df};renderConc()})}
function renderConc(){const C=S.cal;let t='<table><tr><th>No</th><th>Konsentrasi (ppm)</th><th>Abs (rata-rata ± SD, n=3)</th><th></th></tr>';
 C.std.forEach((s,i)=>t+=`<tr><td>${i+1}</td><td><input data-i="${i}" type="number" step="0.5" min="0" value="${s.c}"></td><td>${s.a==null?'–':s.a.toFixed(4)+' ± '+s.sd.toFixed(4)}</td><td><button data-m="${i}">Ukur</button></td></tr>`);
 $('stdtab').innerHTML=t+'</table>';
 $('stdtab').querySelectorAll('input').forEach(e=>e.onchange=()=>{const s=C.std[+e.dataset.i];s.c=+e.value;s.a=null;C.fit=null;C.unk=null;renderConc()});
 $('stdtab').querySelectorAll('button').forEach(b=>b.onclick=()=>measStd(+b.dataset.m,false));
 const f=C.fit,u=C.unk;let r='';
 if(f)r+=`<b>Persamaan:</b> y = ${f.a.toFixed(5)}x ${f.b<0?'−':'+'} ${Math.abs(f.b).toFixed(5)}<br><b>R²</b> = ${f.r2.toFixed(5)} ${f.r2>=.995?'✔ baik':'⚠ di bawah 0,995, periksa standar'}<br>LOD ≈ ${f.lod.toFixed(3)} ppm, LOQ ≈ ${f.loq.toFixed(3)} ppm (3,3·s/a dan 10·s/a)`;
 if(u&&f){const aa=C.std.filter(s=>s.a!=null).map(s=>s.a),rng=u.A>=Math.min(...aa)*.999&&u.A<=Math.max(...aa)*1.001;r+=`<hr><b>Sampel:</b> Abs = ${u.A.toFixed(4)} ± ${u.sd.toFixed(4)} (%T = ${(100*Math.pow(10,-u.A)).toFixed(2)})<br>C terukur = ${u.c.toFixed(3)} ppm → C asli = <b>${(u.c*u.df).toFixed(3)} ppm</b> (FP ${u.df})<br>`+(rng?'✔ Abs sampel di dalam rentang kurva':'⚠ Abs sampel di luar rentang kurva: encerkan atau ulangi')}
 $('cres').innerHTML=r;drawCal()}
function drawCal(){const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#fff';g.fillRect(0,0,w,h);const C=S.cal,p=C.std.filter(s=>s.a!=null);
 const xm=Math.max(12,...C.std.map(s=>s.c))*1.1,ym=Math.max(.5,...p.map(s=>s.a),C.unk?C.unk.A:0)*1.2;const X=v=>55+v/xm*(w-70),Y=v=>h-34-v/ym*(h-56);
 g.font='11px sans-serif';g.lineWidth=1;for(let i=0;i<=5;i++){const xv=xm*i/5,yv=ym*i/5;g.strokeStyle='#e6e6e6';g.beginPath();g.moveTo(X(xv),20);g.lineTo(X(xv),h-34);g.moveTo(55,Y(yv));g.lineTo(w-15,Y(yv));g.stroke();g.fillStyle='#333';g.fillText(xv.toFixed(1),X(xv)-8,h-20);g.fillText(yv.toFixed(2),16,Y(yv)+4)}
 g.strokeStyle='#888';g.strokeRect(55,20,w-70,h-54);g.fillStyle='#333';g.fillText('Konsentrasi thiamin (ppm)',w/2-60,h-5);g.save();g.translate(11,h/2+30);g.rotate(-Math.PI/2);g.fillText('Absorbansi',0,0);g.restore();g.fillText('Kurva kalibrasi thiamin @ '+C.l+' nm',60,14);
 const f=C.fit;if(f){g.strokeStyle='#1565c0';g.lineWidth=2;g.beginPath();g.moveTo(X(0),Y(f.b));g.lineTo(X(xm),Y(f.a*xm+f.b));g.stroke();g.lineWidth=1;g.fillStyle='#1565c0';g.fillText('y = '+f.a.toFixed(4)+'x '+(f.b<0?'−':'+')+' '+Math.abs(f.b).toFixed(4),65,36);g.fillText('R² = '+f.r2.toFixed(4),65,50)}
 p.forEach(s=>{g.fillStyle='#d32f2f';g.beginPath();g.arc(X(s.c),Y(s.a),4.5,0,7);g.fill()});
 const u=C.unk;if(u&&f){g.setLineDash([5,4]);g.strokeStyle='#2e7d32';g.beginPath();g.moveTo(55,Y(u.A));g.lineTo(X(u.c),Y(u.A));g.lineTo(X(u.c),h-34);g.stroke();g.setLineDash([]);g.fillStyle='#2e7d32';g.beginPath();g.arc(X(u.c),Y(u.A),5,0,7);g.fill();g.fillText('Sampel '+u.c.toFixed(2)+' ppm',Math.min(X(u.c)+8,w-120),Y(u.A)-8)}
 if(!p.length){g.fillStyle='#666';g.fillText('Ukur standar (tombol Ukur / Ukur semua standar) untuk membuat kurva.',75,h/2)}}
// ---------- skema jalur cahaya (tampak atas)
function drawSch(){const c=$('schc'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#0c121b';g.fillRect(0,0,w,h);
 const X=x=>16+(x+2.9)/5.5*(w-32),Y=z=>14+(z+2.0)/3.4*(h-28);const rgb='rgb('+(col.r*255|0)+','+(col.g*255|0)+','+(col.b*255|0)+')';const v=B.vis,T=B.T,so=B.sOn;
 g.strokeStyle='#3a4d68';g.setLineDash([4,3]);g.strokeRect(X(-.9),Y(-.4),X(.9)-X(-.9),Y(1.4)-Y(-.4));g.setLineDash([]);g.fillStyle='#6f84a3';g.font='9px sans-serif';g.fillText('kompartemen sampel',X(-.85),Y(1.4)+10);
 const line=(p,i,a)=>{g.globalAlpha=Math.max(0,Math.min(1,a))*v;g.strokeStyle=rgb;g.lineWidth=3;g.beginPath();g.moveTo(X(p[i][0]),Y(p[i][1]));g.lineTo(X(p[i+1][0]),Y(p[i+1][1]));g.stroke()};
 for(let i=0;i<common.length-1;i++)line(common,i,1);for(let i=0;i<sampP.length-1;i++)line(sampP,i,(i<3?1:.1+.9*T)*(so?1:.35));for(let i=0;i<refP.length-1;i++)line(refP,i,so?.35:1);g.globalAlpha=1;
 [[.95,1],[.05,0]].forEach(a=>{g.fillStyle=a[1]&&!S.cuv?'rgba(150,200,255,.12)':'rgba(150,200,255,.55)';g.fillRect(X(-.15),Y(a[0]-.15),X(.15)-X(-.15),Y(a[0]+.15)-Y(a[0]-.15))});
 g.strokeStyle='#e8eef5';g.lineWidth=3;MIRS.forEach(m=>{const dx=Math.cos(m[2])*.2,dz=-Math.sin(m[2])*.2;g.beginPath();g.moveTo(X(m[0]-dx),Y(m[1]-dz));g.lineTo(X(m[0]+dx),Y(m[1]+dz));g.stroke()});
 g.fillStyle='#b08d2a';g.fillRect(X(-1.9)-3,Y(-.6)-8,6,16);g.fillStyle='#777';g.beginPath();g.arc(X(-1.1),Y(.5),9,0,7);g.fill();g.fillStyle='#889';g.beginPath();g.arc(X(2.3),Y(.5),8,0,7);g.fill();g.fillStyle=S.inst&&S.warm>2?'#ff9a3c':'#555';g.beginPath();g.arc(X(-2.5),Y(-1.7),7,0,7);g.fill();
 if(v){g.fillStyle='#fff';pulses.forEach(p=>{g.beginPath();g.arc(X(p.s.position.x),Y(p.s.position.z),2.4,0,7);g.fill()})}
 g.font='bold 10px sans-serif';[[1,-2.5,-1.7],[2,-1.9,-1.7],[3,-1.9,-1.2],[4,-1.9,-.6],[5,-1.1,-1.1],[6,-1.1,.5],[7,0,.95],[8,2.3,.5]].forEach(a=>{const x=X(a[1])-10,y=Y(a[2])-10;g.fillStyle='#2d7dd2';g.beginPath();g.arc(x,y,7,0,7);g.fill();g.fillStyle='#fff';g.fillText(a[0],x-3,y+3.5)});
 g.fillStyle='#e8edf3';g.font='10px sans-serif';g.fillText('I0=100',X(.25),Y(.05)+3);if(S.inst)g.fillText('I='+(100*T).toFixed(1),X(.25),Y(.95)+3)}
// ---------- label komponen 3D
const LB=[['Lampu',-2.5,-1.7],['Cermin M1',-1.9,-1.7],['Celah',-1.9,-1.2],['Kisi',-1.9,-.6],['Cermin M2',-1.1,-1.1],['Chopper',-1.1,.5],['Kuvet sampel',0,.95],['Kuvet ref.',0,.05],['PMT',2.3,.5]].map(a=>{const e=document.createElement('div');e.className='lb';e.textContent=a[0];document.body.appendChild(e);return{e,v:new THREE.Vector3(a[1]-3.2,BY+.35,a[2])}});
function updLb(){const w=innerWidth,hh=innerHeight;LB.forEach(l=>{const q=l.v.clone().project(cam);const on=S.lbl&&q.z<1;l.e.style.display=on?'block':'none';if(on){l.e.style.left=((q.x+1)/2*w-20)+'px';l.e.style.top=((1-q.y)/2*hh-8)+'px'}})}
// ---------- UI
const CHK=[['UPS menyala',()=>S.ups],['Instrumen menyala',()=>S.inst],['Komputer menyala',()=>S.pc],['Monitor menyala',()=>S.mon],['Warm-up selesai',()=>S.inst&&S.warm>=WARM],['Cary WinUV dibuka',()=>S.app],['Baseline blanko',()=>S.base],['Kuvet terpasang',()=>S.cuv],['Tutup tertutup',()=>!S.lid]];
function renderUI(){document.querySelectorAll('#p-conc button').forEach(b=>b.disabled=!!S.job);$('chk').innerHTML=CHK.map(c=>`<li class="${c[1]()?'ok':''}">${c[0]}${c[0]==='Warm-up selesai'&&S.inst&&S.warm<WARM?' '+Math.round(S.warm/WARM*100)+'%':''}</li>`).join('');
 $('bLid').textContent=S.lid?'Tutup tutup':'Buka tutup';$('bCuv').textContent=S.cuv?'Ambil kuvet':'Pasang kuvet';$('bX').classList.toggle('on',!!S.xray);$('bB').classList.toggle('on',!!S.beam);
 const st=!S.inst?'Instrument: Not connected':S.warm<WARM?'Instrument: Warming up '+Math.round(S.warm/WARM*100)+'%':'Instrument: Connected – Ready';$('status').textContent=st+(S.job?' | Mengukur…':'');
 $('aStart').disabled=!!S.job;$('aBase').disabled=!!S.job;$('aStop').disabled=!S.job;
 const T=S.cuv?Math.pow(10,-specA(S.lam)):1,A=-Math.log10(T);
 $('hud').textContent=S.inst?`λ  : ${S.lam.toFixed(1)} nm\nI0 : 100.00 (ref)\nI  : ${(100*T).toFixed(2)} (sampel)\n%T : ${(100*T).toFixed(2)}\nAbs: ${(A+(S.job?noise():0)).toFixed(4)}`+(S.lid?'\n⚠ tutup terbuka':'')+(!S.cuv?'\n⚠ kuvet kosong':''):'Instrumen OFF'}
function syncX(){shells.forEach(s=>{s.m.raycast=(S.xray&&!s.keep)?()=>{}:THREE.Mesh.prototype.raycast})}
$('smp').onchange=e=>{S.sample=e.target.value;$('conc').disabled=S.sample==='blank'||S.sample==='unk';setLiq()};$('conc').oninput=e=>{S.conc=+e.target.value;$('cv').textContent=S.conc;setLiq()};
$('bLid').onclick=toggleLid;$('bCuv').onclick=toggleCuv;$('bX').onclick=()=>{S.xray=S.xray?0:1;syncX()};$('bB').onclick=()=>S.beam=S.beam?0:1;
$('bR').onclick=e=>{ctl.autoRotate=!ctl.autoRotate;e.target.classList.toggle('on',ctl.autoRotate)};$('bA').onclick=()=>openApp(true);$('xapp').onclick=()=>openApp(false);
$('bFS').onclick=()=>{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen().catch(()=>toast('Layar penuh diblokir browser.'))};$('bRe').onclick=()=>location.reload();
$('aBase').onclick=startBase;$('aStart').onclick=start;$('aStop').onclick=()=>{S.job=null};$('aCsv').onclick=csv;$('cAll').onclick=()=>measStd(0,true);$('cFit').onclick=calc;$('cUnk').onclick=measUnk;$('cClr').onclick=()=>{S.cal.std.forEach(s=>{s.a=null});S.cal.fit=null;S.cal.unk=null;renderConc()};$('bL').onclick=()=>{S.lbl=S.lbl?0:1;$('bL').classList.toggle('on',!!S.lbl)};
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{if(S.job)return;S.tab=b.dataset.t;document.querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('on',x===b));$('p-scan').hidden=S.tab!=='scan';$('p-simple').hidden=S.tab!=='simple';$('p-conc').hidden=S.tab!=='conc';if(S.tab==='conc')renderConc();S.res=null;drawTable()});
const V={front:[[-1,5.5,12],[1,.8,0]],top:[[1,16,.1],[1,0,0]],back:[[1,5,-12],[1,.8,0]],side:[[14,4,3],[0,.8,0]],inst:[[-3.2,4.5,6.5],[-3.2,.7,.5]],cuv:[[-3.2,2.6,3.6],[-3.2,.8,.9]],mon:[[5,2.2,4.5],[5,1.2,-.6]]};
let fly=null;document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{const v=V[b.dataset.v];fly={t:0,p0:cam.position.clone(),t0:ctl.target.clone(),p1:new THREE.Vector3(...v[0]),t1:new THREE.Vector3(...v[1])}});
// klik 3D
const rc=new THREE.Raycaster(),mp=new THREE.Vector2();let dn=null;
function pick(e){const r=ren.domElement.getBoundingClientRect();mp.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);rc.setFromCamera(mp,cam);const h=rc.intersectObjects(clickables,false);return h.length?h[0].object.userData.key:null}
ren.domElement.addEventListener('pointerdown',e=>dn=[e.clientX,e.clientY]);
ren.domElement.addEventListener('pointerup',e=>{if(!dn||Math.hypot(e.clientX-dn[0],e.clientY-dn[1])>5)return;const k=pick(e);if(!k)return;showInfo(k);
 if(k==='upsbtn')power('ups');else if(k==='sw')power('inst');else if(k==='pcbtn')power('pc');else if(k==='monbtn')power('mon');else if(k==='lid')toggleLid();else if(k==='cuv')toggleCuv();else if(k==='screen'&&desk())openApp(true)});
ren.domElement.addEventListener('pointermove',e=>{ren.domElement.style.cursor=pick(e)?'pointer':'default'});
function resize(){const w=innerWidth,h=innerHeight;ren.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}addEventListener('resize',resize);resize();
// ---------- loop
const B={vis:0,T:1,sOn:true};const clk=new THREE.Clock();let xk=0,uiT=0,chA=0,lastLamp=0;const col=new THREE.Color();
setLiq();syncX();$('conc').disabled=true;
function loop(){requestAnimationFrame(loop);const dt=Math.min(clk.getDelta(),.1);
 if(S.inst)S.warm=Math.min(WARM,S.warm+dt);if(S.pc&&!S.booted){S.bootT+=dt;if(S.bootT>4)S.booted=1}
 runJob(dt);
 if(fly){fly.t=Math.min(1,fly.t+dt/.9);const k=fly.t*fly.t*(3-2*fly.t);cam.position.lerpVectors(fly.p0,fly.p1,k);ctl.target.lerpVectors(fly.t0,fly.t1,k);if(fly.t>=1)fly=null}
 ctl.update();
 // animasi objek
 const lt=S.lid?-1.6:0;lid.rotation.x+=(lt-lid.rotation.x)*Math.min(1,dt*5);
 cuvK+=((S.cuv?1:0)-cuvK)*Math.min(1,dt*5);cuvS.position.set(1.6*(1-cuvK),.18+(.8-.18)*cuvK+Math.sin(Math.PI*cuvK)*.5,3+(.95-3)*cuvK);
 rocker.rotation.x=S.inst?-.3:.3;ledM.emissive.setHex(S.inst?0x00ff00:0);ledM.color.setHex(S.inst?0x22ff22:0x114411);
 upsLed.forEach((l,i)=>{const on=S.ups&&performance.now()%100000>0&&true;l.material.emissive.setHex(on?0x00ff00:0);l.material.color.setHex(on?0x22ff22:0x114411)});
 pcLed.material.emissive.setHex(S.pc?0x00ff00:0);monLed.material.emissive.setHex(S.mon?0x00ff00:0);
 xk+=((S.xray?1:0)-xk)*Math.min(1,dt*4);shW.opacity=shD.opacity=1-.88*xk;shW.depthWrite=shD.depthWrite=xk<.05;shells.forEach(s=>{s.e.visible=xk>.02;s.e.material.opacity=xk*.9});
 // lampu & berkas
 const lampOn=S.inst&&S.warm>2;if(lampOn&&!S.autoX){S.autoX=1;S.xray=1;syncX();toast("Mode transparan aktif otomatis agar berkas terlihat (tombol Transparan untuk mematikan).")}lampVM.emissive.setHex(lampOn&&S.lam>=350?0xff7a00:0);lampD.material.emissive.setHex(lampOn&&S.lam<350?0x2299cc:0);
 chop.rotation.y+=(S.inst?(S.job?6:3):0)*dt;grat.rotation.y=(S.lam-190)/710*.8;
 W(S.lam);col.setRGB(...W(S.lam));[mC,mS1,mS2,mR,pM].forEach(m=>m.color.copy(col));
 const T=S.cuv&&!S.lid?Math.pow(10,-specA(S.lam)):1;const vis=S.beam&&lampOn?1:0;const sOn=Math.sin(chop.rotation.y*2)>0;B.vis=vis;B.T=T;B.sOn=sOn;
 mC.opacity=.9*vis;mS1.opacity=.9*vis*(sOn?1:.3);mR.opacity=.9*vis*(sOn?.3:1);mS2.opacity=.9*vis*(sOn?1:.3)*(.1+.9*T);
 pmtM.emissive.setRGB(col.r*.5*T*vis,col.g*.5*T*vis,col.b*.5*T*vis);halos.forEach(q=>{q.m.color.copy(col);const f=q.t==="c"?1:q.t==="s1"?(sOn?1:.3):q.t==="s2"?(sOn?1:.3)*(.1+.9*T):q.t==="r"?(sOn?.3:1):.3+.7*T;q.m.opacity=.8*vis*f});
 const v=S.job?3.2:1.4;pulses.forEach(p=>{p.s.visible=!!vis;if(!vis)return;p.u+=v*dt;const q=posAt(p.r,p.u);p.s.position.set(q[0],BY,q[1]);const u=p.u%p.r.L;const sc=(p.k===0&&u>dCuv)?.2+.8*T:1;p.s.scale.setScalar(sc)});
 // UI
 drawScreen();updLb();drawSch();uiT+=dt;if(uiT>.15){uiT=0;renderUI();if(S.app){drawChart();if(S.res&&S.res.type==='simple')drawTable()}}
 ren.render(scene,cam)}
loop();
}
</script></body></html>

"""

components.html(HTML, height=height, scrolling=False)
