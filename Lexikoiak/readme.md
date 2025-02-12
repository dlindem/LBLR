# Euskal testuetatik lexikoia ateratzeko

Lexikoia: Testu batean agertzen diren formak, zerrenda batean, ondorengo datuekin batera:
* Testu-hitza (tokena)
* Testu-hitz egokitua, OEH-ko lemategiarekin konparatuko dena
  * Horretarako, `data/grafia_arauak` karpetan dauden arautegiak erabiltzen dira; autore bakoitzak bere arautegia izan dezake.
* OEH lemategitik, lema izateko hauteslea
  * Hasperena ez idatzi izana posibletzat hartzen da
  * OEH lemaren amaierako -a gabe ere bilatu egiten da
  * testu-hitz egokituaren hasierarekin bat datorren lema-hauteslee luzeena aukeratzen da
* OEH lemak MLV Wikibasean duen identifikatzailea
  * MLV Wikibaseko orritik, OEH-ra joan daiteke
* Testu-hitzaren testuingurua (esaldi osoa hartzen saiatzen da)

## Wikisource-ko dokumentuen egitura

Wikisourceko dokumentuetako edukiak lexikoia ateratzeko aintzat har daitezen, ondorengo baldintzak bete behar dira:
* Edukia `<span lang="EU"> ... </span>` bezalako elementuen barruan egon behar da
  * Orain, `EU`, `ES` eta `LA` hizkuntzetarako atera daitezke lexikoiak
* Dokumentuak `{{aingura|x}}` formatuko aingurak behar ditu
  * Aintzat hartzeko lehenengo edukiaren aurretik, aingura bat egon behar da
  * Aingurak `<span lang="xx">` elementuen kanpoan edo barruan egon daitezke
  * Paragrafo bakoitzak hasieran bere aingura izatea komeni da. Paragrafo barruan ez da komeni
* Paragrafo-saltuak lerro huts batez adierazten dira (bi errenkada-salto paragrafoaren amaieran)
* Jatorrizko testuaren parte ez diren elementuak (paratestuak) `<ins>...</ins>` elementuaren barruan egon behar dira
  * Lexikoia ekoizteko, ez dira aintzat hartuko, nahiz eta `<span lang="xx">` baten barruan egon
  * Paragrafo osoak izan behar dira (`<ins>...</ins>` aurretik eta ondoren lerro huts bat)
* Oin-oharrak `<ref>...</ref>` elementuaren barruan egon behar dira, oin-oharrari dagokion tokian bertan
  * Lexikoia ekoizteko, ez dira aintzat hartuko, nahiz eta `<span lang="xx">` baten barruan egon
* `<cite>...</cite>` jatorrizko egileak egiten dituen aipuentzako erreferentzia bibliografikoak, adib. `(Joan 19.)`
* `<ref>...</ref>` `<ins>...</ins>` barruan egon daiteke: `<ins>...<ref>...</ref></ins>`.
* `<ins>...</ins>` eta `<ref>...</ref>` ez diren bestelako html tag-ak eliminatu egingo dira lexikoia ekoitzi baino lehen; barruan eduki dezaketen testua, aldiz, ez.

## Bildumaren parte diren Wikisource dokumentuak

Lexikoia ateratzeko, testua Wikisource proiektua izan behar da.
* Hiru motako wikisource proiektuak daude:
  * Wikisource orri bakar batean bertan testua dutenak (adib. Etxepare Linguae Vasconum Primitiae)
  * Wikisource orri batzuetan bertan testua dutenak (kapituloka, adib. Axular Gero)
  * PDF baten transkripzioa direnak (PDF orrialde bakoitzak bere testu-orria du, adib. Larramendi Azkoitiko Sermoia)
* `wikisource_proiektuak.csv` fitxategian dago proiektuen zerrenda
  * Beti:
    * Lehenengo zutabean: Wikisource proiektuaren orrialde nagusia
    * Hainbat (kapitulu-)orrialde badira, orrialde nagusia jarri (aurkibidea duena)
  * PDF transkripzioa bada:
    * Bigarren zutabean: PDF fitxategiaren helbidea, orrialde zenbakirik gabe
    * Hirugarren zutabean: PDF-aren orrialde kopurua