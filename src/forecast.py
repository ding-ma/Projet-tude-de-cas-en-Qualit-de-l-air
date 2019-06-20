import datetime
import os
import re
import sqlite3 as sql
from datetime import timedelta

import Gemmach as Gm

filelocation = Gm.filelocation

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
    if sMonth in Gm.oddMonths:
        return Gm.days[1:-2]
    if sMonth in Gm.evenMonths:
        return Gm.days[1:-3]
    if leap is True and int(sMonth) is 2:
        return Gm.days[1:-4]
    if leap is False and int(sMonth) is 2:
        return Gm.days[1:-5]
    ###

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
    elif eMonth in Gm.oddMonths and int(eDay) > 31:
        dateErrors()
    elif eMonth in Gm.evenMonths and int(eDay) > 30:
        dateErrors()
    elif sMonth > eMonth:
        dateErrors()
    elif sMonth == eMonth and sDay > eDay:
        dateErrors()
    else:
        print("End Date: " + eYear, eMonth, eDay)


def dateErrors():
    raise Exception("Date format error, please check what you have entered")


def time(sTime, eTime):
    global formattedSelectedTimeWithComma
    #gets index then generates a list within the index
    sIndex = Gm.hours.index(sTime)
    eIndex = Gm.hours.index(eTime)
    unformattedSelectedTime = ""
    for timeList in range(eIndex - sIndex + 1):
        unformattedSelectedTime += Gm.hour24[sIndex + timeList]
    # for every 3 character
    formattedSelectedTimeWithComma = ','.join(
        unformattedSelectedTime[i:i + 2] for i in range(0, len(unformattedSelectedTime), 2))


def rarcFile():
    file = open("forecast", "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.forecasts.aqhi.basedonnees\n"
        "ext = observation.db"
        "\nheure = " + formattedSelectedTimeWithComma +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("Forecast Config Files Saved")

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


fstdDict = {
    "O3": "1",
    "N2": "2",
    "AF": "3",
    "AC": "4",
    "S2": "5",
    "CO": "7",
    "NO": "8"
}

lstofSpecies = []
def generateFromDB(stationID):
    sDate = datetime.date(int(sYear),int(sMonth),int(sDay))
    eDate = datetime.date(int(eYear),int(eMonth),int(eDay))
    delta = eDate-sDate
    daylst = []
    for i in range(delta.days + 1):
        a = sDate + timedelta(days=i)
        daylst.append(a)
    for d in daylst:
        date = str(d.strftime("%Y%m%d"))
        lstofSpeciesFST = formattedParticuleString.split(" ")
        for et in lstofSpeciesFST:
            lstofSpecies.append(fstdDict[et])
        sqlfilelst = []
        path = "/rarc/operation.forecasts.aqhi.basedonnees/"
        for a in os.listdir(filelocation + path):
            if a.startswith(date) and a.endswith("_observation.db"):
                sqlfilelst.append(a)
        templst = []
        for e,s in zip(lstofSpecies, lstofSpeciesFST):
            print("Extracting " + s + " from database...")
            for sqlfile in sorted(sqlfilelst):
                connection = sql.connect(filelocation + path + sqlfile)
                c = connection.cursor()
                # forcast
                # c.execute("SELECT type,name,sql,tbl_name FROM main.sqlite_master;")
                # c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.forecast WHERE station LIKE '%"+station+"%' ESCAPE '\\' AND specie LIKE '%"+species+"%' ESCAPE '\\' );")
                # c.execute("SELECT _rowid_,* FROM main.forecast WHERE station LIKE '%"+station+"%' ESCAPE '\\' AND specie LIKE '%"+species+"%' ESCAPE '\\' ORDER BY date ASC;")

                # for obs
                c.execute("SELECT COUNT(*) FROM (SELECT _rowid_,* FROM main.observation );")
                c.execute(
                    "SELECT _rowid_,* FROM main.observation WHERE station LIKE " + stationID + " AND (specie LIKE " + e + ") ORDER BY _rowid_ ASC;")
                for i in c.fetchall():
                    d = datetime.datetime.utcfromtimestamp(i[3]).strftime('%Y%m%d')
                    hour = datetime.datetime.utcfromtimestamp(i[3]).strftime('%H')
                    concentration = str(i[5])
                    writestr = d + "," + hour + "," + concentration
                    templst.append(writestr)

            print("Writing to file\n")
            file = open("output/OBS__ID" + stationID + "__" + date + "_" + s + ".csv", "w+")
            # (11, 10102, 8, 1559984400, 25, 5.0)
            file.write("Date,Hour,Value\n")
            for l in templst:
                file.write(l + "\n")
            templst.clear()
    print("Job done, see folder-->" + filelocation + "/output\n")