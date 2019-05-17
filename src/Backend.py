#!/usr/bin/env python3


# Notes: def modelChosen(model): always needs to be the last function!

# to connect to host, not working
# def CMCServerConnection():  # add arguments to change user/pass
#     host = "sci-eccc-in.science.gc.ca"
#     host = "199.212.17.148"
#     user = "sair001"
#     passw= "1AiqaCom!"
#     port = 22
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.WarningPolicy())
#     print(" Connecting to %s \n with username: %s... \n" % (host, user))
#     client.connect(hostname=host, port=port, username=user,password=passw)
#     print("connected")
#     stdin, stdout, stderr = client.exec_command("alias")
#     print(stderr.readlines)

# checks for date input errors


# change filename to gemmach
def inputStartDate(sDate):
    global sYear
    global sMonth
    global sDay
    unformatattedDate = sDate.split("/")
    sYear = unformatattedDate[0]
    sMonth = unformatattedDate[1]
    sDay = unformatattedDate[2]

    oddMonths = ("01", "03", "05", "07", "09", "11")
    evenMonths = ("04", "06", "08", "10", "12")

    if len(sYear) != 4 or len(sMonth) != 2 or sMonth > "12" or len(sDay) != 2:
        dateErrors()
    elif sMonth == "02" and int(sDay) > 28:
        dateErrors()
    elif sMonth in oddMonths and int(sDay) > 31:
        dateErrors()
    elif sMonth in evenMonths and int(sDay) > 30:
        dateErrors()
    else:
        print("Start Date: " + sYear, sMonth, sDay)


def inputEndDate(eDate):
    global eYear
    global eMonth
    global eDay
    unformatattedDate = eDate.split("/")
    eYear = unformatattedDate[0]
    eMonth = unformatattedDate[1]
    eDay = unformatattedDate[2]

    oddMonths = ("01", "03", "05", "07", "09", "11")
    evenMonths = ("04", "06", "08", "10", "12")

    if len(eYear) != 4 or len(eMonth) != 2 or eMonth > "12" or len(eDay) != 2:
        dateErrors()
    elif eMonth == "02" and int(eDay) > 28:
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


def dateErrors():
    raise Exception("Date format error, please check what you have entered")


def time(sTime, eTime):
    global formattedSelectedTimeWithComma
    global formattedSelectedTimeWithSpace
    global sTimeBash
    sTimeBash = sTime
    hours = (
        "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
        "016",
        "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
        "033",
        "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")
    sIndex = hours.index(sTime)
    eIndex = hours.index(eTime)
    unformattedSelectedTime = ""
    for timeList in range(eIndex - sIndex + 1):
        unformattedSelectedTime += hours[sIndex + timeList]
    formattedSelectedTimeWithComma = addComma(unformattedSelectedTime)
    formattedSelectedTimeWithSpace = addSpace(unformattedSelectedTime)


def addComma(string):
    return ','.join(string[i:i + 3] for i in range(0, len(string), 3))


def addSpace(string):
    return ' '.join(string[i:i + 3] for i in range(0, len(string), 3))


def modelCheckbox(h_00, h_12):
    global modelHour
    global modelHourBash
    h_00 = int(h_00)
    h_12 = int(h_12)
    if (h_00 is True and h_12 is False) or (h_00 is 1 and h_12 is 0):
        modelHour = "00"
        modelHourBash = "00"
    elif (h_12 is True and h_00 is False) or (h_00 is 0 and h_12 is 1):
        modelHour = "12"
        modelHourBash = "12"
    elif (h_12 and h_00 is True) or (h_00 is 1 and h_12 is 1):
        modelHour = "00,12"
        modelHourBash = "00"
    else:
        modelHour = " "

# used for bashfile
def listOfDays():
    global formattedDay
    days = (
        "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
        , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
    sIndex = days.index(sDay)
    eIndex = days.index(eDay)
    unformattedDay = ""
    for dayList in range(eIndex - sIndex + 1):
        unformattedDay += days[sIndex + dayList]
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


def particuleCheckBox(O3, NO2, others, PM25):
    # TODO dictionary for others?
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
    formattedParticuleString = ' '.join(
        unformattedParticuleString[i:i + 2] for i in range(0, len(unformattedParticuleString), 2))

# rarc cmd
# rarc -i /home/sair001/rarcdirectives/gemmach -tmpdir ./temp
def rarcFile():
    file = open("gemmach", "w")
    file.write(
        "target = /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.forecasts.mach\n"
        "ext = " + formattedSelectedTimeWithComma +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    bashFile()
    print("File Saved")


def bashFile():
    modelHourWithSpace = modelHour.replace(",", " ")
    fileBash = open("gemmachBashTest.bash", 'w')
    fileBash.write(
        "#!/bin/bash\n"
        "PathOut=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest"
        "\nPathIn=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach"
        "\nDateDebut=" + sYear + sMonth +
        "\nDateFin=" + eYear + eMonth +
        "\nListeMois=\"" + formattedMonthlist + "\""
                                                "\nAnnee=" + sYear +  # not used
        "\nTag1=TEST"
        "\neditfst=/fs/ssm/eccc/mrd/rpn/utils/16.2/ubuntu-14.04-amd64-64/bin/editfst"
        "\nType=species"
        "\nGrille=regeta"
        "\nFichierTICTAC=/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/operation.forecasts.mach/${DateDebut}" + sDay + modelHourBash + "_" + sTimeBash +
        "\nListeVersionsGEM=\"operation.forecasts.mach\""
        "\nListeEspeces=\"" + formattedParticuleString + "\""
                                                         "\nListeNiveaux=\"76696048\""  # TODO confirm levels
        "\nListeJours=\"" + formattedDay + "\""
        "\nListePasse=\"" + modelHourWithSpace + "\""
        "\nListeHeures=\"" + formattedSelectedTimeWithSpace + "\""
          "\n################# Extraction#############"
          "\nfor VersionGEM in  ${ListeVersionsGEM}"
          "\ndo"
          "\nFileOut1=${PathOut}/${VersionGEM}/${Tag1}.${DateDebut}_${DateFin}_${Grille}.fst"
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
    print("saved!")
