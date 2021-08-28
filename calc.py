import dbAccess as db

def mainCalculations(pSliderValues, pConstant):
    """
    help this function.....
    """
    Zinsen = pConstant["Zinsen"]
    FinanJahren = pConstant["FinanJahren"]
    BedienerGehalt = pConstant["BedienerGehalt"]
    Anzahlbediener = pConstant["Anzahlbediener"]
    VerwaltungsKosten = pConstant["VerwaltungsKosten"]
    HaftPflichtVersicherung = pConstant["HaftPflichtVersicherung"]
    WartungBohranlage = pConstant["WartungBohranlage"]
    ReparaturBohranlage = pConstant["ReparaturBohranlage"]
    ErsatzteilBohranlage = pConstant["ErsatzteilBohranlage"]
    SonstigeKosten = pConstant["SonstigeKosten"]
    MaschinePreis = pSliderValues["gesamtInvestitionSlider"]
    InstandErsatzteile = pSliderValues["gesamtInstandhaltungSlider"]
    BohrstundenProJahr = pSliderValues["bohrstundenProJahrSlider"]
    MaschineRestWert = pSliderValues["maschinenRestWertSlider"]
    baustellenVariabelKosten =  pSliderValues["baustellenVariabelKostenSlider"]
    preisProMeterSlider =  pSliderValues["preisProMeterSlider"]
    LaengeBohrungSlider =  pSliderValues["LaengeBohrungSlider"]
    baustellenGesamtzeitSlider =  pSliderValues["baustellenGesamtzeitSlider"]

    # Berechnungen fuer ein Jahr
    AnnuityFactor = (((1+Zinsen)**FinanJahren)*Zinsen)/(((1+Zinsen)**FinanJahren)-1)
    JahresFinan = (((100-MaschineRestWert)/100)*MaschinePreis)*AnnuityFactor
    GemeinkostenEinJahr = JahresFinan+(BedienerGehalt*Anzahlbediener)+VerwaltungsKosten+HaftPflichtVersicherung+SonstigeKosten
    InstadhaltungskostenEinJahr = InstandErsatzteile
    BasisJahrKost = GemeinkostenEinJahr+InstadhaltungskostenEinJahr
    BasisStundenSatzMaschine = BasisJahrKost/BohrstundenProJahr
    AnzahlBaustellenProJahr = BohrstundenProJahr/baustellenGesamtzeitSlider
    VariableBohrungskostenEinJahr = AnzahlBaustellenProJahr*baustellenVariabelKosten
    GesamtJahresKosten = GemeinkostenEinJahr+InstadhaltungskostenEinJahr+VariableBohrungskostenEinJahr
    UmsatzProJahr = preisProMeterSlider*LaengeBohrungSlider*AnzahlBaustellenProJahr
    Gewinn=UmsatzProJahr-GesamtJahresKosten
    ROI=Gewinn/UmsatzProJahr*100

    # Berechnungen fuer n Finanzjahre 
    TCO = (GemeinkostenEinJahr+InstadhaltungskostenEinJahr+VariableBohrungskostenEinJahr)*FinanJahren
    InstadhaltungskostenFinanzjahre = InstadhaltungskostenEinJahr*FinanJahren
    GemeinkostenFinanzjahre = GemeinkostenEinJahr*FinanJahren
    VariableBohrungskostenFinanzjahre = VariableBohrungskostenEinJahr*FinanJahren

    KumGewinn = []
    for jahr in range(1,FinanJahren+1):
        KumGewinn.append(jahr*Gewinn)

    Ergebnisse = {
        "Basisstundensatz": BasisStundenSatzMaschine,
        "TCO": TCO,
        "ROI": ROI, 
        "InstadhaltungskostenEinJahr": InstadhaltungskostenEinJahr,
        "GemeinkostenEinJahr": GemeinkostenEinJahr,
        "VariableBohrungskostenEinJahr": VariableBohrungskostenEinJahr,
        "InstadhaltungskostenFinanzjahre": InstadhaltungskostenFinanzjahre,
        "GemeinkostenFinanzjahre": GemeinkostenFinanzjahre,
        "VariableBohrungskostenFinanzjahre": VariableBohrungskostenFinanzjahre,
        "Gewinn": Gewinn,
        "KumGewinn": KumGewinn,
        "GesamtJahresKosten": GesamtJahresKosten, 
        "UmsatzProJahr": UmsatzProJahr,
        "FinanzJahre": FinanJahren
    }

    return Ergebnisse

