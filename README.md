# Genetikai adatbázisok - 2021

Cél: VCF és egyéb genomikai adatok támogatására adatbázis létrehozása.

### 02.15. hét
- VCF fájl adatstruktúrájának vizsgálata:
    Variánsok a referencia genom mentén
- [VCFServer](https://pubmed.ncbi.nlm.nih.gov/31127704/): 
    - web file system, core: C, frontend: JS, backend: Perl
    - VCF -> JSON array -> MongoDB
- Heti TODO: TileDB, SeqArray, MonetDB, Szakirodalmak olvasása
  
### 02.22. hét
- [SeqArray](https://academic.oup.com/bioinformatics/article/33/15/2251/3072873)
    - C++ impl, R-ben elérhető (BioConductor)
    - Genomic Data Structure: multiple array-oriented datasets
    - tömörítés, parallel: több local file-ba ír és összemergeli

-[GMQL](https://re.public.polimi.it/retrieve/handle/11311/1146279/539727/290300a109.pdf)
    - GenoMetric Query Language
    - region- és array-based gen representation
    - Apacha Spark, cloud-based engine
    - row-based tárolás, join rosszul skálázódik
    - webes interface
    - 3D-s tárolás: koordináta, minta, signal (minden attribútum)
    - Scala API

-[GenomicsDB](https://gatk.broadinstitute.org/hc/en-us/articles/360035891051-GenomicsDB)
    - GVCF adatformátum: minden egyes genom pozícióra van rekord, akkor is, ha nincs ott mutáció
    - API: Java, Python, C++
    - parallel, columnar sparse arrays
    - shared-nothing architektúra

-[MonetDB SAM/BAM modul](https://core.ac.uk/download/pdf/301631246.pdf)
    - Column store
    - SAM/BAM betöltése db-be, exportálás, gyakori szekvencia illesztési function-ok SQL-be implementálása
    - R támogatás
    - Szekvenciális/Pairwise tárolási séma
    - Future Work: VCF modul készítése a MonetDB-hez

-[TileDB](https://github.com/TileDB-Inc/TileDB-VCF)
    - Multidimensional array architektúra
    - C++ impl, API: Java, Python, C, C++, terminál kliens
    - jó (lineáris) skálázódás, több 100k exomon tesztelt
    - Párhuzamos query-ket támogatja: minden write független, lock-free, konzisztens
    - multi-sample VCF-ek összemergelése
    - 3D-ben a VCF adatokat tárolja, 1D-be a metaadatokat
    - Fejlesztik folyamatosan

- Heti TODO:
    - MonetDB: rákérdezni, hogy VCF modult megvalósították-e, milyen index lehetőségek vannak
    - TileDB: architektúra átnézése, kipróbálás, létezik-e SQL-szerű lekérdezés, Query optimalizálás, fejlesztői doksi, storage manager vagy db?


### 03.01. hét
- MonetDB: nincs VCF modul, de leveleztem velük és érdekli őket a lehetőség

- TileDB:
    - Más tanulmányban Storage manager-ként hivatkoznak rá
    - Data management system: dense és sparse array-hez is optimális
    - Update műveletek batch-ekbe vannak, amik fragmenteket alkotnak és szekvenciálisan alkalmazzák őket timestamp alapján, ha túl sok a fragment akkor consolidation lépés keretében többet összeolvasztanak
    - párhuzamos: multithreas és multiprocess, lightweight lockolás, atomi műveletek
    - Array: dimenziók (domain-ek kombinációja), attribútumok
    - Adattípusok: int, float, char, vektor (fix vagy változó hossz)
    - Tárolás: hiába multidim disk-en 1D-ben kell -> global cell order meghatározása (sor/oszlop folytonos állítható)
        - Tile méret megadása, tile-on belüli és tile order megadása
        - Sparse esetben: data tile korlátos, hogy hány nem üres cella van benne
        - Tile alapú tömörítés
        - Fizikailag: 1 array - 1 folder és azonbelül pl minden attríbútumhoz 1-2 file tartozik
    - Sparse array indexelés: R-fa alapú
    - Windows-on nem sikerült kipróbálni
    - Nincs SQL-szerű lekérdező nyelv hozzá

- MonetDB vs PostgreSQL tanulmány [link](https://www.researchgate.net/publication/280232082_Genome_Data_Management_using_RDBMSs)
    - PostgreSQL: disk-en van -> I/O optimalizálás az index célja
    - MonetDB: main-memory-ban van -> CPU számítás optimalizálás az index célja
        - Önoptimalizáló rendszere van: adaptive index, CPU-tuned query execution, run-time query optimalization
        - 1 oszlop nem fér a memóriába, akkor swap és memory mapped file-ok segítségével oldja meg -> csökken a performancia

- Heti TODO:
    - PostgreSQL: column store megoldások keresése és kipróbálása
    - Összehasonlító tanulmányban szereplő séma és lekérdezések kipróbálása VCF adatokon: MonetDB, PostgreSQL - column store is

### 03.08. hét
- [Row vs Column store tanulmány](https://dl.acm.org/doi/abs/10.14778/1687553.1687625):
    - Hogyan lehet column store architektúrát imitálni row-store adatbázisban?
        - Vertikális partíció vagy minden oszlop indexelése
    - Query executor és storage layer level-en viszont szignifikáns különbségek vannak, úgy gondolják nem lehet ugyanazt elérni

- PostgreSQL column store megoldások:
    - [Swarm64](https://swarm64.com/columnstore-index-webcast/): csak oszlop alapú indexelés
    - [ZedStore](https://github.com/greenplum-db/postgres/tree/zedstore): belső felépítés B-fák alapján, performancián nem javít sokat, még fejlesztés alatt áll
    - [cstore](https://github.com/citusdata/cstore_fdw): sok hiányossága van pl nincs index, p-key, f-key, de ez a legígéretesebb, ezt tesztelem

- Szintetikus adatokon adatbázisok tesztelése:
![Adatbázisok összehasonlító elemzése](https://github.com/liptakpanna/gen_db/blob/master/docs/first_db_test.png)

- Heti TODO:
    - Kooplex példa VCF-ekre és a megadott minta lekérdezések alapján a tesztek megismétlése
    - MonetDB memória csökkentés hogyan befolyásolja a performanciát

### 03.15. hét
- VCf adatokon végzett tesztek:
![Adatbázisok összehasonlító elemzése 2](https://github.com/liptakpanna/gen_db/blob/master/docs/second_db_test.png)

- Heti TODO:

### 03.22. hét
- Adatexploráció:
    - sample_coverage ref vs mutations ref: eltérő, mert a sample_coverage ref 1 adott poz-ra vonatkozó referencia bázis, a mutations ref pedig magába foglalhat több bázist pl ATACATG -> A mutáció
    - allel_freq: mintánként eltérő
- Cache törlésével 1.futtatás vizsgálata
- Redundáns sémák tesztelése