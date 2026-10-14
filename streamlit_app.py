"""Digital Twin Spektrofotometer UV-Vis (Agilent Cary 100) - Analisis Thiamin
SATU FILE SAJA: seluruh model 3D (Three.js) sudah tertanam di dalam file ini.
Jalankan: streamlit run app.py
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Digital Twin Cary 100 UV-Vis · Hasil Dinamis", page_icon="🔬", layout="wide")

with st.sidebar:
    st.header("Pengaturan tampilan")
    height = st.slider("Tinggi tampilan (px)", 600, 1400, 1000, 50)

HTML = r"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digital Twin Cary 100 UV-Vis</title>
<style>
:root{--bg:#10161f;--card:#16202eeb;--line:#2b3d55;--tx:#e6edf5;--mut:#8fa3bd;--ac:#35c2b0;--ac2:#4b8df8;--warn:#ff7b6b}
*{box-sizing:border-box}body{margin:0;font:13px/1.35 "Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--tx);overflow:hidden}
/* Area alat dipisahkan dari panel info agar keterangan tidak menutupi model 3D. */
#c{position:fixed;inset:0 320px 0 0;width:calc(100% - 320px);height:100%;display:block}
button,select,input{font:inherit}
button{background:#22324a;color:var(--tx);border:1px solid var(--line);border-radius:7px;padding:5px 10px;cursor:pointer;transition:background .15s}
button:hover{background:#2e4466}button.on{background:var(--ac2);border-color:#8db6ff;color:#fff}button.pri{background:var(--ac);border-color:#8de8db;color:#04211d;font-weight:600}button:disabled{opacity:.45;cursor:not-allowed}
.bar{position:fixed;top:8px;left:8px;right:328px;display:flex;flex-wrap:wrap;gap:8px;z-index:12;pointer-events:none}
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
#hud{display:none!important}
.cell{min-width:72px;background:#0b121b;border:1px solid var(--line);border-radius:8px;padding:3px 8px;text-align:center}.cell small{display:block;color:var(--mut);font-size:10px}
.cell b{font:600 16px ui-monospace,Consolas,monospace}.cell.hi b{color:var(--ac)}.warn{align-self:center;color:var(--warn);font-size:12px;padding:0 6px;white-space:nowrap}
.lb{position:fixed;pointer-events:auto;cursor:pointer;user-select:none;font-size:10px;background:#000b;color:#fff;padding:2px 5px;border:1px solid #61748b;border-radius:4px;z-index:3;white-space:nowrap;transition:background .15s,border-color .15s}.lb:hover{background:#17665f;border-color:#7be3d5}
#toast{position:fixed;top:56px;left:50%;transform:translateX(-50%);background:#b3321f;color:#fff;padding:7px 14px;border-radius:6px;z-index:9;opacity:0;transition:opacity .3s;pointer-events:none;max-width:90%}
/* HUD alur optik: ringkas, tajam, dan tidak menutupi komponen saat Kenali Bagian aktif. */
#opticalStatus{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:6;width:min(540px,88vw);padding:10px 13px 9px;border:1px solid #42637f;border-radius:13px;background:linear-gradient(135deg,rgba(7,17,29,.94),rgba(18,39,58,.9));box-shadow:0 8px 28px #0008;backdrop-filter:blur(10px);color:#eaf5ff;pointer-events:none;transition:opacity .2s,transform .2s}
#opticalStatus[hidden]{display:none!important}
.optic-hud-head{display:flex;align-items:center;gap:7px;font-size:9px;letter-spacing:.13em;font-weight:800;color:#87e5d7;text-transform:uppercase}
.optic-live-dot{width:7px;height:7px;border-radius:50%;background:#43e0b7;box-shadow:0 0 10px #43e0b7;animation:opticPulse 1.6s infinite}
@keyframes opticPulse{0%,100%{opacity:.55;transform:scale(.8)}50%{opacity:1;transform:scale(1.25)}}
#opticalStep{font-size:13px;font-weight:700;line-height:1.35;margin-top:5px;color:#fff}
#opticalDetail{font-size:10px;line-height:1.4;margin-top:3px;color:#b4c8dc}
.optic-stages{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin-top:9px}
.optic-stage{min-width:0;display:flex;align-items:center;gap:5px;padding:5px 6px;border:1px solid #344b61;border-radius:7px;background:#101d2a;color:#7990a8;font-size:9px;white-space:nowrap;overflow:hidden}
.optic-stage i{width:6px;height:6px;display:block;flex:none;border-radius:50%;background:#566b80}
.optic-stage.active{color:#f3ffff;border-color:#35c2b0;background:#123b3b;box-shadow:inset 0 0 10px #35c2b022}
.optic-stage.active i{background:#55e4d0;box-shadow:0 0 8px #55e4d0}
.optic-stage.done{color:#a5c9d4;border-color:#315c69}
.optic-stage.done i{background:#35c2b0}
.wt-actions{display:flex;align-items:center;gap:5px}
.wt-actions #minApp{background:#edf2f8;color:#173354;border:1px solid #fff;font-weight:800;font-size:16px;line-height:1;padding:1px 8px}
.wt-actions #xapp{background:#c33;border-color:#fff;color:#fff;padding:0 7px}
#app{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:min(1160px,98vw);max-height:94vh;overflow:auto;background:#ece9d8;color:#111;border:2px solid #0a246a;border-radius:6px;z-index:8;box-shadow:0 10px 40px #000a}
#app[hidden]{display:none}.wt{background:linear-gradient(#2a62d0,#0a3fa8);color:#fff;padding:5px 8px;display:flex;justify-content:space-between;align-items:center}
.wt button{padding:0 7px;background:#c33;border-color:#fff;color:#fff}
#app .bd{padding:10px}
.app-main-grid{display:grid;grid-template-columns:minmax(300px,.88fr) minmax(430px,1.12fr);gap:12px;align-items:start}
.graph-column,.controls-column{min-width:0}
.graph-heading{font-size:13px;font-weight:700;color:#173c6b;margin:2px 0 7px}
.history-top{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:10px 0 6px;font-weight:700;color:#243b59}
.history-top button{white-space:nowrap}
#simpleHistorySection[hidden],#scanBox[hidden]{display:none!important}
#simpleHistorySection{border-top:1px solid #b5b5b5;margin-top:10px;padding-top:4px}
#chart{width:100%;height:auto;display:block;min-width:0}
#testWeightWrap{margin:7px 0;padding:6px;border:1px solid #bbb;background:#fffdf3;border-radius:5px}
#testWeightWrap[hidden]{display:none!important}
@media(max-width:900px){#app{width:96vw}#app .app-main-grid{grid-template-columns:minmax(0,1fr)}#app .controls-column{order:2}#app .graph-column{order:1}}#app button{background:#f3f3ee;color:#111;border:1px solid #777}#app button:hover{background:#fff}#app button.on{background:#cfe0ff}
#app input{width:74px}#app input#massa{width:90px}#app table{width:100%;border-collapse:collapse;font-size:12px}#app td,#app th{border:1px solid #aaa;padding:2px 5px;text-align:right}
#app td input{width:92px}
#app .bx{border:1px solid #aaa;background:#f6f4e8;padding:6px;margin-top:6px;line-height:2}
#status{margin:6px 0;font-weight:600}canvas#chart{width:100%;background:#fff;border:1px solid #888}
#scanRes{margin:4px 0;font-size:12px}
#graphHeading{margin-bottom:6px}
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

/* Layar pembuka sebelum simulasi instrumen */
#welcome{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(ellipse at 18% 12%,#203a59 0,#101923 48%,#080c12 100%);color:#eaf2fb;overflow:auto}
#welcome[hidden]{display:none}
.welcome-card{width:min(760px,94vw);padding:clamp(24px,5vw,52px);border:1px solid #35516e;border-radius:24px;background:linear-gradient(145deg,#15263aee,#0d1521f5);box-shadow:0 25px 90px #0009}
.welcome-kicker{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#62d9c8;font-weight:700;margin-bottom:14px}
.welcome-card h1{font-size:clamp(28px,4vw,46px);line-height:1.08;margin:0 0 14px;color:#fff}
.welcome-card p{font-size:15px;line-height:1.7;color:#b9c9da;max-width:650px}
.welcome-pills{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 26px}.welcome-pills span{border:1px solid #314a63;background:#101c2a;padding:7px 11px;border-radius:999px;color:#d4e2ef;font-size:12px}
#welcome .cover-btn{background:#35c2b0;color:#06241f;border:0;font-weight:800;border-radius:10px;padding:12px 20px;font-size:14px}
#welcome .cover-note{font-size:11px;color:#8da4bc;margin-top:18px}
/* Menu tiga titik dan panduan kerja */
#menuWrap{position:fixed;right:10px;top:8px;z-index:14;pointer-events:auto}
#menuBtn{width:38px;height:38px;padding:0;border-radius:10px;font-size:24px;line-height:1;background:#16202ef2;border-color:#47617e;box-shadow:0 2px 12px #0007}
#menuDrop{position:absolute;right:0;top:44px;width:190px;background:#16202e;border:1px solid #39516b;border-radius:11px;padding:6px;box-shadow:0 12px 30px #0009}
#menuDrop[hidden],#howtoBackdrop[hidden]{display:none}
#menuDrop button{width:100%;text-align:left;padding:10px;border:0;background:transparent;border-radius:7px}
#menuDrop button:hover{background:#243b52}
#howtoBackdrop{position:fixed;inset:0;z-index:40;background:#050a11c9;display:flex;align-items:center;justify-content:center;padding:18px}
.howto-card{width:min(850px,96vw);max-height:90vh;overflow:auto;background:#111c2a;color:#e6edf5;border:1px solid #3b526d;border-radius:16px;box-shadow:0 20px 65px #000b}
.howto-head{position:sticky;top:0;background:#142236;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #2b4057;z-index:1}
.howto-head h2{margin:0;color:#fff;font-size:21px}.howto-body{padding:18px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.howto-section{background:#172638;border:1px solid #30465d;border-radius:12px;padding:15px}.howto-section h3{margin:0 0 10px;color:#62d9c8;font-size:15px}.howto-section ol{padding-left:18px;margin:0;color:#c7d5e4}.howto-section li{margin:0 0 9px;line-height:1.5;font-size:12px}
.howto-foot{padding:0 18px 18px;color:#8fa3bd;font-size:11px;line-height:1.5}
#zeroNotice{margin-top:8px;padding:8px 9px;border-radius:8px;border:1px solid #775c2e;background:#372a16;color:#ffd58a;font-size:11px;line-height:1.45}
#zeroNotice.done{border-color:#23695a;background:#102e28;color:#8ce8c9}
body:not(.started) .panel-toggle{display:none}
@media(max-width:700px){.howto-body{grid-template-columns:1fr}.welcome-card{padding:24px}.welcome-card p{font-size:13px}}


/* Fokus animasi otomatis: sembunyikan tabel/panel selama proses berjalan. */
#animationFocusHud{position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:60;width:min(530px,94vw);display:flex;align-items:center;justify-content:space-between;gap:14px;padding:10px 12px;border:1px solid #43627c;border-radius:13px;background:linear-gradient(135deg,rgba(7,17,29,.94),rgba(18,39,59,.94));box-shadow:0 12px 32px #0008;color:#eaf4fc;backdrop-filter:blur(12px)}
#animationFocusHud[hidden]{display:none!important}
.focus-copy{min-width:0;flex:1}
.focus-kicker{display:flex;align-items:center;gap:7px;color:#7ae5d5;font-size:9px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.focus-dot{width:7px;height:7px;flex:none;border-radius:50%;background:#48e0bc;box-shadow:0 0 10px #48e0bc;animation:opticPulse 1.4s infinite}
#focusProcessName{display:block;margin-top:3px;font-size:13px;line-height:1.25;font-weight:800;color:#fff}
#focusProcessDetail{display:block;margin-top:3px;font-size:10px;line-height:1.35;color:#b4c8dc}
.focus-actions{display:flex;gap:5px;align-items:center;flex:none}
#animationFocusHud button{padding:7px 9px;border-radius:8px;white-space:nowrap;font-weight:700;font-size:11px;background:#1b3450;border-color:#45627e;color:#edf6ff}
#animationFocusHud #focusPause{background:#35c2b0;border-color:#8de8db;color:#04211d}
#animationFocusHud #focusStop{background:#57251f;border-color:#a64c41;color:#fff}
body.focus-animation #c{position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important}
body.focus-animation .bar,body.focus-animation .col,body.focus-animation .panel-toggle,body.focus-animation #menuWrap,body.focus-animation #toast,body.focus-animation #app,body.focus-animation #howtoBackdrop,body.focus-animation .lb{display:none!important}
/* HUD proses optik tetap terlihat dalam mode fokus, hanya saat pembacaan aktif. */
body.focus-animation #opticalStatus{display:block!important}
body.focus-animation #animationFocusHud{display:flex!important}
body.focus-animation #hud{display:none!important}
body.focus-animation{background:#10161f}
@media(max-width:600px){#animationFocusHud{align-items:flex-start;gap:8px;padding:8px}.focus-actions{flex-wrap:wrap;justify-content:flex-end}#animationFocusHud button{padding:6px 7px;font-size:10px}#focusProcessDetail{max-width:48vw}}


/* Panel Concentration ditata menjadi langkah kerja yang jelas dan dapat discroll. */
#p-conc{max-height:66vh;overflow:auto;padding:2px 5px 8px 0;color:#1e344d}
.calc-guide{padding:9px 11px;border:1px solid #b6c9dc;border-radius:9px;background:#edf5fc;color:#294762;line-height:1.45;font-size:11px;margin:7px 0 10px}
.calc-section{border:1px solid #c5d2df;border-radius:10px;background:#f8fbff;padding:10px;margin:8px 0;color:#1d344c;box-shadow:0 1px 2px #15304a10}
.calc-section-title{display:flex;gap:9px;align-items:flex-start;margin:0 0 8px}
.calc-section-number{display:grid;place-items:center;flex:none;width:25px;height:25px;border-radius:8px;background:#d8e9fa;color:#184d7a;font-weight:800;font-size:12px}
.calc-section-title h4{margin:0 0 3px;color:#174e7b;font-size:13px;font-weight:800}
.calc-section-title p,.calc-help{margin:0;color:#52677e;font-size:10px;line-height:1.45}
.calc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:8px 0}
.calc-field{display:block;color:#334d68;font-weight:700;font-size:10px;min-width:0}
.calc-field input{width:100%!important;max-width:100%;display:block;margin-top:4px;padding:5px;border:1px solid #9dafc3;border-radius:5px;background:#fff;color:#182b40}
.calc-warning{margin:8px 0;padding:9px 11px;border-left:3px solid #c46b18;background:#fff3df;color:#6f3900;border-radius:6px;font-size:12px;line-height:1.45}
.calc-formula{padding:8px;border-radius:7px;background:#eaf3e9;border:1px solid #bfdbbc;color:#2d5d31;font-size:10px;line-height:1.45;margin:8px 0}
#testWeightSummary{overflow-x:auto;margin-top:8px}
#testWeightSummary table{width:100%;border-collapse:collapse;font-size:10px;color:#23384c}
#testWeightSummary th,#testWeightSummary td{border:1px solid #cfdae5;padding:4px;text-align:left;vertical-align:middle}
#testWeightSummary th{background:#eaf1f8;color:#254661}
#testWeightSummary input{width:82px!important;max-width:100%;padding:4px;border:1px solid #b5c3d1;border-radius:4px;background:#fff;color:#18314a}
.nominal-ok{color:#216b3b;font-weight:700}.nominal-warn{color:#a14b16;font-weight:800}
#testWeightWrap{margin:7px 0;padding:7px;border:1px solid #b9d0e4;background:#edf6ff;border-radius:7px}
#testWeightWrap[hidden]{display:none!important}
#regularSampleFields[hidden]{display:none!important}
.calc-actions{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px}
.calc-actions button{margin:0}
@media(max-width:520px){.calc-grid{grid-template-columns:1fr}#p-conc{max-height:62vh}}

</style></head><body>
<canvas id="c"></canvas>
<div id="welcome">
 <div class="welcome-card">
  <div class="welcome-kicker">Laboratorium Analisis Instrumental · Simulasi Edukasi</div>
  <h1>Digital Twin<br>Spektrofotometer UV-Vis</h1>
  <div class="welcome-pills"><span>Model instrumen 3D</span><span>Zero blank aquades</span><span>Standar 0–25 ppm</span><span>Kurva kalibrasi</span></div>
  <button id="enterApp" class="cover-btn" type="button">Mulai Simulasi <span aria-hidden="true">→</span></button>
 </div>
</div>
<div id="menuWrap">
 <button id="menuBtn" type="button" aria-label="Buka menu" title="Menu">⋮</button>
 <div id="menuDrop" hidden><button id="openHowto" type="button">📘 &nbsp; Cara Kerja</button></div>
</div>
<div id="howtoBackdrop" hidden>
 <div class="howto-card" role="dialog" aria-modal="true" aria-labelledby="howtoTitle">
  <div class="howto-head"><h2 id="howtoTitle">Cara Kerja</h2><button id="closeHowto" type="button" aria-label="Tutup panduan">✕</button></div>
  <div class="howto-body">
   <section class="howto-section"><h3>1. Persiapan</h3><ol>
    <li>Nyalakan UPS terlebih dahulu, lalu instrumen, komputer, dan monitor.</li>
    <li>Tunggu proses warm-up selesai.</li>
    <li>Buka aplikasi Cary WinUV dari tombol toolbar atau layar monitor.</li>
    <li>Buka kompartemen sampel, pasang kuvet bersih berisi aquades, kemudian tutup kompartemen.</li>
    <li>Pastikan larutan yang dipilih adalah Aquades. Lakukan Zero Blank satu kali sebelum pengukuran.</li>
   </ol></section>
   <section class="howto-section"><h3>2. Pengukuran</h3><ol>
    <li>Pastikan Zero Blank aquades sudah berhasil. Pilih tab <b>Concentration</b> untuk mengukur deret standar 0, 5, 10, 15, 20, dan 25 ppm.</li>
    <li>Tekan <b>Ukur semua standar</b>, lalu <b>Hitung kurva</b> untuk memperoleh persamaan kalibrasi, koefisien korelasi r, dan grafik dengan konsentrasi pada sumbu X serta absorbansi pada sumbu Y.</li>
    <li>Untuk uji presisi, pilih <b>Presisi 1–5</b> pada Larutan kerja lalu lakukan pengukuran pada panjang gelombang analisis.</li>
    <li>Untuk uji akurasi, pilih <b>Akurasi 1</b>. Masukkan bobot masing-masing sampel sesuai data praktikum pada kolom Bobot akurasi (g); nilai awal 0,005 g hanya nilai contoh.</li>
    <li>Hasil Simple Reads akan terus ditambahkan ke tabel setiap kali pengukuran selesai. Gunakan tombol <b>Reset tabel</b> hanya saat ingin menghapus riwayat tabel tersebut.</li>
    <li>Saat pengukuran berjalan, bagian luar instrumen menjadi transparan agar jalur proses terlihat, tanpa label nama komponen.</li>
    <li>Tekan <b>Jeda proses</b> lalu <b>Kenali Bagian</b> untuk menampilkan label komponen dan membaca penjelasannya. Keluar dari mode Kenali Bagian sebelum melanjutkan proses.</li>
   </ol></section>
   <section class="howto-section"><h3>3. Mematikan Alat</h3><ol>
    <li>Hentikan pengukuran yang sedang berjalan dan tutup jendela Cary WinUV.</li>
    <li>Ambil kuvet, buang larutan sesuai prosedur laboratorium, lalu bersihkan kuvet.</li>
    <li>Matikan monitor, kemudian komputer.</li>
    <li>Matikan instrumen setelah aplikasi dan komputer selesai digunakan.</li>
    <li>Matikan UPS paling akhir. Ikuti SOP laboratorium jika urutan resmi di tempat praktik berbeda.</li>
   </ol></section>
  </div>
  <div class="howto-foot">Catatan: simulasi ini bersifat edukatif. Nilai λmax acuan 246,0 nm diatur pada konstanta DATA_LMAX_NM; ubah sesuai hasil praktikum aktual. Parameter hasil selain nilai masukan tetap ilustratif. Untuk praktikum aktual, blanko harus mengikuti SOP dan matriks pelarut sampel.</div>
 </div>
</div>
<div class="bar">
 <div class="grp"><span>Kamera</span><button data-v="front">Depan</button><button data-v="top">Atas</button><button data-v="back">Belakang</button><button data-v="side">Samping</button><button data-v="inst">Instrumen</button><button data-v="opt">Optik</button><button data-v="lamp">Lampu</button><button data-v="cuv">Kuvet</button><button data-v="mon">Monitor</button></div>
 <div class="grp"><span>Tampilan</span><button id="bX">Transparan</button><button id="bB" class="on">Berkas</button><button id="bL">Label</button><button id="bR">Putar</button><button id="bIdentify" title="Jeda pengukuran dan kenali komponen">Kenali Bagian</button><button id="bPause">Jeda animasi</button></div>
 <div class="grp"><button id="bA" class="pri">Buka Cary WinUV</button><button id="bP">Panel</button><button id="bFS">Layar penuh</button><button id="bRe">Reset</button></div>
</div>
<!-- Tombol panah untuk menyembunyikan dan memunculkan panel samping -->
<button id="toggleLeft" class="panel-toggle" type="button" aria-label="Sembunyikan panel kiri" title="Sembunyikan panel kiri">‹</button>
<button id="toggleRight" class="panel-toggle" type="button" aria-label="Sembunyikan panel kanan" title="Sembunyikan panel kanan">›</button>
<div class="col" id="colL">
 <div class="panel"><h4>Urutan operasi</h4><div id="prog"><i></i></div><ul id="chk"></ul></div>
 <div class="panel"><h4>Sampel &amp; kuvet</h4>
  <label class="lab">Larutan kerja</label><select id="smp">
   <optgroup label="Zero Blank"><option value="aquades">Aquades (Zero Blank)</option></optgroup>
   <optgroup label="Standar Thiamin">
    <option value="std_0">Standar 0 ppm</option><option value="std_5">Standar 5 ppm</option><option value="std_10">Standar 10 ppm</option><option value="std_15">Standar 15 ppm</option><option value="std_20">Standar 20 ppm</option><option value="std_25">Standar 25 ppm</option>
   </optgroup>
   <optgroup label="Uji Presisi"><option value="pres_1">Presisi 1</option><option value="pres_2">Presisi 2</option><option value="pres_3">Presisi 3</option><option value="pres_4">Presisi 4</option><option value="pres_5">Presisi 5</option></optgroup>
   <optgroup label="Uji Akurasi"><option value="akurasi_1">Akurasi 1</option></optgroup>
   <option value="spike">Sampel + spike</option>
   <option value="unk">Sampel tidak diketahui</option>
  </select>
  <div id="zeroNotice">⚠ Belum melakukan Zero Blank. Pilih Aquades, siapkan kuvet, lalu klik <b>Zero Blank (Aquades)</b> sebelum mengukur larutan lain.</div>
  <div id="testWeightWrap" hidden><label class="lab" id="testWeightLabel" for="testWeight">Bobot sampel uji (g)</label><input id="testWeight" type="number" min="0.0001" step="0.0001" value="0.0050" style="width:100%"><p class="cap">Bobot disimpan terpisah untuk Presisi 1–5 dan satu pengukuran Akurasi 1. Nilai awal masing-masing 0,0050 g; ubah sesuai hasil penimbangan praktikum.</p></div>
  <label class="lab">Konsentrasi standar aktif: <b id="cv">5</b> ppm</label><input type="range" id="conc" min="0" max="25" step="5" value="5">
  <div class="row" style="margin-top:8px"><button id="bLid">Buka tutup</button><button id="bCuv">Pasang kuvet</button></div>
  <p class="cap" style="margin:8px 0 0">Spektrum thiamin bersifat ilustratif (λmax sekitar 246 nm; verifikasi dengan SOP). Untuk daerah UV, gunakan kuvet kuarsa. Bobot Akurasi 1 dapat diinput sesuai data praktikum; nilai awal 0,005 g hanya contoh.</p></div>
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
  <div class="cap">1 Lampu → 2 Cermin M1 → 3 Celah masuk → 4 Kisi (memilih λ) → 5 Cermin M2 → 6 Chopper → 7 Kuvet sampel &amp; referensi → 8 Detektor PMT. Kedua jalur digambar bersamaan untuk memperjelas lintasan; partikel foton menunjukkan urutan sampel/referensi yang dimodulasi chopper. Berkas sampel meredup setelah kuvet.</div></div>
</div>
<div class="panel" id="hud"></div>
<div id="toast"></div>
<div id="opticalStatus" hidden aria-live="polite">
 <div class="optic-hud-head"><span class="optic-live-dot"></span> Simulasi alur optik aktif</div>
 <div id="opticalStep">Menunggu instrumen siap</div>
 <div id="opticalDetail">Sumber cahaya → monokromator → sistem berkas → kuvet → detektor.</div>
 <div class="optic-stages">
  <div class="optic-stage" data-stage="0"><i></i><span>Sumber</span></div>
  <div class="optic-stage" data-stage="1"><i></i><span>Monokromator</span></div>
  <div class="optic-stage" data-stage="2"><i></i><span>Chopper</span></div>
  <div class="optic-stage" data-stage="3"><i></i><span>Kuvet</span></div>
  <div class="optic-stage" data-stage="4"><i></i><span>Detektor</span></div>
 </div>
</div>

<div id="animationFocusHud" hidden aria-live="polite">
 <div class="focus-copy">
  <div class="focus-kicker"><span class="focus-dot"></span> Mode fokus animasi</div>
  <strong id="focusProcessName">Menyiapkan proses optik</strong>
  <small id="focusProcessDetail">Tampilan tabel dan panel akan kembali setelah proses selesai.</small>
 </div>
 <div class="focus-actions">
  <button id="focusPause" type="button">Jeda proses</button>
  <button id="focusIdentify" type="button" title="Jeda lalu tampilkan label komponen">Kenali</button>
  <button id="focusStop" type="button">Stop</button>
 </div>
</div>
<div id="app" hidden>
 <div class="wt"><span>Cary WinUV · Simulasi pengukuran</span><div class="wt-actions"><button id="minApp" type="button" title="Minimalkan untuk melihat animasi 3D">−</button><button id="xapp" type="button" title="Tutup aplikasi">✕</button></div></div>
 <div class="bd">
  <div class="app-main-grid">
   <section class="graph-column">
    <div id="graphHeading" class="graph-heading">Grafik spektrum / kurva kalibrasi</div>
    <canvas id="chart" width="800" height="480"></canvas>
    <div id="scanBox"><div id="scanRes"></div><button id="bUseL">Pakai λmax untuk analisis</button></div>
    <div id="simpleHistorySection" hidden>
     <div class="history-top"><span>Riwayat Simple Reads</span><button id="aRefresh" type="button" title="Refresh tampilan dan kosongkan tabel riwayat">↻ Refresh / Reset tabel</button></div>
     <div id="tbl"></div>
    </div>
   </section>
   <section class="controls-column">
    <div id="status"></div>
    <div style="margin:4px 0 8px"><button data-t="scan" class="on">Scan</button> <button data-t="simple">Simple Reads</button> <button data-t="conc">Concentration</button></div>
    <div id="p-scan" style="margin:6px 0">λ awal <input id="s0" type="number" value="400"> nm &nbsp; λ akhir <input id="s1" type="number" value="200"> nm <small>(190–900; urut menurun)</small><p style="margin:5px 0;color:#314d75;font-size:11px"><b>Scan λmax hanya menggunakan standar 25 ppm.</b> Nilai λmax acuan muncul pada grafik setelah scan selesai.</p></div>
    <div id="p-simple" style="margin:6px 0" hidden>λ <input id="sl" type="number" value="246"> nm &nbsp; Replikat <input id="sn" type="number" value="3" min="1" max="10"><p class="cap">Setiap pembacaan akan ditambahkan ke Riwayat Simple Reads. Mengganti larutan tidak menghapus data sebelumnya.</p></div>
    <div id="p-conc" hidden style="margin:6px 0">
     <div class="calc-guide"><b>Urutan kerja:</b> (1) ukur deret standar dan hitung kurva, (2) ukur sampel lalu hitung kadar, (3) evaluasi presisi/akurasi memakai bobot, bukan memasukkan bobot sebagai ppm.</div>
     <section class="calc-section">
      <div class="calc-section-title"><span class="calc-section-number">1</span><div><h4>Kurva Kalibrasi Standar</h4><p>Deret standar 0, 5, 10, 15, 20, dan 25 ppm. Nilai absorbansi awal diisi memakai data praktikum yang kamu kirim, tetapi setiap sel tetap bisa diedit manual.</p></div></div>
      <label class="calc-field">Sumber data saat tombol Ukur ditekan<select id="stdDataMode"><option value="praktikum" selected>Data praktikum (dari tabel Excel)</option><option value="simulasi">Simulasi pembacaan alat</option></select></label>
      <p id="stdDataModeHint" class="calc-help">Mode data praktikum aktif: tombol Ukur akan memakai nilai absorbansi di tabel (termasuk hasil edit manual). Animasi alat tetap berjalan. Pilih Simulasi pembacaan alat untuk mengganti nilai dengan hasil simulasi.</p>
      <label class="calc-field">Panjang gelombang analisis (nm)<input id="cl" type="number" value="246" min="190" max="900" step="0.1"></label>
      <div style="margin:5px 0"><button id="cUseL">Pakai λmax hasil Scan</button> <small>(acuan awal sekitar 246 nm)</small></div>
      <div id="stdtab"></div>
      <div class="calc-actions"><button id="cAll">Ukur semua standar</button><button id="cFit">Hitung kurva</button><button id="cClr">Reset data kalibrasi</button><button id="cAddStd" disabled title="Deret standar tetap 0, 5, 10, 15, 20, dan 25 ppm">Standar tetap 0–25 ppm</button></div>
      <p class="calc-help" style="margin-top:7px">Hasil akhir di bawah dihitung ulang otomatis setelah nilai konsentrasi atau absorbansi standar selesai diedit (tekan Enter atau pindah dari sel). Kadar sampel, uji presisi, akurasi, dan % recovery memakai kurva kalibrasi terbaru.</p>
     </section>
     <section class="calc-section" id="assaySection">
      <div class="calc-section-title"><span class="calc-section-number">2</span><div><h4>Perhitungan Kadar Sampel</h4><p>Setelah kurva dihitung, absorbansi sampel akan dikonversi menjadi konsentrasi larutan dan kadar berdasarkan volume, pengenceran, serta massa.</p></div></div>
      <div id="regularSampleFields">
       <div class="calc-grid">
        <label class="calc-field">Massa sampel (g)<input id="massa" type="number" step="0.0001" min="0" value="2.5012"></label>
        <label class="calc-field">Volume labu (mL)<input id="vol" type="number" step="1" min="0" value="50"></label>
        <label class="calc-field">Faktor pengenceran<input id="df" type="number" min="1" step="0.5" value="1"></label>
        <label class="calc-field">Bobot rata-rata tablet (g, opsional)<input id="tabw" type="number" step="0.001" min="0" placeholder="contoh: 0.500"></label>
       </div>
       <div class="calc-actions"><button id="cUnk">Ukur sampel</button></div>
      </div>
      <div id="weightSampleNote" class="calc-formula" hidden>Mode uji bobot aktif. Bobot, volume preparasi, dan faktor pengenceran digunakan untuk menghitung konsentrasi nominal; input massa sampel biasa disembunyikan supaya tidak tertukar.</div>
      <label class="calc-field">Absorbansi sampel (AU)<input id="aU" type="number" step="0.001" min="0" placeholder="terisi otomatis atau ketik manual"></label>
      <div class="calc-actions"><button id="applyLastRead" type="button" title="Pindahkan hasil sampel terakhir dari Simple Reads">Ambil hasil sampel terakhir</button></div>
      <small id="sampleAbsSource" style="display:block;color:#52677e;margin:5px 0">Nilai otomatis diambil dari rata-rata pembacaan Simple Reads; tetap bisa diedit manual.</small>
     </section>
     <section class="calc-section" id="weightTestSection">
      <div class="calc-section-title"><span class="calc-section-number">3</span><div><h4>Uji Presisi dan Akurasi Berbasis Bobot</h4><p>Larutan uji dihitung dari massa timbang dan cara preparasi. Bobot (g) bukan ppm; nilai bobot menentukan konsentrasi nominal setelah memperhitungkan volume dan pengenceran.</p></div></div>
      <div class="calc-grid">
       <label class="calc-field">Volume labu larutan uji (mL)<input id="testVol" type="number" min="0.1" step="1" value="50"></label>
       <label class="calc-field">Faktor pengenceran uji<input id="testDF" type="number" min="0.1" step="0.5" value="4"></label>
      </div>
      <div class="calc-formula">Rumus konsentrasi nominal: <b>C (ppm) = bobot (g) × 1.000.000 ÷ [volume (mL) × faktor pengenceran]</b>. Nilai awal 0,0050 g; volume 50 mL dan pengenceran 4× memberi sekitar 25 ppm. Format angka Indonesia digunakan: <b>25,000 ppm berarti 25 ppm</b>, bukan 25.000 ppm. Sesuaikan volume/pengenceran dengan prosedur praktikum aktual.</div>
      <p class="calc-help">Edit setiap bobot di tabel ini, atau pilih Presisi/Akurasi pada menu Larutan kerja di panel kiri untuk mengedit bobot aktif. Absorbansi simulasi dihitung berdasarkan konsentrasi nominal tersebut.</p>
      <div id="testWeightSummary"></div>
     </section>
     <section class="calc-section" id="recoverySection">
      <div class="calc-section-title"><span class="calc-section-number">4</span><div><h4>Uji Recovery (Sampel + Spike)</h4><p>Bagian ini digunakan bila konsentrasi spike yang ditambahkan diketahui.</p></div></div>
      <label class="calc-field">Absorbansi sampel + spike (AU)<input id="aSp" type="number" step="0.001" min="0" placeholder="terisi otomatis atau ketik manual"></label>
      <div class="calc-actions"><button id="applyLastSpike" type="button" title="Pindahkan hasil sampel + spike terakhir">Ambil hasil spike terakhir</button><button id="cSpk">Ukur sampel + spike</button></div>
      <small id="spikeAbsSource" style="display:block;color:#52677e;margin:5px 0">Nilai otomatis dari Simple Reads atau bisa dimasukkan manual.</small>
      <label class="calc-field" style="margin-top:7px">Konsentrasi spike yang ditambahkan (ppm)<input id="cAdd" type="number" step="0.5" min="0" value="2"></label>
     </section>
    </div>
    <div id="cres" style="margin-top:4px;font-size:12px"></div>
    <section id="autoFinalResults" class="calc-section" aria-live="polite" style="margin-top:10px">
      <div class="calc-section-title"><span class="calc-section-number">✓</span><div><h4>Rekapitulasi Hasil Akhir (Otomatis)</h4><p>Semua hasil dihitung ulang dari tabel standar terbaru dan data sampel yang tersedia.</p></div></div>
      <div id="autoFinalResultsBody" class="calc-formula">Masukkan atau ukur data standar, lalu hitung kurva untuk menampilkan hasil akhir.</div>
    </section>
    <div style="margin-top:8px;display:flex;gap:5px;flex-wrap:wrap"><button id="aBase">Zero Blank (Aquades)</button><button id="aStart">Start</button><button id="aStop">Stop</button><button id="aCsv">Ekspor CSV</button></div>
   </section>
  </div>
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
const S={ups:0,inst:0,pc:0,mon:0,booted:0,bootT:0,warm:0,base:0,lid:0,cuv:0,app:0,xray:0,beam:1,job:null,lam:500,sample:'blank',solutionKey:'aquades',conc:5,spkC:2,tab:'scan',res:null,lbl:0,autoX:0,camOpt:0,lampMode:'auto',lampColor:AUTO_V,lampI:1,lmax:null,out:{},identifyMode:0,measureVisual:0,paused:0,batchMeasuring:0,resumeAppAfterIdentify:0,appMinimized:0,opticalClock:0,visualTime:0,simpleHistory:[],lastSampleRead:null,isAutoFillingAbs:false,autoAbsKey:null,focusRestore:null,testVolumeMl:50,testDilutionFactor:4,precisionWeights:{pres_1:0.0050,pres_2:0.0050,pres_3:0.0050,pres_4:0.0050,pres_5:0.0050},accuracyWeights:{akurasi_1:0.0050}};
const DATA_LMAX_NM=246.0; // Nilai acuan dari model/data yang sudah dipakai. Ubah sesuai hasil praktikum aktual.
// Data praktikum yang terlihat pada tabel Excel yang dikirim pengguna.
// Nilai ini menjadi sumber default untuk pengukuran standar; setiap sel tetap bisa diedit manual.
const PRACTICUM_STANDARD_DATA=[
 {c:0,a:0.002},
 {c:5,a:0.212},
 {c:10,a:0.402},
 {c:15,a:0.620},
 {c:20,a:0.811},
 {c:25,a:1.035}
];
function practicumAbsorbanceForConcentration(c){
 const item=PRACTICUM_STANDARD_DATA.find(q=>Math.abs(Number(q.c)-Number(c))<1e-9);
 return item?item.a:null;
}
S.cal={l:246,std:PRACTICUM_STANDARD_DATA.map(q=>({c:q.c,a:q.a,sd:null,source:'praktikum'})),fit:null,unk:null,spk:null};
// ---------- util
let toastT;function toast(t){const e=$('toast');e.textContent=t;e.style.opacity=1;clearTimeout(toastT);toastT=setTimeout(()=>e.style.opacity=0,2800)}
function W(l){let r=0,g=0,b=0;if(l<380)return[.55,.25,1];if(l<440){r=(440-l)/60;b=1}else if(l<490){g=(l-440)/50;b=1}else if(l<510){g=1;b=(510-l)/20}else if(l<580){r=(l-510)/70;g=1}else if(l<645){r=1;g=(645-l)/65}else if(l<=780)r=1;else return[.5,.1,.1];return[r,g,b]}
const G=(l,m,s)=>Math.exp(-.5*((l-m)/s)**2);
const fmtID=(v,d=3)=>Number.isFinite(Number(v))?Number(v).toLocaleString('id-ID',{minimumFractionDigits:d,maximumFractionDigits:d}):'—';
// Thiamin HCl dalam HCl 0,1 M (ILUSTRATIF): puncak ~246 nm, A1%1cm ~410 -> ~0,0395 Abs per ppm
const THI=(l,c)=>c*.0395*(G(l,246,12.5)+.10*G(l,272,16)+.9*G(l,205,11));
const UNK=7.35;
function testWeightForKey(key){if((key||'').startsWith('pres_'))return Number(S.precisionWeights[key]??0.0050);if((key||'').startsWith('akurasi_'))return Number(S.accuracyWeights[key]??0.0050);return NaN}
function testVolumeMl(){const v=+$('testVol')?.value||S.testVolumeMl||50;return v>0?v:50}
function testDilutionFactor(){const d=+$('testDF')?.value||S.testDilutionFactor||4;return d>0?d:4}
function nominalTestConcentrationPPM(key){const w=testWeightForKey(key),v=testVolumeMl(),df=testDilutionFactor();return Number.isFinite(w)&&w>0&&v>0&&df>0?w*1000000/(v*df):NaN}
function testMassFoundMg(abs,fit,volumeMl,dilution){if(!fit||!Number.isFinite(abs)||!Number.isFinite(fit.a)||fit.a<=1e-12)return NaN;const measuredC=(abs-fit.b)/fit.a;if(!Number.isFinite(measuredC)||measuredC<0)return NaN;return measuredC*(dilution||testDilutionFactor())*((volumeMl||testVolumeMl())/1000)}
function specA(l){const s=S.sample;let c=0;if(s==='std')c=S.conc;else if(s==='unk'){const k=S.solutionKey||'pres_1';if(k.startsWith('pres_')||k.startsWith('akurasi_')){c=nominalTestConcentrationPPM(k);if(k.startsWith('pres_')){const offsets=[-.012,.006,.002,-.009,.013];const ix=Math.max(0,Math.min(4,parseInt(k.split('_')[1],10)-1));c*=1+offsets[ix]}}else c=UNK}else if(s==='spk')c=UNK+S.spkC*.97;return Math.min(3.5,THI(l,Number.isFinite(c)?Math.max(0,c):0))}
const noise=()=>(Math.random()-.5)*.004;
const readA=l=>Math.max(0,(S.cuv?specA(l):0)+noise());
// ---------- scene
const scene=new THREE.Scene();scene.background=new THREE.Color(0x1b2330);
const cam=new THREE.PerspectiveCamera(45,1,.1,100);cam.position.set(-1,6.2,16);
const ren=new THREE.WebGLRenderer({canvas:$('c'),antialias:true,alpha:false,powerPreference:'high-performance'});ren.setPixelRatio(Math.min(Math.max(window.devicePixelRatio||1,1.75),2.5));ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;ren.shadowMap.autoUpdate=true;
ren.outputEncoding=THREE.sRGBEncoding;ren.toneMapping=THREE.ACESFilmicToneMapping;ren.toneMappingExposure=1.1;ren.physicallyCorrectLights=false;ren.domElement.style.imageRendering='auto';
{const pm=new THREE.PMREMGenerator(ren),es=new THREE.Scene();es.background=new THREE.Color(0x7d8794);[[0,9,0,14,.5,14,1.8],[10,4,6,2,6,6,1.3],[-10,4,6,2,6,6,1.1],[0,3,-10,16,5,1,.8]].forEach(a=>{const m=new THREE.Mesh(new THREE.BoxGeometry(a[3],a[4],a[5]),new THREE.MeshBasicMaterial({color:new THREE.Color(a[6],a[6],a[6])}));m.position.set(a[0],a[1],a[2]);es.add(m)});scene.environment=pm.fromScene(es,.04).texture}
const ctl=new THREE.OrbitControls(cam,ren.domElement);ctl.target.set(1,.8,0);ctl.maxPolarAngle=Math.PI/2.05;ctl.minDistance=1.5;ctl.maxDistance=24;ctl.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xffffff,0x667788,.8));
const dl=new THREE.DirectionalLight(0xffffff,.9);dl.position.set(5,12,8);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);dl.shadow.bias=-0.00015;dl.shadow.radius=3;Object.assign(dl.shadow.camera,{left:-12,right:12,top:12,bottom:-12});scene.add(dl);
const std=(c,o={})=>new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.6,metalness:.05},o));
function bx(w,h,d,m,x,y,z,p){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),typeof m==='number'?std(m):m);o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;(p||scene).add(o);return o}
function cy(r,h,m,x,y,z,p,rx,rz){const o=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,24),typeof m==='number'?std(m):m);o.position.set(x,y,z);o.rotation.x=rx||0;o.rotation.z=rz||0;o.castShadow=true;(p||scene).add(o);return o}
function sp(r,m,x,y,z,p){const o=new THREE.Mesh(new THREE.SphereGeometry(r,12,12),m);o.position.set(x,y,z);(p||scene).add(o);return o}
const clickables=[];
function tag(m,k){m.traverse(o=>{if(o.isMesh){o.userData.key=k;clickables.push(o)}});return m}
function canvasTex(w,h,fn){const c=document.createElement('canvas');c.width=w;c.height=h;fn(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t}
function plane(pw,ph,tx,x,y,z,p,flat){const m=new THREE.Mesh(new THREE.PlaneGeometry(pw,ph),new THREE.MeshBasicMaterial({map:tx}));m.position.set(x,y,z);if(flat)m.rotation.x=-Math.PI/2;(p||scene).add(m);return m}
const txt=(lines,w,h,bg,fg,fs)=>canvasTex(w,h,(g)=>{g.fillStyle=bg;g.fillRect(0,0,w,h);g.fillStyle=fg;g.font='bold '+fs+'px sans-serif';g.textBaseline='middle';lines.forEach((t,i)=>g.fillText(t,10,h*(i+1)/(lines.length+1)))});
// ---------- Lingkungan laboratorium: lantai, meja keramik, dan dinding cutaway
// Lantai ruang berada di bawah meja; instrumen dan aksesori tetap berada pada permukaan meja y=0.
const floorTile = canvasTex(512,512,(g,w,h)=>{
 const grad=g.createLinearGradient(0,0,w,h);
 grad.addColorStop(0,'#edf1f3');grad.addColorStop(.5,'#e3e9ed');grad.addColorStop(1,'#dce4e8');
 g.fillStyle=grad;g.fillRect(0,0,w,h);
 for(let i=0;i<2400;i++){
  const x=Math.random()*w,y=Math.random()*h,a=.012+Math.random()*.025;
  g.fillStyle=`rgba(75,95,108,${a})`;g.fillRect(x,y,1+Math.random()*2,1+Math.random()*2);
 }
 g.strokeStyle='rgba(120,138,150,.42)';g.lineWidth=4;g.strokeRect(2,2,w-4,h-4);
 g.strokeStyle='rgba(255,255,255,.7)';g.lineWidth=2;g.strokeRect(7,7,w-14,h-14);
});
floorTile.wrapS=floorTile.wrapT=THREE.RepeatWrapping;
floorTile.repeat.set(40,40);floorTile.anisotropy=ren.capabilities.getMaxAnisotropy();
const floorMat=new THREE.MeshStandardMaterial({map:floorTile,color:0xffffff,roughness:.86,metalness:.01});
const floor=new THREE.Mesh(new THREE.PlaneGeometry(100,100),floorMat);
floor.rotation.x=-Math.PI/2;floor.position.y=-1.035;floor.receiveShadow=true;floor.renderOrder=-2;scene.add(floor);

// Pengelompokan dinding agar dinding belakang dapat disembunyikan saat kamera melihat dari belakang.
// Ini adalah tampilan cutaway untuk inspeksi 3D, bukan tembok yang menembus alat.
const rearRoomParts=[];
const leftRoomParts=[];
const rightRoomParts=[];
const wallMat=std(0xe8eef2,{roughness:.94,metalness:0});
function addRoomPart(list,mesh){list.push(mesh);return mesh}
// Dinding belakang beserta panel-panelnya.
addRoomPart(rearRoomParts,bx(30,8,.2,wallMat,0,3,-4.3));
// Dinding samping tetap ada, tetapi bisa di-cutaway jika kamera bergerak ke luar sisi ruangan.
addRoomPart(leftRoomParts,bx(.2,8,40,wallMat,-15,3,15));
addRoomPart(rightRoomParts,bx(.2,8,40,wallMat,15,3,15));
for(let x=-13.25;x<=13.25;x+=3.25)
 addRoomPart(rearRoomParts,bx(.022,7.25,.018,0xcbd7df,x,3,-4.185));
for(let z=-1;z<=31;z+=4){
 addRoomPart(leftRoomParts,bx(.018,7.25,.022,0xcbd7df,-14.84,3,z));
 addRoomPart(rightRoomParts,bx(.018,7.25,.022,0xcbd7df,14.84,3,z));
}
// Lis bawah berada dekat lantai ruangan pada y=-1.035.
addRoomPart(rearRoomParts,bx(30,.22,.075,0x607f90,0,-.925,-4.15));
addRoomPart(leftRoomParts,bx(.075,.22,40,0x607f90,-14.85,-.925,15));
addRoomPart(rightRoomParts,bx(.075,.22,40,0x607f90,14.85,-.925,15));
[-7,4].forEach(x=>addRoomPart(rearRoomParts,bx(.38,8,.26,0x77a5b2,x,3,-4.12)));
const cab=addRoomPart(rearRoomParts,bx(2.6,3,.5,0x8fa3b5,-3,1.5,-4));
cab.material.transparent=true;cab.material.opacity=.46;

// Meja kerja dengan permukaan keramik terang. Ukuran meja menutupi instrumen, UPS, PC, monitor,
// serta aksesori yang sudah dimodelkan pada koordinat y=0.
const tableCeramicTex=canvasTex(256,256,(g,w,h)=>{
 g.fillStyle='#eeeae0';g.fillRect(0,0,w,h);
 const grad=g.createLinearGradient(0,0,w,h);grad.addColorStop(0,'rgba(255,255,255,.45)');grad.addColorStop(1,'rgba(155,164,163,.08)');
 g.fillStyle=grad;g.fillRect(0,0,w,h);
 // Nat tipis dan tepi tile memberikan kesan keramik, tanpa pola yang terlalu mencolok.
 g.strokeStyle='rgba(118,130,133,.33)';g.lineWidth=3;g.strokeRect(2,2,w-4,h-4);
 g.strokeStyle='rgba(255,255,255,.9)';g.lineWidth=1;g.strokeRect(7,7,w-14,h-14);
 for(let i=0;i<260;i++){const x=Math.random()*w,y=Math.random()*h;g.fillStyle=`rgba(110,120,120,${.012+Math.random()*.025})`;g.fillRect(x,y,1.2,1.2)}
});
tableCeramicTex.wrapS=tableCeramicTex.wrapT=THREE.RepeatWrapping;
tableCeramicTex.repeat.set(17,8);tableCeramicTex.anisotropy=ren.capabilities.getMaxAnisotropy();
const tableBaseMat=std(0xd2d6d5,{roughness:.38,metalness:.05});
const tableTop=bx(17,.3,8,tableBaseMat,1.5,-.15,.3);
tableTop.receiveShadow=true;
// Keramik berada sedikit di atas struktur meja agar natnya jelas terlihat.
const tableSurface=new THREE.Mesh(new THREE.PlaneGeometry(17,8),new THREE.MeshStandardMaterial({map:tableCeramicTex,color:0xffffff,roughness:.3,metalness:.015}));
tableSurface.rotation.x=-Math.PI/2;tableSurface.position.set(1.5,.002,.3);tableSurface.receiveShadow=true;tableSurface.renderOrder=1;scene.add(tableSurface);
// Bingkai tepi meja berwarna metalik satin.
const tableEdge=std(0x9ea9ad,{roughness:.32,metalness:.55});
bx(17,.055,.055,tableEdge,1.5,-.125,-3.675);bx(17,.055,.055,tableEdge,1.5,-.125,4.275);
bx(.055,.055,8,tableEdge,-7,-.125,.3);bx(.055,.055,8,tableEdge,10,-.125,.3);
// Rangka dan kaki meja menghubungkan meja ke lantai, sehingga instrumen tidak tampak mengambang.
const tableLegMat=std(0x8c989e,{roughness:.42,metalness:.52});
[[-6.55,-3.35],[9.55,-3.35],[-6.55,3.95],[9.55,3.95]].forEach(([x,z])=>{
 bx(.18,1.0,.18,tableLegMat,x,-.5,z);
 bx(.3,.055,.3,0x717d83,x,-1.005,z);
});
// Apron tipis di bawah permukaan meja, dengan finishing netral.
bx(16.2,.22,.12,0x9ba6aa,1.5,-.36,-3.58);bx(16.2,.22,.12,0x9ba6aa,1.5,-.36,4.18);
bx(.12,.22,7.45,0x9ba6aa,-6.88,-.36,.3);bx(.12,.22,7.45,0x9ba6aa,9.88,-.36,.3);

// Ketika kamera melewati sisi dinding, lakukan cutaway pada dinding tersebut. Ini menghindari
// tombol kamera Belakang/Samping membuat tembok menutupi seluruh model instrumen.
function updateRoomVisibility(){
 const outsideBack=cam.position.z < -4.45;
 const outsideLeft=cam.position.x < -15.2;
 const outsideRight=cam.position.x > 15.2;
 rearRoomParts.forEach(o=>o.visible=!outsideBack);
 leftRoomParts.forEach(o=>o.visible=!outsideLeft);
 rightRoomParts.forEach(o=>o.visible=!outsideRight);
}
const cary=new THREE.Group();cary.position.set(-3.2,0,0);scene.add(cary);
const bumpT=canvasTex(768,768,(g)=>{const d=g.createImageData(768,768);for(let i=0;i<d.data.length;i+=4){const v=124+Math.random()*8;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0)});bumpT.wrapS=bumpT.wrapT=THREE.RepeatWrapping;bumpT.encoding=THREE.LinearEncoding;bumpT.anisotropy=ren.capabilities.getMaxAnisotropy();
const shW=new THREE.MeshPhysicalMaterial({color:0xf1f1ec,roughness:.29,metalness:.025,clearcoat:.8,clearcoatRoughness:.2,bumpMap:bumpT,bumpScale:.065,transparent:true});
const shD=new THREE.MeshPhysicalMaterial({color:0x34373b,roughness:.4,metalness:.14,clearcoat:.55,clearcoatRoughness:.25,bumpMap:bumpT,bumpScale:.06,transparent:true});
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
// Strip depan, trim logam halus, kisi ventilasi, dan sekrup casing beresolusi tinggi.
const instrumentTrim=std(0xb8c0c8,{metalness:.78,roughness:.24,clearcoat:.55});
bx(5.4,.22,.05,new THREE.MeshPhysicalMaterial({color:0x42474d,roughness:.32,metalness:.32,clearcoat:.65}),0,.12,2.21,cary);
bx(5.22,.018,.018,instrumentTrim,0,.265,2.232,cary);
for(let i=0;i<8;i++)bx(.72,.012,.012,0x22272c,1.48,.20+i*.035,2.235,cary);
for(let i=0;i<6;i++)bx(.34,.009,.012,0x181c21,-2.35,.30+i*.035,2.235,cary);
[[-2.48,.31],[2.48,.31],[-2.48,1.47],[2.48,1.47]].forEach(q=>{
 const screw=cy(.026,.012,instrumentTrim,q[0],q[1],2.238,cary,Math.PI/2,0);tag(screw,'body');
 const slot=bx(.025,.004,.004,0x353b42,q[0],q[1],2.247,cary);slot.rotation.z=.55;
});
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
const detectorSignalMat=std(0x8bdcff,{color:0x8bdcff,emissive:0x061c3c,transparent:true,opacity:.8,roughness:.2});
const detectorSignal=tag(sp(.105,detectorSignalMat,2.45,BY,.5,opt),'pmt');
// accessory controller, dinding kompartemen sampel, jendela kuarsa
tag(cy(.16,.7,darkM,-2.35,.64,1.6,opt,0,Math.PI/2),'accctl');tag(cy(.17,.05,gold,-2.0,.64,1.6,opt,0,Math.PI/2),'accctl');
[-.38,1.38].forEach(z=>tag(bx(1.76,.45,.03,steel,0,.74,z,opt),'liner'));
[.95,.05].forEach(z=>[-.86,.86].forEach(x=>tag(bx(.03,.22,.24,glassT(.35),x,BY,z,opt),'window')));
// berkas
const mk=()=>new THREE.MeshBasicMaterial({color:0xffb7ff,transparent:true,opacity:.85,blending:THREE.AdditiveBlending,depthTest:true,depthWrite:false});
// Jalur sebelum kisi (spektrum sumber), jalur sesudah kisi (satu panjang gelombang terpilih), dan dua jalur double-beam.
const mC=mk(),mMono=mk(),mS1=mk(),mS2=mk(),mR=mk(),mLV=mk(),mLD=mk();
const beamGlowMeshes=[];
function seg(a,b,m){
 const A=new THREE.Vector3(a[0],BY,a[1]),B=new THREE.Vector3(b[0],BY,b[1]);const L=A.distanceTo(B);const mid=A.clone().add(B).multiplyScalar(.5);const dir=B.clone().sub(A).normalize();
 const geom=new THREE.CylinderGeometry(.026,.026,L,20,1);const o=new THREE.Mesh(geom,m);o.position.copy(mid);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir);o.renderOrder=10;opt.add(o);
 const gm=new THREE.MeshBasicMaterial({color:m.color.clone(),transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthTest:true,depthWrite:false});const glow=new THREE.Mesh(new THREE.CylinderGeometry(.082,.082,L,20,1),gm);glow.position.copy(mid);glow.quaternion.copy(o.quaternion);glow.renderOrder=9;opt.add(glow);beamGlowMeshes.push({base:m,glow});return o;
}
for(let i=0;i<common.length-1;i++)seg(common[i],common[i+1],i<3?mC:mMono);seg([-2.6,-1.7],[-2.2,-1.7],mLV);seg([-2.2,-1.2],[-2.2,-1.7],mLD);
// Kipas dispersi ilustratif di kisi: seluruh warna berhenti di bidang pemilih, hanya λ terpilih dibuat terang.
const spectrumPalette=['#7c3aed','#9333ea','#4f46e5','#2563eb','#06b6d4','#22c55e','#f59e0b','#ef4444'];
const spectralFan=[];
spectrumPalette.forEach((hex,i)=>{const mat=new THREE.MeshBasicMaterial({color:hex,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthTest:true,depthWrite:false});seg([-1.9,-.6],[-1.25,-1.28+i*.185],mat);spectralFan.push({mat,index:i})});
for(let i=0;i<sampP.length-1;i++)seg(sampP[i],sampP[i+1],i<3?mS1:mS2);
for(let i=0;i<refP.length-1;i++)seg(refP[i],refP[i+1],mR);
function route(a){const p=common.concat(a.slice(1));const cum=[0];for(let i=1;i<p.length;i++)cum.push(cum[i-1]+Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]));return{p,cum,L:cum[cum.length-1]}}
const rS=route(sampP),rR=route(refP);const dCuv=rS.cum[common.length-1+3];
function posAt(r,u){u=u%r.L;let i=1;while(r.cum[i]<u)i++;const t=(u-r.cum[i-1])/(r.cum[i]-r.cum[i-1]);return[r.p[i-1][0]+(r.p[i][0]-r.p[i-1][0])*t,r.p[i-1][1]+(r.p[i][1]-r.p[i-1][1])*t]}
const pM=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:.96,blending:THREE.AdditiveBlending,depthTest:true,depthWrite:false});const pulses=[];
const glowT=canvasTex(128,128,(g)=>{const r=g.createRadialGradient(64,64,0,64,64,64);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.18,'rgba(255,255,255,.8)');r.addColorStop(.42,'rgba(255,255,255,.25)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,128,128)});
// tekstur lampu: INTI SOLID berwarna + lingkar cahaya tipis (bukan gradasi pudar)
const coreT=canvasTex(128,128,(g)=>{const r=g.createRadialGradient(64,64,0,64,64,64);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.40,'rgba(255,255,255,1)');r.addColorStop(.46,'rgba(255,255,255,.75)');r.addColorStop(.62,'rgba(255,255,255,.22)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,128,128)});
const halos=[];[[-2.6,-1.7,'lv',1.1],[-2.2,-1.2,'ld',1.0],[-1.9,-1.7,'c',.55],[-1.9,-.6,'c',.6],[-1.1,-1.1,'c',.55],[-1.1,.5,'c',.6],[-1.1,.95,'s1',.5],[1.5,.95,'s2',.5],[-1.1,.05,'r',.5],[1.5,.05,'r',.5],[2.3,.5,'p',.9],[0,.95,'s1',.4]].forEach(a=>{const lamp=a[2]==='lv'||a[2]==='ld';const m=new THREE.SpriteMaterial({map:lamp?coreT:glowT,color:0xff0000,transparent:true,blending:THREE.AdditiveBlending,depthTest:false,depthWrite:false});const s=new THREE.Sprite(m);s.scale.set(a[3],a[3],1);s.position.set(a[0],BY,a[1]);s.renderOrder=11;opt.add(s);halos.push({m,t:a[2],s,baseScale:a[3]})});
const preGratingLen=rS.cum[3],preChopperLen=rS.cum[common.length-1];
[rS,rR].forEach((r,k)=>{for(let i=0;i<14;i++){
 const mat=pM.clone();const s=sp(.038,mat,0,BY,0,opt);s.renderOrder=12;
 const gm=new THREE.SpriteMaterial({map:glowT,color:0xffffff,transparent:true,opacity:.72,blending:THREE.AdditiveBlending,depthTest:true,depthWrite:false});
 const glow=new THREE.Sprite(gm);glow.scale.set(.24,.24,1);glow.renderOrder=13;opt.add(glow);
 pulses.push({s,glow,mat,r,u:i*r.L/14,k});
}});
// ---------- UPS, PC, monitor, props
const ups=new THREE.Group();ups.position.set(.9,0,.2);scene.add(ups);
tag(rm(slabG(1.2,1.9,1.2,.12),0x16161a,0,.1,0,ups),'ups');bx(1.2,.14,1.9,0xc9a227,0,.07,0,ups);bx(1.2,.14,1.9,0xc9a227,0,1.37,0,ups);
const upsLed=[];for(let i=0;i<5;i++)upsLed.push(sp(.04,std(0x114411,{emissive:0}),-.2+i*.1,.6,.994,ups));
// Detail panel UPS: LCD, chassis seam, status LEDs, vents and fasteners.
const upsPanelMat=new THREE.MeshPhysicalMaterial({color:0x202831,roughness:.32,metalness:.22,clearcoat:.5});
bx(.62,.43,.028,upsPanelMat,-.055,.94,.982,ups);
const upsLCD=canvasTex(384,144,(g,w,h)=>{g.fillStyle='#061219';g.fillRect(0,0,w,h);g.strokeStyle='#2b7682';g.lineWidth=5;g.strokeRect(5,5,w-10,h-10);g.fillStyle='#80f4cf';g.font='bold 36px monospace';g.fillText('UPS ONLINE',18,47);g.font='28px monospace';g.fillText('230 V  |  50 Hz',18,88);g.fillStyle='#5fb99f';g.fillRect(18,108,Math.round((w-36)*.86),8)});
plane(.49,.18,upsLCD,-.055,.97,1.0,ups);
plane(.62,.105,txt(['ICA  •  POWER PROTECTION'],310,52,'#131a22','#d8c99c',18),-.055,.655,.994,ups);
tag(cy(.09,.05,0xd9e1e8,.35,1.0,.997,ups,Math.PI/2),'upsbtn');
for(let i=0;i<9;i++){bx(.38,.012,.012,0x090e13,-.055,.30+i*.025,.984,ups)}
[[-.32,.76],[.21,.76],[-.32,1.12],[.21,1.12]].forEach(p=>{cy(.013,.012,0xc5cbd0,p[0],p[1],1.001,ups,Math.PI/2,0)});
const folder=bx(1.1,.04,1.5,0x6fb3e0,0,1.46,0,ups);
const pcG=new THREE.Group();pcG.position.set(2.7,0,0);scene.add(pcG);
tag(rm(slabG(.95,2.1,1.9,.08),0x15151a,0,0,0,pcG),'pc');
// Front bezel and drive bay with a brushed-metal finish.
bx(.9,.75,.025,new THREE.MeshPhysicalMaterial({color:0x252b32,roughness:.3,metalness:.28,clearcoat:.5}),0,.45,1.072,pcG);
bx(.9,.22,.032,0x0a0a0a,0,1.55,1.075,pcG);
bx(.55,.016,.012,0x929da9,0,1.575,1.095,pcG);bx(.08,.026,.012,0x586575,.32,1.535,1.095,pcG);
tag(cy(.06,.04,0xdde5ed,-.25,1.2,1.085,pcG,Math.PI/2),'pcbtn');
for(let i=0;i<4;i++)bx(.058,.032,.018,0x070a0e,-.11+i*.085,1.2,1.09,pcG);
const pcLed=sp(.03,std(0x114411,{emissive:0}),-.1,1.2,1.105,pcG);plane(.3,.08,txt(['DELL'],180,48,'#737e89','#f2f4f6',18),0,.85,1.092,pcG);
// High-density horizontal air vents and side-panel perforations.
for(let i=0;i<12;i++)bx(.42,.009,.012,0x090d12,.17,.17+i*.035,1.091,pcG);
for(let i=0;i<5;i++){bx(.065,.028,.016,0x05080b,.12+i*.09,1.2,1.094,pcG)}
for(let i=0;i<8;i++)bx(.012,.58,.014,0x2d343d,.485,.43,-.52+i*.145,pcG);
[[-.39,.13],[.39,.13],[-.39,.77],[.39,.77]].forEach(p=>{cy(.012,.012,0x9fa8b2,p[0],p[1],1.092,pcG,Math.PI/2,0)});
bx(.9,.12,1.3,0xcc2b2b,0,1.96,0,pcG);
const mon=new THREE.Group();mon.position.set(5,0,-.6);scene.add(mon);
// Weighted stand and graphite bezel with a high-density 1024×600 display texture.
cy(.31,.065,new THREE.MeshPhysicalMaterial({color:0x1a1d22,roughness:.28,metalness:.3,clearcoat:.65}),0,.035,.08,mon,0,0).scale.set(1.48,1,1.05);
bx(.8,.06,.6,0x111111,0,.03,0,mon);bx(.15,.7,.12,new THREE.MeshPhysicalMaterial({color:0x272c33,roughness:.3,metalness:.35}),0,.4,0,mon);
tag(bx(2.7,1.55,.1,new THREE.MeshPhysicalMaterial({color:0x101318,roughness:.26,metalness:.28,clearcoat:.75,clearcoatRoughness:.2}),0,1.3,0,mon),'monbody');
const bezelTex=canvasTex(32,32,(g,w,h)=>{g.fillStyle='#11161d';g.fillRect(0,0,w,h);g.strokeStyle='#333b45';g.lineWidth=2;g.strokeRect(1,1,w-2,h-2)});
plane(2.57,1.49,bezelTex,0,1.3,.054,mon);
const scrC=document.createElement('canvas');scrC.width=1024;scrC.height=600;const scrT=new THREE.CanvasTexture(scrC);scrT.encoding=THREE.sRGBEncoding;scrT.anisotropy=ren.capabilities.getMaxAnisotropy();scrT.minFilter=THREE.LinearMipmapLinearFilter;scrT.magFilter=THREE.LinearFilter;scrT.generateMipmaps=true;
const scr=plane(2.5,1.46,scrT,0,1.3,.058,mon);tag(scr,'screen');
const glareT=canvasTex(512,300,(g,w,h)=>{g.clearRect(0,0,w,h);const gr=g.createLinearGradient(0,0,w*.65,h);gr.addColorStop(0,'rgba(255,255,255,.13)');gr.addColorStop(.35,'rgba(255,255,255,.035)');gr.addColorStop(.7,'rgba(255,255,255,0)');gr.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gr;g.beginPath();g.moveTo(0,0);g.lineTo(w*.3,0);g.lineTo(w,h);g.lineTo(w*.72,h);g.closePath();g.fill()});
const screenGlare=new THREE.Mesh(new THREE.PlaneGeometry(2.5,1.46),new THREE.MeshBasicMaterial({map:glareT,transparent:true,opacity:.58,depthWrite:false}));screenGlare.position.set(0,1.3,.060);mon.add(screenGlare);
plane(.34,.055,txt(['DELL'],160,32,'#11161d','#aeb9c5',14),-.22,.555,.061,mon);
for(let i=0;i<18;i++){const x=-.75+i*.09;bx(.018,.008,.008,0x343b43,x,.57,.0615,mon)}
tag(cy(.05,.03,0x333b44,1.1,.58,.062,mon,Math.PI/2),'monbtn');const monLed=sp(.025,std(0x114411,{emissive:0}),.95,.58,.067,mon);
[[-1.28,.61],[1.28,.61],[-1.28,1.99],[1.28,1.99]].forEach(p=>{cy(.012,.01,0x747e89,p[0],p[1],.061,mon,Math.PI/2,0)});
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
chop:['Chopper ganda','Pada Cary 100, chopper memodulasi jalur sampel dan referensi bergiliran menuju detektor. Garis kedua jalur tetap digambar untuk membantu melihat geometri optik, sedangkan partikel foton menunjukkan urutan waktunya. Animasi diperlambat.'],pmt:['Detektor PMT','Photomultiplier tube mengubah intensitas cahaya menjadi sinyal listrik. Absorbansi A = −log10(I/I0).'],
ups:['UPS (ICA)','Melindungi komputer dan instrumen dari mati listrik dan lonjakan tegangan. Nyalakan PERTAMA, matikan TERAKHIR.'],upsbtn:['Tombol power UPS','Klik untuk ON/OFF. LED hijau menyala bertahap menandakan UPS aktif.'],
pc:['Komputer Dell OptiPlex 7010','Menjalankan Cary WinUV dan mengontrol instrumen.'],pcbtn:['Tombol power komputer','Klik untuk ON/OFF. Nyalakan setelah UPS dan instrumen.'],monbody:['Monitor Dell','Menampilkan Windows 7 dan aplikasi Cary WinUV.'],monbtn:['Tombol power monitor','Nyalakan setelah komputer.'],screen:['Layar monitor','Saat desktop tampil, klik untuk membuka Cary WinUV.'],kbd:['Keyboard','Input aplikasi.'],mouse:['Mouse dan mousepad','Navigasi aplikasi.'],kim:['Kimtech Kimwipes','Tisu bebas serat untuk membersihkan sisi bening kuvet. Jangan menggosok keras.']};
function showInfo(k){const i=INFO[k];if(!i)return;ensureInfoPanelVisible();$('it').textContent=i[0];$('ix').textContent=i[1]}
function showIdentifyGuide(){ensureInfoPanelVisible();$('it').textContent='Mode Kenali Bagian Aktif';$('ix').textContent='Klik label nama komponen pada model 3D, atau klik langsung bagian alat. Nama dan fungsi komponen akan dijelaskan di panel ini tanpa menutupi area instrumen.'}
function ensureInfoPanelVisible(){if(document.body.classList.contains('hp')){document.body.classList.remove('hp');document.body.classList.add('left-hidden')}document.body.classList.remove('right-hidden');if(typeof updatePanelToggleUI==='function')updatePanelToggleUI()}
// ---------- daya
const ORDER=[['ups','UPS'],['inst','instrumen'],['pc','komputer'],['mon','monitor']];
function power(k){if(S.job){toast('Tunggu pengukuran selesai.');return}
 const i=ORDER.findIndex(o=>o[0]===k);
 if(!S[k]){for(let j=0;j<i;j++)if(!S[ORDER[j][0]]){toast('Nyalakan '+ORDER[j][1]+' terlebih dahulu.');return}S[k]=1;if(k==='inst'){S.warm=0}if(k==='pc'){S.bootT=0}}
 else{for(let j=ORDER.length-1;j>i;j--)if(S[ORDER[j][0]]){toast('Matikan '+ORDER[j][1]+' lebih dulu (urutan kebalikan).');return}
  if(S.app){toast('Tutup aplikasi Cary WinUV terlebih dahulu.');return}
  S[k]=0;if(k==='inst'){S.warm=0;S.base=0}if(k==='pc'){S.booted=0}}}
const desk=()=>S.mon&&S.pc&&S.booted;
function openApp(on){
 if(on&&!desk()){toast('Aplikasi hanya bisa dibuka setelah komputer dan monitor menyala & Windows siap.');return}
 if(!on&&(S.job||S.batchMeasuring)){toast('Pengukuran masih berlangsung. Minimalkan jendela untuk melihat animasi 3D tanpa menghentikan pengukuran.');return}
 S.app=on?1:0;S.appMinimized=0;$('app').hidden=!on;drawScreen();
}
function minimizeApp(){if(!S.app)return;S.appMinimized=1;$('app').hidden=true;drawScreen();renderUI();toast('Cary WinUV diminimalkan. Animasi proses optik tetap berjalan. Tekan “Kembalikan Cary WinUV” untuk kembali ke pengukuran.')}
function toggleLid(){if(S.job){toast('Tunggu pengukuran selesai.');return}S.lid=S.lid?0:1}
function toggleCuv(){if(S.job){toast('Tunggu pengukuran selesai.');return}if(!S.lid){toast('Buka tutup kompartemen sampel dulu.');return}S.cuv=S.cuv?0:1}
// ---------- layar monitor
let lastScr='';
function drawScreen(){
 const baseState=!S.mon?'off':!S.pc?'nosig':!S.booted?'boot':'desk'+(S.app&&!S.appMinimized);
 const st=(S.app&&!S.appMinimized&&baseState.startsWith('desk'))?baseState+':'+(S.paused?'PAUSED':(S.job||S.batchMeasuring)?'MEASURING':'READY')+':'+Math.round(S.lam)+':'+(S.base?'ZERO':'NOZERO'):baseState;
 if(st===lastScr)return;lastScr=st;
 const g=scrC.getContext('2d'),w=512,h=300;g.setTransform(2,0,0,2,0,0);g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high';
 g.clearRect(0,0,w,h);
 if(st==='off'){
  g.fillStyle='#03060a';g.fillRect(0,0,w,h);
  const offGlow=g.createRadialGradient(250,150,5,250,150,190);offGlow.addColorStop(0,'#111821');offGlow.addColorStop(1,'#03060a');g.fillStyle=offGlow;g.fillRect(0,0,w,h);
 }else if(st==='nosig'){
  const grad=g.createLinearGradient(0,0,w,h);grad.addColorStop(0,'#071329');grad.addColorStop(1,'#123c62');g.fillStyle=grad;g.fillRect(0,0,w,h);
  g.strokeStyle='#23506f';g.lineWidth=1;for(let x=0;x<w;x+=24){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}for(let y=0;y<h;y+=24){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke()}
  g.fillStyle='#eaf5ff';g.textAlign='center';g.font='600 18px Segoe UI,Arial';g.fillText('NO SIGNAL',w/2,h/2-2);g.font='10px Segoe UI,Arial';g.fillStyle='#9ab7ce';g.fillText('Periksa kabel display dan komputer',w/2,h/2+18);g.textAlign='left';
 }else if(st==='boot'){
  const bg=g.createLinearGradient(0,0,0,h);bg.addColorStop(0,'#020711');bg.addColorStop(1,'#071c32');g.fillStyle=bg;g.fillRect(0,0,w,h);
  g.save();g.translate(w/2,94);for(let i=0;i<12;i++){const a=i*Math.PI/6+(S.visualTime||0)*.35;g.fillStyle=`rgba(103,205,255,${.22+i*.06})`;g.beginPath();g.arc(Math.cos(a)*22,Math.sin(a)*22,2.3,0,Math.PI*2);g.fill()}g.restore();
  g.fillStyle='#edf7ff';g.textAlign='center';g.font='500 15px Segoe UI,Arial';g.fillText('Memulai Windows',w/2,142);g.fillStyle='#91aeca';g.font='10px Segoe UI,Arial';g.fillText('Menyiapkan lingkungan instrumen...',w/2,160);g.textAlign='left';
 }else{
  const bg=g.createLinearGradient(0,0,w,h);bg.addColorStop(0,'#0b2741');bg.addColorStop(.55,'#15506c');bg.addColorStop(1,'#071a33');g.fillStyle=bg;g.fillRect(0,0,w,h);
  const glow=g.createRadialGradient(390,44,0,390,44,180);glow.addColorStop(0,'rgba(69,199,223,.28)');glow.addColorStop(1,'rgba(69,199,223,0)');g.fillStyle=glow;g.fillRect(0,0,w,h);
  // Desktop shortcut icons with high-resolution labels.
  const icons=[['PC','#9fc5de'],['Recycle','#91a6bd'],['Cary WinUV','#49d4b1'],['Simple Reads','#72a9ff'],['Concentration','#e8be67'],['Scan','#ae92ff']];
  icons.forEach((it,i)=>{const col=i<3?0:1,row=i%3,x=12+col*72,y=12+row*49;g.fillStyle='rgba(2,13,24,.22)';g.fillRect(x+3,y+3,31,28);const ig=g.createLinearGradient(x,y,x+28,y+25);ig.addColorStop(0,'#f7fbff');ig.addColorStop(1,it[1]);g.fillStyle=ig;g.fillRect(x,y,27,24);g.strokeStyle='#e1f1fb';g.lineWidth=.7;g.strokeRect(x+.5,y+.5,26,23);g.fillStyle='#112538';g.font='bold 8px Segoe UI,Arial';g.fillText(it[0]==='PC'?'PC':it[0]==='Recycle'?'♻':it[0]==='Cary WinUV'?'UV':it[0]==='Simple Reads'?'SR':it[0]==='Concentration'?'C':'λ',x+8,y+15);g.fillStyle='#f4f8ff';g.font='8px Segoe UI,Arial';g.fillText(it[0],x-1,y+35)});
  // Bottom desktop taskbar.
  g.fillStyle='rgba(4,13,24,.93)';g.fillRect(0,278,w,22);g.fillStyle='#2f9be8';g.fillRect(0,278,5,22);g.fillStyle='#f0f6fc';g.beginPath();g.arc(14,289,5,0,Math.PI*2);g.fill();g.fillStyle='#75bbeb';g.font='9px Segoe UI,Arial';g.fillText('Cari aplikasi',25,292);g.fillStyle='#8ea8bf';g.fillText('Wi-Fi   ▪   100%',w-82,292);
  if(S.app&&!S.appMinimized){
   const x=70,y=27,ww=428,hh=247;
   g.fillStyle='rgba(0,0,0,.42)';g.fillRect(x+4,y+5,ww,hh);
   g.fillStyle='#edf1f7';g.fillRect(x,y,ww,hh);g.strokeStyle='#70859e';g.strokeRect(x+.5,y+.5,ww-1,hh-1);
   const title=g.createLinearGradient(x,y,x,y+20);title.addColorStop(0,'#2b72c8');title.addColorStop(1,'#16498f');g.fillStyle=title;g.fillRect(x,y,ww,20);
   g.fillStyle='#fff';g.font='bold 10px Segoe UI,Arial';g.fillText('Agilent Cary WinUV  |  UV-Visible Spectroscopy',x+8,y+13);
   g.fillStyle='#e8edf5';g.fillRect(x,y+20,ww,18);g.fillStyle='#263a50';g.font='9px Segoe UI,Arial';g.fillText('File   Method   Instrument   Configure   Reports   Help',x+8,y+32);
   const tabs=[['Scan',0],['Simple Reads',1],['Concentration',2]];tabs.forEach(([label,i])=>{const tx=x+8+i*88;g.fillStyle=S.tab===(['scan','simple','conc'][i])?'#d5e6fb':'#f0f2f4';g.fillRect(tx,y+42,84,19);g.strokeStyle='#acb8c8';g.strokeRect(tx+.5,y+42.5,83,18);g.fillStyle='#203d60';g.font='bold 8px Segoe UI,Arial';g.fillText(label,tx+6,y+54)});
   // Plot area and axes inside the simulated app.
   const gx=x+14,gy=y+69,gw=ww-30,gh=118;g.fillStyle='#fff';g.fillRect(gx,gy,gw,gh);g.strokeStyle='#c6d2df';g.lineWidth=.5;
   for(let i=0;i<=5;i++){const xx=gx+i*gw/5,yy=gy+i*gh/5;g.beginPath();g.moveTo(xx,gy);g.lineTo(xx,gy+gh);g.moveTo(gx,yy);g.lineTo(gx+gw,yy);g.stroke()}
   g.strokeStyle='#1b5fab';g.lineWidth=1.8;g.beginPath();for(let i=0;i<=90;i++){const t=i/90,nm=200+200*t;const signal=.04+.8*Math.exp(-.5*Math.pow((nm-246)/18,2))+.12*Math.exp(-.5*Math.pow((nm-205)/12,2));const px=gx+t*gw,py=gy+gh-(signal*gh);if(i===0)g.moveTo(px,py);else g.lineTo(px,py)}g.stroke();
   g.fillStyle='#243a54';g.font='8px Segoe UI,Arial';g.fillText('Absorbansi (AU)',gx+5,gy+10);g.fillText('200',gx-1,gy+gh+9);g.fillText('400',gx+gw-16,gy+gh+9);g.fillText('Panjang gelombang (nm)',gx+gw/2-50,gy+gh+21);
   g.fillStyle='#dfe8f0';g.fillRect(x+8,y+221,ww-16,18);g.fillStyle='#20364b';g.font='8px Segoe UI,Arial';g.fillText('Status: '+(S.paused?'PAUSED':S.job?'MEASURING':'READY')+'   |   λ = '+Number(S.lam).toFixed(1)+' nm   |   Zero Blank: '+(S.base?'OK':'belum'),x+14,y+233);
  }
 }
 scrT.needsUpdate=true;
}
// ---------- pengukuran
function pre(){if(!desk())return'Komputer/monitor belum siap.';if(!S.inst)return'Instrumen belum menyala.';if(S.warm<WARM)return'Warm-up belum selesai.';if(S.lid)return'Tutup kompartemen sampel harus tertutup.';if(!S.cuv)return'Letakkan kuvet di holder sampel.';return''}
function range(){const a=+$('s0').value,b=+$('s1').value;if(!(a>=190&&a<=900&&b>=190&&b<=900&&a>b)){toast('Masukkan λ awal lebih besar daripada λ akhir, dalam rentang 190–900 nm (contoh 400 ke 200).');return null}return[a,b]}
function syncProcessButtons(){const b=$('bPause');if(b){const running=!!(S.job||S.batchMeasuring);b.disabled=false;b.textContent=S.paused?(running?'Lanjutkan proses':'Lanjutkan animasi'):(running?'Jeda proses':'Jeda animasi');b.title=S.paused?'Lanjutkan animasi/proses':(running?'Jeda pengukuran dan animasi':'Jeda animasi visual');b.classList.toggle('on',!!S.paused)}const i=$('bIdentify');if(i){i.classList.toggle('on',!!S.identifyMode);i.textContent=S.identifyMode?'Tutup Kenali Bagian':'Kenali Bagian'}}
function enterAnimationFocus(){
 if(S.focusRestore)return;
 S.focusRestore={
  app:S.app,appMinimized:S.appMinimized,appHidden:$('app').hidden,appDisplay:$('app').style.display,
  panelClasses:['hp','left-hidden','right-hidden'].filter(c=>document.body.classList.contains(c)),
  xray:S.xray,lbl:S.lbl,identifyMode:S.identifyMode,measureVisual:S.measureVisual,
  menuHidden:$('menuDrop').hidden,howtoHidden:$('howtoBackdrop').hidden
 };
 S.identifyMode=0;S.lbl=0;S.xray=0;
 document.body.classList.add('focus-animation');
 $('animationFocusHud').hidden=false;
 // Cary WinUV disembunyikan dari layar dan dari modal, namun statusnya disimpan untuk dipulihkan.
 S.appMinimized=1;$('app').hidden=true;$('app').style.display='none';$('menuDrop').hidden=true;$('howtoBackdrop').hidden=true;
 $('bL').classList.remove('on');$('bX').classList.remove('on');
 syncX();syncAnimationFocusHUD();drawScreen();
 if(typeof resize==='function')requestAnimationFrame(()=>resize());
}
function exitAnimationFocus(){
 const r=S.focusRestore;if(!r)return;
 document.body.classList.remove('focus-animation','hp','left-hidden','right-hidden');
 (r.panelClasses||[]).forEach(c=>document.body.classList.add(c));
 S.app=r.app;S.appMinimized=r.appMinimized;S.xray=r.xray;S.lbl=r.lbl;S.identifyMode=r.identifyMode;S.measureVisual=r.measureVisual;
 $('app').hidden=r.appHidden;$('app').style.display=r.appDisplay||'';$('menuDrop').hidden=r.menuHidden;$('howtoBackdrop').hidden=r.howtoHidden;
 $('animationFocusHud').hidden=true;S.focusRestore=null;
 $('bL').classList.toggle('on',!!S.lbl);$('bX').classList.toggle('on',!!(S.xray||S.identifyMode||S.measureVisual));
 syncX();syncProcessButtons();updatePanelToggleUI();drawScreen();
 if(typeof resize==='function')requestAnimationFrame(()=>resize());
}
function syncAnimationFocusHUD(){
 const hud=$('animationFocusHud');if(!hud)return;
 const running=!!(S.job||S.batchMeasuring);hud.hidden=!S.focusRestore;
 if(!S.focusRestore)return;
 let title='Proses optik berlangsung',detail='Panel dan tabel disembunyikan agar animasi instrumen terlihat penuh.';
 const j=S.job;
 if(S.paused){title='Proses dijeda';detail='Animasi dan waktu pengukuran berhenti. Lanjutkan untuk menyelesaikan pembacaan.'}
 else if(j&&j.type==='base'){title='Zero Blank dengan aquades';detail='Instrumen sedang membaca blanko untuk menetapkan referensi dasar.'}
 else if(j&&j.type==='scan'){title='Scan panjang gelombang · standar 25 ppm';detail='Monokromator sedang memindai '+j.start.toFixed(0)+'–'+j.stop.toFixed(0)+' nm; grafik diurutkan 200 nm di kiri ke 400 nm di kanan. λ saat ini '+S.lam.toFixed(1)+' nm.'}
 else if(j&&j.type==='simple'){title='Simple Reads · '+(j.solutionLabel||'Larutan');detail='Pembacaan replikasi '+Math.min(j.i+1,j.n)+' dari '+j.n+' pada λ '+j.l.toFixed(1)+' nm.'}
 else if(j&&j.type==='read'){title='Pengukuran konsentrasi';detail='Pembacaan absorbansi sedang berlangsung pada λ '+j.l.toFixed(1)+' nm.'}
 else if(S.batchMeasuring){title='Pengukuran deret standar 0–25 ppm';detail='Setiap standar diukur berurutan. Tabel dan panel akan kembali setelah seluruh standar selesai.'}
 $('focusProcessName').textContent=title;$('focusProcessDetail').textContent=detail;
 $('focusPause').textContent=S.paused?'Lanjutkan':'Jeda';$('focusPause').disabled=!running&&!S.paused;
 $('focusStop').disabled=!running;$('focusIdentify').disabled=!running;
}
function syncAnimationFocus(){
 const running=!!(S.job||S.batchMeasuring);
 // Safety net: every active measurement must hide Cary WinUV, even if a measurement path bypasses startJob.
 if(running&&!S.focusRestore)enterAnimationFocus();
 if(S.focusRestore&&!running)exitAnimationFocus();
 else if(S.focusRestore)syncAnimationFocusHUD();
}
function startJob(job){enterAnimationFocus();S.identifyMode=0;S.lbl=0;S.xray=0;$('bL').classList.remove('on');$('bX').classList.remove('on');S.job=job;S.measureVisual=1;S.paused=0;syncX();syncProcessButtons();syncAnimationFocusHUD()}
function finishJob(){S.job=null;S.paused=0;S.measureVisual=!!S.batchMeasuring;syncX();syncProcessButtons()}
function startBase(){if(S.base){toast('Zero Blank sudah berhasil dilakukan. Proses ini hanya dilakukan satu kali per sesi.');return}const e=pre();if(e){toast(e);return}if($('smp').value!=='aquades'){toast('Pilih Aquades sebagai larutan kerja untuk Zero Blank.');return}setSample('blank');startJob({type:'base',l:S.lam,stop:S.lam,rate:0,t:0})}
function start(){if(S.job||S.batchMeasuring){toast('Pengukuran sedang berjalan. Jeda atau hentikan sebelum memulai proses baru.');return}if(S.tab==='conc'){toast('Gunakan tombol Ukur / Ukur semua standar / Ukur sampel.');return}if(S.tab==='scan'){const e=pre();if(e){toast(e);return}if(!S.base){toast('Belum melakukan Zero Blank. Pilih aquades lalu tekan Zero Blank (Aquades).');return}if(S.solutionKey!=='std_25'||S.sample!=='std'||Number(S.conc)!==25){toast('Scan panjang gelombang hanya dapat dilakukan menggunakan Standar 25 ppm.');return}const r=range();if(!r)return;S.res={type:'scan',pts:[]};S.lmax=null;startJob({type:'scan',l:r[0],start:r[0],stop:r[1],rate:(r[1]-r[0])/20,last:r[0]+1,pts:S.res.pts});}
 else{const e=pre();if(e){toast(e);return}if(!S.base){toast('Belum melakukan Zero Blank. Pilih aquades lalu tekan Zero Blank (Aquades).');return}const l=+$('sl').value,n=Math.max(1,Math.min(10,+$('sn').value|0));if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return}S.lam=l;const selected=$('smp').options[$('smp').selectedIndex];const key=S.solutionKey||'aquades';const isWeightTest=key.startsWith('pres_')||key.startsWith('akurasi_');const weight=isWeightTest?testWeightForKey(key):null;const concentration=key.startsWith('std_')?Number(key.split('_')[1]):(isWeightTest?nominalTestConcentrationPPM(key):null);const prepVolumeMl=isWeightTest?testVolumeMl():null,prepDilutionFactor=isWeightTest?testDilutionFactor():null;S.res={type:'simple',rows:[]};startJob({type:'simple',l,n,i:0,t:0,solutionKey:key,solutionLabel:selected?selected.textContent.trim():key,concentration,weight,prepVolumeMl,prepDilutionFactor});}
 if(S.job&&!S.camOpt){S.camOpt=1;flyV('opt')}}
function setAbsorbanceValue(id,value,sourceText){
 const input=$(id);if(!input)return;S.isAutoFillingAbs=true;input.value=Number(value).toFixed(4);S.isAutoFillingAbs=false;
 if(id==='aU'){S.autoAbsKey=S.solutionKey||null;if($('sampleAbsSource'))$('sampleAbsSource').textContent=sourceText||'Absorbansi terisi otomatis. Nilai tetap bisa diedit manual.';}
 if(id==='aSp'&&$('spikeAbsSource'))$('spikeAbsSource').textContent=sourceText||'Absorbansi sampel + spike terisi otomatis. Nilai tetap bisa diedit manual.';
}
function invalidateAutoAbsorbance(reason){if(S.autoAbsKey&&$('aU')){$('aU').value='';S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent=reason||'Larutan atau preparasi berubah. Ukur ulang, atau masukkan absorbansi manual yang sesuai.';renderRes();}}
function applyLastSimpleRead(){
 const r=S.lastSampleRead;if(!r||!Number.isFinite(r.absorbance)){toast('Belum ada hasil pembacaan sampel yang bisa dipindahkan.');return}
 if(S.solutionKey!==r.key&&Array.from($('smp').options).some(o=>o.value===r.key)){$('smp').value=r.key;$('smp').dispatchEvent(new Event('change',{bubbles:true}));}
 if(r.key==='spike'){
  setAbsorbanceValue('aSp',r.absorbance,'Terisi otomatis dari Simple Reads: '+r.solution+' (rata-rata '+r.replicates+' replikasi). Nilai ini tetap bisa diedit manual.');
 }else if(r.key==='unk'||r.key.startsWith('pres_')||r.key.startsWith('akurasi_')){
  setAbsorbanceValue('aU',r.absorbance,'Terisi otomatis dari Simple Reads: '+r.solution+' (rata-rata '+r.replicates+' replikasi). Nilai ini tetap bisa diedit manual.');
 }else{toast('Pembacaan terakhir adalah '+r.solution+', bukan sampel atau sampel + spike.');return}
 if(S.tab!=='conc')switchToTab('conc');else renderConc();renderRes();toast('Absorbansi berhasil dipindahkan ke Concentration. Kamu masih bisa mengedit nilainya.');
}
function runJob(dt){const j=S.job;if(!j||S.paused)return;
 if(j.type==='read'){j.t+=dt;if(j.t>=1.65){j.t=0;j.vals.push(readA(j.l));if(j.vals.length>=j.n){finishJob();j.cb(j.vals)}}}
 else if(j.type==='base'){j.t=(j.t||0)+dt;S.lam=j.l;if(j.t>=1.4){S.base=1;finishJob();S.solutionKey='aquades';setSample('blank');updateSolutionGate();toast('Zero Blank aquades berhasil. Larutan lain kini dapat dipilih; Zero Blank tidak dapat diulang pada sesi ini.')}}
 else if(j.type==='scan'){const next=j.l+j.rate*dt;j.l=j.rate>=0?Math.min(j.stop,next):Math.max(j.stop,next);S.lam=j.l;if(Math.abs(j.l-j.last)>=1){j.last=j.l;j.pts.push([j.l,readA(j.l)])}
  const reached=j.rate>=0?j.l>=j.stop:j.l<=j.stop;if(reached){finishJob();toast('Scan selesai. λmax acuan data = '+DATA_LMAX_NM.toFixed(1)+' nm.')}}
 else{j.t+=dt;if(j.t>=1.8){j.t=0;const a=readA(j.l),pct=100*Math.pow(10,-a);j.i++;S.res.rows.push([j.i,j.l,a,pct]);S.simpleHistory.push({no:S.simpleHistory.length+1,solution:j.solutionLabel||j.solutionKey||'Larutan',key:j.solutionKey||'',concentration:j.concentration,weight:j.weight,prepVolumeMl:j.prepVolumeMl,prepDilutionFactor:j.prepDilutionFactor,replicate:j.i,lambda:j.l,abs:a,transmittance:pct});drawTable();if(j.i>=j.n){
  const measuredRows=S.simpleHistory.slice(-j.n),avgAbs=measuredRows.reduce((sum,row)=>sum+row.abs,0)/Math.max(1,measuredRows.length);
  S.lastSampleRead={key:j.solutionKey||'',solution:j.solutionLabel||j.solutionKey||'Larutan',absorbance:avgAbs,replicates:measuredRows.length,concentration:j.concentration,weight:j.weight,prepVolumeMl:j.prepVolumeMl,prepDilutionFactor:j.prepDilutionFactor,lambda:j.l};
  finishJob();
  const k=S.lastSampleRead.key;
  if(k==='unk'||k.startsWith('pres_')||k.startsWith('akurasi_')){
   setAbsorbanceValue('aU',avgAbs,'Terisi otomatis dari Simple Reads: '+S.lastSampleRead.solution+' (rata-rata '+measuredRows.length+' replikasi). Kamu tetap bisa mengedit nilai ini secara manual.');
   switchToTab('conc');renderConc();toast('Sampel terbaca. Absorbansi rata-rata '+avgAbs.toFixed(4)+' otomatis dikirim ke Concentration.');
  }else if(k==='spike'){
   setAbsorbanceValue('aSp',avgAbs,'Terisi otomatis dari Simple Reads: '+S.lastSampleRead.solution+' (rata-rata '+measuredRows.length+' replikasi). Kamu tetap bisa mengedit nilai ini secara manual.');
   switchToTab('conc');renderConc();toast('Sampel + spike terbaca. Absorbansi rata-rata '+avgAbs.toFixed(4)+' otomatis dikirim ke Concentration.');
  }else toast('Simple Reads selesai. Hasil ditambahkan ke riwayat tabel.');
 }}}}
// ---------- λ maks (puncak spektrum, dihaluskan + interpolasi parabola)
function lmaxOf(p){if(!p||p.length<5)return null;const n=p.length,sm=p.map((q,i)=>{let s=0,c=0;for(let k=-2;k<=2;k++){const j=i+k;if(j>=0&&j<n){s+=p[j][1];c++}}return s/c});
 let k=0;sm.forEach((v,i)=>{if(v>sm[k])k=i});let l=p[k][0],a=sm[k];
 if(k>0&&k<n-1){const y0=sm[k-1],y1=sm[k],y2=sm[k+1],d=y0-2*y1+y2;if(d<0){const off=.5*(y0-y2)/d;if(Math.abs(off)<=1){l=p[k][0]+off*(p[k+1][0]-p[k][0]);a=y1-.25*(y0-y2)*off}}}
 return{l,a}}
function drawChart(){
 if(S.tab==='conc')return drawCal();
 const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;
 g.fillStyle='#fff';g.fillRect(0,0,w,h);g.strokeStyle='#999';g.fillStyle='#333';g.font='11px sans-serif';
 const r=S.res;
 if(!r||r.type!=='scan'||!r.pts.length){
  g.fillText(S.tab==='scan'?'Spektrum akan tampil di sini (200 nm di kiri; 400 nm di kanan)':'Hasil Simple Reads di tabel',10,20);
  if(S.tab==='scan')$('scanRes').innerHTML='λmax belum ada. Jalankan Scan setelah Zero Blank.';
  return;
 }
 const startNm=+$('s0').value,stopNm=+$('s1').value;
 const lo=Math.min(startNm,stopNm),hi=Math.max(startNm,stopNm),span=Math.max(1,hi-lo);
 const x0=52,x1=w-18,y0=20,y1=h-44;
 const X=l=>x0+(l-lo)/span*(x1-x0);
 const ym=Math.max(1,Math.max(...r.pts.map(p=>p[1]))*1.15);
 const Y=v=>y1-v/ym*(y1-y0);
 g.strokeStyle='#999';g.lineWidth=1;g.strokeRect(x0,y0,x1-x0,y1-y0);
 for(let i=0;i<=5;i++){
  const wl=lo+span*i/5,x=X(wl),abs=ym*i/5,y=Y(abs);
  g.strokeStyle='#e4e8ed';g.lineWidth=.7;g.beginPath();g.moveTo(x,y0);g.lineTo(x,y1);g.moveTo(x0,y);g.lineTo(x1,y);g.stroke();
  g.fillStyle='#333';g.textAlign='center';g.fillText(wl.toFixed(0),x,y1+14);g.textAlign='right';g.fillText(abs.toFixed(2),x0-7,y+4);
 }
 g.fillStyle='#333';g.textAlign='center';g.font='11px sans-serif';g.fillText('Panjang gelombang (nm)',(x0+x1)/2,h-7);
 g.save();g.translate(14,(y0+y1)/2);g.rotate(-Math.PI/2);g.textAlign='center';g.fillText('Absorbansi (AU)',0,0);g.restore();
 g.textAlign='right';g.font='10px sans-serif';g.fillText('200 → 400 nm',x1,y0-5);g.textAlign='left';
 // Acquisition can be 400 -> 200, but the plotted line is sorted to display 200 -> 400.
 const pts=[...r.pts].sort((p,q)=>p[0]-q[0]);
 g.strokeStyle='#c00';g.lineWidth=1.8;g.beginPath();pts.forEach((p,i)=>i?g.lineTo(X(p[0]),Y(p[1])):g.moveTo(X(p[0]),Y(p[1])));g.stroke();g.lineWidth=1;
 let m=null;
 if(!S.job&&pts.length>=5){let near=pts[0];for(const p of pts){if(Math.abs(p[0]-DATA_LMAX_NM)<Math.abs(near[0]-DATA_LMAX_NM))near=p}m={l:DATA_LMAX_NM,a:near[1]};S.lmax=m}
 if(S.job){$('scanRes').innerHTML='<b>Pemindaian berlangsung.</b> Akuisisi berjalan sesuai urutan alat, grafik ditampilkan dari 200 nm ke 400 nm.'}
 else if(m){
  g.setLineDash([4,4]);g.strokeStyle='#1565c0';g.beginPath();g.moveTo(X(m.l),y0);g.lineTo(X(m.l),y1);g.stroke();g.setLineDash([]);
  g.fillStyle='#d32f2f';g.beginPath();g.arc(X(m.l),Y(m.a),4.5,0,Math.PI*2);g.fill();
  g.fillStyle='#1565c0';g.font='bold 10px sans-serif';g.textAlign='left';
  const labelX=Math.min(X(m.l)+8,x1-185);const labelY=Math.max(y0+12,Y(m.a)-8);
  g.fillText('λmax data '+m.l.toFixed(1)+' nm, A='+m.a.toFixed(3),labelX,labelY);
  $('scanRes').innerHTML='<b>λmax acuan = '+DATA_LMAX_NM.toFixed(1)+' nm</b>, absorbansi sekitar '+m.a.toFixed(3)+'. Nilai ini acuan simulasi; sesuaikan dengan data praktikum.';
 }
}
function drawTable(){const rows=S.simpleHistory||[];if(!rows.length){$('tbl').innerHTML='<p class="cap" style="color:#444">Belum ada hasil. Pilih larutan kerja lalu jalankan Simple Reads; setiap pembacaan akan ditambahkan di sini.</p>';return}let t='<table><tr><th>#</th><th>Larutan kerja</th><th>Konsentrasi (ppm)</th><th>Replikat</th><th>λ (nm)</th><th>Abs</th><th>%T</th><th>Bobot (g)</th></tr>';rows.forEach(x=>{const conc=x.concentration==null?'—':x.concentration;const weight=x.weight==null?'—':Number(x.weight).toFixed(4);t+=`<tr><td>${x.no}</td><td style="text-align:left">${x.solution}</td><td>${conc}</td><td>${x.replicate}</td><td>${x.lambda.toFixed(1)}</td><td>${x.abs.toFixed(4)}</td><td>${x.transmittance.toFixed(2)}</td><td>${weight}</td></tr>`});$('tbl').innerHTML=t+'</table>'}
function csv(){if(S.tab==='simple'){const rows=S.simpleHistory||[];if(!rows.length){toast('Belum ada hasil Simple Reads untuk diekspor.');return}const q=v=>String(v==null?'':v).replaceAll('\"','\"\"');let t='No,Larutan kerja,Konsentrasi (ppm),Replikat,λ (nm),Abs,%T,Bobot (g)\n'+rows.map(x=>[x.no,q(x.solution),x.concentration??'',x.replicate,x.lambda.toFixed(1),x.abs.toFixed(4),x.transmittance.toFixed(2),x.weight??''].join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv;charset=utf-8'}));a.download='cary100_simple_reads_history.csv';a.click();return}if(S.tab==='conc'){const C=S.cal,q=C.std.filter(s=>s.a!=null);if(!q.length){toast('Belum ada data.');return}let t='ppm,Abs,Sumber\n'+q.map(s=>s.c+','+Number(s.a).toFixed(4)+','+(s.source||'manual')).join('\n');if(C.fit)t+='\n\nslope,'+C.fit.a+'\nintercept,'+C.fit.b+'\nr,'+C.fit.r;const o=S.out;if(o.c!=null)t+='\n\nC terukur (ppm),'+o.c+'\nC asli (ppm),'+o.cA;if(o.mgg!=null)t+='\nKadar (mg/g),'+o.mgg;if(o.rec!=null)t+='\n% Recovery,'+o.rec;const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='kalibrasi_thiamin.csv';a.click();return}const r=S.res;if(!r){toast('Belum ada data.');return}let t=r.type==='scan'?'nm,Abs\n'+r.pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(4)).join('\n'):'n,nm,Abs,%T\n'+r.rows.map(x=>x.map(v=>+v.toFixed(4)).join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='cary100_'+r.type+'.csv';a.click()}
// ---------- kalibrasi thiamin, kadar, recovery
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const sdv=a=>{if(a.length<2)return 0;const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1))};
function setSample(s,c){S.sample=s;if(c!=null){S.conc=c;$('conc').value=c;$('cv').textContent=c}
 if(s==='blank')S.solutionKey='aquades';
 else if(s==='std'&&c!=null)S.solutionKey='std_'+String(Number(c));
 else if(s==='spk')S.solutionKey='spike';
 else if(s==='unk'){const current=$('smp').value;if(current.startsWith('pres_')||current.startsWith('akurasi_')||current==='unk')S.solutionKey=current;else{$('smp').value='unk';S.solutionKey='unk'}}
 if(s==='blank')$('smp').value='aquades';else if(s==='std'&&c!=null)$('smp').value='std_'+String(Number(c));else if(s==='spk')$('smp').value='spike';
 $('conc').disabled=s!=='std';setLiq();updateSolutionGate()}
function readOne(sample,c,cb){const e=pre();if(e){toast(e);return false}if(!S.base){toast('Belum melakukan Zero Blank. Pilih aquades lalu tekan Zero Blank (Aquades).');return false}const l=+$('cl').value;if(!(l>=190&&l<=900)){toast('λ harus 190–900 nm.');return false}S.cal.l=l;S.spkC=+$('cAdd').value||0;setSample(sample,c);S.lam=l;startJob({type:'read',l,n:3,t:0,vals:[],cb});if(!S.camOpt){S.camOpt=1;flyV('opt')}return true}
function measStd(i,all){
 if(all&&!S.batchMeasuring)return;
 if(all&&(S.paused||S.identifyMode)){setTimeout(()=>measStd(i,true),100);return}
 const s=S.cal.std[i];
 if(!s){S.batchMeasuring=0;S.measureVisual=0;syncX();syncProcessButtons();return}
 const mode=$('stdDataMode')?.value||'praktikum';
 const preset=practicumAbsorbanceForConcentration(s.c);
 const practicalValue=(s.a!=null && Number.isFinite(Number(s.a)))?Number(s.a):preset;
 if(mode==='praktikum'&&!Number.isFinite(practicalValue)){
  toast('Tidak ada nilai praktikum untuk konsentrasi '+s.c+' ppm. Isi absorbansi manual atau pilih Simulasi pembacaan alat.');
  if(all){S.batchMeasuring=0;S.measureVisual=0;syncX();syncProcessButtons();}
  return;
 }
 const ok=readOne('std',s.c,v=>{
  if(mode==='praktikum'){
   // Animasi pengukuran tetap berlangsung, namun nilai hasil tabel mengikuti data praktikum/angka manual.
   s.a=(s.a!=null && Number.isFinite(Number(s.a)))?Number(s.a):preset;
   s.sd=null;
   if(s.source!=='manual')s.source='praktikum';
  }else{
   // Mode alternatif: gunakan hasil pembacaan simulasi instrumen, dengan variasi replikasi.
   s.a=mean(v);s.sd=sdv(v);s.source='simulasi';
  }
  S.cal.fit=null;
  if(all&&i+1<S.cal.std.length){renderStd();setTimeout(()=>measStd(i+1,true),300)}
  else{S.batchMeasuring=0;S.measureVisual=0;syncX();syncProcessButtons();calc(true);toast(mode==='praktikum'?'Pengukuran selesai. Nilai kurva menggunakan data praktikum yang ditampilkan pada tabel.':'Pengukuran deret standar simulasi 0–25 ppm selesai.')}
 });
 if(!ok&&all){S.batchMeasuring=0;S.measureVisual=0;syncX();syncProcessButtons()}
}
function calc(quiet){const C=S.cal,p=C.std.filter(s=>s.a!==null&&s.a!==''&&s.c!==null&&s.c!==''&&Number.isFinite(Number(s.a))&&Number.isFinite(Number(s.c)));
 if(p.length<3){C.fit=null;if(!quiet)toast('Minimal 3 standar terisi (absorban terukur atau diketik).');renderStd();renderRes();return}
 const n=p.length,sx=p.reduce((s,q)=>s+q.c,0),sy=p.reduce((s,q)=>s+q.a,0),sxx=p.reduce((s,q)=>s+q.c*q.c,0),sxy=p.reduce((s,q)=>s+q.c*q.a,0);const den=n*sxx-sx*sx;
 if(Math.abs(den)<1e-12){C.fit=null;if(!quiet)toast('Konsentrasi standar harus berbeda-beda.');renderStd();renderRes();return}
 const a=(n*sxy-sx*sy)/den,b=(sy-a*sx)/n,ym=sy/n;if(!Number.isFinite(a)||a<=1e-12){C.fit=null;if(!quiet)toast('Kurva kalibrasi tidak valid: kemiringan (slope) harus positif. Periksa kembali konsentrasi dan absorbansi standar.');renderStd();renderRes();return}const sst=p.reduce((s,q)=>s+(q.a-ym)**2,0),ssr=p.reduce((s,q)=>s+(q.a-(a*q.c+b))**2,0);const syx=n>2?Math.sqrt(ssr/(n-2)):0;
 // Pearson r dihitung langsung dari pasangan data (konsentrasi, absorbansi),
 // bukan dengan mengganti label R² atau hanya menampilkan akar R².
 const xBar=sx/n,yBar=sy/n;
 const ssx=p.reduce((sum,q)=>sum+(q.c-xBar)**2,0);
 const ssy=p.reduce((sum,q)=>sum+(q.a-yBar)**2,0);
 const covarianceSum=p.reduce((sum,q)=>sum+(q.c-xBar)*(q.a-yBar),0);
 const r=(ssx>0&&ssy>0)?Math.max(-1,Math.min(1,covarianceSum/Math.sqrt(ssx*ssy))):NaN;
 // R² tetap disimpan secara internal sebagai statistik regresi; antarmuka menampilkan r.
 const r2=Number.isFinite(r)?r*r:NaN;
 C.fit={a,b,r2,r,n,syx,lod:3.3*syx/a,loq:10*syx/a};renderStd();renderRes()}
function measUnk(){if(!S.cal.fit){toast('Hitung kurva kalibrasi dulu.');return}readOne('unk',null,v=>{const avg=mean(v);S.lastSampleRead={key:S.solutionKey||'unk',solution:'Sampel tidak diketahui',absorbance:avg,replicates:v.length,concentration:null,weight:null,prepVolumeMl:null,prepDilutionFactor:null,lambda:S.cal.l};setAbsorbanceValue('aU',avg,'Absorbansi terisi otomatis dari pembacaan sampel (rata-rata '+v.length+' replikasi). Nilai tetap bisa diedit manual.');renderRes()})}
function measSpk(){if(!S.cal.fit){toast('Hitung kurva kalibrasi dulu.');return}if(!(+$('cAdd').value>0)){toast('Isi konsentrasi spike yang ditambahkan.');return}readOne('spk',null,v=>{const avg=mean(v);S.lastSampleRead={key:'spike',solution:'Sampel + spike',absorbance:avg,replicates:v.length,concentration:null,weight:null,prepVolumeMl:null,prepDilutionFactor:null,lambda:S.cal.l};setAbsorbanceValue('aSp',avg,'Absorbansi sampel + spike terisi otomatis dari '+v.length+' replikasi. Nilai tetap bisa diedit manual.');renderRes()})}
function renderStd(){
 const C=S.cal;
 let t='<table><tr><th>No</th><th>Konsentrasi (ppm)</th><th>Absorban (ukur / ketik)</th><th>Sumber</th><th></th></tr>';
 C.std.forEach((s,i)=>{
  const sourceLabel=s.source==='simulasi'?'Simulasi':s.source==='manual'?'Manual':s.a==null?'Kosong':'Praktikum';
  t+=`<tr><td>${i+1}</td><td><input data-i="${i}" data-k="c" type="number" step="0.5" min="0" value="${s.c==null?'':s.c}"></td><td><input data-i="${i}" data-k="a" type="number" step="0.001" min="0" placeholder="–" value="${s.a==null?'':Number(s.a).toFixed(4)}" title="${s.sd!=null?'SD n=3: '+s.sd.toFixed(4):''}"></td><td>${sourceLabel}</td><td style="text-align:center"><button data-m="${i}">Ukur</button> <button data-d="${i}" title="Hapus nilai baris">✕</button></td></tr>`;
 });
 $('stdtab').innerHTML=t+'</table>';
 $('stdtab').querySelectorAll('input').forEach(e=>e.onchange=()=>{
  const s=C.std[+e.dataset.i];
  if(e.dataset.k==='c'){
   // Konsentrasi dan absorbansi adalah dua input independen. Mengubah Xi
   // tidak boleh diam-diam menimpa Yi, supaya kurva memakai data yang pengguna lihat.
   const v=parseFloat(e.value);
   s.c=Number.isFinite(v)?v:null;
   s.sd=null;
   s.source='manual';
  }else{
   const v=parseFloat(e.value);
   s.a=Number.isFinite(v)?v:null;
   s.sd=null;
   s.source='manual';
  }
  C.fit=null;
  calc(true);
 });
 $('stdtab').querySelectorAll('button[data-m]').forEach(b=>b.onclick=()=>measStd(+b.dataset.m,false));
 $('stdtab').querySelectorAll('button[data-d]').forEach(b=>b.onclick=()=>{const s=C.std[+b.dataset.d];if(s){s.a=null;s.sd=null;s.source='manual'}C.fit=null;renderStd();renderRes()});
 const mode=$('stdDataMode');
 if(mode){
  mode.disabled=!!(S.job||S.batchMeasuring);
  const hint=$('stdDataModeHint');
  if(hint)hint.textContent=mode.value==='praktikum'
   ?'Mode data praktikum aktif: tombol Ukur akan memakai nilai absorbansi di tabel (termasuk hasil edit manual). Animasi alat tetap berjalan. Pilih Simulasi pembacaan alat untuk mengganti nilai dengan hasil simulasi.'
   :'Mode simulasi aktif: saat tombol Ukur digunakan, nilai pada baris akan diganti dengan hasil pembacaan simulasi. Kamu tetap bisa mengedit nilainya secara manual setelah pengukuran.';
 }
}
function renderRes(){
 const C=S.cal,f=C.fit,key=S.solutionKey||'';let r='';C.unk=null;C.spk=null;S.out={};
 if(f)r+=`<div class="calc-formula"><b>Persamaan kalibrasi:</b> A = ${fmtID(f.a,5)} × C ${f.b<0?'−':'+'} ${fmtID(Math.abs(f.b),5)}<br><b>r (koefisien korelasi)</b> = ${fmtID(f.r,5)} ${f.r>=.995?'✔ korelasi linear sangat kuat':'⚠ periksa data standar dan rentang kurva'}<br>LOD ≈ ${fmtID(f.lod,3)} ppm · LOQ ≈ ${fmtID(f.loq,3)} ppm</div>`;
 else r+='<div class="calc-formula">Kurva belum dihitung. Ukur/isi absorbansi standar, minimal tiga konsentrasi yang berbeda, lalu tekan <b>Hitung kurva</b>.</div>';
 const A=parseFloat($('aU').value),isPrecision=key.startsWith('pres_'),isAccuracy=key.startsWith('akurasi_'),isWeightTest=isPrecision||isAccuracy;
 if(f&&Number.isFinite(A)){
  if(!Number.isFinite(f.a)||f.a<=1e-12){r+='<div class="calc-warning">Kurva kalibrasi tidak valid karena slope tidak positif. Periksa ulang data standar sebelum menghitung sampel.</div>';}
  else{
   const c=(A-f.b)/f.a;S.out.c=c;C.unk={A,c,df:1};
   const measuredStd=C.std.filter(s=>s.a!=null&&Number.isFinite(s.c));
   const amin=measuredStd.length?Math.min(...measuredStd.map(s=>s.a)):NaN,amax=measuredStd.length?Math.max(...measuredStd.map(s=>s.a)):NaN;
   const minC=measuredStd.length?Math.min(...measuredStd.map(s=>s.c)):0,maxC=measuredStd.length?Math.max(...measuredStd.map(s=>s.c)):25;
   const inRange=Number.isFinite(amin)&&A>=amin-.01&&A<=amax+.01&&c>=minC-.25&&c<=maxC+.25;
   if(isWeightTest){
    const weight=testWeightForKey(key),weightMg=weight*1000,volume=testVolumeMl(),dilution=testDilutionFactor(),cNominal=nominalTestConcentrationPPM(key);
    const foundMg=c>=0?testMassFoundMg(A,f,volume,dilution):NaN;
    const nominalValid=Number.isFinite(cNominal)&&cNominal>0&&cNominal<=maxC+.25;
    const measuredValid=Number.isFinite(c)&&c>=0&&c<=maxC+.25&&f.a>1e-12;
    const accuracyValid=nominalValid&&measuredValid&&inRange;
    S.out.cA=Number.isFinite(c)&&c>=0?c*dilution:NaN;S.out.mgFound=foundMg;S.out.weight=weight;
    r+=`<section class="calc-section"><div class="calc-section-title"><span class="calc-section-number">${isPrecision?'P':'A'}</span><div><h4>${isPrecision?'Hasil Uji Presisi':'Hasil Uji Akurasi'}</h4><p>Bobot 0,0050 g setara dengan 5,000 mg. Konsentrasi nominal dihitung setelah memperhitungkan volume labu dan faktor pengenceran.</p></div></div>`;
    r+=`Bobot sampel = <b>${fmtID(weight,4)} g</b> (${fmtID(weightMg,3)} mg)<br>Volume labu = <b>${fmtID(volume,1)} mL</b> · Faktor pengenceran = <b>${fmtID(dilution,3)}×</b><br>Konsentrasi nominal setelah pengenceran = <b>${fmtID(cNominal,3)} ppm</b><br>Absorbansi terukur = <b>${fmtID(A,4)} AU</b><br>Konsentrasi terhitung dari kurva = <b>${fmtID(c,3)} ppm</b><br>`;
    if(Number.isFinite(foundMg))r+=`Massa analit terhitung = <b>${fmtID(foundMg,4)} mg</b><br>`;
    else r+='<div class="calc-warning">Massa analit tidak dihitung karena konsentrasi terhitung negatif atau kurva tidak valid. Periksa Zero Blank, absorbansi standar, panjang gelombang, dan hasil pembacaan sampel.</div>';
    if(isAccuracy){
     if(accuracyValid){const ratio=(c/cNominal)*100;S.out.testAccuracy=ratio;r+=`<br><b>Persen perolehan kembali relatif bobot = ${fmtID(ratio,2)}%</b> ${ratio>=80&&ratio<=120?'<span style="color:#216b3b">(dalam rentang cek ilustratif 80–120%)</span>':'<span style="color:#a14b16">(di luar rentang cek ilustratif 80–120%)</span>'}<br><small>Rumus: konsentrasi terukur ÷ konsentrasi nominal × 100%. Rumus ini setara dengan massa analit terhitung ÷ massa acuan × 100% jika volume dan faktor pengenceran yang digunakan sama.</small>`;}
     else{delete S.out.testAccuracy;r+='<div class="calc-warning"><b>% akurasi tidak dihitung.</b> Hasil absorbansi/konsentrasi berada di luar rentang kurva 0–25 ppm atau menghasilkan konsentrasi negatif. Pastikan larutan setelah pengenceran berada dalam rentang standar dan bobot, volume, serta faktor pengenceran sesuai preparasi aktual.</div>';}
    }else{
     const presRows=(S.simpleHistory||[]).filter(row=>String(row.key||'').startsWith('pres_')&&Number.isFinite(row.abs));
     const amounts=presRows.map(row=>testMassFoundMg(row.abs,f,row.prepVolumeMl||volume,row.prepDilutionFactor||dilution)).filter(Number.isFinite);
     if(amounts.length>=2){const avg=amounts.reduce((s,v)=>s+v,0)/amounts.length;const sd=Math.sqrt(amounts.reduce((s,v)=>s+(v-avg)**2,0)/(amounts.length-1));const rsd=avg!==0?sd/Math.abs(avg)*100:NaN;S.out.precisionRSD=rsd;r+=`<hr><b>Ringkasan presisi seluruh hasil Presisi 1–5:</b> n = ${amounts.length}; rata-rata massa terhitung = ${fmtID(avg,4)} mg; SD = ${fmtID(sd,5)} mg; <b>%RSD = ${fmtID(rsd,3)}%</b>.<br><small>%RSD = SD ÷ rata-rata × 100%. Ukur Presisi 1–5 menggunakan kondisi preparasi yang sama sesuai SOP.</small>`;}
     else r+='<hr>Ringkasan %RSD muncul setelah minimal dua hasil Presisi 1–5 yang valid tercatat di riwayat Simple Reads.';
    }
    r+=`<hr><small>Rumus konsentrasi nominal: bobot (g) × 1.000.000 ÷ [volume (mL) × faktor pengenceran]. Format angka Indonesia: <b>25,000 ppm berarti 25 ppm</b>, bukan dua puluh lima ribu ppm. ${cNominal>maxC+.25?'⚠ Konsentrasi nominal di atas rentang standar terukur; lakukan pengenceran sesuai SOP sebelum menilai akurasi.':''}</small></section>`;
    r+=inRange?'✔ Absorbansi berada dalam rentang kurva standar.':'<div class="calc-warning">Absorbansi berada di luar rentang kurva standar. Jangan menyimpulkan persen akurasi dari ekstrapolasi; periksa data atau sesuaikan pengenceran.</div>';
   }else{
    const df=Math.max(1,+$('df').value||1),V=+$('vol').value,m=+$('massa').value,tw=+$('tabw').value;
    if(c<0){r+='<div class="calc-warning"><b>Konsentrasi terhitung negatif.</b> Nilai ini tidak dilaporkan sebagai kadar. Periksa Zero Blank, data kurva, dan pastikan absorbansi sampel sesuai larutan yang dipilih.</div>';}
    else{
     const cA=c*df;C.unk={A,c,df};S.out.cA=cA;
     r+=`<section class="calc-section"><div class="calc-section-title"><span class="calc-section-number">S</span><div><h4>Hasil Kadar Sampel</h4><p>Absorbansi dikonversi memakai persamaan kurva kalibrasi.</p></div></div>`;
     r+=`Absorbansi = <b>${fmtID(A,4)} AU</b> · %T = <b>${fmtID(100*Math.pow(10,-A),2)}%</b><br>Konsentrasi terukur = <b>${fmtID(c,3)} ppm</b><br>Konsentrasi setelah faktor pengenceran = <b>${fmtID(cA,3)} ppm</b> (FP ${fmtID(df,3)})<br>`;
     if(V>0&&m>0){const mgg=cA*(V/1000)/m;S.out.mgg=mgg;r+=`<b>Kadar = ${fmtID(mgg,4)} mg/g</b> = ${fmtID(mgg*100,2)} mg/100 g = ${fmtID(mgg*1000,1)} mg/kg<br>`;if(tw>0)r+=`≈ ${fmtID(mgg*tw,3)} mg/tablet (bobot rata-rata ${fmtID(tw,3)} g)<br>`;r+='<small>Kadar (mg/g) = C (mg/L) × FP × V (L) ÷ massa sampel (g).</small><br>';}
     else r+='<span style="color:#a14b16">Isi massa sampel dan volume labu sesuai preparasi.</span><br>';
     r+=inRange?'✔ Absorbansi berada dalam rentang standar terukur.':'<div class="calc-warning">Absorbansi di luar rentang standar terukur. Hindari ekstrapolasi; encerkan atau siapkan ulang sesuai SOP.</div>';
     const Asp=parseFloat($('aSp').value),add=+$('cAdd').value;
     if(Number.isFinite(Asp)&&add>0){const cs=(Asp-f.b)/f.a;C.spk={A:Asp,c:cs};if(c>=0&&cs>=c&&cs<=maxC+.25){const rec=(cs-c)/add*100;S.out.rec=rec;r+=`<hr><b>Recovery spike:</b> C sampel + spike = ${fmtID(cs,3)} ppm; C sampel = ${fmtID(c,3)} ppm; spike = ${fmtID(add,3)} ppm.<br><b>% Recovery = ${fmtID(rec,2)}%</b> (${rec>=80&&rec<=120?'dalam rentang cek ilustratif 80–120%':'di luar rentang cek ilustratif 80–120%'}).<br><small>%Recovery = (C sampel+spike − C sampel) ÷ C spike × 100.</small>`;}else r+='<div class="calc-warning">% recovery tidak dihitung karena hasil sampel atau sampel + spike negatif/tidak sebanding atau di luar rentang kurva.</div>';}
     else r+='<hr>Recovery spike: ukur sampel + spike atau isi absorbansinya dan konsentrasi spike.';
     r+='</section>';
    }
   }
  }
 }else if(f){r+='<div class="calc-section">Absorbansi belum tersedia. Ukur sampel melalui Simple Reads atau masukkan nilai secara manual.</div>'}
 $('cres').innerHTML=r;drawCal();updateWeightNominalCells();renderAutoFinalResults();
}
function latestMeasurementBatch(key){
 const rows=(S.simpleHistory||[]).filter(row=>row.key===key&&Number.isFinite(Number(row.abs)));
 if(!rows.length)return [];
 // Setiap sesi Simple Reads memulai nomor replikasi dari 1; ambil batch terbaru saja.
 let start=0;
 for(let i=rows.length-1;i>=0;i--){if(Number(rows[i].replicate)===1){start=i;break}}
 return rows.slice(start);
}
function avgBatchAbs(key){const rows=latestMeasurementBatch(key);if(!rows.length)return NaN;return rows.reduce((sum,row)=>sum+Number(row.abs),0)/rows.length}
function calcConcentrationFromAbs(abs,fit){return fit&&Number.isFinite(abs)&&Number.isFinite(fit.a)&&fit.a>1e-12?(abs-fit.b)/fit.a:NaN}
function absorbanceWithinStandards(abs){
 const q=S.cal.std.filter(s=>s.c!==null&&s.c!==''&&s.a!==null&&s.a!==''&&Number.isFinite(Number(s.c))&&Number.isFinite(Number(s.a)));
 if(q.length<2||!Number.isFinite(abs))return false;
 const lo=Math.min(...q.map(s=>Number(s.a))),hi=Math.max(...q.map(s=>Number(s.a)));
 return abs>=lo-.01&&abs<=hi+.01;
}
function renderAutoFinalResults(){
 const host=$('autoFinalResultsBody');if(!host)return;
 const C=S.cal,f=C.fit;
 if(!f||!Number.isFinite(f.a)||f.a<=1e-12){
  host.innerHTML='<b>Hasil akhir belum tersedia.</b> Isi minimal tiga standar dengan konsentrasi berbeda dan absorbansi valid. Setelah tabel standar diedit, kurva dan seluruh hasil akan dihitung ulang otomatis.';
  return;
 }
 const key=S.solutionKey||'';
 const fmt=(v,d=4)=>Number.isFinite(Number(v))?fmtID(Number(v),d):'—';
 let html=`<div><b>Kurva aktif:</b> A = ${fmt(f.a,6)} × C ${f.b<0?'−':'+'} ${fmt(Math.abs(f.b),6)}; <b>r = ${fmt(f.r,6)}</b>. Perubahan tabel standar sudah diterapkan ke hasil berikut.</div>`;
 const sampleHistoryAbs=avgBatchAbs('unk');
 const spikeHistoryAbs=avgBatchAbs('spike');
 let sampleAbs=NaN;
 // Gunakan kolom absorbansi aktif hanya jika konteksnya bukan uji berbobot atau larutan standar.
 if(Number.isFinite(parseFloat($('aU').value)) && !key.startsWith('pres_') && !key.startsWith('akurasi_') && key!=='spike' && key!=='aquades' && !key.startsWith('std_')) sampleAbs=parseFloat($('aU').value);
 if(!Number.isFinite(sampleAbs))sampleAbs=sampleHistoryAbs;
 const cSample=calcConcentrationFromAbs(sampleAbs,f);
 if(Number.isFinite(sampleAbs)&&Number.isFinite(cSample)&&cSample>=0){
  const V=Number($('vol').value),DF=Math.max(1,Number($('df').value)||1),mass=Number($('massa').value);
  html+=`<section style="margin-top:8px"><b>1. Hasil kadar sampel</b><br>Absorbansi sampel = ${fmt(sampleAbs)} AU; konsentrasi terukur = ${fmt(cSample,5)} ppm.`;
  if(V>0&&mass>0){const cOriginal=cSample*DF,mgG=cOriginal*(V/1000)/mass;html+=`<br>Konsentrasi setelah faktor pengenceran = ${fmt(cOriginal,5)} ppm; <b>kadar = ${fmt(mgG,6)} mg/g</b> (${fmt(mgG*100,4)} mg/100 g).`}
  html+=`<br><small>Sumber absorbansi: ${Number.isFinite(parseFloat($('aU').value))&&!key.startsWith('pres_')&&!key.startsWith('akurasi_')?'kolom input aktif':'riwayat pembacaan sampel terbaru'}.</small></section>`;
 }else{
  html+='<section style="margin-top:8px"><b>1. Hasil kadar sampel</b><br>Belum ada absorbansi sampel yang valid. Ukur sampel atau masukkan absorbansi secara manual.</section>';
 }

 // Presisi 1–5: gunakan satu nilai rata-rata per sesi uji, lalu hitung massa analit berdasarkan kurva TERBARU.
 const precisionResults=[];
 for(let i=1;i<=5;i++){
  const k='pres_'+i,rows=latestMeasurementBatch(k),historyAbs=rows.length?rows.reduce((sum,row)=>sum+Number(row.abs),0)/rows.length:NaN;
  const activeAbs=(key===k&&Number.isFinite(parseFloat($('aU').value)))?parseFloat($('aU').value):NaN;
  const abs=Number.isFinite(activeAbs)?activeAbs:historyAbs;
  const refRow=rows.length?rows[rows.length-1]:null;
  if(Number.isFinite(abs)&&(refRow||Number.isFinite(activeAbs))){
   const c=calcConcentrationFromAbs(abs,f),weight=Number(key===k?testWeightForKey(k):(refRow?.weight??testWeightForKey(k))),vol=Number(key===k?testVolumeMl():(refRow?.prepVolumeMl||testVolumeMl())),df=Number(key===k?testDilutionFactor():(refRow?.prepDilutionFactor||testDilutionFactor()));
   const foundMg=c>=0&&vol>0&&df>0?c*df*(vol/1000):NaN;
   precisionResults.push({label:'Presisi '+i,key:k,abs,c,weight,foundMg,rows:rows.length});
  }
 }
 html+='<section style="margin-top:8px"><b>2. Hasil uji presisi</b>';
 if(precisionResults.length){
  html+='<div style="overflow-x:auto"><table><tr><th>Uji</th><th>n</th><th>Rata-rata Abs</th><th>C terhitung (ppm)</th><th>Bobot (g)</th><th>Massa analit (mg)</th></tr>';
  precisionResults.forEach(q=>{html+=`<tr><td>${q.label}</td><td>${q.rows}</td><td>${fmt(q.abs)}</td><td>${fmt(q.c,5)}</td><td>${fmt(q.weight,4)}</td><td>${fmt(q.foundMg,5)}</td></tr>`});
  html+='</table></div>';
  const masses=precisionResults.map(q=>q.foundMg).filter(Number.isFinite);
  if(masses.length>=2){const avg=masses.reduce((sum,v)=>sum+v,0)/masses.length,sd=Math.sqrt(masses.reduce((sum,v)=>sum+(v-avg)**2,0)/(masses.length-1)),rsd=avg!==0?sd/Math.abs(avg)*100:NaN;html+=`Rata-rata massa = ${fmt(avg,5)} mg; SD = ${fmt(sd,6)} mg; <b>%RSD = ${fmt(rsd,4)}%</b>.`}
  else html+='\n<small>Ukur setidaknya dua sampel Presisi yang berbeda untuk menghitung %RSD.</small>';
 }else html+='Belum ada hasil Presisi 1–5 pada riwayat Simple Reads.';
 html+='</section>';

 // Akurasi 1: recalculated from its latest mean absorbance and the currently stored weight/preparation.
 const accRows=latestMeasurementBatch('akurasi_1'),activeAccuracyAbs=(key==='akurasi_1'&&Number.isFinite(parseFloat($('aU').value)))?parseFloat($('aU').value):NaN,accAbs=Number.isFinite(activeAccuracyAbs)?activeAccuracyAbs:(accRows.length?accRows.reduce((sum,row)=>sum+Number(row.abs),0)/accRows.length:NaN);
 html+='<section style="margin-top:8px"><b>3. Hasil uji akurasi</b>';
 if(Number.isFinite(accAbs)){
  const refRow=accRows.length?accRows[accRows.length-1]:null,weight=Number(key==='akurasi_1'?testWeightForKey('akurasi_1'):(refRow?.weight??testWeightForKey('akurasi_1'))),vol=Number(key==='akurasi_1'?testVolumeMl():(refRow?.prepVolumeMl||testVolumeMl())),df=Number(key==='akurasi_1'?testDilutionFactor():(refRow?.prepDilutionFactor||testDilutionFactor())),c=calcConcentrationFromAbs(accAbs,f),nominal=weight*1000000/(vol*df),foundMg=c>=0&&vol>0&&df>0?c*df*(vol/1000):NaN,accuracy=Number.isFinite(foundMg)&&weight>0?foundMg/(weight*1000)*100:NaN;
  html+=`<br>Rata-rata Abs = ${fmt(accAbs)} AU; bobot acuan = ${fmt(weight,4)} g; konsentrasi nominal = ${fmt(nominal,5)} ppm; konsentrasi terukur = ${fmt(c,5)} ppm; massa analit terhitung = ${fmt(foundMg,5)} mg; <b>akurasi = ${fmt(accuracy,3)}%</b>.`;
  if(!absorbanceWithinStandards(accAbs)||!Number.isFinite(c)||c<0||nominal>Math.max(...C.std.map(s=>Number(s.c)).filter(Number.isFinite)))html+='<div class="calc-warning">Absorbansi/konsentrasi akurasi berada di luar rentang kalibrasi. Angka ditampilkan sebagai diagnostik, bukan hasil validasi.</div>';
  else if(accuracy<80||accuracy>120)html+='<div class="calc-warning">Hasil akurasi berada di luar rentang evaluasi 80–120%; periksa bobot, pengenceran, Zero Blank, dan data absorbansi.</div>';
 }else html+='Belum ada hasil Akurasi 1 pada riwayat Simple Reads. Pilih Akurasi 1 lalu ukur untuk menghitung hasilnya.';
 html+='</section>';

 // Recovery uses editable values when both are populated; otherwise it can use the most recent sample/spike reads.
 const recoverySampleAbs=Number.isFinite(parseFloat($('aU').value))&&!key.startsWith('pres_')&&!key.startsWith('akurasi_')&&key!=='spike'&&key!=='aquades'&&!key.startsWith('std_')?parseFloat($('aU').value):sampleHistoryAbs;
 const recoverySpikeAbs=Number.isFinite(parseFloat($('aSp').value))?parseFloat($('aSp').value):spikeHistoryAbs;
 const added=Number($('cAdd').value);
 html+='<section style="margin-top:8px"><b>4. Hasil % recovery</b>';
 if(Number.isFinite(recoverySampleAbs)&&Number.isFinite(recoverySpikeAbs)&&Number.isFinite(added)&&added>0){
  const c0=calcConcentrationFromAbs(recoverySampleAbs,f),csp=calcConcentrationFromAbs(recoverySpikeAbs,f),recovery=(csp-c0)/added*100;
  html+=`<br>Abs sampel = ${fmt(recoverySampleAbs)} AU; Abs sampel + spike = ${fmt(recoverySpikeAbs)} AU; C sampel = ${fmt(c0,5)} ppm; C sampel + spike = ${fmt(csp,5)} ppm; spike ditambahkan = ${fmt(added,5)} ppm; <b>% Recovery = ${fmt(recovery,3)}%</b>.`;
  if(!absorbanceWithinStandards(recoverySampleAbs)||!absorbanceWithinStandards(recoverySpikeAbs)||c0<0||csp<0)html+='<div class="calc-warning">Salah satu pembacaan berada di luar rentang kalibrasi. Recovery dihitung sebagai pemeriksaan, tetapi tidak layak ditafsirkan sebelum sampel sesuai rentang kurva.</div>';
  else if(recovery<80||recovery>120)html+='<div class="calc-warning">Recovery di luar rentang pemeriksaan 80–120%. Periksa kadar spike, nilai absorbansi, dan konsistensi pengenceran.</div>';
 }else html+='Masukkan/ukur absorbansi sampel dan sampel + spike serta isi konsentrasi spike. Hasil otomatis diperbarui saat input berubah.';
 html+='</section>';
 html+='<p class="calc-help" style="margin-bottom:0">Catatan: setiap perubahan konsentrasi atau absorbansi standar akan menghitung ulang regresi, kadar, massa terhitung, %RSD, akurasi, dan recovery berdasarkan kurva terbaru. Hasil uji yang sudah tercatat di riwayat juga dihitung ulang terhadap kurva tersebut.</p>';
 host.innerHTML=html;
}
function renderConc(){renderStd();renderRes();updateTestWeightSummary()}

function drawCal(){const c=$('chart'),g=c.getContext('2d'),w=c.width,h=c.height;g.fillStyle='#fff';g.fillRect(0,0,w,h);const C=S.cal,p=C.std.filter(s=>s.a!=null);
 const xm=Math.max(12,...C.std.map(s=>s.c),C.unk?C.unk.c:0,C.spk?C.spk.c:0)*1.1,ym=Math.max(.5,...p.map(s=>s.a),C.unk?C.unk.A:0,C.spk?C.spk.A:0)*1.2;const X=v=>55+v/xm*(w-70),Y=v=>h-34-v/ym*(h-56);
 g.font='11px sans-serif';g.lineWidth=1;for(let i=0;i<=5;i++){const xv=xm*i/5,yv=ym*i/5;g.strokeStyle='#e6e6e6';g.beginPath();g.moveTo(X(xv),20);g.lineTo(X(xv),h-34);g.moveTo(55,Y(yv));g.lineTo(w-15,Y(yv));g.stroke();g.fillStyle='#333';g.fillText(xv.toFixed(1),X(xv)-8,h-20);g.fillText(yv.toFixed(2),16,Y(yv)+4)}
 g.strokeStyle='#888';g.strokeRect(55,20,w-70,h-54);g.fillStyle='#333';g.font='bold 13px sans-serif';g.fillText('Konsentrasi (ppm)',Math.max(80,w/2-62),h-5);g.save();g.translate(15,h/2+35);g.rotate(-Math.PI/2);g.fillText('Absorbansi (AU)',0,0);g.restore();g.font='bold 12px sans-serif';g.fillText('Kurva kalibrasi thiamin pada '+C.l+' nm',65,14);
 const f=C.fit;if(f){g.strokeStyle='#1565c0';g.lineWidth=2;g.beginPath();g.moveTo(X(0),Y(f.b));g.lineTo(X(xm),Y(f.a*xm+f.b));g.stroke();g.lineWidth=1;g.fillStyle='#1565c0';g.fillText('y = '+f.a.toFixed(4)+'x '+(f.b<0?'−':'+')+' '+Math.abs(f.b).toFixed(4),65,36);g.fillText('r = '+f.r.toFixed(4),65,50)}
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
 const lv0=S.inst&&S.warm>2&&S.lam>=350;line([[-2.6,-1.7],[-2.2,-1.7]],0,lv0?1:0);line([[-2.2,-1.2],[-2.2,-1.7]],0,lv0?0:1);for(let i=0;i<common.length-1;i++)line(common,i,1);for(let i=0;i<sampP.length-1;i++)line(sampP,i,(i<3?1:.1+.9*T));for(let i=0;i<refP.length-1;i++)line(refP,i,1);g.globalAlpha=1;
 [[.95,1],[.05,0]].forEach(a=>{g.fillStyle=a[1]&&!S.cuv?'rgba(150,200,255,.12)':'rgba(150,200,255,.55)';g.fillRect(X(-.15),Y(a[0]-.15),X(.15)-X(-.15),Y(a[0]+.15)-Y(a[0]-.15))});
 g.strokeStyle='#e8eef5';g.lineWidth=3;MIRS.forEach(m=>{const dx=Math.cos(m[2])*.2,dz=-Math.sin(m[2])*.2;g.beginPath();g.moveTo(X(m[0]-dx),Y(m[1]-dz));g.lineTo(X(m[0]+dx),Y(m[1]+dz));g.stroke()});
 g.fillStyle='#b08d2a';g.fillRect(X(-1.9)-3,Y(-.6)-8,6,16);g.fillStyle='#777';g.beginPath();g.arc(X(-1.1),Y(.5),9,0,7);g.fill();g.fillStyle='#889';g.beginPath();g.arc(X(2.3),Y(.5),8,0,7);g.fill();
 const diagramReveal=!!(S.xray||S.identifyMode||S.measureVisual),lv=diagramReveal&&S.inst&&S.warm>2&&S.lam>=350,ld=diagramReveal&&S.inst&&S.warm>2&&S.lam<350,mn=S.lampMode==='manual',c1=mn?S.lampColor:AUTO_V,c2=mn?S.lampColor:AUTO_D;
 g.shadowColor=c1;g.shadowBlur=lv?18:0;g.fillStyle=lv?c1:'#555';g.beginPath();g.arc(X(-2.6),Y(-1.7),9,0,7);g.fill();
 g.shadowColor=c2;g.shadowBlur=ld?18:0;g.fillStyle=ld?c2:'#555';g.beginPath();g.arc(X(-2.2),Y(-1.2),8,0,7);g.fill();g.shadowBlur=0;
 if(v){g.fillStyle='#fff';pulses.forEach(p=>{if(!p.active)return;g.globalAlpha=.95;g.beginPath();g.arc(X(p.s.position.x),Y(p.s.position.z),2.4,0,Math.PI*2);g.fill();g.globalAlpha=1})}
 g.font='bold 10px sans-serif';[[1,-2.6,-1.7],[2,-1.9,-1.7],[3,-1.9,-1.2],[4,-1.9,-.6],[5,-1.1,-1.1],[6,-1.1,.5],[7,0,.95],[8,2.3,.5]].forEach(a=>{const x=X(a[1])-10,y=Y(a[2])-10;g.fillStyle='#2d7dd2';g.beginPath();g.arc(x,y,7,0,7);g.fill();g.fillStyle='#fff';g.fillText(a[0],x-3,y+3.5)});
 g.fillStyle='#e8edf3';g.font='10px sans-serif';g.fillText('I0=100',X(.25),Y(.05)+3);if(S.inst)g.fillText('I='+(100*T).toFixed(1),X(.25),Y(.95)+3)}
// ---------- label komponen 3D
const LB=[['Lampu tungsten',-2.6,-1.7,'lampV'],['Lampu deuterium',-2.2,-1.0,'lampD'],['Cermin M1',-1.9,-1.7,'mirror'],['Celah',-1.9,-1.2,'slit'],['Kisi difraksi',-1.9,-.6,'grat'],['Cermin M2',-1.1,-1.1,'mirror'],['Chopper',-1.1,.5,'chop'],['Kuvet sampel',0,.95,'hold_s'],['Kuvet referensi',0,.05,'hold_r'],['Detektor PMT',2.3,.5,'pmt']].map(a=>{const e=document.createElement('div');e.className='lb';e.textContent=a[0];e.title='Klik untuk membaca penjelasan';e.addEventListener('click',ev=>{ev.stopPropagation();showInfo(a[3])});document.body.appendChild(e);return{e,v:new THREE.Vector3(a[1]-3.2,BY+.35,a[2])}});
function updLb(){const rect=ren.domElement.getBoundingClientRect(),w=rect.width,hh=rect.height;LB.forEach(l=>{const q=l.v.clone().project(cam);const on=S.identifyMode&&S.lbl&&q.z<1&&q.x>=-1&&q.x<=1&&q.y>=-1&&q.y<=1;l.e.style.display=on?'block':'none';if(on){l.e.style.left=(rect.left+(q.x+1)/2*w+8)+'px';l.e.style.top=(rect.top+(1-q.y)/2*hh-10)+'px'}})}
// ---------- UI
const CHK=[['UPS menyala',()=>S.ups],['Instrumen menyala',()=>S.inst],['Komputer menyala',()=>S.pc],['Monitor menyala',()=>S.mon],['Warm-up selesai',()=>S.inst&&S.warm>=WARM],['Cary WinUV dibuka',()=>S.app],['Zero Blank aquades',()=>S.base],['Kuvet terpasang',()=>S.cuv],['Tutup tertutup',()=>!S.lid]];
function renderOpticalStatus(){
 const el=$('opticalStatus');if(!el)return;
 const processRunning=!!(S.job||S.batchMeasuring);
 const visible=!!S.inst&&S.warm>=WARM&&processRunning;
 el.hidden=!visible;if(!visible)return;
 const source=S.lam>=350?'lampu tungsten':'lampu deuterium';
 const phases=[
  ['Sumber cahaya menghasilkan berkas polikromatik',`Sumber aktif: ${source}. Intensitas sumber distabilkan sebelum cahaya masuk ke sistem optik.`,0],
  ['Monokromator memilih panjang gelombang',`Kisi difraksi bergerak untuk memilih λ ${S.lam.toFixed(1)} nm; berkas keluar ditampilkan dengan warna representatif panjang gelombang.`,1],
  ['Chopper memodulasi berkas sampel dan referensi','Kedua jalur optik ditampilkan bersamaan sebagai panduan visual. Pada Cary 100 sesungguhnya, chopper memodulasi sampel dan referensi bergiliran menuju detektor; partikel foton menunjukkan urutan ini.',2],
  ['Berkas melewati kuvet','Sebagian energi diserap larutan. Transmitansi turun sesuai absorbansi simulasi dan kondisi kuvet.',3],
  ['Detektor membaca intensitas cahaya','Sinyal sampel dibandingkan dengan referensi untuk menghasilkan transmitansi dan absorbansi.',4]
 ];
 let ix=Math.floor((S.opticalClock||0)%phases.length),step=null;
 if(S.job&&S.job.type==='base'){step=['Zero Blank dengan aquades','Detektor membaca blanko sebagai referensi dasar sebelum sampel diukur.',4]}
 else if(S.job&&S.job.type==='scan'){step=[`Scan λ ${S.lam.toFixed(1)} nm`,`Monokromator bergerak dari ${S.job.start.toFixed(0)} ke ${S.job.stop.toFixed(0)} nm untuk merekam spektrum standar 25 ppm.`,1]}
 else if(S.paused){step=['Pengukuran dijeda','Aliran foton dan chopper dijeda agar kamu dapat masuk ke mode Kenali Bagian.',ix]}
 else if(S.job||S.batchMeasuring){step=phases[ix]}
 else{step=['Pratinjau alur optik',phases[ix][1],ix]}
 $('opticalStep').textContent=step[0];$('opticalDetail').textContent=step[1];
 document.querySelectorAll('#opticalStatus [data-stage]').forEach(node=>{const i=Number(node.dataset.stage);node.classList.toggle('active',i===step[2]);node.classList.toggle('done',i<step[2])});
}
function renderUI(){document.querySelectorAll('#p-conc button').forEach(b=>b.disabled=!!S.job||!!S.batchMeasuring);$('prog').firstElementChild.style.width=(CHK.filter(c=>c[1]()).length/CHK.length*100)+'%';$('chk').innerHTML=CHK.map(c=>`<li class="${c[1]()?'ok':''}">${c[0]}${c[0]==='Warm-up selesai'&&S.inst&&S.warm<WARM?' '+Math.round(S.warm/WARM*100)+'%':''}</li>`).join('');
 $('bLid').textContent=S.lid?'Tutup tutup':'Buka tutup';$('bCuv').textContent=S.cuv?'Ambil kuvet':'Pasang kuvet';$('bL').classList.toggle('on',!!S.lbl);$('bX').classList.toggle('on',!!(S.xray||S.identifyMode||S.measureVisual));$('bB').classList.toggle('on',!!S.beam);syncProcessButtons();
 const st=!S.inst?'Instrument: Not connected':S.warm<WARM?'Instrument: Warming up '+Math.round(S.warm/WARM*100)+'%':'Instrument: Connected – Ready';$('status').textContent=st+(S.job?(S.paused?' | PROSES DIJEDA':' | Mengukur…'):'');
 $('aStart').disabled=!!S.job||!!S.batchMeasuring||!S.base||(S.tab==='scan'&&S.solutionKey!=='std_25');$('aBase').disabled=!!S.job||!!S.batchMeasuring||!!S.base;$('aStop').disabled=!(S.job||S.batchMeasuring);syncProcessButtons();
 $('cAll').disabled=!!S.job||!S.base;$('cFit').disabled=!!S.job||!S.base;$('cUnk').disabled=!!S.job||!S.base;$('cSpk').disabled=!!S.job||!S.base;
 const lon=S.inst&&S.warm>2;
 $('lmInfo').textContent=lon?'Aktif: '+(S.lam>=350?'lampu tungsten untuk wilayah tampak (visible)':'lampu deuterium untuk wilayah ultraviolet (UV)')+'. Peralihan sumber pada simulasi sekitar 350 nm; cocokkan dengan manual alat.':'Lampu padam. Nyalakan instrumen dan tunggu warm-up.';
 const sw=$('lmSw'),cc=lon?(S.lampMode==='manual'?S.lampColor:(S.lam>=350?AUTO_V:AUTO_D)):'#2a3340';sw.style.background=cc;sw.style.boxShadow=lon?`0 0 ${10+14*S.lampI}px ${cc}`:'none';sw.textContent=lon?(S.lam>=350?'Lampu tungsten menyala':'Lampu deuterium menyala'):'Lampu padam';
 $('hud').innerHTML='';
}
function syncX(){const transparent=!!(S.xray||S.identifyMode||S.measureVisual);shells.forEach(s=>{s.m.raycast=(transparent&&!s.keep)?()=>{}:THREE.Mesh.prototype.raycast})}
function updateTestWeightUI(key){const k=key||S.solutionKey||'';const wrap=$('testWeightWrap');if(!wrap)return;const isPrecision=k.startsWith('pres_'),isAccuracy=k.startsWith('akurasi_'),isWeightTest=isPrecision||isAccuracy;wrap.hidden=!isWeightTest;$('regularSampleFields').hidden=isWeightTest;$('weightSampleNote').hidden=!isWeightTest;if(!isWeightTest)return;const w=testWeightForKey(k);$('testWeightLabel').textContent=(isPrecision?'Bobot sampel Presisi (g)':'Bobot sampel Akurasi (g)')+' · '+k.replace('_',' ').replace(/^(pres|akurasi)/,m=>m==='pres'?'Presisi':'Akurasi');$('testWeight').value=(Number.isFinite(w)?w:0.0050).toFixed(4);$('massa').value=(Number.isFinite(w)?w:0.0050);}
function updateTestWeightSummary(){
 const el=$('testWeightSummary');if(!el)return;
 let t='<table><thead><tr><th>Uji</th><th>Bobot (g)</th><th>Konsentrasi nominal (ppm)</th></tr></thead><tbody>';
 const rows=[];
 for(let i=1;i<=5;i++)rows.push(['pres_'+i,'Presisi '+i]);
 rows.push(['akurasi_1','Akurasi 1']);
 for(const [key,label] of rows){
  const w=testWeightForKey(key),c=nominalTestConcentrationPPM(key),ok=Number.isFinite(c)&&c>=0&&c<=25;
  t+=`<tr><td>${label}</td><td><input data-weight-key="${key}" type="number" min="0.0001" step="0.0001" value="${(Number.isFinite(w)?w:0.0050).toFixed(4)}" aria-label="Bobot ${label} (g)"></td><td data-nominal-key="${key}" class="${ok?'nominal-ok':'nominal-warn'}">${Number.isFinite(c)?fmtID(c,3):'—'}${ok?'':' ⚠'}</td></tr>`;
 }
 t+='</tbody></table>';el.innerHTML=t;
 el.querySelectorAll('input[data-weight-key]').forEach(input=>{input.addEventListener('input',()=>{
  const key=input.dataset.weightKey,v=parseFloat(input.value);if(!Number.isFinite(v)||v<=0)return;
  if(key.startsWith('pres_'))S.precisionWeights[key]=v;else if(key==='akurasi_1')S.accuracyWeights[key]=v;
  if(S.solutionKey===key){$('testWeight').value=v.toFixed(4);$('massa').value=v;if($('aU').value){$('aU').value='';S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent='Bobot berubah setelah pembacaan. Ukur ulang sampel dengan bobot terbaru atau isi absorbansi manual yang sesuai.'}}
  updateWeightNominalCells();renderRes();
 })});
 updateWeightNominalCells();
}
function updateWeightNominalCells(){const volume=testVolumeMl(),df=testDilutionFactor();S.testVolumeMl=volume;S.testDilutionFactor=df;document.querySelectorAll('[data-nominal-key]').forEach(cell=>{const key=cell.dataset.nominalKey,c=nominalTestConcentrationPPM(key),ok=Number.isFinite(c)&&c>=0&&c<=25;cell.textContent=Number.isFinite(c)?fmtID(c,3)+(ok?'':' ⚠ di luar 0–25'): '—';cell.classList.toggle('nominal-ok',ok);cell.classList.toggle('nominal-warn',!ok)});}
function updateSolutionGate(){const sel=$('smp');if(!sel)return;updateTestWeightUI(S.solutionKey);
 if(!S.base){if(sel.value!=='aquades'){sel.value='aquades';S.solutionKey='aquades';S.sample='blank';$('conc').disabled=true;setLiq()}}
 else if(S.tab==='scan'&&sel.value!=='std_25'){sel.value='std_25';S.solutionKey='std_25';S.sample='std';S.conc=25;$('conc').value=25;$('cv').textContent='25';setLiq()}
 Array.from(sel.options).forEach(o=>{o.disabled=!S.base?o.value!=='aquades':(S.tab==='scan'?o.value!=='std_25':false)});
 $('conc').disabled=!S.base||S.tab==='scan'||S.sample!=='std';
 const n=$('zeroNotice');if(n){if(S.base){n.classList.add('done');n.innerHTML=S.tab==='scan'?'✓ Zero Blank aquades berhasil. Mode Scan dikunci ke <b>Standar 25 ppm</b> untuk penentuan λmax. Nilai acuan: '+DATA_LMAX_NM.toFixed(1)+' nm.':'✓ Zero Blank aquades berhasil. Pilihan standar 0–25 ppm, Presisi 1–5, dan Akurasi 1 tersedia. Zero Blank hanya dilakukan sekali selama sesi ini.'}else{n.classList.remove('done');n.innerHTML='⚠ Belum melakukan Zero Blank. Pilih Aquades, siapkan kuvet, lalu klik <b>Zero Blank (Aquades)</b> sebelum mengukur larutan lain.'}}
 }
$('smp').onchange=e=>{const previousKey=S.solutionKey||'';const key=e.target.value;if(previousKey!==key&&$('aU').value){$('aU').value='';S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent='Larutan berubah. Ukur larutan yang dipilih atau masukkan absorbansinya secara manual agar hasil tidak tercampur.'}S.solutionKey=key;S.spkC=+$('cAdd').value||0;if(key==='aquades'){S.sample='blank';S.conc=0;$('cv').textContent='0';$('conc').value=0;$('conc').disabled=true}
 else if(key.startsWith('std_')){S.sample='std';S.conc=Number(key.split('_')[1]);$('conc').value=S.conc;$('cv').textContent=S.conc;$('conc').disabled=false}
 else if(key.startsWith('pres_')||key.startsWith('akurasi_')||key==='unk'){S.sample='unk';$('conc').disabled=true;if(key.startsWith('pres_')||key.startsWith('akurasi_'))$('massa').value=testWeightForKey(key);}
 else if(key==='spike'){S.sample='spk';$('conc').disabled=true}
 setLiq();if(!S.base&&key!=='aquades'){e.target.value='aquades';S.sample='blank';S.solutionKey='aquades';toast('Lakukan Zero Blank dengan aquades terlebih dahulu.')}updateTestWeightUI(S.solutionKey);updateSolutionGate()};
$('conc').oninput=e=>{S.conc=+e.target.value;$('cv').textContent=S.conc;S.sample='std';S.solutionKey='std_'+String(Number(S.conc));$('smp').value=S.solutionKey;setLiq()};
$('bLid').onclick=toggleLid;$('bCuv').onclick=toggleCuv;
$('bX').onclick=()=>{
 if(S.job||S.batchMeasuring){toast('Saat pengukuran berlangsung, transparansi aktif tanpa label. Jeda proses lalu tekan Kenali Bagian untuk membaca nama dan fungsi komponen.');return}
 const turnOn=!(S.xray||S.identifyMode);
 if(turnOn){S.xray=1;S.identifyMode=1;S.lbl=1;$('bL').classList.add('on');showIdentifyGuide();toast('Mode transparan aktif. Klik label atau komponen untuk melihat penjelasannya.')}
 else{S.xray=0;S.identifyMode=0;S.lbl=0;$('bL').classList.remove('on');$('it').textContent='Klik bagian mana saja';$('ix').textContent='Mode transparan dimatikan. Aktifkan Transparan atau Kenali Bagian untuk melihat nama dan penjelasan komponen.';toast('Mode transparan ditutup.')}
 syncX();syncProcessButtons();$('bX').classList.toggle('on',!!(S.xray||S.identifyMode||S.measureVisual));
};
$('bB').onclick=()=>S.beam=S.beam?0:1;
S.autoRotateWanted=false;$('bR').onclick=e=>{S.autoRotateWanted=!S.autoRotateWanted;ctl.autoRotate=S.autoRotateWanted&&!S.paused;e.target.classList.toggle('on',S.autoRotateWanted)};$('bA').onclick=()=>{if(S.app&&S.appMinimized){S.appMinimized=0;$('app').hidden=false;drawScreen();renderUI();toast('Cary WinUV dibuka kembali.')}else openApp(true)};$('minApp').onclick=minimizeApp;$('xapp').onclick=()=>openApp(false);
$('bFS').onclick=()=>{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen().catch(()=>toast('Layar penuh diblokir browser.'))};$('bRe').onclick=()=>location.reload();
$('aBase').onclick=startBase;$('aStart').onclick=start;$('aStop').onclick=()=>{S.batchMeasuring=0;S.measureVisual=0;S.paused=0;finishJob();toast('Proses dihentikan.');};$('aCsv').onclick=csv;$('cAll').onclick=()=>{if(S.job||S.batchMeasuring){toast('Pengukuran sedang berjalan.');return}if(!S.base){toast('Lakukan Zero Blank aquades terlebih dahulu.');return}enterAnimationFocus();S.batchMeasuring=1;S.measureVisual=1;syncProcessButtons();syncAnimationFocusHUD();measStd(0,true)};$('cFit').onclick=()=>calc(false);$('cUnk').onclick=measUnk;$('cSpk').onclick=measSpk;
$('stdDataMode').onchange=()=>{renderStd();toast($('stdDataMode').value==='praktikum'?'Mode data praktikum: pengukuran standar akan mencatat nilai pada tabel.':'Mode simulasi: pengukuran standar akan memakai hasil simulasi instrumen.');};
$('cClr').onclick=()=>{S.cal.std.forEach(s=>{s.a=null;s.sd=null;s.source='manual'});S.cal.fit=null;$('aU').value='';$('aSp').value='';renderConc();toast('Nilai kalibrasi dikosongkan. Mode data praktikum dapat mengisi kembali nilai standar saat tombol Ukur ditekan; input manual tetap tersedia.')};
$('cAddStd').onclick=()=>{const C=S.cal,last=C.std.length?C.std[C.std.length-1].c:0;C.std.push({c:last+5,a:null,sd:null});C.fit=null;calc(true)};
const useL=()=>{if(S.lmax){const v=Math.round(S.lmax.l*10)/10;$('cl').value=v;$('sl').value=v;S.cal.l=v;toast('λ analisis = '+v+' nm (dari λmax scan).');drawCal()}else toast('Lakukan Scan dulu untuk mendapatkan λmax.')};
$('bUseL').onclick=useL;$('cUseL').onclick=useL;$('cl').onchange=()=>{S.cal.l=+$('cl').value;drawCal()};
['massa','vol','df','tabw','aU','aSp','cAdd'].forEach(id=>$(id).oninput=()=>{if(id==='aU'&&!S.isAutoFillingAbs){S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent='Absorbansi diisi manual. Pastikan nilai sesuai larutan, bobot, volume, dan pengenceran yang dipilih.'}S.spkC=+$('cAdd').value||0;renderRes()});
$('aU').addEventListener('change',()=>{if(!S.isAutoFillingAbs&&$('sampleAbsSource'))$('sampleAbsSource').textContent='Nilai absorbansi diinput atau diedit manual. Pengisian manual tetap didukung.'});
$('aSp').addEventListener('change',()=>{if(!S.isAutoFillingAbs&&$('spikeAbsSource'))$('spikeAbsSource').textContent='Nilai absorbansi sampel + spike diinput atau diedit manual.'});
$('applyLastRead').onclick=applyLastSimpleRead;
$('applyLastSpike').onclick=()=>{const r=S.lastSampleRead;if(!r||r.key!=='spike'){toast('Belum ada pembacaan sampel + spike terakhir. Ukur sampel + spike pada Simple Reads dahulu.');return}applyLastSimpleRead()};
$('testWeight').oninput=()=>{const key=S.solutionKey||'',value=parseFloat($('testWeight').value);if(!Number.isFinite(value)||value<=0)return;if(key.startsWith('pres_'))S.precisionWeights[key]=value;else if(key.startsWith('akurasi_'))S.accuracyWeights[key]=value;else return;$('massa').value=value;if($('aU').value){$('aU').value='';S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent='Bobot berubah setelah pembacaan. Ukur ulang sampel dengan bobot terbaru atau isi absorbansi manual yang sesuai.'}const tableInput=$('testWeightSummary').querySelector(`[data-weight-key="${key}"]`);if(tableInput&&document.activeElement!==tableInput)tableInput.value=value.toFixed(4);updateWeightNominalCells();renderRes()};
$('massa').addEventListener('change',()=>{const key=S.solutionKey||'',value=parseFloat($('massa').value);if((key.startsWith('pres_')||key.startsWith('akurasi_'))&&Number.isFinite(value)&&value>0){if(key.startsWith('pres_'))S.precisionWeights[key]=value;else S.accuracyWeights[key]=value;$('testWeight').value=value.toFixed(4);const tableInput=$('testWeightSummary').querySelector(`[data-weight-key="${key}"]`);if(tableInput)tableInput.value=value.toFixed(4);updateWeightNominalCells()}});
['testVol','testDF'].forEach(id=>$(id).addEventListener('input',()=>{S.testVolumeMl=testVolumeMl();S.testDilutionFactor=testDilutionFactor();if((S.solutionKey||'').startsWith('pres_')||(S.solutionKey||'').startsWith('akurasi_')){if($('aU').value){$('aU').value='';S.autoAbsKey=null;if($('sampleAbsSource'))$('sampleAbsSource').textContent='Volume atau faktor pengenceran berubah. Ukur ulang dengan preparasi terbaru atau isi absorbansi manual yang sesuai.'}}updateWeightNominalCells();renderRes()}));
$('aRefresh').onclick=()=>{if(S.job||S.batchMeasuring){toast('Jeda atau hentikan pengukuran sebelum mereset tabel.');return}S.simpleHistory=[];drawTable();toast('Riwayat Simple Reads telah direset. Data kalibrasi tidak dihapus.')};
$('bL').onclick=()=>{if(!S.identifyMode){toast('Aktifkan Transparan atau Kenali Bagian terlebih dahulu.');return}S.lbl=S.lbl?0:1;$('bL').classList.toggle('on',!!S.lbl);if(S.lbl)showIdentifyGuide()};
$('focusPause').onclick=()=>{$('bPause').click()};
$('focusStop').onclick=()=>{S.batchMeasuring=0;S.measureVisual=0;S.paused=0;finishJob();syncAnimationFocusHUD();toast('Proses dihentikan. Tampilan akan dikembalikan.');};
$('focusIdentify').onclick=()=>{if(!(S.job||S.batchMeasuring))return;if(!S.paused)S.paused=1;exitAnimationFocus();syncProcessButtons();$('bIdentify').click();syncAnimationFocusHUD()};
$('bPause').onclick=()=>{const running=!!(S.job||S.batchMeasuring);if(S.paused){if(S.identifyMode){toast('Tutup mode Kenali Bagian sebelum melanjutkan animasi/proses.');return}S.paused=0;if(S.resumeAppAfterIdentify){S.app=1;$('app').hidden=false;S.resumeAppAfterIdentify=0;S.appMinimized=0;drawScreen()}if(running)enterAnimationFocus();toast(running?'Pengukuran dan animasi dilanjutkan.':'Animasi instrumen dilanjutkan.')}else{S.paused=1;toast(running?'Pengukuran dan animasi dijeda.':'Animasi instrumen dijeda. Klik Lanjutkan animasi untuk meneruskan.')}syncProcessButtons();syncAnimationFocusHUD()};
$('bIdentify').onclick=()=>{
 if(!S.identifyMode){
  if((S.job||S.batchMeasuring)&&!S.paused){S.paused=1;toast('Pengukuran dijeda untuk mengenali bagian alat.')}
  if(S.app){S.resumeAppAfterIdentify=1;S.app=0;$('app').hidden=true;drawScreen()}
  S.identifyMode=1;S.lbl=1;syncX();$('bL').classList.add('on');showIdentifyGuide();toast('Mode Kenali Bagian aktif. Klik label atau komponen untuk membaca penjelasannya.')
 }else{
  S.identifyMode=0;S.lbl=0;syncX();$('bL').classList.remove('on');
  if(S.resumeAppAfterIdentify&&!S.paused){S.app=1;$('app').hidden=false;S.resumeAppAfterIdentify=0;drawScreen()}
  toast('Mode Kenali Bagian ditutup. Jika pengukuran dijeda, tekan Lanjutkan proses.')
 }
 syncProcessButtons();$('bX').classList.toggle('on',!!(S.xray||S.identifyMode||S.measureVisual));
};
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
// Cover awal, menu tiga titik, dan panduan Cara Kerja.
$('enterApp').onclick=()=>{document.getElementById('welcome').hidden=true;document.body.classList.add('started');resize();toast('Simulasi siap. Buka menu ⋮ di bagian atas untuk melihat Cara Kerja.')};
$('menuBtn').onclick=()=>{$('menuDrop').hidden=!$('menuDrop').hidden};
$('openHowto').onclick=()=>{$('menuDrop').hidden=true;$('howtoBackdrop').hidden=false};
$('closeHowto').onclick=()=>{$('howtoBackdrop').hidden=true};
$('howtoBackdrop').addEventListener('click',e=>{if(e.target===$('howtoBackdrop'))$('howtoBackdrop').hidden=true});
document.addEventListener('click',e=>{if(!$('menuWrap').contains(e.target))$('menuDrop').hidden=true});
$('lmMode').onchange=e=>{S.lampMode=e.target.value};$('lmColor').oninput=e=>{S.lampColor=e.target.value;S.lampMode='manual';$('lmMode').value='manual'};$('lmI').oninput=e=>{S.lampI=+e.target.value};document.querySelectorAll('[data-lc]').forEach(b=>b.onclick=()=>{S.lampColor=b.dataset.lc;$('lmColor').value=b.dataset.lc;S.lampMode='manual';$('lmMode').value='manual'});
function switchToTab(tab){
 if(S.job||S.batchMeasuring){toast('Selesaikan atau jeda pengukuran sebelum mengganti mode.');return false}
 S.tab=tab;document.querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('on',x.dataset.t===S.tab));
 $('p-scan').hidden=S.tab!=='scan';$('p-simple').hidden=S.tab!=='simple';$('p-conc').hidden=S.tab!=='conc';$('scanBox').hidden=S.tab!=='scan';$('simpleHistorySection').hidden=S.tab!=='simple';$('cres').hidden=S.tab!=='conc';
 $('graphHeading').textContent=S.tab==='conc'?'Kurva kalibrasi: X = Konsentrasi (ppm), Y = Absorbansi (AU)':S.tab==='scan'?'Spektrum: Panjang gelombang (nm) dan absorbansi':'Grafik pembacaan Simple Reads';
 if(S.tab==='conc')renderConc();S.res=null;updateSolutionGate();drawTable();drawChart();return true;
}
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>switchToTab(b.dataset.t));
const V={front:[[-1,5.5,12],[1,.8,0]],top:[[1,16,.1],[1,0,0]],back:[[1,5,-12],[1,.8,0]],side:[[14,4,3],[0,.8,0]],inst:[[-3.2,4.5,6.5],[-3.2,.7,.5]],cuv:[[-3.2,2.6,3.6],[-3.2,.8,.9]],mon:[[5,2.2,4.5],[5,1.2,-.6]],opt:[[-3.2,7.2,2.6],[-3.2,.8,-.1]],lamp:[[-6.8,2.2,.9],[-5.6,.8,-1.5]]};
let fly=null;function flyV(k){const v=V[k];fly={t:0,p0:cam.position.clone(),t0:ctl.target.clone(),p1:new THREE.Vector3(...v[0]),t1:new THREE.Vector3(...v[1])}}document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>flyV(b.dataset.v));
// klik 3D
const rc=new THREE.Raycaster(),mp=new THREE.Vector2();let dn=null;
function pick(e){const r=ren.domElement.getBoundingClientRect();mp.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);rc.setFromCamera(mp,cam);const h=rc.intersectObjects(clickables,false);return h.length?h[0].object.userData.key:null}
ren.domElement.addEventListener('pointerdown',e=>dn=[e.clientX,e.clientY]);
ren.domElement.addEventListener('pointerup',e=>{if(!dn||Math.hypot(e.clientX-dn[0],e.clientY-dn[1])>5)return;const k=pick(e);if(!k)return;if(S.identifyMode)showInfo(k);
 if(k==='upsbtn')power('ups');else if(k==='sw')power('inst');else if(k==='pcbtn')power('pc');else if(k==='monbtn')power('mon');else if(k==='lid')toggleLid();else if(k==='cuv')toggleCuv();else if(k==='screen'&&desk())openApp(true)});
ren.domElement.addEventListener('pointermove',e=>{ren.domElement.style.cursor=pick(e)?'pointer':'default'});
function resize(){const rect=ren.domElement.getBoundingClientRect(),w=Math.max(1,rect.width),h=Math.max(1,rect.height);ren.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}addEventListener('resize',resize);resize();
// ---------- loop
const B={vis:0,T:1,sOn:true};const clk=new THREE.Clock();let xk=0,uiT=0,chA=0,lastLamp=0;const col=new THREE.Color(),beamCol=new THREE.Color(),tA=new THREE.Color(),tB=new THREE.Color();
setLiq();syncX();$('animationFocusHud').hidden=true;$('conc').disabled=true;$('opticalStatus').hidden=true;$('cres').hidden=true;$('simpleHistorySection').hidden=true;$('graphHeading').textContent='Spektrum: Panjang gelombang (nm) dan absorbansi';updatePanelToggleUI();updateTestWeightUI(S.solutionKey);updateSolutionGate();syncProcessButtons();drawTable();updateRoomVisibility();
function loop(){requestAnimationFrame(loop);const dt=Math.min(clk.getDelta(),.1);const animDt=S.paused?0:dt;if(!S.paused)S.visualTime+=dt;const visualMs=S.visualTime*1000;
 if(S.inst)S.warm=Math.min(WARM,S.warm+animDt);if(S.pc&&!S.booted){S.bootT+=animDt;if(S.bootT>4)S.booted=1}
 runJob(animDt);syncAnimationFocus();
  if(fly){fly.t=Math.min(1,fly.t+dt/.9);const k=fly.t*fly.t*(3-2*fly.t);cam.position.lerpVectors(fly.p0,fly.p1,k);ctl.target.lerpVectors(fly.t0,fly.t1,k);if(fly.t>=1)fly=null}
 ctl.autoRotate=!!S.autoRotateWanted&&!S.paused;ctl.update();
 updateRoomVisibility();
 // Animasi mekanik mengikuti satu clock. Saat dijeda, posisi semua komponen tetap konstan.
 const lt=S.lid?-1.6:0;lid.rotation.x+=(lt-lid.rotation.x)*Math.min(1,animDt*5);
 cuvK+=((S.cuv?1:0)-cuvK)*Math.min(1,animDt*5);cuvS.position.set(1.6*(1-cuvK),.18+(.8-.18)*cuvK+Math.sin(Math.PI*cuvK)*.5,3+(.95-3)*cuvK);
 rocker.rotation.x=S.inst?-.3:.3;ledM.emissive.setHex(S.inst?0x00ff00:0);ledM.color.setHex(S.inst?0x22ff22:0x114411);
 upsLed.forEach((l,i)=>{const on=S.ups;l.material.emissive.setHex(on?0x00ff00:0);l.material.color.setHex(on?0x22ff22:0x114411)});
 pcLed.material.emissive.setHex(S.pc?0x00ff00:0);monLed.material.emissive.setHex(S.mon?0x00ff00:0);
 const transparentTarget=(S.xray||S.identifyMode||S.measureVisual)?1:0;xk+=(transparentTarget-xk)*Math.min(1,animDt*4);shW.opacity=shD.opacity=1-.88*xk;shW.depthWrite=shD.depthWrite=xk<.05;shells.forEach(s=>{s.e.visible=xk>.02;s.e.material.opacity=(S.identifyMode?xk*.9:0)});
 // Simulasi proses optik: sumber broadband -> kisi pemilih λ -> chopper double-beam -> kuvet -> detektor.
 const lampOn=S.inst&&S.warm>2;
 const processRunning=!!(S.job||S.batchMeasuring);
 // Komponen optik internal, lampu, halo, dan berkas hanya boleh tampil saat Transparan/Kenali aktif atau animasi pengukuran sedang berjalan.
 const transparentOptics=!!(S.xray||S.identifyMode||S.measureVisual||xk>.25);
 const sourceGlowBoost=(transparentOptics&&processRunning)?1.9:(transparentOptics?1.35:1);
 const LA=lampOn?(S.lam>=350?'v':'d'):null,mn=S.lampMode==='manual',cV=mn?tA.set(S.lampColor):tA.set(AUTO_V),cD=mn?tB.set(S.lampColor):tB.set(AUTO_D),fl=1+.055*Math.sin(visualMs*.045);
 const sourceBeamCol=LA==='d'?cD:LA==='v'?cV:col.set(0xbfd7ed);
 lampVM.color.copy(LA==='v'&&transparentOptics?cV:new THREE.Color(0x442200));lampVM.emissive.copy(cV).multiplyScalar(transparentOptics&&LA==='v'?4.2*S.lampI*fl*sourceGlowBoost:0);
 bulbVM.color.copy(transparentOptics&&LA==='v'?cV:cOff);bulbVM.opacity=transparentOptics&&LA==='v'?.99:0;bulbVM.emissive.copy(cV).multiplyScalar(transparentOptics&&LA==='v'?2.8*S.lampI*fl*sourceGlowBoost:0);
 lampD.material.color.copy(transparentOptics&&LA==='d'?cD:cOff);lampD.material.opacity=transparentOptics&&LA==='d'?.99:0;lampD.material.emissive.copy(cD).multiplyScalar(transparentOptics&&LA==='d'?3.8*S.lampI*fl*sourceGlowBoost:0);
 d2Win.material.color.copy(transparentOptics&&LA==='d'?cD:cOff);d2Win.material.emissive.copy(cD).multiplyScalar(transparentOptics&&LA==='d'?4.8*S.lampI*fl*sourceGlowBoost:0);
 lightV.color.copy(cV);lightV.intensity=transparentOptics&&LA==='v'?(1.1+2.4*xk)*S.lampI*sourceGlowBoost:0;lightD.color.copy(cD);lightD.intensity=transparentOptics&&LA==='d'?(1.1+2.4*xk)*S.lampI*sourceGlowBoost:0;
 sel.position.y+=((LA==='d'?BY:BY+.38)-sel.position.y)*Math.min(1,animDt*6);
 // Chopper berputar lebih lambat; jalur optik digambar bersamaan, sedangkan partikel foton tetap memvisualisasikan timing sampel/referensi Cary 100.
 chop.rotation.y+=(S.paused?0:(S.inst?(S.job?1.15:.42):0))*dt;grat.rotation.y=(S.lam-190)/710*.8;
 beamCol.setRGB(...W(S.lam));col.copy(beamCol);mC.color.copy(sourceBeamCol);mMono.color.copy(beamCol);[mS1,mS2,mR].forEach(m=>m.color.copy(beamCol));mLV.color.copy(cV);mLD.color.copy(cD);
 const T=S.cuv&&!S.lid?Math.pow(10,-specA(S.lam)):1;const vis=S.beam&&lampOn&&transparentOptics?1:0;const sOn=Math.sin(chop.rotation.y*2)>0;B.vis=vis;B.T=T;B.sOn=sOn;
 mC.opacity=.88*vis;mMono.opacity=.94*vis;mLV.opacity=.96*(S.beam&&transparentOptics&&LA==='v'?1:0);mLD.opacity=.96*(S.beam&&transparentOptics&&LA==='d'?1:0);mS1.opacity=.92*vis;mR.opacity=.92*vis;mS2.opacity=.92*vis*(.08+.92*T);
 const opticReveal=!!(S.xray||S.identifyMode||S.measureVisual||xk>.35);
 const fanIndex=Math.max(0,Math.min(spectrumPalette.length-1,Math.round((Math.max(200,Math.min(700,S.lam))-200)/500*(spectrumPalette.length-1))));
 spectralFan.forEach((f,i)=>{f.mat.opacity=opticReveal&&vis?(i===fanIndex?.78:.045):0});
 beamGlowMeshes.forEach(q=>{q.glow.material.color.copy(q.base.color);q.glow.material.opacity=transparentOptics?Math.min(.42,q.base.opacity*.4):0;q.glow.visible=transparentOptics&&q.base.opacity>.018});
 // Detektor menerima sinyal yang berdenyut; intensitas ikut berkurang mengikuti absorbansi sampel.
 const pulseBeat=.72+.28*Math.sin(visualMs*.012);detectorSignalMat.color.copy(beamCol);detectorSignalMat.emissive.copy(beamCol).multiplyScalar(vis?(.15+T*.95)*pulseBeat:0);detectorSignalMat.opacity=vis?(.22+.62*T*pulseBeat):.08;detectorSignal.scale.setScalar(.7+.42*pulseBeat*T);
 pmtM.emissive.setRGB(beamCol.r*(.15+T*.8)*vis*pulseBeat,beamCol.g*(.15+T*.8)*vis*pulseBeat,beamCol.b*(.15+T*.8)*vis*pulseBeat);
 halos.forEach(q=>{const lh=q.t==='lv'||q.t==='ld';q.m.color.copy(q.t==='lv'?cV:q.t==='ld'?cD:beamCol);const f=lh?((q.t==='lv'?LA==='v':LA==='d')?(1+.09*Math.sin(visualMs*.045))*Math.min(1.15,.65+.45*S.lampI):0):q.t==='c'?1:q.t==='s1'?(sOn?1:.12):q.t==='s2'?(sOn?1:.12)*(.08+.92*T):q.t==='r'?(sOn?.12:1):.25+.75*T;if(lh&&q.s){const glowScale=q.baseScale*(transparentOptics?1.55:1)*(processRunning?1.18:1);q.s.scale.set(glowScale,glowScale,1);q.s.renderOrder=transparentOptics?30:11;q.s.visible=transparentOptics}q.m.opacity=transparentOptics?Math.min(1,(lh?.99:.9)*(lh?1:vis)*f*(lh?sourceGlowBoost:1)):0});
 // Foton bergerak perlahan sepanjang jalur 3D; setelah chopper, partikel sampel/referensi mengikuti timing bergiliran.
 if(!S.paused)S.opticalClock=(S.opticalClock||0)+dt*((S.job||S.batchMeasuring)?0.55:0.18);
 const photonSpeed=(S.job||S.batchMeasuring)?1.45:0.62;
 pulses.forEach(p=>{
  if(!S.paused)p.u+=photonSpeed*dt;
  const u=((p.u%p.r.L)+p.r.L)%p.r.L,q=posAt(p.r,u);
  const pastChopper=u>preChopperLen;const branchOn=!pastChopper||(p.k===0?sOn:!sOn);const active=!!vis&&branchOn;p.active=active;
  const photonColor=u<preGratingLen?sourceBeamCol:beamCol;
  p.s.position.set(q[0],BY+.025,q[1]);p.glow.position.set(q[0],BY+.04,q[1]);
  p.mat.color.copy(photonColor);p.mat.opacity=active?.98:.06;p.s.visible=!!vis;
  p.glow.material.color.copy(photonColor);p.glow.material.opacity=active?.78:.025;p.glow.visible=!!vis;
  const absorb=(p.k===0&&u>dCuv)?(.42+.58*T):1;const sz=active?.85+.2*pulseBeat:.65;
  p.s.scale.setScalar(.038*sz*absorb);p.glow.scale.set(.25*sz*absorb,.25*sz*absorb,1);
 });
 // UI
 drawScreen();updLb();drawSch();if(S.focusRestore)syncAnimationFocusHUD();uiT+=dt;if(uiT>.15){uiT=0;renderUI();renderOpticalStatus();if(S.app&&!S.appMinimized){if(S.tab==='scan'||S.tab==='conc'||S.job)drawChart();if(S.tab==='simple')drawTable()}}
 ren.render(scene,cam)}
renderConc();
updateTestWeightSummary();
loop();
}
</script></body></html>

"""

components.html(
    HTML,
    height=height,
    scrolling=False,
)
