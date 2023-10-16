from flask import request, jsonify, request
from src.events import bp
from src.pubsub import publish_to_pubsub

from datetime import datetime


def process_event(event):
    event['user_agent'] = request.headers.get('User-Agent')
    if 'event_timestamp' not in event or 'event_date' not in event:
        event["event_date"] = datetime.utcnow().strftime("%Y-%m-%d")
        event['event_timestamp_micros'] = int(datetime.utcnow().timestamp() * 1000)

    print(event)
    return event

@bp.route('/collect/v1', methods=["POST", "GET"])
def collect_v1():
    if request.method != "POST":
        return jsonify({"error": "405 Method Not Allowed"}), 405
    
    if not request.is_json:
        return jsonify({"error": "400 Bad request - JSON body with at least 1 event is required"}), 400
    
    request_json = request.get_json()
    events = request_json.get("events")

    if not events:
        return jsonify({"error": "400 Bad request - JSON body with at least 1 event is required"}), 400
    
    
    for event in events:
        processed_event = process_event(event)
        publish_to_pubsub(processed_event)


    return jsonify({"processed data": request_json}), 200