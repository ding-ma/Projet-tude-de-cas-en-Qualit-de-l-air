import csv
import difflib
import re

stationFile = open("stations.csv", "r")
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
        difflib.get_close_matches(input, str(r))
        if re.search(input, r):
            return i
        i = i + 1

while True:
    a = difflib.get_close_matches(input(), lstName, n=1, cutoff=.4)
    print(a)
    # ids = lstName.index(a[0])
    # print(lstID[ids])
