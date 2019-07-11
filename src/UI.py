#!/usr/bin/env python3
import glob
import os
import pickle
import shutil
import tkinter as tk
from tkinter import ttk

import FireWork as Fw
import Gemmach as Gm
import Images as Im
import UMOS as Um
import UMOSMist as Umist
import observations as Ob

##loading Pickle





# initial setting
window = tk.Tk()
# window.attributes('-zoomed', True)
#w, h = window.winfo_screenwidth(), window.winfo_screenheight()
w,h = 1025,600
window.geometry("%dx%d+0+0" % (w, h))
window.title("Automatic Image and Data Extraction - AIDE")
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
    btn.config(text="Update")
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

    selectDate.config(values = Gm.returnDateList())

    Um.inputStartDate(a)
    datesplit = Um.inputEndDate(b)
    Um.modelCheckbox(h_00, h_12)
    locID = getComboboxLocation()
    active = False
    Um.particuleCheckBoxAndTime(O3, NO2, PM25, locID,datesplit, active)
    Um.rarcFile(datesplit)

    Fw.level(levelEntry.get())
    Fw.removeAllfile(r'' + Fw.filelocation + "/configFw")
    Fw.time(sTime, eTime)
    Fw.inputStartDate(a)
    Fw.inputEndDate(b)
    Fw.modelCheckbox(h_00, h_12)
    Fw.rarcFile()

    Im.inputStartDate(a)
    Im.inputEndDate(b)
    Im.time(sTime, eTime)
    Im.modelCheckbox(h_00, h_12)
    Im.particuleCheckBox(O3, NO2, others, PM25)
    East = var_east.get()
    EastZoom = var_eastZoom.get()
    NA = var_NA.get()
    NAGem = var_NAGem.get()
    West = var_west.get()
    QcOnt = var_QCOnt.get()
    Im.locationCheckBox(East, EastZoom, NA, NAGem, West, QcOnt)
    Im.RarcFile()
    Im.UMOSRarcFile()

    Ob.inputStartDate(a)
    Ob.inputEndDate(b)
    Ob.particuleCheckBox(O3, NO2, others, PM25)

    Umist.removeAllfile(r'' + Umist.filelocation + "/configMIST")
    Umist.time(sTime, eTime)

    Umist.modelCheckbox(h_00, h_12)
    Umist.inputStartDate(a)
    Umist.inputEndDate(b)



def getdate():
    ind = int(selectDate.current())
    return Gm.returnDateList()[int(selectDate.current())]


selectDate = ttk.Combobox(machTab, values = ["No Date Entered"],state='readonly', width=25)
selectDate.place(x=370,y=195)
selectDate.current(0)

selectDateLabel = tk.Label(machTab, text = "Select a date to treat (UMOS-MIST, Gemmach, FireWork)")
selectDateLabel.place(x=10,y=195)

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


moleculeLabel = tk.Label(machTab, text="Select desired pollutants")
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
searchBtn = tk.Button(machTab, text="Search Station Name or ID", command=SearchNameID)


stationSearchLabel.place(x=680,y=102)
stationSearchField.place(x=550,y=102)
searchBtn.place(x=350,y=100)

separetorline = ttk.Label(machTab,text="________________________________________________________________________________________________________________________________________________________________________________________________________________")
separetorline.place(x=0,y=170)

separetorline1 = ttk.Label(machTab,text="________________________________________________________________________________________________________________________________________________________________________________________________________________")
separetorline1.place(x=0,y=325)
#chronos, gem
#east,east@coast@zoom,north@america,north@america@gemmach,west

ImagesLabel = tk.Label(machTab,text = "Select Locations:")
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
var_QCOnt = tk.BooleanVar()
QCOnt_CheckBtn = tk.Checkbutton(machTab, text = "QC-Ont, Umos only", variable = var_QCOnt)


ImagesLabel.place(x=675,y=390)
NAGem_Checkbtn.place(x=675,y=415)
NorthAmerica_Checkbtn.place(x=775,y=415)
West_Checkbtn.place(x=675,y=435)
East_Checkbtn.place(x=775,y=435)
EastZoom_Checkbtn.place(x=675,y=455)
QCOnt_CheckBtn.place(x=775,y=455)

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
    Gm.bashFile(getdate())
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


btn = tk.Button(machTab, text="Enter Parameters", command=GemClicked, width=15, height=2, bg = "#4ce30f")
btn.place(x=850,y=50)

GemmachLabel = tk.Label(machTab,text = "Gemmach", font = "13")
GemmachLabel.place(x=40,y=235)
scriptBtn = tk.Button(machTab, text="Get Chosen Pollutants", command=StartBash, width=17, height=1)
scriptBtn.place(x=40,y=270)

extrationBtn = tk.Button(machTab, text="Gemmach Extraction", command=StartXRACR, width=17, height=1)
extrationBtn.place(x=40,y=150)


