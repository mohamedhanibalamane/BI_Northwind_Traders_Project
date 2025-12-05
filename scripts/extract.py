# scripts/extract.py

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import argparse
import urllib
import pyodbc  # Utilisation ODBC pour Access

# Charger les variables d'environnement
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
ACCESS_FILE = os.getenv("ACCESS_FILE")

# Dossiers de sortie
SQL_DIR = "data/raw/sqlserver/"
ACCESS_DIR = "data/raw/access/"

os.makedirs(SQL_DIR, exist_ok=True)
os.makedirs(ACCESS_DIR, exist_ok=True)

# Parser arguments
parser = argparse.ArgumentParser(description="Extraire les données depuis SQL Server ou Access")
parser.add_argument("--source", choices=["sqlserver", "access", "all"], default="all",
                    help="Choisir la source : sqlserver, access ou all")
args = parser.parse_args()

# Tables
tables_sqlserver = ["Customers", "Orders", "[Order Details]", "Employees", "Shippers", "Products"]
tables_access = ["Customers", "Orders", "Order Details", "Employees", "Shippers", "Products"]

# --- Extraction SQL Server ---
if args.source in ["sqlserver", "all"]:
    print("Extraction depuis SQL Server...")
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    for table in tables_sqlserver:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", engine)
            filename = table.replace("[", "").replace("]", "")
            df.to_csv(os.path.join(SQL_DIR, f"{filename}.csv"), index=False, encoding='utf-8')
            print(f"✅ {filename} exporté SQL Server → {SQL_DIR}{filename}.csv")
        except Exception as e:
            print(f"❌ Erreur lors de l'export de {table}: {e}")

# --- Extraction Access via ODBC ---
if args.source in ["access", "all"]:
    print("Extraction depuis Access (via ODBC)...")

    access_path = os.path.abspath(ACCESS_FILE)
    if not os.path.exists(access_path):
        print(f"❌ Fichier Access introuvable : {access_path}")
        exit(1)

    # Connexion ODBC
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={access_path};"
    )
    conn = pyodbc.connect(conn_str)

    for table in tables_access:
        try:
            df = pd.read_sql(f"SELECT * FROM [{table}]", conn)
            df.to_csv(os.path.join(ACCESS_DIR, f"{table}.csv"), index=False, encoding='utf-8')
            print(f"✅ {table} exporté Access → {ACCESS_DIR}{table}.csv")
        except Exception as e:
            print(f"❌ Erreur lors de l'export de {table}: {e}")

    conn.close()

print("Extraction terminée.")
