from tkinter.font import Font
from ttkbootstrap import Label, Button

class DayWeather:
    def __init__(self, parentFrame, day, icon, temp):
        self.parentFrame = parentFrame
        self.day = day
        self.icon = icon
        self.temp = temp

        self.frame = Button(parentFrame, bootstyle="outline")
        self.frame.grid(row=0, column=0, padx=10, pady=5)

        self.font = Font(family="맑은 고딕", size=12)
        
        dayLabel = Label(self.frame, text=self.day, bootstyle="primary", font=self.font)
        dayLabel.grid(row=0, column=0, padx=10, pady=4)

        self.font = Font(family="맑은 고딕", size=20)

        icon = Label(self.frame, text=self.icon, bootstyle="primary", font=self.font)
        icon.grid(row=1, column=0, padx=10, pady=4)

        temp = Label(self.frame, text=self.temp, bootstyle="primary")
        temp.grid(row=2, column=0, padx=10, pady=4)

    def get_frame(self):
        return self.frame