# scripts/transform.py

import pandas as pd
import os
from datetime import datetime

RAW_SQL_DIR = "data/raw/sqlserver/"
RAW_ACCESS_DIR = "data/raw/access/"
PROCESSED_DIR = "data/processed/"
REPORT_DIR = "reports/"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

tables = ["Customers", "Orders", "OrderDetails", "Employees", "Shippers", "Products"]

def clean_dates(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def transform_table(df, table_name):
    if table_name == "OrderDetails":
        df['UnitPrice'] = df['UnitPrice'].astype(float)
    if table_name == "Orders":
        df = clean_dates(df, ['OrderDate', 'RequiredDate', 'ShippedDate'])
    if table_name == "Employees":
        df = clean_dates(df, ['BirthDate', 'HireDate'])
    return df

# --- Charger CSV bruts et transformer ---
sql_dfs = {}
access_dfs = {}

for table in tables:
    sql_path = os.path.join(RAW_SQL_DIR, f"{table}.csv")
    access_path = os.path.join(RAW_ACCESS_DIR, f"{table}.csv")
    
    if os.path.exists(sql_path):
        sql_dfs[table] = transform_table(pd.read_csv(sql_path), table)
    
    if os.path.exists(access_path):
        access_dfs[table] = transform_table(pd.read_csv(access_path), table)

# --- Enregistrer les données nettoyées ---
for table, df in sql_dfs.items():
    df.to_csv(os.path.join(PROCESSED_DIR, f"{table}_clean.csv"), index=False, encoding='utf-8')

# --- Créer table KPI-ready ---
orders = sql_dfs["Orders"]
order_details = sql_dfs["OrderDetails"]
customers = sql_dfs["Customers"]
employees = sql_dfs["Employees"]

# Commandes livrées
orders['Delivered'] = orders['ShippedDate'].notna()

# KPI dataset
kpi_df = orders.merge(customers[['CustomerID','CompanyName','City','Country']], on='CustomerID', how='left')
kpi_df = kpi_df.merge(employees[['EmployeeID','FirstName','LastName']], on='EmployeeID', how='left')

kpi_df.to_csv(os.path.join(PROCESSED_DIR, "kpi_dataset.csv"), index=False, encoding='utf-8')
print("✅ Transformation terminée, fichiers nettoyés enregistrés dans data/processed/")

# --- Comparaison SQL vs Access ---
report_lines = []
for table in tables:
    sql_count = len(sql_dfs[table])
    access_count = len(access_dfs[table]) if table in access_dfs else "N/A"
    report_lines.append(f"{table}: SQL={sql_count}, Access={access_count}")

with open(os.path.join(REPORT_DIR, "data_quality_report.md"), "w") as f:
    f.write("# Data Quality Report\n\n")
    f.write("Comparaison SQL Server vs Access\n\n")
    for line in report_lines:
        f.write(f"- {line}\n")

print("✅ Data Quality Report généré : reports/data_quality_report.md")
