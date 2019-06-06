import csv
import re

stationFile = open("aaaa.csv", "r")
reader = csv.reader(stationFile)
stationList = list(reader)
# creates list based on csv entry
lstID = []
lstName = []
#lstDisplay is for the UI
lstDisplay = []
lstLatitude = []
lstLongitude = []
lstProvince = []
for x in range(len(stationList)):
    line = stationList[x]
    ids = line[0]
    name = line[1]
    latitude = line[3]
    longitude = line[4]
    province = line[5]
    lstDisplay.append(ids + ": " + name)
    lstID.append(ids)
    lstName.append(name)
    lstLatitude.append(latitude)
    lstLongitude.append(longitude)
    lstProvince.append(province)


def findx(input):
    i = 0
    for r in lstName:
        if re.search(input, r):
            return i
        i = i + 1


st = "Toronto Downtown"
index = findx(" "+st)
print(lstID[index])