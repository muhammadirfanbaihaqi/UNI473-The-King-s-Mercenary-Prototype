from ultralytics import YOLO

def load_model(model_path):
    return YOLO(model_path)

def detect_koi(model, frame):
    results = model.predict(source=frame, conf=0.5, verbose=False)[0]
    boxes = []
    for r in results.boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = map(int, r)
        boxes.append((x1, y1, x2, y2))
    return boxes
