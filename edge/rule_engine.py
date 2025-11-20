# rule_engine.py - deterministic local rules
import time
from collections import defaultdict

class LocalRuleEngine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.last_preempt = 0
        self.person_counts = defaultdict(int)

    def evaluate(self, tracks):
        actions = []
        # simple aggregations: count persons in this frame
        person_count = 0
        for t in tracks:
            cls = t['class']
            if cls == 'person' and t['conf'] > 0.5:
                person_count += 1
        # pedestrian hold logic
        if person_count >= self.cfg.get('pedestrian_hold_threshold', 3):
            actions.append({'type': 'HOLD_FOR_PEDESTRIANS', 'count': person_count})
        # emergency preempt detection
        for t in tracks:
            cls = t['class']
            if cls in ['fire engine', 'ambulance', 'emergency vehicle', 'truck']: # adapt class names as model provides
                if t['conf'] > 0.6 and time.time() - self.last_preempt > self.cfg.get('preempt_cooldown', 8):
                    actions.append({'type': 'EMERGENCY_PREEMPT', 'id': t['id'], 'class': cls})
                    self.last_preempt = time.time()
        return actions
