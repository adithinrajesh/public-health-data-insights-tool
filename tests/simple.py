import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("db", "health_data.db")
DB_PATH = os.path.abspath(DB_PATH)

conn = sqlite3.connect(DB_PATH)

# See all records
df = pd.read_sql_query("SELECT * FROM patients LIMIT 10", conn)
print(df)

# Summary info
print(df.info())
print(df.describe())

conn.close()