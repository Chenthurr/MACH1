# dashboard endpoints or additional APIs
from flask import Flask, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'service': 'mach10-orchestrator', 'routes': ['/events']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
