#!/usr/bin/env python3
import glob
import os
import pickle
import shutil
import sys
import time
import tkinter as tk
from tkinter import ttk

import FireWork as Fw
import Gemmach as Gm
import Images as Im
import UMOS as Um
import UMOSMist as Umist
import observations as Ob

# initial setting
window = tk.Tk()
# window.attributes('-zoomed', True)
# w, h = window.winfo_screenwidth(), window.winfo_screenheight()
w, h = 1100, 640
window.geometry("%dx%d+0+0" % (w, h))
window.title("Automatic Image and Data Extraction - AIDE")
# window.geometry("1500x1200")
# Defines and places the notebook widget
nb = ttk.Notebook(window)
nb.place(x=0, y=0, width=w, height=h)
# nb.grid(row=1, column=0, columnspan=50, rowspan=100, sticky='NESW')

# Adds tab for Gem-Mach
machTab = ttk.Frame(nb)
nb.add(machTab, text="Tool")


# this function just writes all the user input into all files
def UpdateEverything():
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
    PM25 = var_PM25.get()
    particules = Gm.particuleCheckBox(O3, NO2, "", PM25)
    Gm.rarcFile()
    selectDate.config(values=Gm.returnDateList())
    #    others = otherVariable.get()
    Gm.level("")

    Um.inputStartDate(a)
    datesplit = Um.inputEndDate(b)
    Um.countdates()
    Um.modelCheckbox(h_00, h_12)
    Um.particuleCheckBoxAndTime(O3, NO2, PM25)
    Um.rarcFile(datesplit)

    Fw.level("")
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

    O3img = var_O3_image.get()
    NO2img = var_NO2_image.get()
    PM25img = var_PM25_image.get()
    Im.particuleCheckBox(O3img, NO2img, "", PM25img)

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
    Ob.particuleCheckBox(O3, NO2, "", PM25)

    Umist.removeAllfile(r'' + Umist.filelocation + "/configMIST")
    Umist.time(sTime, eTime)

    Umist.modelCheckbox(h_00, h_12)
    Umist.inputStartDate(a)
    Umist.inputEndDate(b)


def getdate():
    return Gm.returnDateList()[int(selectDate.current())]


def StartXRACR(modelType):
    UpdateEverything()
    if modelType == "UMist":
        Umist.rarcFile()
    os.system("rarc -i " + Gm.filelocation + "/" + modelType + " &")


def UMOSClicked():
    UpdateEverything()
    for filename in glob.glob("rarc/umos*"):
        os.system("rarc -i " + Gm.filelocation + "/" + filename + " &")


extractionLabel = tk.Label(machTab, text="Extraction", font="13")
extractionLabel.place(x=10, y=10)

startDateLabel = tk.Label(machTab, text="Enter Start Date (YYYY/MM/DD)")
enteredDate = tk.Entry(machTab, width=13)
startDateLabel.place(x=10, y=45)
enteredDate.place(x=210, y=45)

# End date
endDateLabel = tk.Label(machTab, text="Enter End Date (YYYY/MM/DD)")
enteredEndDate = tk.Entry(machTab, width=13)
endDateLabel.place(x=325, y=45)
enteredEndDate.place(x=525, y=45)

# Start Hours
sHourLabel = tk.Label(machTab, text="Choose the start time")
sHourcombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
sHourcombo.current(0)
sHourLabel.place(x=650, y=45)
sHourcombo.place(x=650, y=80)

# End Hours
eHourLabel = tk.Label(machTab, text="Choose the end time")
eHourCombo = ttk.Combobox(machTab, values=Gm.hours, state='readonly')
eHourCombo.current(48)
eHourLabel.place(x=850, y=45)
eHourCombo.place(x=850, y=80)

# Hour Selection
modelHourLabel = tk.Label(machTab, text="Select model time (UTC)")
var_00 = tk.BooleanVar(value=True)
hours00_Checkbutton = tk.Checkbutton(machTab, text="00", variable=var_00)
var_12 = tk.BooleanVar()
hours12_Checkbutton = tk.Checkbutton(machTab, text="12", variable=var_12)
modelHourLabel.place(x=10, y=80)
hours00_Checkbutton.place(x=165, y=80)
hours12_Checkbutton.place(x=215, y=80)

separetorline = ttk.Label(machTab,
                          text="________________________________________________________________________________________________________________________________________________________________________________________________________________")
separetorline.place(x=0, y=180)

