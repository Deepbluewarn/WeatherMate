# from tkinter.ttk import LabelFrame
import json
from tkinter import StringVar
from ttkbootstrap import Frame, Label, Toplevel
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *

from weathermate.api.shortTerm import getShortTermWeatherInfo
from weathermate.main.widgets.DayWeather import DayWeather
from weathermate.main.widgets.LiveWeather import LiveWeather
from weathermate.main.widgets.Plot import Plot

import os
from datetime import datetime
import pytz

import pandas as pd
import matplotlib.pyplot as plt

from weathermate.responseHandler.stfc import generateSTFCLiveWeather, generateSTFCPlot, handleShortTermWeatherInfo
from weathermate.tools.translator import SKY_Emote_translator, SKY_translator, weekday_translator

def configTop():
    df = pd.DataFrame()
    top = Toplevel(title='WeatherMate 설정', maxsize=(940, 550))
    
    top.geometry("940x600")
    top.attributes('-topmost', 'true')
    top.grab_set()

    config_frame = Frame(top, bootstyle="default")
    config_frame.grid(row=0, column=0, padx=10, pady=10)

    Label(config_frame, text="지역을 선택하세요", bootstyle="default").grid(row=0, column=0)

    def listByCity(event):
        selected_city = comboBox_1.get()
        nonlocal df
        city_df = df[df['1단계'] == selected_city]

        comboBox_2.set("지역구 선택")
        comboBox_3.set("동네 선택")
        comboBox_2['values'] = sorted(set(city_df['2단계'].dropna().astype(str).to_list()))

    def listBySecond(event):
        selected_value = comboBox_2.get()
        nonlocal df
        second_df = df[df['2단계'] == selected_value]

        comboBox_3.set("동네 선택")
        comboBox_3['values'] = sorted(set(second_df['3단계'].dropna().astype(str).to_list()))
    
    def saveConfig():
        first = df[df['1단계'] == comboBox_1.get()]
        second = first[first['2단계'] == comboBox_2.get()]
        third = second[second['3단계'] == comboBox_3.get()]

        sr_config = {
            'location': [third['격자 X'].to_list()[0], third['격자 Y'].to_list()[0]],
            'location_name': f'{comboBox_1.get()} {comboBox_2.get()} {comboBox_3.get()}',
        }

        with open('config.json', 'w') as f:
            json.dump(sr_config, f)
        
        top.destroy()
        top.update()
    

    cache_file = 'cache.pkl'

    if os.path.exists(cache_file):
        # 캐시된 파일이 존재하면, 캐시된 파일을 읽습니다.
        df = pd.read_pickle(cache_file)
    else:
        # 캐시된 파일이 존재하지 않으면, 원본 파일을 읽고 그 결과를 캐시 파일에 저장합니다.
        df = pd.read_excel('xy.xlsx')
        df.to_pickle(cache_file)
    
    comboBox_1 = ttk.Combobox(config_frame, values=sorted(set(df['1단계'].dropna().astype(str).to_list())))
    comboBox_2 = ttk.Combobox(config_frame)
    comboBox_3 = ttk.Combobox(config_frame)

    comboBox_1.set("도시 선택")
    comboBox_2.set("지역구 선택")
    comboBox_3.set("동네 선택")

    comboBox_1.grid(row=1, column=0, padx=10, pady=10)
    comboBox_1.bind('<<ComboboxSelected>>', listByCity)

    comboBox_2.grid(row=1, column=1, padx=10, pady=10)
    comboBox_2.bind('<<ComboboxSelected>>', listBySecond)

    comboBox_3.grid(row=1, column=2, padx=10, pady=10)

    saveButton = ttk.Button(config_frame, text="저장", command=saveConfig)
    saveButton.grid(row=1, column=3, padx=10, pady=10)

    return top

# def checkConfig():
#     init = False

#     try:
#         with open('config.json', 'r') as f:
#             config_file = json.load(f)
#     except FileNotFoundError:
#         init = True
#     except json.JSONDecodeError:
#         Messagebox.show_error("WeatherMate", "설정 파일을 불러오는 중 문제가 발생했습니다. 설정 파일을 삭제하고 다시 실행해주세요.")

#     # 설정 파일이 없는 경우, 사용자에게 설정을 입력받습니다.

#     if init == True:
#         configTop()

