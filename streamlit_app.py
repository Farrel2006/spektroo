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
    "kurva kalibrasi, kadar, dan % recovery. Data spektrum bersifat ilustratif, bukan data kalibrasi alat."
)

with st.sidebar:
    st.header("Cara memakai")
    st.markdown(
        """
1. Nyalakan berurutan: **UPS** → **instrumen** → **komputer** → **monitor** (klik tombolnya di model 3D).
2. Tunggu *warm-up* selesai (lihat panel *Urutan operasi*). Mode transparan aktif otomatis.
3. Atur **warna & intensitas lampu** di panel *Lampu sumber*. Mode otomatis membedakan lampu tungsten (amber) dan lampu deuterium (ungu).
4. Klik layar monitor atau **Buka Cary WinUV**.
5. Buka tutup, pasang kuvet kuarsa, tutup, lalu **Baseline** (blanko HCl 0,1 M).
6. Tab **Scan** (400–200 nm): grafik bergerak dari panjang gelombang besar ke kecil. λmax dihitung otomatis (data simulasi ≈ 246 nm).
7. Tab **Concentration**:
   - isi absorban standar (**Ukur**, atau ketik manual), lalu **Hitung kurva**;
   - isi **massa sampel**, **volume labu**, **faktor pengenceran**, dan **absorban sampel**;
   - isi **absorban sampel + spike** dan **konsentrasi spike** untuk **% recovery**;
   - hasil: persamaan, R², konsentrasi, **kadar**, **% recovery**, dan grafik **konsentrasi vs absorban**.
        """
    )
    height = st.slider("Tinggi tampilan (px)", 500, 1300, 900, 20)

