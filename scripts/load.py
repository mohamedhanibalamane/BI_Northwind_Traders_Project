# scripts/load.py

import os
import pandas as pd

PROCESSED_DIR = "data/processed/"

tables_clean = ["Customers_clean.csv", "Orders_clean.csv", "OrderDetails_clean.csv", "Employees_clean.csv", "kpi_dataset.csv"]

for file in tables_clean:
    path = os.path.join(PROCESSED_DIR, file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Vérification minimale
        print(f"{file} : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        # Sauvegarde finale
        df.to_csv(path, index=False, encoding='utf-8')
        print(f"✅ {file} chargé dans {PROCESSED_DIR}")
    else:
        print(f"⚠️ Fichier manquant : {file}")

print("✅ Load terminé.")
