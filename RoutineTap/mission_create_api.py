from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import random

# API 기능	            경로	                메서드	        요청값	                        반환값
# 주간 미션 배정	/api/routine/assign-week	POST	{ "uid": "abc123" }	{ "message": "주간 미션이 성공적으로 할당되었습니다." }

routine_bp = Blueprint('routine', __name__, url_prefix='/api/routine')

@routine_bp.route('/assign-week', methods=['POST'])
def assign_weekly_routines():
    db = routine_bp.db
    uid = request.json.get("uid")
    if not uid:
        return jsonify({"error": "uid는 필수입니다."}), 400

    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_start_str = week_start.date().isoformat()

    existing_query = db.collection("weekly_routines") \
        .where("uid", "==", uid) \
        .where("week_start", "==", week_start_str) \
        .stream()

    if any(existing_query):
        return jsonify({"message": "이미 주간 루틴이 존재합니다."}), 200

    all_missions = list(db.collection("missions").stream())
    selected = random.sample(all_missions, 5)

    mission_fields = {}
    for idx, m in enumerate(selected, start=1):
        mission_dict = m.to_dict()
        mission_fields[f"mission{idx}"] = {
            "mission_id": m.id,
            "completed": False
        }

    data = {
        "uid": uid,
        "week_start": week_start_str,
        **mission_fields
    }

    db.collection("weekly_routines").add(data)
    return jsonify({"message": "주간 미션이 성공적으로 할당되었습니다."}), 201


