# BI_Northwind_Traders_Project

Description du projet
--------------------
Ce projet a pour objectif de concevoir une solution BI complète basée sur la base de données Northwind (SQL Server + Access). 
Il inclut un ETL Python pour l’intégration et la transformation des données, ainsi qu’un dashboard analytique présentant les indicateurs clés (KPI). 
Le projet est réalisé en mode individuel et suit une architecture Python + CSV + visualisation.

Structure du projet
------------------
BI_Northwind_Traders_Project/
├── data/
│   ├── raw/          ← Données brutes (Access, SQL Server exports)
│   └── processed/    ← Données transformées et KPI
├── scripts/
│   ├── extract.py    ← Extraction SQL Server / Access
│   ├── transform.py  ← Transformation et nettoyage
│   ├── load.py       ← Chargement des données transformées
│   └── dashboard_pro.py ← Génération du dashboard professionnel
├── notebooks/
│   └── analysis.ipynb  ← Analyse et visualisation
├── figures/
│   └── dashboard.png      ← Dashboard exporté
│   └── dashboard_pro_inline.png ← Dashboard pro inline
├── reports/
│   └── rapport_final.pdf
│   └── data_quality_report.md
├── video/
│   └── presentation.mp4
└── README.md

Dépendances Python
------------------
- pandas  
- numpy  
- matplotlib  
- seaborn  
- sqlalchemy  
- pyodbc  
- python-dotenv  

Installation rapide :
pip install pandas numpy matplotlib seaborn sqlalchemy pyodbc python-dotenv

Installation
------------
1. Cloner le dépôt Git :
   git clone <URL_DU_DEPOT>
   cd BI_Northwind_Traders_Project
2. Vérifier que Python 3.10+ est installé.
3. Placer les fichiers sources Northwind : 
   data/raw/Northwind.accdb
4. Créer le fichier `.env` à la racine :
   DB_SERVER=.\SQLEXPRESS
   DB_NAME=Northwind
   DB_USER=
   DB_PASS=
   ACCESS_FILE=./data/raw/Northwind.accdb

Exécution de l’ETL
------------------
1. Extraction :
   python scripts/extract.py --source sqlserver
   python scripts/extract.py --source access
2. Transformation :
   python scripts/transform.py
3. Chargement :
   python scripts/load.py
4. Génération du dashboard :
   python scripts/dashboard_pro.py

Lancer le notebook d’analyse
----------------------------
jupyter notebook notebooks/analysis.ipynb

Résultats
---------
- KPI CSV : data/processed/kpi_client.csv, kpi_employee.csv, kpi_month.csv
- Graphiques : figures/*.png
- Dashboard : figures/dashboard_pro.png et dashboard_pro_inline.png
- Rapport PDF : reports/rapport_final.pdf
- Vidéo présentation : video/presentation.mp4

Commandes exemples
------------------
python scripts/extract.py --source sqlserver
python scripts/extract.py --source access
python scripts/transform.py
python scripts/load.py
python scripts/dashboard_pro.py
