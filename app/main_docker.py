'''
from fastapi import FastAPI, UploadFile, File, Request
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from app.model import CustomerData
import joblib
import pandas as pd
import json
import os
import io
import time
from datetime import datetime
import pandas as pd

# ==============================================================
# 0. Configuration de l’application FastAPI
# ==============================================================
app = FastAPI(title="API prédiction CLIENTS")

# =============================
# 1. Connexion à PostgreSQL
# =============================
# Configuration de la connexion à la base de données PostgreSQL
user = "postgres"
password = "1992"
host = "localhost"
port = "5432"
database = "customer_bank"  

# Création de l'engine SQLAlchemy pour la connexion
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# =============================
# 2. Modèles SQLAlchemy
# =============================
class InputEmploye(Base):
    __tablename__ = "inputs_customers"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OutputEmploye(Base):
    __tablename__ = "outputs_customers"
    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(Integer, nullable=False)
    label = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Création des tables
Base.metadata.create_all(bind=engine)


# ==============================================================
# 1. Chargement du modèle (au démarrage, pas à chaque requête)
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
    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log de la requête prédictive
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        return {"prediction": int(pred), "label": label}

    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)
        return {"error": "Erreur interne du serveur", "details": str(e)}
    
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
#LOG_DIR = "logs"
#LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")
#os.makedirs(LOG_DIR, exist_ok=True)

#Dossier de logs dans le conteneur Docker
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")

'''
if os.environ.get("GITHUB_ACTIONS") == "true":
    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
else:
    LOG_DIR = "/app/logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")
'''

'''
LOG_DIR = (
    os.path.join(os.path.dirname(__file__), "logs") 
    if os.environ.get("GITHUB_ACTIONS") == "true" 
    else os.environ.get("LOG_DIR", "./logs")
)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "api_logs.jsonl")
'''
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
from fastapi import FastAPI, UploadFile, File, Request
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
# 1. Chargement du modèle (au démarrage, pas à chaque requête)
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
    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log de la requête prédictive
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        return {"prediction": int(pred), "label": label}

    except Exception as e:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "error": str(e),
            "inputs": input_data,
            "status_code": 500
        }
        log_to_json(log_entry)
        return {"error": "Erreur interne du serveur", "details": str(e)}
 ''' 


'''
from fastapi import FastAPI, Request, HTTPException
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
# 1. Chargement du modèle (au démarrage, pas à chaque requête)  
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

def log_to_json(entry: dict):
    """Enregistre une ligne JSON dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger chaque requête HTTP (temps, code, endpoint, etc.)."""
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": 500,
            "execution_time_ms": round(latency, 2),
            "error": str(e)
        }
        log_to_json(log_entry)
        raise e

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
    start_time = time.time()
    input_data = data.dict()
    input_df = pd.DataFrame([input_data])

    try:
        pred = model.predict(input_df)[0]
        label = "Insolvable" if pred == 1 else "Solvable"
        latency = (time.time() - start_time) * 1000  # ms

        # Log détaillé de la prédiction
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "outputs": {"prediction": int(pred), "label": label},
            "latency_ms": round(latency, 2),
            "status_code": 200
        }
        log_to_json(log_entry)

        return {"prediction": int(pred), "label": label}

    except Exception as e:
        latency = (time.time() - start_time) * 1000
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": "/status_client_individuel",
            "inputs": input_data,
            "error": str(e),
            "latency_ms": round(latency, 2),
            "status_code": 500
        }
        log_to_json(log_entry)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
'''



'''
from fastapi import FastAPI, UploadFile, File
from app.model import CustomerData 
import joblib
import pandas as pd
import io

# 0. Création de l'application FastAPI
app = FastAPI(title="API prédiction CLIENTS")

# 1. Chargement du modèle
model = joblib.load("xgboost_features90.joblib")

# 2. Route pour prédiction individuelle
@app.post("/status_client_individuel")
def predict(data: CustomerData):
    input_df = pd.DataFrame([data.dict()])
    pred = model.predict(input_df)[0]
    label = "Insolvable" if pred == 1 else "Solvable"  # Harmonisé
    return {"prediction": int(pred), "label": label}

'''
'''
# 3. Route pour prédictions multiples via CSV

@app.post("/status_multiple_clients_via_csv")
async def status_clients(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"error": "Le fichier doit être au format CSV."}
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        required_columns = list(CustomerData.schema()["properties"].keys())
        # Ajouter colonnes manquantes si besoin
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[required_columns]

        preds = model.predict(df)
        df["prediction"] = preds
        df["prediction_label"] = df["prediction"].map({1: "Insolvable", 0: "Solvable"})
        df = df.reset_index().rename(columns={"index": "ligne"})
        return df[["ligne", "prediction_label"]].to_dict(orient="records")

    except Exception as e:
        return {"error": f"Erreur pendant le traitement du fichier : {str(e)}"}
        '''