# scripts/extract_access_no_odbc.py

import os
import pandas as pd
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

ACCESS_FILE = os.getenv("ACCESS_FILE")
ACCESS_DIR = "data/raw/access/"
os.makedirs(ACCESS_DIR, exist_ok=True)

# Transformer le chemin relatif en absolu
access_path = os.path.abspath(ACCESS_FILE)
if not os.path.exists(access_path):
    print(f"❌ Fichier Access introuvable : {access_path}")
    exit(1)

# Liste des tables à extraire
tables_access = ["Customers", "Orders", "Order Details", "Employees", "Shippers", "Products"]

# Extraction
for table in tables_access:
    try:
        # Lire la table directement depuis Access
        df = pd.read_access(access_path, table_name=table)
        df.to_csv(os.path.join(ACCESS_DIR, f"{table}.csv"), index=False, encoding='utf-8')
        print(f"✅ {table} exporté Access → {ACCESS_DIR}{table}.csv")
    except Exception as e:
        print(f"❌ Erreur lors de l'export de {table}: {e}")

print("Extraction terminée.")
