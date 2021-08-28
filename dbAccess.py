import mysql.connector
import streamlit as st


def connectToDb():
    mydb = mysql.connector.connect(
        host= st.secrets["db_host"], #127.0.0.1
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        database=st.secrets["db_name"]
    )
    return mydb 

# def customConnectToDb(pHost, pUser, pPassword, pName):
#    mydb = mysql.connector.connect(
#         host = pHost, #127.0.0.1
#         user = pUser,
#         password = pPassword,
#         database = pName
#     )
#     return mydb

def getPasswords(pMydb):
    cursor = pMydb.cursor()
    sqlQuery = "SELECT password FROM Passwords"
    cursor.execute(sqlQuery)
    listOfPasswords = cursor.fetchall()
    listOfPasswords = [i[0] for i in listOfPasswords]
    return listOfPasswords

def updateDBFromExcel(pMydb, pFile):
    cursor = pMydb.cursor()

    import xlrd
    wb = xlrd.open_workbook(pFile)
    sheet = wb.sheet_by_name("Database")
    
    
    startRow = 7        # starts at row 0
    currentCol = 3      # starts at col 0
    
    # Inizialize Counters
    countMaschineAdded = 0
    countMaschineUpdated = 0

    while True:
        try:
            sheet.cell_value(startRow, currentCol) 
        except IndexError:
            # Exit the while loop 
            break 

        Firma  = sheet.cell_value(startRow - 4, currentCol-1) 
        Maschine  = sheet.cell_value(startRow - 3, currentCol-1) 
        PROD_MaxDrehMom  = sheet.cell_value(startRow, currentCol) 
        PROD_MaxZugkraft  = sheet.cell_value(startRow + 1, currentCol) 
        PROD_VorshubGeschw  = sheet.cell_value(startRow + 2, currentCol) 
        PROD_SpueLeist  = sheet.cell_value(startRow + 3, currentCol) 
        PROD_GestaengLaenge  = sheet.cell_value(startRow + 4, currentCol) 
        PROD_GestaengWech  = sheet.cell_value(startRow + 5, currentCol) 
        PROD_TurboLeist  = sheet.cell_value(startRow + 6, currentCol) 
        PROD_Bohrauto  = sheet.cell_value(startRow + 7, currentCol) 
        PROD_Ergo  = sheet.cell_value(startRow + 8, currentCol) 
        PROD_DruckEntlas  = sheet.cell_value(startRow + 9, currentCol) 
        PROD_AufAbbau  = sheet.cell_value(startRow + 10, currentCol) 
        PROD_Sicherheit  = sheet.cell_value(startRow + 11, currentCol) 
        PROD_Fahrbar  = sheet.cell_value(startRow + 12, currentCol) 
        PROD_QuickCon  = sheet.cell_value(startRow + 13, currentCol) 
        # PROD_Test = 
        NODOWN_FehlMeld  = sheet.cell_value(startRow + 17, currentCol) 
        NODOWN_NotHyd  = sheet.cell_value(startRow + 18, currentCol) 
        NODOWN_FernDiag  = sheet.cell_value(startRow + 19, currentCol) 
        NODOWN_Dokus  = sheet.cell_value(startRow + 20, currentCol) 
        NODOWN_SoftUp  = sheet.cell_value(startRow + 21, currentCol) 
        NODOWN_WFreund  = sheet.cell_value(startRow + 22, currentCol) 
        NODOWN_ManBohr  = sheet.cell_value(startRow + 23, currentCol) 
        NODOWN_TeilBest  = sheet.cell_value(startRow + 24, currentCol) 
        NODOWN_PlanSoft  = sheet.cell_value(startRow + 25, currentCol) 
        NODOWN_KabKom  = sheet.cell_value(startRow + 26, currentCol) 
        VARKOST_MoAnpass  = sheet.cell_value(startRow + 31, currentCol) 
        VARKOST_NiedMot  = sheet.cell_value(startRow + 32, currentCol) 
        VARKOST_MoPuTec  = sheet.cell_value(startRow + 33, currentCol) 
        VARKOST_DatAuf  = sheet.cell_value(startRow + 34, currentCol) 
        VARKOST_GestKlem  = sheet.cell_value(startRow + 35, currentCol) 
        VARKOST_AnkFest  = sheet.cell_value(startRow + 36, currentCol) 
        VARKOST_MischLei  = sheet.cell_value(startRow + 37, currentCol) 
        VARKOST_DruRein  = sheet.cell_value(startRow + 38, currentCol) 
        VARKOST_BohrAusw  = sheet.cell_value(startRow + 39, currentCol) 
        EINSATZ_MascAb  = sheet.cell_value(startRow + 45, currentCol) 
        EINSATZ_FlaeLeist  = sheet.cell_value(startRow + 46, currentCol) 
        EINSATZ_LafNeig  = sheet.cell_value(startRow + 47, currentCol) 
        EINSATZ_BoxAus  = sheet.cell_value(startRow + 48, currentCol) 
        EINSATZ_GesTyp  = sheet.cell_value(startRow + 49, currentCol) 
        EINSATZ_EInGestae  = sheet.cell_value(startRow + 50, currentCol) 
        EINSATZ_DivVerank  = sheet.cell_value(startRow + 51, currentCol) 
        EINSATZ_DivGestein  = sheet.cell_value(startRow + 52, currentCol) 
        EINSATZ_FahrSchon  = sheet.cell_value(startRow + 53, currentCol) 
        EINSATZ_Oesen  = sheet.cell_value(startRow + 54, currentCol) 
        EINSATZ_KabelBor  = sheet.cell_value(startRow + 55, currentCol) 
        EINSATZ_ZugMess  = sheet.cell_value(startRow + 56, currentCol) 
        EINSATZ_Beleucht  = sheet.cell_value(startRow + 57, currentCol) 
        WVERK_Design  = sheet.cell_value(startRow + 63, currentCol) 
        WVERK_HoheMot  = sheet.cell_value(startRow + 64, currentCol) 
        WVERK_OelSyst  = sheet.cell_value(startRow + 65, currentCol) 
        WVERK_HydTec  = sheet.cell_value(startRow + 66, currentCol) 
        WVERK_Abgas  = sheet.cell_value(startRow + 67, currentCol) 
        WVERK_Ergo  = sheet.cell_value(startRow + 68, currentCol) 
        WVERK_Sicher  = sheet.cell_value(startRow + 69, currentCol) 
        WVERK_Anwend  = sheet.cell_value(startRow + 70, currentCol) 
        WVERK_GesSyst  = sheet.cell_value(startRow + 71, currentCol) 
        WVERK_KomplettBW  = sheet.cell_value(startRow + 72, currentCol) 
        
        sqlCountQuery = "SELECT `ID` FROM MaschinenDaten WHERE Firma=%s AND Maschine=%s"
        valCount = (Firma, Maschine)
        cursor.execute(sqlCountQuery, valCount)
        CountResults = cursor.fetchall()
    
        if len(CountResults)==0:
            # Add new Maschine 
            sql = "INSERT INTO `MaschinenDaten`(`Firma`,`Maschine`,`PROD_MaxDrehMom`,`PROD_MaxZugkraft`,`PROD_VorshubGeschw`,`PROD_SpueLeist`,`PROD_GestaengLaenge`,`PROD_GestaengWech`,`PROD_TurboLeist`,`PROD_Bohrauto`,`PROD_Ergo`,`PROD_DruckEntlas`,`PROD_AufAbbau`,`PROD_Sicherheit`,`PROD_Fahrbar`,`PROD_QuickCon`, `NODOWN_FehlMeld`,`NODOWN_NotHyd`,`NODOWN_FernDiag`,`NODOWN_Dokus`,`NODOWN_SoftUp`,`NODOWN_WFreund`,`NODOWN_ManBohr`,`NODOWN_TeilBest`,`NODOWN_PlanSoft`,`NODOWN_KabKom`,`VARKOST_MoAnpass`,`VARKOST_NiedMot`,`VARKOST_MoPuTec`,`VARKOST_DatAuf`,`VARKOST_GestKlem`,`VARKOST_AnkFest`,`VARKOST_MischLei`,`VARKOST_DruRein`,`VARKOST_BohrAusw`,`EINSATZ_MascAb`,`EINSATZ_FlaeLeist`,`EINSATZ_LafNeig`,`EINSATZ_BoxAus`,`EINSATZ_GesTyp`,`EINSATZ_EInGestae`,`EINSATZ_DivVerank`,`EINSATZ_DivGestein`,`EINSATZ_FahrSchon`,`EINSATZ_Oesen`,`EINSATZ_KabelBor`,`EINSATZ_ZugMess`,`EINSATZ_Beleucht`,`WVERK_Design`,`WVERK_HoheMot`,`WVERK_OelSyst`,`WVERK_HydTec`,`WVERK_Abgas`,`WVERK_Ergo`,`WVERK_Sicher`,`WVERK_Anwend`,`WVERK_GesSyst`,`WVERK_KomplettBW`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Firma, Maschine, PROD_MaxDrehMom, PROD_MaxZugkraft, PROD_VorshubGeschw, PROD_SpueLeist, PROD_GestaengLaenge, PROD_GestaengWech, PROD_TurboLeist, PROD_Bohrauto, PROD_Ergo, PROD_DruckEntlas, PROD_AufAbbau, PROD_Sicherheit, PROD_Fahrbar, PROD_QuickCon, NODOWN_FehlMeld, NODOWN_NotHyd, NODOWN_FernDiag, NODOWN_Dokus, NODOWN_SoftUp, NODOWN_WFreund, NODOWN_ManBohr, NODOWN_TeilBest, NODOWN_PlanSoft, NODOWN_KabKom, VARKOST_MoAnpass, VARKOST_NiedMot, VARKOST_MoPuTec, VARKOST_DatAuf, VARKOST_GestKlem, VARKOST_AnkFest, VARKOST_MischLei, VARKOST_DruRein, VARKOST_BohrAusw, EINSATZ_MascAb, EINSATZ_FlaeLeist, EINSATZ_LafNeig, EINSATZ_BoxAus, EINSATZ_GesTyp, EINSATZ_EInGestae, EINSATZ_DivVerank, EINSATZ_DivGestein, EINSATZ_FahrSchon, EINSATZ_Oesen, EINSATZ_KabelBor, EINSATZ_ZugMess, EINSATZ_Beleucht, WVERK_Design, WVERK_HoheMot, WVERK_OelSyst, WVERK_HydTec, WVERK_Abgas, WVERK_Ergo, WVERK_Sicher, WVERK_Anwend, WVERK_GesSyst, WVERK_KomplettBW)

            countMaschineAdded += 1
        else:
            # Update existing Maschine
            MaschineID = CountResults[0][0]
            sql = "UPDATE `MaschinenDaten` SET `Firma`=%s,`Maschine`=%s,`PROD_MaxDrehMom`=%s,`PROD_MaxZugkraft`=%s,`PROD_VorshubGeschw`=%s,`PROD_SpueLeist`=%s,`PROD_GestaengLaenge`=%s,`PROD_GestaengWech`=%s,`PROD_TurboLeist`=%s,`PROD_Bohrauto`=%s,`PROD_Ergo`=%s,`PROD_DruckEntlas`=%s,`PROD_AufAbbau`=%s,`PROD_Sicherheit`=%s,`PROD_Fahrbar`=%s,`PROD_QuickCon`=%s,`NODOWN_FehlMeld`=%s,`NODOWN_NotHyd`=%s,`NODOWN_FernDiag`=%s,`NODOWN_Dokus`=%s,`NODOWN_SoftUp`=%s,`NODOWN_WFreund`=%s,`NODOWN_ManBohr`=%s,`NODOWN_TeilBest`=%s,`NODOWN_PlanSoft`=%s,`NODOWN_KabKom`=%s,`VARKOST_MoAnpass`=%s,`VARKOST_NiedMot`=%s,`VARKOST_MoPuTec`=%s,`VARKOST_DatAuf`=%s,`VARKOST_GestKlem`=%s,`VARKOST_AnkFest`=%s,`VARKOST_MischLei`=%s,`VARKOST_DruRein`=%s,`VARKOST_BohrAusw`=%s,`EINSATZ_MascAb`=%s,`EINSATZ_FlaeLeist`=%s,`EINSATZ_LafNeig`=%s,`EINSATZ_BoxAus`=%s,`EINSATZ_GesTyp`=%s,`EINSATZ_EInGestae`=%s,`EINSATZ_DivVerank`=%s,`EINSATZ_DivGestein`=%s,`EINSATZ_FahrSchon`=%s,`EINSATZ_Oesen`=%s,`EINSATZ_KabelBor`=%s,`EINSATZ_ZugMess`=%s,`EINSATZ_Beleucht`=%s,`WVERK_Design`=%s,`WVERK_HoheMot`=%s,`WVERK_OelSyst`=%s,`WVERK_HydTec`=%s,`WVERK_Abgas`=%s,`WVERK_Ergo`=%s,`WVERK_Sicher`=%s,`WVERK_Anwend`=%s,`WVERK_GesSyst`=%s,`WVERK_KomplettBW`=%s WHERE `ID`=%s"
            val = (Firma, Maschine, PROD_MaxDrehMom, PROD_MaxZugkraft, PROD_VorshubGeschw, PROD_SpueLeist, PROD_GestaengLaenge, PROD_GestaengWech, PROD_TurboLeist, PROD_Bohrauto, PROD_Ergo, PROD_DruckEntlas, PROD_AufAbbau, PROD_Sicherheit, PROD_Fahrbar, PROD_QuickCon, NODOWN_FehlMeld, NODOWN_NotHyd, NODOWN_FernDiag, NODOWN_Dokus, NODOWN_SoftUp, NODOWN_WFreund, NODOWN_ManBohr, NODOWN_TeilBest, NODOWN_PlanSoft, NODOWN_KabKom, VARKOST_MoAnpass, VARKOST_NiedMot, VARKOST_MoPuTec, VARKOST_DatAuf, VARKOST_GestKlem, VARKOST_AnkFest, VARKOST_MischLei, VARKOST_DruRein, VARKOST_BohrAusw, EINSATZ_MascAb, EINSATZ_FlaeLeist, EINSATZ_LafNeig, EINSATZ_BoxAus, EINSATZ_GesTyp, EINSATZ_EInGestae, EINSATZ_DivVerank, EINSATZ_DivGestein, EINSATZ_FahrSchon, EINSATZ_Oesen, EINSATZ_KabelBor, EINSATZ_ZugMess, EINSATZ_Beleucht, WVERK_Design, WVERK_HoheMot, WVERK_OelSyst, WVERK_HydTec, WVERK_Abgas, WVERK_Ergo, WVERK_Sicher, WVERK_Anwend, WVERK_GesSyst, WVERK_KomplettBW, MaschineID)
            
            countMaschineUpdated += 1


        # Exceute Query and Commit to DB
        cursor.execute(sql, val)
        pMydb.commit()

        # Go to next maschine 3 cols down
        currentCol = currentCol + 3
    
    return "Sucessfully added {:n} Maschines and updated {:n} Maschines".format(countMaschineAdded, countMaschineUpdated)

