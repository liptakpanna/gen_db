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

### 09.07. hét
* cBioPortal fejlesztői dokumentációját, struktúráját megnézni 
    - [x] Függőségek: [mappák köztiről kép](https://github.com/cBioPortal/cbioportal/raw/b81ec59ba59032ce00449e3773fb92c2d3be6d8c/docs/images/maven-module-dependencies.png). JWT tokennel autorizál, oauth2-t felhasználva. **service** mappában Service-k, **web** mappában Controller-ek.
    - [x] Adatbázis-kezelő: MySQL adatbázist használ. Backend oldalon MyBatis lib-el van megoldva az Entity-k elérése pl **model**/Gene, **persistance-mybatis**/GeneMapper (interface), GeneMapperMyBatisRepository (interface implementációja), GeneMapper.xml <- itt van SQL utasítás részletesen
    - [x] Adatbázisséma: [kép](https://github.com/cBioPortal/cbioportal/blob/master/db-scripts/src/main/resources/cbioportal-er-diagram.pdf)
* Összegyűjteni, hogy ezek alapján mi konfigurálható:
    - [ ] Germline mutációk hatékonyabb feltöltése (indexelés lassú?): lehetséges, sőt támogatott [link](https://www.cbioportal.org/results?session_id=5b2cd03c498eb8b3d566adbc)
    - [ ] Mutalisk: szignatúra dekompizíció lehetősége -> ezek hasonlóak? [Issue1](https://github.com/cBioPortal/cbioportal/issues/7833), [Issue2](https://github.com/cBioPortal/cbioportal/issues/7057)
    - [ ] Lehetőség inbreeding mutációk keresésére
  
### 09.14. hét
**TODO:**
- [ ] MySQL függőségek keresése backendben, lecserelés esetén miket kellene módosítani:
- [ ] Adatbázis indexek felderítése (Slack-en utána kérdezni, ha nincs meg):
- [ ] Frontend kód átnézése: új fül hozzadása vagy keresések germline szűkítése milyen teendőkkel járna:
