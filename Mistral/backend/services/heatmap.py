import cv2
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_face_mesh = mp.solutions.face_mesh


def _add_overlay(image, points, color=(255, 0, 0), alpha=0.4):
    """Colorie une zone polygonale avec transparence."""
    overlay = image.copy()
    cv2.fillPoly(overlay, [np.array(points, dtype=np.int32)], color)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)


def add_heatmap(image_bytes, detected_problems):
    """Génère une heatmap sur les vraies zones problématiques."""

    # Lecture image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    h, w = img.shape[:2]

    # Model face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        result = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if not result.multi_face_landmarks:
            return image_bytes  # aucune détection

        face = result.multi_face_landmarks[0]

        # Convert landmarks → coordonnées pixels
        points = [(int(l.x * w), int(l.y * h)) for l in face.landmark]

        # Zones clés
        forehead = points[10:30]     # zone frontale
        left_eye = points[130:160]   # œil gauche
        right_eye = points[360:390]  # œil droit
        mouth = points[0:40]         # bouche + menton
        nose = points[100:150]       # nez

        # Heatmap dynamique selon problèmes IA
        if any("rides" in p for p in detected_problems):
            img = _add_overlay(img, forehead, color=(0, 0, 255), alpha=0.4)

        if any("pores" in p for p in detected_problems):
            img = _add_overlay(img, nose, color=(255, 128, 0), alpha=0.4)

        if any("imperfections" in p or "acné" in p for p in detected_problems):
            img = _add_overlay(img, cheeks := points[50:90], color=(0, 0, 255), alpha=0.4)

        if any("cernes" in p for p in detected_problems):
            img = _add_overlay(img, left_eye, color=(255, 0, 0), alpha=0.4)
            img = _add_overlay(img, right_eye, color=(255, 0, 0), alpha=0.4)

        # Export → bytes
        _, jpeg = cv2.imencode(".jpg", img)
        return jpeg.tobytes()
