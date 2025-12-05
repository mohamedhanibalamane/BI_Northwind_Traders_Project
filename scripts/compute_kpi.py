# scripts/compute_kpi_full.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Créer les dossiers nécessaires
os.makedirs("figures", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 1️⃣ Charger les fichiers transformés (avec la casse exacte)
orders = pd.read_csv("data/processed/Orders_clean.csv", parse_dates=['OrderDate', 'ShippedDate'])
order_details = pd.read_csv("data/processed/OrderDetails_clean.csv")
customers = pd.read_csv("data/processed/Customers_clean.csv")
employees = pd.read_csv("data/processed/Employees_clean.csv")

# 2️⃣ Ajouter colonne "DeliveryStatus"
orders['DeliveryStatus'] = orders['ShippedDate'].apply(lambda x: 'Delivered' if pd.notnull(x) else 'Pending')

# 3️⃣ KPI par client
kpi_client = orders.groupby(['CustomerID', 'DeliveryStatus']).size().unstack(fill_value=0).reset_index()
kpi_client = kpi_client.merge(customers[['CustomerID','CompanyName','City','Country']], on='CustomerID', how='left')
kpi_client.to_csv("data/processed/kpi_client.csv", index=False)

# 4️⃣ KPI par employé
kpi_employee = orders.groupby(['EmployeeID','DeliveryStatus']).size().unstack(fill_value=0).reset_index()
kpi_employee = kpi_employee.merge(employees[['EmployeeID','FirstName','LastName','City','Country']], on='EmployeeID', how='left')
kpi_employee.to_csv("data/processed/kpi_employee.csv", index=False)

# 5️⃣ KPI par mois
orders['MonthYear'] = orders['OrderDate'].dt.to_period('M')
kpi_month = orders.groupby(['MonthYear','DeliveryStatus']).size().unstack(fill_value=0).reset_index()
kpi_month.to_csv("data/processed/kpi_month.csv", index=False)

print("✅ KPI CSV exportés dans data/processed/")

# 6️⃣ Graphiques pour dashboard
sns.set_style("whitegrid")

# --- Top 10 clients par commandes livrées ---
plt.figure(figsize=(12,6))
top_clients = kpi_client.sort_values('Delivered', ascending=False).head(10)
sns.barplot(x='CompanyName', y='Delivered', data=top_clients, color='green', label='Delivered')
sns.barplot(x='CompanyName', y='Pending', data=top_clients, color='red', label='Pending')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Nombre de commandes")
plt.title("Top 10 clients - Commandes livrées vs non livrées")
plt.legend()
plt.tight_layout()
plt.savefig("figures/kpi_client.png")
plt.close()

# --- Top 10 employés par commandes livrées ---
plt.figure(figsize=(12,6))
top_employees = kpi_employee.sort_values('Delivered', ascending=False).head(10)
sns.barplot(x='LastName', y='Delivered', data=top_employees, color='blue', label='Delivered')
sns.barplot(x='LastName', y='Pending', data=top_employees, color='orange', label='Pending')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Nombre de commandes")
plt.title("Top 10 employés - Commandes livrées vs non livrées")
plt.legend()
plt.tight_layout()
plt.savefig("figures/kpi_employee.png")
plt.close()

# --- Évolution commandes par mois ---
plt.figure(figsize=(12,6))
kpi_month_sorted = kpi_month.sort_values('MonthYear')
plt.plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Delivered'], marker='o', color='green', label='Delivered')
plt.plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Pending'], marker='o', color='red', label='Pending')
plt.xticks(rotation=45)
plt.ylabel("Nombre de commandes")
plt.title("Évolution des commandes par mois")
plt.legend()
plt.tight_layout()
plt.savefig("figures/kpi_month.png")
plt.close()

print("✅ Graphiques générés dans figures/")
