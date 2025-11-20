# tracker.py - simple IoU tracker, basic lifecycle
import time

class SimpleTracker:
    def __init__(self):
        self.tracks = {}  # id -> {'bbox':..., 'last_seen':...}
        self.next_id = 1

    def iou(self, a, b):
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        inter = max(0, x2-x1) * max(0, y2-y1)
        areaA = (a[2]-a[0])*(a[3]-a[1])
        areaB = (b[2]-b[0])*(b[3]-b[1])
        denom = areaA + areaB - inter + 1e-6
        return inter / denom

    def update(self, detections):
        matched = []
        updated = []
        # naive matching
        for det in detections:
            bbox = det['bbox']
            best_iou = 0
            best_tid = None
            for tid, t in list(self.tracks.items()):
                i = self.iou(bbox, t['bbox'])
                if i > best_iou:
                    best_iou = i
                    best_tid = tid
            if best_iou > 0.3:
                # assign
                self.tracks[best_tid]['bbox'] = bbox
                self.tracks[best_tid]['last_seen'] = time.time()
                updated.append({'id': best_tid, **det})
            else:
                tid = self.next_id
                self.tracks[tid] = {'bbox': bbox, 'last_seen': time.time()}
                self.next_id += 1
                updated.append({'id': tid, **det})
        # cleanup old
        now = time.time()
        for tid in list(self.tracks.keys()):
            if now - self.tracks[tid]['last_seen'] > 5:
                del self.tracks[tid]
        return updated
