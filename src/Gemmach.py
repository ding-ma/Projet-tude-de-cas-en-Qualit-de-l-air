import collections
import csv
import difflib
import os
import re
import shutil
import string

# Setings used for the entire program, change/ add as needed

# This format is used to bash and rarc scripts
hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031",
    "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047",
    "048")

# This format is used for the tcl script
tcl = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
    "40", "41", "42", "43", "44", "45", "46", "47", "48"]

# This format is used to sort the files
hour24 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
          "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]

# extra hours if needed to be added
# ,"49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72"
# ,"049","050","051","052","053","054","055","056","057","058","059","060","061","062","063","064","065","066","067","068","069","070","071","072"


# Change etiquette here - Gemmach
EticketGEM = "RAQDPS020"

# For UMOS
EticketUMOS = "CAPAMIST"

# For Firework
EticketFW = "RAQDPS019FW"

#Do not touch the rest!
##################################################

years = ("2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012",
         "2013", "2014", "2015", "2016",
         "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029",
         "2030", "2031", "2032", "2033",
         "2034", "2035", "2036", "2037", "2038", "2039", "2040", "2041", "2042", "2043", "2044", "2045", "2046",
         "2047", "2048", "2049", "2050")

days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
    , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "01", "02")


#code to create repos and make sure everything is executable
filelocation = os.getcwd()
directories = ["bash", "config", "rarc", "output", "extracted", "UMOSTreating", "configMIST", "extractedMist", "configFw", "extractedFw"]
for i in directories:
    if not os.path.exists(filelocation+"/"+i):
        os.mkdir(filelocation+"/"+i)
os.system("chmod -R 777 "+ filelocation)
filedirectory = next(os.walk('.'))[1]

# search for StationID or StationName
stationFile = open("stations.csv", "r")
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
        stationName = lstName[index]
        return stationName + " (" + stationID + ") Lat: " + stationLatitude + " Lon: " + stationLongitude


#returns the index of the item if it exist else, it returns false, gets around the item out of bound problem
def isStationFound(StationInput):
    a = difflib.get_close_matches(StationInput, lstName, n=1, cutoff=.4)
    if a is []:
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
    return lstName[index]


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

#returns list of all the stations based on the selected province
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


oddMonths = ("01", "03", "05", "07", "08", "10", "12")
evenMonths = ("04", "06", "09", "11")

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
def inputStartDate(sDate):
    global sYear
    global sMonth
    global sDay
    #splits the entry into a tuple
    unformatattedDate = re.split("/", sDate)
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]
    # checks for leap year
    if int(sYear) % 4 == 0 and int(sYear) % 100 != 0 or int(sYear) % 400 == 0:
        leap = True
    else:
        leap = False

    #this is used for changing the combobox in the UI
    if sMonth in oddMonths:
        return days[1:-2]
    if sMonth in evenMonths:
        return days[1:-3]
    if leap is True and int(sMonth) is 2:
        return days[1:-4]
    if leap is False and int(sMonth) is 2:
        return days[1:-5]
    ###

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
    # error checking
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


listMonth = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
#for bash
def listofMonth():
    global formattedMonthlist
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
    return formattedParticuleString


def level(lv):
    global lev
    #if nothing inputed by user, keep as default
    if lv is "":
        lev = "76696048 93423264"
    # else, change to what the user wrote
    else:
        lev = lv

#generating rarc script
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
    print("Gem-Mach File Saved")

#generates bash script
def bashFile():
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("gemmachBashTest" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut="+filelocation+"/bash"
            "\nPathIn="+filelocation+"/rarc"
            "\nDateDebut=" + sYear + sMonth+
            "\nDateFin=" + eYear + eMonth + eDay+
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
            "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}"+sDay+"_${DateFin}_${Grille}.fst"
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
        print("Bash File Saved!")


#generates script at the chosen location
# What this does is it generates a TCL config file for EVERY hour, EVERY molecule, and every day, this is why there is a lot of file
# This is to bypass the 12h empty date bug from the tcl script
# a lot of 0kb file will be generated from running this script but they are deleted after
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
                        "set Data(TAG1)   \"BashOut" + modelH + "."+sYear+sMonth+sDay+"_"+eYear+eMonth+eDay+"_regeta\"\n"
                        "set Data(TAG3)   \"" + d + "" + hToName + "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \""+modelH+"\"\n"
                        "set Data(levels) \" -1""\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1""\"\n"
                        "set Data(Path)    "+filelocation+"/bash\n"
                        "set Data(PathOut) "+filelocation+"/extracted\n"
                        "set Data(Start)      \"" + sYear + sMonth + "\"\n"
                        "set Data(End)      \"" + eYear + eMonth + "\"\n"
                        "set Data(Eticket)     \""+EticketGEM+"\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "set Data(days) \"" + str(
                        d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n"
                    )
    print("Done")


#runs all the file generated,  it is normal to see Error #8 while running
def launchTCL():
    os.system(" ls "+filelocation+"/config | sort -st '/' -k1,1")
    os.system("chmod -R 777 "+ filelocation+"/config")
    for a in os.listdir('config'):
        os.system("./extract1.tcl " + "config/" + a)


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


#sorts and generates a CSV file in the output folder
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
            file = open("output/GEM__"+"ID"+locationID +"___"+m + p+"___Start"+sYear+sMonth+sDay +"___End"+eYear+eMonth+eDay+ ".csv", "w+")
            file.write("Date,Time,Height,Value\n")
            for i in sorted(os.listdir(destination + m + p)):
                b = open(destination + m + p + "/" + i).read()
                file.write(b)
    print("\nJob done, see folder-->" + filelocation+"/output")