def main():
    print('main called')
    root = ttk.Window(title='WeatherMate', maxsize=(940, 550))
    root.geometry("940x600")

    init = False

    try:
        with open('config.json', 'r') as f:
            config_file = json.load(f)
    except FileNotFoundError:
        init = True
    except json.JSONDecodeError:
        Messagebox.show_error("WeatherMate", "설정 파일을 불러오는 중 문제가 발생했습니다. 설정 파일을 삭제하고 다시 실행해주세요.")

    # 설정 파일이 없는 경우, 사용자에게 설정을 입력받습니다.

    if init == True:
        root.wait_window(configTop())

    try:
        korea = pytz.timezone('Asia/Seoul')
        res = getShortTermWeatherInfo(date = datetime.now(korea).strftime('%Y%m%d'), time = datetime.now(korea).strftime('%H00'))
    except Exception as e:
        Messagebox.show_error("WeatherMate", f"날씨 정보를 불러오는 중 문제가 발생했습니다. 다시 실행해주세요.\n{e}")
        return
    
    # 그래프를 위한 데이터를 처리합니다.
    stfc_plot_df = generateSTFCPlot(res)
    # 현재 날씨 요약 정보를 처리합니다.
    # 단기 예보 정보를 처리합니다.
    stfc_df = handleShortTermWeatherInfo(res)

    # print(stfc_df)

    def onButtonClicked(type):
        print("Button Clicked")
        plt.close('all')
        if type == 'temp':
            x = stfc_plot_df['tmp'].to_list()[:24]
            Plot(live_fcst_frame, stfc_plot_df['tmp'].astype(int).to_list()[:24], stfc_plot_df['time'].to_list()[:24]).grid(row=2, column=0)
        elif type == 'pop':
            Plot(live_fcst_frame, stfc_plot_df['pop'].astype(int).to_list()[:24], stfc_plot_df['time'].to_list()[:24]).grid(row=2, column=0)
        elif type == 'wind':
            Plot(live_fcst_frame, stfc_plot_df['wsd'].astype(float).to_list()[:24], stfc_plot_df['time'].to_list()[:24]).grid(row=2, column=0)


    live_fcst_frame = Frame(root, bootstyle="default")
    live_fcst_frame.grid(row=0, column=0, padx=10, pady=10)

    live_dict = generateSTFCLiveWeather(res)

    LiveWeather(live_fcst_frame, live_dict['PTY'], live_dict['TIME_OF_STR'], live_dict['DAY_OF_WEEK'], live_dict['FCST_TIME'], SKY_Emote_translator(live_dict['SKY']), live_dict['TMP'], live_dict['POP'], live_dict['REH'], live_dict['WSD']).get_frame().grid(row=0, column=0)

    controlFrame = Frame(live_fcst_frame, bootstyle="default")
    controlFrame.grid(row=1, column=0, sticky='w', padx=40, pady=10)

    tempButton = ttk.Button(controlFrame, text="온도", command=lambda: onButtonClicked('temp'))
    tempButton.grid(row=0, column=0, padx=4)

    popButton = ttk.Button(controlFrame, text="강수확률", command=lambda: onButtonClicked('pop'))
    popButton.grid(row=0, column=1, padx=4)

    windButton = ttk.Button(controlFrame, text="바람", command=lambda: onButtonClicked('wind'))
    windButton.grid(row=0, column=2, padx=4)

    Plot(live_fcst_frame, [0], [0]).grid(row=2, column=0)

    st_fcst_frame = ttk.Frame(live_fcst_frame, bootstyle="default")
    st_fcst_frame.grid(row=3, column=0)

    for _ in range(stfc_df['date'].size):
        date = datetime.strptime(stfc_df['date'][_], '%Y%m%d')
        weekday = weekday_translator(date.weekday())
        skyEmote = SKY_Emote_translator(int(stfc_df['sky'][_]))
        temp = f"{stfc_df['temp'][_]['min']}° / {stfc_df['temp'][_]['max']}°"
        
        weather = DayWeather(st_fcst_frame, weekday, skyEmote, temp)
        weather.get_frame().grid(row=0, column=_)

    chatGPTFrame = ttk.LabelFrame(live_fcst_frame, text='AI 제안', bootstyle="default")
    chatGPTFrame.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

    chatGPTLabel = Label(chatGPTFrame, text="Chat with GPT-4", bootstyle="default")
    chatGPTLabel.grid(row=0, column=0, padx=10, pady=10)

    return root

main().mainloop()