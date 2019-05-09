import tkinter as tk
import Backend as Bk

window = tk.Tk()
window.title("Welcome")
window.geometry('800x600')
dateLabel = tk.Label(window, text="Enter Date in YYYY/MM/DD format")
dateLabel.grid(column=0, row=0)
txt = tk.Entry(window, width=10)
txt.grid(column=1, row=0)


def dateClicked():
    res1 = txt.get()
    Bk.inputDate(res1)


btn = tk.Button(window, text=" Enter", command=dateClicked)
btn.grid(column=2, row=0)
window.mainloop()
