from tkinter import *

root = Tk()

def _delete_window():
    print( "delete_window")
    try:
        root.destroy()
    except:
        pass


root.protocol("WM_DELETE_WINDOW", _delete_window)


mainloop()