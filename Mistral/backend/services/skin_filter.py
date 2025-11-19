import cv2
import numpy as np

def beautify_image(image_bytes: bytes) -> bytes:
    """Applique un effet 'après-soin' : peau plus lisse, plus lumineuse, rougeurs réduites."""

    # Lire l’image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 1. Lissage léger de la peau
    smooth = cv2.bilateralFilter(img, d=15, sigmaColor=50, sigmaSpace=50)

    # 2. Réduction légère des rougeurs
    smooth[:, :, 2] = cv2.subtract(smooth[:, :, 2], 20)

    # 3. Boost de luminosité
    hsv = cv2.cvtColor(smooth, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.add(hsv[:, :, 2], 25) 
    final = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Encodage JPEG
    _, buffer = cv2.imencode(".jpg", final)
    return buffer.tobytes()
