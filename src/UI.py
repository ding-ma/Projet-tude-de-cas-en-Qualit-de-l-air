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
import observations as Ob

#import forecast as Fc

# initial setting
window = tk.Tk()
# window.attributes('-zoomed', True)
#w, h = window.winfo_screenwidth(), window.winfo_screenheight()
w,h = 1025,550
window.geometry("%dx%d+0+0" % (w, h))
window.title("tk")
# window.geometry("1500x1200")
# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.place(x=0,y=0,width=w, height=h)
#nb.grid(row=1, column=0, columnspan=50, rowspan=100, sticky='NESW')


# Adds tab for Gem-Mach
machTab = ttk.Frame(nb)
nb.add(machTab, text="Tool")

#this function just writes all the user input into all files
def GemClicked():
    global particules
    a = enteredDate.get()
    Gm.inputStartDate(a)

    b = enteredEndDate.get()
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
    locID = getComboboxLocation()
    active = False
    Um.particuleCheckBoxAndTime(O3, NO2, PM25, locID,datesplit, active)
    Um.rarcFile(datesplit)

    Umist.removeAllfile(r'' + Umist.filelocation + "/configMIST")
    Umist.time(sTime, eTime)
    Umist.inputStartDate(a)
    Umist.inputEndDate(b)
    Umist.modelCheckbox(h_00, h_12)
    Umist.rarcFile()
    Umist.bashFile(particules,locID)

    Fw.level(levelEntry.get())
    Fw.removeAllfile(r'' + Fw.filelocation + "/configFw")
    Fw.time(sTime, eTime)
    Fw.inputStartDate(a)
    Fw.inputEndDate(b)
    Fw.modelCheckbox(h_00, h_12)
    Fw.rarcFile()
    Fw.bashFile(particules, locID)

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

    Ob.inputStartDate(a)
    Ob.inputEndDate(b)
    Ob.particuleCheckBox(O3, NO2, others, PM25)


startDateLabel = tk.Label(machTab, text="Enter Start Date (YYYY/MM/DD)")
enteredDate = tk.Entry(machTab, width=13)
startDateLabel.place(x=10,y=10)
enteredDate.place(x=210,y=12)

# End date
endDateLabel = tk.Label(machTab, text="Enter End Date (YYYY/MM/DD)")
enteredEndDate = tk.Entry(machTab, width=13)
endDateLabel.place(x=10,y=35)
enteredEndDate.place(x=210,y=38)


# Start Hours
sHourLabel = tk.Label(machTab, text="Choose the start time")
sHourcombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
sHourcombo.current(0)
sHourLabel.place(x=340,y=10)
sHourcombo.place(x=340,y=35)


# End Hours
eHourLabel = tk.Label(machTab, text="Choose the end time")
eHourCombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
eHourCombo.current(0)
eHourLabel.place(x=535,y=10)
eHourCombo.place(x=535,y=35)


# Hour Selection
modelHourLabel = tk.Label(machTab, text="Select model time (UTC)")
var_00 = tk.BooleanVar(value=True)
hours00_Checkbutton = tk.Checkbutton(machTab, text="00", variable=var_00)
var_12 = tk.BooleanVar()
hours12_Checkbutton = tk.Checkbutton(machTab, text="12", variable=var_12)
modelHourLabel.place(x=10,y=70)
hours00_Checkbutton.place(x=165,y=70)
hours12_Checkbutton.place(x=215,y=70)


moleculeLabel = tk.Label(machTab, text="Select desired particules")
otherLabel = tk.Label(machTab, text="Others, add no space e.g. UVTT")
var_O3 = tk.BooleanVar(value=True)
O3_Checkbutton = tk.Checkbutton(machTab, text="O3", variable=var_O3)
var_NO2 = tk.BooleanVar()
NO2_Checkbutton = tk.Checkbutton(machTab, text="NO2", variable=var_NO2)
var_PM25 = tk.BooleanVar()
PM25_Checkbutton = tk.Checkbutton(machTab, text="PM2.5", variable=var_PM25)
otherVariable = tk.Entry(machTab, width=13)

moleculeLabel.place(x=10,y=95)
O3_Checkbutton.place(x=165,y=95)
NO2_Checkbutton.place(x=215,y=95)
PM25_Checkbutton.place(x=265,y=95)

# manual add level
levelLabel = tk.Label(machTab, text="Enter Level (optional)")
levelEntry = tk.Entry(machTab, width=15)