def compareMaschines(pDB, pID1, pID2):
    result1 = db.getMaschine(pDB, pID1)
    result2 = db.getMaschine(pDB, pID2)

    # Comparing begins:
    ComparisonResultsProd = [] #[[Caption, Value1, Value2, Difference], ... ]
    ComparisonResultsDownTime = []
    ComparisonResultsVarCost = []
    ComparisonResultsEinsatz = []
    ComparisonResultsWiderverkauf = []

    Captions = ["Max. Drehmoment (nM)", "Max. Zugkraft (kN) ", "Vorschubgeschwindigkeit (sek/m)", "Max. Spülungsleistung", "Gestängelänge", "Gestängewechselzeit (sek)", "Kurzzeitige Turboleistung", "Bohrautomatic", "Kabine Ergonomie", "Schnell Druckentlastung & Wiederfüllung", "Schnell Auf- und Abbaubar (auch Einrichten)", "Allg. Sicherheit", "Kettenfahrwerk Fahrbarkeit", "Quickconnect für Bohrwerkzeuge", "Automatische Fehlermeldung", "Nothydraulik", "Möglicheit der Ferndiagnose", "Abrufbare Dokumentation per Internet", "Online Software Updates", "Bedienerfreundliche Wartungszugänglichkeit", "Manuel Bohren ohne Steuerung", "Teile bestellen per Internet", "Bohrplanungssoftware abrufbar", "Kommunikationsystem in der Kabine", "Verstellbare Motorleistung auch auto. Anpassung", "Niedrigere Max. Motordrehzahl", "Verstellpumpen und -motoren Technik", "Aufnahme von Leistungsdaten", "Gestängeschoned Schmier & Klemmlösung", "Hohe Festigung über Ankersystem", "Hohe Mischleistung", "Hochdruckreiniger an der Maschine", "Optimale Bohrwerkzeugauswahl", "Maschineabmessungen im Betrieb", "Fußdruck/Leistung Verhältiss", "Laffette Neigungsbereich", "Gestängebox Austauschbarkeit", "Gestängetyp Austauschbarkeit", "Einzelne Gestänge Austauschbarkeit", "Diverse Möglichkeiten der Verankerung", "Diverse Möglichkeiten der Gesteinsbohrung", "Leistungsstarkes Fahrwerk auch Bodenschonend", "Ösen zum Heben", "Kabelgeführtes Bohren", "Zugkraftmessung beim Rohreinzug", "Starkes Beleuchtungssystem Nachts", "Sehr hochwertiges Design und Verarbeitung", "Hohe Motorleistung bzw. neidrigeres Max.Drehzahl", "Hocheffizientes ÖLfilter und Ölkühlungsystem", "Ausgereifte Hydrauliktechnik", "Hohe Abgasnorm Standards", "Super Bediener Ergonomie", "Hohe Bediener Sicherheit", "Großes Anwendungsspektrum", "Starke Gesamtsystem Integrität ", "TT als Komplettlieferant für Bohrwerkzeuge und Zubehör"]

    startItem = 3
    produktititaetEnd = 14
    downTimeEnd = 24
    variabelKostenEnd = 33
    erhoeteEinsatzEnd = 46
    widerVerkaufswertEnd = 56

    # Produktivität 
    for i in range(startItem, produktititaetEnd+startItem):
        if result1[i] != result2[i]:
            diff = int(result1[i])-int(result2[i])
            currentItem = [Captions[i-startItem], int(result1[i]), int(result2[i]), diff]
            ComparisonResultsProd.append(currentItem)

    # DownTime 
    for i in range(produktititaetEnd+startItem, downTimeEnd+startItem):
        if result1[i] != result2[i]:
            diff = int(result1[i])-int(result2[i])
            currentItem = [Captions[i-startItem], int(result1[i]), int(result2[i]), diff]
            ComparisonResultsDownTime.append(currentItem)

    # Variabelkosten 
    for i in range(downTimeEnd+startItem, variabelKostenEnd+startItem):
        if result1[i] != result2[i]:
            diff = int(result1[i])-int(result2[i])
            currentItem = [Captions[i-startItem], int(result1[i]), int(result2[i]), diff]
            ComparisonResultsVarCost.append(currentItem)

    # Erhöhte Einsatz 
    for i in range(variabelKostenEnd+startItem, erhoeteEinsatzEnd+startItem):
        if result1[i] != result2[i]:
            diff = int(result1[i])-int(result2[i])
            currentItem = [Captions[i-startItem], int(result1[i]), int(result2[i]), diff]
            ComparisonResultsEinsatz.append(currentItem)

    # WiderverkaufswertEnd 
    for i in range(erhoeteEinsatzEnd+startItem, widerVerkaufswertEnd+startItem):
        if result1[i] != result2[i]:
            diff = int(result1[i])-int(result2[i])
            currentItem = [Captions[i-startItem], int(result1[i]), int(result2[i]), diff]
            ComparisonResultsWiderverkauf.append(currentItem)

    Vergleiche = {
        "Produktivitaet":ComparisonResultsProd,
        "Downtime": ComparisonResultsDownTime,
        "VariableKosten": ComparisonResultsVarCost,
        "ErhoeterEinsatz": ComparisonResultsEinsatz,
        "Wiederverkaufswert": ComparisonResultsWiderverkauf
    }

    return Vergleiche


