import pandas as pd
import os

def load_data():
    # Arrange : on définit le chemin de test
    filepath = "fichier_tests_clients/fichier_test.csv"

    # Act : on charge les données
    df = pd.read_csv(filepath)

    # Assert : on vérifie quelques conditions
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "Le fichier CSV est vide"
    assert "TARGET" in df.columns, "La colonne cible 'TARGET' est absente"
