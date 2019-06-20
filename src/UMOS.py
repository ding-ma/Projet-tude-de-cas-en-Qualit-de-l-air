import calendar
import csv
import glob
import os
import re
import shutil
from datetime import date, timedelta

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
    listOfDays()
    if eDate.timetuple()<date(2017,1,5).timetuple():
        return False


lstsMonth = []
lsteMonth = []
lstDays = []
def datecounter(addDays):
    lstsMonth.clear()
    lsteMonth.clear()
    lstDays.clear()
    startDate = date(int(sYear), int(sMonth), int(sDay))
    endDate = date(int(eYear), int(eMonth), int(eDay))
    if startDate.month is not endDate.month:
        lstsMonth.append(startDate.strftime("%m"))
        lsteMonth.append(endDate.strftime("%m"))
        a = calendar.monthrange(int(sYear), int(sMonth))[1]
        endMonth = date(int(sYear), int(sMonth), a)
        delta1 = endMonth - startDate
        for f in range(delta1.days + addDays):
            a = startDate + timedelta(days=f)
            t = a.strftime("%d")
            lstsMonth.append(t)
        startMonth = date(int(sYear), int(eMonth), 1)
        delta2 = endDate - startMonth
        for q in range(delta2.days + addDays):
            c = startMonth + timedelta(days=q)
            w = c.strftime("%d")
            lsteMonth.append(w)
        return lstsMonth,lsteMonth
    else:
        lstDays.append(startDate.strftime("%m"))
        delta = endDate - startDate
        for a in range(delta.days + addDays):
            e = startDate + timedelta(days=a)
            v = e.strftime("%d")
            lstDays.append(v)
        return lstDays


# used for bashfile
def listOfDays():
    global formattedDay
    global genday
    unformattedDay = ""
    genday = datecounter(1)
    if len(genday) is 2 and isinstance(genday,tuple):
        for l in genday[0]:
            unformattedDay +=l
        for z in genday[1]:
            unformattedDay +=z
    else:
        for l in genday:
            unformattedDay+=l
    formattedDay = ' '.join(unformattedDay[i:i + 2] for i in range(0, len(unformattedDay), 2))


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
    if isinstance(genday,tuple):
        firstmonth = genday[0][0]
        firstmonthdays = genday[0][1:]
        secondmonth = genday[1][0]
        secondmonthdays = genday[1][1:]
        for m in molecule:
            for sub in os.listdir("rarc/operation.umos.aq.prevision.csv."+m.lower()+"sp3"):
                for d in firstmonthdays:
                    for h in modelHourList:
                        if sub == sYear+firstmonth+d+h+"_csv":
                            os.system("cat " + filelocation + "/rarc/operation.umos.aq.prevision.csv." + m.lower() + "sp3/" + sYear+firstmonth+d+h + "_csv | grep "+ stationCode +" > " + filelocation + "/UMOSTreating/" + sYear+firstmonth+d+h + "_csv")
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

        for m in molecule:
            for sub in os.listdir("rarc/operation.umos.aq.prevision.csv."+m.lower()+"sp3"):
                for d in secondmonthdays:
                    for h in modelHourList:
                        if sub == sYear+secondmonth+d+h+"_csv":
                            os.system("cat " + filelocation + "/rarc/operation.umos.aq.prevision.csv." + m.lower() + "sp3/" + sYear+secondmonth+d+h + "_csv | grep "+ stationCode +" > " + filelocation + "/UMOSTreating/" + sYear+secondmonth+d+h + "_csv")
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
    else:
        month = genday[0]
        Day = genday[1:]
        for m in molecule:
            for sub in os.listdir("rarc/operation.umos.aq.prevision.csv."+m.lower()+"sp3"):
                for d in Day:
                    for h in modelHourList:
                        if sub == sYear+month+d+h+"_csv":
                            os.system("cat " + filelocation + "/rarc/operation.umos.aq.prevision.csv." + m.lower() + "sp3/" + sYear+month+d+h + "_csv | grep "+ stationCode +" > " + filelocation + "/UMOSTreating/" + sYear+month+d+h + "_csv")
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
    # for post 2017
    if datesplit is not False:
        if isinstance(genday, tuple):
            firstmonth = genday[0][0]
            firstmonthdays = genday[0][1:]
            for h in modelHourList:
                for mol in moleculeList:
                    for d in firstmonthdays:
                        os.system(
                            "cmcarc -x 'prevision.csv/" + mol.lower() + "sp3.*' -f " + filelocation + "/rarc/operation.umos.aq.prevision/" + sYear + firstmonth + d + h + "_")
            secondmonth = genday[1][0]
            secondmonthdays = genday[1][1:]
            for h in modelHourList:
                for mol in moleculeList:
                    for d in secondmonthdays:
                        os.system(
                            "cmcarc -x 'prevision.csv/" + mol.lower() + "sp3.*' -f " + filelocation + "/rarc/operation.umos.aq.prevision/" + sYear + secondmonth + d + h + "_")
        else:
            month = genday[0]
            Day = genday[1:]
            for h in modelHourList:
                for mol in moleculeList:
                    for d in Day:
                        os.system(
                            "cmcarc -x 'prevision.csv/" + mol.lower() + "sp3.*' -f " + filelocation + "/rarc/operation.umos.aq.prevision/" + sYear + month + d + h + "_")
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
        print("UMOS Config sFiles Saved")


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


