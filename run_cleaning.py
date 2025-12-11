from src.cleaning import load_data_from_db, clean_data, save_cleaned_data

df = load_data_from_db()
df_clean = clean_data(df)
save_cleaned_data(df_clean)