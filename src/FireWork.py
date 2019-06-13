import os
import re
import shutil
from datetime import date, timedelta

import Gemmach as Gm

Eticket = Gm.EticketFW
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
    print("Start Date: " + sDate.strftime("%Y %m %d"))


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
    print("End Date: " + eDate.strftime("%Y %m %d"))
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


# used for bashfile

def datecounter(Type,modelh):
    global daylst
    global daylst12
    global montlst
    daylst = []
    daylst12 =[]
    montlst = []
    unformattedDay = ""
    unformattedMonth = ""
    datedelta = eDate - sDate
    if modelh is 00:
        for ww in range(datedelta.days+1):
            count = sDate + timedelta(days=ww)
            day = count.strftime("%d")
            daylst.append(day)
            unformattedDay +=day
            month = count.strftime("%m")
            montlst.append(month)
        if Type is 1:
            return unformattedDay
        if Type is 2:
            monthSet = sorted(set(montlst))
            for m in monthSet:
                unformattedMonth += m
            return unformattedMonth
    if modelh is 12:
        #this accounts for the extra days the model 12 uses
        for ww in range(datedelta.days + 3):
            count = sDate + timedelta(days=ww)
            day = count.strftime("%d")
            daylst12.append(day)
        return daylst12


# used for bashfile
def listOfDays():
    global formattedDay
    unformattedDay = datecounter(1,00)
    formattedDay = ' '.join(unformattedDay[i:i + 2] for i in range(0, len(unformattedDay), 2))


#for bash
def listofMonth():
    global formattedMonthlist
    unformattedMonthList = datecounter(2,00)
    formattedMonthlist = ' '.join(unformattedMonthList[i:i + 2] for i in range(0, len(unformattedMonthList), 2))


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
    print("Fire-Work RARC File Saved")

def level(lv):
    global lev
    if lv is "":
        lev = "76696048 93423264"
    else:
        lev = lv


def bashFile(formattedParticuleString, loc):
    modelHourList = re.split(",", modelHour)
    for modelHourSeparated in modelHourList:
        fileBash = open("FireWork" + modelHourSeparated + ".bash", 'w')
        fileBash.write(
            "#!/bin/bash\n"
            "PathOut="+filelocation+"/bash"
            "\nPathIn="+filelocation+"/rarc"
            "\nDateDebut=" + sYear + sMonth+sDay+
            "\nDateFin=" + eYear + eMonth + eDay+
            "\nDateDebutMois="+sMonth+
            "\nListeMois=\"" + formattedMonthlist + "\""
            "\nAnnee=" + sYear +  # not used
            "\nTag1=FW"+modelHourSeparated+
            "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
            "\nType=species"
            "\nGrille=regeta"
            "\nFichierTICTAC="+filelocation+"/rarc/operation.forecasts.firework.mach/${Annee}${DateDebutMois}" + sDay + modelHourBash + "_" + sTimeBash +
            "\nListeVersionsGEM=\"operation.forecasts.firework.mach\""
            "\nListeEspeces=\"" + formattedParticuleString + "\""
            "\nListeNiveaux=\"" + lev + "\""  # TODO confirm levels
            "\nListeJours=\"" + formattedDay + "\""
            "\nListePasse=\"" + modelHourSeparated + "\""
            "\nListeHeures=\"" + formattedSelectedTimeWithSpace + "\""
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
    print("Fire-Work Bash File Saved!")
    TCLConfig(formattedParticuleString, loc)


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


def TCLConfig(formattedParticuleString, loc):
    global fpp
    global locationId
    locationId = loc
    fpp = formattedParticuleString
    removeAllfile(r'' + Gm.filelocation + "/configFw")
    particulelist = re.split(" ", formattedParticuleString)
    modelHourList = re.split(",", modelHour)
    listIndex = Gm.lstID.index(loc)
    name = Gm.lstName[listIndex]
    long = Gm.lstLongitude[listIndex]
    lat = Gm.lstLatitude[listIndex]
    executehour = re.split(",", formattedSelectedTimeWithComma)
    s = Gm.hours.index(executehour[0])
    e = Gm.hours.index(executehour[-1])
    for p in particulelist:
        for m in formattedMonthlist.split(" "):
            for modelH in modelHourList:
                if modelH == "12":
                    dayList = datecounter(0, 12)
                else:
                    dayList = daylst
                for d in dayList:
                    for hToFile, hToName in zip(Gm.tcl[s:e + 1], Gm.hour24[s:e + 1]):
                        config = open("configFw/Fw_" +m+ p + d + hToName + modelH + ".tcl", "w")
                        config.write(
                            "set Data(SpLst)  \"" + p + "\" \n"
                            "set Data(TAG1)   \"FW" + modelH + "." + sYear + sMonth + sDay + "_" + eYear + eMonth + eDay + "_regeta\"\n"
                            "set Data(TAG3)   \""+m + d + "" + hToName + "\"\n"
                            "set Data(outTXT)       \"SITE\" \n"
                            "set Data(PASSE) \"" + modelH + "\"\n"
                            "set Data(levels) \" -1\"\n"  # todo confirm levels
                            "set Data(MandatoryLevels) \" 1\"\n"
                            "set Data(Path)    " + filelocation + "/bash\n"
                            "set Data(PathOut) " + filelocation + "/extractedFw\n"
                            "set Data(Start)      \"" + sYear + m + "\"\n"
                            "set Data(End)      \"" + eYear + eMonth + "\"\n"
                            "set Data(Eticket)     \""+Eticket+"\"\n"
                            "set Data(point) \"" + name + "\"\n"
                            "set Data(coord) \"" + lat + " " + long + "\"\n"   
                            "set Data(days) \"" + str(d) + "\"\n"  # todo confirm start day
                            "set Data(hours) \"" + str(hToFile) + "\"\n"
                        )
    print("Done")


def launchTCL():
    os.system(" ls "+filelocation+"/configFw | sort -st '/' -k1,1")
    os.system("chmod -R 777 "+ filelocation+"/configFw")
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

def sortAndGenerate(destination):
    particulelist = re.split(" ", fpp)
    modelHourList = re.split(",", modelHour)
    os.system(" ls " + filelocation + "/extractedFw | sort -st '/' -k1,1")
    for m in modelHourList:
        for p in particulelist:
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
            file = open("output/FW__"+"ID"+locationId +"___"+m + p+"___Start"+sYear+sMonth+sDay +"___End"+eYear+eMonth+eDay+ ".csv", "w+")
            file.write("Date,Time,Height,Value\n")
            for i in sorted(os.listdir(destination + m + p)):
                b = open(destination + m + p + "/" + i).read()
                file.write(b)
    print("\nJob done, see folder-->" + filelocation+"/output")
