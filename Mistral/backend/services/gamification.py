def compute_progression(analyses):
    """Retourne amélioration du score depuis la première analyse."""
    if len(analyses) < 2:
        return None

    first = analyses[0].skin_score or 0
    last = analyses[-1].skin_score or 0

    if first == 0:
        return None

    return round(((last - first) / first) * 100, 2)


def compute_badges(analyses):
    badges = []

    # Badge : 3 analyses
    if len(analyses) >= 3:
        badges.append("🎖️ Découverte : Vous avez réalisé 3 analyses !")

    # Badge : amélioration
    prog = compute_progression(analyses)
    if prog and prog > 5:
        badges.append(f"🌱 Amélioration : +{prog}% depuis vos débuts !")

    # Badge : constance
    if len(analyses) >= 7:
        badges.append("🔥 Constance : 7 jours de routine suivie !")

    return badges, prog
