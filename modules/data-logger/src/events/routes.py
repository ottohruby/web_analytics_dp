from flask import request, jsonify, request
from src.events import bp
from src.pubsub import publish_to_pubsub

# todo check ts

def fix_dims(dims):
    req = [0, 2, 3, 6]
    ids = dict()
    fixed = []
    for item in dims:
        id = int(item.get('id'))
        val = str(item.get('val'))
        if ids.get(id):
            raise ValueError(f"Dimension '{id}' is in list more than once!")
        if id is not None and (val not in ('undefined', 'None')):
            fixed.append({'id': id, 'val': val} )
            ids[id] = 1

    # if(not ids.get(10)):
    #     fixed.append({'id': 10, 'val': request.headers.get('User-Agent')} )

    for id in req:
        if not ids.get(id):
            raise ValueError(f"Required dimension '{id}' is missing")
    return fixed

def fix_metrics(metrics):
    req = [0]
    ids = dict()
    fixed = []
    for item in metrics:
        id = int(item.get('id'))
        val = str(item.get('val'))
        unit = int(item.get('unit'))
        if ids.get(id):
            raise ValueError(f"Dimension '{id}' is in list more than once!")
        if id is not None and (val not in ('undefined', 'None')) and unit is not None:
            fixed.append({'id': id, 'val': val, 'unit': unit} )
            ids[id] = 1

    for id in req:
        if not ids.get(id):
            raise ValueError(f"Required dimension '{id}' is missing")
    return fixed

@bp.route('/collect/v1', methods=["POST", "GET"])
def collect_v1():
    if request.method != "POST":
        return jsonify({"error": "405 Method Not Allowed"}), 405
    
    if not request.is_json:
        return jsonify({"error": "400 Bad request - JSON body with at least 1 event is required"}), 400
    
    request_json = request.get_json()
    print(request_json)
    # events = request_json.get("events", [])

    if not request_json: # is instance of object
        return jsonify({"error": "400 Bad request - Body is not JSON"}), 400
    
    event = {}
    try:
        event['ev_ts'] = request_json['ev_ts']
        event['en_id'] = int(request_json['en_id'])
        event['lg_id'] = int(request_json['lg_id'])
        event['aw_id'] = int(request_json['aw_id'])
        event['dims'] = request_json['dims']
        event['metrics'] = request_json['metrics']
    except KeyError as e:
        return jsonify({"error": f"400 Bad request - {e} parameter is missing"}), 400
    except ValueError as e:
        return jsonify({"error": f"400 Bad request - {e} should be of type int"}), 400
    
    if len(event['dims']) < 1:
        return jsonify({"error": f"400 Bad request - event dims should have at least one param!"}), 400
    
    if len(event['metrics']) < 1:
        return jsonify({"error": f"400 Bad request - event metrics should have at least one param!"}), 400

    try:
        event['dims'] = fix_dims(event['dims'])
        event['metrics'] = fix_metrics(event['metrics'])
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({"error": f"400 Bad request - {e}"}), 400
    publish_to_pubsub(event)

    return jsonify({"processed data": event}), 200