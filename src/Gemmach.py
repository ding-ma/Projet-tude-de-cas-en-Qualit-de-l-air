#!/usr/bin/env python3
import csv
import os
import re
import shutil
import string

# Notes: def modelChosen(model): always needs to be the last function!
filelocation = os.getcwd()

directories = ["bash", "config", "rarc", "output", "extracted"]

for i in directories:
    if not os.path.exists(filelocation+"/"+i):
        os.mkdir(filelocation+"/"+i)
os.system("chmod -R 777 "+ filelocation)
filedirectory = next(os.walk('.'))[1]

# to connect to host, not working
# def CMCServerConnection():  # add arguments to change user/pass
#     host = "sci-eccc-in.science.gc.ca"
#     host = "199.212.17.148"
#     user = "sair001"
#     passw= "1AiqaCom!"
#     port = 22
#     client = paramiko.SSHClient()ll

#     client.set_missing_host_key_policy(paramiko.WarningPolicy())
#     print(" Connecting to %s \n with username: %s... \n" % (host, user))
#     client.connect(hostname=host, port=port, username=user,password=passw)
#     print("connected")
#     stdin, stdout, stderr = client.exec_command("alias")
#     print(stderr.readlines)

# search for StationID or StationName
stationFile = open("stations_DB.csv", "r")
reader = csv.reader(stationFile)
stationList = list(reader)
# creates list based on csv entry
lstID = []
lstName = []
#lstDisplay is for the UI
lstDisplay = []
lstLatitude = []
lstLongitude = []
lstProvince = []
for x in range(len(stationList)):
    line = stationList[x]
    ids = line[0]
    name = line[1]
    latitude = line[3]
    longitude = line[4]
    province = line[5]
    lstDisplay.append(ids + ": " + name)
    lstID.append(ids)
    lstName.append(name)
    lstLatitude.append(latitude)
    lstLongitude.append(longitude)
    lstProvince.append(province)

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
        return string.capwords(station) + " (" + stationID + ") Lat: " + stationLatitude + " Lon: " + stationLongitude


#returns the index of the item if it exist else, it returns false, gets around the item out of bound problem
def isStationFound(StationInput):
    if StationInput in lstName:
        return lstName.index(StationInput)
    return False


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
        return findWithStation(userInput)
    else:
        return findWithID(userInput)


lstNL = []
lstPEI = []
lstNS = []
lstNB = []
lstQC = []
lstONT = []
lstMAN = []
lstSASK = []
lstALB = []
lstBC = []
lstYK = []
lstNWT = []
lstNVT = []
j = 0
for i in lstProvince:
    if i == "1":
        a = lstID[j]
        lstNL.append(a)
    if i == "2":
        b = lstID[j]
        lstPEI.append(b)
    if i == "3":
        c = lstID[j]
        lstNS.append(c)
    if i == "4":
        d = lstID[j]
        lstNB.append(d)
    if i == "5":
        q = lstID[j]
        lstQC.append(q)
    if i == "6":
        w = lstID[j]
        lstONT.append(w)
    if i == "7":
        e = lstID[j]
        lstMAN.append(e)
    if i == "8":
        r = lstID[j]
        lstSASK.append(r)
    if i == "9":
        t = lstID[j]
        lstALB.append(t)
    if i == "10":
        y = lstID[j]
        lstBC.append(y)
    if i == "11":
        u = lstID[j]
        lstNWT.append(u)
    if i == "12":
        o = lstID[j]
        lstYK.append(o)
    if i == "13":
        p = lstID[j]
        lstNVT.append(p)
    j = j + 1

prov = ["AB", "BC", "MB", "NB", 'NL', "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT"]

provinceDic = {
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
    "YT": lstYK
}

provlist = []


def gettingprovlist(prov):
    for y in provinceDic[prov]:
        indexofitem = lstID.index(y)
        display = lstDisplay[indexofitem]
        provlist.append(display)
    return provlist

########

# change filename to gemmach


