import tkinter as tk
import Backend as Bk
from tkinter import ttk


def Clicked():

    sDate = enteredDate.get()
    Bk.inputStartDate(sDate)

    eDate = enteredEndDate.get()
    Bk.inputEndDate(eDate)

    model = modelCombo.get()
    Bk.modelChosen(model)

    tool = toolCombo.get()
    Bk.toolChosen(tool)

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
btn = tk.Button(window, text=" Enter", command=Clicked, width=20,height=5)
btn.grid(column=10, row=10)

# model
modelLabel = tk.Label(window, text="Choose the model")
modelLabel.grid(column=0, row=2)
modelCombo = ttk.Combobox(window,
                            values=[
                                "GEM-MACH",
                                "UMOS",
                                "FireWork",
                                "Others..."], state = 'readonly')
modelCombo.grid(column=0, row=3)
modelCombo.current(0)

# tools
toolLabel = tk.Label(window, text="Choose the tool")
toolLabel.grid(column=0,row=4)
toolCombo = ttk.Combobox(window,
                         values=[
                             "XRARC",
                             "RARC",
                             "Others..."], state = 'readonly')
toolCombo.grid(column =0,row=5)
toolCombo.current(0)

window.mainloop()
