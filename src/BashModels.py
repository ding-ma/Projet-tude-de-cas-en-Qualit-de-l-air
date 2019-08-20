import collections
import difflib
import itertools as IT
import os
import re
import shutil
import string
import tempfile
from datetime import date, timedelta, datetime

import pandas as pd

# Setings used for the entire program, change/ add as needed

# This format is used to bash and rarc scripts
hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031",
    "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047",
    "048")

# This format is used to sort the files
hour24 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]

# extra hours if needed to be added
# ,"49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72"
# ,"049","050","051","052","053","054","055","056","057","058","059","060","061","062","063","064","065","066","067","068","069","070","071","072"


# Do not touch the rest!
##################################################
filelocation = os.getcwd()

stationsDataFrame = pd.read_csv("stations.csv").drop(axis=1,labels=['city', 'address'])
lstID = stationsDataFrame['id'].tolist()
lstName = stationsDataFrame['name_en_ CA'].tolist()
lstLatitude = stationsDataFrame['lat'].tolist()
lstLongitude = stationsDataFrame['lon'].tolist()
lstProvince = stationsDataFrame['province'].tolist()
# todo, fix the zip in a way like gemmach file
lstDisplay = stationsDataFrame[['id', 'name_en_ CA']].values.tolist()

# search algorithm
def findWithStation(station):
    index = isStationFound(string.capwords(station))
    if index is False:
        return "ID not found, invalid station name"
    else:
        # with the index, we can get the other values since all corresponding data are stored at the same index for the same value
        stationID = lstID[index]
        stationLongitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        stationName = lstName[index]
        return stationName + " (" + str(stationID) + ") Lat: " + str(stationLatitude) + " Lon: " + str(stationLongitude)


# returns the index of the item if it exist else, it returns false, gets around the item out of bound problem
def isStationFound(StationInput):
    a = difflib.get_close_matches(StationInput, lstName, n=1, cutoff=.4)
    if len(a) is 0:
        return False
    else:
        return lstName.index(a[0])


# same logic for searching with ID
def findWithID(ID):
    if len(stationsDataFrame[stationsDataFrame['id'] == ID]) == 0:
        return "Station name not found, invalid ID"
    else:
        df_str = re.findall("\S{5,}",
                            (stationsDataFrame[stationsDataFrame['id'] == ID]).to_string(index=False, header=False))
        return df_str[0] + " (" + df_str[1] + ") Lat: " + df_str[3] + " Lon: " + df_str[4]


def isIDFound(IDinput):
    if IDinput in lstID:
        return lstID.index(IDinput)
    return False


# returning the found list
def SearchNameID(userInput):
    # ignores all digit
    patten = re.compile('\D')
    # if there are no digit, search by name. else, search with ID
    if patten.findall(userInput):
        return findWithStation(" " + userInput)
    else:
        return findWithID(int(userInput))


def returnName(ID):
    index = isIDFound(ID)
    if index is False:
        return "Station not in database"
    return lstName[index].strip()


lstNL = stationsDataFrame[stationsDataFrame['province'] == 1].id.tolist()
lstPEI = stationsDataFrame[stationsDataFrame['province'] == 2].id.tolist()
lstNS = stationsDataFrame[stationsDataFrame['province'] == 3].id.tolist()
lstNB = stationsDataFrame[stationsDataFrame['province'] == 4].id.tolist()
lstQC = stationsDataFrame[stationsDataFrame['province'] == 5].id.tolist()
lstONT = stationsDataFrame[stationsDataFrame['province'] == 6].id.tolist()
lstMAN = stationsDataFrame[stationsDataFrame['province'] == 7].id.tolist()
lstSASK = stationsDataFrame[stationsDataFrame['province'] == 8].id.tolist()
lstALB = stationsDataFrame[stationsDataFrame['province'] == 9].id.tolist()
lstBC = stationsDataFrame[stationsDataFrame['province'] == 10].id.tolist()
lstYK = stationsDataFrame[stationsDataFrame['province'] == 11].id.tolist()
lstNWT = stationsDataFrame[stationsDataFrame['province'] == 12].id.tolist()
lstNVT = stationsDataFrame[stationsDataFrame['province'] == 13].id.tolist()

prov = ["Province", "AB", "BC", "MB", "NB", 'NL', "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT", "ALL"]
# returns list of all the stations based on the selected province
provinceDic = {
    "Province": "--",
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
    "ALL": lstNL + lstPEI + lstNS + lstNB + lstQC + lstONT + lstMAN + lstSASK + lstALB + lstBC + lstYK + lstNWT + lstNVT
}

provlist = []


def gettingprovlist(P):
    if P == "Province":
        return "Station"
    for y in provinceDic[P]:
        indexofitem = lstID.index(y)
        display = str(lstDisplay[indexofitem][0])+": "+lstDisplay[indexofitem][1]
        provlist.append(display)
    return provlist


