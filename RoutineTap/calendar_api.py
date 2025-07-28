from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@calendar_bp.route('/weekly-summary', methods=['GET'])
def get_weekly_summary():
    db = calendar_bp.db
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id는 필수입니다."}), 400

    # 이번 주 월요일 계산
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    week_start_str = week_start.date().isoformat()
    week_end_str = week_end.date().isoformat()

    # 루틴 가져오기
    routines_ref = db.collection("weekly_routines") \
        .where("user_id", "==", user_id) \
        .where("week_start", "==", week_start_str) \
        .limit(1)

    docs = list(routines_ref.stream())
    if not docs:
        return jsonify({"error": "이번 주 루틴이 존재하지 않습니다."}), 404

    data = docs[0].to_dict()
    missions = data.get("missions", [])

    completed_list = []
    remaining_routines = []

    for m in missions:
        if m.get("completed"):
            c = m.get("certification", {})
            completed_list.append({
                "routine_id": m.get("mission_id"),
                "title": m.get("title"),
                "content": c.get("content"),
                "date": c.get("date"),
                "image_url": c.get("image_url")
            })
        else:
            remaining_routines.append({
                "routine_id": m.get("mission_id"),
                "title": m.get("title")
            })

    total = len(missions)
    completed = len(completed_list)
    completion_rate = round(completed / total, 2) if total > 0 else 0

    return jsonify({
        "week_start": week_start_str,
        "week_end": week_end_str,
        "total_routines": total,
        "completed_routines": completed,
        "completion_rate": completion_rate,
        "completed_list": completed_list,
        "remaining_routines": remaining_routines
    }), 200
