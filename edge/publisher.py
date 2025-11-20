# publisher.py - supports HTTP and MQTT
import json, time, requests
import paho.mqtt.client as mqtt

class EventPublisher:
    def __init__(self, cfg):
        self.cfg = cfg
        method = cfg.get('method', 'http')
        self.method = method
        if method == 'mqtt':
            self.client = mqtt.Client()
            host = cfg['mqtt']['host']
            port = cfg['mqtt'].get('port', 1883)
            self.topic = cfg['mqtt'].get('topic', 'mach10/events')
            self.client.connect(host, port)
        else:
            self.url = cfg['http']['url']

    def publish(self, payload):
        data = {'ts': time.time(), 'payload': payload}
        if self.method == 'mqtt':
            self.client.publish(self.topic, json.dumps(data))
        else:
            try:
                r = requests.post(self.url, json=data, timeout=2)
                return r.status_code, r.text
            except Exception as e:
                print("Publish HTTP error:", e)
