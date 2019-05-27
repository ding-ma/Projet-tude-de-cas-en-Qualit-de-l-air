import os

#
#
# days = ["05", "06"]
# hours = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20","21", "22", "23"]
#
# path = "/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/config"
# for root, dirs, files in os.walk(path):
#     for file in files:
#         os.remove(os.path.join(root, file))
# for d in days:
#     for h in hours:
#         config = open("config/config"+d+"_"+h+".tcl", "w+")
#         config.write(
#             "set Data(SpLst)  \"O3\" \n"
#             "set Data(TAG1)   \"TEST00.201904_201904_regeta\"\n"
#             "set Data(TAG3)   \""+d+h+"\"\n"
#             "set Data(outTXT)       \"SITE\" \n"
#             "set Data(levels) \"76696048\"\n"  # todo confirm levels
#             "set Data(MandatoryLevels) \"76696048\"\n"
#             "set Data(Path)    /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach\n"
#             "set Data(PathOut) /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out\n"
#             "set Data(Start)      \"" + "2019" + "04" + "\"\n"
#             "set Data(End)      \"" + "2019" + "04" + "\"\n"
#             "set Data(Eticket)     \"RAQDPS020\"\n"
#             "set Data(point) \"" + "Dorval" + "\"\n"
#             "set Data(coord) \"" + "45.47" + " " + "-73.74" + "\"\n"
#             "set Data(days) \"" + str(d) + "\"\n"  # todo confirm start day
#             "set Data(hours) \""+ str(h) +"\"\n"
#         )

# # for a in os.listdir('config'):
# #     os.system("./extract1.tcl "+"config/"+a)
# #
# # for b in os.listdir("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out"):
# #     aa = open("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/"+b,"r").read()
# #     print(b)
#
#
# # docName = []
# # def removeEmptyFile(path):
# #     docList = os.listdir(path)
# #     for doc in docList:
# #         docPath = os.path.join(path,doc)
# #         if os.path.isfile(docPath):
# #             if os.path.getsize(docPath)==0:
# #                 os.remove(docPath)
# #         if os.path.isdir(docPath):
# #             removeEmptyFile(docPath)
# # removeEmptyFile(r'/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out')
#


a = ['config05_6.tcl', 'config06_12.tcl', 'config05_1.tcl', 'config06_7.tcl', 'config06_23.tcl', 'config06_17.tcl',
     'config06_21.tcl', 'config06_14.tcl', 'config06_1.tcl', 'config05_23.tcl', 'config05_2.tcl', 'config06_15.tcl',
     'config05_4.tcl', 'config06_10.tcl', 'config05_13.tcl', 'config06_8.tcl', 'config06_3.tcl', 'config06_2.tcl',
     'config05_16.tcl', 'config06_20.tcl', 'config05_12.tcl', 'config05_14.tcl', 'config05_3.tcl', 'config05_15.tcl',
     'config06_5.tcl', 'config05_0.tcl', 'config06_18.tcl', 'config05_22.tcl', 'config06_4.tcl', 'config05_11.tcl',
     'config05_8.tcl', 'config05_9.tcl', 'config05_18.tcl', 'config06_11.tcl', 'config05_17.tcl', 'config05_21.tcl',
     'config06_22.tcl', 'config06_9.tcl', 'config05_20.tcl', 'config05_7.tcl', 'config06_13.tcl', 'config06_19.tcl',
     'config06_6.tcl', 'config06_0.tcl', 'config05_19.tcl', 'config05_10.tcl', 'config06_16.tcl', 'config05_5.tcl']

days = ["05", "06"]
hours = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
         "20", "21", "22", "23"]
hour = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
        "18", "19", "20", "21", "22", "23"]

for d in days:
    for p, h in zip(hours, hour):
        file = open("out/" + d + h + ".txt", "w+")
        file.write(p + d)
a = os.listdir("out")
print(a)
