from src.database import create_table, load_csv_to_db

# 1. Create the table
create_table()

# 2. Load CSV into database
csv_file_path = r"C:\Users\adith\OneDrive\Desktop\Programming in AI\public-health-data-insights-tool\data\raw\healthcare_dataset.csv"  # <- replace with your CSV file path
load_csv_to_db(csv_file_path)