HTML = r"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digital Twin Cary 100</title>
<style>
:root{--bg:#10161f;--card:#16202eeb;--line:#2b3d55;--tx:#e6edf5;--mut:#8fa3bd;--ac:#35c2b0;--ac2:#4b8df8;--warn:#ff7b6b}
*{box-sizing:border-box}body{margin:0;font:13px/1.35 "Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--tx);overflow:hidden}
/* Area alat dipisahkan dari panel info agar keterangan tidak menutupi model 3D. */
#c{position:fixed;inset:0 320px 0 0;width:calc(100% - 320px);height:100%;display:block}
button,select,input{font:inherit}
button{background:#22324a;color:var(--tx);border:1px solid var(--line);border-radius:7px;padding:5px 10px;cursor:pointer;transition:background .15s}
button:hover{background:#2e4466}button.on{background:var(--ac2);border-color:#8db6ff;color:#fff}button.pri{background:var(--ac);border-color:#8de8db;color:#04211d;font-weight:600}button:disabled{opacity:.45;cursor:not-allowed}
.bar{position:fixed;top:8px;left:8px;right:328px;display:flex;flex-wrap:wrap;gap:8px;z-index:6;pointer-events:none}
.grp{display:flex;flex-wrap:wrap;gap:4px;padding:4px;background:var(--card);border:1px solid var(--line);border-radius:10px;pointer-events:auto;align-items:center}
.grp>span{color:var(--mut);font-size:11px;padding:0 6px 0 4px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.col{position:fixed;top:92px;bottom:80px;width:250px;display:flex;flex-direction:column;gap:8px;z-index:4;overflow:auto;pointer-events:none}
.col>.panel{pointer-events:auto;flex:none}#colL{left:8px}#colR{right:8px;width:304px}
body.hp .col{display:none}
@media(max-width:820px){#c{inset:0;width:100%;height:100%}.bar{right:8px}.col{width:46vw!important;top:120px}#colR{width:46vw!important}#hud{left:50%;transform:translateX(-50%);width:98vw;max-width:98vw}}
h4{margin:0 0 6px;font-size:12px;color:var(--ac);font-weight:600}
#prog{height:4px;background:#243349;border-radius:3px;margin-bottom:8px;overflow:hidden}#prog i{display:block;height:100%;width:0;background:var(--ac);transition:width .3s}
#chk{counter-reset:s;list-style:none;margin:0;padding:0}#chk li{counter-increment:s;display:flex;gap:8px;align-items:center;padding:2px 0;color:var(--mut)}
#chk li:before{content:counter(s);width:18px;height:18px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;font-size:10px;flex:none}
#chk li.ok{color:var(--tx)}#chk li.ok:before{content:"✓";background:var(--ac);color:#04211d;border-color:var(--ac)}
.lab{display:block;margin:7px 0 2px;color:var(--mut);font-size:12px}.panel select,.panel input[type=range]{width:100%}
.row{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.panel input[type=color]{width:34px;height:26px;padding:0;border:1px solid var(--line);border-radius:6px;background:none}
.sw{width:22px;height:22px;border-radius:50%;border:2px solid #fff9;padding:0}
#lmSw{height:34px;border-radius:8px;border:2px solid #fff7;margin-top:8px;display:grid;place-items:center;font-weight:700;font-size:12px;color:#fff;text-shadow:0 0 3px #000,0 0 6px #000;transition:background .2s,box-shadow .2s}
.cap{font-size:11px;color:var(--mut);line-height:1.4}
#hud{position:fixed;left:0;transform:none;bottom:8px;display:flex;gap:6px;align-items:stretch;justify-content:center;padding:6px;z-index:5;width:calc(100% - 320px);max-width:calc(100% - 320px);overflow:auto;background:transparent;border:none;pointer-events:none}
.cell{min-width:72px;background:#0b121b;border:1px solid var(--line);border-radius:8px;padding:3px 8px;text-align:center}.cell small{display:block;color:var(--mut);font-size:10px}
.cell b{font:600 16px ui-monospace,Consolas,monospace}.cell.hi b{color:var(--ac)}.warn{align-self:center;color:var(--warn);font-size:12px;padding:0 6px;white-space:nowrap}
.lb{position:fixed;pointer-events:auto;cursor:pointer;user-select:none;font-size:10px;background:#000b;color:#fff;padding:2px 5px;border:1px solid #61748b;border-radius:4px;z-index:3;white-space:nowrap;transition:background .15s,border-color .15s}.lb:hover{background:#17665f;border-color:#7be3d5}
#toast{position:fixed;top:56px;left:50%;transform:translateX(-50%);background:#b3321f;color:#fff;padding:7px 14px;border-radius:6px;z-index:9;opacity:0;transition:opacity .3s;pointer-events:none;max-width:90%}
#app{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:min(720px,96vw);max-height:94vh;overflow:auto;background:#ece9d8;color:#111;border:2px solid #0a246a;border-radius:6px;z-index:8;box-shadow:0 10px 40px #000a}
#app[hidden]{display:none}.wt{background:linear-gradient(#2a62d0,#0a3fa8);color:#fff;padding:5px 8px;display:flex;justify-content:space-between;align-items:center}
.wt button{padding:0 7px;background:#c33;border-color:#fff;color:#fff}
#app .bd{padding:8px}#app button{background:#f3f3ee;color:#111;border:1px solid #777}#app button:hover{background:#fff}#app button.on{background:#cfe0ff}
#app input{width:74px}#app input#massa{width:90px}#app table{width:100%;border-collapse:collapse;font-size:12px}#app td,#app th{border:1px solid #aaa;padding:2px 5px;text-align:right}
#app td input{width:92px}
#app .bx{border:1px solid #aaa;background:#f6f4e8;padding:6px;margin-top:6px;line-height:2}
#status{margin:6px 0;font-weight:600}canvas#chart{width:100%;background:#fff;border:1px solid #888}
#scanRes{margin:4px 0;font-size:12px}
/* Tombol lipat panel kiri/kanan. Tetap terlihat meskipun panel disembunyikan. */
.panel-toggle{position:fixed;top:50%;transform:translateY(-50%);z-index:7;width:28px;height:58px;padding:0;display:flex;align-items:center;justify-content:center;background:#16202ef2;color:var(--ac);font-size:25px;font-weight:700;border:1px solid #47617e;box-shadow:0 2px 12px #0007;pointer-events:auto}
#toggleLeft{left:258px;border-radius:0 9px 9px 0}
#toggleRight{right:312px;border-radius:9px 0 0 9px}
body.left-hidden #colL{display:none}
body.right-hidden #colR{display:none}
body.left-hidden #toggleLeft,body.hp #toggleLeft{left:8px;border-radius:0 9px 9px 0}
body.right-hidden #toggleRight,body.hp #toggleRight{right:8px;border-radius:9px 0 0 9px}
/* Saat panel kanan tertutup, bidang 3D memakai seluruh lebar tampilan. */
body.right-hidden #c,body.hp #c{inset:0;width:100%;height:100%}
body.right-hidden .bar,body.hp .bar{right:8px}
body.right-hidden #hud,body.hp #hud{left:0;transform:none;width:100%;max-width:100%}
@media(max-width:820px){
 #toggleLeft{left:calc(8px + 46vw)}
 #toggleRight{right:calc(8px + 46vw)}
 body.left-hidden #toggleLeft,body.hp #toggleLeft{left:8px}
 body.right-hidden #toggleRight,body.hp #toggleRight{right:8px}
}
</style></head><body>
<canvas id="c"></canvas>
<div class="bar">
 <div class="grp"><span>Kamera</span><button data-v="front">Depan</button><button data-v="top">Atas</button><button data-v="back">Belakang</button><button data-v="side">Samping</button><button data-v="inst">Instrumen</button><button data-v="opt">Optik</button><button data-v="lamp">Lampu</button><button data-v="cuv">Kuvet</button><button data-v="mon">Monitor</button></div>
 <div class="grp"><span>Tampilan</span><button id="bX">Transparan</button><button id="bB" class="on">Berkas</button><button id="bL" class="on">Label</button><button id="bR">Putar</button></div>
 <div class="grp"><button id="bA" class="pri">Buka Cary WinUV</button><button id="bP">Panel</button><button id="bFS">Layar penuh</button><button id="bRe">Reset</button></div>
</div>
<!-- Tombol panah untuk menyembunyikan dan memunculkan panel samping -->
<button id="toggleLeft" class="panel-toggle" type="button" aria-label="Sembunyikan panel kiri" title="Sembunyikan panel kiri">‹</button>
<button id="toggleRight" class="panel-toggle" type="button" aria-label="Sembunyikan panel kanan" title="Sembunyikan panel kanan">›</button>
<div class="col" id="colL">
 <div class="panel"><h4>Urutan operasi</h4><div id="prog"><i></i></div><ul id="chk"></ul></div>
 <div class="panel"><h4>Sampel &amp; kuvet</h4>
  <label class="lab">Larutan</label><select id="smp"><option value="blank">Blanko (HCl 0,1 M)</option><option value="std">Standar thiamin</option><option value="unk">Sampel thiamin (tak diketahui)</option><option value="spk">Sampel + spike</option></select>
  <label class="lab">Konsentrasi: <b id="cv">6</b> ppm</label><input type="range" id="conc" min="0" max="25" step="0.5" value="6">
  <div class="row" style="margin-top:8px"><button id="bLid">Buka tutup</button><button id="bCuv">Pasang kuvet</button></div>
  <p class="cap" style="margin:8px 0 0">Spektrum thiamin bersifat ilustratif (λmax sekitar 246 nm dalam HCl 0,1 M; verifikasi dengan SOP). Untuk daerah UV, gunakan kuvet kuarsa.</p></div>
 <div class="panel"><h4>Lampu sumber</h4>
  <label class="lab">Mode warna</label><select id="lmMode"><option value="auto">Otomatis (Tungsten = amber, deuterium = ungu)</option><option value="manual">Manual (pilih warna)</option></select>
  <label class="lab">Warna lampu</label><div class="row"><input type="color" id="lmColor" value="#ffb000">
   <button class="sw" data-lc="#ffb000" style="background:#ffb000" title="Amber"></button><button class="sw" data-lc="#ffffff" style="background:#fff" title="Putih"></button><button class="sw" data-lc="#8a4dff" style="background:#8a4dff" title="Ungu UV"></button><button class="sw" data-lc="#1e7bff" style="background:#1e7bff" title="Biru"></button><button class="sw" data-lc="#00d5ff" style="background:#00d5ff" title="Cyan"></button><button class="sw" data-lc="#14e06b" style="background:#14e06b" title="Hijau"></button><button class="sw" data-lc="#ff2d2d" style="background:#ff2d2d" title="Merah"></button></div>
  <label class="lab">Intensitas</label><input type="range" id="lmI" min="0.3" max="2" step="0.1" value="1">
  <div id="lmSw">Lampu padam</div>
  <p class="cap" id="lmInfo" style="margin:8px 0 0"></p></div>
</div>
<div class="col" id="colR">
 <div class="panel" id="info"><h4 id="it">Klik bagian mana saja</h4><div id="ix" class="cap" style="font-size:12px;color:var(--tx)">Klik label komponen pada model atau klik langsung komponennya. Penjelasan tampil di panel samping ini, di luar area alat.</div></div>
 <div class="panel"><h4>Jalur cahaya (tampak atas)</h4><canvas id="schc" width="290" height="190" style="width:100%;display:block;margin:4px 0"></canvas>
  <div class="cap">1 Lampu → 2 Cermin M1 → 3 Celah masuk → 4 Kisi (memilih λ) → 5 Cermin M2 → 6 Chopper (membagi berkas) → 7 Kuvet sampel &amp; referensi → 8 Detektor PMT. Di tiap cermin sudut datang = sudut pantul. Berkas sampel meredup setelah kuvet.</div></div>
</div>
<div class="panel" id="hud"></div>
<div id="toast"></div>
<div id="app" hidden>
 <div class="wt"><span>Cary WinUV</span><button id="xapp">✕</button></div>
 <div class="bd">
  <div><button data-t="scan" class="on">Scan</button> <button data-t="simple">Simple Reads</button> <button data-t="conc">Concentration</button></div>
  <div id="status"></div>
  <div id="p-scan" style="margin:6px 0">λ awal <input id="s0" type="number" value="400"> nm &nbsp; λ akhir <input id="s1" type="number" value="200"> nm <small>(190–900; urut menurun)</small></div>
  <div id="p-simple" style="margin:6px 0" hidden>λ <input id="sl" type="number" value="246"> nm &nbsp; Replikat <input id="sn" type="number" value="3" min="1" max="10"></div>
  <div id="p-conc" hidden style="margin:6px 0">
   λ analisis <input id="cl" type="number" value="246"> nm <button id="cUseL">Pakai λmax scan</button> <small>(thiamin ≈ 246 nm dalam HCl 0,1 M)</small>
   <div id="stdtab"></div>
   <div style="margin-top:4px"><button id="cAddStd">+ Tambah standar</button></div>
   <div class="bx"><b>Sampel</b><br>
    Massa sampel <input id="massa" type="number" step="0.0001" min="0" value="2.5012"> g &nbsp;
    Volume labu <input id="vol" type="number" step="1" min="0" value="50"> mL &nbsp;
    Faktor pengenceran <input id="df" type="number" min="1" step="0.5" value="1"><br>
    Absorban sampel <input id="aU" type="number" step="0.001" min="0" placeholder="isi / ukur"> &nbsp;
    Bobot rata-rata 1 tablet (opsional) <input id="tabw" type="number" step="0.001" min="0" placeholder="g"></div>
   <div class="bx"><b>Recovery (sampel + spike)</b><br>
    Absorban sampel + spike <input id="aSp" type="number" step="0.001" min="0" placeholder="isi / ukur"> &nbsp;
    Konsentrasi spike yang ditambahkan <input id="cAdd" type="number" step="0.5" min="0" value="2"> ppm</div>
   <div style="margin-top:6px;display:flex;gap:5px;flex-wrap:wrap"><button id="cAll">Ukur semua standar</button><button id="cFit">Hitung kurva</button><button id="cUnk">Ukur sampel</button><button id="cSpk">Ukur sampel + spike</button><button id="cClr">Hapus data</button></div></div>
  <canvas id="chart" width="640" height="280"></canvas>
  <div id="scanBox"><div id="scanRes"></div><button id="bUseL">Pakai λmax untuk analisis</button></div>
  <div id="cres" style="margin-top:4px;font-size:12px"></div>
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
const AUTO_V='#ffb000', AUTO_D='#8a4dff';
const S={ups:0,inst:0,pc:0,mon:0,booted:0,bootT:0,warm:0,base:0,lid:0,cuv:0,app:0,xray:0,beam:1,job:null,lam:500,sample:'blank',conc:6,spkC:2,tab:'scan',res:null,lbl:1,autoX:0,camOpt:0,lampMode:'auto',lampColor:AUTO_V,lampI:1,lmax:null,out:{}};
S.cal={l:246,std:[0,5,10,15,20,25].map(c=>({c,a:null,sd:null})),fit:null,unk:null,spk:null};
// ---------- util
let toastT;function toast(t){const e=$('toast');e.textContent=t;e.style.opacity=1;clearTimeout(toastT);toastT=setTimeout(()=>e.style.opacity=0,2800)}
function W(l){let r=0,g=0,b=0;if(l<380)return[.55,.25,1];if(l<440){r=(440-l)/60;b=1}else if(l<490){g=(l-440)/50;b=1}else if(l<510){g=1;b=(510-l)/20}else if(l<580){r=(l-510)/70;g=1}else if(l<645){r=1;g=(645-l)/65}else if(l<=780)r=1;else return[.5,.1,.1];return[r,g,b]}
const G=(l,m,s)=>Math.exp(-.5*((l-m)/s)**2);
// Thiamin HCl dalam HCl 0,1 M (ILUSTRATIF): puncak ~246 nm, A1%1cm ~410 -> ~0,0395 Abs per ppm
const THI=(l,c)=>c*.0395*(G(l,246,12.5)+.10*G(l,272,16)+.9*G(l,205,11));
const UNK=7.35;
function specA(l){const s=S.sample;const c=s==='unk'?UNK:s==='spk'?UNK+S.spkC*.97:s==='std'?S.conc:0;return Math.min(3.5,THI(l,c))}
const noise=()=>(Math.random()-.5)*.004;
const readA=l=>Math.max(0,(S.cuv?specA(l):0)+noise());
// ---------- scene
const scene=new THREE.Scene();scene.background=new THREE.Color(0x1b2330);
const cam=new THREE.PerspectiveCamera(45,1,.1,100);cam.position.set(-1,6.2,16);
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
const bumpT=canvasTex(256,256,(g)=>{const d=g.createImageData(256,256);for(let i=0;i<d.data.length;i+=4){const v=122+Math.random()*12;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0)});bumpT.wrapS=bumpT.wrapT=THREE.RepeatWrapping;bumpT.encoding=THREE.LinearEncoding;
const shW=new THREE.MeshPhysicalMaterial({color:0xf1f1ec,roughness:.36,clearcoat:.55,clearcoatRoughness:.25,bumpMap:bumpT,bumpScale:.12,transparent:true});
const shD=new THREE.MeshPhysicalMaterial({color:0x34373b,roughness:.48,metalness:.1,clearcoat:.35,bumpMap:bumpT,bumpScale:.12,transparent:true});
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
for(let i=0;i<10;i++){bx(.02,.3,.06,0x1c1e22,2.805,.25,-1.8+i*.16,cary);bx(.02,.3,.06,0x1c1e22,-2.805,.25,-1.8+i*.16,cary)}bx(5.4,.012,.02,0x1c1e22,0,.5,2.2,cary);[[-2.6,-2],[2.6,-2],[-2.6,2],[2.6,2]].forEach(a=>cy(.13,.05,0x111111,a[0],-.0,a[1],cary));
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
const silver=new THREE.MeshStandardMaterial({color:0xe6eaee,metalness:1,roughness:.05});
const gold=std(0xc9a227,{metalness:.9,roughness:.3}),steel=std(0x8a9096,{metalness:.7,roughness:.35}),darkM=std(0x2a2d32,{metalness:.4,roughness:.5});
const glassT=o=>std(0xcfe6ff,{transparent:true,opacity:o,roughness:.05,metalness:0});
const common=[[-2.2,-1.7],[-1.9,-1.7],[-1.9,-1.2],[-1.9,-.6],[-1.1,-1.1],[-1.1,.5]];
const sampP=[[-1.1,.5],[-1.1,.95],[-.15,.95],[.15,.95],[1.5,.95],[2.3,.5]];
const refP=[[-1.1,.5],[-1.1,.05],[1.5,.05],[2.3,.5]];
// sasis & rel
bx(5.2,.03,4,std(0x7b8087,{metalness:.5,roughness:.5}),0,.505,0,opt);
[[5.2,.14,.05,0,.58,-2],[5.2,.14,.05,0,.58,2],[.05,.14,4,-2.6,.58,0],[.05,.14,4,2.6,.58,0]].forEach(a=>bx(a[0],a[1],a[2],steel,a[3],a[4],a[5],opt));
[[4.4,.05,.1,0,.66,-.62],[.1,.05,3,2.05,.66,.4]].forEach(a=>tag(bx(a[0],a[1],a[2],steel,a[3],a[4],a[5],opt),'rail'));
// cermin (cakram perak, dudukan, 3 sekrup emas)
const MIRS=[];
function mirrors(p){for(let i=1;i<p.length-1;i++){if(i===3&&p===common)continue;const a=p[i-1],b=p[i],c=p[i+1];const d1=[b[0]-a[0],b[1]-a[1]],d2=[c[0]-b[0],c[1]-b[1]];const n1=Math.hypot(...d1),n2=Math.hypot(...d2);if(n1<.2||n2<.01)continue;const nx=d2[0]/n2-d1[0]/n1,nz=d2[1]/n2-d1[1]/n1;if(Math.hypot(nx,nz)<.1)continue;
 const m=new THREE.Group();m.position.set(b[0],BY,b[1]);m.rotation.y=Math.atan2(nx,nz);MIRS.push([b[0],b[1],m.rotation.y]);
 cy(.17,.035,silver,0,0,0,m,Math.PI/2);bx(.36,.36,.05,darkM,0,0,-.05,m);[[-.11,.11],[.11,.11],[0,-.13]].forEach(s=>cy(.02,.08,gold,s[0],s[1],-.1,m,Math.PI/2));bx(.07,.26,.07,darkM,0,-.2,-.05,m);opt.add(tag(m,'mirror'))}}
mirrors(common);mirrors(sampP);mirrors(refP);
// Lampu tungsten (filamen + bola kaca) dan lampu deuterium (tabung + jendela)
tag(bx(1.0,.5,.8,glassT(.18),-2.35,.78,-1.6,opt),'lampbox');
const cOff=new THREE.Color(0xcfe6ff);
const lampVM=std(0x442200,{emissive:0x000000}),bulbVM=std(0xcfe6ff,{transparent:true,opacity:.3,roughness:.05,emissive:0x000000});
const lampV=cy(.012,.16,lampVM,-2.6,BY,-1.7,opt,0,Math.PI/2);tag(lampV,'lampV');
for(let i=-2;i<=2;i++){const c=new THREE.Mesh(new THREE.TorusGeometry(.03,.007,8,16),lampVM);c.position.set(-2.6+i*.03,BY,-1.7);c.rotation.y=Math.PI/2;opt.add(tag(c,'lampV'))}
tag(sp(.14,bulbVM,-2.6,BY,-1.7,opt),'lampV');tag(cy(.08,.2,gold,-2.8,BY,-1.7,opt,0,Math.PI/2),'lampV');
const lampD=cy(.1,.34,std(0xcfe6ff,{transparent:true,opacity:.4,roughness:.05,emissive:0x000000}),-2.2,BY,-1.0,opt,Math.PI/2,0);tag(lampD,'lampD');
tag(cy(.17,.4,steel,-2.2,BY,-.7,opt,Math.PI/2,0),'lampD');
const d2Win=cy(.07,.02,std(0x99ddff,{emissive:0x000000}),-2.2,BY,-1.19,opt,Math.PI/2,0);tag(d2Win,'lampD');
const sel=new THREE.Group();sel.position.set(-2.2,BY,-1.7);sel.rotation.y=Math.PI/4;cy(.15,.03,silver,0,0,0,sel,Math.PI/2);bx(.3,.3,.04,darkM,0,0,-.04,sel);opt.add(tag(sel,'selector'));
const lightV=new THREE.PointLight(0xffd9a0,0,3.4),lightD=new THREE.PointLight(0x88aaff,0,3.4);lightV.position.set(-2.6,BY+.1,-1.7);lightD.position.set(-2.2,BY+.1,-1.2);opt.add(lightV,lightD);
// premonokromator (visual, sesuai diagram)
tag(bx(.9,.5,.55,glassT(.16),-.35,.78,-1.6,opt),'premono');tag(cy(.12,.22,gold,-.3,.78,-1.6,opt),'premono');tag(cy(.13,.03,glassT(.5),-.65,BY,-1.6,opt,0,Math.PI/2),'premono');
// celah variabel (masuk & keluar)
function slitA(x,z,ry){const s=new THREE.Group();s.position.set(x,BY,z);s.rotation.y=ry;bx(.2,.24,.04,darkM,-.15,0,0,s);bx(.2,.24,.04,darkM,.15,0,0,s);bx(.56,.05,.08,steel,0,.15,0,s);bx(.56,.05,.08,steel,0,-.15,0,s);opt.add(tag(s,'slit'))}
slitA(-1.9,-1.2,0);slitA(-1.5,-.85,Math.atan2(.8,-.5));
// kisi difraksi bergaris
const grat=new THREE.Group();grat.position.set(-1.9,BY,-.6);bx(.38,.3,.06,gold,0,0,0,grat);
plane(.34,.26,canvasTex(128,128,(g)=>{g.fillStyle='#b8b8c0';g.fillRect(0,0,128,128);g.fillStyle='#55606c';for(let i=0;i<128;i+=3)g.fillRect(i,0,1,128)}),0,0,.032,grat);
cy(.18,.08,steel,0,-.22,0,grat);opt.add(tag(grat,'grat'));
// chopper ganda + motor
const chop=new THREE.Group();chop.position.set(-1.1,BY,.5);
[[0,0],[.07,Math.PI/2]].forEach(a=>[0,Math.PI].forEach(t=>{const s=new THREE.Mesh(new THREE.CylinderGeometry(.32,.32,.025,32,1,false,t+a[1],Math.PI/2),std(0x333840,{side:THREE.DoubleSide,metalness:.6,roughness:.4}));s.position.y=a[0];chop.add(s)}));
cy(.05,.2,gold,0,.02,0,chop);cy(.1,.22,darkM,0,-.2,0,chop);opt.add(tag(chop,'chop'));
// detektor PMT
tag(bx(.75,.55,.8,glassT(.2),2.45,.78,.5,opt),'pmt');
const pmtM=std(0x888e96,{emissive:0x000000,metalness:.6,roughness:.3});const pmt=cy(.22,.6,pmtM,2.45,BY,.5,opt,0,Math.PI/2);tag(pmt,'pmt');
tag(cy(.2,.02,glassT(.5),2.1,BY,.5,opt,0,Math.PI/2),'pmt');tag(cy(.38,.06,steel,2.82,BY,.5,opt,0,Math.PI/2),'pmt');
// accessory controller, dinding kompartemen sampel, jendela kuarsa
tag(cy(.16,.7,darkM,-2.35,.64,1.6,opt,0,Math.PI/2),'accctl');tag(cy(.17,.05,gold,-2.0,.64,1.6,opt,0,Math.PI/2),'accctl');
[-.38,1.38].forEach(z=>tag(bx(1.76,.45,.03,steel,0,.74,z,opt),'liner'));
[.95,.05].forEach(z=>[-.86,.86].forEach(x=>tag(bx(.03,.22,.24,glassT(.35),x,BY,z,opt),'window')));
// berkas
const mk=()=>new THREE.MeshBasicMaterial({color:0xff0000,transparent:true,opacity:.85,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});
const mC=mk(),mS1=mk(),mS2=mk(),mR=mk(),mLV=mk(),mLD=mk();
function seg(a,b,m){const A=new THREE.Vector3(a[0],BY,a[1]),B=new THREE.Vector3(b[0],BY,b[1]);const L=A.distanceTo(B);const o=new THREE.Mesh(new THREE.CylinderGeometry(.03,.03,L,8),m);o.position.copy(A).add(B).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),B.clone().sub(A).normalize());o.renderOrder=10;opt.add(o)}
for(let i=0;i<common.length-1;i++)seg(common[i],common[i+1],mC);seg([-2.6,-1.7],[-2.2,-1.7],mLV);seg([-2.2,-1.2],[-2.2,-1.7],mLD);
for(let i=0;i<sampP.length-1;i++)seg(sampP[i],sampP[i+1],i<3?mS1:mS2);
for(let i=0;i<refP.length-1;i++)seg(refP[i],refP[i+1],mR);
function route(a){const p=common.concat(a.slice(1));const cum=[0];for(let i=1;i<p.length;i++)cum.push(cum[i-1]+Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]));return{p,cum,L:cum[cum.length-1]}}
const rS=route(sampP),rR=route(refP);const dCuv=rS.cum[common.length-1+3];
function posAt(r,u){u=u%r.L;let i=1;while(r.cum[i]<u)i++;const t=(u-r.cum[i-1])/(r.cum[i]-r.cum[i-1]);return[r.p[i-1][0]+(r.p[i][0]-r.p[i-1][0])*t,r.p[i-1][1]+(r.p[i][1]-r.p[i-1][1])*t]}
const pM=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});const pulses=[];
const glowT=canvasTex(64,64,(g)=>{const r=g.createRadialGradient(32,32,0,32,32,32);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.3,'rgba(255,255,255,.4)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,64,64)});
// tekstur lampu: INTI SOLID berwarna + lingkar cahaya tipis (bukan gradasi pudar)
const coreT=canvasTex(128,128,(g)=>{const r=g.createRadialGradient(64,64,0,64,64,64);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.40,'rgba(255,255,255,1)');r.addColorStop(.46,'rgba(255,255,255,.75)');r.addColorStop(.62,'rgba(255,255,255,.22)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,128,128)});
const halos=[];[[-2.6,-1.7,'lv',1.1],[-2.2,-1.2,'ld',1.0],[-1.9,-1.7,'c',.55],[-1.9,-.6,'c',.6],[-1.1,-1.1,'c',.55],[-1.1,.5,'c',.6],[-1.1,.95,'s1',.5],[1.5,.95,'s2',.5],[-1.1,.05,'r',.5],[1.5,.05,'r',.5],[2.3,.5,'p',.9],[0,.95,'s1',.4]].forEach(a=>{const lamp=a[2]==='lv'||a[2]==='ld';const m=new THREE.SpriteMaterial({map:lamp?coreT:glowT,color:0xff0000,transparent:true,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});const s=new THREE.Sprite(m);s.scale.set(a[3],a[3],1);s.position.set(a[0],BY,a[1]);s.renderOrder=11;opt.add(s);halos.push({m,t:a[2]})});
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
const INFO={premono:['Premonokromator (model ilustratif)','Komponen ini ditampilkan sebagai ilustrasi jalur optik tambahan. Keberadaan dan konfigurasi pada Cary 100 harus dikonfirmasi dengan manual resmi alat.'],selector:['Cermin pemilih sumber','Mengarahkan sumber cahaya yang digunakan: tungsten untuk daerah tampak dan deuterium untuk daerah UV. Titik perpindahan pada model ini bersifat ilustratif.'],accctl:['Accessory controller','Pengontrol aksesori yang dapat menghubungkan instrumen dengan aksesori yang kompatibel.'],lampbox:['Rumah lampu','Ruang yang menempatkan sumber cahaya tungsten dan deuterium.'],rail:['Rel optik','Rangka penyangga komponen optik agar berada pada posisi yang sejajar.'],liner:['Dinding kompartemen sampel','Bagian yang membatasi area kompartemen tempat kuvet sampel dan referensi ditempatkan.'],window:['Jendela kompartemen optik','Area lintasan berkas cahaya masuk atau keluar dari kompartemen sampel.'],body:['Cangkang Agilent Cary 100','Pelindung luar instrumen. Aktifkan tampilan transparan untuk melihat bagian dalam pada simulasi.'],
lampcover:['Panel kompartemen lampu','Menutup ruang sumber cahaya tungsten dan deuterium pada model simulasi. Rincian konfigurasi lampu harus dicocokkan dengan manual alat yang digunakan.'],
lid:['Tutup kompartemen sampel','Klik untuk membuka/menutup. Harus tertutup saat pengukuran agar cahaya luar tidak masuk. Kompartemen besar memberi fleksibilitas ukuran sampel.'],
sw:['Saklar power instrumen','Klik untuk ON/OFF. Urutan: UPS → instrumen → komputer → monitor (sesuaikan SOP lab Anda).'],
port:['Konektor ACCESSORIES','Port kontrol aksesori terpusat untuk aksesori Agilent dan pihak ketiga.'],label:['Label servis','Berisi data model, tanggal perawatan, dan teknisi. Isi pada model ini hanya ilustrasi.'],qr:['Stiker QR','QR identitas alat dan kartu perawatan (“Scan Here”).'],
hold_s:['Holder kuvet sampel','Tempat kuvet sampel (jalur berkas depan). Pasang kuvet dengan sisi bening menghadap berkas.'],hold_r:['Holder kuvet referensi','Jalur berkas referensi. Pada simulasi berisi aquades.'],cuv:['Kuvet sampel (1 cm)','Klik untuk memasang/mengambil. Tutup kompartemen harus dibuka dulu. Untuk UV (<340 nm, termasuk thiamin 246 nm) WAJIB kuvet kuarsa, bukan kaca/plastik. Pegang sisi buram, bersihkan dengan Kimwipes.'],cuv_ref:['Kuvet referensi','Berisi blanko sebagai pembanding.'],
lampV:['Lampu tungsten','Sumber cahaya tungsten untuk wilayah tampak (visible). Dalam simulasi, lampu ini ditampilkan dengan warna amber pada mode otomatis. Konfigurasi dan rentang operasinya tetap harus mengikuti manual instrumen.'],lampD:['Lampu deuterium','Sumber cahaya deuterium untuk wilayah ultraviolet (UV). Dalam simulasi, lampu ini ditampilkan dengan warna ungu pada mode otomatis. Warna tersebut hanya pembeda visual, bukan warna asli sinar UV.'],
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
function range(){const a=+$('s0').value,b=+$('s1').value;if(!(a>=190&&a<=900&&b>=190&&b<=900&&a>b)){toast('Masukkan λ awal lebih besar daripada λ akhir, dalam rentang 190–900 nm (contoh 400 ke 200).');return null}return[a,b]}
function startBase(){const e=pre();if(e){toast(e);return}if(S.sample!=='blank'){setSample('blank');toast('Larutan di kuvet otomatis diganti blanko (HCl 0,1 M).')}const r=range();if(!r)return;S.job={type:'base',l:r[0],stop:r[1],rate:(r[1]-r[0])/1.5}}
function start(){if(S.tab==='conc'){toast('Gunakan tombol Ukur / Ukur semua standar / Ukur sampel.');return}if(S.tab==='scan'){const e=pre();if(e){toast(e);return}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return}const r=range();if(!r)return;S.res={type:'scan',pts:[]};S.lmax=null;S.job={type:'scan',l:r[0],start:r[0],stop:r[1],rate:(r[1]-r[0])/8,last:r[0]+1,pts:S.res.pts};S.xray=1}
 else{const e=pre();if(e){toast(e);return}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return}const l=+$('sl').value,n=Math.max(1,Math.min(10,+$('sn').value|0));if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return}S.lam=l;S.res={type:'simple',rows:[]};S.job={type:'simple',l,n,i:0,t:0};S.xray=1}
 syncX();if(S.job&&!S.camOpt){S.camOpt=1;flyV('opt')}}
function runJob(dt){const j=S.job;if(!j)return;
 if(j.type==='read'){j.t+=dt;if(j.t>=.8){j.t=0;j.vals.push(readA(j.l));if(j.vals.length>=j.n){S.job=null;j.cb(j.vals)}}}else if(j.type==='scan'||j.type==='base'){const next=j.l+j.rate*dt;j.l=j.rate>=0?Math.min(j.stop,next):Math.max(j.stop,next);S.lam=j.l;if(j.type==='scan'&&Math.abs(j.l-j.last)>=1){j.last=j.l;j.pts.push([j.l,readA(j.l)])}
  const reached=j.rate>=0?j.l>=j.stop:j.l<=j.stop;if(reached){if(j.type==='base'){S.base=1;toast('Baseline selesai.')}else toast('Scan selesai.');S.job=null}}
 else{j.t+=dt;if(j.t>=1.2){j.t=0;const a=readA(j.l);S.res.rows.push([++j.i,j.l,a,100*Math.pow(10,-a)]);if(j.i>=j.n){S.job=null;toast('Simple Reads selesai.')}}}}
// ---------- λ maks (puncak spektrum, dihaluskan + interpolasi parabola)
function lmaxOf(p){if(!p||p.length<5)return null;const n=p.length,sm=p.map((q,i)=>{let s=0,c=0;for(let k=-2;k<=2;k++){const j=i+k;if(j>=0&&j<n){s+=p[j][1];c++}}return s/c});
 let k=0;sm.forEach((v,i)=>{if(v>sm[k])k=i});let l=p[k][0],a=sm[k];
 if(k>0&&k<n-1){const y0=sm[k-1],y1=sm[k],y2=sm[k+1],d=y0-2*y1+y2;if(d<0){const off=.5*(y0-y2)/d;if(Math.abs(off)<=1){l=p[k][0]+off*(p[k+1][0]-p[k][0]);a=y1-.25*(y0-y2)*off}}}
 return{l,a}}
function drawChart(){if(S.tab==='conc')return drawCal();const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#fff';g.fillRect(0,0,w,h);g.strokeStyle='#999';g.fillStyle='#333';g.font='11px sans-serif';
 const r=S.res;if(!r||r.type!=='scan'||!r.pts.length){g.fillText(S.tab==='scan'?'Spektrum akan tampil di sini (λ besar ke kecil; Abs vs nm)':'Hasil Simple Reads di tabel',10,20);if(S.tab==='scan')$('scanRes').innerHTML='λmax belum ada. Jalankan Baseline lalu Start.';return}
 const a=+$('s0').value,b=+$('s1').value;const ym=Math.max(1,Math.max(...r.pts.map(p=>p[1]))*1.15);const X=l=>40+(l-a)/(b-a)*(w-50),Y=v=>h-25-v/ym*(h-40);
 g.strokeStyle='#999';g.strokeRect(40,15,w-50,h-40);
 for(let i=0;i<=4;i++){const wl=a+(b-a)*i/4,x=X(wl),abs=ym*i/4,y=Y(abs);g.strokeStyle='#e4e8ed';g.lineWidth=.7;g.beginPath();g.moveTo(x,15);g.lineTo(x,h-25);g.moveTo(40,y);g.lineTo(w-10,y);g.stroke();g.fillStyle='#333';g.textAlign='center';g.fillText(wl.toFixed(0),x,h-8);g.textAlign='left';g.fillText(abs.toFixed(2),4,y+4)}
 g.fillStyle='#333';g.textAlign='right';g.fillText('λ (nm): besar → kecil',w-12,13);g.textAlign='left';g.fillText('Abs',8,h/2);
 g.strokeStyle='#c00';g.lineWidth=1.5;g.beginPath();r.pts.forEach((p,i)=>i?g.lineTo(X(p[0]),Y(p[1])):g.moveTo(X(p[0]),Y(p[1])));g.stroke();g.lineWidth=1;
 const m=lmaxOf(r.pts);if(m){S.lmax=m;g.setLineDash([4,4]);g.strokeStyle='#1565c0';g.beginPath();g.moveTo(X(m.l),15);g.lineTo(X(m.l),h-25);g.stroke();g.setLineDash([]);g.fillStyle='#d32f2f';g.beginPath();g.arc(X(m.l),Y(m.a),4.5,0,7);g.fill();g.fillStyle='#1565c0';g.font='bold 11px sans-serif';g.fillText('λmax '+m.l.toFixed(1)+' nm, A='+m.a.toFixed(3),Math.min(X(m.l)+8,w-170),Y(m.a)-8);
  $('scanRes').innerHTML='<b>λ maks = '+m.l.toFixed(1)+' nm</b>, absorban maks = '+m.a.toFixed(3)+(S.job?' (scan berjalan…)':'')}}
function drawTable(){const r=S.res;if(!r||r.type!=='simple'){$('tbl').innerHTML='';return}let t='<table><tr><th>#</th><th>λ (nm)</th><th>Abs</th><th>%T</th></tr>';r.rows.forEach(x=>t+=`<tr><td>${x[0]}</td><td>${x[1]}</td><td>${x[2].toFixed(4)}</td><td>${x[3].toFixed(2)}</td></tr>`);if(r.rows.length>1){const m=r.rows.reduce((s,x)=>s+x[2],0)/r.rows.length;const sd=Math.sqrt(r.rows.reduce((s,x)=>s+(x[2]-m)**2,0)/(r.rows.length-1));t+=`<tr><td colspan=2>Rata-rata ± SD</td><td colspan=2>${m.toFixed(4)} ± ${sd.toFixed(4)}</td></tr>`}$('tbl').innerHTML=t+'</table>'}
function csv(){if(S.tab==='conc'){const C=S.cal,q=C.std.filter(s=>s.a!=null);if(!q.length){toast('Belum ada data.');return}let t='ppm,Abs\n'+q.map(s=>s.c+','+s.a.toFixed(4)).join('\n');if(C.fit)t+='\n\nslope,'+C.fit.a+'\nintercept,'+C.fit.b+'\nR2,'+C.fit.r2;const o=S.out;if(o.c!=null)t+='\n\nC terukur (ppm),'+o.c+'\nC asli (ppm),'+o.cA;if(o.mgg!=null)t+='\nKadar (mg/g),'+o.mgg;if(o.rec!=null)t+='\n% Recovery,'+o.rec;const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='kalibrasi_thiamin.csv';a.click();return}const r=S.res;if(!r){toast('Belum ada data.');return}let t=r.type==='scan'?'nm,Abs\n'+r.pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(4)).join('\n'):'n,nm,Abs,%T\n'+r.rows.map(x=>x.map(v=>+v.toFixed(4)).join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='cary100_'+r.type+'.csv';a.click()}
// ---------- kalibrasi thiamin, kadar, recovery
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const sdv=a=>{if(a.length<2)return 0;const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1))};
function setSample(s,c){S.sample=s;if(c!=null){S.conc=c;$('conc').value=c;$('cv').textContent=c}$('smp').value=s;$('conc').disabled=s!=='std';setLiq()}
function readOne(sample,c,cb){const e=pre();if(e){toast(e);return false}if(!S.base){toast('Lakukan Baseline (blanko) dulu.');return false}const l=+$('cl').value;if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return false}S.cal.l=l;S.spkC=+$('cAdd').value||0;setSample(sample,c);S.lam=l;S.xray=1;syncX();S.job={type:'read',l,n:3,t:0,vals:[],cb};if(!S.camOpt){S.camOpt=1;flyV('opt')}return true}
function measStd(i,all){const s=S.cal.std[i];if(!s)return;readOne('std',s.c,v=>{s.a=mean(v);s.sd=sdv(v);S.cal.fit=null;if(all&&i+1<S.cal.std.length){renderStd();setTimeout(()=>measStd(i+1,true),300)}else calc(true)})}
function calc(quiet){const C=S.cal,p=C.std.filter(s=>s.a!=null&&isFinite(s.c));
 if(p.length<3){C.fit=null;if(!quiet)toast('Minimal 3 standar terisi (absorban terukur atau diketik).');renderStd();renderRes();return}
 const n=p.length,sx=p.reduce((s,q)=>s+q.c,0),sy=p.reduce((s,q)=>s+q.a,0),sxx=p.reduce((s,q)=>s+q.c*q.c,0),sxy=p.reduce((s,q)=>s+q.c*q.a,0);const den=n*sxx-sx*sx;
 if(Math.abs(den)<1e-12){C.fit=null;if(!quiet)toast('Konsentrasi standar harus berbeda-beda.');renderStd();renderRes();return}
 const a=(n*sxy-sx*sy)/den,b=(sy-a*sx)/n,ym=sy/n;const sst=p.reduce((s,q)=>s+(q.a-ym)**2,0),ssr=p.reduce((s,q)=>s+(q.a-(a*q.c+b))**2,0);const syx=n>2?Math.sqrt(ssr/(n-2)):0;
 C.fit={a,b,r2:sst>0?1-ssr/sst:NaN,n,syx,lod:3.3*syx/a,loq:10*syx/a};renderStd();renderRes()}
function measUnk(){if(!S.cal.fit){toast('Hitung kurva kalibrasi dulu.');return}readOne('unk',null,v=>{$('aU').value=mean(v).toFixed(4);renderRes()})}
function measSpk(){if(!S.cal.fit){toast('Hitung kurva kalibrasi dulu.');return}if(!(+$('cAdd').value>0)){toast('Isi konsentrasi spike yang ditambahkan.');return}readOne('spk',null,v=>{$('aSp').value=mean(v).toFixed(4);renderRes()})}
function renderStd(){const C=S.cal;let t='<table><tr><th>No</th><th>Konsentrasi (ppm)</th><th>Absorban (ukur / ketik)</th><th></th></tr>';
 C.std.forEach((s,i)=>t+=`<tr><td>${i+1}</td><td><input data-i="${i}" data-k="c" type="number" step="0.5" min="0" value="${s.c}"></td><td><input data-i="${i}" data-k="a" type="number" step="0.001" min="0" placeholder="–" value="${s.a==null?'':s.a.toFixed(4)}" title="${s.sd?'SD n=3: '+s.sd.toFixed(4):''}"></td><td style="text-align:center"><button data-m="${i}">Ukur</button> <button data-d="${i}" title="Hapus baris">✕</button></td></tr>`);
 $('stdtab').innerHTML=t+'</table>';
 $('stdtab').querySelectorAll('input').forEach(e=>e.onchange=()=>{const s=C.std[+e.dataset.i];if(e.dataset.k==='c'){s.c=+e.value;s.a=null;s.sd=null}else{const v=parseFloat(e.value);s.a=isFinite(v)?v:null;s.sd=null}C.fit=null;calc(true)});
 $('stdtab').querySelectorAll('button[data-m]').forEach(b=>b.onclick=()=>measStd(+b.dataset.m,false));
 $('stdtab').querySelectorAll('button[data-d]').forEach(b=>b.onclick=()=>{C.std.splice(+b.dataset.d,1);C.fit=null;calc(true)})}
function renderRes(){const C=S.cal,f=C.fit;let r='';C.unk=null;C.spk=null;S.out={};
 if(f)r+=`<b>Persamaan:</b> y = ${f.a.toFixed(5)}x ${f.b<0?'−':'+'} ${Math.abs(f.b).toFixed(5)}<br><b>R²</b> = ${f.r2.toFixed(5)} ${f.r2>=.995?'✔ baik':'⚠ di bawah 0,995, periksa standar'}<br>LOD ≈ ${f.lod.toFixed(3)} ppm, LOQ ≈ ${f.loq.toFixed(3)} ppm (3,3·s/a dan 10·s/a)`;
 else r+='Kalibrasi belum ada: isi atau ukur minimal 3 standar, lalu <b>Hitung kurva</b>.';
 const A=parseFloat($('aU').value);
 if(f&&isFinite(A)){const df=Math.max(1,+$('df').value||1),V=+$('vol').value,m=+$('massa').value,tw=+$('tabw').value;
  const c=(A-f.b)/f.a,cA=c*df;C.unk={A,c,df};S.out.c=c;S.out.cA=cA;
  const aa=C.std.filter(s=>s.a!=null).map(s=>s.a),rng=A>=Math.min(...aa)*.999&&A<=Math.max(...aa)*1.001;
  r+=`<hr><b>Sampel:</b> Abs = ${A.toFixed(4)} (%T = ${(100*Math.pow(10,-A)).toFixed(2)})<br>C terukur = ${c.toFixed(3)} ppm → C larutan asli = <b>${cA.toFixed(3)} ppm</b> (FP ${df})<br>`;
  if(V>0&&m>0){const mgg=cA*(V/1000)/m;S.out.mgg=mgg;r+=`<b>Kadar = ${mgg.toFixed(4)} mg/g</b> = ${(mgg*100).toFixed(2)} mg/100 g = ${(mgg*1000).toFixed(1)} mg/kg<br>`;if(tw>0)r+=`≈ ${(mgg*tw).toFixed(3)} mg/tablet (bobot rata-rata ${tw} g)<br>`;r+=`<small>Kadar = C × FP × V ÷ massa</small><br>`}
  else r+='<span style="color:#b00">Isi massa sampel dan volume labu untuk menghitung kadar.</span><br>';
  r+=rng?'✔ Abs sampel di dalam rentang kurva':'⚠ Abs sampel di luar rentang kurva: encerkan atau ulangi';
  const Asp=parseFloat($('aSp').value),add=+$('cAdd').value;
  if(isFinite(Asp)&&add>0){const cs=(Asp-f.b)/f.a,rec=(cs-c)/add*100;C.spk={A:Asp,c:cs};S.out.rec=rec;const ok=rec>=80&&rec<=120;
   r+=`<hr><b>Recovery:</b> C sampel+spike = ${cs.toFixed(3)} ppm, C sampel = ${c.toFixed(3)} ppm, spike ditambahkan = ${add} ppm<br><b>% Recovery = ${rec.toFixed(2)} %</b> ${ok?'<span style="color:#1b7a2b">✔ dalam rentang 80–120%</span>':'<span style="color:#b00">⚠ di luar 80–120%</span>'}<br><small>%R = (C sampel+spike − C sampel) ÷ C spike × 100</small>`}
  else r+='<hr>Recovery: isi absorban sampel + spike dan konsentrasi spike (atau klik Ukur sampel + spike).';
 }else if(f)r+='<hr>Isi absorban sampel (atau klik Ukur sampel) untuk menghitung kadar.';
 $('cres').innerHTML=r;drawCal()}
function renderConc(){renderStd();renderRes()}
function drawCal(){const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#fff';g.fillRect(0,0,w,h);const C=S.cal,p=C.std.filter(s=>s.a!=null);
 const xm=Math.max(12,...C.std.map(s=>s.c),C.unk?C.unk.c:0,C.spk?C.spk.c:0)*1.1,ym=Math.max(.5,...p.map(s=>s.a),C.unk?C.unk.A:0,C.spk?C.spk.A:0)*1.2;const X=v=>55+v/xm*(w-70),Y=v=>h-34-v/ym*(h-56);
 g.font='11px sans-serif';g.lineWidth=1;for(let i=0;i<=5;i++){const xv=xm*i/5,yv=ym*i/5;g.strokeStyle='#e6e6e6';g.beginPath();g.moveTo(X(xv),20);g.lineTo(X(xv),h-34);g.moveTo(55,Y(yv));g.lineTo(w-15,Y(yv));g.stroke();g.fillStyle='#333';g.fillText(xv.toFixed(1),X(xv)-8,h-20);g.fillText(yv.toFixed(2),16,Y(yv)+4)}
 g.strokeStyle='#888';g.strokeRect(55,20,w-70,h-54);g.fillStyle='#333';g.fillText('Konsentrasi thiamin (ppm)',w/2-60,h-5);g.save();g.translate(11,h/2+30);g.rotate(-Math.PI/2);g.fillText('Absorbansi',0,0);g.restore();g.fillText('Kurva kalibrasi thiamin @ '+C.l+' nm',60,14);
 const f=C.fit;if(f){g.strokeStyle='#1565c0';g.lineWidth=2;g.beginPath();g.moveTo(X(0),Y(f.b));g.lineTo(X(xm),Y(f.a*xm+f.b));g.stroke();g.lineWidth=1;g.fillStyle='#1565c0';g.fillText('y = '+f.a.toFixed(4)+'x '+(f.b<0?'−':'+')+' '+Math.abs(f.b).toFixed(4),65,36);g.fillText('R² = '+f.r2.toFixed(4),65,50)}
 p.forEach(s=>{g.fillStyle='#d32f2f';g.beginPath();g.arc(X(s.c),Y(s.a),4.5,0,7);g.fill()});
 function mark(u,col,lab,dy){g.setLineDash([5,4]);g.strokeStyle=col;g.beginPath();g.moveTo(55,Y(u.A));g.lineTo(X(u.c),Y(u.A));g.lineTo(X(u.c),h-34);g.stroke();g.setLineDash([]);g.fillStyle=col;g.beginPath();g.arc(X(u.c),Y(u.A),5.5,0,7);g.fill();g.font='bold 11px sans-serif';g.fillText(lab+' '+u.c.toFixed(2)+' ppm',Math.min(X(u.c)+8,w-150),Y(u.A)+dy)}
 if(f&&C.unk)mark({A:C.unk.A,c:C.unk.c},'#2e7d32','Sampel',-8);
 if(f&&C.spk)mark(C.spk,'#ef6c00','+Spike',-8);
 if(!p.length){g.fillStyle='#666';g.fillText('Ukur atau ketik absorban standar untuk membuat kurva.',75,h/2)}}
// ---------- skema jalur cahaya (tampak atas)
function drawSch(){const c=$('schc'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#0c121b';g.fillRect(0,0,w,h);
 const X=x=>16+(x+2.9)/5.5*(w-32),Y=z=>14+(z+2.0)/3.4*(h-28);const rgb='rgb('+(col.r*255|0)+','+(col.g*255|0)+','+(col.b*255|0)+')';const v=B.vis,T=B.T,so=B.sOn;
 g.strokeStyle='#3a4d68';g.setLineDash([4,3]);g.strokeRect(X(-.9),Y(-.4),X(.9)-X(-.9),Y(1.4)-Y(-.4));g.setLineDash([]);g.fillStyle='#6f84a3';g.font='9px sans-serif';g.fillText('kompartemen sampel',X(-.85),Y(1.4)+10);
 const line=(p,i,a)=>{g.globalAlpha=Math.max(0,Math.min(1,a))*v;g.strokeStyle=rgb;g.lineWidth=3;g.beginPath();g.moveTo(X(p[i][0]),Y(p[i][1]));g.lineTo(X(p[i+1][0]),Y(p[i+1][1]));g.stroke()};
 const lv0=S.inst&&S.warm>2&&S.lam>=350;line([[-2.6,-1.7],[-2.2,-1.7]],0,lv0?1:0);line([[-2.2,-1.2],[-2.2,-1.7]],0,lv0?0:1);for(let i=0;i<common.length-1;i++)line(common,i,1);for(let i=0;i<sampP.length-1;i++)line(sampP,i,(i<3?1:.1+.9*T)*(so?1:.35));for(let i=0;i<refP.length-1;i++)line(refP,i,so?.35:1);g.globalAlpha=1;
 [[.95,1],[.05,0]].forEach(a=>{g.fillStyle=a[1]&&!S.cuv?'rgba(150,200,255,.12)':'rgba(150,200,255,.55)';g.fillRect(X(-.15),Y(a[0]-.15),X(.15)-X(-.15),Y(a[0]+.15)-Y(a[0]-.15))});
 g.strokeStyle='#e8eef5';g.lineWidth=3;MIRS.forEach(m=>{const dx=Math.cos(m[2])*.2,dz=-Math.sin(m[2])*.2;g.beginPath();g.moveTo(X(m[0]-dx),Y(m[1]-dz));g.lineTo(X(m[0]+dx),Y(m[1]+dz));g.stroke()});
 g.fillStyle='#b08d2a';g.fillRect(X(-1.9)-3,Y(-.6)-8,6,16);g.fillStyle='#777';g.beginPath();g.arc(X(-1.1),Y(.5),9,0,7);g.fill();g.fillStyle='#889';g.beginPath();g.arc(X(2.3),Y(.5),8,0,7);g.fill();
 const lv=S.inst&&S.warm>2&&S.lam>=350,ld=S.inst&&S.warm>2&&S.lam<350,mn=S.lampMode==='manual',c1=mn?S.lampColor:AUTO_V,c2=mn?S.lampColor:AUTO_D;
 g.shadowColor=c1;g.shadowBlur=lv?18:0;g.fillStyle=lv?c1:'#555';g.beginPath();g.arc(X(-2.6),Y(-1.7),9,0,7);g.fill();
 g.shadowColor=c2;g.shadowBlur=ld?18:0;g.fillStyle=ld?c2:'#555';g.beginPath();g.arc(X(-2.2),Y(-1.2),8,0,7);g.fill();g.shadowBlur=0;
 if(v){g.fillStyle='#fff';pulses.forEach(p=>{g.beginPath();g.arc(X(p.s.position.x),Y(p.s.position.z),2.4,0,7);g.fill()})}
 g.font='bold 10px sans-serif';[[1,-2.6,-1.7],[2,-1.9,-1.7],[3,-1.9,-1.2],[4,-1.9,-.6],[5,-1.1,-1.1],[6,-1.1,.5],[7,0,.95],[8,2.3,.5]].forEach(a=>{const x=X(a[1])-10,y=Y(a[2])-10;g.fillStyle='#2d7dd2';g.beginPath();g.arc(x,y,7,0,7);g.fill();g.fillStyle='#fff';g.fillText(a[0],x-3,y+3.5)});
 g.fillStyle='#e8edf3';g.font='10px sans-serif';g.fillText('I0=100',X(.25),Y(.05)+3);if(S.inst)g.fillText('I='+(100*T).toFixed(1),X(.25),Y(.95)+3)}
// ---------- label komponen 3D
const LB=[['Lampu tungsten',-2.6,-1.7,'lampV'],['Lampu deuterium',-2.2,-1.0,'lampD'],['Cermin M1',-1.9,-1.7,'mirror'],['Celah',-1.9,-1.2,'slit'],['Kisi difraksi',-1.9,-.6,'grat'],['Cermin M2',-1.1,-1.1,'mirror'],['Chopper',-1.1,.5,'chop'],['Kuvet sampel',0,.95,'hold_s'],['Kuvet referensi',0,.05,'hold_r'],['Detektor PMT',2.3,.5,'pmt']].map(a=>{const e=document.createElement('div');e.className='lb';e.textContent=a[0];e.title='Klik untuk membaca penjelasan';e.addEventListener('click',ev=>{ev.stopPropagation();showInfo(a[3])});document.body.appendChild(e);return{e,v:new THREE.Vector3(a[1]-3.2,BY+.35,a[2])}});
function updLb(){const rect=ren.domElement.getBoundingClientRect(),w=rect.width,hh=rect.height;LB.forEach(l=>{const q=l.v.clone().project(cam);const on=S.lbl&&q.z<1&&q.x>=-1&&q.x<=1&&q.y>=-1&&q.y<=1;l.e.style.display=on?'block':'none';if(on){l.e.style.left=(rect.left+(q.x+1)/2*w+8)+'px';l.e.style.top=(rect.top+(1-q.y)/2*hh-10)+'px'}})}
// ---------- UI
const CHK=[['UPS menyala',()=>S.ups],['Instrumen menyala',()=>S.inst],['Komputer menyala',()=>S.pc],['Monitor menyala',()=>S.mon],['Warm-up selesai',()=>S.inst&&S.warm>=WARM],['Cary WinUV dibuka',()=>S.app],['Baseline blanko',()=>S.base],['Kuvet terpasang',()=>S.cuv],['Tutup tertutup',()=>!S.lid]];
function renderUI(){document.querySelectorAll('#p-conc button').forEach(b=>b.disabled=!!S.job);$('prog').firstElementChild.style.width=(CHK.filter(c=>c[1]()).length/CHK.length*100)+'%';$('chk').innerHTML=CHK.map(c=>`<li class="${c[1]()?'ok':''}">${c[0]}${c[0]==='Warm-up selesai'&&S.inst&&S.warm<WARM?' '+Math.round(S.warm/WARM*100)+'%':''}</li>`).join('');
 $('bLid').textContent=S.lid?'Tutup tutup':'Buka tutup';$('bCuv').textContent=S.cuv?'Ambil kuvet':'Pasang kuvet';$('bX').classList.toggle('on',!!S.xray);$('bB').classList.toggle('on',!!S.beam);
 const st=!S.inst?'Instrument: Not connected':S.warm<WARM?'Instrument: Warming up '+Math.round(S.warm/WARM*100)+'%':'Instrument: Connected – Ready';$('status').textContent=st+(S.job?' | Mengukur…':'');
 $('aStart').disabled=!!S.job;$('aBase').disabled=!!S.job;$('aStop').disabled=!S.job;
 const T=S.cuv?Math.pow(10,-specA(S.lam)):1,A=-Math.log10(T);
 const lon=S.inst&&S.warm>2,lampTxt=lon?(S.lam>=350?'Tungsten (Visible)':'Deuterium (UV)'):'padam';
 $('lmInfo').textContent=lon?'Aktif: '+(S.lam>=350?'lampu tungsten untuk wilayah tampak (visible)':'lampu deuterium untuk wilayah ultraviolet (UV)')+'. Peralihan sumber pada simulasi sekitar 350 nm; cocokkan dengan manual alat.':'Lampu padam. Nyalakan instrumen dan tunggu warm-up.';
 const sw=$('lmSw'),cc=lon?(S.lampMode==='manual'?S.lampColor:(S.lam>=350?AUTO_V:AUTO_D)):'#2a3340';sw.style.background=cc;sw.style.boxShadow=lon?`0 0 ${10+14*S.lampI}px ${cc}`:'none';sw.textContent=lon?(S.lam>=350?'Lampu tungsten menyala':'Lampu deuterium menyala'):'Lampu padam';
 const cell=(l,v,c)=>`<div class="cell ${c||''}"><small>${l}</small><b>${v}</b></div>`;
 $('hud').innerHTML=S.inst?cell('λ (nm)',S.lam.toFixed(1))+cell('I0 ref','100.0')+cell('I sampel',(100*T).toFixed(1))+cell('%T',(100*T).toFixed(2))+cell('Abs',(A+(S.job?noise():0)).toFixed(4),'hi')+cell('Sumber',lampTxt)+(S.lid?'<div class="warn">⚠ tutup terbuka</div>':'')+(!S.cuv?'<div class="warn">⚠ kuvet kosong</div>':''):cell('Instrumen','OFF');
}
function syncX(){shells.forEach(s=>{s.m.raycast=(S.xray&&!s.keep)?()=>{}:THREE.Mesh.prototype.raycast})}
$('smp').onchange=e=>{S.sample=e.target.value;S.spkC=+$('cAdd').value||0;$('conc').disabled=S.sample!=='std';setLiq()};$('conc').oninput=e=>{S.conc=+e.target.value;$('cv').textContent=S.conc;setLiq()};
$('bLid').onclick=toggleLid;$('bCuv').onclick=toggleCuv;$('bX').onclick=()=>{S.xray=S.xray?0:1;syncX()};$('bB').onclick=()=>S.beam=S.beam?0:1;
$('bR').onclick=e=>{ctl.autoRotate=!ctl.autoRotate;e.target.classList.toggle('on',ctl.autoRotate)};$('bA').onclick=()=>openApp(true);$('xapp').onclick=()=>openApp(false);
$('bFS').onclick=()=>{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen().catch(()=>toast('Layar penuh diblokir browser.'))};$('bRe').onclick=()=>location.reload();
$('aBase').onclick=startBase;$('aStart').onclick=start;$('aStop').onclick=()=>{S.job=null};$('aCsv').onclick=csv;$('cAll').onclick=()=>measStd(0,true);$('cFit').onclick=()=>calc(false);$('cUnk').onclick=measUnk;$('cSpk').onclick=measSpk;
$('cClr').onclick=()=>{S.cal.std.forEach(s=>{s.a=null;s.sd=null});S.cal.fit=null;$('aU').value='';$('aSp').value='';renderConc()};
$('cAddStd').onclick=()=>{const C=S.cal,last=C.std.length?C.std[C.std.length-1].c:0;C.std.push({c:last+5,a:null,sd:null});C.fit=null;calc(true)};
const useL=()=>{if(S.lmax){const v=Math.round(S.lmax.l*10)/10;$('cl').value=v;$('sl').value=v;S.cal.l=v;toast('λ analisis = '+v+' nm (dari λmax scan).');drawCal()}else toast('Lakukan Scan dulu untuk mendapatkan λmax.')};
$('bUseL').onclick=useL;$('cUseL').onclick=useL;$('cl').onchange=()=>{S.cal.l=+$('cl').value;drawCal()};
['massa','vol','df','tabw','aU','aSp','cAdd'].forEach(id=>$(id).oninput=()=>{S.spkC=+$('cAdd').value||0;renderRes()});
$('bL').onclick=()=>{S.lbl=S.lbl?0:1;$('bL').classList.toggle('on',!!S.lbl)};
function updatePanelToggleUI(){
 const allHidden=document.body.classList.contains('hp');
 const leftHidden=allHidden||document.body.classList.contains('left-hidden');
 const rightHidden=allHidden||document.body.classList.contains('right-hidden');
 const bl=$('toggleLeft'),br=$('toggleRight');
 bl.textContent=leftHidden?'›':'‹';
 bl.title=leftHidden?'Tampilkan panel kiri':'Sembunyikan panel kiri';
 bl.setAttribute('aria-label',bl.title);
 br.textContent=rightHidden?'‹':'›';
 br.title=rightHidden?'Tampilkan panel kanan':'Sembunyikan panel kanan';
 br.setAttribute('aria-label',br.title);
 $('bP').title=allHidden?'Tampilkan semua panel':'Sembunyikan semua panel';
}
$('toggleLeft').onclick=()=>{
 if(document.body.classList.contains('hp')){
  document.body.classList.remove('hp','left-hidden');
  document.body.classList.add('right-hidden');
 }else{
  document.body.classList.toggle('left-hidden');
 }
 updatePanelToggleUI();
};
$('toggleRight').onclick=()=>{
 if(document.body.classList.contains('hp')){
  document.body.classList.remove('hp','right-hidden');
  document.body.classList.add('left-hidden');
 }else{
  document.body.classList.toggle('right-hidden');
 }
 updatePanelToggleUI();
};
$('bP').onclick=()=>{
 if(document.body.classList.contains('hp')){
  document.body.classList.remove('hp','left-hidden','right-hidden');
 }else{
  document.body.classList.add('hp');
 }
 updatePanelToggleUI();
};
$('lmMode').onchange=e=>{S.lampMode=e.target.value};$('lmColor').oninput=e=>{S.lampColor=e.target.value;S.lampMode='manual';$('lmMode').value='manual'};$('lmI').oninput=e=>{S.lampI=+e.target.value};document.querySelectorAll('[data-lc]').forEach(b=>b.onclick=()=>{S.lampColor=b.dataset.lc;$('lmColor').value=b.dataset.lc;S.lampMode='manual';$('lmMode').value='manual'});
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{if(S.job)return;S.tab=b.dataset.t;document.querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('on',x===b));$('p-scan').hidden=S.tab!=='scan';$('p-simple').hidden=S.tab!=='simple';$('p-conc').hidden=S.tab!=='conc';$('scanBox').hidden=S.tab!=='scan';$('cres').hidden=S.tab!=='conc';if(S.tab==='conc')renderConc();S.res=null;drawTable()});
const V={front:[[-1,5.5,12],[1,.8,0]],top:[[1,16,.1],[1,0,0]],back:[[1,5,-12],[1,.8,0]],side:[[14,4,3],[0,.8,0]],inst:[[-3.2,4.5,6.5],[-3.2,.7,.5]],cuv:[[-3.2,2.6,3.6],[-3.2,.8,.9]],mon:[[5,2.2,4.5],[5,1.2,-.6]],opt:[[-3.2,7.2,2.6],[-3.2,.8,-.1]],lamp:[[-6.8,2.2,.9],[-5.6,.8,-1.5]]};
let fly=null;function flyV(k){const v=V[k];fly={t:0,p0:cam.position.clone(),t0:ctl.target.clone(),p1:new THREE.Vector3(...v[0]),t1:new THREE.Vector3(...v[1])}}document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>flyV(b.dataset.v));
// klik 3D
const rc=new THREE.Raycaster(),mp=new THREE.Vector2();let dn=null;
function pick(e){const r=ren.domElement.getBoundingClientRect();mp.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);rc.setFromCamera(mp,cam);const h=rc.intersectObjects(clickables,false);return h.length?h[0].object.userData.key:null}
ren.domElement.addEventListener('pointerdown',e=>dn=[e.clientX,e.clientY]);
ren.domElement.addEventListener('pointerup',e=>{if(!dn||Math.hypot(e.clientX-dn[0],e.clientY-dn[1])>5)return;const k=pick(e);if(!k)return;showInfo(k);
 if(k==='upsbtn')power('ups');else if(k==='sw')power('inst');else if(k==='pcbtn')power('pc');else if(k==='monbtn')power('mon');else if(k==='lid')toggleLid();else if(k==='cuv')toggleCuv();else if(k==='screen'&&desk())openApp(true)});
ren.domElement.addEventListener('pointermove',e=>{ren.domElement.style.cursor=pick(e)?'pointer':'default'});
function resize(){const rect=ren.domElement.getBoundingClientRect(),w=Math.max(1,rect.width),h=Math.max(1,rect.height);ren.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}addEventListener('resize',resize);resize();
// ---------- loop
const B={vis:0,T:1,sOn:true};const clk=new THREE.Clock();let xk=0,uiT=0,chA=0,lastLamp=0;const col=new THREE.Color(),tA=new THREE.Color(),tB=new THREE.Color();
setLiq();syncX();$('conc').disabled=true;$('cres').hidden=true;if(innerWidth<820)document.body.classList.add('hp');updatePanelToggleUI();
function loop(){requestAnimationFrame(loop);const dt=Math.min(clk.getDelta(),.1);
 if(S.inst)S.warm=Math.min(WARM,S.warm+dt);if(S.pc&&!S.booted){S.bootT+=dt;if(S.bootT>4)S.booted=1}
 runJob(dt);
 if(fly){fly.t=Math.min(1,fly.t+dt/.9);const k=fly.t*fly.t*(3-2*fly.t);cam.position.lerpVectors(fly.p0,fly.p1,k);ctl.target.lerpVectors(fly.t0,fly.t1,k);if(fly.t>=1)fly=null}
 ctl.update();
 // animasi objek
 const lt=S.lid?-1.6:0;lid.rotation.x+=(lt-lid.rotation.x)*Math.min(1,dt*5);
 cuvK+=((S.cuv?1:0)-cuvK)*Math.min(1,dt*5);cuvS.position.set(1.6*(1-cuvK),.18+(.8-.18)*cuvK+Math.sin(Math.PI*cuvK)*.5,3+(.95-3)*cuvK);
 rocker.rotation.x=S.inst?-.3:.3;ledM.emissive.setHex(S.inst?0x00ff00:0);ledM.color.setHex(S.inst?0x22ff22:0x114411);
 upsLed.forEach((l,i)=>{const on=S.ups;l.material.emissive.setHex(on?0x00ff00:0);l.material.color.setHex(on?0x22ff22:0x114411)});
 pcLed.material.emissive.setHex(S.pc?0x00ff00:0);monLed.material.emissive.setHex(S.mon?0x00ff00:0);
 xk+=((S.xray?1:0)-xk)*Math.min(1,dt*4);shW.opacity=shD.opacity=1-.88*xk;shW.depthWrite=shD.depthWrite=xk<.05;shells.forEach(s=>{s.e.visible=xk>.02;s.e.material.opacity=xk*.9});
 // lampu & berkas (warna lampu solid dan jelas)
 const lampOn=S.inst&&S.warm>2;if(lampOn&&!S.autoX){S.autoX=1;S.xray=1;syncX();toast("Mode transparan aktif otomatis agar berkas terlihat (tombol Transparan untuk mematikan).")}
 const LA=lampOn?(S.lam>=350?'v':'d'):null,mn=S.lampMode==='manual',cV=mn?tA.set(S.lampColor):tA.set(AUTO_V),cD=mn?tB.set(S.lampColor):tB.set(AUTO_D),fl=1+.04*Math.sin(performance.now()*.05);
 lampVM.color.copy(LA==='v'?cV:new THREE.Color(0x442200));lampVM.emissive.copy(cV).multiplyScalar(LA==='v'?3*S.lampI*fl:0);
 bulbVM.color.copy(LA==='v'?cV:cOff);bulbVM.opacity=LA==='v'?.92:.3;bulbVM.emissive.copy(cV).multiplyScalar(LA==='v'?1.5*S.lampI:0);
 lampD.material.color.copy(LA==='d'?cD:cOff);lampD.material.opacity=LA==='d'?.95:.4;lampD.material.emissive.copy(cD).multiplyScalar(LA==='d'?1.8*S.lampI*fl:0);
 d2Win.material.color.copy(LA==='d'?cD:cOff);d2Win.material.emissive.copy(cD).multiplyScalar(LA==='d'?3*S.lampI:0);
 lightV.color.copy(cV);lightV.intensity=LA==='v'?(.6+1.6*xk)*S.lampI:0;lightD.color.copy(cD);lightD.intensity=LA==='d'?(.6+1.6*xk)*S.lampI:0;
 sel.position.y+=((LA==='d'?BY:BY+.38)-sel.position.y)*Math.min(1,dt*6);
 chop.rotation.y+=(S.inst?(S.job?6:3):0)*dt;grat.rotation.y=(S.lam-190)/710*.8;
 if(S.lampMode==='manual')col.set(S.lampColor);else col.setRGB(...W(S.lam));[mC,mS1,mS2,mR,pM,mLV,mLD].forEach(m=>m.color.copy(col));
 mLV.color.copy(cV);mLD.color.copy(cD);
 const T=S.cuv&&!S.lid?Math.pow(10,-specA(S.lam)):1;const vis=S.beam&&lampOn?1:0;const sOn=Math.sin(chop.rotation.y*2)>0;B.vis=vis;B.T=T;B.sOn=sOn;
 mC.opacity=.9*vis;mLV.opacity=.9*(S.beam&&LA==='v'?1:0);mLD.opacity=.9*(S.beam&&LA==='d'?1:0);mS1.opacity=.9*vis*(sOn?1:.3);mR.opacity=.9*vis*(sOn?.3:1);mS2.opacity=.9*vis*(sOn?1:.3)*(.1+.9*T);
 pmtM.emissive.setRGB(col.r*.5*T*vis,col.g*.5*T*vis,col.b*.5*T*vis);halos.forEach(q=>{const lh=q.t==='lv'||q.t==='ld';q.m.color.copy(q.t==='lv'?cV:q.t==='ld'?cD:col);const f=lh?((q.t==='lv'?LA==='v':LA==='d')?(1+.05*Math.sin(performance.now()*.05))*Math.min(1.1,.55+.45*S.lampI):0):q.t==='c'?1:q.t==='s1'?(sOn?1:.3):q.t==='s2'?(sOn?1:.3)*(.1+.9*T):q.t==='r'?(sOn?.3:1):.3+.7*T;q.m.opacity=Math.min(1,(lh?.95:.8)*(lh?1:vis)*f)});
 const v=S.job?3.2:1.4;pulses.forEach(p=>{p.s.visible=!!vis;if(!vis)return;p.u+=v*dt;const q=posAt(p.r,p.u);p.s.position.set(q[0],BY,q[1]);const u=p.u%p.r.L;const sc=(p.k===0&&u>dCuv)?.2+.8*T:1;p.s.scale.setScalar(sc)});
 // UI
 drawScreen();updLb();drawSch();uiT+=dt;if(uiT>.15){uiT=0;renderUI();if(S.app){if(S.tab==='scan'||S.tab==='conc'||S.job)drawChart();if(S.res&&S.res.type==='simple')drawTable()}}
 ren.render(scene,cam)}
renderConc();
loop();
}
</script></body></html>

"""

components.html(HTML, height=height, scrolling=False)
