import gradio as gr
import pandas as pd
import joblib

# Charger le modèle
model = joblib.load("xgboost_features90.joblib")

# Colonnes attendues (optionnel : tu peux sauvegarder ça avec ton modèle)
expected_cols = None
if hasattr(model, "get_booster"):
    expected_cols = model.get_booster().feature_names

# Fonction de prédiction
def predict_from_csv(file):
    try:
        df = pd.read_csv(file)  # plus robuste que file.name
    except Exception as e:
        return pd.DataFrame({"Erreur": [f"Impossible de lire le CSV ({e})"]})

    # Vérifier colonnes
    if expected_cols:
        missing = set(expected_cols) - set(df.columns)
        if missing:
            return pd.DataFrame({"Erreur": [f"Colonnes manquantes : {', '.join(missing)}"]})

    # Prédiction
    try:
        preds = model.predict(df)
    except Exception as e:
        return pd.DataFrame({"Erreur": [f"Erreur prédiction ({e})"]})

    df["prediction"] = preds
    df["prediction_label"] = df["prediction"].map({1: "Insolvable", 0: "Solvable"}).fillna("Inconnu")

    # Réorganiser pour affichage
    df = df.reset_index().rename(columns={"index": "ligne"})
    return df[["ligne", "prediction_label"]]

# DataFrame vide par défaut
empty_df = pd.DataFrame(columns=["ligne", "prediction_label"])

# Interface Gradio
interface = gr.Interface(
    fn=predict_from_csv,
    inputs=gr.File(label="Téléversez un fichier CSV", file_types=[".csv"]),
    outputs=gr.Dataframe(
        value=empty_df,
        headers=["ligne", "prediction_label"],
        label="Résultats de la prédiction",
        interactive=False
    ),
    title="Prédiction de la solvabilité des clients",
    description="Téléversez un fichier CSV avec les bonnes colonnes pour prédire la solvabilité des clients"
)

if __name__ == "__main__":
    interface.launch()
