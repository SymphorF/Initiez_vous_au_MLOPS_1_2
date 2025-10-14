# Utilisation d’une image Python légère
FROM python:3.12-slim

# Définir le dossier de travail
WORKDIR /app

# Installer Poetry
RUN pip install --no-cache-dir poetry

# Empêcher Poetry de créer un venv dans Docker
RUN poetry config virtualenvs.create false

# Copier fichiers de dépendances
COPY pyproject.toml poetry.lock* ./

# Installer les dépendances (sans dev)
RUN poetry install --no-root --without dev

# Créer le dossier de logs
RUN mkdir -p /app/logs

# Copier le projet
COPY . .

EXPOSE 8000

# Lancer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
