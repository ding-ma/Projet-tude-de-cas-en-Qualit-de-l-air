import os

days = ["05", "06"]
hours = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
         "20", "21", "22", "23"]
hour = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
        "18", "19", "20", "21", "22", "23"]

path = "/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/config"
for root, dirs, files in os.walk(path):
    for file in files:
        os.remove(os.path.join(root, file))
for d in days:
    for p, h in zip(hours, hour):
        config = open("config/" + d + h + ".tcl", "w+")
        config.write(
            "set Data(SpLst)  \"O3\" \n"
            "set Data(TAG1)   \"TEST12.201904_201904_regeta\"\n"
            "set Data(TAG3)   \"" + d + "" + h + "\"\n"
                                                 "set Data(outTXT)       \"SITE\" \n"
                                                 "set Data(levels) \"76696048\"\n"  # todo confirm levels
                                                 "set Data(MandatoryLevels) \"76696048\"\n"
                                                 "set Data(Path)    /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach\n"
                                                 "set Data(PathOut) /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out\n"
                                                 "set Data(Start)      \"" + "2019" + "04" + "\"\n"
                                                                                             "set Data(End)      \"" + "2019" + "04" + "\"\n"
                                                                                                                                       "set Data(Eticket)     \"RAQDPS020\"\n"
                                                                                                                                       "set Data(point) \"" + "Dorval" + "\"\n"
                                                                                                                                                                         "set Data(coord) \"" + "45.47" + " " + "-73.74" + "\"\n"
                                                                                                                                                                                                                           "set Data(days) \"" + str(
                d) + "\"\n"  # todo confirm start day
                     "set Data(hours) \"" + str(p) + "\"\n"
        )

os.system(" ls /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/config | sort -st '/' -k1,1")
for a in os.listdir('config'):
    os.system("./extract1.tcl " + "config/" + a)

#
# for b in os.listdir("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out"):
#     aa = open("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/"+b,"r").read()
#     print(b)


docName = []


def removeEmptyFile(path):
    docList = os.listdir(path)
    for doc in docList:
        docPath = os.path.join(path, doc)
        if os.path.isfile(docPath):
            if os.path.getsize(docPath) == 0:
                os.remove(docPath)
        if os.path.isdir(docPath):
            removeEmptyFile(docPath)


removeEmptyFile(r'/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out')

os.system(
    " ls /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/ | sort -st '/' -k1,1")

alist = sorted(
    os.listdir("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/"))

output = open("output.csv", "w+")
for i in alist:
    b = open("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/" + i,
             "r").read()
    output.write(b)

hourgiven = ["004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018",
             "019", "020"]

tlcHours = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24"]

hour24 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
        "18", "19", "20", "21", "22", "23"]

hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

s = hours.index(hourgiven[0])
e = hours.index(hourgiven[-1])
newl = hour24[s:e + 1]
print(newl)
