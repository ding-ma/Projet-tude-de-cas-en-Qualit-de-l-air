import csv
import re
import string
stationFile = open("stationList-ASCII.csv", "r")
reader = csv.reader(stationFile)
stationList = list(reader)

lstID = []
lstName = []
lstDisplay = []
lstLatitude = []
lstLongitude = []
for x in range(len(stationList)):
    line = stationList[x]
    ids = line[0]
    name = line[1]
    latitude = line[2]
    longitude = line[3]
    lstDisplay.append(ids + ": " + name)
    lstID.append(ids)
    lstName.append(name)
    lstLatitude.append(latitude)
    lstLongitude.append(longitude)


def findWithStation(station):
    index = isStationFound(string.capwords(station))
    if index is False:
        print("Name does not exist")
    else:
        stationID = lstID[index]
        stationLongitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        print(string.capwords(station) + " " + stationID + " " + stationLatitude + " " + stationLongitude)


def isStationFound(StationInput):
    if StationInput in lstName:
        return lstName.index(StationInput)
    return False


def findWithID(ID):
    index = isIDFound(ID)
    if index is False:
        print("ID does not exist")
    else:
        stationName = lstName[index]
        stationLongtitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        print(stationName + " " + ID + " " + stationLatitude + " " + stationLongtitude)


def isIDFound(IDinput):
    if IDinput in lstID:
        return lstID.index(IDinput)
    return False


while True:
    userInput = input()
    # regex to deternime if input is a number of string
    patten = re.compile('\D')
    if patten.findall(userInput):
        findWithStation(userInput)
    else:
        findWithID(userInput)
