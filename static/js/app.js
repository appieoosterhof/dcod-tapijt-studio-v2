/* RepeatTile Studio — Frontend logica */

let currentTileSvg = null;
let currentRepeatSvg = null;

// Zet een SVG (base64) om naar een lage-resolutie PNG op een canvas en toont
// die als bron van het preview-element. Zo komt de schaalbare SVG niet als
// downloadbare afbeelding in beeld.
function svgNaarPngPreview(svgB64, elementId, breedte) {
  try {
    const doel = document.getElementById(elementId);
    if (doel) {
      // SVG rechtstreeks tonen (geen canvas-tussenstap; voorkomt vervorming
      // bij SVG's met alleen viewBox). Cachebuster via leegmaken + nieuwe src.
      doel.src = '';
      doel.src = 'data:image/svg+xml;base64,' + svgB64;
    }
  } catch (e) {
    console.log('Preview-render fout:', e);
  }
}
let currentDessinRef = null;
let currentInfo = null;
let activeTab = 'repeat';

// ─── API sleutel opslaan ──────────────────────────────────────────────────────

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('rt_api_key');
  if (saved) {
    document.getElementById('apiKey').value = saved;
    document.getElementById('rememberKey').checked = true;
  }
});

function toggleApiKey() {
  const el = document.getElementById('apiKey');
  el.type = el.type === 'password' ? 'text' : 'password';
}

function handleRemember() {
  const checked = document.getElementById('rememberKey').checked;
  if (!checked) localStorage.removeItem('rt_api_key');
}

// ─── Prompt suggesties ────────────────────────────────────────────────────────

function setPrompt(text, btn) {
  document.getElementById('prompt').value = text;
  document.getElementById('prompt').focus();
  if (btn && btn.parentElement) {
    btn.parentElement.querySelectorAll('.chip').forEach(function(el){ el.classList.remove('sub-active'); });
    btn.classList.add('sub-active');
  }
}

// ─── Tabs ─────────────────────────────────────────────────────────────────────

function switchTab(tab, btn) {
  activeTab = tab;
  document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const repeat = document.getElementById('previewRepeat');
  const tile = document.getElementById('previewTile');
  if (tab === 'repeat') {
    repeat.style.display = currentRepeatSvg ? 'block' : 'none';
    tile.style.display = 'none';
  } else {
    tile.style.display = currentTileSvg ? 'block' : 'none';
    repeat.style.display = 'none';
  }
}

// ─── Genereer dessin ──────────────────────────────────────────────────────────

