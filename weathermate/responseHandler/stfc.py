# 단기 예보 API 응답을 처리하는 함수

from collections import Counter
from datetime import datetime
from weathermate.api.shortTerm import getShortTermWeatherInfo
import pandas as pd
import pytz

from weathermate.tools.translator import PTY_translator, SKY_translator

def generateSTFCLiveWeather(res):
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H') + '00'
    day_of_week = now.strftime('%A')
    time_str = now.strftime('%p %I:%M').replace('AM', '오전').replace('PM', '오후')

    items = res['response']['body']['items']['item']

    base_dates = []
    base_times = []
    categories = []
    fcst_dates = []
    fcst_times = []
    fcst_values = []
    nx = []
    ny = []

    for item in items:
        base_dates.append(item['baseDate'])
        base_times.append(item['baseTime'])
        fcst_dates.append(item['fcstDate'])
        fcst_times.append(item['fcstTime'])
        fcst_values.append(item['fcstValue'])
        nx.append(item['nx'])
        ny.append(item['ny'])
        categories.append(item['category'])
    
    res = pd.DataFrame({
        'base_date' : base_dates,
        'base_time' : base_times,
        'category' : categories,
        'fcst_date' : fcst_dates,
        'fcst_time' : fcst_times,
        'fcst_value' : fcst_values,
        'nx' : nx,
        'ny' : ny
    })

    mask = res[(res['fcst_date'] == date) & (res['fcst_time'] == time)]



    print('==== Live Weather mask ====')
    print(mask)

    # 만약 mask가 비어있다면 res의 첫번째 row의 fcst_time 을 가져와 mask를 다시 생성한다.
    if mask.empty:
        print('==== Live Weather mask is empty ====')
        print(res)
        time = res.iloc[0]['fcst_time']
        mask = res[(res['fcst_date'] == date) & (res['fcst_time'] == time)]

    pivot = mask.pivot(index='fcst_time', columns='category', values='fcst_value')

    print('==== Live Weather time ====')
    print(time)


    

    # res_df = pd.DataFrame({
    #     'TMP': f"{pivot['TMP'].tolist()[0]}°C",
    #     'POP': f"{pivot['POP'].tolist()[0]}%",
    #     'REH': f"{pivot['REH'].tolist()[0]}%",
    #     'WSD': f"{pivot['WSD'].tolist()[0]}m/s",
    #     'SKY': SKY_translator(int(pivot['SKY'].tolist()[0])),
    #     'PTY': PTY_translator(int(pivot['PTY'].tolist()[0]))
    # })

    res_dict = {
        'TIME_OF_STR': time_str,
        'DAY_OF_WEEK': day_of_week,
        'FCST_TIME': time,
        'TMP': f"{pivot['TMP'].tolist()[0]}",
        'POP': f"{pivot['POP'].tolist()[0]}",
        'REH': f"{pivot['REH'].tolist()[0]}",
        'WSD': f"{pivot['WSD'].tolist()[0]}",
        'SKY': int(pivot['SKY'].tolist()[0]),
        'PTY': int(pivot['PTY'].tolist()[0])
    }

    print('==== Live Weather res_dict ====')
    print(res_dict)

    return res_dict

def generateSTFCPlot(res):
    korea = pytz.timezone('Asia/Seoul')
    nowDate = datetime.now()

    items = res['response']['body']['items']['item']

    categories = []
    fcst_dates = []
    fcst_times = []
    fcst_values = []

    for item in items:
        fcst_dates.append(item['fcstDate'])
        fcst_times.append(item['fcstTime'])
        fcst_values.append(item['fcstValue'])
        categories.append(item['category'])

    res = pd.DataFrame({
        'category' : categories,
        'fcst_date' : fcst_dates,
        'fcst_time' : fcst_times,
        'fcst_value' : fcst_values
    })

    # 20240505

    res['datetime'] = pd.to_datetime(res['fcst_date'] + res['fcst_time'], format='%Y%m%d%H%M')
    
    nowDate = pd.Timestamp.now(tz='Asia/Seoul')

    # res = res[res['datetime'] >= nowDate]
    res = res[res['datetime'].dt.tz_localize('Asia/Seoul') >= nowDate]
    res['datestr'] = res['datetime'].dt.strftime('%H시')

    
    # print(res)

    # TMP, POP
    # VEC(풍향), WSD(풍속)

    tmp = []
    pop = []
    vec = []
    wsd = []
    time = []

    for name, group in res.groupby('category'):
        print(name)
        print(group)

        time = group['datestr'].tolist()

        if name == 'TMP':
            tmp = group['fcst_value'].tolist()
        elif name == 'POP':
            pop = group['fcst_value'].tolist()
        elif name == 'VEC':
            vec = group['fcst_value'].tolist()
        elif name == 'WSD':
            wsd = group['fcst_value'].tolist()
    
    print(len(tmp))
    print(len(pop))
    print(len(vec))
    print(len(wsd))
    print(len(time))

    return pd.DataFrame({
        'time': time,
        'tmp': tmp,
        'pop': pop,
        'vec': vec,
        'wsd': wsd
    })

def handleShortTermWeatherInfo(res):
    # korea = pytz.timezone('Asia/Seoul')
    # res = getShortTermWeatherInfo(date = datetime.now(korea).strftime('%Y%m%d'))
    items = res['response']['body']['items']['item']

    base_dates = []
    base_times = []
    categories = []
    fcst_dates = []
    fcst_times = []
    fcst_values = []
    nx = []
    ny = []

    for item in items:
        base_dates.append(item['baseDate'])
        base_times.append(item['baseTime'])
        fcst_dates.append(item['fcstDate'])
        fcst_times.append(item['fcstTime'])
        fcst_values.append(item['fcstValue'])
        nx.append(item['nx'])
        ny.append(item['ny'])
        categories.append(item['category'])
    
    res = pd.DataFrame({
        'base_date' : base_dates,
        'base_time' : base_times,
        'category' : categories,
        'fcst_date' : fcst_dates,
        'fcst_time' : fcst_times,
        'fcst_value' : fcst_values,
        'nx' : nx,
        'ny' : ny
    })

    grouped = res.groupby(['fcst_date'])

    res_days = []
    res_skies = []
    res_temps = []
    res_pty = []

    for name, group in grouped:
        pivot_table = group.pivot(index='fcst_time', columns='category', values='fcst_value')

        res_days.append(name[0])

        try:
            sky_values = pivot_table['SKY'].tolist()
        except:
            sky_values = []

        try:
            pty_values = pivot_table['PTY'].tolist()
        except:
            pty_values = []
        
        try:
            temp_min_values = pivot_table['TMN'].tolist()
            temp_max_values = pivot_table['TMX'].tolist()
        except:
            temp_min_values = ['-']
            temp_max_values = ['-']

        counter = Counter(sky_values)
        most_common_value = counter.most_common(1)[0][0]
        res_skies.append(most_common_value)

        pty_values = [x for x in pty_values if x != '0']

        counter = Counter(pty_values)

        if len(pty_values) == 0:
            most_common_value = '0'
        else:
            most_common_value = counter.most_common(1)[0][0]
            
        res_pty.append(most_common_value)

        temp_max_values = [x for x in temp_max_values if type(x) == str]
        temp_min_values = [x for x in temp_min_values if type(x) == str]
        
        res_temps.append({
            'min': min(temp_min_values),
            'max': max(temp_max_values)
        })

    return pd.DataFrame({
        'date': res_days,
        'sky': res_skies,
        'temp': res_temps,
        'pty': res_pty
    })

    