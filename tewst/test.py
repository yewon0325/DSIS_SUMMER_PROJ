
import requests

# API URL
url = 'http://apis.data.go.kr/B553530/GHG_LIST_040/GHG_LIST_04_04_20220831_VIEW01'

# 요청 파라미터
params = {
    'ServiceKey': ''
    'pageNo': '1',
    'numOfRows': '10',
    'apiType': 'json',  # 'xml'도 가능
    'q1': '2018',       # 연도
    'q2': 'A012'        # 에너지 코드 (예시)
}

# GET 요청
response = requests.get(url, params=params)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Text:", response.text)  # 응답 내용 출력

try:
    data = response.json()
    print("Parsed JSON:", data)
except Exception as e:
    print("JSON 파싱 실패:", e)