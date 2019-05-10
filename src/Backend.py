import os


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
def inputDate(date):
    unformatattedDate = date.split("/")
    year = unformatattedDate[0]
    month = unformatattedDate[1]
    day = unformatattedDate[2]

    oddMonths = ("01", "03", "05", "07", "09", "11")
    evenMonths = ("04", "06", "08", "10", "12")

    if len(year) != 4 or len(month) != 2 or month > "12" or len(day) != 2:
        dateErrors()
    elif month == "02" and int(day) > 28:
        dateErrors()
    elif month in oddMonths and int(day) > 31:
        dateErrors()
    elif month in evenMonths and int(day) > 30:
        dateErrors()
    else:
        print(year, month, day)


def dateErrors():
    print("Date format error enter them again")


def modelChosen(model):
    if model == "GEM-MACH":
        print("Using GEM-MACH")
    else:
        print("Function not supported yet")

def toolChosen(tool):
    if tool == "XRARC":
        print("Lanching XRARC...")
        os.system('XRARC')
