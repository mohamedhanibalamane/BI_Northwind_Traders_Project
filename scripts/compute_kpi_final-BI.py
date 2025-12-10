# scripts/compute_kpi_final-BI.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Création du dossier figures
# ------------------------------
figures_path = "figures"
os.makedirs(figures_path, exist_ok=True)

# ------------------------------
# Chargement des fichiers du Data Warehouse
# ------------------------------
customers = pd.read_csv("data/dw/DimCustomer.csv")
products = pd.read_csv("data/dw/DimProduct.csv")
employees = pd.read_csv("data/dw/DimEmployee.csv")
orders = pd.read_csv("data/dw/FactOrders.csv")
order_details = pd.read_csv("data/dw/FactOrderDetails.csv")
date_df = pd.read_csv("data/dw/DimDate.csv")

# ------------------------------
# Merge principal
# ------------------------------
df = (
    order_details
    .merge(orders, on="OrderKey")
    .merge(customers, on="CustomerKey")
    .merge(employees, on="EmployeeKey")
    .merge(products, on="ProductKey")
    .merge(date_df, on="DateKey")
)

print("Colonnes disponibles :", df.columns.tolist())

sns.set_style("whitegrid")
plt.rcParams.update({'figure.autolayout': True})


# ==========================================================
# 🆕 CALCUL DU CHIFFRE D'AFFAIRES
# ==========================================================
df["Revenue"] = df["UnitPrice"] * df["Quantity"] * (1 - df["Discount"])

# ==========================================================
# 1️⃣ VENTES PAR MOIS
# ==========================================================
sales_month = df.groupby("Month")["Quantity"].sum().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(data=sales_month, x="Month", y="Quantity",
            palette="Blues_d", edgecolor="black")
plt.title("Ventes par mois", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "sales_per_month_final-BI.png"))
plt.close()


# ==========================================================
# 2️⃣ VENTES PAR PAYS
# ==========================================================
sales_country = df.groupby("CustomerCountry")["Quantity"].sum() \
    .reset_index().sort_values("Quantity", ascending=False)

plt.figure(figsize=(12,6))
sns.barplot(data=sales_country, x="CustomerCountry", y="Quantity",
            palette="Greens_d", edgecolor="black")
plt.xticks(rotation=45)
plt.title("Ventes par pays", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "sales_per_country_final-BI.png"))
plt.close()


# ==========================================================
# 3️⃣ TOP PRODUITS (horizontal)
# ==========================================================
top_products = df.groupby("ProductName")["Quantity"].sum() \
    .reset_index().sort_values("Quantity", ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(data=top_products, y="ProductName", x="Quantity",
            palette="Oranges_d", edgecolor="black")
plt.title("Top 10 produits", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "top_products_final-BI.png"))
plt.close()


# ==========================================================
# 4️⃣ TOP CLIENTS
# ==========================================================
top_clients = df.groupby("CustomerName")["Quantity"].sum() \
    .reset_index().sort_values("Quantity", ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(data=top_clients, y="CustomerName", x="Quantity",
            palette="Purples_d", edgecolor="black")
plt.title("Top 10 clients", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "top_clients_final-BI.png"))
plt.close()


# ==========================================================
# 5️⃣ TOP EMPLOYÉS
# ==========================================================
top_employees = df.groupby(["FirstName", "LastName"])["Quantity"].sum().reset_index()
top_employees["EmployeeName"] = top_employees["FirstName"] + " " + top_employees["LastName"]
top_employees = top_employees.sort_values("Quantity", ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(data=top_employees, y="EmployeeName", x="Quantity",
            palette="coolwarm", edgecolor="black")
plt.title("Top 10 employés", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "top_employees_final-BI.png"))
plt.close()


# ==========================================================
# 6️⃣ ÉVOLUTION DES COMMANDES
# ==========================================================
monthly_orders = df.groupby("Month")["OrderKey"].nunique().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=monthly_orders, x="Month", y="OrderKey",
             marker="o", linewidth=3)
