from bs4 import BeautifulSoup
import os, sys, re, csv, time
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import xwbi

done_items = ["HaranburuDebozino.xml",
"GarraldaDostatzia.xml",
"MendiburuIgande.xml",
"BarrensoroUztaro.xml",
"MogelJAAbarka.xml",
"MendiburuOtoitzI.xml",
"BarbierMixterio.xml",
"UriarteIlla.xml",
"ZerbitzariIxtorio.xml",
"MogelBIpuionak.xml",
"IztuetaGipuzkoa.xml",
"OtaegiKEguren.xml",
"ArreseETxindor.xml",
"LizarragaKristoBirjina.xml",
"Kanpion.xml",
"LeizarragaKalen.xml",
"EtxebZibuNoelak.xml",
"LarregiBerriko.xml",
"LekuonaMDukat.xml",
"MogelJAKonfesino.xml",
"Txirrita.xml",
"ZutagapeMatxin.xml",
"TartasArima.xml",
"OihenartNeurtitzak.xml",
"FraiOgetabost.xml",
"MunibeSariak.xml",
"LauaxetaSolteak.xml",
"AzkueEParnaso.xml",
"LabaienDomenjon.xml",
"LarregiZaharreko.xml",
"IztuetaDantza.xml",
"AranaSOlerkijak.xml",
"LabaienLurrikara.xml",
"ArreseEBidean.xml",
"LizardiAhizpak.xml",
"LabaienAgar.xml",
"LabaienPetrikillo.xml",
"MogelJAIkasbidea.xml",
"DuvoisinLaborantza.xml",
"AgirreAErakusBirjina.xml",
"UriarteBibliaIII.xml",
"AgirreAErakusKonfesio.xml",
"LabaienJostuna.xml",
"LauaxetaBarrijak.xml",
"ZubimendiZumalakarregi.xml",
"ElizanburuMHirur.xml",
"AnonimErrelazionea.xml",
"ConstantinDonjuan.xml",
"MendiburuDoktrina.xml",
"AnonimPartiak.xml",
"ZerbitzariGogorrak.xml",
"AnonimPartia.xml",
"IntxauspeItzulpenak.xml",
"AzkueRGuzur.xml",
"LizardiLaino.xml",
"TartasOnsa.xml",
"DuvoisinBibleaIII.xml",
"AnibarroAlkarturik.xml",
"AzkueROrtzuri.xml",
"MendiburuBiziera.xml",
"LizardiUmezurtz.xml",
"LabaienKalifornia.xml",
"AlthabeHunkailu.xml",
"AranbillagaImitazionea.xml",
"MaitieOtoitzak.xml",
"LizardiBiotz.xml",
"HarizmendiOfizioa.xml",
"ArrutiLukainka.xml",
"LeizarragaTesta.xml",
"OrixeEdesti.xml",
"IntxauspeElhestaldiak.xml",
"AnonimRuth.xml",
"IraizozLapurren.xml",
"KardaberazEjerzizioakI.xml",
"AdemaKantikak.xml",
"AbbadieLaborarier.xml",
"DasanzaAbisua.xml",
"AnonimKozinera.xml",
"AdemaPelegrin.xml",
"MogelJJEskolia.xml",
"FraiLelengo.xml",
"LhandeYolanda.xml",
"XahoAzti.xml",
"MendiburuFestegun.xml",
"EtxanizArraldea.xml",
"KardaberazSenarEmazte.xml",
"MunibeBurlado.xml",
"AzkarateGaltzaundi.xml",
"JoanategiSainduen.xml",
"MonhoOlerkiak.xml",
"ArreseBeitiaAldizkarietakoak.xml",
"ArgainaratzDeboten.xml",
"ArreseEZara.xml",
"LauaxetaAzalpenakI.xml",
"DuvoisinBibleaI.xml",
"EtxeitaAu.xml",
"Webster.xml",
"EtxepareJBideBuruxkak.xml",
"ZerbitzariGerlan.xml",
"ZabalaSermoiakI.xml",
"DuhaldeMeditazioneak.xml",
"UrruzunoSasiletrau.xml",
"AgerreKazetari.xml",
"IraizozYesuKristo.xml",
"BasabeEzkutua.xml",
"MogelJAIpuinak.xml",
"NunezPorru.xml",
"AnibarroEskuliburua.xml",
"EtxepareBPrimitiae.xml",
"KardaberazOndoiltzen.xml",
"EtxepareJLandGereziak.xml",
"DuvoisinBibleaII.xml",
"BetolazaDoktrina.xml",
"MogelJAErakasle.xml",
"BarbierPiarresI.xml",
"Lazarraga.xml",
"FraiOlgeeta.xml",
"HiriUrruGontze.xml",
"JohanategiBenoat.xml",
"OrixeKruz.xml",
"LaphitzBisaindu.xml",
"AnibarroGero.xml",
"AxularGero.xml",
"LabaienOstegun.xml",
"LizarragaSanduak.xml",
"ZubimendiAberri.xml",
"ZamarripaKili.xml",
"LabaienTxinparta.xml",
"FraiAzkeneko.xml",
"LapeireKredo.xml",
"HiriUrruZezenak.xml",
"KardaberazBerrionak.xml",
"JautarkolBiozkadak.xml",
"Xenpelar.xml",
"LizardiEzkondu.xml",
"MendiageKantak.xml",
"IparragirreEresiak.xml",
"EtxeberriaJKOngi.xml",
"RobinKoplak.xml",
"MujikaPernando.xml",
"AnabitarteDonostia.xml",
"ZerbitzariMetsikorat.xml",
"AgirreDLorea.xml",
"BarbierPiarresII.xml",
"UriarteBibliaI.xml",
"ZubiaDoktrina.xml",
"MaruriTxindorEgadak.xml",
"AlthabeBotanika.xml",
"ConstantinHaritxaba.xml",
"HiribarrenMontebideo.xml",
"HualdeDoktrina.xml",
"LabaienIrunxeme.xml",
"MaterreDotrina.xml",
"LarregiSainduen.xml",
"LauaxetaArrats.xml",
"ArxuBonaparte.xml",
"LeonImitazionea.xml",
"ZamarripaGoraBegira.xml",
"AbbadieAphezak.xml",
"BeriainMeza.xml",
"OlaetxeaDotrina.xml",
"DuvoisinEderra.xml",
"AnonimIrakasdea.xml",
"ArreseBeitiaKantaria.xml",
"IturriagaDialogoak.xml",
"IntxauspeHilabetia.xml",
"Bilintx.xml",
"LabaienMuga.xml",
"KardaberazKristabaI.xml",
"UrruzunoIruZiri.xml",
"LauaxetaItzuliak.xml",
"ArxuAlhegiak.xml",
"KirikinoBigarren.xml",
"MaisterImitazionia.xml",
"GoienetxeMarexal.xml",
"AzkueRUrlo.xml",
"UriarteBerbaldijak.xml",
"LabaienEuskalEguna.xml",
"UrruzunoUrzale.xml",
"AgirreDErromara.xml",
"LotsatiPoemak.xml",
"AgirreDSermoiak.xml",
"EtxeitaJosetxo.xml",
"LabaienMalentxo.xml",
"HualdeGore.xml",
"ArtolaPMotxa.xml",
"LarrekoNafar.xml",
"PouvreauImitazionea.xml",
"DakonagerreAtheka.xml",
"LardizabalBerriko.xml",
"LarrekoLekuko.xml",
"BaraziartMeditazione.xml",
"ArreseEBerrizte.xml",
"LeizarragaKonfesionea.xml",
"ZerbitzariBanhar.xml",
"AnonimRuthLlodio.xml",
"KardaberazIspillu.xml",
"LizardiAundiki.xml",
"ArrutiOlerkiak.xml",
"MendiburuFranzisko.xml",
"AzkueRLatsibi.xml",
"AnonimKristi.xml",
"UrruzunoZerura.xml",
"ZabalaSermoiakII.xml",
"HiriUrruMintza.xml",
"MogelJAPaskal.xml",
"ZabalaAlegiak.xml",
"LeizarragaKateximea.xml",
"KirikinoEdoGeuk.xml",
"MihuraImitazionea.xml",
"ArrueGIlla.xml",
"ZamarripaAnaiak.xml",
"ApaolazaTxerren.xml",
"BeriainDotrina.xml",
"KardaberazDebozino.xml",
"MogelJAErakusaldiak.xml",
"MendiburuOtoitzIII.xml",
"UbillosEkarlea.xml",
"ManterolaGGoiIzpiak.xml",
"AranaJIPekatu.xml",
"KardaberazIgnazio.xml",
"AranaJIIgnazio.xml",
"BustintzaEIpunak.xml",
"BatxiArrano.xml",
"GoietxeFableak.xml",
"LegazIkasbidea.xml",
"LeizarragaForma.xml",
"BarrutiaIkuskizuna.xml",
"EtxebSaraLauUrduri.xml",
"AstarloaPDomeka.xml",
"MendiburuReglak.xml",
"KardaberazJesusMaria.xml",
"AnibarroLorasorta.xml",
"OtxoluaBertolda.xml",
"EtxebDorreItxasoko.xml",
"VoltoireDialogoak.xml",
"KardaberazJosefa.xml",
"KardaberazMezaKomunioa.xml",
"Bordel.xml",
"ZerbitzariAzkaine.xml",
"BelapeireKatexima.xml",
"EtxamendiM.xml",
"LabaienIparragirre.xml",
"GaritaonandiaIpuin.xml",
"KardaberazKristabaII.xml",
"LafitteLiteraturaz.xml",
"GoniAgertziak.xml",
"KardaberazAfektoak.xml",
"KirikinoAbarrak.xml",
"BordesNoelen.xml",
"EtxebSaraGazteriari.xml",
"AgirreAErakusLegeak.xml",
"OxobiZonbait.xml",
"ManezaundiArtikuluak.xml",
"KardaberazDotrinea.xml",
"BarbierXokoan.xml",
"LarramendiTestuak.xml",
"DuvoisinSolastaldiak.xml",
"EgiategiEkheia.xml",
"OrixeTormes.xml",
"IturzaetaAzalduerak.xml",
"HiribarrenEgia.xml",
"LabaienJokua.xml",
"FraiSakramen.xml",
"OihenarteBelxitina.xml",
"ElizanburuMLehenagoko.xml",
"GazteluzarEgia.xml",
"ZerbitzariArtho.xml",
"LizarragaZenbaitSandu.xml",
"AzkueRBetiko.xml",
"UriarteBibliaII.xml",
"MendiburuOtoitzII.xml",
"LabaienBizarpeituti.xml",
"EguzkitzaAuzia.xml",
"HaranederGudu.xml",
"BelaustegigoitiaAndoni.xml",
"OrixeEuskaldunak.xml",
"LabaienPestaburu.xml",
"AnabitarteUsauri.xml",
"DuvoisinTelemake.xml",
"DuvoisinBaigorri.xml",
"AgirreAErakusSakramentu.xml",
"AzkueRBizkaira.xml",
"OrixeKiton.xml",
"KardaberazEjerzizioakIV.xml",
"ZamarripaFiri.xml",
"OtanoAlkar.xml",
"EtxeitaJaioterri.xml",
"ArrueGGenobeba.xml",
"HiribarrenEskaldunak.xml",
"EtxebSaraHatsapenak.xml",
"LauaxetaAzalpenakII.xml",
"AzkueRGaldua.xml",
"NunezEbaisto.xml",
"MendiburuDebozioa.xml",
"HarispeKarmela.xml",
"MikelestorenaZerura.xml",
"HiribarrenBestak.xml",
"TapiaOlerkiak.xml",
"HaranederEbanjelioa.xml",
"LeizarragaAbc.xml",
"MaruriLiliTxingar.xml",
"EtxebZibuManual.xml",
"LabaienGaltzaundi.xml",
"IturbeKuartetak.xml",
"EtxepareJBideBeribilez.xml",
"LardizabalZarreko.xml",
"ArbelbideIgandea.xml",
"AgirreDGaroa.xml",
"ArreseBeitiaAstiOrduetako.xml",
"OrixeMireio.xml",
"AgirreDKresala.xml",
"LizardiHitzlauz.xml",
"OrixeMuinetan.xml",
"AntiaAsiskoa.xml",
"PouvreauFilotea.xml",
"LafitteMurtuts.xml",
"GamizOlerkiak.xml"
]

