# Skinalyze (projet "Infrastructures et Systèmes Logiciels" - ENSAE 2025)

## Introduction
La documentation présentée ici vise à détailler et expliquer les aspects du site web _Skinalyze_. L'outil de _Skinalyze_ permet aux utilisateurs webs de recevoir un diagnostic de peau personnalisé à leur cas d'étude. Ce diagnostic personnalisé se base sur une image téléversée par l'usager. 
_Skinalyze_ est une première approche pour les clients dans le but de comprendre la santé dermatologique de leur peau. En plus de cela, un volet de recommendations et de conseils est mis à disposition pour des fins esthétiques cherchés par le client.
Puisque les files d'attente pour les professionnels de la médecine esthétique et dermatologique sont relativement allongées, _Skinalyze_ consiste à offrir aux utilisateurs une partie des soins conseillés par ces professionnels, à un coût moindre que ces derniers. C'est alors que _Skinalyze_ fournit un accès plus répandu et aisé aux soins dermatologiques pour tous les usagers, mais aussi aux conseils de nutrition.

## Objectif
À travers une fusion de langages de programmation et de développement, ce projet s'inscrit dans une logique de diffusion de l'usage versatile de la technologie pour répondre aux besoins quotidiens des usagers. Ainsi, _Skinalyze_ est une porte d'entrée vers les conseils de nutrition et de dermatologie, améliorés par l'intelligence artificielle (IA) pour offrir une expérience personnalisée aux clients. Il est important de noter que les conseils résultant de _Skinalyze_ ne remplacent en aucun cas les conseils et soins procurés par un professionnel de la santé, _Skinalyze_ figure tel un outil d'aide à la décision. 

## Technologies utilisées
- __Back end__
  - Python (version 3.11) : serveur backend principal
    - Werkzeug : sécurisation des noms de fichiers (utilitaire Flask)
  - Docker : conteneurisation de l'application
  - SQLite3 : base de données locale pour stocker l'historique des analyses
  - API Mistral AI : Vision Language Model (modèle ```pixtral-12b-2409```) utilisé pour les analyses d'images et pour les générations de diagnostics de peau
- __Front end__
  - HTML : structure des pages webs
  - Flask : framework Python pour créer l'application
    - Jinja2 : moteur de templates Flask
  - CSS : personnalisation de style de l'interface web
  - Images statiques : ressources visuelles
- __Utilitaires__
  - JSON :
    - Extraction de métriques depuis les réponses de Mistral AI
    - Stockage de données structurées
  - Regex (re) :
    - Nettoyage du texte généré
  - Base64 :
    - Encodage d'images pour l'API Mistral AI
- __Déploiement___
  - Docker :
    - Déploiement de l'application
    - Conteneurisation
    - Orchestration des services
- __Sécurité__
  - Hook (```@app.before_request```) : authentification pour protéger les routes
  - Flask : clé pour permettre des sessions sécurisées

## Architecture du projet
Le schéma ci-dessous détaille l'arborescence du projet, en spécifiant les fichiers et leur dossier associé. 

```
skincare-advisor/─ static/
│   ├── hero.png
│   ├── main.css
│── templates/
│   ├── history.html
│   ├── landing.html
│   ├── layout.html
│   ├── login.html
│   └── processing.html
│   └── result.html
│   └── upload.html
│── tests/
│   ├── conftest.py
│   ├── test_app.py
│── .dockerignore
│── .gitignore
│── README.md
│── app.py
│── docker-compose.yaml
│── dockerfile
│── requirements.txt
```

 
## Tests de validation et de robustesse
Afin de tester la robustesse, et donc de valider les commandes, des tests unitaires ont été mobilisés dans cette situation. 

Tout d'abord, le premier test unitaire (```test_app.py```) vise à tester l'application web de _Skinalyze_. Les élements ci-dessous répertorie une poignée d'exemples pour mieux comprendre ce que ce premier test unitaire englobe. 
- ```test_analyze_without_upload``` : test de la gestion d'erreur quand une image n'est pas téléversée
- ```test_history_page``` : test de l'accès à l'historique des analyses
-```test_result_contains_metrics``` : affichage complet des résultats d'analyse

