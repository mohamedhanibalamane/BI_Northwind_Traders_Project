import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# =====================================================
# 1️⃣ Charger variables du .env
# =====================================================
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")       # .\SQLEXPRESS
DW_DB_NAME = os.getenv("DW_DB_NAME")     # Northwind_DW

# =====================================================
# 2️⃣ Connexion SQLAlchemy pour DW (Windows Auth)
# =====================================================
engine = create_engine(
    f"mssql+pyodbc://@{DB_SERVER}/{DW_DB_NAME}"
    "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
)

# =====================================================
# 3️⃣ Créer les schémas
# =====================================================
print("🏗 Création des schémas si inexistants...")

with engine.begin() as conn:
    conn.execute(text(
        "IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name='dw') "
        "EXEC('CREATE SCHEMA dw');"
    ))

print("✔ Schémas créés.")


# =====================================================
# 4️⃣ Charger les CSV nettoyés nécessaires
# =====================================================
print("📥 Lecture des fichiers nettoyés...")

customers = pd.read_csv("data/processed/Customers_clean.csv")
products = pd.read_csv("data/processed/Products_clean.csv")
employees = pd.read_csv("data/processed/Employees_clean.csv")
shippers = pd.read_csv("data/processed/Shippers_clean.csv")
orders = pd.read_csv("data/processed/Orders_clean.csv")
order_details = pd.read_csv("data/processed/OrderDetails_clean.csv")

print("✔ Données chargées.")


# =====================================================
# 5️⃣ Construire DimDate
# =====================================================
print("🗓 Construction DimDate...")

orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
date_df = pd.DataFrame({"Date": pd.date_range(orders["OrderDate"].min(),
                                              orders["OrderDate"].max())})

date_df["DateKey"] = date_df["Date"].dt.strftime("%Y%m%d").astype(int)
date_df["Year"] = date_df["Date"].dt.year
date_df["Month"] = date_df["Date"].dt.month
date_df["MonthName"] = date_df["Date"].dt.strftime("%B")
date_df["Quarter"] = date_df["Date"].dt.quarter


# =====================================================
# 6️⃣ Construire les Dimensions nécessaires
# =====================================================
print("📚 Construction des dimensions...")

DimCustomer = customers.rename(columns={
    "CustomerID": "CustomerKey",
    "CompanyName": "CustomerName",
    "Country": "CustomerCountry"
})[["CustomerKey", "CustomerName", "CustomerCountry"]]

DimProduct = products.rename(columns={
    "ProductID": "ProductKey",
    "ProductName": "ProductName"
})[["ProductKey", "ProductName"]]

DimEmployee = employees.rename(columns={
    "EmployeeID": "EmployeeKey",
    "LastName": "LastName",
    "FirstName": "FirstName",
    "Country": "EmployeeCountry"
})[["EmployeeKey", "LastName", "FirstName", "EmployeeCountry"]]

DimShipper = shippers.rename(columns={
    "ShipperID": "ShipperKey",
    "CompanyName": "ShipperName"
})[["ShipperKey", "ShipperName"]]


# =====================================================
# 7️⃣ Construire les tables de faits
# =====================================================
print("📊 Construction des faits...")

orders["DateKey"] = orders["OrderDate"].dt.strftime("%Y%m%d").astype(int)

FactOrders = orders.rename(columns={
    "OrderID": "OrderKey",
    "CustomerID": "CustomerKey",
    "EmployeeID": "EmployeeKey",
    "ShipVia": "ShipperKey"
})[["OrderKey", "CustomerKey", "EmployeeKey", "ShipperKey", "DateKey"]]

FactOrderDetails = order_details.rename(columns={
    "OrderID": "OrderKey",
    "ProductID": "ProductKey",
    "UnitPrice": "UnitPrice",
    "Quantity": "Quantity",
    "Discount": "Discount"
})[["OrderKey", "ProductKey", "UnitPrice", "Quantity", "Discount"]]


# =====================================================
# 8️⃣ Sauvegarder fichiers DW dans /data/dw/
# =====================================================
print("💾 Sauvegarde des fichiers DW...")

os.makedirs("data/dw", exist_ok=True)

tables_to_save = {
    "DimCustomer": DimCustomer,
    "DimProduct": DimProduct,
    "DimEmployee": DimEmployee,
    "DimShipper": DimShipper,
    "DimDate": date_df,
    "FactOrders": FactOrders,
    "FactOrderDetails": FactOrderDetails
}

for name, df in tables_to_save.items():
    df.to_csv(f"data/dw/{name}.csv", index=False)

print("📁 Fichiers DW sauvegardés.")


# =====================================================
# 9️⃣ Charger dans SQL Server (schéma dw)
# =====================================================
print("⬆ Chargement des tables dans SQL Server...")

with engine.begin() as conn:
    for name, df in tables_to_save.items():
        print(f"  → dw.{name}")
        df.to_sql(name, conn, schema="dw", if_exists="replace", index=False)

print("🎉 Data Warehouse construit et chargé avec succès !")
