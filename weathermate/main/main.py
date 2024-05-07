# from tkinter.ttk import LabelFrame
import asyncio
import json
import threading
from tkinter import StringVar
from ttkbootstrap import Frame, Label, Toplevel
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

from weathermate.api.ai import get_ai_response
from weathermate.api.air_condition import getAirConditionStationList
from weathermate.api.shortTerm import getShortTermWeatherInfo
from weathermate.main.widgets.DayWeather import DayWeather
from weathermate.main.widgets.LiveWeather import LiveWeather
from weathermate.main.widgets.Plot import Plot

import os
from datetime import datetime
import pytz

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from weathermate.responseHandler.stfc import generateSTFCLiveWeather, generateSTFCPlot, handleShortTermWeatherInfo
from weathermate.tools.translator import SKY_Emote_translator, SKY_translator, weekday_translator

font_name = fm.FontProperties(fname='./font.ttf').get_name()
plt.rc('font', family=font_name)

class ConfigTopLevel:
    def __init__(self, parentFrame) -> None:
        self.df = pd.DataFrame()
        self.top = Frame(parentFrame)

        self.config_frame = Frame(self.top, bootstyle="default")
        self.config_frame.grid(row=0, column=0, padx=10, pady=10)

        self.cache_file = 'cache.pkl'

        if os.path.exists(self.cache_file):
            # 캐시된 파일이 존재하면, 캐시된 파일을 읽습니다.
            self.df = pd.read_pickle(self.cache_file)
        else:
            # 캐시된 파일이 존재하지 않으면, 원본 파일을 읽고 그 결과를 캐시 파일에 저장합니다.
            self.df = pd.read_excel('xy.xlsx')
            self.df.to_pickle(self.cache_file)

        self.comboBox_1 = ttk.Combobox()
        self.comboBox_2 = ttk.Combobox()
        self.comboBox_3 = ttk.Combobox()
        self.comboBox_4 = ttk.Combobox()

    def getFrame(self):
        return self.top

    def getTopLevel(self):
        Label(self.config_frame, text="지역을 선택하세요", bootstyle="default").grid(row=0, column=0)

        comboBox_1 = ttk.Combobox(self.config_frame, values=sorted(set(self.df['1단계'].dropna().astype(str).to_list())))
        comboBox_2 = ttk.Combobox(self.config_frame)
        comboBox_3 = ttk.Combobox(self.config_frame)
        comboBox_4 = ttk.Combobox(self.config_frame)

        comboBox_1.set("도시 선택")
        comboBox_2.set("지역구 선택")
        comboBox_3.set("동네 선택")

        comboBox_1.grid(row=1, column=0, padx=10, pady=10)
        comboBox_1.bind('<<ComboboxSelected>>', self.listByCity)

        comboBox_2.grid(row=1, column=1, padx=10, pady=10)
        comboBox_2.bind('<<ComboboxSelected>>', self.listBySecond)

        comboBox_3.grid(row=1, column=2, padx=10, pady=10)

        comboBox_4.grid(row=1, column=3, padx=10, pady=10)

        saveButton = ttk.Button(self.config_frame, text="저장", command=self.saveConfig)
        saveButton.grid(row=1, column=3, padx=10, pady=10)

        return self.top

    def listByCity(self, event):
        selected_city = self.comboBox_1.get()
        city_df = self.df[self.df['1단계'] == selected_city]

        self.comboBox_2.set("지역구 선택")
        self.comboBox_3.set("동네 선택")
        self.comboBox_4.set("미세먼지 측정소 선택")
        self.comboBox_2['values'] = sorted(set(city_df['2단계'].dropna().astype(str).to_list()))

        # 도시별 미세먼지 측정소 정보를 가져옵니다.

        try:
            stationList = asyncio.create_task(getAirConditionStationList(selected_city))['response']['body']['items']
        except Exception as e:
            Messagebox.show_error(f"미세먼지 측정소 정보를 불러오는 중 문제가 발생했습니다. 다시 실행해주세요.\n{e}", "WeatherMate")
            self.comboBox_1.set("도시 선택")
            return
        self.comboBox_4['values'] = [x['stationName'] for x in stationList]

    def listBySecond(self, event):
        selected_value = self.comboBox_2.get()
        second_df = self.df[self.df['2단계'] == selected_value]

        self.comboBox_3.set("동네 선택")
        self.comboBox_3['values'] = sorted(set(second_df['3단계'].dropna().astype(str).to_list()))
    
    def saveConfig(self):
        first = self.df[self.df['1단계'] == self.comboBox_1.get()]
        second = first[first['2단계'] == self.comboBox_2.get()]
        third = second[second['3단계'] == self.comboBox_3.get()]

        sr_config = {
            'location': [third['격자 X'].to_list()[0], third['격자 Y'].to_list()[0]],
            'location_name': f'{self.comboBox_1.get()} {self.comboBox_2.get()} {self.comboBox_3.get()}',
            'location_cityName': self.comboBox_1.get(),
            'location_secondName': self.comboBox_2.get(),
            'location_thirdName': self.comboBox_3.get(),
            'ac_station': self.comboBox_4.get()
        }

        with open('config.json', 'w') as f:
            json.dump(sr_config, f)
        
        self.top.destroy()
        self.top.update()


