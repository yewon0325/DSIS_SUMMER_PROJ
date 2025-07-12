from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("HomeTap/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def hello():
    return "백엔드 서버가 정상 작동 중입니다."

#  인증 정보 저장 API
@app.route("/submit_certification", methods=["POST"])
def submit_certification():
    data = request.json  # 앱에서 보낸 JSON 데이터

    uid = data["uid"]
    mission = data["mission"]
    photo_url = data["photo_url"]

    today = datetime.now().strftime("%Y%m%d")
    doc_id = f"{uid}_{today}"

    # 인증 정보 Firestore에 저장
    db.collection("certifications").document(doc_id).set({
        "user_id": uid,
        "mission": mission,
        "date": today,
        "photo_url": photo_url
    })

    return jsonify({"message": "인증 저장 완료!"})

# Flask 실행
if __name__ == "__main__":
    app.run(debug=True)
