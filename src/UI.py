#!/usr/bin/env python3
import glob
import os
import shutil
import tkinter as tk
from tkinter import ttk

import FireWork as Fw
import Gemmach as Gm
import Images as Im
import UMOS as Um
import UMOSMist as Umist

# initial setting
window = tk.Tk()
# window.attributes('-zoomed', True)
#w, h = window.winfo_screenwidth(), window.winfo_screenheight()
w,h = 1225,890
window.geometry("%dx%d+0+0" % (w, h))
window.title("NAME")
# window.geometry("1500x1200")
# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.grid(row=1, column=0, columnspan=50, rowspan=100, sticky='NESW')


# Adds tab for Gem-Mach
machTab = ttk.Frame(nb)
nb.add(machTab, text="Gem-Mach")

def sDate():
    year = yearCombo.get()
    month = Gm.monthDict[monthCombo.get()]
    startDate = startDateCombo.get()
    return year+"/"+month+"/"+startDate

def eDate():
    month = Gm.monthDict[monthCombo.get()]
    year = yearCombo.get()
    endDate = endDateCombo.get()
    return year + "/" + month + "/" + endDate

#this function just writes all the user input into all files
def GemClicked():
    a = sDate()
    b = eDate()
    Gm.inputStartDate(a)
    Gm.inputEndDate(b)

    sTime = sHourcombo.get()
    eTime = eHourCombo.get()
    Gm.time(sTime, eTime)

    h_00 = var_00.get()
    h_12 = var_12.get()
    Gm.modelCheckbox(h_00, h_12)

    O3 = var_O3.get()
    NO2 = var_NO2.get()
    others = otherVariable.get()
    PM25 = var_PM25.get()
    particules = Gm.particuleCheckBox(O3, NO2, others, PM25)

    Gm.level(levelEntry.get())
    Gm.rarcFile()

    Um.inputStartDate(a)
    datesplit = Um.inputEndDate(b)
    Um.modelCheckbox(h_00, h_12)
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    loc = locationlst[location]
    active = False
    Um.particuleCheckBoxAndTime(O3, NO2, PM25, loc,datesplit, active)
    Um.rarcFile(datesplit)

    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    loc = locationlst[location]

    Umist.removeAllfile(r'' + Umist.filelocation + "/configMIST")
    Umist.time(sTime, eTime)
    Umist.inputStartDate(a)
    Umist.inputEndDate(b)
    Umist.modelCheckbox(h_00, h_12)
    Umist.rarcFile()
    Umist.bashFile(particules,loc)

    Fw.level(levelEntry.get())
    Fw.removeAllfile(r'' + Fw.filelocation + "/configFw")
    Fw.time(sTime, eTime)
    Fw.inputStartDate(a)
    Fw.inputEndDate(b)
    Fw.modelCheckbox(h_00, h_12)
    Fw.rarcFile()
    Fw.bashFile(particules, loc)

    Im.inputStartDate(a)
    Im.inputEndDate(b)
    Im.time(sTime, eTime)
    Im.modelCheckbox(h_00,h_12)
    Im.particuleCheckBox(O3, NO2, others, PM25)
    East = var_east.get()
    EastZoom = var_eastZoom.get()
    NA = var_NA.get()
    NAGem = var_NAGem.get()
    West = var_west.get()
    Im.locationCheckBox(East,EastZoom,NA,NAGem,West)
    Im.RarcFile()
    Im.UMOSRarcFile()


rarcLabel = tk.Label(machTab, text="Rarc Settings", font="20")
rarcLabel.grid(column=0, row=0)
# Start date
yearCombo = ttk.Combobox(machTab, values = list(Gm.years),state='readonly')
yearCombo.grid(column=0, row=1)
yearCombo.current(18)


# these are binded together in order to dynamicaly change the days displayed according to the year and month
def monthChanger(evt):
    a = sDate()
    b = Gm.inputStartDate(a)
    startDateCombo.config(values =b)
    endDateCombo.config(values =b)


#month combobox
monthCombo = ttk.Combobox(machTab, values = list(Gm.monthDict.keys()), state = 'readonly')
monthCombo.grid(column=1, row=1)
monthCombo.current(0)
monthCombo.bind('<<ComboboxSelected>>', monthChanger)
yearCombo.bind('<<ComboboxSelected>>', monthChanger)


#start date combobox
startDateCombo = ttk.Combobox(machTab, values = Gm.days[1:-2], state = 'readonly')
startDateCombo.grid(column=0, row=2)
startDateCombo.current(0)

