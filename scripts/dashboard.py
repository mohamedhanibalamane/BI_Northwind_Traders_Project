# scripts/dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Créer le dossier figures si n'existe pas
os.makedirs("figures", exist_ok=True)

# ------------------------------
# Charger les KPI générés à l'étape D
# ------------------------------
data_path = "data/processed/"

kpi_client = pd.read_csv(os.path.join(data_path, "kpi_client.csv"))
kpi_employee = pd.read_csv(os.path.join(data_path, "kpi_employee.csv"))
kpi_month = pd.read_csv(os.path.join(data_path, "kpi_month.csv"))

# ------------------------------
# Configuration style
# ------------------------------
sns.set_style("whitegrid")
plt.rcParams.update({'figure.autolayout': True})

# ------------------------------
# Création du dashboard complet
# ------------------------------
fig, axes = plt.subplots(3, 1, figsize=(14, 18))

# --- Graphique 1 : Top 10 clients par commandes livrées ---
top_clients = kpi_client.sort_values('Delivered', ascending=False).head(10)
sns.barplot(
    x='CompanyName', y='Delivered', data=top_clients, color='green', ax=axes[0], label='Livrées'
)
sns.barplot(
    x='CompanyName', y='Pending', data=top_clients, color='red', ax=axes[0], label='Non livrées'
)
axes[0].set_title("Top 10 clients - Commandes livrées vs non livrées", fontsize=14)
axes[0].set_ylabel("Nombre de commandes")
axes[0].tick_params(axis='x', rotation=45)
axes[0].legend()

# --- Graphique 2 : Top 10 employés par commandes livrées ---
top_employees = kpi_employee.sort_values('Delivered', ascending=False).head(10)
sns.barplot(
    x='LastName', y='Delivered', data=top_employees, color='blue', ax=axes[1], label='Livrées'
)
sns.barplot(
    x='LastName', y='Pending', data=top_employees, color='orange', ax=axes[1], label='Non livrées'
)
axes[1].set_title("Top 10 employés - Commandes livrées vs non livrées", fontsize=14)
axes[1].set_ylabel("Nombre de commandes")
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend()

# --- Graphique 3 : Évolution des commandes par mois ---
kpi_month_sorted = kpi_month.sort_values('MonthYear')
axes[2].plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Delivered'], 
             marker='o', color='green', label='Livrées')
axes[2].plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Pending'], 
             marker='o', color='red', label='Non livrées')
axes[2].set_title("Évolution des commandes par mois", fontsize=14)
axes[2].set_ylabel("Nombre de commandes")
axes[2].tick_params(axis='x', rotation=45)
axes[2].legend()

# ------------------------------
# Sauvegarde du dashboard complet
# ------------------------------
dashboard_path = os.path.join("figures", "dashboard.png")
plt.tight_layout()
plt.savefig(dashboard_path, dpi=300)
plt.close()

print(f"✅ Dashboard généré et sauvegardé dans {dashboard_path}")