async function generate() {
  const apiKey = document.getElementById('apiKey').value.trim();
  const prompt = document.getElementById('prompt').value.trim();
  const tileCm = document.getElementById('tileCm').value;
  const repeatType = 'full';
  const dpi = document.getElementById('dpi').value;

  if (!apiKey) return setStatus('Vul eerst uw API-sleutel in.', 'error');
  if (!prompt) return setStatus('Vul een dessin beschrijving in.', 'error');

  // API sleutel opslaan indien gewenst
  if (document.getElementById('rememberKey').checked) {
    localStorage.setItem('rt_api_key', apiKey);
  }

  setLoading(true);
  setStatus('AI analyseert uw prompt...', '');

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, api_key: apiKey, tile_cm: tileCm, repeat_type: repeatType, dpi, motief_schaal: (parseInt(document.getElementById('motiefSchaal')?.value) || 100), aangepast_palet: (document.getElementById('gebruikKleuren')?.checked ? { background: document.getElementById('kleur0')?.value, primary: document.getElementById('kleur1')?.value, secondary: document.getElementById('kleur2')?.value, accent1: document.getElementById('kleur3')?.value, accent2: document.getElementById('kleur4')?.value } : null) })
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      setStatus(data.error || 'Er ging iets mis. Probeer opnieuw.', 'error');
      setLoading(false);
      return;
    }

    // SVG data opslaan
    currentTileSvg = data.tile_svg_b64;
    currentRepeatSvg = data.repeat_svg_b64;
    currentInfo = data.info;

    // Preview tonen als lage-resolutie PNG (SVG niet zichtbaar/downloadbaar)
    svgNaarPngPreview(data.tile_svg_b64, 'previewTile', 350);
    svgNaarPngPreview(data.repeat_svg_b64, 'previewRepeat', 700);
    document.getElementById('previewTile').style.display = activeTab === 'tile' ? 'block' : 'none';
    document.getElementById('previewRepeat').style.display = activeTab === 'repeat' ? 'block' : 'none';
    document.getElementById('emptyState').style.display = 'none';

    // Badges
    const badges = document.getElementById('badges');
    badges.style.display = 'flex';
    document.getElementById('badgeDpi').textContent = dpi + ' DPI';
    document.getElementById('badgeStyle').textContent = data.info.style;

    // Info kaarten
    const infoCards = document.getElementById('infoCards');
    infoCards.style.display = 'grid';
    document.getElementById('infoDpi').textContent = dpi + ' DPI';
    document.getElementById('infoPx').textContent = data.info.tile_px + ' × ' + data.info.tile_px + ' px';
    document.getElementById('infoStyle').textContent = data.info.style;
    document.getElementById('infoRepeat').textContent = repeatType;

    // Beschrijving
    const descBox = document.getElementById('descBox');
    descBox.style.display = 'flex';
    document.getElementById('descText').textContent = data.info.description || '—';

    // Verkoopblokken: Sfeer / Geschikt voor / Ontwerpvisie (vult bij ELKE generatie)
    const vulChips = (id, arr) => {
      const el = document.getElementById(id);
      if (!el) return;
      el.innerHTML = '';
      (arr || []).forEach(w => {
        if (!w) return;
        const s = document.createElement('span');
        s.textContent = w;
        el.appendChild(s);
      });
    };
    vulChips('wbSfeer', data.info.sfeer);
    vulChips('wbGeschikt', data.info.geschikt_voor);
    const wbVisie = document.getElementById('wbVisie');
    if (wbVisie) wbVisie.textContent = data.info.ontwerpvisie || data.info.description || '—';

    // Kleurpalet
    const paletteRow = document.getElementById('paletteRow');
    paletteRow.style.display = 'flex';
    const swatches = document.getElementById('paletteSwatches');
    swatches.innerHTML = '';
    const colors = data.info.colors || {};
    Object.entries(colors).forEach(([name, hex]) => {
      const s = document.createElement('div');
      s.className = 'swatch';
      s.style.background = hex;
      s.title = name + ': ' + hex;
      swatches.appendChild(s);
    });

    // Export knoppen tonen
    document.getElementById('exportRow').style.display = 'flex';
  document.getElementById('bestelRow').style.display = 'block';
  const now = new Date();
  currentDessinRef = 'DCOD-' + now.getFullYear() + String(now.getMonth()+1).padStart(2,'0') + String(now.getDate()).padStart(2,'0') + '-' + String(now.getHours()).padStart(2,'0') + String(now.getMinutes()).padStart(2,'0') + String(now.getSeconds()).padStart(2,'0');
  const refEl = document.getElementById('dessinRef');
  if (refEl) refEl.textContent = currentDessinRef;

    setStatus('✓ Alle dessins zijn vectorgebaseerd. Deze preview is gemaakt in een lage PNG-resolutie; bij bestelling wordt het originele, schaalbare vectorbestand naar DCOD doorgestuurd voor de productie van uw tapijt.', 'success');

  } catch (err) {
    setStatus('Verbindingsfout. Is de server actief?', 'error');
    console.error(err);
  }

  setLoading(false);
}

// ─── Export functies ──────────────────────────────────────────────────────────