levelLabel.place(x=705,y=10)
levelEntry.place(x=850,y=10)
otherLabel.place(x=10,y=120)
otherVariable.place(x=210,y=120)

# stations
def combined(event):
    Gm.provlist.clear()
    name = comboprov.get()
    provlist = Gm.gettingprovlist(name)
    combostations.config(values=provlist)


locationLabel = ttk.Label(machTab, text="Select Location:")


#province combobox
comboprov = ttk.Combobox(machTab, values=Gm.prov, width=10, state='readonly')
comboprov.bind('<<ComboboxSelected>>', combined)
comboprov.current(0)

#stations from the province combobox
combostations = ttk.Combobox(machTab, values=Gm.gettingprovlist("Province"), width=30, state='readonly')

combostations.current(0)
locationLabel.place(x=340,y=70)
comboprov.place(x=450,y=70)
combostations.place(x=565,y=70)

#suff for the search
displayString = ""
stationSearchField = ttk.Entry(machTab, width=15)
def SearchNameID():
    userInput = stationSearchField.get()
    dString = Gm.SearchNameID(userInput)
    stationSearchLabel.config(text=dString)


stationSearchLabel = tk.Label(machTab, text=displayString)
searchBtn = tk.Button(machTab, text="Search Name or ID", command=SearchNameID)


stationSearchLabel.place(x=630,y=102)
stationSearchField.place(x=500,y=102)
searchBtn.place(x=350,y=100)

#chronos, gem
#east,east@coast@zoom,north@america,north@america@gemmach,west

ImagesLabel = tk.Label(machTab,text = "Select Locations")
var_east = tk.BooleanVar(value=True)
East_Checkbtn = tk.Checkbutton(machTab, text = "East", variable = var_east)
var_eastZoom = tk.BooleanVar()
EastZoom_Checkbtn = tk.Checkbutton(machTab, text = "Zoomed East", variable = var_eastZoom)
var_NA = tk.BooleanVar()
NorthAmerica_Checkbtn = tk.Checkbutton(machTab, text = "North America", variable = var_NA)
var_NAGem = tk.BooleanVar()
NAGem_Checkbtn = tk.Checkbutton(machTab, text = "NA - GEM", variable = var_NAGem)
var_west = tk.BooleanVar()
West_Checkbtn = tk.Checkbutton(machTab, text = "West", variable = var_west)

ImagesLabel.place(x=550,y=365)
NAGem_Checkbtn.place(x=675,y=365)
NorthAmerica_Checkbtn.place(x=775,y=365)
West_Checkbtn.place(x=675,y=385)
East_Checkbtn.place(x=775,y=385)
EastZoom_Checkbtn.place(x=675,y=405)

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


btn = tk.Button(machTab, text="Write to file", command=GemClicked, width=15, height=2, bg = "#4ce30f")
btn.place(x=850,y=50)

GemmachLabel = tk.Label(machTab,text = "Gemmach", font = "13")
GemmachLabel.place(x=50,y=160)
scriptBtn = tk.Button(machTab, text="Start Script", command=StartBash, width=17, height=1)
scriptBtn.place(x=40,y=220)

extrationBtn = tk.Button(machTab, text="Start Extraction", command=StartXRACR, width=17, height=1)
extrationBtn.place(x=40,y=190)


def getLocation():
    # Bk.removeAllfile(r''+Bk.filelocation+"/bash")
    Gm.removeAllfile(r'' + Gm.filelocation + "/config")
    Gm.getEticket()
    locID = getComboboxLocation()
    Gm.locationExtraction(locID)
    Gm.launchTCL()
    Gm.removeEmptyFile(r'' + Gm.filelocation + "/extracted")
    Gm.sortAndGenerate(Gm.filelocation + "/extracted/")


locationBtn = tk.Button(machTab, text="Get data at location", command=getLocation, width=17, height=1)
locationBtn.place(x=40,y=250)


def UMOSClicked():
    for filename in glob.glob("rarc/umos*"):
        os.system("rarc -i " + Gm.filelocation + "/" + filename + " &")


UmosLabel = tk.Label(machTab,text = "UMOS", font = "13")
UmosLabel.place(x=255,y=160)

UMOSBtnExt = tk.Button(machTab, text="Start Extraction", command = UMOSClicked, width=17, height=1)
UMOSBtnExt.place(x=225,y=190)


