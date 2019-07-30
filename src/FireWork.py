import itertools as IT
import os
import re
import shutil
import tempfile
from datetime import date, timedelta, datetime

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


def rarcFile():
    file = open("FireWork", "w")
    file.write(
        "target = "+filelocation+"/rarc\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.forecasts.firework.mach\n"
        "ext = " + formattedSelectedTimeWithComma +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    modelHourList = re.split(",", modelHour)
    fileEticket = open("FireEticket.tcl", "w")
    fileEticket.write(
        "#!/bin/bash\n"
        "# : - \\"
        "\nexec /fs/ssm/eccc/cmo/cmoe/apps/SPI_7.12.0_all/tclsh \"$0\" \"$@\""
        "\npackage require TclData\n"
        "set Path "+filelocation+"/rarc/operation.forecasts.firework.mach/"
        "\nset bashFST "+ sYear + sMonth+sDay+modelHourList[0]+"_"+formattedSelectedTimeWithComma.split(",")[0]+
        "\nset FileOut [open FwEticket.txt w+]"
        "\nset FileIn [ lsort -dictionary [ glob $Path$bashFST ] ]"
        "\nfstdfile open 1 read  $FileIn"
        "\nset eticket [fstdfile info 1 ETIKET]"
        "\nputs $eticket"
        "\nputs $FileOut \"$eticket\""
        "\nfstdfile close 1"
        "\nclose $FileOut")


def level(lv):
    global lev
    if lv is "":
        lev = "76696048 93423264"
    else:
        lev = lv


def bashFile(formattedParticuleString, selectedDate):
    year = selectedDate.split("/")[0]
    month = selectedDate.split("/")[1]
    day = selectedDate.split("/")[2]
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("FireWork" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut="+filelocation+"/bash"
            "\nPathIn="+filelocation+"/rarc"
            "\nDateDebut=" + year + month+day+
            "\nDateFin=" + year + month+day+
            "\nDateDebutMois="+sMonth+
            "\nListeMois=\"" + month + "\""
            "\nAnnee=" + year +  # not used
            "\nTag1=FW"+modelHourSeparated+
            "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
            "\nType=species"
            "\nGrille=regeta"
            "\nFichierTICTAC="+filelocation+"/rarc/operation.forecasts.firework.mach/${Annee}${DateDebutMois}" + sDay + modelHourBash + "_" + sTimeBash +
            "\nListeVersionsGEM=\"operation.forecasts.firework.mach\""
            "\nListeEspeces=\"O3 N2 AF\"" #f ormattedParticuleString
            "\nListeNiveaux=\"" + lev + "\""  # TODO confirm levels
            "\nListeJours=\"" + day + "\""
            "\nListePasse=\"" + modelHourSeparated + "\""
            "\nListeHeures=\"" + formattedSelectedTimeWithSpace + "\""
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
            "\nFileIn1=${PathIn}/${VersionGEM}/${Annee}${mois}${jour}${passe}_${heure}"
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
            "\nDESIRE (-1,\"$Espece\",-1, -1, $niveau, -1, -1) "
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
    print("Fire-Work Config Files Saved!")


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


def TCLConfig(formattedParticuleString, loc,selectedDate):
    getEticket()
    global fpp
    global locationId
    locationId = loc
    fpp = formattedParticuleString
    removeAllfile(r'' + Gm.filelocation + "/configFw")
    modelHourList = re.split(",", modelHour)
    for modelH in modelHourList:
        if modelH == "12":
            generateTCL(modelH,formattedParticuleString, loc, selectedDate.split("/"))
        if modelH == "00":
            generateTCL(modelH,formattedParticuleString, loc,selectedDate.split("/"))


def getEticket():
    os.system("./FireEticket.tcl")


def generateTCL(modelH,formattedParticuleString, loc,selectedDate):
    global locationID
    FireWorkEticket = open("FwEticket.txt", "r")
    year = selectedDate[0]
    month = selectedDate[1]
    day = selectedDate[2]
    Eticket = FireWorkEticket.read().strip()
    particulelist = re.split(" ", formattedParticuleString)
    listIndex = Gm.lstID.index(loc)
    name = Gm.lstName[listIndex]
    long = Gm.lstLongitude[listIndex]
    lat = Gm.lstLatitude[listIndex]
    executehour = re.split(",", formattedSelectedTimeWithComma)
    locationID = Gm.lstID[listIndex]
    s = Gm.hours.index(executehour[0])
    e = Gm.hours.index(executehour[-1])

    for I in range(int(e)-int(s)+1):
        for p in particulelist:
            starttime = datetime(int(year),int(month),int(day),int(modelH))+timedelta(hours = int(s))
            generatedTime = starttime +timedelta(hours = I)
            time00Format = generatedTime.strftime("%H")
            time0Format = generatedTime.strftime("%-H")
            dateToFile = generatedTime.strftime("%d")
            monthToFile = generatedTime.strftime("%m")
            config = open("configFw/Fw_" + monthToFile + p + dateToFile + time00Format + modelH + ".tcl", "w")
            config.write(
                "set Data(SpLst)  \"" + p + "\" \n"
                "set Data(TAG1)   \"FW" + modelH + "." + year + month + day + "_regeta\"\n"
                "set Data(TAG3)   \"" + monthToFile + dateToFile + time00Format + "\"\n"
                "set Data(outTXT)       \"SITE\" \n"
                "set Data(PASSE) \"" + modelH + "\"\n"
                "set Data(levels) \" -1\"\n"  # todo confirm levels
                "set Data(MandatoryLevels) \" 1\"\n"
                "set Data(Path)    " + filelocation + "/bash\n"
                "set Data(PathOut) " + filelocation + "/extractedFw\n"
                "set Data(Start)      \"" + year + monthToFile + "\"\n"
                "set Data(End)      \"" + year + monthToFile + "\"\n"
                "set Data(Eticket)     \"" + Eticket + "\"\n"
                "set Data(point) \"" + name + "\"\n"
                "set Data(coord) \"" + lat + " " + long + "\"\n"
                "set Data(days) \"" + str(dateToFile) + "\"\n"  # todo confirm start day
                "set Data(hours) \"" + str(time0Format) + "\"\n")


def launchTCL():
    os.system(" ls "+filelocation+"/configFw | sort -st '/' -k1,1")
    os.system("chmod -R 744 "+ filelocation+"/configFw")
    for a in os.listdir('configFw'):
        os.system("./extract1.tcl " + "configFw/" + a)


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

def checkifBashFileExist(selectedDate,numberChecked):
    templst = selectedDate.split("/")
    year = templst[0]
    month = templst[1]
    day = templst[2]
    if numberChecked is 1:
        fileToMatch = "FW00."+year+month+day+"_regeta.fst"
        if fileToMatch in os.listdir("bash/"):
            return True
        else:
            return False
    if numberChecked is 2:
        fileToMatch = "FW12." + year + month + day + "_regeta.fst"
        if fileToMatch in os.listdir("bash/"):
            return True
        else:
            return False
    if numberChecked is 3:
        fileToMatch00 = "FW00."+year+month+day+"_regeta.fst"
        fileToMatch12 = "FW12." + year + month + day + "_regeta.fst"
        if (fileToMatch00 and fileToMatch12) in os.listdir("bash/"):
            return True
        else:
            return False


def sortAndGenerate(destination, selectedDate):
    year = selectedDate.split("/")[0]
    month = selectedDate.split("/")[1]
    day = selectedDate.split("/")[2]
    particulelist = re.split(" ", fpp)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extractedFw | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            uniqueName = uniquify("output/FW__"+"ID"+ locationID + "___" + m + p + "___" + year + month + day + "_.csv")
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
            file = open(uniqueName, "w+")
            file.write("Date,Time,Height,Value\n")
            for i in sorted(os.listdir(destination + m + p)):
                file.write(open(destination + m + p + "/" + i).read())
    print("\nJob done, see folder-->" + filelocation+"/output")
