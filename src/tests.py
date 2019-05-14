import tkinter as tk
from tkinter import ttk

main = tk.Tk()
main.title('Notebook Demo')
main.geometry('500x500')

# gives weight to the cells in the grid
rows = 0
while rows < 50:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight=1)
    rows += 1

# Defines and places the notebook widget
nb = ttk.Notebook(main)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

# Adds tab 1 of the notebook
page1 = ttk.Frame(nb)
nb.add(page1, text="Gem-mach")


hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

# Start Hours
sHourLabel = tk.Label(page1, text="Choose the start time")
sHourLabel.grid(column=5, row=4)
sHourcombo = ttk.Combobox(page1, values=hours, state='readonly')
sHourcombo.grid(column=5, row=5)
sHourcombo.current(0)

# Adds tab 2 of the notebook
page2 = ttk.Frame(nb)
nb.add(page2, text='Tab2')

main.mainloop()
