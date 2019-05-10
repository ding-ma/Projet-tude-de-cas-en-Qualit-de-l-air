import tkinter as tk
import Backend as Bk
from tkinter import ttk


def Clicked():

    date = enteredDate.get()
    Bk.inputDate(date)

    model = modelCombo.get()
    Bk.modelChosen(model)

    tool = toolCombo.get()
    Bk.toolChosen(tool)

window = tk.Tk()
window.title("Welcome")
window.geometry('800x600')

# date
dateLabel = tk.Label(window, text="Enter Date in YYYY/MM/DD format")
dateLabel.grid(column=0, row=0)
enteredDate = tk.Entry(window, width=13)
enteredDate.grid(column=1, row=0)

# execute button
btn = tk.Button(window, text=" Enter", command=Clicked, width=20,height=5)
btn.grid(column=10, row=10)

# model
modelLabel = tk.Label(window, text="Choose the model")
modelLabel.grid(column=0, row=1)
modelCombo = ttk.Combobox(window,
                            values=[
                                "GEM-MACH",
                                "UMOS",
                                "FireWork",
                                "Others..."], state = 'readonly')
modelCombo.grid(column=0, row=2)
modelCombo.current(0)

# tools
toolLabel = tk.Label(window, text="Choose the tool")
toolLabel.grid(column=0,row=3)
toolCombo = ttk.Combobox(window,
                         values=[
                             "XRARC",
                             "RARC",
                             "Others..."], state = 'readonly')
toolCombo.grid(column =0,row=4)
toolCombo.current(0)

window.mainloop()
