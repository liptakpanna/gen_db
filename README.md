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
- [x] MySQL függőségek keresése backendben, lecserelés esetén miket kellene módosítani: **core** mappában MySQLBulkLoader fájlból tölt be táblába.
- [x] Adatbázis indexek felderítése (Slack-en utána kérdezni, ha nincs meg): migration.sql-ben KEY_MUTATION_EVENT_DETAILS, többi általában 1 oszlopra.
- [ ] Frontend kód átnézése: új fül hozzadása vagy keresések germline szűkítése milyen teendőkkel járna:

### 09.21. hét.
- [ ] Importálás megvizsgálása: hogyan történik, milyen bemenete lehet, **core** mappán kívül is implementálva van-e:
   **core** mappán belül **scripts**-ben találhatóak azok a command line-ból futtatható Perl scriptek, amik például az adatok importálását végzik, úgy hogy meghívják a **core**-s pl ImportMutSigData *run()* metódusát. Majd a kapott fájlt továbbítja a MutSigReader-nek, ami betölti a MySQLBulkLoader és a DaoMutSig segítségével az adatbázisba.
- [ ] Bináris fájlok betöltése: Semmi jelét nem találtam.
- [ ] Betöltés multithread?

### 09.28. hét.
 - Foreign key check ki van kapcsolva a MySQLBulkLoader-ben
 - Session controllert is kell indítani hozzá
 
### 10.05. hét.
 - Fájl kérés teszteléshez -> melanoma tanulmány
 - Logolásokkal kiegészítés: MySQLBulkLoader-ben, hogy kiderüljön, hol a szűk keresztmetszet

### 10.12. hét.
 - Backend szerkezetének átnézése
 - Email küldes kérdésekkel: fájl importálás core mappán kívül is megtalálható-e? párhuzamos importálás? bináris fájl betöltése?
 
### 10.19. hét.
 - Adatbázis verziók nem voltak kompatibilisek a backend verzióval/seed adatbázissal, ezért manuálisan kellett kiegészíteni a hiányzó oszlopokkal.
 - Futattás teszt tanulmányokkal
 - Email-re érkezett válasz: nem található meg egyelőre, mert még nem tudják hogyan csinálják; problémás, mert vannak olyan műveletek, ahol ellenőrizni kell, hogy létezik-e már rekord azon a néven, ha nem akkor hozzáadni; nincs rá lehetőség.
 
### 10.26.
 - Futtatás a melanoma tanulmányra: log elemzése, ennek alapján logolás bővítése
    - ImportMutationData osztályban logolás: 
        - 1 sec alatt 5-15 ezer sort dolgoz fel az extended_mutation fájlból.
        - Sorok feldolgozása közben lekérdezések: Sample(Cached) Cancer_Study_ID(FK) és Stable_ID(Unique) alapján, Uniprot Uniprot_ID(Key) alapján, Gene(cached) geneSymbol alapján guess-ek közül, Mutation_event entrez,chr,start_pos,end_pos,tumor_seq,protein_change,type(közös index) alapján
    - 1.4 millió adat feldolgozása, de ebből csak kb 550k kerül be : 
        - Kb 10p ImportMutationData sorok ellenőrzése, majd kb fél perc, hogy tempfile-ba betöltse mutation_event és mutation rekordokat
        - Kb 7p Load tempfileból into mutation_event , FK check off, ez MySQLBulkLoader
        - Kb 18p Load tempfileból into mutation, FK check off, ez MySQLBulkLoader
        - Egész tanulmány importálás 40 percet vesz igénybe
    - Ötlet: Tempfile több kisebb részre osztása és ezek párhuzamos betöltése, de kell clean up, ha bármelyik szál hibával ér véget, illetve az ID auto_increment mutation_event-nél és előre be van állítva ellenőrizni kell, hogy okozhat-e problémát.
 - MySQL-ben létezik-e bináris fájl betöltés: pg_read_binary_file megfelelője - esetleg blob, de az oszlop, és lassabb.
 
### 11.02. hét
 - Skálázódás kérdése: eddig 1.4 millió mutációból elfogadott, azaz valójában betöltött 550 ezret
  - Több: mivel sok kritériumnak kell megfelelni, ezért más cBioPortal-os tanulmányokból szerettem volna hozzáadni mutációkat, de az extended_mutation fájlok header-ja eltérő oszlopból áll (132 a felhasznált melanoma tanulmányé). Ahhoz, hogy ez működjön nem elég hozzáadni a sorokat, hanem korrigálni kell ezeket az oszlopbeli eltéréseket.
  - Kevesebb: kb megfelezve 700k mutációból (viszonylag véletlenszerűen törölt) 310ezret olvasott be. 
    - Kb 5 perc alatt olvasott végig 700 ezer sort
    - Kb 2 perc Load tempfileból into mutation_event
    - Kb 4 perc Load tempfileból into mutation
    - Egész csökkentett tanulmány importálása 11 perc volt
    
### 11.09. hét
- data_mutations_extended fájl oszlopainak értelmezése: [Összefoglaló](https://github.com/liptakpanna/gen_db/blob/master/docs/mutation_oszlopok.odt)
- Ezek alapján új mutációk generálása, hogy az importált mutációk száma elérhesse az 1 milliót:
    - 2 millió adat feldolgozása, ebből kb 1.14 millió kerül be ténylegesen: 
        - Kb 15p ImportMutationData sorok ellenőrzése, majd kb 2*fél perc, hogy tempfile-ba betöltse mutation_event és mutation rekordokat
        - Kb 32p Load tempfileból into mutation_event
        - Kb 56p Load tempfileból into mutation
        - Egész tanulmány importálás 2 órát vett igénybe (előző tanulmányok törölve lettek előtte, így mindent 0-ról importált)
        
### 11.16. hét
 - Plotok:
 
 ![Line processing plot](https://github.com/liptakpanna/gen_db/blob/master/docs/cbioportal_line_process_plot.png) ![Load data into database plot](https://github.com/liptakpanna/gen_db/blob/master/docs/cbioportal_load_data_plot.png)
 - A sorok feldolgozása után egy tempfile-ból kerülnek betöltésre a rekordok az adatbázisba. Egy táblához tartozó tempfile a betöltendő sorok adatait tartalmazza tab-bal tagolva.
 - Párhuzamosítás:
