import pandas_access as mdb
from dotenv import load_dotenv
import os

load_dotenv()

access_path = os.path.abspath(os.getenv("ACCESS_FILE"))

tables = mdb.list_tables(access_path)
print("Tables dans Access :", tables)
