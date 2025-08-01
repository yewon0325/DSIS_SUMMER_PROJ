from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone

# API 기능	            경로	        메서드	                      요청값	                            
# 미션 인증	    /api/routine/complete	POST	{"uid": "abc123","mission_id": "m001","description": "텀블러 들고 다녔습니다!","image_url": "https://yourcdn.com/abc123/tumbler.jpg"}

routine_bp = Blueprint('routine', __name__, url_prefix='/api/routine')

@routine_bp.route('/complete', methods=['POST'])
def complete_routine():
    db = routine_bp.db
    data = request.json

    uid = data.get("uid")
    mission_id = data.get("mission_id")
    description = data.get("description")
    image_url = data.get("image_url")

    if not all([uid, mission_id, description, image_url]):
        return jsonify({"error": "uid, mission_id, description, image_url는 필수입니다."}), 400

    now = datetime.now(timezone.utc)
    week_start = (now - timedelta(days=now.weekday())).date().isoformat()

    docs = db.collection("weekly_routines") \
        .where("uid", "==", uid) \
        .where("week_start", "==", week_start) \
        .limit(1).stream()

    doc_list = list(docs)
    if not doc_list:
        return jsonify({"error": "해당 주간 미션을 찾을 수 없습니다."}), 404

    doc_ref = doc_list[0].reference
    routine_data = doc_list[0].to_dict()

    # 미션 찾기
    target_key = None
    for i in range(1, 6):
        key = f"mission{i}"
        mission = routine_data.get(key, {})
        if mission.get("mission_id") == mission_id:
            target_key = key
            break

    if not target_key:
        return jsonify({"error": "이번 주 루틴에 해당 미션이 없습니다."}), 404

    # 미션 정보 가져오기
    mission_doc = db.collection("missions").document(mission_id).get()
    if not mission_doc.exists:
        return jsonify({"error": "해당 미션이 존재하지 않습니다."}), 404

    mission_data = mission_doc.to_dict()
    carbon_reduction = mission_data.get("carbon_reduction", 0.0)
    title = mission_data.get("title")

    # 루틴 업데이트
    routine_data[target_key]["completed"] = True
    routine_data[target_key]["date"] = now.isoformat()
    doc_ref.update({target_key: routine_data[target_key]})

    # 인증 저장
    db.collection("certifications").add({
        "uid": uid,
        "mission_id": mission_id,
        "title": title,
        "description": description,
        "image_url": image_url,
        "date": now,
        "carbon_reduction": carbon_reduction
    })

    # 유저 탄소 감소 업데이트
    user_ref = db.collection("users").document(uid)
    user_snapshot = user_ref.get()
    current_total = user_snapshot.to_dict().get("total_carbon_reduction", 0.0) if user_snapshot.exists else 0.0
    new_total = round(current_total + carbon_reduction, 2)
    user_ref.update({"total_carbon_reduction": new_total})

    return jsonify({
        "message": "미션 인증이 완료되었습니다.",
        "carbon_reduction": carbon_reduction,
        "total_carbon_reduction": new_total
    }), 200