def UMOSGetLocation():
    locID = getComboboxLocation()
    O3 = var_O3.get()
    NO2 = var_NO2.get()
    PM25 = var_PM25.get()
    b = enteredEndDate.get()
    Gm.inputEndDate(b)
    datesplit = Um.inputEndDate(b)
    active = True
    Um.particuleCheckBoxAndTime(O3, NO2, PM25, locID, datesplit, active)


UMOSBtnGetFile = tk.Button(machTab, text="Get Data at location", command = UMOSGetLocation, width=17, height=1)
UMOSBtnGetFile.place(x=225,y=220)

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
    Umist.TCLConfig(particules,getComboboxLocation())
    Umist.launchTCL()
    Umist.removeEmptyFile(r'' + Umist.filelocation + "/extractedMist")
    Umist.sortAndGenerate(Umist.filelocation + "/extractedMist/")


UmosMist = tk.Label(machTab,text = "UMOS-MIST", font = "13")
UmosMist.place(x=455,y=160)

mistBashBtn = tk.Button(machTab, text = "Bash", command = MISTClicked, width=17, height=1)
mistBashBtn.place(x=438,y=220)

mistExtraction = tk.Button(machTab, text = "Start Extraction", command =MISTRARC, width=17, height=1)
mistExtraction.place(x=438,y=190)

mistTCLBtn = tk.Button(machTab, text = "Get Data Location", command = MistGetLocation,width=17, height=1)
mistTCLBtn.place(x=438,y=250)

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
    Fw.TCLConfig(particules,getComboboxLocation())
    Fw.launchTCL()
    Fw.removeEmptyFile(r'' + Fw.filelocation + "/extractedFw")
    Fw.sortAndGenerate(Fw.filelocation + "/extractedFw/")


FireWork = tk.Label(machTab,text = "FireWork", font = "13")
FireWork.place(x=655,y=160)

fwBashBtn = tk.Button(machTab, text = "Bash", command = FwClicked,width=17, height=1)
fwBashBtn.place(x=638,y=220)

fwRarcBtn = tk.Button(machTab, text = "Rarc", command = FwRarc, width=17, height=1)
fwRarcBtn.place(x=638,y=190)

fwTCLbtn = tk.Button(machTab, text = "Get Data Location", command = FwGetLocation, width=17, height=1)
fwTCLbtn.place(x=638,y=250)

giflst =[]
def getImg():
    Im.generateImage()
    #update list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values=sorted(giflst))


imagesct = tk.Label(machTab,text = "Image Section", font = "17")
imagesct.place(x=10,y=300)

imgextraction = tk.Label(machTab, text ="Gemmach", font = "13")
imgextraction.place(x=50, y=335)
ImgBtn = tk.Button(machTab, text = "Get Images, GM", command = getImg, width=17, height=1)
ImgBtn.place(x=40,y=390)


gifs = os.listdir("output")
for g in gifs:
    if g.endswith(".gif"):
        giflst.append(g)


def getUMOSimg():
    t = UmosImgLocation.get()
    Im.generateUMOSImage(t)
    #this part updates the list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values = sorted(giflst))


def IMRARC():
    os.system("rarc -i " + Gm.filelocation + "/image &")


ImgRarcBtn = tk.Button(machTab, text = "Rarc, Im-Gm", command = IMRARC,width=17, height=1)
ImgRarcBtn.place(x=40,y=360)

def UmosImgRarc():
    os.system("rarc -i " + Gm.filelocation + "/imageUMOS &")


imgUmos = tk.Label(machTab,text = "UMOS", font = "13")
imgUmos.place(x=255,y=335)

ImgUmosRarcBtn = tk.Button(machTab, text = "Rarc, Im-Um", command =UmosImgRarc,width=17, height=1)
ImgUmosRarcBtn.place(x=225,y=360)

UmosImgBtn = tk.Button(machTab, text ="Get img, UM", command = getUMOSimg,width=17, height=1)
UmosImgBtn.place(x=438,y=390)

UmosImgLocation = ttk.Combobox(machTab, values = ["@sfc_", "@sfc@diff_"], state='readonly')
UmosImgLocation.place(x=225,y=393)
UmosImgLocation.current(0)

animateCombo = ttk.Combobox(machTab, values =sorted(giflst),width=55, height=10, state='readonly')
animateCombo.place(x=180,y=453)
#animateCombo.current(0)


