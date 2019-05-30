# import os
# import csv
#
# filelocation = os.getcwd()
#
# # for l in os.listdir(filelocation+"/rarc/operation.umos.aq.prevision/prevision.csv"):
# #     for f in os.listdir(filelocation+"/rarc/operation.umos.aq.prevision/prevision.csv/"+l):
# #         print(f)
# mollst = ["O3", "N2", "P2"]
# date = "20190304"
# passe = "00"
# for ss in mollst:
#     os.system("cmcarc -x 'prevision.csv/"+ss.lower()+"sp3.*' -f "+filelocation+"/rarc/operation.umos.aq.prevision/"+date+passe+"_")
#
#
# stationEntered = "105001"
#
# file = open("UMOS_Ref.csv", "r")
# reader = csv.reader(file)
# UMOSRefList = list(reader)
# lstStationID = []
# lstUMOSID = []
#
# for x in range(len(UMOSRefList)):
#     line = UMOSRefList[x]
#     stationID = line[1]
#     lstStationID.append(stationID)
#     UMOSID = line[2]
#     lstUMOSID.append(UMOSID)
#
# referenceDict = dict(zip(lstStationID,lstUMOSID))
#
# val = referenceDict[stationEntered]
#
# for sub in os.listdir("prevision.csv"):
#     for file in os.listdir("prevision.csv/"+sub):
#         os.system("cat "+filelocation+"/prevision.csv/"+sub+"/"+file +"| grep "+val+" > "+filelocation+"/UMOSTreating/"+file+sub)
#     for untreated in os.listdir("UMOSTreating"):
#         with open("UMOSTreating/"+untreated, "r") as infile, open("output/UMOS__"+untreated+".csv",'w') as outfile:
#             for line in infile:
#                 withcomma = line.replace('|',',')
#                 withoutspace = withcomma.replace(" ", "")
#                 changeName = withoutspace.replace(val, stationEntered)
#                 outfile.write(changeName)


import datetime
import re
inputdate ="03"
form = re.split("0", inputdate)

ini = datetime.date(2016,int(form[1]),30)
end = ini+datetime.timedelta(days=4)
if len(str(end.month)) !=2:
    a = "0"+str(end.month)
    print(a)
