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
        print(sYear, sMonth, sDay)

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

    if len(eYear) != 4 or len(eMonth) != 2 or eMonth> "12" or len(eDay) != 2:
        dateErrors()
    elif eMonth == "02" and int(eDay) > 28:
        dateErrors()
    elif eMonth in oddMonths and int(eDay) > 31:
        dateErrors()
    elif eMonth in evenMonths and int(eDay) > 30:
        dateErrors()
    else:
        print(eYear, eMonth, eDay)

def dateErrors():
    print("Date format error enter them again")



def toolChosen(tool):
    if tool == "XRARC":
        print("Lanching XRARC...")
    # os.system('XRARC')


def time(sTime, eTime):
    hours = (
        "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
        "016",
        "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
        "033",
        "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")
    sIndex = hours.index(sTime)
    eIndex = hours.index(eTime)
    global extTime
    for timeList in range(eIndex - sIndex + 1):
        extTime = hours[sIndex + timeList]
        print(extTime)


def modelChosen(model):
    if model == "GEM-MACH":
        print("Using GEM-MACH")
        file = open("gemmach", "w")
        file.write(
            "target = /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma\n"
            "filter = copy\n"
            "postprocess = nopost\n"
            "date = "
            # start
            + sYear + "," + sMonth + "," + sDay + ","
            # end
            + eYear + "," + eMonth + "," + eDay +
            "\nbranche = operation.forecasts.mach\n"
            "ext = "  # TODO format the extTime into the appropriate format in order to insert it
            "\nheure = 00\n"
            "priority = online\n"
            "inc = 1\n"
            "#\n")

    else:
        print("Function not supported yet")