def animate():
    index = animateCombo.current()
    os.system("animate output/"+sorted(giflst)[index]+" &")


animateBtn = tk.Button(machTab, text = "Animate GIF", command = animate,width=17, height=1)
animateBtn.place(x=10,y=450)


def getComboboxLocation():
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    locID = locationlst[location]
    return locID


# forecastLocationBtn = tk.Button(fireWorkTab, text = "Get at location, fc", command=forecastGetLocation, width=17, height=1)
# forecastLocationBtn.grid(column=1, row=6)

def RarcObservation():
    os.system("rarc -i " + Gm.filelocation + "/observations &")


def ObservationGetLocation():
    locID = getComboboxLocation()
    Ob.generateFromDB(locID)


obs = tk.Label(machTab,text = "Observations", font = "13")
obs.place(x=855,y=160)
observationRarcBtn = tk.Button(machTab,text = "Rarc, OBS", command=RarcObservation, width=17, height=1)
observationRarcBtn.place(x=838,y=190)

observationLocationBtn = tk.Button(machTab, text = "Get at location, OBS", command=ObservationGetLocation, width=17, height=1)
observationLocationBtn.place(x=838,y=220)

folderdict = {
    "operation.forecasts.firework.mach": "Firework",
    "operation.images.umoscr": "Umos Images",
    "operation.umos.aq.prevision.csv.n2sp3": "Umos NO2, Pre 2017",
    "operation.images.chronos": "Images Gemmach",
    "operation.umos.aq.prevision.csv.o3sp3": "Umos O3, Pre 2017",
    "operation.scribeMat.mist.aq": "Umos-Mist",
    "operation.forecasts.mach": "Gemmach",
    "operation.observations.dbase.surface.airnow": "Observations",
    "operation.umos.aq.prevision.csv.p2sp3": "Umos PM 2.5, Pre 2017",
    "operation.umos.aq.prevision": "Umos, Post 2017"
}



folder_names = []
convertedFolderName = []
def rarcFolderDeletion():
    folder_names.clear()
    convertedFolderName.clear()
    for filename in os.listdir("rarc"):
        if os.path.isdir("rarc/"+filename):
            folder_names.append(filename)
    for folder in folder_names:
        if folder in folderdict:
            f = folderdict[folder]
            convertedFolderName.append(f)
        else:
            folderdict[folder] = folder
            convertedFolderName.append(folder)


def deleteRarcFile():
    rarcFolderDeletion()
    popup = tk.Tk()
    popup.geometry("%dx%d+0+0" % (375, 200))
    popup.wm_title("BE CAREFUL")
    archnames = tk.Label(popup,text = "Select file directory to delete")
    archnames.place(x=85,y=10)
    filelst = ttk.Combobox(popup, values =sorted(convertedFolderName), width = 40, state='readonly')
    filelst.place(x=15,y=50)
    B1 = ttk.Button(popup, text="Cancel", command=popup.destroy, width=10)
    B1.place(x=55,y=160)

    def confirmDelete():
        inv_folderDict = {v: k for k, v in folderdict.items()}
        a = int(filelst.current())
        todel = sorted(convertedFolderName)[a]
        shutil.rmtree("rarc/"+inv_folderDict[todel])
        rarcFolderDeletion()
        popup.destroy()

    b2 = tk.Button(popup, text = "Confirm delete", command = confirmDelete, width=10, bg = 'red')
    b2.place(x=195,y=160)
    popup.mainloop()


deletebtn = tk.Button(machTab, text="Delete Extracted Files", bg = "red", command = deleteRarcFile, width=17, height=2)
deletebtn.place(x=850,y=450)
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
                                     "- This program will automatically generate the working directories and make sure to include the 2 csv files and all .py files!\n",
                     justify = "left")
notesInfo.grid(column=0, row=0)
#https://www.python-course.eu/tkinter_text_widget.php

# img = tk.PhotoImage(file = "smog-montreal.gif")
# imglabal = tk.Label(window,image = img)
# imglabal.grid(column=0, row=50, pady = (325,0), sticky='w')
#imglabal.grid(column=0, row=50, pady = (325,0), sticky='w')
s = ttk.Style()
s.theme_use('classic')
window.mainloop()

# notes: active var for particuleCheckBoxAndTime allowed me to use the same code for different purposes, when you write
# file, you dont want to get the location right now because the file may not be extracted yet