AlpaNumDataLabel = tk.Label(machTab, text="Alphanumerical Data:")
AlpaNumDataLabel.place(x=10, y=115)

extrationBtn = tk.Button(machTab, text="Gemmach Extraction", command=lambda: StartXRACR("gemmach"), width=17, height=1)
extrationBtn.place(x=150, y=115)

fwRarcBtn = tk.Button(machTab, text="FireWork Extraction", command=lambda: StartXRACR("FireWork"), width=17, height=1)
fwRarcBtn.place(x=330, y=115)

mistExtraction = tk.Button(machTab, text="UMOS-Mist Extraction", command=lambda: StartXRACR("UMist"), width=17,
                           height=1)
mistExtraction.place(x=510, y=115)

UMOSBtnExt = tk.Button(machTab, text="UMOS Extraction", command=UMOSClicked, width=17, height=1)
UMOSBtnExt.place(x=690, y=115)

observationRarcBtn = tk.Button(machTab, text="Observation Extraction", command=lambda: StartXRACR("observations"),
                               width=17, height=1)
observationRarcBtn.place(x=870, y=115)

imagesLabel = tk.Label(machTab, text="Images:")
imagesLabel.place(x=10, y=160)

ImgRarcBtn = tk.Button(machTab, text="Gemmach Extraction", command=lambda: StartXRACR("image"), width=17, height=1)
ImgRarcBtn.place(x=150, y=160)

ImgUmosRarcBtn = tk.Button(machTab, text="UMOS-Mist Extraction", command=lambda: StartXRACR("imageUMOS"), width=17,
                           height=1)
ImgUmosRarcBtn.place(x=510, y=160)

#####################################################################
# start of alpha data treatment

separetorline1 = ttk.Label(machTab,
                           text="________________________________________________________________________________________________________________________________________________________________________________________________________________")
separetorline1.place(x=0, y=415)

AlpaNumDataLabel1 = tk.Label(machTab, text="Alphanumerical Data Treatment", font="13")
AlpaNumDataLabel1.place(x=10, y=210)

moleculeLabel = tk.Label(machTab, text="Select pollutant(s):")

var_O3 = tk.BooleanVar(value=True)
O3_Checkbutton = tk.Checkbutton(machTab, text="O3", variable=var_O3)
var_NO2 = tk.BooleanVar()
NO2_Checkbutton = tk.Checkbutton(machTab, text="NO2", variable=var_NO2)
var_PM25 = tk.BooleanVar()
PM25_Checkbutton = tk.Checkbutton(machTab, text="PM2.5", variable=var_PM25)

moleculeLabel.place(x=10, y=245)
O3_Checkbutton.place(x=165, y=245)
NO2_Checkbutton.place(x=215, y=245)
PM25_Checkbutton.place(x=265, y=245)


# stations
def combined(event):
    Gm.provlist.clear()
    name = comboprov.get()
    provlist = Gm.gettingprovlist(name)
    combostations.config(values=provlist)


locationLabel = ttk.Label(machTab, text="Select Station:")
# province combobox
comboprov = ttk.Combobox(machTab, values=Gm.prov, width=10, state='readonly')
comboprov.bind('<<ComboboxSelected>>', combined)
comboprov.current(0)
# stations from the province combobox
combostations = ttk.Combobox(machTab, values=Gm.gettingprovlist("Province"), width=30, state='readonly')
combostations.current(0)
locationLabel.place(x=400, y=245)
comboprov.place(x=510, y=245)
combostations.place(x=625, y=245)

# suff for the search
displayString = ""
stationSearchField = ttk.Entry(machTab, width=15)


def SearchNameID():
    userInput = stationSearchField.get()
    dString = Gm.SearchNameID(userInput)
    stationSearchLabel.config(text=dString)


stationSearchLabel = tk.Label(machTab, text=displayString)
searchBtn = tk.Button(machTab, text="Search Station Name or ID", command=SearchNameID)

stationSearchLabel.place(x=730, y=275)
stationSearchField.place(x=600, y=275)
searchBtn.place(x=400, y=275)


