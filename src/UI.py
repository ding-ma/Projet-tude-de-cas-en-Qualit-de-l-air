import tkinter as tk
from tkinter import ttk

import Backend as Bk


def Clicked():
    sDate = enteredDate.get()
    Bk.inputStartDate(sDate)

    eDate = enteredEndDate.get()
    Bk.inputEndDate(eDate)

    model = modelCombo.get()
    Bk.modelChosen(model)

    tool = toolCombo.get()
    Bk.toolChosen(tool)

    sTime = sHourcombo.get()
    eTime = eHourCombo.get()
    Bk.time(sTime, eTime)



window = tk.Tk()
window.title("Welcome")
window.geometry('800x600')

# Start date
startDateLabel = tk.Label(window, text="Enter Start Date in YYYY/MM/DD format")
startDateLabel.grid(column=0, row=0)
enteredDate = tk.Entry(window, width=13)
enteredDate.grid(column=1, row=0)

# Start date
endDateLabel = tk.Label(window, text="Enter End Date in YYYY/MM/DD format")
endDateLabel.grid(column=0, row=1)
enteredEndDate = tk.Entry(window, width=13)
enteredEndDate.grid(column=1, row=1)

# execute button
btn = tk.Button(window, text=" Enter", command=Clicked, width=20, height=5)
btn.grid(column=10, row=10)

# model
modelLabel = tk.Label(window, text="Choose the model")
modelLabel.grid(column=0, row=2)
modelCombo = ttk.Combobox(window,
                          values=[
                              "GEM-MACH",
                              "UMOS",
                              "FireWork",
                              "Others..."], state='readonly')
modelCombo.grid(column=0, row=3)
modelCombo.current(0)

# tools
toolLabel = tk.Label(window, text="Choose the tool")
toolLabel.grid(column=0, row=4)
toolCombo = ttk.Combobox(window,
                         values=[
                             "XRARC",
                             "RARC",
                             "Others..."], state='readonly')
toolCombo.grid(column=0, row=5)
toolCombo.current(0)

hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

# Start Hours
sHourLabel = tk.Label(window, text="Choose the start time")
sHourLabel.grid(column=5, row=4)
sHourcombo = ttk.Combobox(window, values=hours, state='readonly')
sHourcombo.grid(column=5, row=5)
sHourcombo.current(0)

# End Hours
eHourLabel = tk.Label(window, text="Choose the end time")
eHourLabel.grid(column=7, row=4)
eHourCombo = ttk.Combobox(window, values=hours, state='readonly')
eHourCombo.grid(column=7, row=5)
eHourCombo.current(0)

modelhours = ("00", "12")

# System.out.print('"'+","+'"'+i)
window.mainloop()
