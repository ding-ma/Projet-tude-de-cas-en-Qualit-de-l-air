import os
import sqlite3 as sql
from datetime import date, timedelta

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
eDay = 11
sDate = date(sYear,sMonth,sDay)
eDate = date(eYear,eMonth,eDay)
delta1 = eDate-sDate
lstfile = []
for i in range(delta1.days+2):
    e=sDate+timedelta(days=i)
    print(e)
    for a in os.listdir("sql"):
        if a.startswith(e.strftime("%Y%m%d")):
            lstfile.append(a)

for l in lstfile:
    for s in ["1","2", "3"]:
        stationID = "50128"
        species = "1"
        connection = sql.connect("sql\\"+l)
        c = connection.cursor()
        c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.header)")
        c.execute("SELECT _rowid_,* FROM main.header WHERE id_stn LIKE '%50128%'")
        idObslst = []
        for i in c.fetchall():
            if i[6] == int(sDate.strftime("%Y%m%d")):  # range of dates
                print("TIME: " + str(i[7]))
                c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.data)")
                c.execute("SELECT _rowid_,* FROM main.data WHERE id_obs =" + str(i[1]) + " AND species =" + s)
                for p in c.fetchall():
                    print(s+"--"+str(p[8]))
