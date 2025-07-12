from flask import Blueprint, request, jsonify
from datetime import datetime
from firebase_admin import firestore

cert_bp = Blueprint("cert", __name__)
db = firestore.client()

@cert_bp.route("/submit_certification", methods=["POST"])
def submit_certification():
    data = request.json
    
    uid = data["uid"]
    mission = data["mission"]
    photo_url = data["photo_url"]

    today = datetime.now().strftime("%Y%m%d")
    doc_id = f"{uid}_{today}"

    db.collection("certifications").document(doc_id).set({
        "user_id": uid,
        "mission": mission,
        "date": today,
        "photo_url": photo_url
    })

    return jsonify({"message": "인증 저장 완료!"})

@cert_bp.route("/reword", methods=["get"])
def reword_point():
    data = request.json
    
