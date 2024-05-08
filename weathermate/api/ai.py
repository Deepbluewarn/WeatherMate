import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OpenAI.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()


def get_ai_response(live_dict, stfc_plot_df):

    temp = live_dict['TMP']
    reh = live_dict['REH']
    pop = live_dict['POP']

    current_time = live_dict['TIME_OF_STR']
    temp_time_data = ','.join(stfc_plot_df['time'].to_list()[:24])
    pop_time_data = ','.join(stfc_plot_df['pop'].to_list()[:24])
    wsd_time_data = ','.join(stfc_plot_df['wsd'].to_list()[:24])

    messages = [
        {
            "role": "system", 
            "content": """
                날씨에 대한 데이터를 보고 사용자에게 조언을 제공하는 프로그램입니다. 
                온도, 상대습도, 강수 확률 등을 고려하여 사용자에게 적절한 옷차림과 우산 여부, 또는 야외 활동 여부를 추천합니다.
                데이터에 대한 설명은 생략하고 조언만 간단하게 한 문장 이내로 작성해주세요.

                현재 날씨에 대한 옷차림, 우산 여부에 대한 조언과 이후 날씨에 대한 조언도 제공해주세요.

                참고로 비가 온다는 판단은 강수 확률이 50% 이상일 때로 정의합니다.
            """
        },
        {
            "role": "user", 
            "content": f"""
                온도는 {temp}도, 상대습도는 {reh}%, 강수확률은 {pop}% 입니다.

                현재 시각: {current_time}
                기온 시계열 데이터: {temp_time_data}
                강수확률 시계열 데이터: {pop_time_data}
                풍속 시계열 데이터: {wsd_time_data}
            """
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return completion.choices[0].message.content