def updateDBFromExcel2(pMydb, pFile, pKategorien):
    cursor = pMydb.cursor()

    import xlrd
    wb = xlrd.open_workbook(pFile)
    sheet = wb.sheet_by_name("Database")

    startMerkmaleCategory1 = 8 # Where the Merkmale for Category 1 start (Produktivität)
    colMerkmale = 1
    numberLanguages = 2 # Change this value, when adding or removing languages
    rowLanguages = 6 # Row where language declared  
    colMaschineStart = colMerkmale + numberLanguages + 2

    CategoryKeys = list(pKategorien.keys())
    CategoryNames = list(pKategorien.values())

    # Merkmale = [ [7,8,9...], [36, 37, ...], ...]
    Merkmale = []
    MerkmaleNames = []
    categoryCount = 1
    currentMerkmale = []
    currentMerkmalNames = []
    currentRow = startMerkmaleCategory1

    # Iterate for each Category 
    while True:
        try:
            sheet.cell_value(currentRow, colMerkmale) 
        except IndexError:
            # Store Values
            Merkmale.append(currentMerkmale)
            MerkmaleNames.append(currentMerkmalNames)

            # Exit the while loop, when out of Range 
            break 
        
        currentMerkmalName = sheet.cell_value(currentRow, colMerkmale)
        
        if categoryCount<len(CategoryNames):
            # If we are not in the last Kategorie
            if CategoryNames[categoryCount] == currentMerkmalName: 
                # Store Values
                Merkmale.append(currentMerkmale)
                MerkmaleNames.append(currentMerkmalNames)
                # Clean up for Next Category 
                currentMerkmalNames = []
                currentMerkmale = []
                categoryCount = categoryCount + 1
                currentRow = currentRow + 1
                continue
            
        # Add a new Merkmal to list
        if not(currentMerkmalName == ""):
            # If not Empty 
            currentMerkmale.append(currentRow)
            currentMerkmalNames.append(currentMerkmalName)

        currentRow = currentRow + 1

    # Delete all existing maschines
    query = "DELETE FROM MaschinenDaten2"
    cursor.execute(query)
    # print(f"Deleted all rows")

    # Update DB to contain the right amount of Merkmale
    for i in range(len(CategoryKeys)):
        # Remove all the old 
        for j in range(50):
            currentColName = CategoryKeys[i] + f"_{j}"
            query = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE column_name=%s"
            val = (currentColName, )
            cursor.execute(query, val)
            CountResults = cursor.fetchall()

            if not(len(CountResults) == 0):
                # Drop this column
                query = f"ALTER TABLE `MaschinenDaten2` DROP `{currentColName}`;"
                cursor.execute(query)
                #print(f"Deleted column {currentColName}")

        # Add the new
        for j in range(len(Merkmale[i])):
            currentColName = CategoryKeys[i] + f"_{j}"
            query = f"ALTER TABLE `MaschinenDaten2` ADD `{currentColName}` DOUBLE  NULL ;"
            cursor.execute(query)
            #print(f"Added column {currentColName}")
        
    # Post Merkmale Data to DB
    currentCol = colMaschineStart
    maschinesAdded = 0

    while True:
        try:
            sheet.cell_value(startMerkmaleCategory1, currentCol) 
        except IndexError:
            # Exit the while loop, when out of Range, no more maschines 
            break 
        
        currentFirma = sheet.cell_value(startMerkmaleCategory1-5, currentCol-1) 
        currentName = sheet.cell_value(startMerkmaleCategory1-4, currentCol-1) 

        query = "INSERT INTO `MaschinenDaten2` (`Firma`,`Maschine`) VALUES (%s,%s)"
        vals = (currentFirma, currentName)
        cursor.execute(query, vals)
        pMydb.commit()
        
        # Get the ID for current Maschine 
        sqlCountQuery = "SELECT `ID` FROM MaschinenDaten2 WHERE Firma=%s AND Maschine=%s"
        valCount = (currentFirma, currentName)
        cursor.execute(sqlCountQuery, valCount)
        CountResults = cursor.fetchall()

        if len(CountResults)==0:
            print("Maschine nicht gefunden")
            print(CountResults)
        else:
            currentID = CountResults[0][0]
            # print(f"Maschine gefunden mit ID = {currentID}")
            for i in range(len(CategoryKeys)):
                for j in range(len(Merkmale[i])):
                    currentColName = CategoryKeys[i] + f"_{j}"
                    currentColValue = sheet.cell_value(Merkmale[i][j], currentCol)
                    
                    try:
                        float(currentColValue)
                    except ValueError:
                         currentColValue = "NULL"

                    query = f"UPDATE `MaschinenDaten2` SET `{currentColName}`={currentColValue} WHERE `ID`={currentID}"
                    cursor.execute(query)
                    pMydb.commit()

        maschinesAdded = maschinesAdded + 1 
        currentCol = currentCol + 3

    print(f"Added {maschinesAdded} Maschines")

    

    # Collect Merkmale Names 
    merkmaleDict = dict()
    einheiten = dict()
    Sprachen = []

    for k in range(numberLanguages):
        # Each Language
        currentLanguage = sheet.cell_value(rowLanguages,colMerkmale+k)
        Sprachen.append(currentLanguage)

        merkmaleDict[currentLanguage] = dict()

        for i in range(len(CategoryKeys)):
            # Each Category 
            for j in range(len(Merkmale[i])):
                # Each Merkmal 
                    currentColName = CategoryKeys[i] + f"_{j}"
                    currentMerkmalName = sheet.cell_value(Merkmale[i][j], colMerkmale+k)
                    
                    currentEinheit = sheet.cell_value(Merkmale[i][j], colMerkmale+numberLanguages)
                    einheiten[currentColName] = currentEinheit
                    merkmaleDict[currentLanguage][currentColName] = currentMerkmalName


    # Post Data to Database

    # Delete all
    query = "DELETE FROM `Merkmale`"
    cursor.execute(query)
    pMydb.commit()

    for currentLanguage in Sprachen:
        # Each Language
        # check if Language has a Column in Database
        query = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE column_name=%s"
        val = (currentLanguage, )
        cursor.execute(query, val)
        CountResults = cursor.fetchall()
        
        if len(CountResults) == 0:
            # If not exist then add a new column for language
            query = f"ALTER TABLE `Merkmale` ADD `{currentLanguage}` TEXT NULL ;"
            cursor.execute(query)
            pMydb.commit()
            print(f"Added Column for {currentLanguage}")

    for currentColName in merkmaleDict[Sprachen[0]]:
        # Each Merkmal 
        currentMerkmalName = merkmaleDict[Sprachen[0]][currentColName]
        currentEinheit = einheiten[currentColName]
        queryPart = ""
        queryPartValues = ""
        vals = (currentColName, currentEinheit)
        for Sprache in Sprachen:
            if Sprache == Sprachen[-1]:
                # Last one
                queryPart = queryPart + f"`{Sprache}`"
                queryPartValues = queryPartValues + "%s"
            else: 
                # Not last one
                queryPart = queryPart + f"`{Sprache}`, "
                queryPartValues = queryPartValues + "%s, "
            
            vals = vals + (merkmaleDict[Sprache][currentColName],)


        query = f"INSERT INTO `Merkmale` (`merkmalKey`, `einheit`, {queryPart}) VALUES (%s, %s, {queryPartValues})"
        

        cursor.execute(query, vals)
        pMydb.commit()
    
def getMaschine(pMydb, pID):

    cursor = pMydb.cursor(dictionary=True)
    query = "SELECT * FROM `MaschinenDaten2` WHERE `ID`= %s"
    values = (pID, )
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result[0]

def getIdOfMaschine(pMydb, pFirma, pName):
    cursor = pMydb.cursor()
    query = "SELECT ID FROM `MaschinenDaten2` WHERE `Firma`= %s AND `Maschine`=%s"
    values = (pFirma, pName)
    cursor.execute(query, values)
    result = cursor.fetchall()
    return result[0][0]

def getMerkmale(pMydb):
    cursor = pMydb.cursor(dictionary=True)
    query = "SELECT * FROM `Merkmale`"
    cursor.execute(query)
    result = cursor.fetchall()
    return result