def getLocation():
    # Bk.removeAllfile(r''+Bk.filelocation+"/bash")
    Gm.removeAllfile(r'' + Gm.filelocation + "/config")
    Gm.getEticket()
    locID = getComboboxLocation()
    Gm.locationExtraction(locID,getdate())
    Gm.launchTCL()
    Gm.removeEmptyFile(r'' + Gm.filelocation + "/extracted")
    Gm.sortAndGenerate(Gm.filelocation + "/extracted/", getdate())


locationBtn = tk.Button(machTab, text="Get data at Station", command=getLocation, width=17, height=1)
locationBtn.place(x=40,y=300)


def UMOSClicked():
    for filename in glob.glob("rarc/umos*"):
        os.system("rarc -i " + Gm.filelocation + "/" + filename + " &")


UmosLabel = tk.Label(machTab,text = "UMOS", font = "13")
UmosLabel.place(x=638,y=235)

UMOSBtnExt = tk.Button(machTab, text="UMOS Extraction", command = UMOSClicked, width=17, height=1)
UMOSBtnExt.place(x=638,y=150)


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


UMOSBtnGetFile = tk.Button(machTab, text="Get data at Station", command = UMOSGetLocation, width=17, height=1)
UMOSBtnGetFile.place(x=638,y=270)

def MISTClicked():
    Umist.bashFile(particules, getdate())
    os.system("chmod -R 744 " + Umist.filelocation)
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
    Umist.rarcFile()
    os.system("rarc -i " + Umist.filelocation + "/UMist &")

def MistGetLocation():
    Umist.writeEticket(getdate())
    shutil.rmtree("extractedMist")
    os.mkdir("extractedMist")
    os.system("./UmosMistEticket.tcl")
    Umist.TCLConfig(particules,getComboboxLocation(),getdate())
    Umist.launchTCL()
    Umist.removeEmptyFile(r'' + Umist.filelocation + "/extractedMist")
    Umist.sortAndGenerate(Umist.filelocation + "/extractedMist/",getdate())


UmosMist = tk.Label(machTab,text = "UMOS-MIST", font = "13")
UmosMist.place(x=438,y=235)

mistBashBtn = tk.Button(machTab, text = "Get Chosen Pollutants", command = MISTClicked, width=17, height=1)
mistBashBtn.place(x=438,y=270)

mistExtraction = tk.Button(machTab, text = "UMOS-Mist Extraction", command =MISTRARC, width=17, height=1)
mistExtraction.place(x=438,y=150)

mistTCLBtn = tk.Button(machTab, text = "Get data at Station", command = MistGetLocation,width=17, height=1)
mistTCLBtn.place(x=438,y=300)

# tab for FireWork
def FwRarc():
    os.system("rarc -i " + Umist.filelocation + "/FireWork &")

def FwClicked():
    Fw.bashFile(particules, getdate())
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
    Fw.TCLConfig(particules,getComboboxLocation(),getdate())
    Fw.launchTCL()
    Fw.removeEmptyFile(r'' + Fw.filelocation + "/extractedFw")
    Fw.sortAndGenerate(Fw.filelocation + "/extractedFw/",getdate())


FireWork = tk.Label(machTab,text = "FireWork", font = "13")
FireWork.place(x=255,y=235)

fwBashBtn = tk.Button(machTab, text = "Get Chosen Pollutants", command = FwClicked,width=17, height=1)
fwBashBtn.place(x=255,y=270)

fwRarcBtn = tk.Button(machTab, text="FireWork Extraction", command = FwRarc, width=17, height=1)
fwRarcBtn.place(x=255,y=150)

fwTCLbtn = tk.Button(machTab, text = "Get data at Station", command = FwGetLocation, width=17, height=1)
fwTCLbtn.place(x=255,y=300)

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


imagesct = tk.Label(machTab,text = "Image Section", font = "13")
imagesct.place(x=10,y=350)

imgextraction = tk.Label(machTab, text ="Gemmach", font = "13")
imgextraction.place(x=40, y=375)
ImgBtn = tk.Button(machTab, text = "Get Images", command = getImg, width=17, height=1)
ImgBtn.place(x=40,y=440)


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


ImgRarcBtn = tk.Button(machTab, text = "Start Extraction", command = IMRARC,width=17, height=1)
ImgRarcBtn.place(x=40,y=410)

def UmosImgRarc():
    os.system("rarc -i " + Gm.filelocation + "/imageUMOS &")


imgUmos = tk.Label(machTab,text = "UMOS", font = "13")
imgUmos.place(x=225,y=375)

ImgUmosRarcBtn = tk.Button(machTab, text = "Start Extraction", command =UmosImgRarc,width=17, height=1)
ImgUmosRarcBtn.place(x=225,y=410)

UmosImgBtn = tk.Button(machTab, text ="Get images", command = getUMOSimg,width=17, height=1)
UmosImgBtn.place(x=438,y=440)

UmosImgLocation = ttk.Combobox(machTab, values = ["@sfc_", "@sfc@diff_"], state='readonly')
UmosImgLocation.place(x=225,y=443)
UmosImgLocation.current(0)

