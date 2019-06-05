import csv
import glob
import os
import re
import shutil

import Gemmach as Gm

#creates a dictionary based on the station ID and 3 letter Code
filelocation = Gm.filelocation
file = open("UMOS_Ref.csv", "r")
reader = csv.reader(file)
UMOSRefList = list(reader)
lstStationID = []
lstUMOSID = []

for x in range(len(UMOSRefList)):
    line = UMOSRefList[x]
    stationID = line[1]
    lstStationID.append(stationID)
    UMOSID = line[2]
    lstUMOSID.append(UMOSID)

referenceDict = dict(zip(lstStationID,lstUMOSID))

#formats the start date
def inputStartDate(sDate):
    global sYear
    global sMonth
    global sDay
    #splits the entry into a tuple
    unformatattedDate = re.split("/",sDate)
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
    elif sMonth in Gm.oddMonths and int(sDay) > 31:
        dateErrors()
    elif sMonth in Gm.evenMonths and int(sDay) > 30:
        dateErrors()


# end date
def inputEndDate(eDate):
    global eYear
    global eMonth
    global eDay
    unformatattedDate = re.split("/", eDate)
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
    elif eMonth in Gm.oddMonths and int(eDay) > 31:
        dateErrors()
    elif eMonth in Gm.evenMonths and int(eDay) > 30:
        dateErrors()
    elif sMonth > eMonth:
        dateErrors()
    elif sMonth == eMonth and sDay > eDay:
        dateErrors()
    #used to distinguish which archive to go see
    if int(eYear+eMonth+eDay)<20170105:
        return False


def dateErrors():
    raise Exception("Date format error, please check what you have entered")

def modelCheckbox(h_00, h_12):
    global modelHour
    global modelHourBash
    global bothCheked
    global modelHourList
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
    modelHourList = re.split(",", modelHour)


def getDataAtLocationPre2017(locationID, molecule, modelHourList):
    stationCode = referenceDict[locationID]
    startDateIndex = Gm.days.index(sDay)
    endDateIndex = Gm.days.index(eDay)
    daylst = Gm.days[startDateIndex:endDateIndex + 1]
    for m in molecule:
        for sub in os.listdir("rarc/operation.umos.aq.prevision.csv."+m.lower()+"sp3"):
            for d in daylst:
                for h in modelHourList:
                    if sub == sYear+sMonth+d+h+"_csv":
                        os.system("cat " + filelocation + "/rarc/operation.umos.aq.prevision.csv." + m.lower() + "sp3/" + sYear+sMonth+d+h + "_csv | grep "+ stationCode +" > " + filelocation + "/UMOSTreating/" + sYear+sMonth+d+h + "_csv")
        for untreated in os.listdir("UMOSTreating"):
            with open("UMOSTreating/" + untreated, "r") as infile, open(
                    "output/UMOS__ID" + locationID +"__"+ untreated +m.lower()+ ".csv",
                    'w') as outfile:
                outfile.write("Date_Orig,Date_Valid,Code_Stn(ID),Lat,Lon,Vertical,Var,Value\n")
                for line in infile:
                    withcomma = line.replace('|', ',')
                    withoutspace = withcomma.replace(" ", "")
                    changeName = withoutspace.replace(stationCode, locationID)
                    outfile.write(changeName)
    print("Job done, see folder-->" + filelocation + "/output")
    removeAllfile(r'' + filelocation + "/UMOSTreating")


def particuleCheckBoxAndTime(O3, NO2, PM25, loc, datesplit, active):
    global moleculeList
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
        stringPM25 = "P2"
    unformattedParticuleString = stringO3 + stringNO2 + stringPM25
    # for every 2 character, add space
    formattedParticuleString = ' '.join(unformattedParticuleString[i:i + 2] for i in range(0, len(unformattedParticuleString), 2))
    moleculeList = re.split(" ", formattedParticuleString)
    if datesplit is not False:
        for h in modelHourList:
            for mol in moleculeList:
                os.system(
                    "cmcarc -x 'prevision.csv/" + mol.lower() + "sp3.*' -f " + filelocation + "/rarc/operation.umos.aq.prevision/" + sYear+sMonth+sDay+h+ "_")
        if active is True:
            getDataAtLocation(loc)
            print("\nFile Extracted, Getting Location Data")
    else:
        if active is True:
            getDataAtLocationPre2017(loc, moleculeList, modelHourList)


def rarcFile(datesplit):
    for filename in glob.glob("rarc/umos*"):
        os.remove(filename)
    if datesplit is not False:
        umosFile = open("rarc/umos", "w")
        umosFile.write(
            "target = "+filelocation+"/rarc\n"
            "filter = copy\n"
            "postprocess = nopost\n"
            "date = "
            # start
            + sYear + "," + sMonth + "," + sDay + ","
            # end
            + eYear + "," + eMonth + "," + eDay +
            "\nbranche = operation.umos.aq.prevision\n"
            "ext = noextension\n"
            "heure = "+modelHour+"\n"
            "priority = online\n"
            "inc = 1\n"
            "#\n")
        print("UMOS File Saved")
    else:
        for l in moleculeList:
            umosFile = open("rarc/umos"+l, "w")
            umosFile.write(
                "target = " + filelocation + "/rarc\n"
                                             "filter = copy\n"
                                             "postprocess = nopost\n"
                                             "date = "
                # start
                + sYear + "," + sMonth + "," + sDay + ","
                # end
                + eYear + "," + eMonth + "," + eDay +
                "\nbranche = operation.umos.aq.prevision.csv."+l.lower()+"sp3\n"
                "ext = ***\n"
                "heure = " + modelHour + "\n"
                                         "priority = online\n"
                                         "inc = 1\n"
                                         "#\n")
        print("UMOS File Saved")


Name = []
def removeAllfile(path):
    Name = os.listdir(path)
    for doc in Name:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) > 0:
                os.remove(docPath)


def getDataAtLocation(locationID):
    stationCode = referenceDict[locationID]
    for sub in os.listdir("prevision.csv"):
        for file in os.listdir("prevision.csv/" + sub):
            os.system(
                "cat " + filelocation + "/prevision.csv/" + sub + "/" + file + "| grep " + stationCode + " > " + filelocation + "/UMOSTreating/" + file + sub)
        for untreated in os.listdir("UMOSTreating"):
            with open("UMOSTreating/" + untreated, "r") as infile, open("output/UMOS__ID"+locationID +"__"+ untreated + ".csv",
                                                                        'w') as outfile:
                outfile.write("Date_Orig,Date_Valid,Code_Stn(ID),Lat,Lon,Vertical,Var,Value\n")
                for line in infile:
                    withcomma = line.replace('|', ',')
                    withoutspace = withcomma.replace(" ", "")
                    changeName = withoutspace.replace(stationCode, locationID)
                    outfile.write(changeName)
    print("Job done, see folder-->" + filelocation+"/output")
    removeAllfile(r''+filelocation + "/UMOSTreating")
    shutil.rmtree("prevision.csv")