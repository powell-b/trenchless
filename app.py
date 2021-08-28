
import streamlit as st
import dbAccess as db
import calc
import pandas as pd
import localize as l


mysqlDB = db.connectToDb()
listOfPasswords = db.getPasswords(mysqlDB)

st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');
                button, label, h2, h3, h4, h1 {
                    font-family: 'Open Sans', sans-serif !important;
                }
                h3 {
                    font-weight:600 !important;
                }
                div.stDataFrame > div > div > div > div > div > div {
                    font-family: 'Open Sans', sans-serif !important;
                    color: #000 !important;
                }
                div.stDataFrame > div > div > div > div > div {
                    font-family: 'Open Sans', sans-serif !important;
                }
            <style>
            """, unsafe_allow_html=True)

def seperateNameAndCompany(pString):
    ListFirmaAndName = pString.split(":")
    Firma = ListFirmaAndName[0]
    Name = ListFirmaAndName[1][1:]
    return Firma, Name

sprache = st.sidebar.selectbox("Sprache/Language/...", l.getListOfLangages())
password = st.sidebar.text_input(f"{l.text('password', sprache)}", type="password")

# Find Start Merkmale for each Category


if password in listOfPasswords:
    # Define Stundensatz Constants 
    Zinsen = 0.04
    FinanJahren = 7

    TTBedienerGehalt = 80000
    TTAnzahlbediener = 2
    TTVerwaltungsKosten = 100000
    TTHaftPflichtVersicherung = 25000
    TTWartungBohranlage = 8000
    TTReparaturBohranlage = 6000
    TTErsatzteilBohranlage = 25000
    TTSonstigeKosten = 15000

    BedienerGehalt = 80000
    Anzahlbediener = 2
    VerwaltungsKosten = 100000
    HaftPflichtVersicherung = 25000
    WartungBohranlage = 8000
    ReparaturBohranlage = 6000
    ErsatzteilBohranlage = 25000
    SonstigeKosten = 15000

    # Define Baustellen Kosten Constants

    Kategorien = {
        "PROD": "Produktivität",
        "DOWN": "Weniger Downtime",
        "KOSTEN": "Kosten reduzieren",
        "EINSATZ": "Erhöhte Einsatzmöglichkeiten",
        "VERKAUF": "Wiederverkaufswert steigern"
    }


    # Make constants Dictonary
    constants = {
        "Zinsen": Zinsen,
        "FinanJahren": FinanJahren,
        "BedienerGehalt":BedienerGehalt,
        "Anzahlbediener": Anzahlbediener,
        "VerwaltungsKosten": VerwaltungsKosten,
        "HaftPflichtVersicherung": HaftPflichtVersicherung,
        "WartungBohranlage": WartungBohranlage,
        "ReparaturBohranlage": ReparaturBohranlage,
        "ErsatzteilBohranlage": ErsatzteilBohranlage,
        "SonstigeKosten": SonstigeKosten,
        #"TotalFixKost": TotalFixKost,

        "TTZinsen": Zinsen,
        "TTFinanJahren": FinanJahren,
        "TTBedienerGehalt":BedienerGehalt,
        "TTAnzahlbediener": Anzahlbediener,
        "TTVerwaltungsKosten": VerwaltungsKosten,
        "TTHaftPflichtVersicherung": HaftPflichtVersicherung,
        "TTWartungBohranlage": WartungBohranlage,
        "TTReparaturBohranlage": ReparaturBohranlage,
        "TTErsatzteilBohranlage": ErsatzteilBohranlage,
        "TTSonstigeKosten": SonstigeKosten

    }

    # Create Sliders
    #value1 = st.slider("Value1", 1, 10)
    #value2 = st.slider("Value2", 1, 10)

    st.sidebar.markdown(f"### {l.text('inputs', sprache)}")

    # Maschine Select Box
    ListOfTTMaschines = [ "TRACTO: 130ACS", "TRACTO: 15XPT", "TRACTO: 18N"]
    CompareList130ACS = ["Ditch Witch: JT30AT", "AT BoreTec: MT15 RockDrill"]
    CompareList15XPT = ["Vermeer: D40x55 S3", "Ditch Witch: JT30"]
    CompareList18N = ["Vermeer: D40x55 S3", "Ditch Witch: JT40"]

    Maschine1Select = st.sidebar.selectbox("TRACTO", ListOfTTMaschines)

    if Maschine1Select == ListOfTTMaschines[0]:
        Maschine2Select = st.sidebar.selectbox("Maschine 2", CompareList130ACS)
    elif Maschine1Select == ListOfTTMaschines[1]:
        Maschine2Select = st.sidebar.selectbox("Maschine 2", CompareList15XPT)
    elif Maschine1Select == ListOfTTMaschines[2]:
        Maschine2Select = st.sidebar.selectbox("Maschine 2", CompareList18N)

    # Streamlit Display

    st.sidebar.markdown(f"### {l.text('gesamtInvest', sprache)}")
    gesamtInvestitionSlider1 = st.sidebar.slider(Maschine1Select+"   [in €]", 200000,800000, step=1000)
    gesamtInvestitionSlider2 = st.sidebar.slider(Maschine2Select+"   [in €]", 200000,800000)
    gesamtInvestitionUnterschied = ((gesamtInvestitionSlider2 - gesamtInvestitionSlider1)/gesamtInvestitionSlider1)*100

    st.sidebar.markdown(f"### {l.text('InstandhaltungundErsatzteilKostenimJahr', sprache)}")
    gesamtInstandhaltungSlider1 = st.sidebar.slider(Maschine1Select+"   [in €]", 10000,50000, step=1000)
    gesamtInstandhaltungSlider2 = st.sidebar.slider(Maschine2Select+"   [in €]", 10000,50000)
    gesamtInstandhaltungUnterschied = ((gesamtInstandhaltungSlider2 - gesamtInstandhaltungSlider1)/gesamtInstandhaltungSlider1)*100

    st.sidebar.markdown(f"### {l.text('BaustelleGesamtzeit',sprache)}")
    baustellenGesamtzeitSlider1 = st.sidebar.slider(Maschine1Select+"  [in h]", 5.0,25.0, step=0.5)
    baustellenGesamtzeitSlider2 = st.sidebar.slider(Maschine2Select+"  [in h]", 5.0,25.0, step=0.5)
    gesamtBaustellenZeitUnterschied = ((baustellenGesamtzeitSlider2 - baustellenGesamtzeitSlider1)/baustellenGesamtzeitSlider2)*100

    st.sidebar.markdown(f"### {l.text('LaengederBohrung',sprache)}")
    LaengeBohrungSlider = st.sidebar.slider(Maschine1Select+Maschine2Select+"  [in m]", 10,250, step=1)
    LaengeBohrungSliderUnterschied = ((LaengeBohrungSlider - LaengeBohrungSlider )/LaengeBohrungSlider)*100


    st.sidebar.markdown(f"### {l.text('BaustelleGesamtvariabelkosten',sprache)}")
    baustellenVariabelKostenSlider1 = st.sidebar.slider(Maschine1Select+"  [in €]", 500,10000, step=50)
    baustellenVariabelKostenSlider2 = st.sidebar.slider(Maschine2Select+"  [in €]", 500,10000, step=50)
    gesamtVariabelKostUnterschied = ((baustellenVariabelKostenSlider2 - baustellenVariabelKostenSlider1)/baustellenVariabelKostenSlider2)*100

    st.sidebar.markdown(f"### {l.text('PreisproMeter',sprache)}")
    preisProMeterSlider = st.sidebar.slider(Maschine1Select+Maschine2Select+"  [in €/m]", 10,200, step=1)
    gesamtPreisMeterUnterschied = ((preisProMeterSlider - preisProMeterSlider )/preisProMeterSlider)*100

    st.sidebar.markdown(f"### {l.text('GesamtBohrstundenimJahr',sprache)}")
    bohrstundenProJahrSlider1 = st.sidebar.slider(Maschine1Select+" [in h]", 500,8000, step=10)
    bohrstundenProJahrSlider2 = st.sidebar.slider(Maschine2Select+" [in h]", 500,8000, step=10)
    gesamtbohrstundenUnterschied = ((bohrstundenProJahrSlider2 - bohrstundenProJahrSlider1)/bohrstundenProJahrSlider2)*100

    st.sidebar.markdown(f"### {l.text('MaschinenRestwert',sprache)}")
    maschinenRestWertSlider1 = st.sidebar.slider(Maschine1Select+" [in %]", 5,50)
    maschinenRestWertSlider2 = st.sidebar.slider(Maschine2Select+" [in %]", 5,50)
    gesamtRestWertUnterschied = ((maschinenRestWertSlider2 - maschinenRestWertSlider1)/maschinenRestWertSlider1)*100



    # Eingabe Übersicht
    dataDict = {
        Maschine1Select:[
            gesamtInvestitionSlider1,gesamtInstandhaltungSlider1, baustellenGesamtzeitSlider1, LaengeBohrungSlider, baustellenVariabelKostenSlider1, preisProMeterSlider, bohrstundenProJahrSlider1, maschinenRestWertSlider1], 
        Maschine2Select:[
            gesamtInvestitionSlider2, gesamtInstandhaltungSlider2, baustellenGesamtzeitSlider2, LaengeBohrungSlider, baustellenVariabelKostenSlider2,preisProMeterSlider, bohrstundenProJahrSlider2, maschinenRestWertSlider2], 
        f"{l.text('PercentUnterschied',sprache)}": [
            gesamtInvestitionUnterschied, gesamtInstandhaltungUnterschied, gesamtBaustellenZeitUnterschied, LaengeBohrungSliderUnterschied, gesamtVariabelKostUnterschied, gesamtPreisMeterUnterschied, gesamtbohrstundenUnterschied, gesamtRestWertUnterschied]
        }
    classes = [
        f"{l.text('gesamtInvest', sprache)}",
        f"{l.text('InstandhaltungundErsatzteilKostenimJahr', sprache)}",
        f"{l.text('Baustellengesamtzeit', sprache)}",
        f"{l.text('LaengederBohrung', sprache)}",
        f"{l.text('Baustellenvariabelkosten', sprache)}",
        f"{l.text('PreisproMeter', sprache)}",
        f"{l.text('BohrstundenproJahr', sprache)}",
        f"{l.text('Maschinenrestwert', sprache)}"
        ]
    Data = pd.DataFrame(data=dataDict, index=classes)
    st.markdown(f"### {l.text('EingabeUebersicht',sprache)}")
    st.write(Data.style.format("{:,.1f}"))


    # Make Slider Dicts
    sliderValuesMaschine1 = {
        "gesamtInvestitionSlider": gesamtInvestitionSlider1,
        "gesamtInstandhaltungSlider": gesamtInstandhaltungSlider1,
        "baustellenGesamtzeitSlider": baustellenGesamtzeitSlider1,
        "baustellenVariabelKostenSlider": baustellenVariabelKostenSlider1,
        "bohrstundenProJahrSlider": bohrstundenProJahrSlider1,
        "maschinenRestWertSlider": maschinenRestWertSlider1,
        "preisProMeterSlider": preisProMeterSlider,
        "LaengeBohrungSlider": LaengeBohrungSlider
    }

    sliderValuesMaschine2 = {
        "gesamtInvestitionSlider": gesamtInvestitionSlider2,
        "gesamtInstandhaltungSlider": gesamtInstandhaltungSlider2,
        "baustellenGesamtzeitSlider": baustellenGesamtzeitSlider2,
        "baustellenVariabelKostenSlider": baustellenVariabelKostenSlider2,
        "bohrstundenProJahrSlider": bohrstundenProJahrSlider2,
        "maschinenRestWertSlider": maschinenRestWertSlider2,
        "preisProMeterSlider": preisProMeterSlider,
        "LaengeBohrungSlider": LaengeBohrungSlider
    }


    if st.button("TCO & ROI"+ "  " + Maschine1Select +  "  " + "vs" + "  "  + Maschine2Select):
        ergebnisseMaschine1 = calc.mainCalculations(sliderValuesMaschine1, constants)
        ergebnisseMaschine2 = calc.mainCalculations(sliderValuesMaschine2, constants)

        # TCO Chart 
        dataTC0Chart = [[ergebnisseMaschine1["GemeinkostenFinanzjahre"], ergebnisseMaschine1["InstadhaltungskostenFinanzjahre"], ergebnisseMaschine1["VariableBohrungskostenFinanzjahre"]], [ergebnisseMaschine2["GemeinkostenFinanzjahre"], ergebnisseMaschine2["InstadhaltungskostenFinanzjahre"], ergebnisseMaschine2["VariableBohrungskostenFinanzjahre"]]]
        indexTCOChart = [Maschine1Select, Maschine2Select]
        columnsTCOChart = [f"{l.text('Gemeinkosten',sprache)}", f"{l.text('Instandhaltungskosten',sprache)}", f"{l.text('VariabelBohrungskosten',sprache)}"]
        dfTCO =  pd.DataFrame(dataTC0Chart, indexTCOChart, columnsTCOChart)
        st.markdown(f"### {l.text('TotalCostofOwnershipBreakdown', sprache)}")
        st.write(dfTCO.style.format("{:,.0f}"))
        st.bar_chart(dfTCO)

        # Kum Gewinn Chart
        dataKumGewinnChartTransposed = [ergebnisseMaschine1["KumGewinn"], ergebnisseMaschine2["KumGewinn"]]
        dataKumGewinnChart = [*zip(*dataKumGewinnChartTransposed)]
        indexKumGewinnChart = [i for i in range(1, ergebnisseMaschine1["FinanzJahre"]+1)]
        columnsKumGewinnChart = [f"{Maschine1Select} {l.text('Gewinn',sprache)}", f"{Maschine2Select} {l.text('Gewinn',sprache)}"]
        dfKumGewinn =  pd.DataFrame(dataKumGewinnChart, indexKumGewinnChart, columnsKumGewinnChart)
        st.markdown(f"### {l.text('KummulierteGewinn',sprache)}")
        #st.write(dfKumGewinn.round(0))
        st.write(dfKumGewinn.style.format("{:,.0f}"))

        axKumGewinn = dfKumGewinn.plot.bar(stacked=False, rot=0)
        st.pyplot(axKumGewinn.figure)


        # KPI Tabelle 
        dataKPI = [[ergebnisseMaschine1["Basisstundensatz"], ergebnisseMaschine1["TCO"], ergebnisseMaschine1["ROI"]], [ergebnisseMaschine2["Basisstundensatz"], ergebnisseMaschine2["TCO"], ergebnisseMaschine2["ROI"]]]
        indexKPI = [Maschine1Select, Maschine2Select]
        columnsKPI = [f"{l.text('BasisStundensatzinEuro', sprache)}", f"{l.text('TCOinEuro', sprache)}", f"{l.text('ROIinPercent', sprache)}"]
        dfKPI =  pd.DataFrame(dataKPI, indexKPI, columnsKPI)
        st.markdown(f"### {l.text('KeyPerformanceIndicators',sprache)}")
        #st.write(dfKPI.round (0))
        st.write(dfKPI.style.format("{:,.0f}"))


    if st.button(f"{l.text('Merkmalvergleich',sprache)} {Maschine1Select} vs {Maschine2Select}"):

        # Kategorien = {
        #   "Key1": "Name1 in Exel to separate",
        #   "Key2": "Name2 in Exel to separate",    
        # }
        Kategorien = {
            "PROD": "Produktivität",
            "DOWN": "Weniger Downtime",
            "KOSTEN": "Kosten reduzieren",
            "EINSATZ": "Erhöhte Einsatzmöglichkeiten",
            "VERKAUF": "Wiederverkaufswert steigern"
        }
        # Create Database 
        theDatabase = db.connectToDb()
        FirmaMaschine1, NameMaschine1 = seperateNameAndCompany(Maschine1Select)
        FirmaMaschine2, NameMaschine2 = seperateNameAndCompany(Maschine2Select)
        idMaschine1 = db.getIdOfMaschine(theDatabase, FirmaMaschine1, NameMaschine1)
        idMaschine2 = db.getIdOfMaschine(theDatabase, FirmaMaschine2, NameMaschine2)
        result = calc.compareMaschines2(theDatabase, idMaschine1, idMaschine2, Kategorien, sprache)
        columsCompareDf = [
            #f"{l.text('Merkmal',sprache)}", 
            #f"{l.text('Einheit',sprache)}", 
            Maschine1Select, 
            Maschine2Select, 
            f"{l.text('Unterschied',sprache)}"
        ]

        for KategoryKey in Kategorien:
            st.markdown(f"### {l.text(KategoryKey,sprache)}")
            st.markdown(f"*{l.text('RatingText',sprache)}*")
            st.write(
                pd.DataFrame(
                    data=result[KategoryKey]["values"],
                    columns=columsCompareDf,
                    index = [f"{result[KategoryKey]['names'][i]} [{result[KategoryKey]['einheiten'][i]}]" for i in range(len(result[KategoryKey]["names"]))]
                )
            )

    # if st.button("Update DB from Exel"):
    #     exelFile = st.secrets["excelFile"]
    #     Kategorien = {
    #         "PROD": "Produktivität",
    #         "DOWN": "Weniger Downtime",
    #         "KOSTEN": "Kosten reduzieren",
    #         "EINSATZ": "Erhöhte Einsatzmöglichkeiten",
    #         "VERKAUF": "Wiederverkaufswert steigern"
    #     }
    #     db.updateDBFromExcel2(db.connectToDb(),exelFile, Kategorien)

else: 
    st.write(f"{l.text('PasswortEingeben',sprache)}")