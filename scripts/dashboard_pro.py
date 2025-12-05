# scripts/dashboard_pro.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Créer le dossier figures si n'existe pas
os.makedirs("figures", exist_ok=True)

# ------------------------------
# Charger les KPI
# ------------------------------
data_path = "data/processed/"

kpi_client = pd.read_csv(os.path.join(data_path, "kpi_client.csv"))
kpi_employee = pd.read_csv(os.path.join(data_path, "kpi_employee.csv"))
kpi_month = pd.read_csv(os.path.join(data_path, "kpi_month.csv"))

# ------------------------------
# Style et configuration globale
# ------------------------------
sns.set_style("whitegrid")
plt.rcParams.update({'figure.autolayout': True})

# ------------------------------
# Création de la figure globale
# ------------------------------
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle("Dashboard BI - Northwind Traders", fontsize=20, fontweight='bold')

# ------------------------------
# 1️⃣ Top 10 clients - commandes livrées vs non livrées
# ------------------------------
top_clients = kpi_client.sort_values('Delivered', ascending=False).head(10)
sns.barplot(
    x='CompanyName', y='Delivered', data=top_clients, color='green', ax=axes[0,0], label='Livrées'
)
sns.barplot(
    x='CompanyName', y='Pending', data=top_clients, color='red', ax=axes[0,0], label='Non livrées'
)
axes[0,0].set_title("Top 10 clients", fontsize=14, fontweight='bold')
axes[0,0].set_ylabel("Nombre de commandes")
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].legend()

# ------------------------------
# 2️⃣ Top 10 employés - commandes livrées vs non livrées
# ------------------------------
top_employees = kpi_employee.sort_values('Delivered', ascending=False).head(10)
sns.barplot(
    x='LastName', y='Delivered', data=top_employees, color='blue', ax=axes[0,1], label='Livrées'
)
sns.barplot(
    x='LastName', y='Pending', data=top_employees, color='orange', ax=axes[0,1], label='Non livrées'
)
axes[0,1].set_title("Top 10 employés", fontsize=14, fontweight='bold')
axes[0,1].set_ylabel("Nombre de commandes")
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].legend()

# ------------------------------
# 3️⃣ Évolution des commandes par mois
# ------------------------------
kpi_month_sorted = kpi_month.sort_values('MonthYear')
axes[1,0].plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Delivered'], 
               marker='o', color='green', label='Livrées')
axes[1,0].plot(kpi_month_sorted['MonthYear'].astype(str), kpi_month_sorted['Pending'], 
               marker='o', color='red', label='Non livrées')
axes[1,0].set_title("Évolution des commandes par mois", fontsize=14, fontweight='bold')
axes[1,0].set_ylabel("Nombre de commandes")
axes[1,0].tick_params(axis='x', rotation=45)
axes[1,0].legend()

# ------------------------------
# 4️⃣ KPI récapitulatifs
# ------------------------------
# Calculer quelques indicateurs clés
total_orders = kpi_client['Delivered'].sum() + kpi_client['Pending'].sum()
total_delivered = kpi_client['Delivered'].sum()
total_pending = kpi_client['Pending'].sum()
top_client_name = top_clients.iloc[0]['CompanyName']
top_employee_name = top_employees.iloc[0]['FirstName'] + " " + top_employees.iloc[0]['LastName']

axes[1,1].axis('off')  # pas d'axes pour ce panneau

# Ajouter un tableau ou texte résumé
summary_text = f"""
🔹 Total commandes : {total_orders}
🔹 Commandes livrées : {total_delivered}
🔹 Commandes non livrées : {total_pending}

🔹 Meilleur client : {top_client_name}
🔹 Meilleur employé : {top_employee_name}
"""
axes[1,1].text(0.1, 0.5, summary_text, fontsize=14, fontweight='bold', va='center')

# ------------------------------
# Sauvegarde du dashboard
# ------------------------------
dashboard_path = os.path.join("figures", "dashboard_pro.png")
plt.tight_layout(rect=[0, 0, 1, 0.96])  # pour laisser de la place au titre global
plt.savefig(dashboard_path, dpi=300)
plt.close()

print(f"✅ Dashboard professionnel généré et sauvegardé dans {dashboard_path}")
