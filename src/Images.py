import calendar
import os
import re
import shutil
from datetime import date, timedelta

import Gemmach as Gm

filelocation = Gm.filelocation

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


bothCheked = 0
def modelCheckbox(h_00, h_12):
    global modelHour
    global modelHourBash
    global bothCheked
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


def time(sTime, eTime):
    global formattedSelectedTimeWithComma
    global formattedSelectedTimeWithSpace
    global sTimeBash
    sTimeBash = sTime
    #gets index then generates a list within the index
    sIndex = Gm.hours.index(sTime)
    eIndex = Gm.hours.index(eTime)
    unformattedSelectedTime = ""
    for timeList in range(eIndex - sIndex + 1):
        unformattedSelectedTime += Gm.hours[sIndex + timeList]
    # for every 3 character
    formattedSelectedTimeWithComma = ','.join(
        unformattedSelectedTime[i:i + 3] for i in range(0, len(unformattedSelectedTime), 3))
    formattedSelectedTimeWithSpace = ' '.join(
        unformattedSelectedTime[i:i + 3] for i in range(0, len(unformattedSelectedTime), 3))


def particuleCheckBox(O3, NO2, others, PM25):
    global formattedParticuleString
    global particulelst
    particulelst = []
    O3 = int(O3)
    NO2 = int(NO2)
    PM25 = int(PM25)
    stringO3 = ""
    stringNO2 = ""
    stringPM25 = ""
    if O3 is 1:
        stringO3 = "o3"
        particulelst.append(stringO3)
    if NO2 is 1:
        stringNO2 = "no2"
        particulelst.append(stringNO2)
    if PM25 is 1:
        stringPM25 = "af"
        particulelst.append(stringPM25)
    unformattedParticuleString = stringO3 + stringNO2 + stringPM25 + others
    # for every 2 character, add space
    formattedParticuleString = ' '.join(
        unformattedParticuleString[i:i + 2] for i in range(0, len(unformattedParticuleString), 2))


#east,east@coast@zoom,north@america,north@america@gemmach,west
def locationCheckBox(East, EastZoom,NA,NAGem,West,QcOnt):
    global locationlst
    global rarcString
    East = int(East)
    EastZoom = int(EastZoom)
    NA = int(NA)
    NAGem = int(NAGem)
    West = int(West)
    QcOnt = int(QcOnt)
    strEast = ""
    strEastZoom = ""
    strNA = ""
    strNAGem = ""
    strWest = ""
    strQCOnt = ""
    if East is 1:
        strEast = "east,"
    if EastZoom is 1:
        strEastZoom = "east@coast@zoom,"
    if NA is 1:
        strNA = "north@america,"
    if NAGem is 1:
        strNAGem = "north@america@gemmach,"
    if West is 1:
        strWest = "west,"
    if QcOnt is 1:
        strQCOnt = "quebec@ontario"
    rarcString = strEast + strEastZoom+strNA+strNAGem+strWest+strQCOnt
    tempList = re.split(",", rarcString)
    locationlst = tempList[:-1]


