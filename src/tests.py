import csv
import re
import string
import tkinter as tk
from tkinter import ttk

stationFile = open("stations_DB.csv", "r")
reader = csv.reader(stationFile)
stationList = list(reader)

# creates list based on csv entry
lstID = []
lstName = []
# lstDisplay is for the UI
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


# search algorithm
def findWithStation(station):
    index = isStationFound(string.capwords(station))
    if index is False:
        return "ID not found, invalid station name"
    else:
        # with the index, we can get the other values since all corresponding data are stored at the same index for the same value
        stationID = lstID[index]
        stationLongitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        return string.capwords(station) + " (" + stationID + ") Lat: " + stationLatitude + " Lon: " + stationLongitude


# returns the index of the item if it exist else, it returns false, gets around the item out of bound problem
def isStationFound(StationInput):
    if StationInput in lstName:
        return lstName.index(StationInput)
    return False


# same logic for searching with ID
def findWithID(ID):
    index = isIDFound(ID)
    if index is False:
        return "Station name not found, invalid ID"
    else:
        stationName = lstName[index]
        stationLongtitude = lstLongitude[index]
        stationLatitude = lstLatitude[index]
        return stationName + " (" + ID + ") Lat: " + stationLatitude + " Lon: " + stationLongtitude


def isIDFound(IDinput):
    if IDinput in lstID:
        return lstID.index(IDinput)
    return False


# returning the found list
def SearchNameID(userInput):
    # ignores all digit
    patten = re.compile('\D')
    # if there are no digit, search by name. else, search with ID
    if patten.findall(userInput):
        return findWithStation(userInput)
    else:
        return findWithID(userInput)


lstNL = []
lstPEI = []
lstNS = []
lstNB = []
lstQC = []
lstONT = []
lstMAN = []
lstSASK = []
lstALB = []
lstBC = []
lstYK = []
lstNWT = []
lstNVT = []
j = 0
for i in lstProvince:
    if i == "1":
        a = lstID[j]
        lstNL.append(a)
    if i == "2":
        b = lstID[j]
        lstPEI.append(b)
    if i == "3":
        c = lstID[j]
        lstNS.append(c)
    if i == "4":
        d = lstID[j]
        lstNB.append(d)
    if i == "5":
        q = lstID[j]
        lstQC.append(q)
    if i == "6":
        w = lstID[j]
        lstONT.append(w)
    if i == "7":
        e = lstID[j]
        lstMAN.append(e)
    if i == "8":
        r = lstID[j]
        lstSASK.append(r)
    if i == "9":
        t = lstID[j]
        lstALB.append(t)
    if i == "10":
        y = lstID[j]
        lstBC.append(y)
    if i == "11":
        u = lstID[j]
        lstNWT.append(u)
    if i == "12":
        o = lstID[j]
        lstYK.append(o)
    if i == "13":
        p = lstID[j]
        lstNVT.append(p)
    j = j + 1

for m in lstQC:
    indexofitem = lstID.index(m)
    name = lstName[indexofitem]
    ids = lstID[indexofitem]

province = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia',
            'Ontario',
            'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Nunavut', 'Yukon']

provinceDic = {
    "AB": lstALB,
    "BC": lstBC,
    "MB": lstMAN,
    "NB": lstNB,
    'NL': lstNL,
    "NS": lstNS,
    "ON": lstONT,
    "PE": lstPEI,
    "QC": lstQC,
    "SK": lstSASK,
    "NT": lstNWT,
    "NU": lstNVT,
    "YT": lstYK
}

testlst = []


def abca(prov):
    for y in provinceDic[prov]:
        indexofitem = lstID.index(y)
        display = lstDisplay[indexofitem]
        testlst.append(display)
    return testlst


window = tk.Tk()
# window.attributes('-zoomed', True)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()


# todo: optimize
# optimize this thing, we should be able to get the k,v pair of the dictionary directly from the combobox but i dont know how
# did a really big workaround for dynamically updating the other list too

def vv(event):
    testlst.clear()
    aaaa = comboprov.get()
    abca(aaaa)
    combostations.config(values=testlst)


trylist = ["AB", "BC", "MB", "NB", 'NL', "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT"]

comboprov = ttk.Combobox(window, values=trylist, width=10, state='readonly')
comboprov.grid(column=2, row=2)
comboprov.bind('<<ComboboxSelected>>', vv)
comboprov.current(0)

combostations = ttk.Combobox(window, values=lstDisplay, width=30, state='readonly')
combostations.grid(column=3, row=2)
combostations.current(1)

window.geometry("%dx%d+0+0" % (w, h))

window.mainloop()
