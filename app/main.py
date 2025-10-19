
'''
from fastapi import FastAPI, Request
from app.model import CustomerData
import joblib
import pandas as pd
import json
import os
import time
from datetime import datetime

# ==============================================================
# 0. Configuration de l’application FastAPI
# ==============================================================
app = FastAPI(title="API prédiction CLIENTS")

# ==============================================================
# 1. Chargement du modèle
# ==============================================================
MODEL_PATH = "xgboost_features90.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès depuis {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {e}")

# ==============================================================
# 2. Configuration du logging JSON
# ==============================================================

LOG_DIR = (
    os.path.join(os.path.dirname(__file__), "logs") 
    if os.environ.get("GITHUB_ACTIONS") == "true" 
    else os.environ.get("LOG_DIR", "./logs")
)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")

# compteur global (auto-incrément)
client_counter = 1

# Charger le dernier ID existant au redémarrage
if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            last_line = list(f)[-1]
            last_entry = json.loads(last_line)
            if "client_id" in last_entry:
                client_counter = last_entry["client_id"] + 1
    except Exception:
        client_counter = 1


def log_to_json(entry: dict):
    """Enregistre une ligne JSON dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger chaque requête HTTP (temps, code, endpoint, etc.)."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # en ms

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "execution_time_ms": round(process_time, 2)
    }
    log_to_json(log_entry)
    return response


# ==============================================================
# 3. Endpoint pour prédiction individuelle
# ==============================================================
@app.post("/status_client_individuel")
def predict(data: CustomerData):
    global client_counter

    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])
    client_id = client_counter  # ID auto-incrémenté pour chaque client

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log de la requête prédictive
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        # Incrémentation du compteur pour la prochaine requête
        client_counter += 1

        return {
            "client_id": client_id,
            "prediction": int(pred),
            "label": label
        }

    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)

        client_counter += 1
        return {
            "client_id": client_id,
            "error": "Erreur interne du serveur",
            "details": str(e)
        }


# ==============================================================
# 4. Endpoint pour vider les logs
# ==============================================================
@app.delete("/reset_logs")
def reset_logs():
    """Supprime les logs existants et remet la numérotation à 1."""
    global client_counter

    # Supprimer le fichier
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    client_counter = 1
    return {"message": "Logs supprimés avec succès. Numérotation réinitialisée à 1."}

'''










from fastapi import FastAPI, Request
from app.model import CustomerData
import joblib
import pandas as pd
import json
import os
import time
from datetime import datetime

# ==============================================================
# 0. Configuration de l’application FastAPI
# ==============================================================
app = FastAPI(title="API prédiction CLIENTS")

# ==============================================================
# 1. Chargement du modèle
# ==============================================================
MODEL_PATH = "xgboost_features90.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès depuis {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {e}")

# ==============================================================
# 2. Configuration du logging JSON
# ==============================================================


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)


'''
# def detect_docker():
#    """Détecte si le code tourne dans un conteneur Docker."""
#    try:
#        with open('/proc/1/cgroup', 'rt') as f:
#            content = f.read()
#            return 'docker' in content or 'kubepods' in content
#    except Exception:
#        return False


#if os.environ.get("GITHUB_ACTIONS") == "true":
#    # Environnement GitHub Actions (CI/CD)
#    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
#    LOG_FILE = os.path.join(LOG_DIR, "ci_logs.jsonl")

#elif detect_docker():
#    # Environnement Docker (production / conteneur)
#    LOG_DIR = "/app/logs"
#    LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")

#else:
#    # Environnement local (développement)
#    LOG_DIR = "./logs"
#    LOG_FILE = os.path.join(LOG_DIR, "local_logs.jsonl")

# Création du dossier si nécessaire
#os.makedirs(LOG_DIR, exist_ok=True)
'''

print(f"📂 Logs enregistrés dans : {LOG_FILE}")

# ==============================================================
# 3. Chargement du dernier ID client
# ==============================================================

# compteur global (auto-incrément)
client_counter = 1

# Charger le dernier ID existant au redémarrage
if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            last_line = list(f)[-1]
            last_entry = json.loads(last_line)
            if "client_id" in last_entry:
                client_counter = last_entry["client_id"] + 1
    except Exception:
        client_counter = 1


