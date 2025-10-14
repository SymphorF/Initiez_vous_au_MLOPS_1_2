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


4. Lancer MLflow en local :

bash 

poetry shell

mlflow ui

http://127.0.0.1:5000


5. Docker

Voici le workflow résumé :

Builder l’image Docker (crée l’image avec l'application et ses dépendances) :

docker build -t fastapi-app .


Lancer un conteneur à partir de l’image (exécuter l'app en arrière-plan, mapper le port 8000 du conteneur vers le PC) :

docker run -d -p 8000:8000 --name fastapi-app fastapi-app


Accéder à l’API via le navigateur (FastAPI fournit automatiquement la documentation interactive Swagger) :

http://localhost:8000/docs


💡 Astuce :

Pour inspecter les logs du conteneur pour voir ce qui se passe :

docker logs -f fastapi-app