# detector.py - ultralytics YOLO wrapper
from ultralytics import YOLO
import numpy as np

class YOLODetector:
    def __init__(self, cfg):
        weights = cfg.get('weights', 'yolov8n.pt')
        self.model = YOLO(weights)
        self.conf = cfg.get('conf', 0.35)
        # Optionally restrict classes (e.g., person, bicycle, car, ambulance-class) by mapping.
        self.names = self.model.names

    def detect(self, frame):
        # model returns results list; we use predict with numpy array
        results = self.model.predict(source=frame, conf=self.conf, device='0', verbose=False)
        detections = []
        for r in results:
            boxes = r.boxes
            if boxes is None:
                continue
            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                name = self.names.get(cls, str(cls))
                detections.append({'class': name, 'conf': conf, 'bbox': [int(x1),int(y1),int(x2),int(y2)]})
        return detections
