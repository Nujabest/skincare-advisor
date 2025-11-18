import numpy as np
from engine.analyze import analyze_skin

def test_analyze_skin(tmp_path):
    # Génère une fausse image blanche 100x100
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    path = tmp_path / "test.jpg"

    import cv2
    cv2.imwrite(str(path), img)

    # Exécution du moteur
    result = analyze_skin(str(path))

    # Vérifications
    assert "brightness" in result
    assert result["brightness"] > 0
