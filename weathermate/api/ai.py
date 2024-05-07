import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OpenAI.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

async def get_ai_response(temp, reh, pop):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": """
                    날씨에 대한 데이터를 보고 사용자에게 조언을 제공하는 프로그램입니다. 
                    온도, 상대습도, 강수 확률 등을 고려하여 사용자에게 적절한 옷차림과 우산 여부, 또는 야외 활동 여부를 추천합니다.
                    데이터에 대한 설명은 생략하고 조언만 간단하게 한 문장 이내로 작성해주세요.
                """
            },
            {
                "role": "user", 
                "content": f'온도는 {temp}도, 상대습도는 {reh}%, 강수확률은 {pop}% 입니다.'
            },
        ]
    )

    return completion.choices[0].message.content
