# VISION-001 — Floor Visualization Platform

**Status:** strategische productvisie voor de lange termijn. Richtinggevend voor toekomstige BUILD's. **Niet met terugwerkende kracht van toepassing op reeds afgeronde BUILD's** — met name BUILD-004 (Context Interpreter) blijft ongewijzigd, zowel qua scope als implementatie. Dit document bevat geen architectuurbesluit dat vandaag iets in de codebase wijzigt.

---

## Kernbesluit

De DCOD Dessinator wordt op de lange termijn ontwikkeld als een **Floor Visualization Platform**.

De visualisatie werkt altijd vanuit één gestandaardiseerd **Scene-model**, ongeacht de bron van de invoer.

## Toekomstige invoerbronnen

- **DCOD Scene** — een voorgekalibreerde scene, zoals de bestaande kantoor-mockup die deze sessie is gekalibreerd.
- **Eigen projectfoto** — een door de architect aangeleverde foto van de daadwerkelijke projectruimte.
- **Eigen 3D-impressie** — een door de architect aangeleverde 3D-render of -impressie.

Alle invoer wordt eerst omgezet naar één Scene. De **Floor Visualization Engine** werkt uitsluitend met deze gestandaardiseerde Scene — niet rechtstreeks met de brongegevens (foto, 3D-impressie, of vooraf gekalibreerde mockup).

## Architectuurprincipe

**De vloerafwerking is het primaire ontwerpobject. De ruimte is uitsluitend context voor de visualisatie.**

Dit keert de nadruk om ten opzichte van hoe de huidige mockup-functionaliteit is opgebouwd (een vaste foto met een ingepast vloerpatroon): niet de ruimte staat centraal met de vloer als toevoeging, maar de vloerafwerking staat centraal en de ruimte — via welke bron dan ook — is het decor waarin die wordt getoond.

## Relatie tot de bestaande architectuur

- **Mockup Engine** (één van de vier deelsystemen uit `CLAUDE.md`) is het bestaande, werkende systeem waar deze visie op voortbouwt — met name de recent gekalibreerde kantoor-mockup (`ROOM_MOCKUPS`, `static/js/app.js`) is in deze visie te herkennen als een eerste, handmatige versie van wat later een "DCOD Scene" zou worden.
- **DesignContext Model v1** heeft mockups expliciet buiten de v1-scope geplaatst ("mockups vallen buiten de DesignContext van v1"). Deze visie **wijzigt die scope-keuze niet met terugwerkende kracht** — ze beschrijft een toekomstige richting, geen huidig besluit om die scope-grens nu te verleggen.
- **BUILD-004 (Context Interpreter)** blijft volledig ongewijzigd, zowel in scope als in reeds gecommitte implementatie. Deze visie is er niet met terugwerkende kracht op toegepast en had dat ook niet moeten worden — dat was de reden om dit als apart document vast te leggen in plaats van BUILD-004 aan te passen.

## Reikwijdte van dit document

Dit is een visiedocument, geen BUILD en geen SPEC. Het legt een richting vast, geen concrete verantwoordelijkheid, geen Definition of Done, geen technisch ontwerp. Wanneer deze visie de basis wordt voor concreet werk, verdient dat een eigen BUILD (met eigen functioneel en technisch ontwerp, volgens dezelfde gecontroleerde-migratie-discipline als BUILD-002 t/m BUILD-005), niet een uitbreiding van een bestaande, afgeronde BUILD.
