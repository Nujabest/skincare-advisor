import cv2
import numpy as np


def analyze_skin(image_path: str) -> dict:
    img = cv2.imread(image_path)

    # Simuler des indicateurs
    brightness = np.mean(img)
    redness = np.mean(img[:, :, 2])

    return {"brightness": brightness, "redness": redness}
