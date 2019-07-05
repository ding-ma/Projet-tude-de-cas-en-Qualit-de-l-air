import calendar
import itertools as IT
import os
import re
import shutil
import tempfile
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


def datecounter(selectedDate,addDays):
    templist = selectedDate.split("/")
    lstsMonth = []
    lsteMonth = []
    lstDays = []
    lstsMonth.clear()
    lsteMonth.clear()
    lstDays.clear()
    startDate = date(int(templist[0]), int(templist[1]), int(templist[2]))
    endDate = date(int(templist[0]), int(templist[1]), int(templist[2]))
    delta = endDate - startDate
    for a in range(delta.days + addDays):
        e = startDate + timedelta(days=a)
        v = e.strftime("%d")
        lstDays.append(v)
    return lstDays


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
        "set Path " + filelocation + "/rarc/operation.scribeMat.mist.aq"
        "\nset bashFST "+ sYear + sMonth + sDay +modelHourList[0]+ "_mist_anal" +
        "\nset FileOut [open UmosMistEticket.txt w+]"
        "\nset FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]"
        "\nfstdfile open 1 read  $FileIn"
        "\nset eticket [fstdfile info 1 ETIKET]"
        "\nputs $eticket"
        "\nputs $FileOut \"$eticket\""
        "\nfstdfile close 1"
        "\nclose $FileOut"
    )


def bashFile(formattedParticuleString, selectedDate):
    year = selectedDate.split("/")[0]
    month = selectedDate.split("/")[1]
    day = selectedDate.split("/")[2]
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("UmosMist" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut=" + filelocation + "/bash"
            "\nPathIn=" + filelocation + "/rarc"
            "\nDateDebut=" + year + month+day+
            "\nDateFin=" + year + month+day+
            "\nListeMois=\"" + month + "\""
            "\nAnnee=" + year +  # not used
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
            "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}_${Grille}.fst"
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
            "\n${editfst} -s ${FileIn1} -d ${FileOut1} <<EOF"                                                                                                                                                                                                                                  "\nDESIRE (-1,\"$Espece\",-1, -1, $niveau, [0" +
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


def TCLConfig(formattedParticuleString, loc,selectedDate):
    getEticket()
    global fpp
    global locationId
    modelHourList = re.split(",", modelHour)
    locationId = loc
    fpp = formattedParticuleString
    removeAllfile(r'' + Gm.filelocation + "/config")
    for modelH in modelHourList:
        if modelH == "12":
            generateTCL(datecounter(selectedDate,3), modelH, locationId, fpp,selectedDate.split("/"))
        if modelH == "00":
            generateTCL(datecounter(selectedDate,2), modelH, locationId, fpp, selectedDate.split("/"))


def generateTCL(g, modelH, loc, fpp,selectedDate):
    year = selectedDate[0]
    month = selectedDate[1]
    day = selectedDate[2]
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
    if int(day) == calendar.monthrange(int(year), 1)[1]:
        lastday = g[0]
        firstdays = g[1:]
        nextmonth = date(int(year),int(month)+1, int(month)).strftime("%m")
        for p in particulelist:
            for d in firstdays:
                for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                    config = open("configMIST/MIST_" + nextmonth + p + d + hToName + modelH + ".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"UMOSmist" + modelH + "." + year + month + day + "_regeta\"\n"
                       "set Data(TAG3)   \""+ nextmonth + d + hToName + "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(levels) \" -1\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1\"\n"
                        "set Data(Path)    " + filelocation + "/bash\n"
                        "set Data(PathOut) " + filelocation + "/extractedMist\n"
                        "set Data(Start)      \"" + year + nextmonth + "\"\n"
                        "set Data(End)      \"" + year + nextmonth + "\"\n"
                        "set Data(Eticket)     \"" + Eticket + "\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "#set Data(ID) \"ID" + loc + "\"\n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(days) \"" + str(d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n")
        for p in particulelist:
            for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                config = open("configMIST/MIST_" + nextmonth + p + lastday + hToName + modelH + ".tcl", "w")
                config.write(
                    "set Data(SpLst)  \"" + p + "\" \n"
                    "set Data(TAG1)   \"UMOSmist" + modelH + "." + year + month + day + "_regeta\"\n"
                   "set Data(TAG3)   \""+ nextmonth + lastday + hToName + "\"\n"
                    "set Data(outTXT)       \"SITE\" \n"
                    "set Data(PASSE) \"" + modelH + "\"\n"
                    "set Data(levels) \" -1\"\n"  # todo confirm levels
                    "set Data(MandatoryLevels) \" 1\"\n"
                    "set Data(Path)    " + filelocation + "/bash\n"
                    "set Data(PathOut) " + filelocation + "/extractedMist\n"
                    "set Data(Start)      \"" + year + nextmonth + "\"\n"
                    "set Data(End)      \"" + year + nextmonth + "\"\n"
                    "set Data(Eticket)     \"" + Eticket + "\"\n"
                    "set Data(point) \"" + name + "\"\n"
                    "set Data(coord) \"" + lat + " " + long + "\"\n"
                    "#set Data(ID) \"ID" + loc + "\"\n"
                    "set Data(PASSE) \"" + modelH + "\"\n"
                    "set Data(days) \"" + str(lastday) + "\"\n"  # todo confirm start day
                    "set Data(hours) \"" + str(hToFile) + "\"\n")
    else:
        for p in particulelist:
            for d in list(g):
                for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                    config = open("configMIST/MIST_" + month + p + d + hToName + modelH + ".tcl", "w")
                    config.write(
                        "set Data(SpLst)  \"" + p + "\" \n"
                        "set Data(TAG1)   \"UMOSmist" + modelH + "." + year + month + day + "_regeta\"\n"
                       "set Data(TAG3)   \""+ month + d + hToName + "\"\n"
                        "set Data(outTXT)       \"SITE\" \n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(levels) \" -1\"\n"  # todo confirm levels
                        "set Data(MandatoryLevels) \" 1\"\n"
                        "set Data(Path)    " + filelocation + "/bash\n"
                        "set Data(PathOut) " + filelocation + "/extractedMist\n"
                        "set Data(Start)      \"" + year + month + "\"\n"
                        "set Data(End)      \"" + year + month + "\"\n"
                        "set Data(Eticket)     \"" + Eticket + "\"\n"
                        "set Data(point) \"" + name + "\"\n"
                        "set Data(coord) \"" + lat + " " + long + "\"\n"
                        "#set Data(ID) \"ID" + loc + "\"\n"
                        "set Data(PASSE) \"" + modelH + "\"\n"
                        "set Data(days) \"" + str(d) + "\"\n"  # todo confirm start day
                        "set Data(hours) \"" + str(hToFile) + "\"\n")


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



def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


def sortAndGenerate(destination,selectedDate):
    year = selectedDate.split("/")[0]
    month = selectedDate.split("/")[1]
    day = selectedDate.split("/")[2]
    particulelist = re.split(" ", fpp)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extractedMist | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            uniqueFileName = uniquify("output/UMOS-Mist__" + "ID" + locationId + "___" + m + p + "___" + year + month + day +".csv")
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
            file = open(uniqueFileName,"w+")
            file.write("Date,Time,Height,Value\n")
            for i in sorted(os.listdir(destination + m + p)):
                file.write(open(destination + m + p + "/" + i).read())
    print("\nJob done, see folder-->" + filelocation + "/output")
