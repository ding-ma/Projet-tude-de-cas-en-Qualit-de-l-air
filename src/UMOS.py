import csv

file = open("UMOS_Ref.csv", "r")
reader = csv.reader(file)
UMOSRefList = list(reader)

lstStationID = []
lstUMOSID = []
for x in range(len(UMOSRefList)):
    line = UMOSRefList[x]
    stationID = line[1]
    lstStationID.append(stationID)
    UMOSID = line[2]
    lstUMOSID.append(UMOSID)

referenceDict = dict(zip(lstUMOSID,lstStationID))

lstofref = ["SJO", "MOC","HAM"]

for l in lstofref:
    print(referenceDict[l])