def RarcFile():
    file = open("image", "w")
    file.write(
        "target = " + filelocation + "/rarc\n"
                                     "filter = copy\n"
                                     "postprocess = nopost\n"
                                     "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.images.chronos\n"
        "ext = " + rarcString +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("Gemmach Image Config Files Saved")


def UMOSRarcFile():
    file = open("imageUMOS", "w")
    file.write(
        "target = " + filelocation + "/rarc\n"
                                     "filter = copy\n"
                                     "postprocess = nopost\n"
                                     "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.images.umoscr\n"
        "ext = " + rarcString +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("UMOS Image Config Files Saved")

def generateImage():
    molecules = particulelst
    modelhourlist = re.split(",", modelHour)
    if isinstance(genday,tuple):
        firstmonth = genday[0][0]
        firstmonthdays = genday[0][1:]
        for day in firstmonthdays:
            for location in locationlst:
                for m in molecules:
                    for h in modelhourlist:
                        os.system("cmcarc -x "+sYear+firstmonth+day+h+"_054_GM_"+location+"_I_GEMMACH_"+m+"@sfc@001.* -f "+os.getcwd()+ "/rarc/operation.images.chronos/"+sYear+firstmonth+day+h+"_"+location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd()+"/imgTemp")

                        print("extracted: "+m+location+h)
                        purge(os.getcwd(),sYear+firstmonth+day+h+"_054_GM_"+location+"_I_GEMMACH_"+m+"@sfc@001.*")
                        print("generating gif: "+m+location+h)

                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + firstmonth + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001* "
                            + filelocation + "/output/GEM__" + sYear + firstmonth + day + h +"_"+ m+"_" + location + ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir end months")

        month = genday[1][0]
        secondmonthdays = genday[1][1:]
        for day in secondmonthdays:
            for location in locationlst:
                for m in molecules:
                    for h in modelhourlist:
                        os.system(
                            "cmcarc -x " + sYear + month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.* -f " + os.getcwd() + "/rarc/operation.images.chronos/" + sYear + month + day + h + "_" + location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd() + "/imgTemp")

                        print("extracted: " + m + location + h)
                        purge(os.getcwd(),
                              sYear + month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.*")
                        print("generating gif: " + m + location + h)

                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001* "
                            + filelocation + "/output/GEM__" + sYear + month + day + h + "_" + m + "_" + location + ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir start month")
    else:
        Month = genday[0]
        Day = genday[1:]
        for day in Day:
            for location in locationlst:
                for m in molecules:
                    for h in modelhourlist:
                        os.system(
                            "cmcarc -x " + sYear + Month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.* -f " + os.getcwd() + "/rarc/operation.images.chronos/" + sYear + Month + day + h + "_" + location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd() + "/imgTemp")

                        print("extracted: " + m + location + h)
                        purge(os.getcwd(),
                              sYear + Month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.*")
                        print("generating gif: " + m + location + h)

                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + Month + day + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001* "
                            + filelocation + "/output/GEM__" + sYear + Month + day + h + "_" + m + "_" + location + ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir start month")
    print("\nJob done, see folder-->" + filelocation+"/output")


def generateUMOSImage(t):
    molecules = particulelst
    modelhourlist = re.split(",", modelHour)
    if isinstance(genday,tuple):
        firstmonth = genday[0][0]
        firstmonthdays = genday[0][1:]
        for location in locationlst:
            for day in firstmonthdays:
                for m in molecules:
                    for h in modelhourlist:
                        os.system("cmcarc -x "+sYear+firstmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+".* -f "+os.getcwd()+ "/rarc/operation.images.umoscr/"+sYear+firstmonth+day+h+"_"+location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd()+"/imgTemp")

                        print("extracted: "+m+location+h)
                        purge(os.getcwd(),sYear+firstmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+".*")
                        print("generating gif: "+m+location+h)
                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" +sYear+firstmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+"* "
                            + filelocation + "/output/UMOS__" + sYear + firstmonth + day + h + "_"+m+"_" + location +t+ ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir end month")
        secondmonth = genday[1][0]
        secondmonthdays = genday[1][1:]
        for location in locationlst:
            for day in secondmonthdays:
                for m in molecules:
                    for h in modelhourlist:
                        os.system("cmcarc -x "+sYear+secondmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+".* -f "+os.getcwd()+ "/rarc/operation.images.umoscr/"+sYear+secondmonth+day+h+"_"+location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd()+"/imgTemp")

                        print("extracted: "+m+location+h)
                        purge(os.getcwd(),sYear+secondmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+".*")
                        print("generating gif: "+m+location+h)
                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" +sYear+secondmonth+day+h+"_054_UA_"+location+"_I_UMOS@GEMMACH_"+m+t+"* "
                            + filelocation + "/output/UMOS__" + sYear + secondmonth + day + h + "_"+m+"_" + location +t+ ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir start month")
    else:
        Month = genday[0]
        Day = genday[1:]
        for location in locationlst:
            for day in Day:
                for m in molecules:
                    for h in modelhourlist:
                        os.system(
                            "cmcarc -x " + sYear + Month + day + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + ".* -f " + os.getcwd() + "/rarc/operation.images.umoscr/" + sYear + Month + day + h + "_" + location)

                        def purge(dir, pattern):
                            for f in os.listdir(dir):
                                if re.search(pattern, f):
                                    shutil.move(f, os.getcwd() + "/imgTemp")

                        print("extracted: " + m + location + h)
                        purge(os.getcwd(),
                              sYear + Month + day + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + ".*")
                        print("generating gif: " + m + location + h)
                        os.system(
                            "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + Month + day + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + "* "
                            + filelocation + "/output/UMOS__" + sYear + Month + day + h + "_" + m + "_" + location + t + ".gif")
                        shutil.rmtree("imgTemp")
                        os.mkdir("imgTemp")
                        print("remaking dir start month")
    print("\nJob done, see folder-->" + filelocation+"/output")