def log_to_json(entry: dict):
    """Enregistre une ligne JSON dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger chaque requête HTTP (temps, code, endpoint, etc.)."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # en ms

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "execution_time_ms": round(process_time, 2)
    }
    log_to_json(log_entry)
    return response


# ==============================================================
# 4. Endpoint pour prédiction individuelle
# ==============================================================
@app.post("/status_client_individuel")
def predict(data: CustomerData):
    global client_counter

    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])
    client_id = client_counter  # ID auto-incrémenté pour chaque client

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log de la requête prédictive
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        # Incrémentation du compteur pour la prochaine requête
        client_counter += 1

        return {
            "client_id": client_id,
            "prediction": int(pred),
            "label": label
        }

    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)

        client_counter += 1
        return {
            "client_id": client_id,
            "error": "Erreur interne du serveur",
            "details": str(e)
        }


# ==============================================================
# 5. Endpoint pour vider les logs
# ==============================================================
@app.delete("/reset_logs")
def reset_logs():
    """Supprime les logs existants et remet la numérotation à 1."""
    global client_counter

    # Supprimer le fichier
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    client_counter = 1
    return {"message": "Logs supprimés avec succès. Numérotation réinitialisée à 1."}

    









'''
from fastapi import FastAPI, Request
from app.model import CustomerData
import joblib
import pandas as pd
import json
import os
import time
from datetime import datetime

# ==============================================================
# 0. Configuration de l’application FastAPI
# ==============================================================
app = FastAPI(title="API prédiction CLIENTS")

# ==============================================================
# 1. Chargement du modèle
# ==============================================================
MODEL_PATH = "xgboost_features90.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès depuis {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {e}")

# ==============================================================
# 2. Configuration du logging JSON
# ==============================================================

def detect_docker():
    """Détecte si on tourne dans un conteneur Docker."""
    try:
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read() or 'kubepods' in f.read()
    except Exception:
        return False

if os.environ.get("GITHUB_ACTIONS") == "true":
    # CI/CD GitHub
    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
elif detect_docker():
    # Environnement Docker
    LOG_DIR = "/app/logs"
else:
    # Local
    LOG_DIR = "./logs"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")

print(f"📂 Logs enregistrés dans : {LOG_FILE}")

# ==============================================================
# 3. Chargement du dernier ID client
# ==============================================================

# compteur global (auto-incrément)
client_counter = 1

# Charger le dernier ID existant au redémarrage
if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            last_line = list(f)[-1]
            last_entry = json.loads(last_line)
            if "client_id" in last_entry:
                client_counter = last_entry["client_id"] + 1
    except Exception:
        client_counter = 1


def log_to_json(entry: dict):
    """Enregistre une ligne JSON dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger chaque requête HTTP (temps, code, endpoint, etc.)."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # en ms

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "execution_time_ms": round(process_time, 2)
    }
    log_to_json(log_entry)
    return response


# ==============================================================
# 4. Endpoint pour prédiction individuelle
# ==============================================================
@app.post("/status_client_individuel")
def predict(data: CustomerData):
    global client_counter

    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])
    client_id = client_counter  # ID auto-incrémenté pour chaque client

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log de la requête prédictive
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        # Incrémentation du compteur pour la prochaine requête
        client_counter += 1

        return {
            "client_id": client_id,
            "prediction": int(pred),
            "label": label
        }

    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)

        client_counter += 1
        return {
            "client_id": client_id,
            "error": "Erreur interne du serveur",
            "details": str(e)
        }


# ==============================================================
# 5. Endpoint pour vider les logs
# ==============================================================
@app.delete("/reset_logs")
def reset_logs():
    """Supprime les logs existants et remet la numérotation à 1."""
    global client_counter

    # Supprimer le fichier
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    client_counter = 1
    return {"message": "Logs supprimés avec succès. Numérotation réinitialisée à 1."}

'''





'''
from fastapi import FastAPI, Request
from app.model import CustomerData
import joblib
import pandas as pd
import json
import os
import time
from datetime import datetime
import cProfile

# ==============================================================  
# 0. Configuration de l’application FastAPI  
# ==============================================================  
app = FastAPI(title="API prédiction CLIENTS")

# ==============================================================  
# 1. Chargement du modèle  
# ==============================================================  
MODEL_PATH = "xgboost_features90.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès depuis {MODEL_PATH}")
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {e}")

# ==============================================================  
# 2. Configuration du logging JSON  
# ==============================================================  
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)

print(f"📂 Logs enregistrés dans : {LOG_FILE}")

# ==============================================================  
# 3. Chargement du dernier ID client  
# ==============================================================  
client_counter = 1

if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            last_line = list(f)[-1]
            last_entry = json.loads(last_line)
            if "client_id" in last_entry:
                client_counter = last_entry["client_id"] + 1
    except Exception:
        client_counter = 1


def log_to_json(entry: dict):
    """Enregistre une ligne JSON dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger chaque requête HTTP (temps, code, endpoint, etc.)."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # en ms

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "execution_time_ms": round(process_time, 2)
    }
    log_to_json(log_entry)
    return response


# ==============================================================  
# 4. Endpoint pour prédiction individuelle (avec profilage)  
# ==============================================================  
@app.post("/status_client_individuel")
def predict(data: CustomerData):
    global client_counter

    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])
    client_id = client_counter  # ID auto-incrémenté pour chaque client

    # === Activation du profilage ===
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # === Arrêt du profilage ===
        profiler.disable()

        # === Sauvegarde du profil ===
        profile_file = os.path.join(LOG_DIR, f"profile_{client_id}.prof")
        profiler.dump_stats(profile_file)

        # === Enregistrement dans les logs JSONL ===
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "profile_file": profile_file,  # 🔗 lien vers fichier de profil
            "status_code": 200
        }
        log_to_json(log_entry)

        client_counter += 1

        return {
            "client_id": client_id,
            "prediction": int(pred),
            "label": label
        }

    except Exception as e:
        profiler.disable()
        client_counter += 1

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_id": client_id,
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)

        return {
            "client_id": client_id,
            "error": "Erreur interne du serveur",
            "details": str(e)
        }


# ==============================================================  
# 5. Endpoint pour vider les logs  
# ==============================================================  
@app.delete("/reset_logs")
def reset_logs():
    """Supprime les logs existants et remet la numérotation à 1."""
    global client_counter

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    client_counter = 1
    return {"message": "Logs supprimés avec succès. Numérotation réinitialisée à 1."}
'''