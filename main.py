import cv2
import time
import csv
import os
from datetime import datetime
from util import get_parking_spots_bboxes, empty_or_not
from tkinter import filedialog
import tkinter as tk

# ===== CHỌN VIDEO =====
root = tk.Tk()
root.withdraw()

video_path = filedialog.askopenfilename(
    title="Chọn video",
    filetypes=[("Video files", "*.mp4 *.avi")]
)

if video_path == "":
    print("Không chọn video!")
    exit()

cap = cv2.VideoCapture(video_path)

# ===== LOAD MASK =====
mask = cv2.imread("mask_1920_1080.png", 0)
connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
spots = get_parking_spots_bboxes(connected_components)

# ===== STATE =====
spot_states = [False] * len(spots)
start_times = [None] * len(spots)
saved_flag = [False] * len(spots)

# ===== TẠO THƯ MỤC =====
if not os.path.exists("images"):
    os.makedirs("images")

# ===== FILE CSV =====
log_path = os.path.join(os.getcwd(), "log.csv")
print("Log file:", log_path)

log_file = open(log_path, "a", newline="", encoding="utf-8")
writer = csv.writer(log_file)

if os.stat(log_path).st_size == 0:
    writer.writerow(["Vị trí", "Thời gian đỗ", "Giờ vào", "Giờ ra", "Ảnh"])
    log_file.flush()

frame_count = 0

# ===== LOOP =====
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    if frame_count % 5 == 0:
        new_states = []

        for i, (x, y, w, h) in enumerate(spots):
            spot = frame[y:y+h, x:x+w]

            if spot is None or spot.size == 0:
                new_states.append(False)
                continue

            new_states.append(empty_or_not(spot))

        now = time.time()

        for i in range(len(spots)):
            prev = spot_states[i]
            curr = new_states[i]

            # 🔴 → 🟢 (xe rời)
            if prev == False and curr == True:

                if start_times[i] is not None and not saved_flag[i]:

                    duration = int(now - start_times[i])

                    # ❌ bỏ nếu quá ngắn
                    if duration < 3:
                        continue

                    x, y, w, h = spots[i]

                    # ===== MỞ RỘNG KHUNG (FULL XE) =====
                    h_frame, w_frame, _ = frame.shape

                    pad_x = int(w * 0.6)
                    pad_y = int(h * 0.8)

                    x1 = max(0, x - pad_x)
                    y1 = max(0, y - pad_y)
                    x2 = min(w_frame, x + w + pad_x)
                    y2 = min(h_frame, y + h + pad_y)

                    img = frame[y1:y2, x1:x2]

                    filename = f"images/slot_{i}_{int(now)}.jpg"
                    cv2.imwrite(filename, img)

                    # ===== FORMAT TIME =====
                    start_str = datetime.fromtimestamp(start_times[i]).strftime("%d/%m/%Y %H:%M:%S")
                    end_str = datetime.fromtimestamp(now).strftime("%d/%m/%Y %H:%M:%S")

                    minutes = duration // 60
                    seconds = duration % 60
                    duration_str = f"{minutes:02d}:{seconds:02d}"

                    writer.writerow([f"A{i}", duration_str, start_str, end_str, filename])
                    log_file.flush()

                    saved_flag[i] = True

                    print(f"Saved: Slot {i}, {duration}s")

            # 🟢 → 🔴 (xe vào)
            if curr == False:
                if start_times[i] is None:
                    start_times[i] = now
                    saved_flag[i] = False
            else:
                start_times[i] = None

        spot_states = new_states

    # ===== HIỂN THỊ =====
    for i, (x, y, w, h) in enumerate(spots):
        color = (0, 255, 0) if spot_states[i] else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    cv2.imshow("Parking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
log_file.close()
cv2.destroyAllWindows()