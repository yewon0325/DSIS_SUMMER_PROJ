import requests

# API URL
url = 'http://apis.data.go.kr/B553530/GHG_LIST_040/GHG_LIST_04_04_20220831_VIEW01'

params = {
    'ServiceKey': 'mLK6c23e65hfr6QCC9LfzukbIT4S5LX5KRqDnC89paX%2Br2PFba3L1532lMJ%2B%2F7ouM7B4GPlbkNcGYCZtt3PoOA%3D%3D',
    'pageNo': '1',
    'numOfRows': '10',
    'apiType': 'JSON',
    'q1': '2018',        # 연도
    'q2': 'A012'
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)
print("Response Headers:", response.headers)
print("Response Text:", response.text)

try:
    data = response.json()
    print("Parsed JSON:", data)
except Exception as e:
    print("JSON 파싱 실패:", e)
