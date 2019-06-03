import os
import re

import Gemmach as Gm

filelocation = os.getcwd()

oddMonths = ("01", "03", "05", "07", "09", "11")
evenMonths = ("04", "06", "08", "10", "12")

def inputStartDate(sDate):
    global sYear
    global sMonth
    global sDay
    #splits the entry into a tuple
    print(sDate)
    unformatattedDate = re.split("/", sDate)
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]
    # checks for leap year
    if int(sYear) % 4 == 0 and int(sYear) % 100 != 0 or int(sYear) % 400 == 0:
        leap = True
    else:
        leap = False
    #checks if the user input is correct
    if len(sYear) != 4 or len(sMonth) != 2 or sMonth > "12" or len(sDay) != 2:
        dateErrors()
    elif leap is True and int(sDay) > 29 and sMonth == "02":
        dateErrors()
    elif leap is False and sMonth == "02" and int(sDay) > 28:
        dateErrors()
    elif sMonth in oddMonths and int(sDay) > 31:
        dateErrors()
    elif sMonth in evenMonths and int(sDay) > 30:
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

    if len(eYear) != 4 or len(eMonth) != 2 or eMonth > "12" or len(eDay) != 2:
        dateErrors()
    elif leap is True and eMonth == "02" and int(eDay) > 29:
        dateErrors()
    elif leap is False and eMonth == "02" and int(eDay) > 28:
        dateErrors()
    elif eMonth in oddMonths and int(eDay) > 31:
        dateErrors()
    elif eMonth in evenMonths and int(eDay) > 30:
        dateErrors()
    elif sMonth > eMonth:
        dateErrors()
    elif sMonth == eMonth and sDay > eDay:
        dateErrors()
    else:
        print("End Date: " + eYear, eMonth, eDay)
        listOfDays()
        listofMonth()

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

days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
    , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
# used for bashfile

def listOfDays():
    global formattedDay
    global startDateIndex
    global endDateIndex
    startDateIndex = days.index(sDay)
    endDateIndex = days.index(eDay)
    unformattedDay = ""
    for dayList in range(endDateIndex - startDateIndex + 1):
        unformattedDay += days[startDateIndex + dayList]
    #for every 2 character, adds space
    formattedDay = ' '.join(unformattedDay[i:i + 2] for i in range(0, len(unformattedDay), 2))

def listofMonth():
    global formattedMonthlist
    listMonth = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
    sIndex = listMonth.index(sMonth)
    eIndex = listMonth.index(eMonth)
    unformattedMonthList = ""
    for monthList in range(eIndex - sIndex + 1):
        unformattedMonthList += listMonth[sIndex + monthList]
        formattedMonthlist = ' '.join(unformattedMonthList[i:i + 2] for i in range(0, len(unformattedMonthList), 2))
def dateErrors():
    raise Exception("Date format error, please check what you have entered")

def bashFile():

    fileBash = open("UMOSmist.bash", 'w+')
    fileBash.write(
        "#!/bin/bash\n"
        "PathOut="+filelocation+"/bash"
        "\nPathIn="+filelocation+"/rarc"
        "\nDateDebut=" + sYear + sMonth+
        "\nDateFin=" + eYear + eMonth + eDay+
        "\nListeMois=\"" + formattedMonthlist + "\""
        "\nAnnee=" + sYear +  # not used
        "\nTag1=BashOut"+modelHourSeparated+
        "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
        "\nType=species"
        "\nGrille=regeta"
        "\nFichierTICTAC="+filelocation+"/rarc/operation.forecasts.mach/${DateDebut}" + sDay + modelHourBash + "_" + sTimeBash +
        "\nListeVersionsGEM=\"operation.forecasts.mach\""
        "\nListeEspeces=\"" + Gm.get_formattedParticuleString() + "\""
        "\nListeNiveaux=\"" + "-1" + "\""  # TODO confirm levels
        "\nListeJours=\"" + "-1" + "\""
        "\nListePasse=\"" + "-1" + "\""
        "\nListeHeures=\"" + "-1" + "\""
        "\n################# Extraction#############"
        "\nfor VersionGEM in  ${ListeVersionsGEM}"
        "\ndo"
        "\nFileOut1=${PathOut}/${Tag1}.${DateDebut}"+sDay+"_${DateFin}_${Grille}.fst"
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
        "\nFileIn1=${PathIn}/${VersionGEM}/${DateDebut}${jour}${passe}_${heure}"
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
    print("Bash File Saved!")