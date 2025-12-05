import pyodbc
import os

# Chemin complet vers ton fichier Access
access_file = r"C:\Users\WELTINFO\Desktop\BI_Northwind_Traders_Project\data\raw\Northwind2012.accdb"

# Chaîne de connexion ODBC pour Access
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    f"DBQ={access_file};"
)

# Connexion
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Lister toutes les tables de la base
for row in cursor.tables():
    print(row.table_name)

conn.close()
