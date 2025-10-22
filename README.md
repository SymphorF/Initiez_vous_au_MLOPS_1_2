# Initiez_vous_au_MLOPS_2_2

L'objectif de ce travail est de déployer en production le modèle de scoring développé précédemment en créant une API conteneurisée avec Docker pour le département "Crédit Express". Il s'agit également de mettre en place un système de monitoring via un dashboard pour suivre les performances du modèle en environnement de production.

Ce projet utilise Python avec Poetry pour la gestion d'environnement virtuel, et JupyterLab pour l'exploration des données.

## 📁 Structure du projet

``` 
Projet-8/
├── .github/workflows/                       # Fichiers YAML définissant les workflows CI/CD de GitHub Actions
├── HUGGING_FACE_INITIEZ_VOUS_AU_MLOPS_1_2/  # Configuration et déploiement du modèle sur Hugging Face
├── app/                                     # Application principale (API, interface ou script Hugging Face)
├── cProfile/                                # Résultats et rapports du profilage des performances de l’API
├── drifts/                                  # Détection de dérive de données avec Evidently pour vérifier la cohérence du modèle en production
├── modeles/                                 # Modèles entraînés et sauvegardés (fichiers .joblib, .pkl, etc.)
├── notebook/                                # Notebooks Jupyter pour exploration, entraînement, et analyse
├── presentation/                            # Dossier de présentation du projet (PowerPoint, PDF, etc.)
├── tests/                                   # Tests unitaires et fonctionnels pour assurer la fiabilité du code
├── .gitignore                               # Liste des fichiers et dossiers à ignorer par Git
├── Dockerfile                               # Fichier de configuration Docker pour créer l’image du projet
├── README.md                                # Ce fichier
├── docker-compose.yml                       # Orchestration multi-conteneurs (API, base de données, monitoring, etc.)
├── poetry.lock                              # Verrouillage des versions des dépendances (généré automatiquement par Poetry)
├── profile_api.py                           # Script de profilage des performances de l’API
├── profile_api_optimized.py                 # Version optimisée du script de profilage
├── pyproject.toml                           # Fichier principal de configuration du projet et des dépendances (Poetry)
├── lien.txt                                 # Liens publics vers Hugging Face et GitHub
└── xgboost_features90.joblib                # Modèle XGBoost utilisé pour cette expérience
``` 

🚀 **Présentation du projet**
Ce projet vise à prédire des tester le tracking des modèles sur mlflow

⚙️ **Instructions**

1. Clonner le dépot :

bash

git clone https://github.com/SymphorF/Initiez_vous_au_MLOPS_1_2.git

cd Initiez_vous_au_MLOPS_1_2


2. Télécharger les données brutes sur Kaggle

https://www.kaggle.com/c/home-credit-default-risk/data

- application_test.csv
- application_train.csv
- bureau.csv
- bureau_balance.csv
- credit_card_balance.csv
- HomeCredit_columns_description.csv'
- installments_payments.csv
- POS_CASH_balance.csv
- previous_application.csv
- sample_submission.csv

3. Créer un environnement virtuel :

bash

poetry install

poetry shell  


4. Docker

Voici le workflow résumé :