#end date combobox
endDateCombo = ttk.Combobox(machTab, values = Gm.days[1:-2], state = 'readonly')
endDateCombo.grid(column=1, row=2)
endDateCombo.current(0)
# Start date
# endDateLabel = tk.Label(machTab, text="Enter End Date (YYYY/MM/DD)")
# endDateLabel.grid(column=0, row=2)
# enteredEndDate = tk.Entry(machTab, width=13)
# enteredEndDate.grid(column=1, row=2)

# Start Hours
sHourLabel = tk.Label(machTab, text="Choose the start time")
sHourLabel.grid(column=2, row=1)
sHourcombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
sHourcombo.grid(column=2, row=2)
sHourcombo.current(0)

# End Hours
eHourLabel = tk.Label(machTab, text="Choose the end time")
eHourLabel.grid(column=3, row=1, padx=15)
eHourCombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
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
O3_Checkbutton = tk.Checkbutton(machTab, text="O3", variable=var_O3)
O3_Checkbutton.grid(column=1, row=11)
var_NO2 = tk.BooleanVar()
NO2_Checkbutton = tk.Checkbutton(machTab, text="NO2", variable=var_NO2)
NO2_Checkbutton.grid(column=2, row=11)
var_PM25 = tk.BooleanVar()
PM25_Checkbutton = tk.Checkbutton(machTab, text="PM2.5", variable=var_PM25)
PM25_Checkbutton.grid(column=3, row=11)
otherVariable = tk.Entry(machTab, width=13)
otherVariable.grid(column=5, row=11)

# manual add level
levelLabel = tk.Label(machTab, text="Enter Level (optional, default: 76696048/93423264)")
levelLabel.grid(column=4, row=1)
levelEntry = tk.Entry(machTab, width=15)
levelEntry.grid(column=4, row=2)


# stations
def combined(event):
    Gm.provlist.clear()
    name = comboprov.get()
    provlist = Gm.gettingprovlist(name)
    combostations.config(values=provlist)


#province combobox
comboprov = ttk.Combobox(machTab, values=Gm.prov, width=10, state='readonly')
comboprov.grid(column=0, row=14)
comboprov.bind('<<ComboboxSelected>>', combined)
comboprov.current(0)

#stations from the province combobox
combostations = ttk.Combobox(machTab, values=Gm.gettingprovlist("AB"), width=30, state='readonly')
combostations.grid(column=1, row=14)
combostations.current(1)

locationLabel = ttk.Label(machTab, text="Get Data At Location", font=20)
locationLabel.grid(column=0, row=13, pady=(15, 0))
# stationCombo = ttk.Combobox(machTab, values=Bk.lstDisplay, state='readonly')
# stationCombo.grid(column=0, row=13, pady=(20, 0))
# stationCombo.current(0)

displayString = "Search Name or ID"
stationSearchField = ttk.Entry(machTab, width=15)
stationSearchField.grid(column=3, row=14, pady=(20, 0))


def SearchNameID():
    userInput = stationSearchField.get()
    dString = Gm.SearchNameID(userInput)
    stationSearchLabel.config(text=dString)


#suff for the search
stationSearchLabel = tk.Label(machTab, text=displayString)
stationSearchLabel.grid(column=2, row=14, pady=(20, 0), padx=(60, 0))
searchBtn = tk.Button(machTab, text="Search", command=SearchNameID)
searchBtn.grid(column=4, row=14, pady=(20, 0))

#chronos, gem
#east,east@coast@zoom,north@america,north@america@gemmach,west

var_east = tk.BooleanVar(value=True)
East_Checkbtn = tk.Checkbutton(machTab, text = "East", variable = var_east)
East_Checkbtn.grid(column=3, row=10)
var_eastZoom = tk.BooleanVar()
EastZoom_Checkbtn = tk.Checkbutton(machTab, text = "Zoomed East", variable = var_eastZoom)
EastZoom_Checkbtn.grid(column=4, row=10)
var_NA = tk.BooleanVar()
NorthAmerica_Checkbtn = tk.Checkbutton(machTab, text = "North America", variable = var_NA)
NorthAmerica_Checkbtn.grid(column=5, row=10)
var_NAGem = tk.BooleanVar()
NAGem_Checkbtn = tk.Checkbutton(machTab, text = "NA - GEM", variable = var_NAGem)
NAGem_Checkbtn.grid(column=6, row=10)
var_west = tk.BooleanVar()
West_Checkbtn = tk.Checkbutton(machTab, text = "West", variable = var_west)
West_Checkbtn.grid(column=7, row=10)
#umos

