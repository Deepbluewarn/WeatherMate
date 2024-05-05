import tkinter

window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("640x400+100+100")
window.resizable(False, False)



# toplevel = tkinter.Toplevel(window)
# toplevel.geometry("320x200+820+100")

# label=tkinter.Label(toplevel, text="YUN DAE HEE")
# label.pack()

mainLabel = tkinter.Label(window, text="YUN DAE HEE")
mainLabel.pack()

window.mainloop()