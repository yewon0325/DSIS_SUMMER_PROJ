from firebase_admin import firestore, credentials, initialize_app
from flask import Flask, jsonify
from datetime import datetime
import firebase_admin
import random

app = Flask(__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate("HomeTap/serviceAccountKey.json")
    initialize_app(cred)

db = firestore.client()

# 다시 수정 예정
def insert_initial_missions():
    missions = [
        {"title": "텀블러 사용하기", "point": 20},
        {"title": "대중교통 이용하기", "point": 30},
        {"title": "플라스틱 줄이기", "point": 25},
        {"title": "분리수거 하기", "point": 15},
        {"title": "엘리베이터 대신 계단 이용하기", "point": 10},
        {"title": "현수막 대신 온라인 홍보하기", "point": 20},
        {"title": "다회용 장바구니 사용하기", "point": 25},
        {"title": "종이컵 대신 머그컵 사용하기", "point": 20},
        {"title": "양면 인쇄하기", "point": 15},
        {"title": "종이 영수증 대신 문자 수령하기", "point": 10}
    ]

    for i, mission in enumerate(missions):
        doc_id = f"mission_{i+1}"
        db.collection("missions").document(doc_id).set(mission)


insert_initial_missions()


def get_current_week_id():
    today = datetime.now()
    return today.strftime("%Y-W%U")  # 예: "2025-W28"

# 주간 미션 불러오기 또는 생성
@app.route("/weekly_missions", methods=["GET"])
def get_weekly_missions():
    week_id = get_current_week_id()
    
    # DB에서 현재 주차(예: "2025-W28")에 해당하는 미션 문서를 가져옴
    # 없으면 새로운 미션을 생성해야 함
    weekly_doc = db.collection("weekly_missions").document(week_id).get()

    if weekly_doc.exists:
        return jsonify(weekly_doc.to_dict()["missions"])
    else:
        missions_ref = db.collection("missions").stream()
        # 위의 각 문서(doc)를 .to_dict()로 변환
        mission_list = [doc.to_dict() for doc in missions_ref]
        random_missions = random.sample(mission_list, k=5)

        db.collection("weekly_missions").document(week_id).set({
            "missions": random_missions,
            "created_at": datetime.now().isoformat()
        })

        return jsonify(random_missions)

if __name__ == "__main__":
    app.run(debug=True)
