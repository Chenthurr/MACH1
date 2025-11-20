# signal_controller.py - mock signal controller that accepts preemption commands
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/preempt', methods=['POST'])
def preempt():
    data = request.get_json()
    # simulate verifying GPS, siren match etc. For mock: accept and respond
    print("Signal preempt request:", data)
    # Return mock timing plan
    return jsonify({'status':'preempted', 'plan': {'green_for':30}})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
