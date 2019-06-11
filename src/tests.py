import datetime
import os
import sqlite3 as sql

import Gemmach as Gm

f =os.getcwd()
speciesDict = {
    "1":"O3",
    "2":"NO2",
    "3":"PM2.5",
    "4":"PM10",
    "5":"SO2",
    "6":"H2S",
    "7":"CO",
    "8":"NO",
    "9":"TRS",
    "10":"AQHI",
    "-":"ALL"
}

sqlfilelst = []
station = "50128"
enteredspecies = "-"
species = enteredspecies.replace(",", " OR specie LIKE ")
enteredate = "20190524"

t = "_observation.db"
path = "\\rarc\\operation.forecasts.aqhi.basedonnees\\"
for a in os.listdir(f+path):
    if a.startswith(enteredate) and a.endswith(t):
        sqlfilelst.append(a)


templst = []
for e in enteredspecies.split(","):
    for sqlfile in sqlfilelst:
        connection = sql.connect(f+path+sqlfile)
        c = connection.cursor()
    #forcast
    # c.execute("SELECT type,name,sql,tbl_name FROM main.sqlite_master;")
    # c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.forecast WHERE station LIKE '%"+station+"%' ESCAPE '\\' AND specie LIKE '%"+species+"%' ESCAPE '\\' );")
    # c.execute("SELECT _rowid_,* FROM main.forecast WHERE station LIKE '%"+station+"%' ESCAPE '\\' AND specie LIKE '%"+species+"%' ESCAPE '\\' ORDER BY date ASC;")

        #for obs
        c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.observation );")
        if species is "-":
            c.execute(
                "SELECT _rowid_,* FROM main.observation WHERE station LIKE " + station + " ORDER BY _rowid_ ASC;")
        else:
            c.execute("SELECT _rowid_,* FROM main.observation WHERE station LIKE "+station+" AND (specie LIKE "+e+") ORDER BY _rowid_ ASC;")
        for i in c.fetchall():
            converted = speciesDict[str(i[2])]
            stationName = Gm.returnName(str(i[1]))
            date = datetime.datetime.utcfromtimestamp(i[3]).strftime('%Y%m%d')
            hour = datetime.datetime.utcfromtimestamp(i[3]).strftime('%H')
            concentration = str(i[5])
            writestr = str(i[1])+","+date+","+hour+","+converted+","+concentration
            templst.append(writestr)

    file = open("OBS__ID"+station+"__"+enteredate+"_"+speciesDict[e]+".csv", "w+")
    # (11, 10102, 8, 1559984400, 25, 5.0)
    file.write("Location(ID),Date,Hour,Molecule,Concentration\n")
    for l in templst:
        file.write(l+"\n")
    templst.clear()
