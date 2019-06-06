import tkinter as tk

window = tk.Tk()
# window.attributes('-zoomed', True)
#w, h = window.winfo_screenwidth(), window.winfo_screenheight()
w,h = 1225,890
window.geometry("%dx%d+0+0" % (w, h))
img = tk.PhotoImage(file = "aa.gif")
imglabal = tk.Label(window,image = img)
imglabal.grid(column=0, row=50, sticky='w')

window.mainloop()
#convert -delay 35 -loop 0 *.png aa.gif
