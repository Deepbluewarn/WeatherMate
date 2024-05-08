import asyncio
from tkinter.font import Font
from ttkbootstrap import Frame, Label

from weathermate.api.air_condition import getAirConditionInfo
from weathermate.tools.config import getUserConfig
from weathermate.tools.translator import PTY_translator, airConditionGrade_translator

class LiveWeather:
    def __init__(self, parentFrame, pty, time_of_str, day_of_week, time, icon, temp, pop, reh, wind):
        self.parentFrame = parentFrame
        self.time_of_str = time_of_str
        self.day_of_week = day_of_week
        self.pty = pty
        self.time = time
        self.icon = icon
        self.temp = temp
        self.pop = pop + '%'
        self.reh = reh + '%'
        self.wind = wind + 'm/s'

        self.mainFrame = Frame(parentFrame, bootstyle="default")
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid(row=0, column=0, padx=40, sticky='ew')


        self.leftFrame = Frame(self.mainFrame, bootstyle="default")
        self.leftFrame.grid(row=0, column=0, sticky='w')

        self.rightFrame = Frame(self.mainFrame, bootstyle="default")
        self.rightFrame.grid(row=0, column=1, sticky='e')

        # leftFrame 설정 (아이콘, 온도, 강수확률, 습도, 풍속 정보 표시)

        self.font = Font(family="맑은 고딕", size=20)

        icon = Label(self.leftFrame, text=self.icon, bootstyle="default", font=self.font)
        icon.grid(row=0, column=0)

        tempFrame = Frame(self.leftFrame, bootstyle="default")

        temp = Label(tempFrame, text=self.temp, bootstyle="default", font=self.font)
        temp.grid(row=0, column=0)

        temp = Label(tempFrame, text='°C', bootstyle="default", font=self.font)
        temp.grid(row=0, column=1)

        tempFrame.grid(row=0, column=1)

        infoFrame = Frame(self.leftFrame, bootstyle="default")
        infoFrame.grid(row=0, column=2, padx=10)
        
        popLabel = Label(infoFrame, text='강수확률: ' + self.pop, bootstyle="primary")
        popLabel.grid(row=0, column=0, sticky='w')

        rehLabel = Label(infoFrame, text='습도: ' + self.reh, bootstyle="primary")
        rehLabel.grid(row=1, column=0, sticky='w')

        windLabel = Label(infoFrame, text='풍속: ' + self.wind, bootstyle="primary")
        windLabel.grid(row=2, column=0, sticky='w')

        # rightFrame 설정 (날씨 정보와 현재 시간 표시)

        self.font = Font(family="맑은 고딕", size=16)

        weatherStrLabel = Label(self.rightFrame, text='날씨', bootstyle="default", font=self.font)
        weatherStrLabel.grid(row=0, column=0, sticky='e')

        self.font = Font(family="맑은 고딕", size=10)

        timeLabel = Label(self.rightFrame, text=f'({self.day_of_week}) {self.time_of_str}', bootstyle="default", font=self.font)
        timeLabel.grid(row=1, column=0, sticky='e')


        if self.pty == 0:
            text = ''
        else:
            text = PTY_translator(self.pty)

        weatherLabel = Label(self.rightFrame, text=text, bootstyle="default", font=self.font)
        weatherLabel.grid(row=2, column=0, sticky='e')

        userConfig = getUserConfig()
        res = getAirConditionInfo(userConfig['ac_station'])

        res = res['response']['body']['items']

        if len(res) == 0:
            text = '미세먼지 정보가 없습니다.'
        else:
            res = res[0]
            text = f'미세먼지: {res["pm10Value"]}㎍/㎥ ({airConditionGrade_translator(int(res["pm10Grade"]))})'

        air_conditionLable = Label(self.rightFrame, text=text, bootstyle="default", font=self.font)
        air_conditionLable.grid(row=3, column=0, sticky='e')

        weatherLabel = Label(self.rightFrame, text=userConfig['location_name'], bootstyle="default", font=self.font)
        weatherLabel.grid(row=4, column=0, sticky='e')

    def get_frame(self):
        return self.mainFrame