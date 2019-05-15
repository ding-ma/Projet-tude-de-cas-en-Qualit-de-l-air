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

import logging
# checks for date input errors
import os


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
    else:
        print("End Date: " + eYear, eMonth, eDay)


def dateErrors():
    print("Date format error enter them again")


def time(sTime, eTime):
    global formattedSelectedTime
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
    formattedSelectedTime = addComma(unformattedSelectedTime)


def addComma(string):
    return ','.join(string[i:i + 3] for i in range(0, len(string), 3))


def modelCheckbox(h_00, h_12):
    global modelHour
    h_00 = int(h_00)
    h_12 = int(h_12)
    if (h_00 is True and h_12 is False) or (h_00 is 1 and h_12 is 0):
        modelHour = "00"
    elif (h_12 is True and h_00 is False) or (h_00 is 0 and h_12 is 1):
        modelHour = "12"
    elif (h_12 and h_00 is True) or (h_00 is 1 and h_12 is 1):
        modelHour = "00,12"
    else:
        modelHour = " "


# rarc cmd
# rarc -i /home/sair001/rarcdirectives/gemmach -tmpdir ./temp
def writeFile():
    file = open("gemmach", "w")
    file.write(
        "target = $TMPDIR\n"
        "filter = copy\n"
        "postprocess = nopost\n"
        "date = "
        # start
        + sYear + "," + sMonth + "," + sDay + ","
        # end
        + eYear + "," + eMonth + "," + eDay +
        "\nbranche = operation.forecasts.mach\n"
        "ext = " + formattedSelectedTime +
        "\nheure = " + modelHour +
        "\npriority = online\n"
        "inc = 1\n"
        "#\n")
    print("File Saved")
