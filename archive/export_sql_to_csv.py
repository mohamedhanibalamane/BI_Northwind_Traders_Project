import pandas as pd
import pyodbc
import os

output_folder = "./data/raw/sqlserver/"
os.makedirs(output_folder, exist_ok=True)

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=Northwind;"
    "Trusted_Connection=yes;"
)

tables = [
    "Categories",
    "CustomerCustomerDemo",
    "CustomerDemographics",
    "Customers",
    "Employees",
    "EmployeeTerritories",
    "[Order Details]",
    "Orders",
    "Products",
    "Region",
    "Shippers",
    "Suppliers",
    "Territories"
]

for table in tables:
    print(f"Exporting {table}...")
    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    clean_name = (
        table.replace("[", "")
             .replace("]", "")
             .replace(" ", "")
    )

    df.to_csv(
        f"{output_folder}{clean_name}.csv",
        index=False,
        encoding="utf-8"
    )

print("\n✔✔✔ Export terminé avec succès !")