########
#this is IMPORTANT, otherwise the hashtable will not give this in order
monthDict = collections.OrderedDict()
monthDict['January'] = '01'
monthDict['February'] = '02'
monthDict['March'] = '03'
monthDict['April'] = '04'
monthDict['May'] = '05'
monthDict['June'] = '06'
monthDict['July'] = '07'
monthDict['August'] = '08'
monthDict['September'] = '09'
monthDict['October'] = '10'
monthDict['November'] = '11'
monthDict['December'] = '12'

#formats the start date
def inputStartDate(sD):
    global sYear
    global sMonth
    global sDay
    global sDate
    #splits the entry into a tuple
    unformatattedDate = re.split("/", sD)
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]
    sDate = date(int(sYear),int(sMonth),int(sDay))
    print("Start Date: " + sDate.strftime("%Y %m %d"))

WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# end date
def inputEndDate(eD):
    global eYear
    global eMonth
    global eDay
    global eDate
    unformatattedDate = eD.split("/")
    eYear = unformatattedDate[0]
    eMonth = unformatattedDate[1]
    eDay = unformatattedDate[2]
    eDate = date(int(eYear), int(eMonth), int(eDay))
    print("End Date: " + eDate.strftime("%Y %m %d"))
    if eDate.month - sDate.month > 2 or eDate.year - sDate.year > 1:
        raise Exception(WARNING+"Entered date range is too big, the dates have to be within 2 months"+ENDC)


lstYMD=[]
def returnDateList():
    lstYMD.clear()
    delta = eDate-sDate
    for i in range(delta.days +1):
        date = sDate + timedelta(days=i)
        lstYMD.append(date.strftime("%Y/%m/%d"))
    return sorted(lstYMD)


def usertime(sTime, eTime):
    global formattedSelectedTimeWithComma
    global formattedSelectedTimeWithSpace
    global sTimeBash
    sTimeBash = sTime
    #gets index then generates a list within the index
    sIndex = hours.index(sTime)
    eIndex = hours.index(eTime)
    unformattedSelectedTime = ""
    for timeList in range(eIndex - sIndex + 1):
        unformattedSelectedTime += hours[sIndex + timeList]
    # for every 3 character
    formattedSelectedTimeWithComma = ','.join(
        unformattedSelectedTime[i:i + 3] for i in range(0, len(unformattedSelectedTime), 3))
    formattedSelectedTimeWithSpace = ' '.join(
        unformattedSelectedTime[i:i + 3] for i in range(0, len(unformattedSelectedTime), 3))
    print("Start Time: "+hour24[sIndex])
    print("End Time: "+hour24[eIndex])


bothCheked = 0
def modelCheckbox(h_00, h_12):
    global modelHour
    global modelHourBash
    global bothCheked
    h_00 = int(h_00)
    h_12 = int(h_12)
    if (h_00 is True and h_12 is False) or (h_00 is 1 and h_12 is 0):
        modelHour = "00"
        modelHourBash = "00"
        bothCheked = 1
    elif (h_12 is True and h_00 is False) or (h_00 is 0 and h_12 is 1):
        modelHour = "12"
        modelHourBash = "12"
        bothCheked = 2
    elif (h_12 and h_00 is True) or (h_00 is 1 and h_12 is 1):
        modelHour = "00,12"
        modelHourBash = "00"
        bothCheked = 3
    else:
        modelHour = " "


def particuleCheckBox(O3, NO2, others, PM25):
    global formattedParticuleString
    O3 = int(O3)
    NO2 = int(NO2)
    PM25 = int(PM25)
    stringO3 = ""
    stringNO2 = ""
    stringPM25 = ""
    if O3 is 1:
        stringO3 = "O3"
    if NO2 is 1:
        stringNO2 = "N2"
    if PM25 is 1:
        stringPM25 = "AF"
    unformattedParticuleString = stringO3 + stringNO2 + stringPM25 + others
    # for every 2 character, add space
    formattedParticuleString = ' '.join(
        unformattedParticuleString[i:i + 2] for i in range(0, len(unformattedParticuleString), 2))
    return formattedParticuleString


def level(lv):
    global lev
    #if nothing inputed by user, keep as default
    if lv is "":
        lev = "76696048 93423264"
    # else, change to what the user wrote
    else:
        lev = lv