imageExtCombo = ttk.Combobox(machTab, values = ["east", ""])
####


# in order for the command to run on CMC server, it has to be ISOLATED and no passed through functions
# other way works on windows
# os.system("spi")
# Bk.execute("py tests.py")
# Bk.log("py tests.py")
# Bk.execute("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach")


def StartXRACR():
    os.system("rarc -i " + Gm.filelocation + "/gemmach &")


def StartBash():
    os.system("chmod -R 777 " + Fw.filelocation)
    if Gm.bothCheked is 1:
        os.system("./gemmachBashTest00.bash &")
        print("Done, file located at -->" + Gm.filelocation + "/bash")
    if Gm.bothCheked is 2:
        os.system("./gemmachBashTest12.bash &")
        print("Done, file located at -->" + Gm.filelocation + "/bash")
    if Gm.bothCheked is 3:
        os.system("./gemmachBashTest00.bash &")
        os.system("./gemmachBashTest12.bash &")
        print("Done, file located at -->" + Gm.filelocation + "/bash")


btn = tk.Button(machTab, text="Write to file (1)", command=GemClicked, width=15, height=1)
btn.grid(column=10, row=1, pady=5)

scriptBtn = tk.Button(machTab, text="Start Script (3)", command=StartBash, width=15, height=1)
scriptBtn.grid(column=10, row=11, padx=40)

extrationBtn = tk.Button(machTab, text="Start Extraction (2)", command=StartXRACR, width=15, height=1)
extrationBtn.grid(column=10, row=2)


def testing():
    #print(os.path.isdir("gem"))
    print(sDate())


extrationBtn = tk.Button(machTab, text="Check if file exist", command=testing, width=15, height=1)
extrationBtn.grid(column=10, row=3)


def getLocation():
    # Bk.removeAllfile(r''+Bk.filelocation+"/bash")
    Gm.removeAllfile(r'' + Gm.filelocation + "/config")
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    loc = locationlst[location]
    Gm.locationExtraction(loc)
    Gm.launchTCL()
    Gm.removeEmptyFile(r'' + Gm.filelocation + "/extracted")
    Gm.sortAndGenerate(Gm.filelocation + "/extracted/")


locationBtn = tk.Button(machTab, text="Get data at location (4)", command=getLocation, width=17, height=1)
locationBtn.grid(column=10, row=14)
###########################################
#           end of Gem-mach Tab           #
###########################################

# tab for UMOS
umosTab = ttk.Frame(nb)
nb.add(umosTab, text="UMOS")


def UMOSClicked():
    for filename in glob.glob("rarc/umos*"):
        os.system("rarc -i " + Gm.filelocation + "/" + filename + " &")


UMOSBtnExt = tk.Button(umosTab, text="Start Extraction(1)", command = UMOSClicked, width=17, height=1)
UMOSBtnExt.grid(column=0, row=0)


def UMOSGetLocation():
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    loc = locationlst[location]
    O3 = var_O3.get()
    NO2 = var_NO2.get()
    PM25 = var_PM25.get()
    b = eDate()
    Gm.inputEndDate(b)
    datesplit = Um.inputEndDate(b)
    active = True
    Um.particuleCheckBoxAndTime(O3, NO2, PM25, loc, datesplit, active)


UMOSBtnGetFile = tk.Button(umosTab, text="Get Data at location (2)", command = UMOSGetLocation, width=17, height=1)
UMOSBtnGetFile.grid(column=0, row=1)

def MISTClicked():
    os.system("chmod -R 777 " + Fw.filelocation)
    if Umist.bothCheked is 1:
        os.system("./UmosMist00.bash &")
        print("Done, file located at -->" + Umist.filelocation + "/bash")
    if Umist.bothCheked is 2:
        os.system("./UmosMist12.bash &")
        print("Done, file located at -->" + Umist.filelocation + "/bash")
    if Umist.bothCheked is 3:
        os.system("./UmosMist00.bash &")
        os.system("./UmosMist12.bash &")
        print("Done, file located at -->" + Umist.filelocation + "/bash")


def MISTRARC():
    os.system("rarc -i " + Umist.filelocation + "/UMist &")

def MistGetLocation():
    shutil.rmtree("extractedMist")
    os.mkdir("extractedMist")
    Umist.launchTCL()
    Umist.removeEmptyFile(r'' + Umist.filelocation + "/extractedMist")
    Umist.sortAndGenerate(Umist.filelocation + "/extractedMist/")


mistBashBtn = tk.Button(umosTab, text = "Bash - Mist", command = MISTClicked, width=17, height=1)
mistBashBtn.grid(column=3, row=1)