class Main:
    def __init__(self) -> None:
        self.root = ttk.Window(title='WeatherMate', maxsize=(940, 550))
        self.root.geometry("940x550")

        needConfig = self.checkConfig()

        print('Need Config:', needConfig)

        if needConfig == False:
            ConfigTopLevel(self.root).getFrame().grid(row=0, column=0, padx=10, pady=10)

        self.live_fcst_frame = Frame(self.root, bootstyle="default")
        self.live_fcst_frame.grid(row=0, column=0, padx=10, pady=10)

        self.loadingLabel = Label(self.live_fcst_frame, text='날씨 정보 로딩 중...', bootstyle="default")
        self.loadingLabel.grid(row=0, column=0, padx=10, pady=10)

        self.root.update()

    def getFrame(self):
        return self.root
    
    async def initialize(self):
        # 컨트롤 패널 생성
        self.controlFrame = Frame(self.live_fcst_frame, bootstyle="default")
        self.controlFrame.grid(row=1, column=0, sticky='w', padx=40, pady=10)

        self.tempButton = ttk.Button(self.controlFrame, text="온도", command=lambda: self.onButtonClicked('temp'))
        self.tempButton.grid(row=0, column=0, padx=4)

        self.popButton = ttk.Button(self.controlFrame, text="강수확률", command=lambda: self.onButtonClicked('pop'))
        self.popButton.grid(row=0, column=1, padx=4)

        self.windButton = ttk.Button(self.controlFrame, text="바람", command=lambda: self.onButtonClicked('wind'))
        self.windButton.grid(row=0, column=2, padx=4)

        # AI 제안 프레임 생성
        self.chatGPTFrame = ttk.LabelFrame(self.live_fcst_frame, text='AI 제안', bootstyle="default")
        self.chatGPTFrame.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

        self.chatGPTLabel = Label(self.chatGPTFrame, text='AI 조언 로딩 중...', bootstyle="default")
        self.chatGPTLabel.grid(row=0, column=0, padx=10, pady=10)

        try:
            korea = pytz.timezone('Asia/Seoul')
            self.STres = await getShortTermWeatherInfo(date = datetime.now(korea).strftime('%Y%m%d'), time = datetime.now(korea).strftime('%H00'))
        except Exception as e:
            Messagebox.show_error(f"날씨 정보를 불러오는 중 문제가 발생했습니다. 다시 실행해주세요.\n{e}", "WeatherMate")
            return
        
        # 그래프를 위한 데이터를 처리합니다.
        self.stfc_plot_df = generateSTFCPlot(self.STres)
        # 현재 날씨 요약 정보를 처리합니다.
        # 단기 예보 정보를 처리합니다.
        self.stfc_df = handleShortTermWeatherInfo(self.STres)
        # 단기 예보 정보로 현재 날씨 정보를 생성합니다.
        self.live_dict = generateSTFCLiveWeather(self.STres)

        LiveWeather(
            self.live_fcst_frame, 
            self.live_dict['PTY'], 
            self.live_dict['TIME_OF_STR'], 
            self.live_dict['DAY_OF_WEEK'], 
            self.live_dict['FCST_TIME'],
            SKY_Emote_translator(self.live_dict['SKY']), 
            self.live_dict['TMP'], 
            self.live_dict['POP'], 
            self.live_dict['REH'], 
            self.live_dict['WSD']
        ).get_frame().grid(row=0, column=0)

        st_fcst_frame = ttk.Frame(self.live_fcst_frame, bootstyle="default")
        st_fcst_frame.grid(row=3, column=0)

        for _ in range(self.stfc_df['date'].size):
            date = datetime.strptime(self.stfc_df['date'][_], '%Y%m%d')
            weekday = weekday_translator(date.weekday())
            skyEmote = SKY_Emote_translator(int(self.stfc_df['sky'][_]))
            temp = f"{self.stfc_df['temp'][_]['min']}° / {self.stfc_df['temp'][_]['max']}°"
            
            weather = DayWeather(st_fcst_frame, weekday, skyEmote, temp)
            weather.get_frame().grid(row=0, column=_)

        self.ai_res = await get_ai_response(self.live_dict['TMP'], self.live_dict['REH'], self.live_dict['POP'])
        self.chatGPTLabel.config(text=self.ai_res)

    def onButtonClicked(self, type):
        print("Button Clicked")
        plt.close('all')
        if type == 'temp':
            Plot(self.live_fcst_frame, self.stfc_plot_df['tmp'].astype(int).to_list()[:24], self.stfc_plot_df['time'].to_list()[:24], '기온').grid(row=2, column=0)
        elif type == 'pop':
            Plot(self.live_fcst_frame, self.stfc_plot_df['pop'].astype(int).to_list()[:24], self.stfc_plot_df['time'].to_list()[:24], '강수확률').grid(row=2, column=0)
        elif type == 'wind':
            Plot(self.live_fcst_frame, self.stfc_plot_df['wsd'].astype(float).to_list()[:24], self.stfc_plot_df['time'].to_list()[:24], '풍속').grid(row=2, column=0)

    def init_defaultPlot(self):
        Plot(self.live_fcst_frame, self.stfc_plot_df['tmp'].astype(int).to_list()[:24], self.stfc_plot_df['time'].to_list()[:24], '기온').grid(row=2, column=0)
    
    def checkConfig(self):
        try:
            with open('config.json', 'r') as f:
                json.load(f)
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            return False

        return True

if __name__ == '__main__':
    app = Main()

    app.getFrame().after(1000, app.initialize)
    app.getFrame().mainloop()
    