Ensuite, un second test (```conftest.py```), sous la forme d'un fichier de configuration pytest, permet d'expérimenter l'environnement de test pour l'application. Cet environnement prépare un contexte isolé et prévisible pour tous les tests. Les exemples ci-dessous élaborent le contenu de ce test : 
- ```small.png``` : génération d'une image, sous format PNG, valide pour éviter de fournir une image externe de test
- ```@pytest.fixture client``` : élément principal de ce test, dans lequel un client complet est configuré pour préparer aux différents tests ultérieurs

## Guide utilisateur (utilisation du site)
Cette section a pour but de guider l'utilisateur à naviguer le site web _Skinalyze_,  mais aussi de détailler les pages webs disponibles. 

1. Page d'accueil (connexion)
2. Téléversement d'une image
3. Consultation du diagnostic personnalisé
4. Historique

Le site web présente au total 4 pages, incluant l'historique. L'ordre d'utilisation est comme la liste ci-dessus. 

Tout d'abord, l'utilisateur est mené vers la page d'accueil qui présente le site web avec une brève présentation, pour ensuite se connecter à son propre compte. En second lieu, l'utilisateur commence son expérience avec le téléversement d'une image. Il faut savoir que le site web n'accepte que les images sous format WEBP, JPG, JPEG et PNG. Lors de la sélection de l'image, l'utilisateur peut rajouter, sous forme de texte, des commentaires pouvant aider à étayer son futur diagnostic. 
Après validation de l'image sélectionnée, l'utilisateur se retrouve alors sur son diagnostic personnel. Six mesures sont mises en place pour résumer la situation de l'utilisateur, basée sur l'image :
- Acné : existence d'acné ou non
- Risque irritation
- Confiance : niveau de confiance de l'analyse IA générée
- Urgence : urgence de traitement ou non
- Score peau : score sur 100 points au total, permettant d'indiquer à l'utilisateur l'amélioration possible de sa condition dermatologique
- Inflammation : présence ou non d'une zone d'inflammation sur la peau
Un diagnostic plus complet est fourni, contenant les conseils de routine, de nutrition et de compléments alimentaires. Une section dédiée à la consultation chez un professionnel de santé est impérativement insérée comme rappel pour l'utilisateur.
Enfin, le client aura le choix de voir son historique d'analyse, ainsi que de refaire une analyse pour une autre zone de peau. 

## Déploiement de l'application
Le déploiement de l'application s'est fait à travers une conteneurisation sous Docker. En parallèle, un achat d'un nom de domaine a été effectué afin d'héberger le site web de [Skinalyze](https://www.skinalyze.xyz). Le site web est alors consultable depuis le lien fourni précédemment. Seul un compte est nécessaire pour accéder et bénéficier des services de _Skinalyze_. 

## Conclusion
Ce projet _Skinalyze_ est une application web d'analyse de peau qui combine des langages de programmation et l'intelligence artificielle (IA) de Mistral AI. Elle permet aux utilisateurs de télécharger des photos, d'obtenir des analyses automatisées avec des recommandations personnalisées et de consulter leur historique.
L'architecture utilise SQLite, Flask et Docker pour créer une solution légère et portable. L'intégration de l'API Mistral Vision démontre une intégration des technologies d'IA, avec extraction structurée de métriques et génération de diagnostics détaillés.
Pour alimenter la complétude du projet, des tests unitaires et de configuration, couvrant un large champ de développement, ont été inclus. 
_Skinalyze_ illustre alors comment l'IA peut être mise au service de la santé dermatologique à travers une application web accessible et intuitive.

Projet réalisé par : 
- Ben Belgacem Dikra
- Elamranijoutei Rime
- Mascret Arthur (Nujabest)
- Pidburachynskyi Arsen (apidburachynskyi)
- Tran Cindy (cindyoff)