animateCombo = ttk.Combobox(machTab, values =sorted(giflst),width=55, height=10, state='readonly')
animateCombo.place(x=180,y=503)
#animateCombo.current(0)


def animate():
    index = animateCombo.current()
    os.system("animate output/"+sorted(giflst)[index]+" &")


animateBtn = tk.Button(machTab, text = "Animate GIF", command = animate,width=17, height=1)
animateBtn.place(x=10,y=500)


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
obs.place(x=838,y=235)
observationRarcBtn = tk.Button(machTab,text = "Observation Extraction", command=RarcObservation, width=17, height=1)
observationRarcBtn.place(x=838,y=150)

observationLocationBtn = tk.Button(machTab, text = "Get Data at Station", command=ObservationGetLocation, width=17, height=1)
observationLocationBtn.place(x=838,y=270)

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


#delete folder UI
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

#######################################
#end


deletebtn = tk.Button(machTab, text="Delete Extracted Files", bg = "red", command = deleteRarcFile, width=17, height=2)
deletebtn.place(x=850,y=500)
# tab for help
helptab = ttk.Frame(nb)
nb.add(helptab, text="Quick Start Guide", )
firstpartLabel = tk.Label(helptab, text = "Enter all the necessary information in the first part of the program."
                                          "\nPress \"Write to file\" to configure the program"
                                          "\nUse \"Update\" button when there are some changes made in the configuration"
                                          "\nThen select which models you want to extract. "
                                          "\nNote: at leat ONE of every checkbox needs to be checked.")
firstpartLabel.place(x=10,y=10)

secondpartLabel = tk.Label(helptab, text="Gemmach,Firework, and UMOS-Mist only works with a single date. Select the date to start treating"
                                         "\nThe button order goes from top to bottom. Wait until the process is done to start the next one"
                                         "\nFor the same date and pollutant settings, if you would like at another station, select it and update the file. Then press \"Get data at station\"."
                                         "\nYou do not have to go through the entire process again."
                                         "\nFor UMOS and Observations, press \"Get data at station\" for the file to be generated. Update the station if another place is desired")
secondpartLabel.place(x=10,y=100)

thirdpartLabel = tk.Label(helptab, text = "The images works with a series of date. It takes the same configuration settings from the first part."
                                          "\nThen select which images you would like to generate. Press on \"Get Images\". This works with a series of date"
                                          "\nFor the UMOS, there is @sfc_ (at surface) or @sfc_diff_ (surface difference between UMOS and Gemmach)."
                                          "\n\tSelect one of them then get the images"
                                          "\nThere is a function called \"Animate GIF\" to animate the selected GIF in the combobox.")
thirdpartLabel.place(x=10,y=190)


moreinfo = tk.Label(helptab,text="For more info on how the program works, visit this link:")
moreinfo.place(x=10,y=280)
websiteEntry = tk.Entry(helptab,state='readonly')
websiteVar = tk.StringVar()
websiteVar.set("http://ewiki.wul.qc.ec.gc.ca/wiki/index.php/Cr%C3%A9ation_d%27un_outil_informatique_pour_faciliter_les_%C3%A9tudes_de_cas_en_qualit%C3%A9_de_l%27air")
websiteEntry.config(textvariable=websiteVar,relief='flat', width =145,highlightthickness=0)
websiteEntry.place(x=10,y=300)
s = ttk.Style()
s.theme_use('classic')

def loadDB():
    dbFile = open("configuration", "rb")
    db = pickle.load(dbFile)

    enteredstartDateVar = tk.StringVar()
    enteredstartDateVar.set(db[0])
    enteredDate.config(textvariable=enteredstartDateVar)

    enteredEndDateVar = tk.StringVar()
    enteredEndDateVar.set(db[1])
    enteredEndDate.config(textvariable=enteredEndDateVar)

    sHourcombo.current(db[2])
    eHourCombo.current(db[3])

    comboprov.current(db[4])

    print(db[5])
    combostations.current(db[5])

    selectDate.config(values=db[6])
    selectDate.current(db[7])
    dbFile.close()


try:
    loadDB()
except:
    pass

def storeDB():
    try:
        os.remove("configuration")
    except:
        pass
    dbFile = open("configuration", "ab")
    GemClicked()
    pickle.dump([
        enteredDate.get(),
        enteredEndDate.get(),
        sHourcombo.current(),
        eHourCombo.current(),
        comboprov.current(),
        combostations.current(),
        Gm.returnDateList(),
        selectDate.current()
                 ], dbFile)
    print(combostations.current())
    dbFile.close()


def _delete_window():
    storeDB()
    print("Configuration Saved!")
    window.destroy()


window.protocol("WM_DELETE_WINDOW", _delete_window)
window.mainloop()

# notes: active var for particuleCheckBoxAndTime allowed me to use the same code for different purposes, when you write
# file, you dont want to get the location right now because the file may not be extracted yet
