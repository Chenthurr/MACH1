# orchestrator.py - receive events from edges and decide actions (very simple)
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import requests
app = Flask(__name__)
CORS(app)

# simple in-memory store
events = []

@app.route('/event', methods=['POST'])
def event():
    payload = request.get_json()
    if not payload:
        return jsonify({"status":"bad_request"}), 400
    # store minimal
    events.append(payload)
    # simple validation + escalation
    actions = []
    for act in payload.get('payload', []):
        if act.get('type') == 'EMERGENCY_PREEMPT':
            # mock call to signal controller
            try:
                sc_resp = requests.post('http://signal_controller:8090/preempt', json={'id': act.get('id'), 'class': act.get('class')}, timeout=1)
                actions.append({'escalated': True, 'signal_resp': sc_resp.text})
            except Exception as e:
                actions.append({'escalated': False, 'error': str(e)})
        elif act.get('type') == 'HOLD_FOR_PEDESTRIANS':
            # store for dashboard analytics
            actions.append({'held': True, 'count': act.get('count')})
    return jsonify({'status':'ok', 'actions': actions})

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events[-100:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
