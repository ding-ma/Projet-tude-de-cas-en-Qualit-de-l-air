import csv
import glob
import os
import re
import shutil
from datetime import date, timedelta, datetime

import pandas as pd

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
    if eDate.timetuple()<date(2017,1,5).timetuple():
        return False


lstdates = []
def countdates():
    delta = eDate - sDate
    for i in range(delta.days + 1):
        d = sDate + timedelta(days=i)
        lstdates.append(d)

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


def particuleCheckBoxAndTime(O3, NO2, PM25):
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
    return re.split(" ", formattedParticuleString)


def getDataAtLocationPre2017(locationID, molescules):
    stationCode = referenceDict[locationID]
    for m in molescules:
        print("extracting: " + m.lower())
        for sub in os.listdir("rarc/operation.umos.aq.prevision.csv."+m.lower()+"sp3"):
            for date in lstdates:
                for h in modelHourList:
                    if sub == str(date.year) + str(date.strftime("%m")) + str(date.strftime("%d"))+h+"_csv":
                        os.system("cat " + filelocation + "/rarc/operation.umos.aq.prevision.csv." + m.lower() + "sp3/"
                                  + str(date.year) + str(date.strftime("%m")) + str(date.strftime("%d")) +h + "_csv | grep "+ stationCode +" > "
                                  + filelocation + "/UMOSTreating/"  + str(date.year) + str(date.strftime("%m")) + str(date.strftime("%d")) +h + "_csv")
        for untreated in os.listdir("UMOSTreating"):
            if os.stat("UMOSTreating/" + untreated).st_size > 500:
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


def extractwithCMCARC(particules):
    for mol in particules:
        for h in modelHourList:
            print("extracting: " + mol.lower())
            for date in lstdates:
                os.system(
                    "cmcarc -x 'prevision.csv/" + mol.lower() + "sp3.*' -f " + filelocation + "/rarc/operation.umos.aq.prevision/" + str(
                        date.year) + str(date.strftime("%m")) + str(date.strftime("%d")) + h + "_")


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

subconverterdict = {
    "p2":"AF",
    "o3":"O3",
    "n2":"NO2"
}


def toExcel(name):
    df = pd.read_csv("output/"+name)
    df.drop(['Lat', 'Lon', 'Vertical', 'Var'], axis=1, inplace=True)
    dateorg_lst = df['Date_Orig'].tolist()
    datevalid_list = df['Date_Valid'].tolist()
    values_lst = df['Value'].tolist()
    timelst = []
    orglst = []
    valst = []
    for org, val in zip(dateorg_lst, datevalid_list):
        orgchanged = datetime.strptime(org, "%Y-%m-%d%H:%M:%S").strftime("%Y%m%d%H")
        valchanged = datetime.strptime(val, "%Y-%m-%d%H:%M:%S").strftime("%Y%m%d")
        hchanged = datetime.strptime(val, "%Y-%m-%d%H:%M:%S").strftime("%H")
        orglst.append(orgchanged)
        valst.append(valchanged)
        timelst.append(hchanged)
    # ['Model Time', 'Date', 'Time', 'Value']
    #{'Model Time': orglst, 'Date': valst, 'Time': timelst, 'Values': values_lst}
    dfnew = pd.DataFrame()
    dfnew.to_excel("excel_output/"+name[:-4]+".xlsx", engine="xlsxwriter", index=False, index_label=False)

def getDataAtLocation(locationID):
    try:
        stationCode = referenceDict[locationID]
        for sub in os.listdir("prevision.csv"):
            for file in os.listdir("prevision.csv/" + sub):
                os.system(
                    "cat " + filelocation + "/prevision.csv/" + sub + "/" + file + "| grep " + stationCode + " > " + filelocation + "/UMOSTreating/" + file + sub)
            for untreated in os.listdir("UMOSTreating"):
                date = untreated.split("_")[0]
                filename = date + "_UMOS_" + subconverterdict[sub[:2]] + "_" + Gm.returnName(locationID) + ".csv"
                # prevents having empty files
                if os.stat("UMOSTreating/" + untreated).st_size > 500:
                    with open("UMOSTreating/" + untreated, "r") as infile, open(
                            "output/"+filename, "w") as outfile:
                        # UMOS__ID"+locationID +"__"+ untreated + ".csv",'w'
                        outfile.write("Date_Orig,Date_Valid,Code_Stn(ID),Lat,Lon,Vertical,Var,Value\n")
                        for line in infile:
                            withcomma = line.replace('|', ',')
                            withoutspace = withcomma.replace(" ", "")
                            changeName = withoutspace.replace(stationCode, locationID)
                            outfile.write(changeName)
                toExcel(filename)

        print("\nJob done, see folder for csv file-->" + filelocation + "/output")
        print("\nJob done, see folder for excel file-->" + filelocation + "/excel_output")
        removeAllfile(r'' + filelocation + "/UMOSTreating")
        shutil.rmtree("prevision.csv")
    except KeyError:
        print("The station chosen does not have a UMOS code.")