async function exportFile(format, type) {
  if (!currentTileSvg || !currentRepeatSvg) {
    setStatus('Genereer eerst een dessin.', 'error');
    return;
  }

  const svgB64 = type === 'tile' ? currentTileSvg : currentRepeatSvg;
  const cm = document.getElementById('tileCm').value;
  const dpi = document.getElementById('dpi').value;
  const repeatType = 'full';
  const ts = Date.now();
  const filename = `dessin_${type}_${cm}cm_${dpi}dpi_${ts}.${format}`;

  setStatus(`Exporteren als ${format.toUpperCase()}...`, '');

  try {
    const response = await fetch(`/api/export/${format}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ svg_b64: svgB64, dpi: parseInt(dpi), tile_cm: parseInt(cm), filename })
    });

    if (!response.ok) {
      const err = await response.json();
      setStatus(err.error || 'Export mislukt.', 'error');
      return;
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setStatus(`✓ ${format.toUpperCase()} gedownload: ${filename}`, 'success');

  } catch (err) {
    setStatus('Export mislukt. Probeer opnieuw.', 'error');
    console.error(err);
  }
}

// ─── Hulpfuncties ─────────────────────────────────────────────────────────────

function setStatus(msg, type) {
  const el = document.getElementById('statusMsg');
  el.textContent = msg;
  el.className = 'status-msg' + (type ? ' ' + type : '');
}

function setLoading(loading) {
  const btn = document.getElementById('btnGenerate');
  const icon = document.getElementById('btnIcon');
  const text = document.getElementById('btnText');
  btn.disabled = loading;
  if (loading) {
    btn.classList.add('loading');
    icon.textContent = '↻';
    text.textContent = 'Genereren...';
  } else {
    btn.classList.remove('loading');
    icon.textContent = '✦';
    text.textContent = 'Genereer dessin';
  }
}

// Enter in prompt veld = genereren
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('prompt').addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) generate();
  });
});

async function verstuurBestelling() {
  const naam = document.getElementById('bestelNaam').value.trim();
  const email = document.getElementById('bestelEmail').value.trim();
  const telefoon = document.getElementById('bestelTelefoon').value.trim();
  const wensen = document.getElementById('bestelWensen').value.trim();
  if (!naam || !email) {
    document.getElementById('bestelFout').textContent = 'Vul uw naam en e-mailadres in zodat wij u kunnen bereiken.';
    document.getElementById('bestelFout').style.display = 'block';
    return;
  }
  const bedrijf = document.getElementById('bestelBedrijf')?.value.trim() || '';
  const dessin_info = document.getElementById('descText')?.textContent || '';
  const dessin_ref = currentDessinRef || 'Onbekend';
  const repeat_type = 'Full repeat';
  const tegel_maat = document.getElementById('tileCm')?.options[document.getElementById('tileCm')?.selectedIndex]?.text || '';
  const resolutie = document.getElementById('dpi')?.options[document.getElementById('dpi')?.selectedIndex]?.text || '';
  const datum = new Date().toLocaleDateString('nl-NL', {day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit'});

  let img_b64 = '';
  try {
    const canvas = document.createElement('canvas');
    const previewImg = document.getElementById('previewRepeat');
    if (previewImg && previewImg.naturalWidth > 0) {
      canvas.width = previewImg.naturalWidth;
      canvas.height = previewImg.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(previewImg, 0, 0);
      img_b64 = canvas.toDataURL('image/png').split(',')[1];
    }
  } catch(e) { console.log('Afbeelding niet beschikbaar:', e); }
  slaContactGegevensOp(naam, email, telefoon);
  const product = document.querySelector('input[name="product"]:checked')?.value || 'Printtapijt';
  const breedte = document.getElementById('bestelBreedte')?.value || '';
  const lengte = document.getElementById('bestelLengte')?.value || '';
  const m2 = breedte && lengte ? ((breedte * lengte) / 10000).toFixed(2) + ' m²' : 'Niet opgegeven';
  document.getElementById('bestelFout').style.display = 'none';
  document.getElementById('btnVerstuur').textContent = 'Verzenden...';
  document.getElementById('btnVerstuur').disabled = true;
  try {
  const staaltje = document.getElementById('bestelSaaltje')?.checked ? 'Ja' : 'Nee';
  const straat = document.getElementById('bestelStraat')?.value || '';
  const postcode = document.getElementById('bestelPostcode')?.value || '';
  const plaats = document.getElementById('bestelPlaats')?.value || '';
  const land = document.getElementById('bestelLand')?.value || 'Nederland';
  const adres = document.getElementById('bestelAdres')?.value || '';
  const res = await fetch('/api/bestelling', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ kleuren: ([0,1,2,3,4].map(function(i){var lbls=['achtergrond','primair','secondair','accent 1','accent 2'];var hx=(document.getElementById('kleur'+i+'hex')||document.getElementById('kleur'+i)||{}).value||'';var r=(document.getElementById('kleur'+i+'r')||{}).value||'';var g=(document.getElementById('kleur'+i+'g')||{}).value||'';var b=(document.getElementById('kleur'+i+'b')||{}).value||'';return {label:lbls[i],hex:hx,r:r,g:g,b:b};})), naam, email, telefoon, bedrijf, wensen, dessin_info, dessin_ref, repeat_type, tegel_maat, resolutie, datum, img_b64, tile_svg_b64: currentTileSvg, repeat_svg_b64: currentRepeatSvg, product, afmeting: breedte && lengte ? breedte + ' x ' + lengte + ' cm (' + m2 + ')' : 'Niet opgegeven', staaltje, straat, postcode, plaats, land })
    });
    const data = await res.json();
    if (data.success) {
      document.getElementById('bestelModal').style.display = 'none';
      alert('Uw aanvraag is verzonden! U ontvangt een kopie per e-mail. Wij nemen binnen 2 werkdagen contact met u op.');
    } else {
      document.getElementById('bestelFout').textContent = 'Fout bij verzenden. Bel ons direct.';
      document.getElementById('bestelFout').style.display = 'block';
      document.getElementById('btnVerstuur').textContent = 'Stuur offerte aanvraag';
      document.getElementById('btnVerstuur').disabled = false;
    }
  } catch(e) {
    document.getElementById('bestelFout').textContent = 'Fout bij verzenden. Bel ons direct.';
    document.getElementById('bestelFout').style.display = 'block';
    document.getElementById('btnVerstuur').textContent = 'Stuur offerte aanvraag';
    document.getElementById('btnVerstuur').disabled = false;
  }
}

// Kleurenpalet synchronisatie
function rgbToHex(r, g, b) {
  return '#' + [r,g,b].map(x => Math.max(0,Math.min(255,parseInt(x)||0)).toString(16).padStart(2,'0')).join('');
}
function hexToRgbParts(hex) {
  return [parseInt(hex.slice(1,3),16), parseInt(hex.slice(3,5),16), parseInt(hex.slice(5,7),16)];
}
function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
}
function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return r + ',' + g + ',' + b;
}
document.addEventListener('DOMContentLoaded', () => {
  for (let i = 0; i < 5; i++) {
    const picker = document.getElementById('kleur' + i);
    const hex = document.getElementById('kleur' + i + 'hex');
    const rEl = document.getElementById('kleur' + i + 'r');
    const gEl = document.getElementById('kleur' + i + 'g');
    const bEl = document.getElementById('kleur' + i + 'b');
    if (!picker) continue;
    const syncFromHex = (h) => {
      if (hex) hex.value = h;
      picker.value = h;
      const [r,g,b] = hexToRgbParts(h);
      if (rEl) rEl.value = r;
      if (gEl) gEl.value = g;
      if (bEl) bEl.value = b;
    };
    const syncFromRgb = () => {
      const r = rEl?.value||0, g = gEl?.value||0, b = bEl?.value||0;
      const h = rgbToHex(r,g,b);
      picker.value = h;
      if (hex) hex.value = h;
    };
    picker.addEventListener('input', () => syncFromHex(picker.value));
    if (hex) hex.addEventListener('input', () => { if(/^#[0-9A-Fa-f]{6}$/.test(hex.value)) syncFromHex(hex.value); });
    if (rEl) rEl.addEventListener('input', syncFromRgb);
    if (gEl) gEl.addEventListener('input', syncFromRgb);
    if (bEl) bEl.addEventListener('input', syncFromRgb);
  }
});

// Contactgegevens opslaan en laden
function laadContactGegevens() {
  const naam = localStorage.getItem('bestel_naam') || '';
  const email = localStorage.getItem('bestel_email') || '';
  const telefoon = localStorage.getItem('bestel_telefoon') || '';
  const bedrijf = localStorage.getItem('bestel_bedrijf') || '';
  const straat = localStorage.getItem('bestel_straat') || '';
  const postcode = localStorage.getItem('bestel_postcode') || '';
  const plaats = localStorage.getItem('bestel_plaats') || '';
  if (naam) document.getElementById('bestelNaam').value = naam;
  if (email) document.getElementById('bestelEmail').value = email;
  if (telefoon) document.getElementById('bestelTelefoon').value = telefoon;
  if (bedrijf) document.getElementById('bestelBedrijf').value = bedrijf;
  if (straat) document.getElementById('bestelStraat').value = straat;
  if (postcode) document.getElementById('bestelPostcode').value = postcode;
  if (plaats) document.getElementById('bestelPlaats').value = plaats;
  if (document.getElementById('bestelNaam')) document.getElementById('bestelNaam').value = naam;
  if (document.getElementById('bestelEmail')) document.getElementById('bestelEmail').value = email;
  if (document.getElementById('bestelTelefoon')) document.getElementById('bestelTelefoon').value = telefoon;
}

function slaContactGegevensOp(naam, email, telefoon) {
  localStorage.setItem('bestel_naam', naam);
  localStorage.setItem('bestel_email', email);
  localStorage.setItem('bestel_telefoon', telefoon);
  const b = document.getElementById('bestelBedrijf')?.value || '';
  const s = document.getElementById('bestelStraat')?.value || '';
  const p = document.getElementById('bestelPostcode')?.value || '';
  const pl = document.getElementById('bestelPlaats')?.value || '';
  if (b) localStorage.setItem('bestel_bedrijf', b);
  if (s) localStorage.setItem('bestel_straat', s);
  if (p) localStorage.setItem('bestel_postcode', p);
  if (pl) localStorage.setItem('bestel_plaats', pl);
}

// Staaltje tonen/verbergen
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('bestelSaaltje')?.addEventListener('change', function() {
    document.getElementById('bestelAdresVeld').style.display = this.checked ? 'block' : 'none';
  });
});

// M2 berekening
document.addEventListener('DOMContentLoaded', () => {
  function berekenM2() {
    const b = parseFloat(document.getElementById('bestelBreedte')?.value) || 0;
    const l = parseFloat(document.getElementById('bestelLengte')?.value) || 0;
    const m2 = b && l ? ((b * l) / 10000).toFixed(2) + ' m²' : '— m²';
    const el = document.getElementById('bestelM2');
    if (el) el.textContent = m2;
  }
  document.getElementById('bestelBreedte')?.addEventListener('input', berekenM2);
  document.getElementById('bestelLengte')?.addEventListener('input', berekenM2);
});


/* ---- Floorvisualizer: Bekijk in ruimte ---- */
(function(){
  var SRC = 600;

  /* ---- Mockup-configuratie ----
     Eenmalig gekalibreerde hoekpunten per mockup-foto. Geen interactieve
     kalibratietool: nieuwe mockups worden handmatig 1x uitgelijnd en hier
     als vaste waarden toegevoegd. floorPoints = vloer-hoekpunten als
     fractie van de scene (TL,TR,BL,BR). offsetX/offsetY (in px van de
     patroon-tegel) en rotation (in graden) zijn optioneel, default 0 --
     alleen invullen als een specifiek dessin/mockup dat nodig heeft. */
  window.ROOM_MOCKUPS = window.ROOM_MOCKUPS || {
    kantoor: {
      label: "Werkplekken & Kantoren",
      image: "/static/img/kantoor_meubellaag.png",
      floorPoints: [[0.150,0.547],[1.02,0.547],[-0.230,1.0],[1.107,1.0]],
      offsetX: 0,
      offsetY: 0,
      rotation: 0
    }
    /* Later toe te voegen, zodra de foto's + kalibratie klaar zijn:
    hotels: { label: "Hotels & Hospitality", image: "/static/img/hotels_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 },
    overheid: { label: "Overheid & Publieke gebouwen", image: "/static/img/overheid_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 },
    musea: { label: "Musea & Bibliotheken", image: "/static/img/musea_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 }
    */
  };

  var ACTIEVE_MOCKUP = "kantoor";
  function huidigeMockup(){ return window.ROOM_MOCKUPS[ACTIEVE_MOCKUP] || window.ROOM_MOCKUPS.kantoor; }

  var FR = huidigeMockup().floorPoints;
  function adj(m){return [m[4]*m[8]-m[5]*m[7],m[2]*m[7]-m[1]*m[8],m[1]*m[5]-m[2]*m[4],m[5]*m[6]-m[3]*m[8],m[0]*m[8]-m[2]*m[6],m[2]*m[3]-m[0]*m[5],m[3]*m[7]-m[4]*m[6],m[1]*m[6]-m[0]*m[7],m[0]*m[4]-m[1]*m[3]];}
  function mmm(a,b){var c=[];for(var i=0;i<3;i++)for(var j=0;j<3;j++){var s=0;for(var k=0;k<3;k++)s+=a[3*i+k]*b[3*k+j];c[3*i+j]=s;}return c;}
  function mmv(m,v){return [m[0]*v[0]+m[1]*v[1]+m[2]*v[2],m[3]*v[0]+m[4]*v[1]+m[5]*v[2],m[6]*v[0]+m[7]*v[1]+m[8]*v[2]];}
  function b2p(x1,y1,x2,y2,x3,y3,x4,y4){var m=[x1,x2,x3,y1,y2,y3,1,1,1];var v=mmv(adj(m),[x4,y4,1]);return mmm(m,[v[0],0,0,0,v[1],0,0,0,v[2]]);}
  function ruimteLayout(){
    var scene=document.getElementById('ruimteScene'); if(!scene) return;
    var W=scene.clientWidth, H=Math.round(W*1024/1536); scene.style.height=H+'px';
    var d=FR.map(function(p){return {x:p[0]*W,y:p[1]*H};});
    var s=b2p(0,0,SRC,0,0,SRC,SRC,SRC);
    var dd=b2p(d[0].x,d[0].y,d[1].x,d[1].y,d[2].x,d[2].y,d[3].x,d[3].y);
    var t=mmm(dd,adj(s));
    for(var i=0;i<9;i++) t[i]=t[i]/t[8];
    var m=[t[0],t[3],0,t[6],t[1],t[4],0,t[7],0,0,1,0,t[2],t[5],0,t[8]];
    var c=document.getElementById('ruimteCarpet');
    c.style.transform='matrix3d('+m.join(',')+')'; c.style.transformOrigin='0 0';
  }
  function ruimteScale(){
    var s=+document.getElementById('ruimteScale').value;
    var mockup=huidigeMockup();
    var offX=mockup.offsetX||0, offY=mockup.offsetY||0;
    var c=document.getElementById('ruimteCarpet');
    c.style.backgroundSize=s+'px '+s+'px';
    c.style.backgroundPosition=offX+'px '+offY+'px';
  }
  window.openVisualizer=function(){
    if(typeof currentTileSvg==='undefined' || !currentTileSvg){ alert('Genereer eerst een dessin.'); return; }
    var mockup=huidigeMockup();
    FR = mockup.floorPoints;
    document.getElementById('ruimteCarpet').style.backgroundImage="url('data:image/svg+xml;base64,"+currentTileSvg+"')";
    document.getElementById('ruimteMeubels').src=mockup.image;
    ruimteScale();
    document.getElementById('ruimteModal').style.display='flex';
    setTimeout(ruimteLayout,40);
  };
  document.addEventListener('input',function(e){ if(e.target && e.target.id==='ruimteScale') ruimteScale(); });
  window.addEventListener('resize',function(){ var md=document.getElementById('ruimteModal'); if(md && md.style.display==='flex') ruimteLayout(); });
})();

// Japandi-collectie: submenu tonen na klik op Japandi
function showJapandiSub(){
  var el=document.getElementById('japandiSub');
  if(el){ el.style.display='flex'; }
}

// Art Deco-collectie: submenu tonen na klik op Art Deco
function showArtdecoSub(){
  var el=document.getElementById('artdecoSub');
  if(el){ el.style.display='flex'; }
}

// Etalage: genereer een voorbeelddessin direct (zonder AI/sleutel)
async function genereerVoorbeeld(style, prompt, palet){
  try{
    var pin=document.getElementById('prompt'); if(pin) pin.value=prompt;
    if(typeof setLoading==='function') setLoading(true);
    if(typeof setStatus==='function') setStatus('Voorbeeld genereren...','');
    var tileCm=(document.getElementById('tileCm')||{}).value||40;
    var dpi=(document.getElementById('dpi')||{}).value||150;
    const resp=await fetch('/api/generate',{method:'POST',cache:'no-store',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({direct:true,style:style,prompt:prompt,palet:palet,tile_cm:tileCm,repeat_type:'full',dpi:dpi})});
    const data=await resp.json();
    if(!resp.ok||data.error){ if(typeof setStatus==='function') setStatus(data.error||'Mislukt.','error'); if(typeof setLoading==='function') setLoading(false); return; }
    currentTileSvg=data.tile_svg_b64; currentRepeatSvg=data.repeat_svg_b64; currentInfo=data.info;
    svgNaarPngPreview(data.tile_svg_b64,'previewTile',350);
    svgNaarPngPreview(data.repeat_svg_b64,'previewRepeat',700);
    var pt=document.getElementById('previewTile'), pr=document.getElementById('previewRepeat');
    if(pt) pt.style.display=(activeTab==='tile')?'block':'none';
    if(pr) pr.style.display=(activeTab==='repeat')?'block':'none';
    if(typeof setLoading==='function') setLoading(false);
    if(typeof setStatus==='function') setStatus('Klaar.','success');
    if(pr&&pr.scrollIntoView) pr.scrollIntoView({behavior:'smooth',block:'center'});
  }catch(e){ if(typeof setStatus==='function') setStatus('Fout: '+e.message,'error'); if(typeof setLoading==='function') setLoading(false); }
}


/* ===== DCOD Dessinator - inspiratie-koppeling (Fase B+C) ===== */
/* Centrale bron. 'generator' is intern; de gebruiker ziet alleen 'title'. */
var DCOD_CONCEPTS = {
  neo_deco:      { title:"Neo Deco",       description:"Eigentijdse geometrie voor representatieve interieurs.", generator:"art_deco_waaier", palette:"hospitality", prompt:"Art Deco waaier, luxe entree met warme messingaccenten, ritmische geometrie, rustige uitstraling", palet:{background:"#1a1a1a",primary:"#d8b24a",secondary:"#8a6a2e",accent1:"#efe6cf",accent2:"#c9a24a"} },
  aardlagen:     { title:"Aardlagen",      description:"Organische lagen en natuurlijke structuur in aardtinten.", generator:"aardlagen", palette:"aardlagen", prompt:"aardlagen, organische natuurlijke lagen, vloeiende structuur in aardtinten", palet:{background:"#e6d9b8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#3b4d2c",accent2:"#23311f"} },
  japandi:       { title:"Japandi",        description:"Rust en minimalisme met gedempte natuurlijke tinten.", generator:"japandi", palette:"japandi", prompt:"japandi, rustige minimalistische vloer met gedempte natuurlijke tinten, variant: river_stones", palet:{background:"#e6d9b8",primary:"#626451",secondary:"#6E7359",accent1:"#8D9971",accent2:"#B5C49F"} },
  urban_plaid:   { title:"Urban Plaid",    description:"Rustig architectonisch raster voor moderne werkplekken.", generator:"urban_plaid", palette:"urban", prompt:"urban plaid, architectonisch ruitpatroon met warme textiele uitstraling", palet:{background:"#e8d5c0",primary:"#c38d96",secondary:"#b5734e",accent1:"#b5734e",accent2:"#e8d5c0"} },
  cirkels:       { title:"Cirkels",        description:"Ritmische cirkels, elegant en dynamisch.", generator:"cirkels", palette:"hospitality", prompt:"alleen cirkels, ritmisch en elegant, strak en dynamisch", palet:{background:"#1a1a1a",primary:"#c9a24a",secondary:"#efe6cf",accent1:"#8a6a2e",accent2:"#ffffff"} },
  botanisch:     { title:"Botanisch",      description:"Expressief en bloemrijk in vol koloriet.", generator:"vrije_vormen", palette:"natuurlijk", prompt:"vrije vormen organisch, expressief en bloemrijk in vol koloriet", palet:{background:"#e6d9b8",primary:"#a03d5d",secondary:"#c9a24a",accent1:"#4e7a4e",accent2:"#6f8a4e"} },
  hoogtelijnen:  { title:"Hoogtelijnen",   description:"Vloeiende contourlijnen, rustig en verfijnd.", generator:"hoogtelijnen", palette:"natuurlijk", prompt:"hoogtelijnen, vloeiende topografische contourlijnen, rustig en verfijnd", palet:{background:"#e9e0c8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#42502e",accent2:"#8aa06a"} },
  weefstructuren:{ title:"Weefstructuren", description:"Geweven textiele structuur, warm en tactiel.", generator:"urban_plaid", palette:"natuurlijk", prompt:"urban plaid, geweven textiele structuur, warm en tactiel", palet:{background:"#e6ddc8",primary:"#b89a6a",secondary:"#8a6a4e",accent1:"#6f5a3e",accent2:"#d8c8a8"} },
  lijnenspel:    { title:"Lijnenspel",     description:"Ritmisch grafisch lijnenpatroon.", generator:"lijnenspel", palette:"zakelijk", prompt:"lijnenspel, ritmisch grafisch lijnenpatroon", palet:{background:"#EFE6CF",primary:"#003614",secondary:"#A7C58E",accent1:"#12301a",accent2:"#6f8a4e"} },
  neo_bauhaus:   { title:"Neo Bauhaus",    description:"Heldere geometrische composities met een moderne, architectonische uitstraling.", generator:"bauhaus", palette:"geometrisch", prompt:"Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs", palet:{background:"#1a1a1a",primary:"#d4622a",secondary:"#4a4a4a",accent1:"#c9a24a",accent2:"#efe6cf"} },
  vrije_vormen:  { title:"Vrije vormen",   description:"Speelse organische composities met een eigentijds karakter.", generator:"vrije_vormen", palette:"artistiek", prompt:"Vrije organische vormen, vloeiend en natuurlijk", palet:{background:"#F5F1E8",primary:"#6f8a4e",secondary:"#C9A24A",accent1:"#0E2117",accent2:"#A7C58E"} }
};
/* project-sleutel -> nette naam (voor de breadcrumb) */
var DCOD_PROJECTS = {
  werkplekken:"Werkplekken & Kantoren", hotels:"Hotels & Leisure",
  overheid:"Overheid & Publieke gebouwen", musea:"Musea & Bibliotheken"
};
window.addEventListener('DOMContentLoaded', function(){
  try {
    var params = new URLSearchParams(window.location.search);
    var key = params.get('concept');
    if (!key) return;                          /* geen concept => normale Dessinator */
    var c = DCOD_CONCEPTS[key];
    if (!c) return;
    var projKey = params.get('project') || '';
    var projNaam = DCOD_PROJECTS[projKey] || '';

    /* 1) verberg de etalage/voorbeeldkaarten */
    var empty = document.getElementById('emptyState');
    if (empty) empty.style.display = 'none';

    /* 2) breadcrumb-header invoegen boven de preview */
    var host = (document.getElementById('previewRepeat') || {}).parentNode;
    if (host && !document.getElementById('conceptHeader')) {
      var h = document.createElement('div');
      h.id = 'conceptHeader';
      h.style.cssText = 'margin:0 0 18px;padding:18px 22px;border:1px solid rgba(0,54,20,.14);border-radius:14px;background:linear-gradient(180deg,rgba(167,197,142,.10),rgba(167,197,142,.03));';
      var crumb = '';
      if (projNaam) crumb += '<span style="color:#5a6b57">'+projNaam+'</span> <span style="color:#A7C58E">&rarr;</span> ';
      crumb += '<span style="color:#5a6b57">'+c.title+'</span> <span style="color:#A7C58E">&rarr;</span> <span style="color:#5a6b57">Uw eerste voorstel</span>';
      h.innerHTML =
        '<div style="font-size:12px;letter-spacing:.06em;margin-bottom:10px;text-transform:uppercase">'+crumb+'</div>'+
        '<div style="font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#8a9a86">Startconcept</div>'+
        '<div style="font-family:Georgia,serif;font-size:26px;color:#003614;margin:2px 0 3px">'+c.title+'</div>'+
        (projNaam?'<div style="font-size:12px;color:#8a9a86">'+projNaam+'</div>':'')+
        (c.description?'<div style="font-size:13.5px;color:#5a6b57;margin-top:8px">'+c.description+'</div>':'');
      host.insertBefore(h, host.firstChild);
    }

    /* 3) direct genereren via de bestaande motor */
    function start(){
      if (typeof genereerVoorbeeld === 'function') { genereerVoorbeeld(key, c.prompt, c.palet); }
      else { setTimeout(start, 120); }
    }
    setTimeout(start, 160);
  } catch(e) { /* stil: nooit de Dessinator breken */ }
});
/* ===== einde inspiratie-koppeling ===== */

