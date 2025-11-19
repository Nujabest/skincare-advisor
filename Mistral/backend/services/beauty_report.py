from typing import Optional, Dict, Any


def _format_list(items) -> str:
    if not items:
        return "aucun élément notable."
    if isinstance(items, str):
        return items
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " et " + items[-1]


def generate_premium_report(user, ai_results):
    """
    Rapport premium narratif, professionnel, basé uniquement sur :
    - Analyse IA de la photo
    - Âge
    - Sexe
    """

    if not user or not ai_results:
        return None

    age = getattr(user, "age", None)
    sexe = getattr(user, "sexe", None)

    score = ai_results.get("skin_score")
    type_peau = ai_results.get("type_peau") or "non déterminé"
    problemes = ai_results.get("problemes") or []
    recommandations = ai_results.get("recommandations") or []
    problemes_txt = ", ".join(problemes) if problemes else "aucune imperfection majeure"
    reco_txt = ", ".join(recommandations) if recommandations else None

    # ---------------------
    # TEXTE ULTRA PRO
    # ---------------------
    texte = ""

    # Intro – très professionnelle
    texte += (
        "Voici une analyse approfondie de l’état actuel de votre peau, réalisée à partir de la photo fournie "
        "et adaptée à votre profil dermatologique général. "
        "Cette évaluation met en lumière la qualité de la texture cutanée, l’équilibre hydrolipidique et "
        "les signes visibles pouvant influencer la santé et l’éclat de la peau. "
    )

    # Mention de l'âge & sexe uniquement si disponibles
    if age or sexe:
        texte += "Les recommandations ci-dessous sont ajustées en tenant compte de votre physiologie. "

    # État global
    texte += (
        f"\n\nL’état général de votre peau correspond actuellement à un type **{type_peau}**, "
        f"avec un score d’évaluation de **{score}/10**. "
        "Ce score reflète la qualité globale de la surface cutanée, la présence éventuelle d’irrégularités "
        "ainsi que l’homogénéité du teint."
    )

    # Problèmes observés
    texte += (
        f"\n\nL’analyse visuelle détecte principalement : **{problemes_txt}**. "
        "Ces éléments indiquent des zones où la peau nécessite une attention ciblée, "
        "notamment pour améliorer la régularité, la luminosité et la souplesse du tissu cutané."
    )

    # Recommandations
    if reco_txt:
        texte += (
            f"\n\nPour optimiser l’état de votre peau, il serait bénéfique de travailler sur : {reco_txt}. "
            "Ces axes d’amélioration permettent de renforcer la barrière cutanée, "
            "d’équilibrer la production de sébum et de stimuler la régénération cellulaire."
        )

    # Routine pro – PARAGRAPHE, PAS de puces
    texte += (
        "\n\nUne routine quotidienne adaptée peut significativement améliorer l’aspect et le confort de votre peau. "
        "Le matin, elle devrait commencer par un nettoyage doux, suivi d’un soin préparateur hydratant. "
        "L’application d’un sérum ciblé, choisi selon les besoins révélés par l’analyse, permettra d'optimiser "
        "l’efficacité de votre crème de jour. "
        "Une protection solaire doit être appliquée en dernière étape afin de prévenir le vieillissement cutané "
        "et les taches pigmentaires.\n\n"
        "Le soir, un double nettoyage soigné permettra d’éliminer impuretés et particules accumulées. "
        "Un sérum régénérant ou rééquilibrant aidera la peau à corriger les micro-altérations observées au cours de la journée. "
        "Enfin, une crème plus riche facilitera le renouvellement cellulaire nocturne et renforcera l’hydratation profonde."
    )

    # Hygiène de vie – paragraphes naturels
    texte += (
        "\n\nCertaines habitudes peuvent également soutenir vos progrès. "
        "Une bonne hydratation, un sommeil régulier et une exposition solaire contrôlée favorisent une peau plus lumineuse "
        "et plus résistante. L’alimentation joue un rôle essentiel : une consommation régulière d’antioxydants "
        "aide à limiter le stress oxydatif responsable du teint terne et du vieillissement prématuré."
    )

    # Conclusion douce et premium
    texte += (
        "\n\nEn combinant une routine adaptée, des gestes réguliers et un suivi des besoins identifiés, "
        "vous pourrez observer une amélioration progressive de la texture, de la luminosité et du confort cutané "
        "dans les semaines à venir."
    )

    return texte

    if user is None or ai_results is None:
        return None

    # Profil utilisateur
    age = getattr(user, "age", None)
    sexe = getattr(user, "sexe", None)
    type_habituel = getattr(user, "type_peau_habituel", None)
    sensibilites = getattr(user, "sensibilites", None)
    routine = getattr(user, "routine_actuelle", None)
    objectifs = getattr(user, "objectifs", None)

    # Analyse IA
    score = ai_results.get("skin_score")
    type_detecte = ai_results.get("type_peau") or "non déterminé"
    problemes = ai_results.get("problemes") or []
    recommandations = ai_results.get("recommandations") or []

    problemes_txt = _format_list(problemes)
    reco_txt = _format_list(recommandations)

    # Texte professionnel
    rapport = []

    # ================================
    # 1. Profil général
    # ================================
    intro = "## 🔍 Analyse professionnelle de votre peau\n\n"
    intro += "Cette évaluation combine votre profil personnel avec une analyse visuelle avancée.\n\n"

    if age or sexe or type_habituel:
        intro += "**Profil analysé :**\n"
        if age:
            intro += f"- Âge : environ **{age} ans**\n"
        if sexe:
            intro += f"- Genre renseigné : **{sexe}**\n"
        if type_habituel:
            intro += f"- Type de peau déclaré : **{type_habituel}**\n"
    else:
        intro += "_Peu d’informations personnelles renseignées — l’analyse reste donc plus générale._\n"

    rapport.append(intro)

    # ================================
    # 2. État global de la peau
    # ================================
    rapport.append(
        f"## 📊 État cutané global\n"
        f"- Score estimé : **{score}/10**\n"
        f"- Type détecté : **{type_detecte}**\n\n"
        f"L’évaluation tient compte de la texture de la peau, de l’uniformité du teint, de la présence de signes d’oxydation, "
        f"de la qualité de la barrière cutanée et de l’observation des zones sèches, grasses ou fragilisées.\n"
    )

    # ================================
    # 3. Analyse détaillée
    # ================================
    rapport.append(
        "## 🧪 Analyse détaillée des points observés\n"
        f"Les éléments suivants ont été identifiés : **{problemes_txt}**.\n\n"
        f"Cela peut refléter un déséquilibre hydrolipidique (eau/gras), une accumulation de kératine, "
        f"un relâchement cutané ou une sensibilité accrue selon les zones.\n"
    )

    # ================================
    # 4. Sensibilités (si déclarées)
    # ================================
    if sensibilites:
        rapport.append(
            "## ⚠️ Zones de vigilance personnelle\n"
            f"Vous avez mentionné une sensibilité particulière à : **{sensibilites}**.\n"
            "Cela doit être pris en compte dans le choix des textures et des actifs.\n"
        )

    # ================================
    # 5. Objectifs beauté
    # ================================
    if objectifs:
        rapport.append(
            "## 🎯 Objectifs déclarés\n"
            f"Vos priorités actuelles : **{objectifs}**.\n"
            "Les recommandations ci-dessous sont adaptées pour progresser efficacement.\n"
        )

    # ================================
    # 6. Recommandations expertes
    # ================================
    rapport.append(
        "## 🧴 Recommandations expertes\n"
        f"Selon l'analyse, les actions prioritaires seraient : **{reco_txt}**.\n\n"
        "Ce travail se concentre principalement sur l’amélioration de la barrière cutanée, la régulation du sébum, "
        "la réduction des imperfections et l’uniformité du teint.\n"
    )

    # ================================
    # 7. Routine matin & soir
    # ================================
    routine_txt = """
## 🌅 Routine matin (expert)
- Nettoyant doux (sans sulfate)
- Lotion hydratante pour préparer la peau
- Sérum adapté (niacinamide, vitamine C ou hydratant selon les besoins)
- Crème légère pour renforcer la barrière cutanée
- Protection solaire SPF 30+ (obligatoire, même par temps nuageux)

## 🌙 Routine soir (expert)
- Démaquillage + nettoyage doux
- Sérum ciblé :
  - anti-imperfections si pores dilatés
  - hydratant si peau déshydratée
  - anti-âge si ridules
- Crème nourrissante pour régénération nocturne
- Exfoliation douce 1–2 fois/semaine (AHA, BHA ou enzymatique selon sensibilité)
"""
    rapport.append(routine_txt)

    # ================================
    # 8. Hygiène de vie
    # ================================
    rapport.append(
        "## 🌿 Conseils complémentaires (hygiène de vie)\n"
        "- Hydratation régulière (1,5 L/jour minimum)\n"
        "- Exposition solaire contrôlée, filtre anti-UV indispensable\n"
        "- Sommeil réparateur (7–8h/nuit)\n"
        "- Réduction du stress (respiration, activité physique)\n"
        "- Alimentation riche en antioxydants (fruits rouges, vitamine C)\n"
    )

    # ================================
    # 9. Bilan final
    # ================================
    rapport.append(
        "## ✔️ Bilan\n"
        f"La peau présente : **{problemes_txt}**. Avec une routine stable, "
        "les premières améliorations visibles apparaissent généralement entre **3 et 6 semaines**.\n"
        "Une régularité dans les soins est essentielle pour optimiser les résultats."
    )

    return "\n\n".join(rapport)
