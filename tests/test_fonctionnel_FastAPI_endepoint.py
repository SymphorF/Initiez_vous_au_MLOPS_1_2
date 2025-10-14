import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app  # ton app FastAPI

client = TestClient(app)

def test_predict_endpoint():
    payload = {"feature1": 3.5, "feature2": 1.2}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200, "Le code de retour n’est pas 200"
    json_data = response.json()
    assert "prediction" in json_data, "Clé 'prediction' absente de la réponse"
    assert isinstance(json_data["prediction"], (int, float)), "Le format de la prédiction est incorrect"

