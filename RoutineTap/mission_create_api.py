from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import random

routine_bp = Blueprint('routine', __name__, url_prefix='/api/routine')

@routine_bp.route('/assign-week', methods=['POST'])
def assign_weekly_routines():
    db = routine_bp.db
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id는 필수입니다."}), 400

    # 이번 주 월요일 계산
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_start_str = week_start.date().isoformat()

    # 기존 주간 루틴 있으면 중복 방지
    existing_query = db.collection("weekly_routines") \
        .where("user_id", "==", user_id) \
        .where("week_start", "==", week_start_str) \
        .stream()

    if any(existing_query):
        return jsonify({"message": "이미 주간 루틴이 존재합니다."}), 200

    # missions 컬렉션에서 5개 랜덤 선택
    all_missions = list(db.collection("missions").stream())
    selected = random.sample(all_missions, 5)

    mission_list = []
    for m in selected:
        mission_dict = m.to_dict()
        mission_list.append({
            "mission_id": m.id,
            "title": mission_dict.get("title"),
            "completed": False,
            "certification": None
        })

    # Firestore 저장
    data = {
        "user_id": user_id,
        "week_start": week_start_str,
        "missions": mission_list
    }
    db.collection("weekly_routines").add(data)
    return jsonify({"message": "주간 미션이 성공적으로 할당되었습니다."}), 201
