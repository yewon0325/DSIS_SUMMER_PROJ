import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("HomeTap\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# users 컬렉션에 user1 문서 추가
doc_ref = db.collection("users").document("user1")
doc_ref.set({
    "name": "홍길동",
    "email": "hong@example.com",
    "point": 100
})

print("데이터가 성공적으로 추가되었습니다.")