oddMonths = ("01", "03", "05", "07", "09", "11")
evenMonths = ("04", "06", "08", "10", "12")


#formats the start date
def inputStartDate(sDate):
    global sYear
    global sMonth
    global sDay
    #splits the entry into a tuple
    unformatattedDate = sDate.split("/")
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]
    # checks for leap year
    if int(sYear) % 4 == 0 and int(sYear) % 100 != 0 or int(sYear) % 400 == 0:
        leap = True
    else:
        leap = False
    #checks if the user input is correct
    if len(sYear) != 4 or len(sMonth) != 2 or sMonth > "12" or len(sDay) != 2:
        dateErrors()
    elif leap is True and int(sDay) > 29 and sMonth == "02":
        dateErrors()
    elif leap is False and sMonth == "02" and int(sDay) > 28:
        dateErrors()
    elif sMonth in oddMonths and int(sDay) > 31:
        dateErrors()
    elif sMonth in evenMonths and int(sDay) > 30:
        dateErrors()
    else:
        print("Start Date: " + sYear, sMonth, sDay)


# end date
def inputEndDate(eDate):
    global eYear
    global eMonth
    global eDay
    unformatattedDate = eDate.split("/")
    eYear = unformatattedDate[0]
    eMonth = unformatattedDate[1]
    eDay = unformatattedDate[2]
    # checks for leap year
    if int(eYear) % 4 == 0 and int(eYear) % 100 != 0 or int(eYear) % 400 == 0:
        leap = True
    else:
        leap = False

    if len(eYear) != 4 or len(eMonth) != 2 or eMonth > "12" or len(eDay) != 2:
        dateErrors()
    elif leap is True and eMonth == "02" and int(eDay) > 29:
        dateErrors()
    elif leap is False and eMonth == "02" and int(eDay) > 28:
        dateErrors()
    elif eMonth in oddMonths and int(eDay) > 31:
        dateErrors()
    elif eMonth in evenMonths and int(eDay) > 30:
        dateErrors()
    elif sMonth > eMonth:
        dateErrors()
    elif sMonth == eMonth and sDay > eDay:
        dateErrors()
    else:
        print("End Date: " + eYear, eMonth, eDay)
        listOfDays()
        listofMonth()


def dateErrors():
    raise Exception("Date format error, please check what you have entered")


hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

def time(sTime, eTime):
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


days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
    , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
# used for bashfile
def listOfDays():
    global formattedDay
    global startDateIndex
    global endDateIndex
    startDateIndex = days.index(sDay)
    endDateIndex = days.index(eDay)
    unformattedDay = ""
    for dayList in range(endDateIndex - startDateIndex + 1):
        unformattedDay += days[startDateIndex + dayList]
    #for every 2 character, adds space
    formattedDay = ' '.join(unformattedDay[i:i + 2] for i in range(0, len(unformattedDay), 2))

#for bash
def listofMonth():
    global formattedMonthlist
    listMonth = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
    sIndex = listMonth.index(sMonth)
    eIndex = listMonth.index(eMonth)
    unformattedMonthList = ""
    for monthList in range(eIndex - sIndex + 1):
        unformattedMonthList += listMonth[sIndex + monthList]
        formattedMonthlist = ' '.join(unformattedMonthList[i:i + 2] for i in range(0, len(unformattedMonthList), 2))

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


def level(lv):
    global lev
    if lv is "":
        lev = "93423264 76696048"
    else:
        lev = lv

