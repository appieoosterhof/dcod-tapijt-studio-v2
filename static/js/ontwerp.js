/*
 * BUILD-021 + BUILD-022 -- Design Brain-frontend (DCOD-ontwerpstudio).
 *
 * Additieve, zelfstandige vanilla-JS controller op de bestaande
 * /api/design-brain-endpoints. BUILD-022 voegt de belevingslaag toe (hero,
 * atelier-presentatie, selectieve onthulling, microcopy). De state-flow, de
 * fase()-machine, alle endpoint-aanroepen en gesprek_id/localStorage blijven
 * ONGEWIJZIGD in gedrag.
 *
 * AB-012: de AI-infrastructuur is volledig verborgen -- de frontend kent GEEN
 * API-sleutel, provider, model of configuratie; de sleutel is uitsluitend
 * serverconfiguratie. Bij onbeschikbaarheid uitsluitend een mensvriendelijke
 * studio-melding, nooit technische details.
 */
(function () {
  "use strict";

  var BASE = "/api/design-brain";
  var LS_KEY = "db_gesprek_id";
  // AB-012: de AI-infrastructuur is volledig verborgen. Geen enkele
  // API-sleutel/config in de frontend; bij onbeschikbaarheid uitsluitend deze
  // mensvriendelijke melding.
  var STUDIO_ONBESCHIKBAAR = "Onze ontwerpstudio is momenteel niet beschikbaar. Probeert u het later nogmaals of neem contact op met DCOD.";

  // ── Client-state (spiegel; backend is leidend) ──────────────────────────────
  var state = {
    gesprek_id: null,
    bezig: false,       // in-flight lock
    toestand: null,
    chat: [],
    laatsteVervolgstap: null,
    scenes: null,
  };
  var _html = {};       // per-sectie cache: alleen gewijzigde secties animeren

  // ── Helpers ─────────────────────────────────────────────────────────────────
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
  function reduceer() { return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }

  // Zet HTML uitsluitend als het veranderde; animeer alleen dan (geen flikkering
  // op ongewijzigde secties). Retourneert of er een wijziging was.
  function zetInhoud(id, html) {
    if (_html[id] === html) return false;
    _html[id] = html;
    var e = el(id); if (!e) return false;
    e.innerHTML = html;
    if (!reduceer()) { e.classList.remove("onthul"); void e.offsetWidth; e.classList.add("onthul"); }
    return true;
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
    var v = el("verstuur"); if (v) v.textContent = bezig ? "…" : "→";
  }

  // ── Gesprek starten / herstellen ────────────────────────────────────────────
  function start() {
    var opgeslagen = localStorage.getItem(LS_KEY);
    if (opgeslagen) {
      state.gesprek_id = opgeslagen;
      api("GET", "/" + opgeslagen)
        .then(function (r) {
          if (r.data && r.data.success) {
            state.toestand = r.data.toestand;
            document.body.classList.add("gestart");  // lopend gesprek: sla de hero over
            render();
          }
        })
        .catch(function () {});
    } else {
      nieuwGesprek();
    }
  }

  function nieuwGesprek() {
    document.body.classList.remove("gestart");
    document.body.removeAttribute("data-sfeer");
    var hi = el("heroInvoer"); if (hi) hi.value = "";
    localStorage.removeItem(LS_KEY);
    state.toestand = null; state.chat = []; state.laatsteVervolgstap = null; state.scenes = null;
    _html = {};
    el("eind").classList.remove("zichtbaar");
    api("POST", "/gesprek")
      .then(function (r) {
        state.gesprek_id = r.data.gesprek_id;
        localStorage.setItem(LS_KEY, state.gesprek_id);
        state.chat.push({ rol: "dessinator", tekst: "Fijn dat u er bent. Vertel me gerust in uw eigen woorden waar deze ruimte van droomt — ik denk met u mee." });
        render();
      })
      .catch(function () { melding("Ik kon het atelier even niet openen — probeer het zo opnieuw."); });
  }

  function verlopenGesprek() {
    localStorage.removeItem(LS_KEY);
    melding("Dit gesprek is niet meer beschikbaar — we beginnen zo opnieuw.");
    setTimeout(nieuwGesprek, 500);
  }

  // ── Hero -> werkbank (presentatie; geen paginawissel) ───────────────────────
  function beginMetHero() {
    var t = el("heroInvoer").value.trim();
    if (!t) { el("heroInvoer").focus(); return; }
    el("invoer").value = t;
    document.body.classList.add("gestart");
    verstuur();
  }

  // ── Decoratief sfeer-attribuut (HARDE GRENS, BUILD-022 §10) ──────────────────
  // Zet uitsluitend een CSS-attribuut voor de sfeer-gradient. Interpreteert
  // niets, voedt de keten niet, roept geen endpoint aan, bewaart niets. Het is
  // ambiance; de echte interpretatie blijft exclusief bij de Context Interpreter.
  function pasSfeerToe(tekst) {
    var s = (tekst || "").toLowerCase(), m = "";
    if (/warm|gezellig|hout|aards|goud|amber/.test(s)) m = "warm";
    else if (/rustig|kalm|ingetogen|sereen|zen/.test(s)) m = "rustig";
    else if (/grafisch|strak|modern|geometr|bold|statement|contrast/.test(s)) m = "grafisch";
    else if (/organisch|vloeiend|natuurlijk|zacht|golvend/.test(s)) m = "organisch";
    if (m) document.body.setAttribute("data-sfeer", m);
  }

  // ── Dialoog ─────────────────────────────────────────────────────────────────
  function verstuur() {
    var tekst = el("invoer").value.trim();
    if (!tekst) return;
    pasSfeerToe(tekst);                          // uitsluitend decoratief
    state.chat.push({ rol: "gebruiker", tekst: tekst });
    el("invoer").value = ""; melding(""); render();
    api("POST", "/" + state.gesprek_id + "/dialoog", { invoer: tekst })
      .then(function (r) {
        var d = r.data;
        if (!d.success) {
          if (d.onbeschikbaar) melding(STUDIO_ONBESCHIKBAAR);
          else toonSignaleringen(d.signaleringen, "Vertel me gerust nog iets meer over de sfeer die u zoekt.");
          return;
        }
        state.laatsteVervolgstap = d.vervolgstap || null;
        if (d.vervolgstap && d.vervolgstap.inhoud) state.chat.push({ rol: "dessinator", tekst: d.vervolgstap.inhoud });
        return ververs();
      })
      .catch(function (e) { if (!e || (!e._verlopen && !e._bezig)) netwerkfout(); });
  }

  // ── Acties (bevestigen / kiezen / ophalen) ──────────────────────────────────
  function post(path, body) {
    return api("POST", "/" + state.gesprek_id + path, body)
      .then(function (r) {
        if (r.data && r.data.success === false) {
          if (r.data.onbeschikbaar) { melding(STUDIO_ONBESCHIKBAAR); return null; }
          if (r.data.signaleringen) { toonSignaleringen(r.data.signaleringen, "Er ontbreekt nog net iets voor deze stap."); return null; }
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

  // ── Fase-afleiding uit de backend-toestand (ongewijzigd) ────────────────────
  function fase() {
    var t = state.toestand; if (!t) return "dialoog";
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
      visie: !!ov.bevestigd_door_architect, strategie: st.status === "vastgesteld",
      concept: co.status === "bevestigd", floor: !!t.floor_design,
      materiaal: !!t.material_profile, patroon: !!t.pattern_profile, eind: !!t.pakket,
    };
  }
  function actieveMijlpaal(f) {
    return ({ dialoog: "visie", strategie_voorstellen: "strategie", strategie_bevestigen: "strategie",
      concept_vormen: "concept", concept_bevestigen: "concept", floor_designs_ophalen: "floor", floor_design_kiezen: "floor",
      material_ophalen: "materiaal", material_kiezen: "materiaal", pattern_ophalen: "patroon", pattern_kiezen: "patroon",
      svg_renderen: "patroon", ruimte_kiezen: "patroon", afronden: "eind", eind: "eind" })[f];
  }
  function hoofdstukVan(f) {
    return ({ dialoog: "We verkennen samen uw wensen",
      strategie_voorstellen: "We bepalen de richting", strategie_bevestigen: "We bepalen de richting",
      concept_vormen: "We geven het karakter vorm", concept_bevestigen: "We geven het karakter vorm",
      floor_designs_ophalen: "We kiezen het ontwerp", floor_design_kiezen: "We kiezen het ontwerp",
      material_ophalen: "We kiezen het materiaal", material_kiezen: "We kiezen het materiaal",
      pattern_ophalen: "We tekenen het dessin", pattern_kiezen: "We tekenen het dessin", svg_renderen: "We tekenen het dessin",
      ruimte_kiezen: "We leggen het in uw ruimte", afronden: "Uw verhaal is bijna compleet", eind: "Klaar voor DCOD" })[f] || "";
  }

  // ── Rendering ───────────────────────────────────────────────────────────────
  function render() { renderVoortgang(); renderGesprek(); renderActie(); renderViz(); renderSamenvatting(); renderEind(); }

  // Atelier-fluistering i.p.v. teller (mijlpalen blijven; geen "stap x van y").
  function renderVoortgang() {
    var s = mijlpaalStatus(), f = fase(), actief = actieveMijlpaal(f), dots = "";
    for (var i = 0; i < MIJLPALEN.length; i++) {
      var k = MIJLPALEN[i][0], c = "dot";
      if (s[k]) c += " klaar"; else if (k === actief) c += " nu";
      dots += '<span class="' + c + '"></span>';
    }
    zetInhoud("voortgang", '<span class="dot-reeks">' + dots + '</span><span class="hoofdstuk-tekst">' + esc(hoofdstukVan(f)) + "</span>");
  }

  function renderGesprek() {
    var h = "";
    for (var i = 0; i < state.chat.length; i++) {
      var laatste = (i === state.chat.length - 1 && !state.bezig);
      h += '<div class="bericht ' + state.chat[i].rol + (laatste ? " nieuw" : "") + '">' + esc(state.chat[i].tekst) + "</div>";
    }
    if (state.bezig) h += '<div class="bezig">De Dessinator denkt met u mee…</div>';
    if (_html["gesprek"] !== h) { _html["gesprek"] = h; el("gesprek").innerHTML = h; }
    var g = el("gesprek"); g.scrollTop = g.scrollHeight;
    el("invoerrij").style.display = (fase() === "dialoog") ? "flex" : "none";
  }

  function renderActie() {
    var f = fase(), h = "";
    if (f === "dialoog" && state.laatsteVervolgstap && state.laatsteVervolgstap.type === "samenvatting_ter_bevestiging") {
      h = kaart("Klopt dit beeld?", "Bevestig deze richting, of stuur bij in het gesprek.", [knik("Ja, dit is de sfeer", "bevestig-visie")]);
    } else if (f === "strategie_bevestigen") {
      h = kaart("Onze ontwerprichting", esc(state.toestand.design_context.ontwerpstrategie.aanpak || ""), [knik("Ja, deze kant op", "bevestig-strategie")]);
    } else if (f === "concept_bevestigen") {
      var co = state.toestand.design_context.concept;
      h = kaart("Het karakter", "Een " + esc(co.stijlfamilie || "eigen") + " karakter, " + esc(co.complexiteit || "in balans") + ".", [knik("Dit klopt", "bevestig-concept")]);
    } else if (f === "floor_design_kiezen") {
      h = keuzeKaart("Welke richting spreekt u aan?", state.toestand.floor_designs, "ontwerprichting", "bevestig-floor-design");
    } else if (f === "material_kiezen") {
      h = keuzeKaart("Welk materiaal past hierbij?", state.toestand.material_profiles, "uitstraling", "bevestig-material-profile");
    } else if (f === "pattern_kiezen") {
      h = keuzeKaart("Welk patroon wordt het?", state.toestand.pattern_profiles, "motiefstructuur", "bevestig-pattern-profile");
    } else if (f === "ruimte_kiezen") {
      h = '<div class="kaart"><h3>Waar wilt u het zien?</h3><p>Kies de ruimte waarin we uw vloer leggen.</p><div id="scenelijst" class="keuzes"><div class="bezig">Even uw ruimtes ophalen…</div></div><p style="margin-top:10px;font-size:12.5px">Geen passende ruimte? <a href="/scene-builder" target="_blank">Voeg er hier een toe</a>.</p></div>';
    } else if (f === "afronden") {
      h = kaart("Tevreden met dit ontwerp?", "Dan brengen we alles samen voor DCOD.", [knik("Dit is 'm — geef door aan DCOD", "transfer-package")]);
    }
    zetInhoud("actie", h);
    if (f === "ruimte_kiezen") laadScenes();
  }

  function kaart(titel, tekst, knoppenHtml) {
    return '<div class="kaart"><h3>' + esc(titel) + '</h3><p>' + tekst + '</p><div class="acties">' + knoppenHtml.join("") + "</div></div>";
  }
  function knik(label, actiePad) { return '<button class="knik" data-actie="' + esc(actiePad) + '">' + esc(label) + "</button>"; }
  function keuzeKaart(titel, lijst, veld, actiePad) {
    var h = '<div class="kaart"><h3>' + esc(titel) + '</h3><div class="keuzes">';
    for (var i = 0; i < (lijst || []).length; i++) {
      var label = lijst[i][veld] || lijst[i].motivering || ("Optie " + (i + 1));
      h += '<button class="keuze" data-actie="' + esc(actiePad) + '" data-index="' + i + '">' + esc(label) + "</button>";
    }
    return h + "</div></div>";
  }

  function renderViz() {
    var t = state.toestand, h, isMockup = false;
    if (!t) { h = '<div class="leeg">Zodra we samen een richting kiezen, verschijnt hier uw vloer.</div>'; }
    else if (t.visualisatie && t.visualisatie.beeld) { h = mockupHtml(t.visualisatie.beeld); isMockup = true; }
    else if (t.svg_resultaat && t.svg_resultaat.svg) {
      h = '<img alt="Uw dessin" src="data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(t.svg_resultaat.svg))) + '"/>';
    } else {
      var co = t.design_context && t.design_context.concept;
      if (co && co.kleurpalet) {
        h = '<div class="stalen">';
        for (var k in co.kleurpalet) { var v = co.kleurpalet[k]; if (typeof v === "string" && v[0] === "#") h += '<span class="staal" style="background:' + esc(v) + '"></span>'; }
        h += "</div>";
      } else { h = '<div class="leeg">Zodra we samen een richting kiezen, verschijnt hier uw vloer.</div>'; }
    }
    zetInhoud("viz", h);
    if (isMockup) { var mk = el("viz").querySelector(".mockup"); if (mk) requestAnimationFrame(function () { mk.classList.add("gelegd"); }); }
  }

  // Zelfstandige mockup uit de FVE-beeld-payload (geen matrix3d, geen kopie van
  // app.js): achtergrond + dessin-overlay op het vloerpolygon via CSS clip-path.
  function mockupHtml(beeld) {
    var achtergrond = beeld.achtergrond_url || "", poly = beeld.vloerpolygon || [], svg = beeld.svg || "";
    var uri = svg ? ("data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)))) : "";
    var clip = poly.length >= 3 ? "clip-path:polygon(" + poly.map(function (p) { return (p[0] * 100) + "% " + (p[1] * 100) + "%"; }).join(",") + ");" : "";
    var overlay = uri ? '<div class="dessin-overlay" style="background-image:url(' + esc(uri) + ');' + clip + '"></div>' : "";
    if (!achtergrond) return '<div class="leeg">Uw vloer verschijnt hier zodra u de ruimte kiest.</div>';
    return '<div class="mockup"><img class="achtergrond" alt="Uw ruimte" src="' + esc(achtergrond) + '"/>' + overlay + "</div>";
  }

  function renderSamenvatting() {
    var t = state.toestand; if (!t) { zetInhoud("samenvatting", ""); return; }
    var dc = t.design_context || {}, ov = dc.ontwerpvisie || {}, st = dc.ontwerpstrategie || {}, co = dc.concept || {};
    var rijen = [];
    if (ov.vrije_tekst) rijen.push(["Wens", ov.vrije_tekst]);
    if (ov.sfeer) rijen.push(["Sfeer", ov.sfeer]);
    if (st.aanpak) rijen.push(["Richting", st.aanpak]);
    if (co.stijlfamilie) rijen.push(["Stijl", co.stijlfamilie]);
    if (t.floor_design) rijen.push(["Ontwerp", t.floor_design.ontwerprichting]);
    if (t.material_profile) rijen.push(["Materiaal", t.material_profile.uitstraling || t.material_profile.materiaalsoort]);
    if (t.pattern_profile) rijen.push(["Patroon", t.pattern_profile.motiefstructuur]);
    if (!rijen.length) { zetInhoud("samenvatting", ""); return; }
    var h = "<dl>";
    for (var i = 0; i < rijen.length; i++) h += "<dt>" + esc(rijen[i][0]) + "</dt><dd>" + esc(rijen[i][1]) + "</dd>";
    zetInhoud("samenvatting", h + "</dl>");
  }

  function renderEind() {
    var t = state.toestand, eind = el("eind");
    if (!t || !t.pakket) { eind.classList.remove("zichtbaar"); return; }
    eind.classList.add("zichtbaar");
    zetInhoud("eindinhoud",
      '<div class="titel">Het verhaal van deze ruimte, verteld in uw vloer.</div>' +
      '<p style="font-size:14px;color:var(--text);margin-bottom:10px">Uw ontwerp is compleet — uw wens, de richting, het materiaal en het dessin in uw eigen ruimte, samengebracht tot één geheel.</p>' +
      '<p style="font-size:13px;color:var(--muted)">DCOD ontvangt uw ontwerp en neemt contact op voor de uitvoering. Er wordt nog niets besteld of afgerekend.</p>');
  }

  // ── Scene Builder-koppeling (lazy) ──────────────────────────────────────────
  function laadScenes() {
    if (state.scenes) { toonScenes(); return; }
    fetch("/api/scenes", { cache: "no-store" }).then(function (r) { return r.json(); })
      .then(function (d) { state.scenes = (d && d.scenes) || []; toonScenes(); })
      .catch(function () { var l = el("scenelijst"); if (l) l.innerHTML = '<div class="leeg">Uw ruimtes konden even niet worden geladen.</div>'; });
  }
  function toonScenes() {
    var l = el("scenelijst"); if (!l) return;
    if (!state.scenes.length) { l.innerHTML = '<div class="leeg">Nog geen ruimtes — voeg er een toe via de Scene Builder.</div>'; return; }
    var h = "";
    for (var i = 0; i < state.scenes.length; i++) { var s = state.scenes[i]; h += '<button class="keuze" data-scene="' + esc(s.id) + '">' + esc(s.naam || s.id) + "</button>"; }
    l.innerHTML = h;
  }

  // ── Event-delegatie ─────────────────────────────────────────────────────────
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("button") : null;
    if (!b || b.disabled) return;
    if (b.id === "nieuwGesprek") { nieuwGesprek(); return; }
    if (b.id === "heroVerstuur") { beginMetHero(); return; }
    if (b.id === "verstuur") { verstuur(); return; }
    if (b.getAttribute("data-scene")) { post("/visualisatie", { scene_id: b.getAttribute("data-scene") }); return; }
    var actie = b.getAttribute("data-actie");
    if (actie) { var idx = b.getAttribute("data-index"); post("/" + actie, idx != null ? { index: parseInt(idx, 10) } : undefined); }
  });

  var verstuurDebounced = debounce(verstuur, 250);
  el("invoer").addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); verstuurDebounced(); } });
  el("heroInvoer").addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); beginMetHero(); } });

  // ── Foutbegeleiding (mensvriendelijk; nooit AI-infra/technische details) ────
  // AB-012: geen enkele verwijzing naar sleutels, modellen of providers.
  function vriendelijk(sig, fallback) {
    var tekst = (sig && sig.length) ? sig.join(" ") : "";
    if (/onvoldoende|ontbreekt|niet bevestigd|leeg/i.test(tekst)) return fallback || "Vertel me gerust nog iets meer, dan kunnen we verder.";
    return fallback || "Er ging even iets mis — zullen we het opnieuw proberen?";
  }
  function toonSignaleringen(sig, fallback) { melding(vriendelijk(sig, fallback)); }
  function netwerkfout() { melding(STUDIO_ONBESCHIKBAAR); }

  // ── Init ────────────────────────────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", start);
})();
