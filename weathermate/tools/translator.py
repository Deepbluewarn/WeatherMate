# 기상청 API 문서에 따라 SKY, PTY 값을 해석하는 함수

def SKY_translator(value):
    SKY_dict = {
        1: '맑음',
        3: '구름 많음',
        4: '흐림'
    }
    return SKY_dict.get(value, 'N/A')

def SKY_Emote_translator(value):
    SKY_dict = {
        1: '☀',
        3: '🌤',
        4: '☁'
    }
    return SKY_dict.get(value, 'N/A')
    
def PTY_translator(value):
    PTY_dict = {
        0: '없음',
        1: '비',
        2: '비/눈',
        3: '눈',
        4: '소나기'
    }
    return PTY_dict.get(value, 'N/A')

def PTY_Emote_translator(value):
    PTY_dict = {
        0: '.',
        1: '🌧',
        2: '🌧/❄',
        3: '❄',
        4: '🌧'
    }
    return PTY_dict.get(value, 'N/A')
    
def weekday_translator(value):
    weekday_dict = {
        0: '월',
        1: '화',
        2: '수',
        3: '목',
        4: '금',
        5: '토',
        6: '일'
    }
    return weekday_dict.get(value, 'N/A')
    
def api_err_translator(err_code):
    err_dict = {
        '00': '정상',
        '01': '어플리케이션 에러',
        '02': '데이터베이스 에러',
        '03': '데이터없음 에러',
        '04': 'HTTP 에러',
        '05': '서비스 연결실패 에러',
        '10': '잘못된 요청 파라메터 에러',
        '11': '필수요청 파라메터가 없음',
        '12': '해당 오픈API서비스가 없거나 폐기됨',
        '20': '서비스 접근거부',
        '21': '일시적으로 사용할 수 없는 서비스 키',
        '22': '서비스 요청제한횟수 초과에러',
        '30': '등록되지 않은 서비스키',
        '31': '기한만료된 서비스키',
        '32': '등록되지 않은 IP',
        '33': '서명되지 않은 호출',
        '99': '기타에러'
    }
    return err_dict.get(err_code, '알 수 없는 에러 코드')

def shortenCityName(city):
    res = ''
    if city == '서울특별시':
        res = '서울'
    elif city == '부산광역시':
        res = '부산'
    elif city == '대구광역시':
        res = '대구'
    elif city == '인천광역시':
        res = '인천'
    elif city == '광주광역시':
        res = '광주'
    elif city == '대전광역시':
        res = '대전'
    elif city == '울산광역시':
        res = '울산'
    elif city == '세종특별자치시':
        res = '세종'
    elif city == '경기도':
        res = '경기'
    elif city == '강원도':
        res = '강원'
    elif city == '충청북도':
        res = '충북'
    elif city == '충청남도':
        res = '충남'
    elif city == '전라북도':
        res = '전북'
    elif city == '전라남도':
        res = '전남'
    elif city == '경상북도':
        res = '경북'
    elif city == '경상남도':
        res = '경남'
    elif city == '제주특별자치도':
        res = '제주'
    return res

def airConditionGrade_translator(value):
    grade_dict = {
        1: '좋음',
        2: '보통',
        3: '나쁨',
        4: '매우 나쁨'
    }
    return grade_dict.get(value, 'N/A')