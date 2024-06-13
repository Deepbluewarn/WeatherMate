from tkinter import *

root = Tk()
root.geometry("200x200")

button1 = Button(root, text="Button 1")
button1.grid(row=0, column=0, sticky="nsew")

button2 = Button(root, text="Button 2")
button2.grid(row=1, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()