plt.grid(True, linestyle="--", alpha=0.5)
plt.title("Évolution des commandes", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "orders_evolution_final-BI.png"))
plt.close()


# ==========================================================
# 🆕 7️⃣ CHIFFRE D'AFFAIRES PAR MOIS
# ==========================================================
revenue_month = df.groupby("Month")["Revenue"].sum().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(data=revenue_month, x="Month", y="Revenue",
            palette="Reds_d", edgecolor="black")
plt.title("Chiffre d'affaires par mois", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "revenue_per_month_final-BI.png"))
plt.close()


# ==========================================================
# 🆕 8️⃣ PANIER MOYEN
# ==========================================================
basket = df.groupby("OrderKey")["Revenue"].sum()
average_basket = basket.mean()

plt.figure(figsize=(10,6))
sns.lineplot(x=basket.index, y=basket.values, marker="o")
plt.title("Panier total par commande", fontsize=16, fontweight="bold")
plt.xlabel("Commande")
plt.ylabel("Montant (€)")
plt.savefig(os.path.join(figures_path, "average_basket_final-BI.png"))
plt.close()


# ==========================================================
# 9️⃣ PIE CHART – Répartition ventes / pays
# ==========================================================
plt.figure(figsize=(9,9))
plt.pie(
    sales_country["Quantity"],
    labels=sales_country["CustomerCountry"],
    autopct="%1.1f%%",
    startangle=140,
    colors=sns.color_palette("Spectral", len(sales_country))
)
plt.title("Répartition des ventes par pays", fontsize=16, fontweight="bold")
plt.savefig(os.path.join(figures_path, "sales_country_pie_final-BI.png"))
plt.close()


# ==========================================================
# 🔟 DASHBOARD COMPLET
# ==========================================================
fig, axes = plt.subplots(4, 3, figsize=(28,25))
fig.suptitle("Dashboard Northwind – Version FINAL BI", fontsize=22, fontweight="bold")

sns.barplot(data=sales_month, x="Month", y="Quantity",
            palette="Blues_d", ax=axes[0,0])
axes[0,0].set_title("Ventes par mois")

sns.barplot(data=sales_country, x="CustomerCountry", y="Quantity",
            palette="Greens_d", ax=axes[0,1])
axes[0,1].set_title("Ventes par pays")
axes[0,1].tick_params(rotation=45)

sns.barplot(data=top_products, y="ProductName", x="Quantity",
            palette="Oranges_d", ax=axes[0,2])
axes[0,2].set_title("Top produits")

sns.barplot(data=top_clients, y="CustomerName", x="Quantity",
            palette="Purples_d", ax=axes[1,0])
axes[1,0].set_title("Top clients")

sns.barplot(data=top_employees, y="EmployeeName", x="Quantity",
            palette="coolwarm", ax=axes[1,1])
axes[1,1].set_title("Top employés")

sns.lineplot(data=monthly_orders, x="Month", y="OrderKey",
             marker="o", linewidth=3, ax=axes[1,2])
axes[1,2].set_title("Évolution des commandes")

sns.barplot(data=revenue_month, x="Month", y="Revenue",
            palette="Reds_d", ax=axes[2,0])
axes[2,0].set_title("Chiffre d'affaires")

sns.lineplot(x=basket.index, y=basket.values, marker="o", ax=axes[2,1])
axes[2,1].set_title("Panier total par commande")

axes[2,2].pie(
    sales_country["Quantity"],
    labels=sales_country["CustomerCountry"],
    autopct="%1.1f%%",
    colors=sns.color_palette("Spectral", len(sales_country))
)
axes[2,2].set_title("Ventes par pays (Pie)")

axes[3,0].axis("off")
axes[3,1].axis("off")
axes[3,2].axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(figures_path, "dashboard_complet_final-BI.png"), dpi=300)
plt.close()

print("✅ Statistiques FINAL-BI générées dans le dossier 'figures'")
