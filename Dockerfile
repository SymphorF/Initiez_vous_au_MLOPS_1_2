# ================================
# 1️⃣ Image de base
# ================================
FROM python:3.12-slim

# ================================
# 2️⃣ Définir le répertoire de travail
# ================================
WORKDIR /app

# ================================
# 3️⃣ Installer Poetry
# ================================
RUN pip install --no-cache-dir poetry

# Désactiver la création d'environnements virtuels (on reste dans le global)
RUN poetry config virtualenvs.create false

# ================================
# 4️⃣ Copier les fichiers de dépendances
# ================================
COPY pyproject.toml poetry.lock* ./

# ================================
# 5️⃣ Installer les dépendances sans les dev
# ================================
RUN poetry install --no-root --without dev

# ================================
# 6️⃣ Créer le dossier de logs (utilisé dans ton code)
# ================================
RUN mkdir -p /app/logs

# ================================
# 7️⃣ Copier le code du projet
# ================================
COPY . .
# Copier spécifiquement le fichier de profilage
COPY profile_api.py /app/profile_api.py
# ================================
# 8️⃣ Exposer le port FastAPI
# ================================
EXPOSE 8000

# ================================
# 9️⃣ Commande de lancement
# ================================
CMD ["uvicorn", "app.main_docker:app", "--host", "0.0.0.0", "--port", "8000"]
