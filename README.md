# BI_Northwind_Traders_Project

Introduction
L'objectif de ce projet est de concevoir une solution BI complète à partir des données Northwind issues de SQL Server et Microsoft Access. Le projet couvre l'ensemble du pipeline décisionnel :
• Extraction et nettoyage des données
• Transformation avancée via Python
• Construction d'un Data Warehouse en étoile
• Calcul d'indicateurs KPI
• Production d'un dashboard analytique (PNG + HTML)
• Documentation complète et vidéo explicative
Objectifs et périmètre
Objectifs principaux
• Construire un Data Warehouse cohérent basé sur Northwind
• Réaliser un ETL Python complet
• Générer des indicateurs métier (KPI)
• Produire un dashboard professionnel regroupant toutes les statistiques
• Livrer un projet entièrement reproductible
Périmètre des livrables
• build_dw.py, compute_kpi_final-Bl.py
• analysis-final-Bl.ipynb
• Dossiers /data, /scripts, /figures, /reports
• Dashboard : PNG + HTML
• Rapport PDF + vidéo explicative
• README pour exécution
Architecture générale
Le projet suit une architecture BI standard : RAW → PROCESSED → DATA WAREHOUSE → KPI → FIGURES → ANALYTICS
Processus ETL
Extraction
• Récupération des données Access (Northwind2012.accdb)
• Export des tables en CSV dans data/raw/access/
• Import de tables SQL Server exportées dans data/raw/sqlserver/
Transformation
• Nettoyage des colonnes et harmonisation des types
• Conversion des dates et génération des clés (DateKey YYYYMMDD)
• Fusion des tables pour préparer les KPI
• Calcul du chiffre d’affaires : Revenue = UnitPrice × Quantity × (1 - Discount)
Chargement
• Création des dimensions & faits dans data/dw/
• Chargement automatique dans SQL Server via sqlalchemy + pyodbc
Data Warehouse
Dimensions
• DimCustomer : CustomerKey, CustomerName, Country
• DimProduct : ProductKey, ProductName
• DimEmployee : EmployeeKey, FirstName, LastName, Country
• DimShipper : ShipperKey, ShipperName
• DimDate : DateKey, Date, Year, Month, MonthName, Quarter
Tables de faits
• FactOrders : OrderKey, CustomerKey, EmployeeKey, ShipperKey, DateKey
• FactOrderDetails : ProductKey, OrderKey, UnitPrice, Quantity, Discount
Scripts Python & Notebook
• build_dw.py : construit les dimensions et faits, sauvegarde en CSV et charge dans SQL Server
• compute_kpi_final-Bl.py : fusionne DW, calcule les KPI, génère les images PNG et le dashboard complet
• analysis-final-Bl.ipynb : visualisation interactive des KPI, export HTML
KPI & Dashboard
Les visualisations générées : Ventes par mois, Ventes par pays, Top 10 produits, Top 10 clients, Top 10 employés, Évolution des commandes, Chiffre d'affaires par mois, Panier total par commande, Répartition des ventes (Pie Chart), Dashboard HTML complet.
Exécution et reproduction
Installation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Étapes d'exécution
python scripts/build_dw.py
python scripts/compute_kpi_final-Bl.py
jupyter lab
Le dashboard HTML est dans : figures/dashboard_total_final-Bl.html
Justification des choix techniques
• Python : simplicité et richesse des bibliothèques
• Pandas : manipulation performante des données
• Matplotlib / Seaborn : graphiques professionnels
• SQLAlchemy + pyodbc : intégration fiable avec SQL Server
• Jupyter Notebook : idéal pour analyses et présentation
• Schéma en étoile : modèle BI classique, simple et efficace
Qualité des données & tests
• Vérification des clés
• Conversion des dates
• Comparaison des totaux avant/après transformation
• Contrôle des colonnes attendues
• Détection des valeurs nulles
• Logs d'erreurs lors du chargement SQL Server
Conclusion
Le projet FINAL-BI Northwind aboutit à une solution BI complète, fonctionnelle et entièrement automatisée. Les données brutes (Access + SQL Server) sont transformées en Data Warehouse fiable, analysées pour produire des KPI pertinents et un dashboard professionnel en HTML & PNG. Solution réplicable, documentée et évolutive : Power BI, Streamlit, automatisation Airflow, SCD2… Pipeline maîtrisé : ETL → DW → KPI → Dashboard

