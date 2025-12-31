# Skinalyze (projet "Infrastructures et Systèmes Logiciels" - ENSAE 2025)

## Introduction
La documentation présentée ici vise à détailler et expliquer les aspects du site web _Skinalyze_. L'outil de _Skinalyze_ permet aux utilisateurs webs de recevoir un diagnostic de peau personnalisé à leur cas d'étude. Ce diagnostic personnalisé se base sur une image téléversée par l'usager. 
_Skinalyze_ est une première approche pour les clients dans le but de comprendre la santé dermatologique de leur peau. En plus de cela, un volet de recommendations et de conseils est mis à disposition pour des fins esthétiques cherchés par le client.
Puisque les files d'attente pour les professionnels de la médecine esthétique et dermatologique sont relativement allongées, _Skinalyze_ consiste à offrir aux utilisateurs une partie des soins conseillés par ces professionnels, à un coût moindre que ces derniers. C'est alors que _Skinalyze_ fournit un accès plus répandu et aisé aux soins dermatologiques pour tous les usagers, mais aussi aux conseils de nutrition.

## Objectif
À travers une fusion de langages de programmation et de développement, ce projet s'inscrit dans une logique de diffusion de l'usage versatile de la technologie pour répondre aux besoins quotidiens des usagers. Ainsi, _Skinalyze_ est une porte d'entrée vers les conseils de nutrition et de dermatologie, améliorés par l'intelligence artificielle (IA) pour offrir une expérience personnalisée aux clients. 

## Technologies utilisées
- __Back end__
  - Python : serveur backend principal
  - Docker : conteneurisation et déploiement de l'application
- __Front end__
  - HTML : structure des pages webs
  - CSS : personnalisation de style de l'interface web
  - Images statiques : ressources visuelles

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

Ensuite, un second test 

## Guide utilisateur (utilisation du site)


## Conception fonctionnelle
Cas d’utilisation

Parcours utilisateur

Description des pages

Page d’accueil

Page de connexion

Tableau de bord

Etc.

## Déploiement de l'application

Achat d'un domaine

## Conclusion
+++

Projet réalisé par : 
- Ben Belgacem Dikra
- Elamranijoutei Rime
- Mascret Arthur (Nujabest)
- Pidburachynskyi Arsen (apidburachynskyi)
- Tran Cindy (cindyoff)
