# app.py - orchestrates capture -> detect -> track -> rules -> publish
import yaml, time
from camera import RTSPCapture
from detector import YOLODetector
from tracker import SimpleTracker
from rule_engine import LocalRuleEngine
from publisher import EventPublisher
import cv2, os

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, 'config.yaml')) as f:
    cfg = yaml.safe_load(f)

cam = RTSPCapture(cfg['camera']['source'])
detector = YOLODetector(cfg['model'])
tracker = SimpleTracker()
engine = LocalRuleEngine(cfg['rules'])
publisher = EventPublisher(cfg['publisher'])

print("Edge node started. Camera:", cfg['camera']['source'])
try:
    while True:
        frame = cam.read()
        if frame is None:
            time.sleep(0.05)
            continue
        detections = detector.detect(frame)
        tracks = tracker.update(detections)
        actions = engine.evaluate(tracks)
        if actions:
            pub_resp = publisher.publish(actions)
            print("Published actions:", actions, "resp:", pub_resp)
        # small delay to limit CPU in local dev
        time.sleep(0.03)
except KeyboardInterrupt:
    cam.release()
    print("Shutting down edge node.")

