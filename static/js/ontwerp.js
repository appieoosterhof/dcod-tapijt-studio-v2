/*
 * BUILD-021 -- Design Brain-frontend ("Ontwerp zelf met AI").
 *
 * Additieve, zelfstandige vanilla-JS controller op de bestaande
 * /api/design-brain-endpoints (BUILD-019/020). Geen framework, geen wijziging
 * aan de bestaande Dessinator (app.js) of aan /api/generate.
 *
 * Principes (BUILD-021 technisch):
 *   - unidirectioneel: actie -> API -> state bijwerken -> re-render;
 *   - de BACKEND is bron van waarheid (fase afgeleid uit de toestand);
 *   - gesprek_id in localStorage (herstel); api_key UITSLUITEND in-memory;
 *   - in-flight-vergrendeling + debounce; stale-veilige visualisatie.
 */
(function () {
  "use strict";

  var BASE = "/api/design-brain";
  var LS_KEY = "db_gesprek_id";

  // ── Client-state (spiegel; backend is leidend) ──────────────────────────────
  var state = {
    gesprek_id: null,
    api_key: "",        // in-memory only -- nooit in localStorage
    bezig: false,       // in-flight lock
    toestand: null,     // laatste volledige toestand van de backend
    chat: [],           // {rol:'gebruiker'|'dessinator', tekst}
    laatsteVervolgstap: null,
    scenes: null,       // lazy geladen scene-lijst (cache)
  };

  // ── DOM-helpers ─────────────────────────────────────────────────────────────
  function el(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function melding(t) { el("melding").textContent = t || ""; }
  function debounce(fn, ms) {
    var t; return function () { var a = arguments, c = this; clearTimeout(t); t = setTimeout(function () { fn.apply(c, a); }, ms); };
  }

  // ── API-laag: in-flight-lock + foutafhandeling ──────────────────────────────
  function api(method, path, body) {
    if (state.bezig) return Promise.reject({ _bezig: true });
    state.bezig = true; zetKnoppen(true);
    return fetch(BASE + path, {
      method: method,
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
      body: body ? JSON.stringify(body) : undefined,
    })
      .then(function (resp) {
        return resp.json().catch(function () { return {}; }).then(function (data) {
          return { status: resp.status, data: data };
        });
      })
      .then(function (r) {
        if (r.status === 404) { verlopenGesprek(); throw { _verlopen: true }; }
        return r;
      })
      .finally(function () { state.bezig = false; zetKnoppen(false); });
  }

  function zetKnoppen(bezig) {
    var knoppen = document.querySelectorAll("button");
    for (var i = 0; i < knoppen.length; i++) {
      if (knoppen[i].id === "nieuwGesprek") continue;
      knoppen[i].disabled = bezig;
    }
    el("verstuur").textContent = bezig ? "…" : "Stuur";
  }

  // ── Gesprek starten / herstellen ────────────────────────────────────────────
  function start() {
    var opgeslagen = localStorage.getItem(LS_KEY);
    if (opgeslagen) {
      state.gesprek_id = opgeslagen;
      api("GET", "/" + opgeslagen)
        .then(function (r) { if (r.data && r.data.success) { state.toestand = r.data.toestand; render(); } })
        .catch(function () {});
    } else {
      nieuwGesprek();
    }
  }

  function nieuwGesprek() {
    localStorage.removeItem(LS_KEY);
    state.toestand = null; state.chat = []; state.laatsteVervolgstap = null; state.scenes = null;
    el("eind").classList.remove("zichtbaar");
    api("POST", "/gesprek")
      .then(function (r) {
        state.gesprek_id = r.data.gesprek_id;
        localStorage.setItem(LS_KEY, state.gesprek_id);
        state.chat.push({ rol: "dessinator", tekst: "Vertel me over de ruimte die u wilt aankleden — in uw eigen woorden." });
        render();
      })
      .catch(function () { melding("Kon geen gesprek starten. Probeer het opnieuw."); });
  }

  function verlopenGesprek() {
    localStorage.removeItem(LS_KEY);
    melding("Dit gesprek is niet meer beschikbaar — we beginnen opnieuw.");
    setTimeout(nieuwGesprek, 400);
  }

  // ── Dialoog ─────────────────────────────────────────────────────────────────
  function verstuur() {
    var tekst = el("invoer").value.trim();
    if (!tekst) return;
    state.api_key = el("apiKey").value.trim();  // in-memory
    state.chat.push({ rol: "gebruiker", tekst: tekst });
    el("invoer").value = ""; melding(""); render();
    api("POST", "/" + state.gesprek_id + "/dialoog", { invoer: tekst, api_key: state.api_key })
      .then(function (r) {
        var d = r.data;
        if (!d.success) { toonSignaleringen(d.signaleringen, "Ik heb nog iets meer nodig om verder te kunnen."); return; }
        state.laatsteVervolgstap = d.vervolgstap || null;
        if (d.vervolgstap && d.vervolgstap.inhoud) state.chat.push({ rol: "dessinator", tekst: d.vervolgstap.inhoud });
        // toestand ophalen (bron van waarheid) zodat laag 1/2 zichtbaar wordt
        return ververs();
      })
      .catch(function (e) { if (!e || !e._verlopen && !e._bezig) netwerkfout(); });
  }

  // ── Acties (bevestigen / kiezen / ophalen) ──────────────────────────────────
  function post(path, body) {
    return api("POST", "/" + state.gesprek_id + path, body)
      .then(function (r) {
        if (r.data && r.data.success === false && r.data.signaleringen) {
          toonSignaleringen(r.data.signaleringen, "Er ontbreekt nog iets voor deze stap.");
          return null;
        }
        return ververs();
      })
      .catch(function (e) { if (!e || (!e._verlopen && !e._bezig)) netwerkfout(); return null; });
  }

  function ververs() {
    return api("GET", "/" + state.gesprek_id).then(function (r) {
      if (r.data && r.data.success) { state.toestand = r.data.toestand; advance(); render(); }
    });
  }

  // Auto-advance: haal server-afgeleide tussenstappen automatisch op (minder
  // klikken); de gebruiker bevestigt/kiest uitsluitend de mijlpalen.
  function advance() {
    if (state.bezig) return;
    var f = fase();
    if (f === "strategie_voorstellen") { post("/ontwerpstrategie"); }
    else if (f === "concept_vormen") { post("/concept"); }
    else if (f === "floor_designs_ophalen") { post("/floor-designs"); }
    else if (f === "material_ophalen") { post("/material-profiles"); }
    else if (f === "pattern_ophalen") { post("/pattern-profiles"); }
    else if (f === "svg_renderen") { post("/svg"); }
  }

  // ── Fase-afleiding uit de backend-toestand ──────────────────────────────────
  function fase() {
    var t = state.toestand; if (!t) return "dialoog";  // vers gesprek = dialoogfase
    var dc = t.design_context || {};
    var ov = dc.ontwerpvisie || {}, st = dc.ontwerpstrategie || {}, co = dc.concept || {};
    if (!ov.bevestigd_door_architect) return "dialoog";
    if (st.status !== "vastgesteld") return st.aanpak ? "strategie_bevestigen" : "strategie_voorstellen";
    if (co.status !== "bevestigd") return co.stijlfamilie ? "concept_bevestigen" : "concept_vormen";
    if (!t.floor_design) return (t.floor_designs && t.floor_designs.length) ? "floor_design_kiezen" : "floor_designs_ophalen";
    if (!t.material_profile) return (t.material_profiles && t.material_profiles.length) ? "material_kiezen" : "material_ophalen";
    if (!t.pattern_profile) return (t.pattern_profiles && t.pattern_profiles.length) ? "pattern_kiezen" : "pattern_ophalen";
    if (!t.svg_resultaat) return "svg_renderen";
    if (!t.visualisatie) return "ruimte_kiezen";
    if (!t.pakket) return "afronden";
    return "eind";
  }

  var MIJLPALEN = [
    ["visie", "Visie"], ["strategie", "Richting"], ["concept", "Concept"],
    ["floor", "Ontwerp"], ["materiaal", "Materiaal"], ["patroon", "Patroon"], ["eind", "Klaar"],
  ];
  function mijlpaalStatus() {
    var t = state.toestand || {}, dc = t.design_context || {};
    var ov = dc.ontwerpvisie || {}, st = dc.ontwerpstrategie || {}, co = dc.concept || {};
    return {
      visie: !!ov.bevestigd_door_architect,
      strategie: st.status === "vastgesteld",
      concept: co.status === "bevestigd",
      floor: !!t.floor_design,
      materiaal: !!t.material_profile,
      patroon: !!t.pattern_profile,
      eind: !!t.pakket,
    };
  }

  // ── Rendering ───────────────────────────────────────────────────────────────
  function render() { renderVoortgang(); renderGesprek(); renderActie(); renderViz(); renderSamenvatting(); renderEind(); }

  function renderVoortgang() {
    var s = mijlpaalStatus(), f = fase(), h = "";
    var actieveKey = ({ dialoog: "visie", strategie_voorstellen: "strategie", strategie_bevestigen: "strategie",
      concept_vormen: "concept", concept_bevestigen: "concept", floor_designs_ophalen: "floor", floor_design_kiezen: "floor",
      material_ophalen: "materiaal", material_kiezen: "materiaal", pattern_ophalen: "patroon", pattern_kiezen: "patroon",
      svg_renderen: "patroon", ruimte_kiezen: "patroon", afronden: "eind", eind: "eind" })[f];
    for (var i = 0; i < MIJLPALEN.length; i++) {
      var k = MIJLPALEN[i][0], klasse = "mijlpaal";
      if (s[k]) klasse += " klaar"; else if (k === actieveKey) klasse += " actief";
      h += '<div class="' + klasse + '"><span class="bol"></span>' + esc(MIJLPALEN[i][1]) + "</div>";
    }
    el("voortgang").innerHTML = h;
  }

  function renderGesprek() {
    var h = "";
    for (var i = 0; i < state.chat.length; i++) {
      h += '<div class="bericht ' + state.chat[i].rol + '">' + esc(state.chat[i].tekst) + "</div>";
    }
    if (state.bezig) h += '<div class="bezig">De Dessinator denkt met u mee…</div>';
    var g = el("gesprek"); g.innerHTML = h; g.scrollTop = g.scrollHeight;
    var inDialoog = fase() === "dialoog";
    el("invoerrij").style.display = inDialoog ? "flex" : "none";
  }

  function renderActie() {
    var f = fase(), h = "";
    if (f === "dialoog" && state.laatsteVervolgstap && state.laatsteVervolgstap.type === "samenvatting_ter_bevestiging") {
      h = kaart("Klopt dit beeld?", "Bevestig de visie, of stuur bij in het gesprek.",
        [knop("Bevestig de visie", "bevestig-visie")]);
    } else if (f === "strategie_bevestigen") {
      var st = state.toestand.design_context.ontwerpstrategie;
      h = kaart("Onze ontwerprichting", esc(st.aanpak || ""), [knop("Ja, deze richting", "bevestig-strategie")]);
    } else if (f === "concept_bevestigen") {
      var co = state.toestand.design_context.concept;
      h = kaart("Het karakter", "Stijl: " + esc(co.stijlfamilie || "") + " — complexiteit: " + esc(co.complexiteit || ""),
        [knop("Dit klopt", "bevestig-concept")]);
    } else if (f === "floor_design_kiezen") {
      h = keuzeKaart("Kies een ontwerprichting", state.toestand.floor_designs, "ontwerprichting", "bevestig-floor-design");
    } else if (f === "material_kiezen") {
      h = keuzeKaart("Kies het materiaal", state.toestand.material_profiles, "uitstraling", "bevestig-material-profile");
    } else if (f === "pattern_kiezen") {
      h = keuzeKaart("Kies het patroon", state.toestand.pattern_profiles, "motiefstructuur", "bevestig-pattern-profile");
    } else if (f === "ruimte_kiezen") {
      h = '<div class="kaart"><h3>Kies uw ruimte</h3><p>Waar wilt u het resultaat zien?</p><div id="scenelijst" class="keuzes"><div class="bezig">Ruimtes laden…</div></div><p style="margin-top:8px">Geen passende ruimte? <a href="/scene-builder" target="_blank">Voeg er een toe</a>.</p></div>';
    } else if (f === "afronden") {
      h = kaart("Tevreden met dit ontwerp?", "Dan bundelen we alles voor DCOD.", [knop("Dit is 'm — draag over aan DCOD", "transfer-package")]);
    }
    el("actie").innerHTML = h;
    if (f === "ruimte_kiezen") laadScenes();
  }

  function kaart(titel, tekst, knoppenHtml) {
    return '<div class="kaart"><h3>' + esc(titel) + '</h3><p>' + tekst + '</p><div class="acties">' + knoppenHtml.join("") + "</div></div>";
  }
  function knop(label, actiePad) { return '<button data-actie="' + esc(actiePad) + '">' + esc(label) + "</button>"; }
  function keuzeKaart(titel, lijst, veld, actiePad) {
    var h = '<div class="kaart"><h3>' + esc(titel) + '</h3><div class="keuzes">';
    for (var i = 0; i < (lijst || []).length; i++) {
      var label = lijst[i][veld] || lijst[i].motivering || ("Optie " + (i + 1));
      h += '<button class="keuze" data-actie="' + esc(actiePad) + '" data-index="' + i + '">' + esc(label) + "</button>";
    }
    return h + "</div></div>";
  }

  function renderViz() {
    var t = state.toestand, viz = el("viz");
    if (!t) { viz.innerHTML = '<div class="leeg">Zodra we een richting kiezen, verschijnt hier het beeld.</div>'; return; }
    // Mockup (in de ruimte) heeft voorrang; daarna dessin-staal; daarna sfeerbeeld.
    if (t.visualisatie && t.visualisatie.beeld) { viz.innerHTML = mockupHtml(t.visualisatie.beeld); return; }
    if (t.svg_resultaat && t.svg_resultaat.svg) {
      var uri = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(t.svg_resultaat.svg)));
      viz.innerHTML = '<img alt="Uw dessin" src="' + uri + '"/>'; return;
    }
    var co = t.design_context && t.design_context.concept;
    if (co && co.kleurpalet) {
      var h = '<div class="stalen">';
      var pal = co.kleurpalet;
      for (var k in pal) { if (typeof pal[k] === "string" && pal[k][0] === "#") h += '<span class="staal" style="background:' + esc(pal[k]) + '"></span>'; }
      viz.innerHTML = h + "</div>"; return;
    }
    viz.innerHTML = '<div class="leeg">Zodra we een richting kiezen, verschijnt hier het beeld.</div>';
  }

  // Eerste-niveau, ZELFSTANDIGE mockup uit de FVE-beeld-payload (geen matrix3d,
  // geen kopie van app.js): achtergrond + dessin-overlay geknipt op het
  // vloerpolygon via CSS clip-path (BUILD-021 technisch).
  function mockupHtml(beeld) {
    var achtergrond = beeld.achtergrond_url || "";
    var poly = beeld.vloerpolygon || [];
    var svg = beeld.svg || "";
    var uri = svg ? ("data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)))) : "";
    var clip = "";
    if (poly.length >= 3) {
      clip = "clip-path:polygon(" + poly.map(function (p) { return (p[0] * 100) + "% " + (p[1] * 100) + "%"; }).join(",") + ");";
    }
    var overlay = uri
      ? '<div class="dessin-overlay" style="background-image:url(' + esc(uri) + ');' + clip + '"></div>'
      : "";
    if (!achtergrond) return '<div class="leeg">Beeld in de ruimte wordt getoond zodra de ruimte is gekozen.</div>';
    return '<div class="mockup"><img class="achtergrond" alt="Ruimte" src="' + esc(achtergrond) + '"/>' + overlay + "</div>";
  }

  function renderSamenvatting() {
    var t = state.toestand; if (!t) return;
    var dc = t.design_context || {}, ov = dc.ontwerpvisie || {}, st = dc.ontwerpstrategie || {}, co = dc.concept || {};
    var rijen = [];
    if (ov.vrije_tekst) rijen.push(["Wens", ov.vrije_tekst]);
    if (ov.sfeer) rijen.push(["Sfeer", ov.sfeer]);
    if (st.aanpak) rijen.push(["Richting", st.aanpak]);
    if (co.stijlfamilie) rijen.push(["Stijl", co.stijlfamilie]);
    if (t.floor_design) rijen.push(["Ontwerp", t.floor_design.ontwerprichting]);
    if (t.material_profile) rijen.push(["Materiaal", t.material_profile.uitstraling || t.material_profile.materiaalsoort]);
    if (t.pattern_profile) rijen.push(["Patroon", t.pattern_profile.motiefstructuur]);
    if (!rijen.length) { el("samenvatting").innerHTML = '<div class="leeg">Uw keuzes verschijnen hier terwijl we samen ontwerpen.</div>'; return; }
    var h = "<dl>";
    for (var i = 0; i < rijen.length; i++) h += "<dt>" + esc(rijen[i][0]) + "</dt><dd>" + esc(rijen[i][1]) + "</dd>";
    el("samenvatting").innerHTML = h + "</dl>";
  }

  function renderEind() {
    var t = state.toestand, eind = el("eind");
    if (!t || !t.pakket) { eind.classList.remove("zichtbaar"); return; }
    eind.classList.add("zichtbaar");
    el("eindinhoud").innerHTML =
      "<p style='font-size:14px;margin-bottom:10px'>Uw ontwerp is volledig gebundeld voor DCOD: uw visie, de ontwerprichting, het materiaal en het beeld in de ruimte.</p>" +
      "<p style='color:var(--muted);font-size:13px'>DCOD ontvangt uw ontwerp en neemt contact op voor de uitvoering. Er wordt nog niets besteld of afgerekend.</p>";
  }

  // ── Scene Builder-koppeling (lazy) ──────────────────────────────────────────
  function laadScenes() {
    if (state.scenes) { toonScenes(); return; }
    fetch("/api/scenes", { cache: "no-store" }).then(function (r) { return r.json(); })
      .then(function (d) { state.scenes = (d && d.scenes) || []; toonScenes(); })
      .catch(function () { var l = el("scenelijst"); if (l) l.innerHTML = '<div class="leeg">Ruimtes konden niet worden geladen.</div>'; });
  }
  function toonScenes() {
    var l = el("scenelijst"); if (!l) return;
    if (!state.scenes.length) { l.innerHTML = '<div class="leeg">Nog geen ruimtes. Voeg er een toe via de Scene Builder.</div>'; return; }
    var h = "";
    for (var i = 0; i < state.scenes.length; i++) {
      var s = state.scenes[i];
      h += '<button class="keuze" data-scene="' + esc(s.id) + '">' + esc(s.naam || s.id) + "</button>";
    }
    l.innerHTML = h;
  }

  // ── Event-delegatie ─────────────────────────────────────────────────────────
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("button") : null;
    if (!b || b.disabled) return;
    if (b.id === "nieuwGesprek") { nieuwGesprek(); return; }
    if (b.id === "verstuur") { verstuur(); return; }
    if (b.getAttribute("data-scene")) { post("/visualisatie", { scene_id: b.getAttribute("data-scene") }); return; }
    var actie = b.getAttribute("data-actie");
    if (actie) {
      var idx = b.getAttribute("data-index");
      post("/" + actie, idx != null ? { index: parseInt(idx, 10) } : undefined);
    }
  });

  var verstuurDebounced = debounce(verstuur, 250);
  el("invoer").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); verstuurDebounced(); }
  });

  // Vertaal backend-signaleringen naar mensvriendelijke copy (BUILD-021 §6);
  // nooit een ruwe foutcode tonen.
  function vriendelijk(sig, fallback) {
    var tekst = (sig && sig.length) ? sig.join(" ") : "";
    if (/api_key/i.test(tekst)) return "Vul eerst uw API-sleutel in (rechtsboven) om samen verder te ontwerpen.";
    if (/onvoldoende|ontbreekt|niet bevestigd|leeg/i.test(tekst)) return fallback || "Ik heb nog iets meer over uw wensen nodig om verder te kunnen.";
    return fallback || "Er ging iets mis. Probeer het zo opnieuw.";
  }
  function toonSignaleringen(sig, fallback) { melding(vriendelijk(sig, fallback)); }
  function netwerkfout() { melding("Er ging iets mis met de verbinding. Probeer het zo opnieuw."); }

  // ── Init ────────────────────────────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", start);
})();
