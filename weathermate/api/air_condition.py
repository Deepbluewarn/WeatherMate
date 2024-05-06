import os
import requests
from dotenv import load_dotenv
from weathermate.tools.config import getUserConfig
from weathermate.tools.translator import shortenCityName

load_dotenv()

def getAirConditionStationList(cityName):
    url = os.environ.get('API_AIRKOREA_LIST_BASE_URL') + '/getMsrstnList'

    params = {
        'serviceKey': os.environ.get('API_AIRKOREA_SERVICE_KEY'),
        'returnType': 'json',
        'addr': shortenCityName(cityName),
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    
async def getAirConditionInfo(stationName):
    url = os.environ.get('API_AIRKOREA_LIVE_BASE_URL') + '/getMsrstnAcctoRltmMesureDnsty'

    params = {
        'serviceKey': os.environ.get('API_AIRKOREA_SERVICE_KEY'),
        'returnType': 'json',
        'stationName': stationName,
        'dataTerm': 'DAILY',
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(e)