def compareMaschines2(pDB, pID1, pID2, pKategorien, pLanguage):
    result1 = db.getMaschine(pDB, pID1)
    result2 = db.getMaschine(pDB, pID2)

    merkmale = db.getMerkmale(pDB)

    CategoryKeys = list(pKategorien.keys())
    CategoryNames = list(pKategorien.values())
    
    Vergleiche = dict()

    # Count Categories 
    for currentCategoryKey in CategoryKeys:
        
        # Select all Data for this Category
        Vergleiche[currentCategoryKey] = dict()
        Vergleiche[currentCategoryKey]["names"] = list()
        Vergleiche[currentCategoryKey]["values"] = list()
        Vergleiche[currentCategoryKey]["einheiten"] = list()
        for i in range(50):
            currentKey = f"{currentCategoryKey}_{i}"
            if currentKey in result1.keys():
                Value1 = result1[currentKey]
                Value2 = result2[currentKey]
                if not(Value1 == Value2):
                    if not(Value1 == None or Value2 == None):
                        Difference = Value1 - Value2
                    else:
                        Difference = None
                    
                    Values = [Value1, Value2, Difference]
                    MerkmalName = next((item for item in merkmale if item["merkmalKey"] == currentKey), None)
                    if MerkmalName == None:
                        raise(ValueError, "Key not found in Merkmale DB")
                    
                    Vergleiche[currentCategoryKey]["names"].append(MerkmalName[pLanguage])
                    Vergleiche[currentCategoryKey]["values"].append(Values)
                    Vergleiche[currentCategoryKey]["einheiten"].append(MerkmalName["einheit"])
        

    # Vergleiche = {
    #     "Kategorie1": {
    #         "names" = [
    #             "Name in richtiger Sprache 1",
    #             "Name in richtiger Sprache 1",
    #             ...
    #         ]
    #         "values" = [
    #             [Wert1Maschine1, Wert1Maschine2, Unterschied1],
    #             [Wert2Maschine1, Wert2Maschine2, Unterschied2],
    #             ...
    #         ]
    #     }
    # }

    return Vergleiche
