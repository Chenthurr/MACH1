Prereqs (local dev)

Docker & Docker Compose installed.

Optional: GPU drivers & nvidia-docker if you want GPU acceleration.

Download a YOLOv8 weight into edge/ (e.g., yolov8n.pt) or change config to use ultralytics default.

Steps

Put a short sample video into edge/test_videos/sample_road.mp4 (create edge/test_videos/ folder).

From repo root run:

docker-compose build
docker-compose up


Logs:

edge service prints detections and publishes events to cloud (HTTP POST to http://cloud:8080/event).

cloud receives events and forwards emergency preempts to signal_controller.

Verify:

Visit http://localhost:8080/events to see last events (from host; cloud container maps 8080).

Visit http://localhost:8090/status to confirm signal controller reachable.

5) Example: Integrating Real Ambulance GPS Verification (design note)

In production, before preempting signals, you should cross-validate:

GPS feed from ambulance (location + heading).

Siren audio detection (edge audio model).

Map matching to route.
Implement this in cloud/orchestrator.py as a verification pipeline before calling signal_controller/preempt.

6) Production hardening checklist

Use TLS for all endpoints (MQTT over TLS, HTTPS with certs).

Implement authentication and RBAC for edges and cloud (JWT/ECDSA).

Rate limiting and anti-spoofing: ensure only registered edges can send events; sign events.

Use a persistent DB (TimescaleDB/Postgres) for event storage, not in-memory list.

Use a managed MQTT broker (AWS IoT / Azure IoT Hub) for scale.

Replace SimpleTracker with robust trackers (ByteTrack, DeepSORT) for occlusion handling.

Add model monitoring and MLOps (Seldon, MLflow, ArgoCD) for model updates, A/B testing.

Privacy: anonymize, blur faces, redact license plates at edge. Store only metadata in cloud.

7) Testing utilities & small helper scripts
edge/test_emitter.py (to send synthetic events)
import requests, time
url = "http://localhost:8080/event"
for i in range(3):
    payload = {
        'ts': time.time(),
        'payload': [{'type':'EMERGENCY_PREEMPT','id':i,'class':'ambulance'}]
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.text)
    time.sleep(1)

8) Notes about YOLO labels for emergency vehicles & VRUs

Out-of-the-box COCO labels won't include "ambulance" or "rickshaw". Two options:

Fine-tune YOLOv8 on a dataset labelled for ambulances, rickshaws, auto-rickshaws, local VRUs.

Use class mapping heuristics: detect vehicle + emergency light pattern color + siren audio to infer ambulance.

For accurate rickshaw/cycle/rickshaw detection you should prepare a small local dataset (100–1000 annotated images) and train on top of pretrained weights.

9) Quick customization pointers

To switch edge to MQTT publish set publisher.method to mqtt in config.yaml.

To point to real RTSP, replace camera.source with rtsp://<user>:<pass>@camera-ip/stream.

Tune rules.preempt_cooldown to avoid frequent toggles.

10) Example minimal commit message for this repo
Initial fullstack scaffold: edge (YOLOv8+OpenCV, local rule engine), cloud (orchestrator + signal controller mock), docker-compose and docs for hybrid prototype.
