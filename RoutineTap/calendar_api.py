from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone

# API 기능	                경로	               메서드	    요청값	                   
# 주간 달성률 조회	/api/calendar/weekly-summary	 GET	    ?uid=abc123

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@calendar_bp.route('/weekly-summary', methods=['GET'])
def get_weekly_summary():
    db = calendar_bp.db
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "uid는 필수입니다."}), 400

    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    week_start_str = week_start.date().isoformat()
    week_end_str = week_end.date().isoformat()

    docs = list(db.collection("weekly_routines")
        .where("uid", "==", uid)
        .where("week_start", "==", week_start_str)
        .limit(1)
        .stream())

    if not docs:
        return jsonify({"error": "이번 주 루틴이 존재하지 않습니다."}), 404

    routine_data = docs[0].to_dict()
    completed_list = []
    remaining_routines = []

    for i in range(1, 6):
        key = f"mission{i}"
        mission_entry = routine_data.get(key)
        if not mission_entry:
            continue

        mission_id = mission_entry.get("mission_id")
        completed = mission_entry.get("completed", False)

        if completed:
            cert_docs = list(db.collection("certifications")
                .where("uid", "==", uid)
                .where("mission_id", "==", mission_id)
                .order_by("date", direction="DESCENDING")
                .limit(1)
                .stream())
            if cert_docs:
                cert = cert_docs[0].to_dict()
                completed_list.append({
                    "routine_id": mission_id,
                    "title": cert.get("title"),
                    "description": cert.get("description"),
                    "image_url": cert.get("image_url"),
                    "date": cert.get("date")
                })
        else:
            mission_doc = db.collection("missions").document(mission_id).get()
            title = mission_doc.to_dict().get("title") if mission_doc.exists else "(알 수 없음)"
            remaining_routines.append({
                "routine_id": mission_id,
                "title": title
            })

    total = 5
    completed_count = len(completed_list)
    completion_rate = round(completed_count / total, 2)

    return jsonify({
        "week_start": week_start_str,
        "week_end": week_end_str,
        "total_routines": total,
        "completed_routines": completed_count,
        "completion_rate": completion_rate,
        "completed_list": completed_list,
        "remaining_routines": remaining_routines
    }), 200
