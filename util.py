import os
import pickle
import numpy as np
import cv2

EMPTY = True

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "model", "model.p")

if not os.path.exists(model_path):
    raise FileNotFoundError("Không tìm thấy model.p")

MODEL = pickle.load(open(model_path, "rb"))

REVERSE_LABEL = False  # nếu toàn đỏ → đổi True


def empty_or_not(spot_bgr):
    try:
        if spot_bgr is None or spot_bgr.size == 0:
            return False

        img = cv2.resize(spot_bgr, (15, 15))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0

        flat = img.flatten().reshape(1, -1)
        y = MODEL.predict(flat)[0]

        return (y == 1) if REVERSE_LABEL else (y == 0)

    except:
        return False


def get_parking_spots_bboxes(connected_components):
    (totalLabels, _, values, _) = connected_components

    slots = []
    for i in range(1, totalLabels):
        x = int(values[i, cv2.CC_STAT_LEFT])
        y = int(values[i, cv2.CC_STAT_TOP])
        w = int(values[i, cv2.CC_STAT_WIDTH])
        h = int(values[i, cv2.CC_STAT_HEIGHT])

        if w * h > 500:
            slots.append([x, y, w, h])

    return slots