def UMOSGetLocation():
    b = enteredEndDate.get()
    Um.inputStartDate(enteredDate.get())
    datesplit = Um.inputEndDate(b)
    locID = getComboboxLocation()
    # extraction
    O3 = var_O3.get()
    NO2 = var_NO2.get()
    PM25 = var_PM25.get()
    h_00 = var_00.get()
    h_12 = var_12.get()
    particules = Um.particuleCheckBoxAndTime(O3, NO2, PM25)
    Um.countdates()
    Um.modelCheckbox(h_00, h_12)
    if datesplit is False:
        # pre17
        Um.getDataAtLocationPre2017(locID, particules)
        pass
    else:
        # post 17
        Um.extractwithCMCARC(particules)
        Um.getDataAtLocation(locID)


UMOSBtnGetFile = tk.Button(machTab, text="Get UMOS Data at Station", command=UMOSGetLocation, width=25, height=1)
UMOSBtnGetFile.place(x=50, y=320)


def ObservationGetLocation():
    UpdateEverything()
    Ob.listadys()
    locID = getComboboxLocation()
    Ob.generateFromDB(locID)


observationLocationBtn = tk.Button(machTab, text="Get Observation Data at Station", command=ObservationGetLocation,
                                   width=25, height=1)
observationLocationBtn.place(x=300, y=320)

selectDate = ttk.Combobox(machTab, values=["No Date Entered"], state='readonly', width=25)
selectDate.place(x=370, y=360)
selectDate.current(0)

selectDateLabel = tk.Label(machTab, text="Select a date to treat (UMOS-MIST, Gemmach, FireWork)")
selectDateLabel.place(x=10, y=360)


def getLocation():
    UpdateEverything()
    StartBash("gemmachBashTest")
    time.sleep(1)
    Gm.removeAllfile(r'' + Gm.filelocation + "/config")
    Gm.getEticket()
    locID = getComboboxLocation()
    Gm.locationExtraction(locID, getdate())
    Gm.launchTCL()
    Gm.removeEmptyFile(r'' + Gm.filelocation + "/extracted")
    Gm.sortAndGenerate(Gm.filelocation + "/extracted/", getdate())


locationBtn = tk.Button(machTab, text="Get Gemmach data at Station", command=getLocation, width=25, height=1)
locationBtn.place(x=50, y=395)


def MistGetLocation():
    UpdateEverything()
    StartXRACR("UmosMist")
    time.sleep(1)
    Umist.writeEticket(getdate())
    shutil.rmtree("extractedMist")
    os.mkdir("extractedMist")
    os.system("./UmosMistEticket.tcl")
    Umist.TCLConfig(particules, getComboboxLocation(), getdate())
    Umist.launchTCL()
    Umist.removeEmptyFile(r'' + Umist.filelocation + "/extractedMist")
    Umist.sortAndGenerate(Umist.filelocation + "/extractedMist/", getdate())


mistTCLBtn = tk.Button(machTab, text="Get UMOS-Mist data at Station", command=MistGetLocation, width=25, height=1)
mistTCLBtn.place(x=550, y=395)


def FwGetLocation():
    UpdateEverything()
    StartXRACR("FireWork")
    time.sleep(1)
    shutil.rmtree("extractedFw")
    os.mkdir("extractedFw")
    Fw.TCLConfig(particules, getComboboxLocation(), getdate())
    Fw.launchTCL()
    Fw.removeEmptyFile(r'' + Fw.filelocation + "/extractedFw")
    Fw.sortAndGenerate(Fw.filelocation + "/extractedFw/", getdate())


fwTCLbtn = tk.Button(machTab, text="Get FireWork data at Station", command=FwGetLocation, width=25, height=1)
fwTCLbtn.place(x=300, y=395)


def StartBash(modelType):
    Gm.bashFile(getdate())
    time.sleep(1)
    os.system("chmod -R 777 " + Gm.filelocation)
    if Gm.bothCheked is 1:
        os.system("./" + modelType + "00.bash ")
        print("Done, file located at -->" + Gm.filelocation + "/bash")
    if Gm.bothCheked is 2:
        os.system("./" + modelType + "12.bash ")
        print("Done, file located at -->" + Gm.filelocation + "/bash")
    if Gm.bothCheked is 3:
        os.system("./" + modelType + "00.bash ")
        os.system("./" + modelType + "12.bash ")
        print("Done, file located at -->" + Gm.filelocation + "/bash")


##############################################################################################################


imagesct = tk.Label(machTab, text="Image Section", font="13")
imagesct.place(x=10, y=440)

moleculeLabel_image = tk.Label(machTab, text="Select pollutant(s):")

