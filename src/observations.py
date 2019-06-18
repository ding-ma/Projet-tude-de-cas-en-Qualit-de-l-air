import os
import re
import sqlite3 as sql
from datetime import date, timedelta
from sys import platform

import Gemmach as Gm

filelocation = Gm.filelocation

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
    path = "/fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetQA/rarc/operation.observations.dbase.surface.airnow/"

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
    delta1 = eDate - sDate
    for i in range(delta1.days + 2):
        e = sDate + timedelta(days=i)
        lstdays.append(e)
        for a in os.listdir(path):
            if a.startswith(e.strftime("%Y%m%d")):
                lstfile.append(a)
    rarcFile()


def rarcFile():
    file = open("observations", "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "+lstdays[0].strftime("%Y,%m,%d")+","+
        # end
        lstdays[-1].strftime("%Y,%m,%d")+
        "\nbranche = operation.observations.dbase.surface.airnow\n"
        "ext = ***"
        "\nheure = 00,06,12,18"
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")

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


lstofSpecies = []
def generateFromDB(stationID):
    lstofSpeciesFST = formattedParticuleString.split(" ")
    lstofSpecies.clear()
    for et in lstofSpeciesFST:
        lstofSpecies.append(fstdDict[et])
    templst = []
    for s,sp in zip(lstofSpecies,lstofSpeciesFST):
        file = open("output/OBS__ID"+stationID+"__" + sp +"__START"+sDate.strftime("%Y%m%d")+"__END"+eDate.strftime("%Y%m%d")+ ".csv", "w+")
        file.write("Date,Time,Value\n")
        for d in lstdays[:-1]:  # skips last date, but lstfile contains it so it reads it. we just need the last 3h of the eDate in the last file
            for l in lstfile:
                connection = sql.connect(path+l)
                c = connection.cursor()
                c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.header)")
                c.execute("SELECT _rowid_,* FROM main.header WHERE id_stn LIKE '%0"+stationID+"%'")
                for i in c.fetchall():
                    if i[6] == int(d.strftime("%Y%m%d")):  # range of dates
                        #print("TIME: " + str(i[7])+" DATE: "+d.strftime("%Y%m%d"))
                        c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.data)")
                        c.execute("SELECT _rowid_,* FROM main.data WHERE id_obs =" + str(i[1]) + " AND species =" + s)
                        for p in c.fetchall():
                            print("Value: "+str((p[8]))+","+sp +", H"+str(i[7]/10000))
                            templst.append(d.strftime("%Y%m%d") + "," + str(i[7]/10000)+","+str((p[8]))+"\n")
        for t in templst:
            file.write(t)
        templst.clear()
    print("Job done, see folder-->" + filelocation + "/output\n")