vocab = {"G-0": "Q1436",
"G-ANT": "Q1437",
"G-BER": "Q1438",
"G-ERL": "Q1439",
"G-NAR": "Q1440",
"G-POE": "Q1441",
"G-SAI": "Q1442",
"M-0": "Q1443",
"M-16": "Q1444",
"M-17-1": "Q1445",
"M-17-2": "Q1446",
"M-18-1": "Q1447",
"M-18-2": "Q1448",
"M-19-1": "Q1449",
"M-19-2": "Q1450",
"M-20-1": "Q1451",
"M-20-2": "Q1452",
"E-0": "Q1453",
"E-BAT": "Q1454",
"E-BIZ": "Q1455",
"E-BNA": "Q1456",
"E-ERR": "Q1457",
"E-GIP": "Q1458",
"E-GNA": "Q1459",
"E-LAP": "Q1460",
"E-NAF": "Q1461",
"E-ZAR": "Q1462",
"E-ZUB": "Q1463"}

with open('ekc-authors-wd-wb.csv') as file1:
    authors_csv = csv.DictReader(file1, delimiter="\t")
    authors = {}
    for row in authors_csv:
        authors[row['authorname']] = row['MLV_Qid']


for filename in os.listdir('TEI-UTF8'):
    print(f"Now processing: {filename}")
    if filename in done_items:
        continue


    with open(f"TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
        soup = BeautifulSoup(tei_file, 'lxml')
    with open(f"TEI-UTF8/{filename}", 'r', encoding="utf-8") as tei_file:
        rawfile = tei_file.read()

    # child item (version level)

    statements = [{'prop_nr': 'P5', 'value': 'Q19', 'type': 'item'},
                  {'prop_nr': 'P192', 'value': 'Q22', 'type': 'item'}]

    author_qid = authors[soup.author.getText()]
    statements.append({'prop_nr': 'P13', 'value': author_qid, 'type': 'item'})

    title = soup.title.getText()
    statements.append({'prop_nr': 'P11', 'value': title, 'type': 'string'})
    labels = [{'lang': 'eu', 'value': f'{title} (TEI)'}]

    idno = soup.idno.getText()
    statements.append({'prop_nr': 'P191', 'value': idno, 'type': 'string'})
    textpage = f'Testua:{idno}/TEI'
    statements.append({'prop_nr': 'P124', 'value': textpage, 'type': 'string'})

    aliases = [{'lang': 'eu', 'value': idno}]
    descriptions = [{'lang': 'eu', 'value': f'testu klasikoaren TEI bertsioa [{idno}] (armiarma / EKC)'}]

    availability_statement = soup.availability.getText()
    url = re.search(r'http.*', availability_statement).group(0).replace("http://klasikoak.armiarma.com","https://klasikoak.armiarma.eus")
    statements.append({'prop_nr': 'P86', 'value': url, 'type': 'url'})

    textqid = xwbi.itemwrite({'qid': False, 'statements': statements, 'labels': labels, 'descriptions': descriptions, 'aliases': aliases})

    # parent item (work level)

    labels = [{'lang': 'eu', 'value': title}]
    statements = [{'prop_nr': 'P5', 'value': 'Q23', 'type': 'item'},
                  {'prop_nr': 'P50', 'value': textqid, 'type': 'item'}]

    statements.append({'prop_nr': 'P13', 'value': author_qid, 'type': 'item'})
    statements.append({'prop_nr': 'P11', 'value': title, 'type': 'string'})
    descriptions = [{'lang': 'eu', 'value': f'testu klasikoa [{idno}]'}]
    aliases = [{'lang': 'eu', 'value': idno}]


    keyws = []
    for keyw in re.findall(r'<list><item>([^<]+)</item></list>', rawfile):
        print(keyw, end=" > ")
        keyw_qid = vocab[keyw]
        print(keyw_qid)
        statements.append({'prop_nr': 'P189', 'value': keyw_qid, 'type': 'item'})

    parentqid = xwbi.itemwrite(
        {'qid': False, 'statements': statements, 'labels': labels, 'descriptions': descriptions, 'aliases': aliases})





    time.sleep(1)

# with open('ekc_authors.csv', 'w') as file:
#     file.write(result)

