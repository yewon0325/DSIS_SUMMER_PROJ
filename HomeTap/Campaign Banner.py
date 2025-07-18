
import requests
from datetime import datetime
from firebase_admin import firestore


# API URL (엔드포인트)
url = 'https://api.odcloud.kr/api/15134147/v1/uddi:b32bc822-54fc-46e2-afd2-ddea4589ccf0'

# 요청 파라미터
params = {
    'page': 1,              # 페이지 번호
    'perPage': 3,          # 페이지당 데이터 수
    'returnType': 'JSON',   # 응답 포맷 (기본: JSON)
    'serviceKey': 'mLK6c23e65hfr6QCC9LfzukbIT4S5LX5KRqDnC89paX+r2PFba3L1532lMJ+/7ouM7B4GPlbkNcGYCZtt3PoOA=='
}

# GET 요청
response = requests.get(url, params=params)

# 응답 확인
if response.status_code == 200:
    data = response.json()
    print("응답 데이터:", data)
else:
    print(f"요청 실패: 상태코드 {response.status_code}")
    print(response.text)