var_O3_image = tk.BooleanVar(value=True)
O3_Checkbutton_image = tk.Checkbutton(machTab, text="O3", variable=var_O3_image)
var_NO2_image = tk.BooleanVar()
NO2_Checkbutton_image = tk.Checkbutton(machTab, text="NO2", variable=var_NO2_image)
var_PM25_image = tk.BooleanVar()
PM25_Checkbutton_image = tk.Checkbutton(machTab, text="PM2.5", variable=var_PM25_image)

moleculeLabel_image.place(x=10, y=480)
O3_Checkbutton_image.place(x=165, y=480)
NO2_Checkbutton_image.place(x=215, y=480)
PM25_Checkbutton_image.place(x=265, y=480)

ImagesLabel = tk.Label(machTab, text="Select Locations:")
var_east = tk.BooleanVar(value=True)
East_Checkbtn = tk.Checkbutton(machTab, text="East", variable=var_east)
var_eastZoom = tk.BooleanVar()
EastZoom_Checkbtn = tk.Checkbutton(machTab, text="Zoomed East", variable=var_eastZoom)
var_NA = tk.BooleanVar()
NorthAmerica_Checkbtn = tk.Checkbutton(machTab, text="North America", variable=var_NA)
var_NAGem = tk.BooleanVar()
NAGem_Checkbtn = tk.Checkbutton(machTab, text="NA - GEM", variable=var_NAGem)
var_west = tk.BooleanVar()
West_Checkbtn = tk.Checkbutton(machTab, text="West", variable=var_west)
var_QCOnt = tk.BooleanVar()
QCOnt_CheckBtn = tk.Checkbutton(machTab, text="QC-Ont, Umos-Mist only", variable=var_QCOnt)

ImagesLabel.place(x=450, y=480)
NAGem_Checkbtn.place(x=605, y=480)
NorthAmerica_Checkbtn.place(x=605, y=505)
West_Checkbtn.place(x=725, y=480)
East_Checkbtn.place(x=725, y=505)
EastZoom_Checkbtn.place(x=805, y=480)
QCOnt_CheckBtn.place(x=805, y=505)

imageExtCombo = ttk.Combobox(machTab, values=["east", ""])
giflst = []


def getImg():
    UpdateEverything()
    Im.generateImage()
    # update list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values=sorted(giflst))


ImgBtn = tk.Button(machTab, text="Get Gemmach Images", command=getImg, width=17, height=1)
ImgBtn.place(x=50, y=525)

gifs = os.listdir("output")
for g in gifs:
    if g.endswith(".gif"):
        giflst.append(g)


def getUMOSimg():
    UpdateEverything()
    t = UmosImgLocation.get()
    Im.generateUMOSImage(t)
    # this part updates the list
    giflst.clear()
    gif = os.listdir("output")
    for g in gif:
        if g.endswith(".gif"):
            giflst.append(g)
    animateCombo.config(values=sorted(giflst))


UmosImgBtn = tk.Button(machTab, text="Get UMOS-Mist images", command=getUMOSimg, width=19, height=1)
UmosImgBtn.place(x=250, y=525)

UmosImgLocation = ttk.Combobox(machTab, values=["@sfc_", "@sfc@diff_"], state='readonly')
UmosImgLocation.place(x=435, y=525)
UmosImgLocation.current(0)

animateCombo = ttk.Combobox(machTab, values=sorted(giflst), width=55, height=10, state='readonly')
animateCombo.place(x=180, y=565)


# animateCombo.current(0)


def animate():
    index = animateCombo.current()
    os.system("animate output/" + sorted(giflst)[index] + " &")


animateBtn = tk.Button(machTab, text="Animate GIF", command=animate, width=17, height=1)
animateBtn.place(x=10, y=565)


def getComboboxLocation():
    location = int(combostations.current())
    province = comboprov.get()
    locationlst = Gm.provinceDic[province]
    locID = locationlst[location]
    return locID


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

# delete folder UI
folder_names = []
convertedFolderName = []


def rarcFolderDeletion():
    folder_names.clear()
    convertedFolderName.clear()
    for filename in os.listdir("rarc"):
        if os.path.isdir("rarc/" + filename):
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
    archnames = tk.Label(popup, text="Select file directory to delete")
    archnames.place(x=85, y=10)
    filelst = ttk.Combobox(popup, values=sorted(convertedFolderName), width=40, state='readonly')
    filelst.place(x=15, y=50)
    B1 = ttk.Button(popup, text="Cancel", command=popup.destroy, width=10)
    B1.place(x=55, y=160)

    def confirmDelete():
        inv_folderDict = {v: k for k, v in folderdict.items()}
        a = int(filelst.current())
        todel = sorted(convertedFolderName)[a]
        shutil.rmtree("rarc/" + inv_folderDict[todel])
        rarcFolderDeletion()
        popup.destroy()

    b2 = tk.Button(popup, text="Confirm delete", command=confirmDelete, width=10, bg='red')
    b2.place(x=195, y=160)
    popup.mainloop()