- Builder l’image Docker (crée l’image avec l'application et ses dépendances) :

docker build -t fastapi-app .

- Lancer un conteneur à partir de l’image (exécuter l'app en arrière-plan, mapper le port 8000 du conteneur vers le PC) :

docker run -d -p 8000:8000 --name fastapi-app -v ./app/logs:/app/logs fastapi-app

- Accéder à l’API via le navigateur (FastAPI fournit automatiquement la documentation interactive Swagger) :

http://localhost:8000/docs (bien sûre en utilisant le post correct pour visualiser, dans ce exple c'est le port 8000)

- Pour afficher les logs 

docker cp fastapi-app:/app/logs/api_logs.jsonl ./api_logs.jsonl


**💡 Astuce :**

*Pour inspecter les logs du conteneur pour voir ce qui se passe :*

docker logs -f fastapi-app

*Pour visualiser les ports déjà utilisé par docker*

docker ps

*Pour arrêter un conteneur en particulier*

docker stop nom_du_conteneur (exp: docker stop eager_jemison)
docker rm nom_du_conteneur (exp: docker rm eager_jemison)

*Pour arrêter tous les conteneurs en même temps:*

docker stop $(docker ps -q)

*Pour supprimer tous les conteneurs (libérer les ports):*

docker rm $(docker ps -aq)

*Pour nettoyer tout le système Docker (arrêter tous les conteneurs, toutes les images non utilisées...):*

docker system prune -a

*Pour visualiser l'ensemble des images créées sur docker*

docker images

*Pour supprimer une image*

docker rmi id_image (exp docker rmi c111c74738e7)

Pensez à supprimer d'abord le conteneur utilisant cette image avant de la supprimer (voir méthode ci-dessus)


5. FastAPI

- L'API peut être lancé en local ou depuis docker

  * En local : 

    bash

    /app

    fastapi dev main.py

  * Depuis docker (voir l'étape 4) 

- Pour tester l'application FastAPI
   
  * Sur l'interface fastapi: 

    Cliquer sur "Try it out"

    Mettez les valeurs correspondantes des features (par défaut 0 partout) 

    Vous pouvez aussi recupérer les données de productions directement sur le ficher csv recupéré précédement, en faisant un copier-coller des features et une colonne au choix des valeurs de feature pour les introduire selon le format par défaut dans l'app FastAPI.

    Ensuite vérifiez le résultat sur la route en dessous "Client solvable" (correspondant à la valeur 0) ou "Client insolvable" (correspondant à la valeur 1).

    Vous pouvez tester plusieurs requettes.
  
  * Les requettes sont enregistrées de façon instantanée dans le fichier "api_logs.jsonl" situé dans le repertoire logs/

  * Pour remettre l'ensemble des logs enregistrées cliquez sur "DELETE" sur l'interface FastAPI.

6. Drifts

 Objectif : le drift ou dérive des données à pour objectif de détecter si le comportement des données réelles changent avec le temps

- Les données de production de ce test de drifts sont fictives, elles sont donc créées à partir de nos données brutes (car n'ayant pas des données réelles de production), voir données créées dans le notebook "Extract_data_drifts.ipynb" ces données  de production sont donc utilisées pour comparer au données de test pour vérifier le drift.

- Pour créer un rapport de drift en format html à partir de nos données, lancer le notebook "drift_test_evidently.ipynb"

- Enfin, à partir de l'étape II du notebook "Extract_data_drifts.ipynb", on prépare les mêmes données de production pour qu'elles correspondent au format demandé par l'application FastAPI, l'objectif étant de tester l'enregistrement des endpoints dans le log "api_log.jsonl", pour se faire, voir l'étape suivante

     
7. cProfile 

“Profiling des performances avec cProfile” 👇

*Afin d’analyser les performances de l’API et d’identifier les points de ralentissement (temps d’exécution du modèle, du chargement des données, etc.), un profilage est effectué à l’aide du module Python cProfile à partir du fichier **profile_api.py** à la racine du projet*

- Exécuter le profiling en local

 bash 

 à la racine du projet : 

 python profile_api.py *(Pour la version standard)*

 python profile_api_optimized.py *(Pour la version avec latence optimisée)*

 💡 Cela lancera plusieurs requêtes internes à l’API et affichera dans le terminal la liste des fonctions les plus lentes, avec leur temps d’exécution cumulé et moyen. Et la ligne de code stats.dump_stats() exportera les résultat dans un fichier à la racine appelé **"profiling_results.prof"** (pour les premiiers résultats) et **"profiling_results_optimized.prof"** (pour les résultats avec temps de latences optimisés) 


- Exploiter les résultats 

 Installer et lancer Snakeviz :

 pip install snakeviz

 bash 

 cProfile   

 snakeviz profiling_results.prof *(pour les premiers résultats)*

 snakeviz profiling_results_optimized.prof *(pour les résultats optimisés)*


 - (Optionnel) Exécuter le profiling dans Docker
 
 bash 

 *à la racine du projet :*

 *BUILDEZ*

 docker compose build
 
 *Une fois ton conteneur lancé, entre dedans :*

 docker ps

 docker exec -it fastapi-app bash

 python profile_api.py

 *pour sortir:*
 
 exit


8. Hugging Face

- Visualisez et tester l'app sur Hugging face

 Rendez-vous sur le lien https://huggingface.co/spaces/Symphor/HUGGING_FACE_INITIEZ_VOUS_AU_MLOPS_1_2

 Lorsque l'application est prête, cherchez un fichier en .csv client respectant le format des colonnes et introduisez dans l'app (voir le fichier nommé 'fichier_test.csv' dont le lien de téléchargement se trouve dans le fichier "liens" à la racine du projet)
 
 Lancez l'app en cliquant sur Submit sur l'interface HuggingFace pour visualiser les résultats


- Si vous souhaitez clonner le dépot HuggingFace et le déployer 
 
 Sur HuggingFace, cliquez sur NewSpace

 Remplissez les informations requises en vous assurant d'avoir le même nom de projet que celui du dossier (vous pouvez le renommer)

 Clonnez le projet

 bash  

 git clone https://huggingface.co/spaces/Symphor/HUGGING_FACE_INITIEZ_VOUS_AU_MLOPS_1_2


 cd HUGGING_FACE_INITIEZ_VOUS_AU_MLOPS_1_2 (si vous gardez le même nom)

 Utiliser app.py comme fichier principal.

 git add app.py

 git commit -m "Add application file"

 git push

 L'app est déployée sur votre space.
