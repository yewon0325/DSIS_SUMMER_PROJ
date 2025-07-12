from flask import Blueprint, request, jsonify
from datetime import datetime
from firebase_admin import firestore

home_bp = Blueprint("home", __name__)
db = firestore.client()

@home_bp.route("/home_tap", methods=['POST'])
def user_login():
    data = request.json

    uid = data["uid"]
    password =  data["password"]

    # Firestore에 사용자 정보 저장 (users 콜렉션)
    db.collection("users").document(uid).set({
        "uid": uid,
        "password": password,
        "login_time": datetime.now().isoformat()
    })

    return jsonify({"message": "로그인 및 저장 완료!"})


@home_bp.route("/home_tap/<uid>", methods=['GET'])
def user_home(uid):
    doc = db.collection("users").document(uid).get()

    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({"error": "사용자 정보를 찾을 수 없습니다."}), 404