mistExtraction = tk.Button(umosTab, text = "Start Extraction, Mist", command =MISTRARC, width=17, height=1)
mistExtraction.grid(column=2, row=0)

mistTCLBtn = tk.Button(umosTab, text = "Get Data Location, Mist", command = MistGetLocation,width=17, height=1)
mistTCLBtn.grid(column=2, row=1)

# tab for FireWork
def FwRarc():
    os.system("rarc -i " + Umist.filelocation + "/FireWork &")

def FwClicked():
    os.system("chmod -R 777 " + Fw.filelocation)
    if Fw.bothCheked is 1:
        os.system("./FireWork00.bash &")
        print("Done, file located at -->" + Fw.filelocation + "/bash")
    if Fw.bothCheked is 2:
        os.system("./FireWork12.bash &")
        print("Done, file located at -->" + Fw.filelocation + "/bash")
    if Fw.bothCheked is 3:
        os.system("./FireWork00.bash &")
        os.system("./FireWork12.bash &")
        print("Done, file located at -->" + Fw.filelocation + "/bash")

def FwGetLocation():
    shutil.rmtree("extractedFw")
    os.mkdir("extractedFw")
    Fw.launchTCL()
    Fw.removeEmptyFile(r'' + Fw.filelocation + "/extractedFw")
    Fw.sortAndGenerate(Fw.filelocation + "/extractedFw/")


fireWorkTab = ttk.Frame(nb)
nb.add(fireWorkTab, text="FireWork")

fwBashBtn = tk.Button(fireWorkTab, text = "Bash Fw", command = FwClicked,width=17, height=1)
fwBashBtn.grid(column=0, row=1)

fwRarcBtn = tk.Button(fireWorkTab, text = "Rarc, Fw", command = FwRarc, width=17, height=1)
fwRarcBtn.grid(column=0, row=0)

fwTCLbtn = tk.Button(fireWorkTab, text = "Get Data Location, Fw", command = FwGetLocation, width=17, height=1)
fwTCLbtn.grid(column=1, row=0)

giflst =[]
def getImg():
    location = ImgCombo.get()
    Im.generateImage(location)
    #update list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values=sorted(giflst))


ImgCombo = ttk.Combobox(fireWorkTab, values=["east", "west","north@america", "north@america@gemmach"], width=20, state='readonly')
ImgCombo.grid(column=1, row=2)
ImgCombo.current(0)

ImgBtn = tk.Button(fireWorkTab, text = "Get Images, GM", command = getImg, width=17, height=1)
ImgBtn.grid(column=1, row=1)

UmosImgCombo = ttk.Combobox(fireWorkTab, values=["north@america", "east", "west", "north@america@gemmach"], state='readonly')
UmosImgCombo.grid(column=0, row=3)
UmosImgCombo.current(0)

UmosImgLocation = ttk.Combobox(fireWorkTab, values = ["@sfc_", "@sfc@diff_"], state='readonly')
UmosImgLocation.grid(column=1, row=3)
UmosImgLocation.current(0)

gifs = os.listdir("output")
for g in gifs:
    if g.endswith(".gif"):
        giflst.append(g)


def getUMOSimg():
    t = UmosImgCombo.get()
    location = UmosImgLocation.get()
    Im.generateUMOSImage(t,location)
    #this part updates the list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values = sorted(giflst))


UmosImgBtn = tk.Button(fireWorkTab, text ="Get img, UM", command = getUMOSimg,width=17, height=1)
UmosImgBtn.grid(column=0, row=4)

def IMRARC():
    os.system("rarc -i " + Gm.filelocation + "/image &")


ImgRarcBtn = tk.Button(fireWorkTab, text = "Rarc, Im-Gm", command = IMRARC,width=17, height=1)
ImgRarcBtn.grid(column=0, row=1)

def UmosImgRarc():
    os.system("rarc -i " + Gm.filelocation + "/imageUMOS &")


ImgUmosRarcBtn = tk.Button(fireWorkTab, text = "Rarc, Im-Um", command =UmosImgRarc,width=17, height=1)
ImgUmosRarcBtn.grid(column=0, row=2)


animateCombo = ttk.Combobox(fireWorkTab, values =sorted(giflst),width=45, height=10, state='readonly')
animateCombo.grid(column=1, row=5)
#animateCombo.current(0)


def animate():
    index = animateCombo.current()
    os.system("animate output/"+sorted(giflst)[index]+" &")


