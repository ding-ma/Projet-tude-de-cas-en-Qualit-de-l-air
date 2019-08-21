import os
import re
import shutil
from datetime import date, timedelta

import BashModels as Bm

filelocation = Bm.filelocation


# formats the start date
def inputStartDate(sD):
    global sYear
    global sMonth
    global sDay
    global sDate
    # splits the entry into a tuple
    unformatattedDate = re.split("/", sD)
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]
    sDate = date(int(sYear), int(sMonth), int(sDay))


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
    generateDatelst()


lstDate = []


def generateDatelst():
    lstDate.clear()
    delta = eDate - sDate
    for i in range(delta.days + 1):
        date = sDate + timedelta(days=i)
        lstDate.append(date)


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
    # gets index then generates a list within the index
    sIndex = Bm.hours.index(sTime)
    eIndex = Bm.hours.index(eTime)
    unformattedSelectedTime = ""
    for timeList in range(eIndex - sIndex + 1):
        unformattedSelectedTime += Bm.hours[sIndex + timeList]
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


# east,east@coast@zoom,north@america,north@america@gemmach,west
def locationCheckBox(East, EastZoom, NA, NAGem, West, QcOnt):
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
        strQCOnt = "quebec@ontario,"
    rarcString = strEast + strEastZoom + strNA + strNAGem + strWest + strQCOnt
    # east,east@coast@zoom,north@america,north@america@gemmach,west,quebec@ontario,
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
        "ext = east,east@coast@zoom,north@america,north@america@gemmach,west,quebec@ontario," +
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
        "ext = east,east@coast@zoom,north@america,north@america@gemmach,west,quebec@ontario," +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("UMOS Image Config Files Saved")


def generateImage():
    molecules = particulelst
    modelhourlist = re.split(",", modelHour)
    for day_obj in lstDate:
        for location in locationlst:
            for m in molecules:
                for h in modelhourlist:
                    if location == "quebec@ontario":
                        continue
                    os.system(
                        "cmcarc -x " + sYear + day_obj.strftime("%m") + day_obj.strftime(
                            "%d") + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.* -f " + os.getcwd() + "/rarc/operation.images.chronos/" + sYear + day_obj.strftime(
                            "%m") + day_obj.strftime("%d") + h + "_" + location)

                    def purge(dir, pattern):
                        for f in os.listdir(dir):
                            if re.search(pattern, f):
                                shutil.move(f, os.getcwd() + "/imgTemp")

                    print("extracted: " + m + "-" + location + day_obj.strftime("-%Y%m%d") + h)
                    purge(os.getcwd(),
                          sYear + day_obj.strftime("%m") + day_obj.strftime(
                              "%d") + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001.*")
                    print("generating gif: " + m + "-" + location + day_obj.strftime("-%Y%m%d") + h)

                    os.system(
                        "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + day_obj.strftime(
                            "%m") + day_obj.strftime(
                            "%d") + h + "_054_GM_" + location + "_I_GEMMACH_" + m + "@sfc@001* "
                        + filelocation + "/output_img/" + sYear + day_obj.strftime("%m") + day_obj.strftime(
                            "%d") + h + "_IMG_Gemmach" + m + "_" + location + ".gif")
                    shutil.rmtree("imgTemp")
                    os.mkdir("imgTemp")
    print("\nJob done, see folder for images-->" + filelocation + "/output_img")


def generateUMOSImage(t):
    molecules = particulelst
    modelhourlist = re.split(",", modelHour)
    for location in locationlst:
        for day_obj in lstDate:
            for m in molecules:
                for h in modelhourlist:
                    os.system(
                        "cmcarc -x " + sYear + day_obj.strftime("%m") + day_obj.strftime(
                            "%d") + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + ".* -f " + os.getcwd() + "/rarc/operation.images.umoscr/" + sYear + day_obj.strftime(
                            "%m") + day_obj.strftime("%d") + h + "_" + location)

                    def purge(dir, pattern):
                        for f in os.listdir(dir):
                            if re.search(pattern, f):
                                shutil.move(f, os.getcwd() + "/imgTemp")

                    print("extracted: " + m + "-" + location + day_obj.strftime("-%Y%m%d") + h)
                    purge(os.getcwd(),
                          sYear + day_obj.strftime("%m") + day_obj.strftime(
                              "%d") + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + ".*")
                    print("generating gif: " + m + "-" + location + day_obj.strftime("-%Y%m%d") + h)
                    os.system(
                        "convert -delay 35 -loop 0 " + filelocation + "/imgTemp/" + sYear + day_obj.strftime(
                            "%m") + day_obj.strftime(
                            "%d") + h + "_054_UA_" + location + "_I_UMOS@GEMMACH_" + m + t + "* "
                        + filelocation + "/output_img/" + sYear + day_obj.strftime("%m") + day_obj.strftime(
                            "%d") + h + "_IMG_UMOS" + m + "_" + location + t + ".gif")
                    shutil.rmtree("imgTemp")
                    os.mkdir("imgTemp")
    print("\nJob done, see folder for images-->" + filelocation + "/output_img")
