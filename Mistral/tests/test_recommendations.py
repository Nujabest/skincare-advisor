from backend.services.recommendation_service import get_recommendations

def test_get_recommendations_dry():
    recos = get_recommendations("Dry")
    assert isinstance(recos, list)
    assert len(recos) > 0
    assert "Utiliser une crème hydratante" in recos

def test_get_recommendations_oily():
    recos = get_recommendations("Oily")
    assert isinstance(recos, list)
    assert len(recos) > 0
    assert "Masque à l’argile" in recos

def test_get_recommendations_unknown():
    recos = get_recommendations("Unknown")
    assert isinstance(recos, list)
    assert len(recos) == 0
