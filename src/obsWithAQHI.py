import csv
import os
from datetime import datetime, timedelta

import pandas as pd

startDate = datetime(2019, 5, 1)
endDate = datetime(2019, 5, 15)
listofDate = []
delta = endDate - startDate
for i in range(delta.days + 1):
    listofDate.append((startDate + timedelta(days=i)).strftime("%Y%m%d"))


stationlst = []
datelst = []
hourlst = []
O3lst = []
NO2lst = []
PM25lst = []
def getQuickData(stationID, polluant):
    if os.path.exists(
            "/fs/home/fs1/ords/oth/airq_central/frc002/Data/CAS/Observations/Station/" + stationID) is True:
        for files in sorted(
                os.listdir("/fs/home/fs1/ords/oth/airq_central/frc002/Data/CAS/Observations/Station/" + stationID)):
            for days in listofDate:
                if files.endswith(stationID + "_" + days + ".csv"):
                    f = open(
                        "/fs/home/fs1/ords/oth/airq_central/frc002/Data/CAS/Observations/Station/" + stationID + "/" + files,
                        "r")
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

    # use this line when pandas will be updated on the server:
    # dfNO['Date(DD/MM/YYYY)'] = pd.to_datetime(dfNO['Date(DD/MM/YYYY)']).dt.strftime("%Y%m%d")

    formatteddatelst = []
    formattedhourlst = []

    for day in datelst:
        d = datetime.strptime(day,"%Y-%m-%d").strftime("%Y%m%d")
        formatteddatelst.append(d)

    for hour in hourlst:
        h = datetime.strptime(hour, "%H:%M:%S").strftime("%H")
        formattedhourlst.append(h)

    columnheader = ["Date","Hour(Z)","Value"]
    if polluant is 1:
        dfPM = pd.DataFrame(list(zip(formatteddatelst,formattedhourlst,PM25lst)),columns=columnheader)
        dfPM.to_csv("monthfiles/" + startDate.strftime("%Y%m") + "_" + stationID + "PM25.csv", sep=",",
                   index=False)
        dfPM.to_excel("monthfiles/"+startDate.strftime("%Y%m") + "_" + stationID + "PM25.xlsx", engine="xlsxwriter")

    if polluant is 2:
        dfNO = pd.DataFrame(list(zip(formatteddatelst,formattedhourlst,NO2lst)),columns=columnheader)

        dfNO.to_csv("monthfiles/" + startDate.strftime("%Y%m") + "_" + stationID + "NO2.csv", sep=",",
                   index=False)
        dfNO.to_excel("monthfiles/" + startDate.strftime("%Y%m") + "_" + stationID + "NO2.xlsx", engine="xlsxwriter")

    if polluant is 3:
        dfO3 = pd.DataFrame(list(zip(formatteddatelst,formattedhourlst,O3lst)),columns=columnheader)
        dfO3.to_csv("monthfiles/" + startDate.strftime("%Y%m") + "_" + stationID + "O3.csv", sep=",", index=False)
        dfO3.to_excel("monthfiles/" + startDate.strftime("%Y%m") + "_" + stationID + "O3.xlsx", engine="xlsxwriter")

    stationlst.clear()
    datelst.clear()
    hourlst.clear()
    NO2lst.clear()
    O3lst.clear()
    PM25lst.clear()
    formatteddatelst.clear()
    formattedhourlst.clear()


getQuickData("50128",2)

