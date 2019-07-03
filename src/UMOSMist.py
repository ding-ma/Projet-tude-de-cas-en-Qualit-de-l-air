import calendar
import os
import re
import shutil
from datetime import date, timedelta

import Gemmach as Gm

filelocation = Gm.filelocation


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
    listOfDays()
    listofMonth()


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


def datecounter(addDays):
    # global daylst12
    # global montlst

    lstsMonth = []
    lsteMonth = []
    lstDays = []
    lstsMonth.clear()
    lsteMonth.clear()
    lstDays.clear()
    startDate = date(int(sYear), int(sMonth), int(sDay))
    endDate = date(int(eYear), int(eMonth), int(eDay))
    if startDate.month is not endDate.month:
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
        return lstsMonth, lsteMonth
    else:
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
    unformattedDay = []
    genday = datecounter(2)
    if len(genday) is 2 and isinstance(genday, tuple):
        for l in genday[0]:
            unformattedDay += l
        for z in genday[1]:
            unformattedDay += z
    else:
        for l in genday:
            unformattedDay += l
    formattedDay = (' '.join(set(unformattedDay)))


# for bash
def listofMonth():
    global formattedMonthlist
    unformattedMonthList = ""
    lst = [sMonth, eMonth]
    for form in set(lst):
        unformattedMonthList += form
    formattedMonthlist = ' '.join(unformattedMonthList[i:i + 2] for i in range(0, len(unformattedMonthList), 2))


