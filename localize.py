import json

def text(pKey, pLanguage):
    
    with open("translations.json") as json_file:
        contentDict = json.load(json_file)

        if not(pLanguage in contentDict):
            print(f"Language {pLanguage} does not exist")

        else:
            if not(pKey in contentDict[pLanguage]):
                print(f"No Identifier {pKey} in {pLanguage} is defined")
            
            else:
                return(contentDict[pLanguage][pKey])


def getListOfLangages():
    with open("translations.json") as json_file:
        contentDict = json.load(json_file)
        return list(contentDict.keys())

