from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

# API 기능	            경로	   메서드	            요청값	                            반환값
# 월별 인증 개수 조회	/api/calendar	GET	   ?uid=abc123&month=2025-07	    { "2025-07-01": 1, "2025-07-04": 2, ... }

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')

@calendar_bp.route('', methods=['GET'])
def get_calendar_view():
    db = calendar_bp.db
    uid = request.args.get('uid')
    month = request.args.get('month')  # 형식: "2025-07"

    if not uid or not month:
        return jsonify({'error': 'uid와 month는 필수입니다. (예: 2025-07)'}), 400

    try:
        start_date = datetime.strptime(month + "-01", "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({'error': 'month 형식이 잘못되었습니다. 예: 2025-07'}), 400

    # 다음 달 1일 계산
    if start_date.month == 12:
        end_date = datetime(start_date.year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_date = datetime(start_date.year, start_date.month + 1, 1, tzinfo=timezone.utc)

    # Firestore 쿼리 (uid만 필터)
    query = db.collection('certifications') \
            .where('uid', '==', uid)

    all_docs = query.stream()
    result = {}

    for doc in all_docs:
        data = doc.to_dict()
        verified_at = data.get("date")

        if not verified_at or verified_at < start_date or verified_at >= end_date:
            continue

        date_str = verified_at.date().isoformat()
        result[date_str] = result.get(date_str, 0) + 1

    return jsonify(result), 200