deletebtn = tk.Button(machTab, text="Delete Extracted Files", bg="red", command=deleteRarcFile, width=17, height=1)
deletebtn.place(x=850, y=565)
#######################################

# tab for help
helptab = ttk.Frame(nb)
nb.add(helptab, text="Quick Start Guide", )
firstpartLabel = tk.Label(helptab, text="Enter all the necessary information in the first part of the program."
                                        "\nPress \"Write to file\" to configure the program"
                                        "\nUse \"Update\" button when there are some changes made in the configuration"
                                        "\nThen select which models you want to extract. "
                                        "\nNote: at leat ONE of every checkbox needs to be checked.")
firstpartLabel.place(x=10, y=10)

secondpartLabel = tk.Label(helptab,
                           text="Gemmach,Firework, and UMOS-Mist only works with a single date. Select the date to start treating"
                                "\nThe button order goes from top to bottom. Wait until the process is done to start the next one"
                                "\nFor the same date and pollutant settings, if you would like at another station, select it and update the file. Then press \"Get data at station\"."
                                "\nYou do not have to go through the entire process again."
                                "\nFor UMOS and Observations, press \"Get data at station\" for the file to be generated. Update the station if another place is desired")
secondpartLabel.place(x=10, y=100)

thirdpartLabel = tk.Label(helptab,
                          text="The images works with a series of date. It takes the same configuration settings from the first part."
                               "\nThen select which images you would like to generate. Press on \"Get Images\". This works with a series of date"
                               "\nFor the UMOS, there is @sfc_ (at surface) or @sfc_diff_ (surface difference between UMOS and Gemmach)."
                               "\n\tSelect one of them then get the images"
                               "\nThere is a function called \"Animate GIF\" to animate the selected GIF in the combobox.")
thirdpartLabel.place(x=10, y=190)

moreinfo = tk.Label(helptab, text="For more info on how the program works, visit this link:")
moreinfo.place(x=10, y=280)
websiteEntry = tk.Entry(helptab, state='readonly')
websiteVar = tk.StringVar()
websiteVar.set(
    "http://ewiki.wul.qc.ec.gc.ca/wiki/index.php/Cr%C3%A9ation_d%27un_outil_informatique_pour_faciliter_les_%C3%A9tudes_de_cas_en_qualit%C3%A9_de_l%27air")
websiteEntry.config(textvariable=websiteVar, relief='flat', width=145, highlightthickness=0)
websiteEntry.place(x=10, y=300)
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

    selectDate.config(values=db[4])
    selectDate.current(db[5])
    dbFile.close()


try:
    loadDB()
    UpdateEverything()
except:
    pass


def storeDB():
    try:
        os.remove("configuration")
    except:
        pass
    if enteredDate.get() != "" and enteredEndDate != "":
        dbFile = open("configuration", "ab")
        UpdateEverything()
        pickle.dump([
            enteredDate.get(),
            enteredEndDate.get(),
            sHourcombo.current(),
            eHourCombo.current(),
            Gm.returnDateList(),
            selectDate.current()
        ], dbFile)
        dbFile.close()
        print("Configuration Saved!")


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def _delete_window():
    blockPrint()
    storeDB()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", _delete_window)
window.mainloop()

# notes: active var for particuleCheckBoxAndTime allowed me to use the same code for different purposes, when you write
# file, you dont want to get the location right now because the file may not be extracted yet

# additional code for extra features
# if the level is added, need to change the empty string into get what the user entered in the textbox  to in there --> Gm.level("")
# manual add level
# otherLabel = tk.Label(machTab, text="Others, add no space e.g. UVTT")
# otherVariable = tk.Entry(machTab, width=13)
# levelLabel = tk.Label(machTab, text="Enter Level (optional)")
# levelEntry = tk.Entry(machTab, width=15)

# levelLabel.place(x=705,y=10)
# levelEntry.place(x=850,y=10)
# otherLabel.place(x=10,y=120)
# otherVariable.place(x=210,y=120)