animateBtn = tk.Button(fireWorkTab, text = "Animate GIF", command = animate,width=17, height=1)
animateBtn.grid(column=0, row=5)
# tab for help
helptab = ttk.Frame(nb)
nb.add(helptab, text="Help/Info", )

gemmachinfo = tk.Label(helptab, text="GEMMACH - How it works:\n"
                                     "Step 1: user enters all necesary info\n"
                                     "Step 2: uses RARC command line settings to extract data from CMC server\n"
                                     "Step 3: the bash script will isolate the corresponding polluant into a .fst file \n"
                                     "Step 4: the tcl script will get the polluant data at a specific point on the map \n"
                                     "\nGEMMACH - INFO:\n"
                                     "- ALWAYS write to file when you are changing some settings\n "
                                     "- Sometimes 00 has bugs, make sure to unselect and reselect it\n"
                                     "- If the .fst already exists, you may skip the according step\n"
                                     ,justify = "left")
gemmachinfo.grid(column=0, row=2,sticky='w')

umosinfo = tk.Label(helptab, text = "UMOS - How it works:\n"
                                    "Step 1: Takes all the information entered with \"Write to file (1)\" in Gem tab\n"
                                    "Step 2: Use Rarc if the files are not extracted already\n"
                                    "Step 3: Get the data at the chosen station\n"
                                    "\nUMOS Info\n"
                                    "There is a separation of file directory in the archives at 2017 Jan 07\n"
                                    "But the output and functionality of the application still remains the same\n"
                                    "UMOSTreating Folder is a temporary folder, it is normal that there are no files in it because they are deleted after the app finish running\n"
                    ,justify = "left")
umosinfo.place(x=425,y=315)

umosMistinfo = tk.Label(helptab, text = "UMOS-Mist - How it works:\n"
                                        "Same concept as Gemmach\n"
                                        "Step 1: Takes all the information entered with \"Write to file (1)\" in Gem tab\n"
                                        "Step 2: Use Rarc if the files are not extracted already\n"
                                        "Step 3: Use the Bash button to isolate the interested molecule and level \n"
                                        "Step 4: Get the data at the chosen station\n"
                        ,justify = "left")
umosMistinfo.grid(column=0, row=1, sticky='w')

fwInfo = tk.Label(helptab, text = "FireWork - How it works: \n"
                                  "Same concept as Gemmach\n"
                                  "The files are automatically generated from the gemmach tab\n"
                                  "Step 1: use extract file if the files are not extracted\n"
                                  "Step 2: Use the Bash button to isolate the interested molecule and level\n"
                                  "Step 3: Get the data at the chosen station\n"
                                  "! Warning! FireWork model does not run all year long, it might be normal if \nit gives you nothing if you try to run this in the middle of the winter :)"
                  ,justify = "left")
fwInfo.place(x=425,y=180)
#fwInfo.grid(column=1, row=1)
notesInfo = tk.Label(helptab, text = "Notes:\n"
                                     "-If you want the data at another location, change it in the Gemmach Tab and press WRITE TO FILE so it updates everything, "
                                     "you do not need to go through the entire process again. \nJust press \"get data at location\" it will generate a new csv file with the new station\n"
                                     "- By default the level value are: 93423264(before Septemember 9 2016) 76696048 (After that date)\n"
                                     "- Always consult the commandline text of the program to see what is going on\n"
                                     "- It is normal that there is error #8 while running Gemmach,UmosMist, and FireWork script for getting data at location"
                                     "since they rely on some empty fields\n"
                                     "- If RARC gives you a grand total of 0, it means that the file already exists in the folder OR the file does not exis in the archives\n"
                                     "- If there are hours that needs to be added, consult Gemmach.py file, make sure to add the time to 3 lists\n"
                                     "- if there are stations that needs to be added, add them to the \"station_DB.csv\", add them to the END and fill the entire ROW with the corresponding data\n"
                                     "- If the eticket needs to be changed, see Gemmach.py to change them\n"
                                     "- This program will automatically generate the working directories and make sure to include the 2 csv files!\n",
                     justify = "left")
notesInfo.grid(column=0, row=0)
#https://www.python-course.eu/tkinter_text_widget.php

img = tk.PhotoImage(file = "smog-montreal.gif")
imglabal = tk.Label(window,image = img)
imglabal.grid(column=0, row=50, pady = (325,0), sticky='w')
#imglabal.grid(column=0, row=50, pady = (325,0), sticky='w')
window.mainloop()

# notes: active var for particuleCheckBoxAndTime allowed me to use the same code for different purposes, when you write
# file, you dont want to get the location right now because the file may not be extracted yet
