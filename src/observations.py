import csv
import os
import re
import sqlite3 as sql
import time
from datetime import date, timedelta, datetime
from sys import platform

import pandas as pd

import BashModels as Bm

filelocation = Bm.filelocation

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
    listadys()


if platform =="win32":
    path = "M:\Projet-tude-de-cas-en-Qualit-de-l-air\src\sql"
else:
    path = filelocation+"/rarc/operation.observations.dbase.surface.airnow/"

lstfile = []
lstdays = []

fstdDict = {
    "O3": "1",
    "N2": "2",
    "AF": "3",
    "AC": "4",
    "S2": "5",
    "CO": "7",
    "NO": "8"
}

def listadys():
    lstdays.clear()
    lstfile.clear()
    delta1 = eDate - sDate
    for i in range(delta1.days + 2):
        e = sDate + timedelta(days=i)
        lstdays.append(e)
        if os.path.exists(path):
            for a in os.listdir(path):
                if a.startswith(e.strftime("%Y%m%d")):
                    lstfile.append(a)
    rarcFile()


def rarcFile():
    days = timedelta(days=1)
    file = open("observations", "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "+sDate.strftime("%Y,%m,%d")+","+
        # end
        (eDate + days).strftime("%Y,%m,%d")+
        "\nbranche = operation.observations.dbase.surface.airnow\n"
        "ext = ***"
        "\nheure = 00,06,12,18"
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("Observation Config File Saved!")

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


AQHI_path = "/fs/home/fs1/ords/oth/airq_central/frc002/Data/CAS/Observations/Station/"
stationlst = []
datelst = []
hourlst = []
O3lst = []
NO2lst = []
PM25lst = []

def getQuickData(stationID):
    stationName = Bm.returnName(stationID)
    if os.path.exists(AQHI_path + stationID) is True:
        for files in sorted(
                os.listdir(AQHI_path + stationID)):
            for days in lstdays[:-1]:
                if files.endswith(stationID + "_" + days.strftime("%Y%m%d") + ".csv"):
                    f = open(AQHI_path + stationID + "/" + files, "r")
                    csvFile = list(csv.reader(f))
                    for z in range(len(csvFile)):
                        row = csvFile[z]
                        if row != ['station', 'Date', 'UTC', 'AQHI', 'O3', 'NO2', 'PM2.5', 'PM10', 'SO2', 'H2S',
                                   'CO',
                                   'NO', 'TRS']:
                            station = row[0]
                            stationlst.append(station)
                            date = row[1]
                            datelst.append(date)
                            hour = row[2]
                            hourlst.append(hour)
                            NO2 = row[5]
                            NO2lst.append(NO2)
                            O3 = row[4]
                            O3lst.append(O3)
                            PM25 = row[6]
                            PM25lst.append(PM25)
    else:
        print("This station does not exist in db-AQHI, try using the archives...")

    # use this line when pandas will be updated on the server:
    # dfNO['Date(DD/MM/YYYY)'] = pd.to_datetime(dfNO['Date(DD/MM/YYYY)']).dt.strftime("%Y%m%d")

    formatteddatelst = []
    formattedhourlst = []

    for day in datelst:
        d = datetime.strptime(day, "%Y-%m-%d").strftime("%Y%m%d")
        formatteddatelst.append(d)

    for hour in hourlst:
        h = datetime.strptime(hour, "%H:%M:%S").strftime("%H")
        formattedhourlst.append(h)

    columnheader = ["Date", "Hour(Z)", "Value"]
    if "AF" in formattedParticuleString:
        dfPM = pd.DataFrame(list(zip(formatteddatelst, formattedhourlst, PM25lst)), columns=columnheader)
        dfPM.to_csv("output_csv/" + sDate.strftime("%Y%m%d")+"_" + eDate.strftime("%Y%m%d") +"_OBS_AF_" + stationName + ".csv", sep=",", index=False)
        dfPM.to_excel("output_excel/" + sDate.strftime("%Y%m%d") +"_"+ eDate.strftime("%Y%m%d") +"_OBS_AF_" + stationName + ".xlsx", engine="xlsxwriter")

    if "N2" in formattedParticuleString:
        dfNO = pd.DataFrame(list(zip(formatteddatelst, formattedhourlst, NO2lst)), columns=columnheader)

        dfNO.to_csv("output_csv/" + sDate.strftime("%Y%m%d")+"_" + eDate.strftime("%Y%m%d") +"_OBS_N2_" + stationName+".csv", sep=",",index=False)
        dfNO.to_excel("output_excel/"+ sDate.strftime("%Y%m%d")+"_" + eDate.strftime("%Y%m%d") +"_OBS_N2_" + stationName+ ".xlsx", engine="xlsxwriter")

    if "O3" in formattedParticuleString:
        dfO3 = pd.DataFrame(list(zip(formatteddatelst, formattedhourlst, O3lst)), columns=columnheader)
        dfO3.to_csv("output_csv/"  + sDate.strftime("%Y%m%d")+"_" + eDate.strftime("%Y%m%d") +"_OBS_O3_" + stationName+".csv", sep=",", index=False)
        dfO3.to_excel("output_excel/" + sDate.strftime("%Y%m%d")+"_" + eDate.strftime("%Y%m%d") +"_OBS_O3_" + stationName+ ".xlsx", engine="xlsxwriter")

    stationlst.clear()
    datelst.clear()
    hourlst.clear()
    NO2lst.clear()
    O3lst.clear()
    PM25lst.clear()
    formatteddatelst.clear()
    formattedhourlst.clear()
    print("\nJob done, see folder for csv file-->" + filelocation + "/output_csv")
    print("\nJob done, see folder for excel file-->" + filelocation + "/output_excel")


lstofSpecies = []
def generateFromDB(stationID):
    lstofSpeciesFST = formattedParticuleString.split(" ")
    lstofSpecies.clear()
    for et in lstofSpeciesFST:
        lstofSpecies.append(fstdDict[et])
    templst = []
    for s,sp in zip(lstofSpecies,lstofSpeciesFST):
        for d in lstdays[:-1]:  # skips last date, but lstfile contains it so it reads it. we just need the last 3h of the eDate in the last file
            for l in lstfile:
                print("searching db: "+ l)
                connection = sql.connect(path+l)
                c = connection.cursor()
                c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.header);")
                c.execute("SELECT _rowid_,* FROM main.header WHERE id_stn LIKE '%0"+stationID+"%'")
                for i in c.fetchall():
                    if i[6] == int(d.strftime("%Y%m%d")):  # range of dates
                        print("TIME: " + str(i[7])+" DATE: "+d.strftime("%Y%m%d"))
                        c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.data)")
                        c.execute("SELECT _rowid_,* FROM main.data WHERE id_obs =" + str(i[1]) + " AND species =" + s)
                        for p in c.fetchall():
                            #str(int(i[7]/10000))
                            if int(i[7]/10000) <10:
                                pre10 = d.strftime("%Y%m%d") + ",0" + str(int(i[7]/10000))+","+str((p[8]))+"\n"
                                templst.append(pre10)
                            else:
                                post10 = d.strftime("%Y%m%d") + "," + str(int(i[7] / 10000)) + "," + str((p[8])) + "\n"
                                templst.append(post10)
        bb = sorted(templst)
        if len(bb) <1:
            print(Bm.FAIL + sp + " NOT found at station " + stationID + Bm.ENDC)
            if len(lstofSpeciesFST)>1:
                print("Trying other selected pollutants...")
            time.sleep(2)
            continue
        print("Writing to file")
        fileName = sDate.strftime("%Y%m%d") + "_" + eDate.strftime("%Y%m%d") +"_OBS_" + sp +"_" + Bm.returnName(stationID) + ".csv"
        # open("output/OBS__ID" + stationID + "__" + sp + "__START" + sDate.strftime("%Y%m%d") + "__END" + eDate.strftime("%Y%m%d") + ".csv", "w+")
        file = open("output_csv/" +fileName, "w+")
        file.write("Date,Time(Z),Value\n")
        for t in bb:
            file.write(t)
        templst.clear()
        file.close()
        Bm.generateExcel(fileName)
        #raise Exception(Gm.FAIL+sp+" NOT found at station " + stationID+ Gm.ENDC)
    print("\nJob done, see folder for csv file-->" + filelocation + "/output_csv")
    print("\nJob done, see folder for excel file-->" + filelocation + "/output_excel")