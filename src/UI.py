#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk

import Gemmach as GM

# initial setting
window = tk.Tk()
# window.attributes('-zoomed', True)
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
# window.geometry("1500x1200")
# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

# Adds tab for Gem-Mach
machTab = ttk.Frame(nb)
nb.add(machTab, text="Gem-Mach")


def Clicked():
    sDate = enteredDate.get()
    GM.inputStartDate(sDate)

    eDate = enteredEndDate.get()
    GM.inputEndDate(eDate)

    sTime = sHourcombo.get()
    eTime = eHourCombo.get()
    GM.time(sTime, eTime)

    h_00 = var_00.get()
    h_12 = var_12.get()
    GM.modelCheckbox(h_00, h_12)

    O3 = var_O3.get()
    NO2 = var_NO2.get()
    others = otherVariable.get()
    PM25 = var_PM25.get()
    GM.particuleCheckBox(O3, NO2, others, PM25)

    GM.level(levelEntry.get())
    GM.rarcFile()

rarcLabel = tk.Label(machTab, text="Rarc Settings", font="20")
rarcLabel.grid(column=0, row=0)
# Start date
startDateLabel = tk.Label(machTab, text="Enter Start Date (YYYY/MM/DD)")
startDateLabel.grid(column=0, row=1)
enteredDate = tk.Entry(machTab, width=13)
enteredDate.grid(column=1, row=1)

# Start date
endDateLabel = tk.Label(machTab, text="Enter End Date (YYYY/MM/DD)")
endDateLabel.grid(column=0, row=2)
enteredEndDate = tk.Entry(machTab, width=13)
enteredEndDate.grid(column=1, row=2)

# Start Hours
sHourLabel = tk.Label(machTab, text="Choose the start time")
sHourLabel.grid(column=2, row=1)
sHourcombo = ttk.Combobox(machTab, values=GM.hours, state='readonly')
sHourcombo.grid(column=2, row=2)
sHourcombo.current(0)

# End Hours
eHourLabel = tk.Label(machTab, text="Choose the end time")
eHourLabel.grid(column=3, row=1, padx=15)
eHourCombo = ttk.Combobox(machTab, values=GM.hours, state='readonly')
eHourCombo.grid(column=3, row=2, padx=15)
eHourCombo.current(0)

# Hour Selection
modelHourLabel = tk.Label(machTab, text="Select model time (UTC)")
modelHourLabel.grid(column=0, row=10)
var_00 = tk.BooleanVar(value=True)
hours00_Checkbutton = tk.Checkbutton(machTab, text="00", variable=var_00)
hours00_Checkbutton.grid(column=1, row=10)
var_12 = tk.BooleanVar()
hours12_Checkbutton = tk.Checkbutton(machTab, text="12", variable=var_12)
hours12_Checkbutton.grid(column=2, row=10)

bashLabel = tk.Label(machTab, text="Bash Script Settings", font="20")
bashLabel.grid(column=0, row=9, pady=(10, 0))
# molecule checkbox
# moleculeList = ("O3", "NO2", "CO", "PM2.5")
# AF in fst, PM 2.5
# N2 for NO2
moleculeLabel = tk.Label(machTab, text="Select desired particules")
moleculeLabel.grid(column=0, row=11)
otherLabel = tk.Label(machTab, text="Others, add no space e.g. UVTT")
otherLabel.grid(column=4, row=11)
var_O3 = tk.BooleanVar(value=True)
O3_Checkbutton = tk.Checkbutton(machTab, text="O3", variable = var_O3)
O3_Checkbutton.grid(column=1, row=11)
var_NO2 = tk.BooleanVar()
NO2_Checkbutton = tk.Checkbutton(machTab, text ="NO2", variable = var_NO2)
NO2_Checkbutton.grid(column=2, row=11)
var_PM25 = tk.BooleanVar()
PM25_Checkbutton = tk.Checkbutton(machTab, text ="PM2.5", variable = var_PM25)
PM25_Checkbutton.grid(column=3, row=11)
otherVariable = tk.Entry(machTab, width=13)
otherVariable.grid(column=5, row=11)

# manual add level
levelLabel = tk.Label(machTab, text="Enter Level (optinal)")
levelLabel.grid(column=4, row=1)
levelEntry = tk.Entry(machTab, width=15)
levelEntry.grid(column=4, row=2)

# stations
def combined(event):
    GM.provlist.clear()
    name = comboprov.get()
    provlist = GM.gettingprovlist(name)
    combostations.config(values=provlist)