def rarcFile():
    modelHourList = re.split(",", modelHour)
    file = open("UMist", "w")
    file.write(
        "target = " + filelocation + "/rarc\n"
                                     "filter = copy\n"
                                     "postprocess = nopost\n"
                                     "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.scribeMat.mist.aq\n"
        "ext = ***"
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    fileEticket = open("UmosMistEticket.tcl", "w")
    fileEticket.write(
        "#!/bin/bash\n"
        "# : - \\"
        "\nexec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh \"$0\" \"$@\""
        "\npackage require TclData\n"
        "set Path " + filelocation + "/bash/"
                                     "\nset bashFST UMOSmist" + modelHourList[
            0] + "." + sYear + sMonth + sDay + "_" + eYear + eMonth + eDay + "_regeta.fst" +
        "\nset FileOut [open UmosMistEticket.txt w+]"
        "\nset FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]"
        "\nfstdfile open 1 read  $FileIn"
        "\nset eticket [fstdfile info 1 ETIKET]"
        "\nputs $eticket"
        "\nputs $FileOut \"$eticket\""
        "\nfstdfile close 1"
        "\nclose $FileOut"
    )


def bashFile(formattedParticuleString, loc):
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("UmosMist" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut=" + filelocation + "/bash"
                                        "\nPathIn=" + filelocation + "/rarc"
                                                                     "\nDateDebut=" + sYear + sMonth + sDay +
            "\nDateFin=" + eYear + eMonth + eDay +
            "\nListeMois=\"" + sMonth + "\""
                                        "\nAnnee=" + sYear +  # not used
            "\nTag1=UMOSmist" + modelHourSeparated +
            "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
            "\nType=species"
            "\nGrille=regeta"
            "\nFichierTICTAC=" + filelocation + "/rarc/operation.scribeMat.mist.aq/${DateDebut}" + modelHourSeparated + "_mist_anal"
            "\nListeVersionsGEM=\"operation.scribeMat.mist.aq\""
            "\nListeEspeces=\"" + formattedParticuleString + "\""
            "\nListeNiveaux=\"-1\""  # TODO confirm levels
            "\nListeJours=\"-1\""
            "\nListePasse=\"-1\""
            "\nListeHeures=\"-1\""
            "\n################# Extraction#############"
            "\nfor VersionGEM in  ${ListeVersionsGEM}"
            "\ndo"
            "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst"
            "\nif [  ${FileOut1}  ]; then"
            "\nrm -rf  ${FileOut1}"
            "\nelse"
            "\ncontinue"
            "\nfi"
            "\nFileIn=${FichierTICTAC}"
            "\n${editfst} -s ${FileIn} -d ${FileOut1} <<EOF"
            "\nDESIRE(-1,['>>','^^'],-1,-1,-1,-1,-1)"
            "\nZAP(-1,-1,'CAPAMIST',-1,-1,-1,-1)"
            "\nEOF"
            "\nfor mois in ${ListeMois}"
            "\ndo"
            "\necho ${mois}"
            "\nfor jour in ${ListeJours}"
            "\ndo"
            "\nfor passe  in ${ListePasse}"
            "\ndo"
            "\nfor heure in ${ListeHeures}"
            "\ndo"
            "\necho ${heure}"
            "\nFileIn1=${PathIn}/${VersionGEM}/${DateDebut}" + modelHourSeparated + "_mist_anal"
            "\nif [ ! ${FileIn1}  ]; then"
            "\ncontinue"
            "\nelse"
            "\necho \"-------------\""
            "\necho ${FileIn1} \"file does exist\""
            "\nfi"
            "\necho ${FileIn1}"
            "\nfor Espece in ${ListeEspeces}"
            "\ndo"
            "\nif [ \"$Espece\" = \"P0\" ] || [ \"$Espece\" = \"TCC\" ] ; then"
            "\n${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF"
            "\nDESIRE (-1,\"$Espece\",-1, -1, 0, -1, -1)"
            "\nEOF"
            "\nelse"
            "\nfor niveau in  ${ListeNiveaux}"
            "\ndo"
            "\n${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF"
                                                                                                                                                                                                                                                 "\nDESIRE (-1,\"$Espece\",-1, -1, $niveau, [0" +
            formattedSelectedTimeWithSpace.split(" ")[0] + ",@,0" + formattedSelectedTimeWithSpace.split(" ")[
                -1] + ",DELTA,1], -1)"
                      "\nZAP(-1,-1,'CAPAMIST',-1,-1,-1,-1)"
                      "\nEOF"
                      "\ndone"
                      "\nfi"
                      "\ndone"
                      "\ndone"
                      "\ndone"
                      "\ndone"
                      "\ndone"
                      "\ndone\n"
        )
    print("UMOS-Mist Config Files Saved!")


def time(sTime, eTime):
    global formattedSelectedTimeWithComma
    global formattedSelectedTimeWithSpace
    global sTimeBash
    sTimeBash = sTime
    # gets index then generates a list within the index
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


def getEticket():
    os.system("./UmosMistEticket.tcl")


def TCLConfig(formattedParticuleString, loc):
    getEticket()
    global fpp
    global locationId
    modelHourList = re.split(",", modelHour)
    locationId = loc
    fpp = formattedParticuleString
    removeAllfile(r'' + Gm.filelocation + "/config")
    for modelH in modelHourList:
        if modelH == "12":
            g = datecounter(3)
            generateTCL(g, modelH, locationId, fpp)
        if modelH == "00":
            generateTCL(genday, modelH, locationId, fpp)


def generateTCL(g, modelH, loc, fpp):
    umistEticket = open("UmosMistEticket.txt", "r")
    Eticket = umistEticket.read().strip()
    particulelist = re.split(" ", fpp)
    listIndex = Gm.lstID.index(loc)
    name = Gm.lstName[listIndex]
    long = Gm.lstLongitude[listIndex]
    lat = Gm.lstLatitude[listIndex]
    executehour = re.split(",", formattedSelectedTimeWithComma)
    s = Gm.hours.index(executehour[0])
    e = Gm.hours.index(executehour[-1])
    if int(sMonth) is not int(eMonth):
        for p in particulelist:
            for d in g[0]:
                for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                    config = open("configMIST/MIST_" + sMonth + p + d + hToName + modelH + ".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"UMOSmist" + modelH + "." + sYear + sMonth + sDay + "_" + eYear + eMonth + eDay + "_regeta\"\n"
                        "set Data(TAG3)   \""+d+ sMonth + hToName+ "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(levels) \" -1\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1\"\n"
                        "set Data(Path)    " + filelocation + "/bash\n"
                        "set Data(PathOut) " + filelocation + "/extractedMist\n"
                        "set Data(Start)      \"" + sYear + sMonth + "\"\n"
                        "set Data(End)      \"" + eYear + eMonth + "\"\n"
                        "set Data(Eticket)     \"" + Eticket + "\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "#set Data(ID) \"ID" + loc + "\"\n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(days) \"" + str(
                        d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n"
                    )
        for p in particulelist:
            for d in g[1]:
                for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                    config = open("configMIST/MIST_" + eMonth + p + d + hToName + modelH + ".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"UMOSmist" + modelH + "." + sYear + sMonth + sDay + "_" + eYear + eMonth + eDay + "_regeta\"\n"
                       "set Data(TAG3)   \""+d+ sMonth + hToName+ "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(levels) \" -1\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1\"\n"
                        "set Data(Path)    " + filelocation + "/bash\n"
                        "set Data(PathOut) " + filelocation + "/extractedMist\n"
                        "set Data(Start)      \"" + sYear + eMonth + "\"\n"
                        "set Data(End)      \"" + eYear + eMonth + "\"\n"
                        "set Data(Eticket)     \"" + Eticket + "\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "#set Data(ID) \"ID" + loc + "\"\n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(days) \"" + str(
                        d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n"
                    )
    else:
        dayList = list(genday)
        for p in particulelist:
            for d in dayList:
                for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                    config = open("configMIST/MIST_" + sMonth + p + d + hToName + modelH + ".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"UMOSmist" + modelH + "." + sYear + sMonth + sDay + "_" + eYear + eMonth + eDay + "_regeta\"\n"
                       "set Data(TAG3)   \""+d+ sMonth + hToName+ "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(levels) \" -1\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1\"\n"
                        "set Data(Path)    " + filelocation + "/bash\n"
                        "set Data(PathOut) " + filelocation + "/extractedMist\n"
                        "set Data(Start)      \"" + sYear + sMonth + "\"\n"
                        "set Data(End)      \"" + eYear + eMonth + "\"\n"
                        "set Data(Eticket)     \"" + Eticket + "\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "#set Data(ID) \"ID" + loc + "\"\n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(days) \"" + str(
                        d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n"
                    )
    print("Done")


def launchTCL():
    os.system(" ls " + filelocation + "/config | sort -st '/' -k1,1")
    os.system("chmod -R 777 " + filelocation + "/configMIST")
    for a in os.listdir('configMIST'):
        os.system("./extract1.tcl " + "configMIST/" + a)


def removeEmptyFile(path):
    docList = os.listdir(path)
    for doc in docList:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) == 0:
                os.remove(docPath)
        if os.path.isdir(docPath):
            removeEmptyFile(docPath)


Name = []


def removeAllfile(path):
    Name = os.listdir(path)
    for doc in Name:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) > 0:
                os.remove(docPath)


def sortAndGenerate(destination):
    particulelist = re.split(" ", fpp)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extractedMist | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                for delete in Gm.HtoDelete:
                    #takes the 4th character to sort
                    if f.startswith(delete,4):
                        os.remove(destination + f)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
            file = open(
                "output/UMOS-Mist__" + "ID" + locationId + "___" + m + p + "___Start" + sYear + sMonth + sDay + "___End" + eYear + eMonth + eDay + ".csv",
                "w+")
            file.write("Date,Time,Height,Value\n")
            for i in sorted(os.listdir(destination + m + p)):
                b = open(destination + m + p + "/" + i).read()
                file.write(b)
    print("\nJob done, see folder-->" + filelocation + "/output")
