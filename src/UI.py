#!/usr/bin/env python3
import csv
import datetime
import logging
import os
import tkinter as tk
from tkinter import ttk

import Backend as Bk

# initial setting
window = tk.Tk()
window.title("Welcome")
window.geometry('800x600')

logging.basicConfig(filename='logs.log', level=logging.DEBUG)
logging.info("Program Launched: " + str(datetime.datetime.now()))

# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

# Adds tab for Gem-Mach
machTab = ttk.Frame(nb)
nb.add(machTab, text="Gem-Mach")


def Clicked():
    sDate = enteredDate.get()
    Bk.inputStartDate(sDate)

    eDate = enteredEndDate.get()
    Bk.inputEndDate(eDate)

    sTime = sHourcombo.get()
    eTime = eHourCombo.get()
    Bk.time(sTime, eTime)

    h_00 = var_00.get()
    h_12 = var_12.get()
    Bk.modelCheckbox(h_00, h_12)

    O3 = var_O3.get()
    NO2 = var_NO2.get()
    others = otherVariable.get()
    PM25 = var_PM25.get()
    Bk.particuleCheckBox(O3, NO2, others, PM25)

    Bk.rarcFile()


# Start date
startDateLabel = tk.Label(machTab, text="Enter Start Date in YYYY/MM/DD format")
startDateLabel.grid(column=0, row=0)
enteredDate = tk.Entry(machTab, width=13)
enteredDate.grid(column=1, row=0)

# Start date
endDateLabel = tk.Label(machTab, text="Enter End Date in YYYY/MM/DD format")
endDateLabel.grid(column=0, row=1)
enteredEndDate = tk.Entry(machTab, width=13)
enteredEndDate.grid(column=1, row=1)

# execute button
btn = tk.Button(machTab, text="Write to file", command=Clicked, width=20, height=5)
btn.grid(column=10, row=10)

hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

# Start Hours
sHourLabel = tk.Label(machTab, text="Choose the start time")
sHourLabel.grid(column=5, row=4)
sHourcombo = ttk.Combobox(machTab, values=hours, state='readonly')
sHourcombo.grid(column=5, row=5)
sHourcombo.current(0)

# End Hours
eHourLabel = tk.Label(machTab, text="Choose the end time")
eHourLabel.grid(column=7, row=4)
eHourCombo = ttk.Combobox(machTab, values=hours, state='readonly')
eHourCombo.grid(column=7, row=5)
eHourCombo.current(0)

# Hour Selection
modelHourLabel = tk.Label(machTab, text="Select model time (UTC)")
modelHourLabel.grid(column=0, row=7)
var_00 = tk.BooleanVar(value=True)
hours00_Checkbutton = tk.Checkbutton(machTab, text="00", variable=var_00)
hours00_Checkbutton.grid(column=1, row=7)
var_12 = tk.BooleanVar()
hours12_Checkbutton = tk.Checkbutton(machTab, text="12", variable=var_12)
hours12_Checkbutton.grid(column=2, row=7)

# molecule checkbox
# moleculeList = ("O3", "NO2", "CO", "PM2.5")
# AF in fst, PM 2.5
# N2 for NO2
moleculeLabel = tk.Label(machTab, text="Select desired particules(for others, add no space e.g. UVTT)")
moleculeLabel.grid(column=0, row=8)
var_O3 = tk.BooleanVar(value=True)
O3_Checkbutton = tk.Checkbutton(machTab, text="O3", variable = var_O3)
O3_Checkbutton.grid(column=1, row=8)
var_NO2 = tk.BooleanVar()
NO2_Checkbutton = tk.Checkbutton(machTab, text ="NO2", variable = var_NO2)
NO2_Checkbutton.grid(column=2, row=8)
var_PM25 = tk.BooleanVar()
PM25_Checkbutton = tk.Checkbutton(machTab, text ="PM2.5", variable = var_PM25)
PM25_Checkbutton.grid(column=3, row=8)
otherVariable = tk.Entry(machTab, width=13)
otherVariable.grid(column=4, row=8)

# station list display
# TODO not done yet
# maybe create a class
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

stationCombo = ttk.Combobox(machTab, values=lstDisplay, state='readonly')
stationCombo.grid(column=1, row=15)
####


# in order for the command to run on CMC server, it has to be ISOLATED and no passed through functions
# other way works on windows
# os.system("spi")
# Bk.execute("py tests.py")
# Bk.log("py tests.py")
# Bk.execute("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach")


# logging doesnt work on linux server
def Log():
    myCmd = os.popen("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach").read()
    logging.info(myCmd)


def StartXRACR():
    os.system("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach &")


extrationBtn = tk.Button(machTab, text="Start Extraction", command=StartXRACR, width=20, height=5)
extrationBtn.grid(column=10, row=11)


def StartBash():
    os.system("./gemmachBashTest.bash &")


scriptBtn = tk.Button(machTab, text="Start Script", command=StartBash, width=20, height=5)
scriptBtn.grid(column=11, row=11)
###########################################
#           end of Gem-mach Tab           #
###########################################

# tab for UMOS
umosTab = ttk.Frame(nb)
nb.add(umosTab, text="UMOS")

# tab for FireWork
fireWorkTab = ttk.Frame(nb)
nb.add(fireWorkTab, text="FireWork")

window.mainloop()