comboprov = ttk.Combobox(machTab, values=GM.prov, width=10, state='readonly')
comboprov.grid(column=0, row=14)
comboprov.bind('<<ComboboxSelected>>', combined)
comboprov.current(0)

combostations = ttk.Combobox(machTab, values=GM.gettingprovlist("AB"), width=30, state='readonly')
combostations.grid(column=1, row=14)
combostations.current(1)

locationLabel = ttk.Label(machTab, text = "Get Data At Location", font = 20)
locationLabel.grid(column=0, row=13, pady=(15,0))
# stationCombo = ttk.Combobox(machTab, values=Bk.lstDisplay, state='readonly')
# stationCombo.grid(column=0, row=13, pady=(20, 0))
# stationCombo.current(0)

displayString = "Search Name or ID"
stationSearchField = ttk.Entry(machTab, width=15)
stationSearchField.grid(column=3, row=14, pady=(20, 0))


def SearchNameID():
    userInput = stationSearchField.get()
    displayString = GM.SearchNameID(userInput)
    stationSearchLabel.config(text=displayString)


stationSearchLabel = tk.Label(machTab, text=displayString)
stationSearchLabel.grid(column=2, row=14, pady=(20, 0), padx=(60, 0))
searchBtn = tk.Button(machTab, text="Search", command=SearchNameID)
searchBtn.grid(column=4, row=14, pady=(20, 0))
####


# in order for the command to run on CMC server, it has to be ISOLATED and no passed through functions
# other way works on windows
# os.system("spi")
# Bk.execute("py tests.py")
# Bk.log("py tests.py")
# Bk.execute("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach")


def StartXRACR():
    os.system("rarc -i " + GM.filelocation + "/gemmach &")


def StartBash():
    if GM.bothCheked is 1:
        os.system("./gemmachBashTest00.bash &")
        print("Done, file located at -->" + GM.filelocation + "/bash")
    if GM.bothCheked is 2:
        os.system("./gemmachBashTest12.bash &")
        print("Done, file located at -->" + GM.filelocation + "/bash")
    if GM.bothCheked is 3:
        os.system("./gemmachBashTest00.bash &")
        os.system("./gemmachBashTest12.bash &")
        print("Done, file located at -->" + GM.filelocation + "/bash")


btn = tk.Button(machTab, text="Write to file (1)", command=Clicked, width=15, height=1)
btn.grid(column=10, row=1, pady=5)

scriptBtn = tk.Button(machTab, text="Start Script (3)", command=StartBash, width=15, height=1)
scriptBtn.grid(column=10, row=11, padx=40)

extrationBtn = tk.Button(machTab, text="Start Extraction (2)", command=StartXRACR, width=15, height=1)
extrationBtn.grid(column=10, row=2)


def testing():
    print(os.path.isdir("gem"))


extrationBtn = tk.Button(machTab, text="Check if file exist", command=testing, width=15, height=1)
extrationBtn.grid(column=10, row=3)


def getLocation():
    #Bk.removeAllfile(r''+Bk.filelocation+"/bash")
    GM.removeAllfile(r'' + GM.filelocation + "/config")
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = GM.provinceDic[province]
    loc = locationlst[location]
    GM.locationExtraction(loc)
    GM.launchTCL()
    GM.removeEmptyFile(r'' + GM.filelocation + "/extracted")
    GM.sortAndGenerate(GM.filelocation + "/extracted/")


locationBtn = tk.Button(machTab, text="Get data at location (4)", command=getLocation, width=17, height=1)
locationBtn.grid(column=10, row=14)
###########################################
#           end of Gem-mach Tab           #
###########################################

# tab for UMOS
umosTab = ttk.Frame(nb)
nb.add(umosTab, text="UMOS")

# tab for FireWork
fireWorkTab = ttk.Frame(nb)
nb.add(fireWorkTab, text="FireWork")

# tab for help
help = ttk.Frame(nb)
nb.add(help, text="Help/Info")

gemmachinfo = tk.Label(help, text = "GEMMACH - How it works:\n"
                                    "Step 1: user enters all necesary info\n"
                                    "Step 2: uses RARC command line settings to extract data from CMC server\n"
                                    "Step 3: the bash script will isolate the corresponding polluant into a .fst file \n"
                                    "Step 4: the tcl script will get the polluant data at a specific point on the map \n"
                                    "GEMMACH - INFO:\n"
                                    "- ALWAYS write to file when you are changing some settings\n "
                                    "- Sometimes 00 has bugs, make sure to unselect and reselect it\n"
                                    "- If the .fst already exists, you may skip the according step\n"
                                    "")
gemmachinfo.grid(column=0, row=0)

window.mainloop()
