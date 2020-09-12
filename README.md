# Genetikai adatbázisok

[Bevezető előadás](https://github.com/liptakpanna/gen_db/blob/master/docs/gen_db.pptx)

## cBioPortal

[Github](https://github.com/cBioPortal/cbioportal)

[Dokumentáció](https://docs.cbioportal.org/)

Külön dokumentáció, repo van [backend-ről](https://github.com/cBioPortal/cbioportal/blob/master/docs/Backend-Code-Organization.md) és [frontend-ről](https://github.com/cbioportal/cbioportal-frontend).

- Backend: Java, Spring, Maven
- Frontend: React, TypeScript, MobX

Fejlesztést támogatják [(guidlines)](https://github.com/cBioPortal/cbioportal/blob/master/docs/Backend-Development-Guidelines.md): van [Slack channel](https://slack.cbioportal.org/), ahol segítenek, ha kérdés van.

License: ha jól értelmezem, akkor szabadon felhasználható, annyi a megkötés, hogy mielőtt valamit publikussá akar tenni az ember, köteles megosztani előbb a cBioPortal-lal.

* cBioPortal fejlesztői dokumentációját, struktúráját megnézni 
    - [ ] Függőségek: 
    - [ ] Adatbázis-kezelő:
    - [ ] Adatbázisséma:
* Összegyűjteni, hogy ezek alapján mi konfigurálható:
    - [ ] Germline mutációk hatékonyabb feltöltése (indexelés lassú?)
    - [ ] Mutalisk: szignatúra dekompizíció lehetősége -> ezek hasonlóak? [Issue1](https://github.com/cBioPortal/cbioportal/issues/7833), [Issue2](https://github.com/cBioPortal/cbioportal/issues/7057)
    - [ ] Lehetőség inbreeding mutációk keresésére
