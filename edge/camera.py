# camera.py - supports video file and RTSP
import cv2
import time

class RTSPCapture:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source {source}")
    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            # loop video for testing
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                return None
        return frame
    def release(self):
        self.cap.release()
