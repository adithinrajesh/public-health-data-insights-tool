from src.database import create_table, load_csv_to_db
import os

# 1. Create the table
create_table()

# 2. Load CSV into database
csv_file_path = os.path.join(
    os.path.dirname(__file__), 
    "data", "raw", "healthcare_dataset.csv"
)
load_csv_to_db(csv_file_path)
