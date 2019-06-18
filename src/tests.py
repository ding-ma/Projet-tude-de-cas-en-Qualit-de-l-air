import os
import sqlite3 as sql
import time
from datetime import date, timedelta

start = time.clock()

sqlTimedict = {
    "00": (210000, 220000, 230000, 0, 10000, 20000),
    "06": (30000, 40000, 50000, 60000, 70000, 80000),
    "12": {"90000", "100000", "110000", "120000", "130000", "140000"},
    "18": (150000, 160000, 170000, 180000, 190000, 200000)
}

userInputDict = {
    "210000": "00",
    "220000": "00",
    "230000": "00",
    "0": "00",
    "10000": "00",
    "20000": "00",
}
for i in range(3, 21):
    if 3 <= i <= 8:
        userInputDict[str(i) + "0000"] = "06"
    if 9 <= i <= 14:
        userInputDict[str(i) + "0000"] = "12"
    if 15 <= i <= 20:
        userInputDict[str(i) + "0000"] = "18"

sYear= 2019
sMonth = 6
sDay = 11
eYear = 2019
eMonth = 6
eDay = 14
sDate = date(sYear,sMonth,sDay)
eDate = date(eYear,eMonth,eDay)
delta1 = eDate-sDate
lstfile = []
lstdays = []
linuxpath = "/fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/ProjetQA/rarc/operation.observations.dbase.surface.airnow/"
windowspath = "sql\\"
for i in range(delta1.days+2):
    e=sDate+timedelta(days=i)
    lstdays.append(e)
    for a in os.listdir(windowspath):
        if a.startswith(e.strftime("%Y%m%d")):
            lstfile.append(a)


species = ["1","2", "3"]
stationID = "50128"
templst = []
for s in species:
    file = open("output/OBS_" + s + ".csv", "w+")
    file.write("Date,Time,Value\n")
    for d in lstdays[:-1]:  # skips last date, but lstfile contains it so it reads it. we just need the last 3h of the eDate in the last file
        for l in lstfile:
            connection = sql.connect(windowspath+l)
            c = connection.cursor()
            c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.header)")
            c.execute("SELECT _rowid_,* FROM main.header WHERE id_stn LIKE '%50128%'")
            idObslst = []
            for i in c.fetchall():
                if i[6] == int(d.strftime("%Y%m%d")):  # range of dates
                    #print("TIME: " + str(i[7])+" DATE: "+d.strftime("%Y%m%d"))
                    c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.data)")
                    c.execute("SELECT _rowid_,* FROM main.data WHERE id_obs =" + str(i[1]) + " AND species =" + s)
                    for p in c.fetchall():
                        #print(d.strftime("%Y%m%d") + "," + str(i[7])+","+str((p[8]))+","+s)
                        templst.append(d.strftime("%Y%m%d") + "," + str(i[7])+","+str((p[8]))+","+s+"\n")

    for t in templst:
        file.write(t)
    templst.clear()

end = time.clock()
print(end-start)