def rarcFile(modelType,branche):
    modelHourList = re.split(",", modelHour)
    file = open(modelType, "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = "+branche+"\n"
        "ext = " + formattedSelectedTimeWithComma +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    fileEticket = open(modelType+"Eticket.tcl", "w")
    fileEticket.write(
        "#!/bin/bash\n"
        "# : - \\"
        "\nexec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh \"$0\" \"$@\""
        "\npackage require TclData\n"
        "set Path "+filelocation+"/rarc/"+branche+"/"
        "\nset bashFST "+ sYear + sMonth+sDay+modelHourList[0]+"_"+formattedSelectedTimeWithComma.split(",")[0]+
        "\nset FileOut [open "+modelType+"Eticket.txt w+]"
        "\nset FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]"
        "\nfstdfile open 1 read  $FileIn"
        "\nset eticket [fstdfile info 1 ETIKET]"
        "\nputs $eticket"
        "\nputs $FileOut \"$eticket\""
        "\nfstdfile close 1"
        "\nclose $FileOut"
    )


def bashFile(selectedDate,modeltype,branche):
    templst = selectedDate.split("/")
    year = templst[0]
    month = templst[1]
    day = templst[2]
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open(modeltype + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut="+filelocation+"/bash"
            "\nPathIn="+filelocation+"/rarc"
            "\nDateDebut=" + year + month+day+
            "\nDateFin=" + year + month + day+
            "\nDateDebutMois="+month+
            "\nListeMois=\"" + month + "\""
            "\nAnnee=" + year +  # not useds
            "\nTag1="+modeltype+modelHourSeparated+
            "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
            "\nType=species"
            "\nFichierTICTAC="+filelocation+"/rarc/"+branche+"/${Annee}${DateDebutMois}" + day + modelHourBash + "_" + sTimeBash +
            "\nListeVersionsGEM=\""+branche+"\""
            "\nListeEspeces=\""+formattedParticuleString+"\"" # formattedParticuleString, if other polluant are needed
            "\nListeNiveaux=\"" + lev + "\""  # TODO confirm levels
            "\nListeJours=\"" + day + "\""
            "\nListePasse=\"" + modelHourSeparated + "\""
            "\nListeHeures=\"" + formattedSelectedTimeWithSpace + "\""
            "\n################# Extraction#############"
            "\nfor VersionGEM in  ${ListeVersionsGEM}"
            "\ndo"
            "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}.fst"
            "\nif [  ${FileOut1}  ]; then"
            "\nrm -rf  ${FileOut1}"
            "\nelse"
            "\ncontinue"
            "\nfi"
            "\nFileIn=${FichierTICTAC}"
            "\n${editfst} -s ${FileIn} -d ${FileOut1} <<EOF"
            "\nDESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)"
            "\nEOF"
            "\nfor mois in ${ListeMois}"
            "\ndo"
            "\necho ${mois}"
            "\nfor jour in ${ListeJours}"
            "\ndo"
            "\nfor passe  in ${ListePasse}"
            "\ndo"
            "\nfor heure in ${ListeHeures}"
            "\ndo"
            "\necho ${heure}"
            "\nFileIn1=${PathIn}/${VersionGEM}/${Annee}${mois}${jour}${passe}_${heure}"
            "\nif [ ! ${FileIn1}  ]; then"
            "\ncontinue"
            "\nelse"
            "\necho \"-------------\""
            "\necho ${FileIn1} \"file does exist\""
            "\nfi"
            "\necho ${FileIn1}"
            "\nfor Espece in ${ListeEspeces}"
            "\ndo"
            "\nif [ \"$Espece\" = \"P0\" ] || [ \"$Espece\" = \"TCC\" ] ; then"
            "\n${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF"
            "\nDESIRE (-1,\"$Espece\",-1, -1, 0, -1, -1)"
            "\nEOF"
            "\nelse"
            "\nfor niveau in  ${ListeNiveaux}"
            "\ndo"
            "\n${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF"
            "\nDESIRE (-1,\"$Espece\",-1, -1, $niveau, -1, -1) "
            "\nEOF"
            "\ndone"
            "\nfi"
            "\ndone"
            "\ndone"
            "\ndone"
            "\ndone"
            "\ndone"
            "\ndone\n"
            )
        print(modeltype+" Config Files Saved!")


def getEticket(modelType):
    os.system("./"+modelType+"Eticket.tcl")


#generates script at the chosen location
# What this does is it generates a TCL config file for EVERY hour, EVERY molecule, and every day, this is why there is a lot of file
# This is to bypass the 12h empty date bug from the tcl script
# a lot of 0kb file will be generated from running this script but they are deleted after
def locationExtraction(iditem, selectedDate,modelType):
    modelHourList = re.split(",", modelHour)
    #deletelist = os.listdir(filelocation+"/extracted")
    shutil.rmtree(filelocation+"/extracted"+modelType)
    os.mkdir(filelocation+"/extracted"+modelType)
    for modelH in modelHourList:
        if modelH == "12":
            generateTCL(modelH,iditem,selectedDate.split("/"),modelType)
        if modelH == "00":
            generateTCL(modelH,iditem,selectedDate.split("/"),modelType)


def generateTCL(modelH,iditem,selectedDate,modelType):
    global locationID
    year = selectedDate[0]
    month = selectedDate[1]
    day = selectedDate[2]
    gemFileEticket = open(modelType+"Eticket.txt", "r")
    EticketGM = gemFileEticket.read().strip()
    listIndex = lstID.index(iditem)
    name = lstName[listIndex]
    long = lstLongitude[listIndex]
    lat = lstLatitude[listIndex]
    executehour = re.split(",", formattedSelectedTimeWithComma)
    s = hours.index(executehour[0])
    e = hours.index(executehour[-1])
    particulelist = re.split(" ", formattedParticuleString)
    locationID = lstID[listIndex]

    for I in range(int(e)-int(s)+1):
        for p in particulelist:
            starttime = datetime(int(year),int(month),int(day),int(modelH))+timedelta(hours = int(s))
            generatedTime = starttime +timedelta(hours = I)
            time00Format = generatedTime.strftime("%H")
            time0Format = generatedTime.strftime("%-H")
            dateToFile = generatedTime.strftime("%d")
            monthToFile = generatedTime.strftime("%m")
            config = open("config"+modelType+"/" + p+"_"+monthToFile + dateToFile + time00Format + modelH + ".tcl", "w")
            config.write(
                "set Data(SpLst)  \"" + p + "\" \n"
                "set Data(TAG1)   \""+modelType + modelH + "." + year + month + day + "\"\n"
                "set Data(TAG3)   \"" + monthToFile + dateToFile + time00Format + "\"\n"
                "set Data(outTXT)       \"SITE\" \n"
                "set Data(PASSE) \"" + modelH + "\"\n"
                "set Data(levels) \"-1""\"\n"
                "set Data(MandatoryLevels) \" "+year + month + day+modelH+"\"\n"
                "set Data(Path)    " + filelocation + "/bash\n"
                "set Data(PathOut) " + filelocation + "/extracted"+modelType+"\n"
                "set Data(Start)      \"" + year + monthToFile + "\"\n"
                "set Data(End)      \"" + year + monthToFile + "\"\n"
                "set Data(Eticket)     \"" + EticketGM + "\"\n"
                "set Data(point) \"" + name + "\"\n"
                "set Data(coord) \"" + str(lat) + " " + str(long) + "\"\n"
                "set Data(days) \"" + dateToFile + "\"\n"
                "set Data(hours) \"" + time0Format + "\"\n")

#runs all the file generated,  it is normal to see Error #8 while running
def launchTCL(modelType):
    os.system(" ls "+filelocation+"/config"+modelType+" | sort -st '/' -k1,1")
    os.system("chmod -R 744 "+ filelocation+"/config"+modelType)
    for a in os.listdir('config'+modelType):
        print(a)
        os.system("./extract1.tcl " + "config"+modelType+"/" + a)


#removes empty file that are generated
docName = []
def removeEmptyFile(path):
    docList = os.listdir(path)
    for doc in docList:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) == 0:
                os.remove(docPath)
        if os.path.isdir(docPath):
            removeEmptyFile(docPath)


