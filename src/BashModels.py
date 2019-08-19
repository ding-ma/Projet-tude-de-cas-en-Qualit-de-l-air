import difflib
import os
import re
import string

import pandas as pd

# Setings used for the entire program, change/ add as needed

# This format is used to bash and rarc scripts
hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031",
    "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

# This format is used to sort the files
hour24 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]

# extra hours if needed to be added
# ,"49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72"
# ,"049","050","051","052","053","054","055","056","057","058","059","060","061","062","063","064","065","066","067","068","069","070","071","072"


#Do not touch the rest!
##################################################

#code to create repos and make sure everything is executable
filelocation = os.getcwd()
directories = ["bash", "config", "rarc", "output", "extracted", "UMOSTreating", "configMIST", "extractedMist", "configFw",
               "extractedFw","imgTemp","output_csv", "output_img", "output_excel"]
for i in directories:
    if not os.path.exists(filelocation+"/"+i):
        os.mkdir(filelocation+"/"+i)
os.system("chmod -R 744 "+ filelocation)
filedirectory = next(os.walk('.'))[1]


stationsDataFrame = pd.read_csv("stations.csv").drop(columns=['city','address'])

lstID = stationsDataFrame['id'].tolist()
lstName = stationsDataFrame['name_en_ CA'].tolist()
lstLatitude = stationsDataFrame['lat'].tolist()
lstLongitude = stationsDataFrame['lon'].tolist()
lstProvince = stationsDataFrame['province'].tolist()
# todo, fix the zip in a way like gemmach file
lstDisplay = stationsDataFrame[['id','name_en_ CA']].values.tolist()


#search algorithm
def findWithStation(station):
    index = isStationFound(string.capwords(station))
    if index is False:
        return "ID not found, invalid station name"
    else:
        #with the index, we can get the other values since all corresponding data are stored at the same index for the same value
        stationID = lstID[index]
        stationLongitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        stationName = lstName[index]
        return stationName + " (" + str(stationID) + ") Lat: " + str(stationLatitude) + " Lon: " + str(stationLongitude)


#returns the index of the item if it exist else, it returns false, gets around the item out of bound problem
def isStationFound(StationInput):
    a = difflib.get_close_matches(StationInput, lstName, n=1, cutoff=.4)
    if len(a) is 0:
        return False
    else:
        return lstName.index(a[0])


#same logic for searching with ID
def findWithID(ID):
    index = isIDFound(ID)
    if index is False:
        return "Station name not found, invalid ID"
    else:
        stationName = lstName[index]
        stationLongtitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        return stationName + " (" + ID + ") Lat: " + stationLatitude + " Lon: " + stationLongtitude


def isIDFound(IDinput):
    if IDinput in lstID:
        return lstID.index(IDinput)
    return False


# returning the found list
def SearchNameID(userInput):
    #ignores all digit
    patten = re.compile('\D')
    #if there are no digit, search by name. else, search with ID
    if patten.findall(userInput):
        return findWithStation(" "+userInput)
    else:
        return findWithID(userInput)

def returnName(ID):
    index = isIDFound(ID)
    if index is False:
        return "Station not in database"
    return lstName[index].strip()


lstNL = stationsDataFrame[stationsDataFrame['province'] ==1].id.tolist()
lstPEI = stationsDataFrame[stationsDataFrame['province'] ==2].id.tolist()
lstNS = stationsDataFrame[stationsDataFrame['province'] ==3].id.tolist()
lstNB = stationsDataFrame[stationsDataFrame['province'] ==4].id.tolist()
lstQC = stationsDataFrame[stationsDataFrame['province'] ==5].id.tolist()
lstONT = stationsDataFrame[stationsDataFrame['province'] ==6].id.tolist()
lstMAN = stationsDataFrame[stationsDataFrame['province'] ==7].id.tolist()
lstSASK = stationsDataFrame[stationsDataFrame['province'] ==8].id.tolist()
lstALB = stationsDataFrame[stationsDataFrame['province'] ==9].id.tolist()
lstBC = stationsDataFrame[stationsDataFrame['province'] ==10].id.tolist()
lstYK = stationsDataFrame[stationsDataFrame['province'] ==11].id.tolist()
lstNWT = stationsDataFrame[stationsDataFrame['province'] ==12].id.tolist()
lstNVT = stationsDataFrame[stationsDataFrame['province'] ==13].id.tolist()

prov = ["Province","AB", "BC", "MB", "NB", 'NL', "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT", "ALL"]
# returns list of all the stations based on the selected province
provinceDic = {
    "Province":"--",
    "AB": lstALB,
    "BC": lstBC,
    "MB": lstMAN,
    "NB": lstNB,
    'NL': lstNL,
    "NS": lstNS,
    "ON": lstONT,
    "PE": lstPEI,
    "QC": lstQC,
    "SK": lstSASK,
    "NT": lstNWT,
    "NU": lstNVT,
    "YT": lstYK,
    "ALL":lstNL+lstPEI+lstNS+lstNB+lstQC+lstONT+lstMAN+lstSASK+lstALB+lstBC+lstYK+lstNWT+lstNVT
}

provlist = []


def gettingprovlist(P):
    if P == "Province":
        return "Station"
    for y in provinceDic[P]:
        indexofitem = lstID.index(y)
        display = lstDisplay[indexofitem][0]
        provlist.append(display)
    return provlist

########


#print(SearchNameID("Crofton Heights"))
a = (stationsDataFrame[stationsDataFrame['id']==129999]).to_string(header=False,index=False)
if stationsDataFrame[stationsDataFrame['id']==145645645646].empty:
    print("ID does not exist")