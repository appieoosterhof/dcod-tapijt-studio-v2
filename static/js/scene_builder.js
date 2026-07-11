/* Scene Builder (BUILD-006) — losstaande pagina, raakt app.js/de bestaande
   Dessinator-flow niet aan. Vier hoekpunten worden altijd handmatig
   gesleept: geen automatische detectie, geen AI. */
(function () {
  var huidigeSceneId = null;
  var polygon = null; // [[x,y],[x,y],[x,y],[x,y]] als fractie van de afbeelding, TL/TR/BL/BR
  var kleuren = ['#ff4d4d', '#4dff4d', '#4d8cff', '#ffe14d'];
  var labels = ['TL', 'TR', 'BL', 'BR'];
  var sleepIndex = null;

  function statusTonen(tekst, elId) {
    document.getElementById(elId || 'status').textContent = tekst;
  }

  function standaardPolygon() {
    // Redelijk startpunt: een ingezoomd vlak in het midden-onder van de
    // afbeelding, puur als startpositie om te verslepen -- geen kalibratie.
    return [[0.25, 0.55], [0.75, 0.55], [0.05, 0.95], [0.95, 0.95]];
  }

  function tekenPunten() {
    var container = document.getElementById('sceneAfbeelding');
    var img = document.getElementById('sceneImg');
    var breedte = img.clientWidth, hoogte = img.clientHeight;
    document.querySelectorAll('.punt').forEach(function (p) { p.remove(); });
    polygon.forEach(function (p, i) {
      var punt = document.createElement('div');
      punt.className = 'punt';
      punt.style.left = (p[0] * breedte) + 'px';
      punt.style.top = (p[1] * hoogte) + 'px';
      punt.style.background = kleuren[i];
      punt.dataset.index = i;
      punt.title = labels[i];
      container.appendChild(punt);
    });
  }

  document.addEventListener('pointerdown', function (e) {
    if (!e.target.classList || !e.target.classList.contains('punt')) return;
    sleepIndex = +e.target.dataset.index;
    e.target.setPointerCapture && e.target.setPointerCapture(e.pointerId);
    e.preventDefault();
  });

  document.addEventListener('pointermove', function (e) {
    if (sleepIndex === null) return;
    var container = document.getElementById('sceneAfbeelding');
    var rect = container.getBoundingClientRect();
    var fx = (e.clientX - rect.left) / rect.width;
    var fy = (e.clientY - rect.top) / rect.height;
    polygon[sleepIndex] = [Math.round(fx * 1000) / 1000, Math.round(fy * 1000) / 1000];
    tekenPunten();
  });

  document.addEventListener('pointerup', function () { sleepIndex = null; });

  function toonKalibratieVoorScene(scene) {
    huidigeSceneId = scene.id;
    polygon = (scene.surface && scene.surface.polygon && scene.surface.polygon.length === 4)
      ? scene.surface.polygon
      : standaardPolygon();
    var img = document.getElementById('sceneImg');
    img.src = scene.achtergrond_url;
    document.getElementById('kalibratieBlok').style.display = 'block';
    document.getElementById('kalibratieStatus').textContent = '';
    img.onload = tekenPunten;
    if (img.complete) tekenPunten();
  }

  async function scenesLijstLaden() {
    var resp = await fetch('/api/scenes');
    var data = await resp.json();
    var ul = document.getElementById('scenesLijst');
    ul.innerHTML = '';
    if (!data.scenes || data.scenes.length === 0) {
      var leeg = document.createElement('li');
      leeg.textContent = 'Nog geen scenes aangemaakt.';
      leeg.style.cursor = 'default';
      ul.appendChild(leeg);
      return;
    }
    data.scenes.forEach(function (s) {
      var li = document.createElement('li');
      var naam = document.createElement('span');
      naam.textContent = s.naam;
      var badge = document.createElement('span');
      badge.className = 'badge';
      badge.textContent = s.gekalibreerd ? 'gekalibreerd' : 'nog niet gekalibreerd';
      li.appendChild(naam);
      li.appendChild(badge);
      li.addEventListener('click', async function () {
        var r = await fetch('/api/scenes/' + s.id);
        var scene = await r.json();
        toonKalibratieVoorScene(scene);
        window.scrollTo({ top: document.getElementById('kalibratieBlok').offsetTop - 20, behavior: 'smooth' });
      });
      ul.appendChild(li);
    });
  }

  document.getElementById('aanmakenKnop').addEventListener('click', async function () {
    var naam = document.getElementById('naamVeld').value.trim() || 'Naamloze scene';
    var bestandVeld = document.getElementById('bestandVeld');
    if (!bestandVeld.files || !bestandVeld.files[0]) {
      statusTonen('Kies eerst een achtergrondafbeelding.');
      return;
    }
    var form = new FormData();
    form.append('naam', naam);
    form.append('achtergrond', bestandVeld.files[0]);
    statusTonen('Bezig met aanmaken...');
    try {
      var resp = await fetch('/api/scenes', { method: 'POST', body: form });
      var scene = await resp.json();
      if (!resp.ok) { statusTonen('Fout: ' + (scene.error || resp.status)); return; }
      statusTonen('Scene "' + scene.naam + '" aangemaakt.');
      toonKalibratieVoorScene(scene);
      scenesLijstLaden();
    } catch (err) {
      statusTonen('Fout: ' + err);
    }
  });

  document.getElementById('opslaanKnop').addEventListener('click', async function () {
    if (!huidigeSceneId) return;
    var el = document.getElementById('kalibratieStatus');
    el.textContent = 'Opslaan...';
    try {
      var resp = await fetch('/api/scenes/' + huidigeSceneId + '/calibratie', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ polygon: polygon }),
      });
      var data = await resp.json();
      if (!resp.ok) { el.textContent = 'Fout: ' + (data.error || resp.status); return; }
      el.textContent = 'Kalibratie opgeslagen.';
      scenesLijstLaden();
    } catch (err) {
      el.textContent = 'Fout: ' + err;
    }
  });

  scenesLijstLaden();
})();
