from flask import Flask, render_template, Response, send_from_directory, request, jsonify
import cv2
import csv
import os
import time
import threading
from datetime import datetime
from util import get_parking_spots_bboxes, empty_or_not

app = Flask(__name__)

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "log.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMAGE_DIR, exist_ok=True)

# ===== LOAD MASK =====
mask = cv2.imread(os.path.join(BASE_DIR, "mask_1920_1080.png"), 0)
cc = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
spots = get_parking_spots_bboxes(cc)

# ===== VIDEO =====
VIDEO_PATH = os.path.join(BASE_DIR, "parking_1920_1080.mp4")

cap_stream = cv2.VideoCapture(VIDEO_PATH)
cap_detect = cv2.VideoCapture(VIDEO_PATH)

# ===== STATE =====
spot_states = [False] * len(spots)
start_times = [None] * len(spots)
saved_flag = [False] * len(spots)

# ===== INIT CSV =====
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Vị trí", "Thời gian đỗ", "Giờ vào", "Giờ ra", "Ảnh"])


# ===== LOAD CSV =====
def load_data():
    try:
        with open(LOG_PATH, newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))[::-1]
    except:
        return []


# ===== DETECT THREAD =====
def detect_and_log():
    global cap_detect

    while True:
        ret, frame = cap_detect.read()

        if not ret:
            cap_detect.release()
            cap_detect = cv2.VideoCapture(VIDEO_PATH)
            continue

        now = time.time()

        for i, (x, y, w, h) in enumerate(spots):
            spot = frame[y:y+h, x:x+w]

            if spot is None or spot.size == 0:
                continue

            state = empty_or_not(spot)

            # xe vào
            if not state:
                if start_times[i] is None:
                    start_times[i] = now
                    saved_flag[i] = False

            # xe ra
            else:
                if start_times[i] and not saved_flag[i]:
                    duration = int(now - start_times[i])

                    if duration < 3:
                        continue

                    # ===== FULL XE =====
                    hF, wF, _ = frame.shape
                    pad_x = int(w * 0.6)
                    pad_y = int(h * 0.8)

                    x1 = max(0, x - pad_x)
                    y1 = max(0, y - pad_y)
                    x2 = min(wF, x + w + pad_x)
                    y2 = min(hF, y + h + pad_y)

                    img = frame[y1:y2, x1:x2]

                    filename = f"slot_{i}_{int(now)}.jpg"
                    filepath = os.path.join(IMAGE_DIR, filename)

                    cv2.imwrite(filepath, img)

                    # time format
                    start_str = datetime.fromtimestamp(start_times[i]).strftime("%d/%m/%Y %H:%M:%S")
                    end_str = datetime.fromtimestamp(now).strftime("%d/%m/%Y %H:%M:%S")
                    duration_str = f"{duration//60:02d}:{duration%60:02d}"

                    with open(LOG_PATH, "a", newline='', encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([f"A{i}", duration_str, start_str, end_str, filename])

                    print("Saved:", filename)

                    saved_flag[i] = True

                start_times[i] = None

        time.sleep(0.01)


# ===== VIDEO STREAM =====
def generate_frames():
    global cap_stream, spot_states

    frame_count = 0

    while True:
        success, frame = cap_stream.read()

        if not success:
            cap_stream.release()
            cap_stream = cv2.VideoCapture(VIDEO_PATH)
            continue

        frame_count += 1

        if frame_count % 5 == 0:
            for i, (x, y, w, h) in enumerate(spots):
                spot = frame[y:y+h, x:x+w]

                if spot is None or spot.size == 0:
                    continue

                spot_states[i] = empty_or_not(spot)

        empty_count = sum(spot_states)

        for i, (x, y, w, h) in enumerate(spots):
            color = (0, 255, 0) if spot_states[i] else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(frame,
                    f"Empty: {empty_count}/{len(spots)}",
                    (50, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255, 255, 255),
                    3)

        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        frame_bytes = buffer.tobytes()

        time.sleep(0.03)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# ===== ROUTES =====
@app.route("/", methods=["GET", "POST"])
def index():
    global VIDEO_PATH, cap_stream, cap_detect

    if request.method == "POST":
        file = request.files.get("video")
        if file:
            VIDEO_PATH = os.path.join(BASE_DIR, "input.mp4")
            file.save(VIDEO_PATH)

            cap_stream.release()
            cap_detect.release()

            cap_stream = cv2.VideoCapture(VIDEO_PATH)
            cap_detect = cv2.VideoCapture(VIDEO_PATH)

    return render_template("index.html", data=load_data())


@app.route("/api/log")
def api_log():
    return jsonify(load_data())


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)


# ===== RUN =====
if __name__ == "__main__":
    threading.Thread(target=detect_and_log, daemon=True).start()
    app.run(debug=True, use_reloader=False, threaded=True)