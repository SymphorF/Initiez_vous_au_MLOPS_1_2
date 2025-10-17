# Initiez_vous_au_MLOPS_1_2
Utilisez MLFlow pour tracker les expérimentations

Ce projet utilise Python avec Poetry pour la gestion d'environnement virtuel, et JupyterLab pour l'exploration des données.

## 📁 Structure du projet

``` 
Projet-4/
├── data_brut/ # Données brutes
├── data/ # Données aggrégées
├── .gitignore # Dossiers à ignorer par Git lors des pushs
├── images/ # Images matrices de confusions et score kaggle
├── mlruns # Base de données locale de mlflow
├── sample # Echantillons de modèles pour tests Kaggle
├── Fonkou_Symphor_1_notebook_120825.ipynb  # Notebooks Jupyter
├── pyproject.toml # Dépendances du projet
├── poetry.lock # Verrouillage des versions (auto-généré)
├── lien.txt # Lien publique de lancement mlflow
├── Presentation PP
└── README.md # Ce fichier
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

5. cProfile 

“Profiling des performances avec cProfile” 👇

*Afin d’analyser les performances de l’API et d’identifier les points de ralentissement (temps d’exécution du modèle, du chargement des données, etc.), un profilage est effectué à l’aide du module Python cProfile. à partir du fichier **profile_api.py** à la racine du projet*

- Exécuter le profiling en local

 bash 

 à la racine du projet : 

 python profile_api.py

 💡 Cela lancera plusieurs requêtes internes à l’API et affichera dans le terminal la liste des fonctions les plus lentes, avec leur temps d’exécution cumulé et moyen. Et la ligne de code stats.dump_stats("profiling_results.prof") exportera les résultat dans un fichier à la racine appelé "profiling_results.prof"

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
 

- Exploiter les résultats 

 Installer et lancer Snakeviz :

 pip install snakeviz

 bash 

 cProfile   

 snakeviz profiling_results.prof