# rarc cmd
# rarc -i /home/sair001/rarcdirectives/gemmach -tmpdir ./temp
def rarcFile():
    file = open("gemmach", "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.forecasts.mach\n"
        "ext = " + formattedSelectedTimeWithComma +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    bashFile()
    print("File Saved")


def bashFile():
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("gemmachBashTest" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut="+filelocation+"/bash"
            "\nPathIn="+filelocation+"/rarc"
            "\nDateDebut=" + sYear + sMonth +
            "\nDateFin=" + eYear + eMonth +
            "\nListeMois=\"" + formattedMonthlist + "\""
            "\nAnnee=" + sYear +  # not used
            "\nTag1=BashOut"+modelHourSeparated+
            "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
            "\nType=species"
            "\nGrille=regeta"
            "\nFichierTICTAC="+filelocation+"/rarc/operation.forecasts.mach/${DateDebut}" + sDay + modelHourBash + "_" + sTimeBash +
            "\nListeVersionsGEM=\"operation.forecasts.mach\""
            "\nListeEspeces=\"" + formattedParticuleString + "\""
            "\nListeNiveaux=\"" + lev + "\""  # TODO confirm levels
            "\nListeJours=\"" + formattedDay + "\""
            "\nListePasse=\"" + modelHourSeparated + "\""
            "\nListeHeures=\"" + formattedSelectedTimeWithSpace + "\""
            "\n################# Extraction#############"
            "\nfor VersionGEM in  ${ListeVersionsGEM}"
            "\ndo"
            "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst"
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
            "\nFileIn1=${PathIn}/${VersionGEM}/${DateDebut}${jour}${passe}_${heure}"
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
        print("saved!")


tcl = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
    "40", "41", "42", "43", "44", "45", "46", "47", "48"]

hour24 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]

def locationExtraction(iditem):
    deletelist = os.listdir(filelocation+"/extracted")
    for d in deletelist:
        shutil.rmtree(filelocation+"/extracted/" + d)
    global locationID
    listIndex = lstID.index(iditem)
    name = lstName[listIndex]
    long = lstLongitude[listIndex]
    lat = lstLatitude[listIndex]
    locationID = lstID[listIndex]
    modelHourList = re.split(",", modelHour)
    executehour = re.split(",", formattedSelectedTimeWithComma)
    s = hours.index(executehour[0])
    e = hours.index(executehour[-1])
    particulelist = re.split(" ", formattedParticuleString)
    if sYear+sMonth+sDay > "20160907":
        level = "76696048"
    else:
        level = "93423264"
    for p in particulelist:
        for modelH in modelHourList:
            if modelH == "12":
                dayList = days[startDateIndex: endDateIndex + 2]
            else:
                dayList = days[startDateIndex: endDateIndex + 1]
            for d in dayList:
                for hToFile, hToName in zip(tcl[s:e + 1], hour24[s:e + 1]):
                    config = open("config/" +p+ d + hToName + modelH +".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"BashOut" + modelH + "."+sYear+sDay+"_"+eYear+eDay+"_regeta\"\n"
                        "set Data(TAG3)   \"" + d + "" + hToName + "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \""+modelH+"\"\n"
                        "set Data(levels) \" "+level+"\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" "+level+"\"\n"
                        "set Data(Path)    "+filelocation+"/bash\n"
                        "set Data(PathOut) "+filelocation+"/extracted\n"
                        "set Data(Start)      \"" + sYear + sMonth + "\"\n"
                        "set Data(End)      \"" + eYear + eMonth + "\"\n"
                        "set Data(Eticket)     \"RAQDPS020\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "set Data(days) \"" + str(
                        d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n"
                    )
    print("Done")


def launchTCL():
    os.system(" ls "+filelocation+"/config | sort -st '/' -k1,1")
    os.system("chmod -R 777 "+ filelocation+"/config")
    for a in os.listdir('config'):
        os.system("./extract1.tcl " + "config/" + a)


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


Name = []
def removeAllfile(path):
    Name = os.listdir(path)
    for doc in Name:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) > 0:
                os.remove(docPath)

def sortAndGenerate(destination):
    particulelist = re.split(" ", formattedParticuleString)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extracted | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
            file = open("output/"+"ID"+locationID +"___"+m + p+"___Start"+sYear+sMonth+sDay +"___End"+eYear+eMonth+eDay+ ".csv", "w+")
            for i in sorted(os.listdir(destination + m + p)):
                b = open(destination + m + p + "/" + i).read()
                file.write(b)
    print("\nJob done, see folder-->" + filelocation+"/output")