#deletes all file after the script is done running
Name = []
def removeAllfile(path):
    Name = os.listdir(path)
    for doc in Name:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) > 0:
                os.remove(docPath)


def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


def generateExcel(fileName):
    df = pd.read_csv("output_csv/"+fileName)
    hourslst = df['Time(Z)'].tolist()
    temp = []
    for h in hourslst:
        t = datetime.strptime(str(h), "%H").strftime("%H")
        temp.append(t)
    df['Time(Z)'] = temp
    df['Value'] = df['Value'].round(0)
    df.to_excel(filelocation+"/output_excel/"+fileName[:-4]+".xlsx",engine="xlsxwriter",  index=False, index_label=False)

#sorts and generates a CSV file in the output folder
def sortAndGenerate(destination, selectedDate,modelType):
    year = selectedDate.split("/")[0]
    month = selectedDate.split("/")[1]
    day = selectedDate.split("/")[2]
    particulelist = re.split(" ", formattedParticuleString)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extracted"+modelType+" | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            #output/GEM__" + "ID" + locationID + "___" + m + p + "___" + year + month + day +"_.csv
            uniqueFileName = uniquify("output_csv/"+year + month + day +m+"_"+modelType+"_"+p+"_"+returnName(locationID)+".csv")
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
                file = open(uniqueFileName, "w+")
                file.write("Model Run,Date,Time(Z),Value\n")
                for i in sorted(os.listdir(destination + m + p)):
                    file.write(open(destination + m + p + "/" + i).read())
                file.close()
            generateExcel(uniqueFileName.split("/")[-1])
    # generateExcel(exceltreatinglst)
    print("\nJob done, see folder for csv file-->" + filelocation + "/output_csv")
    print("\nJob done, see folder for excel file-->" + filelocation + "/output_excel")
