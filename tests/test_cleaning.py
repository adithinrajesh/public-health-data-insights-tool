import pytest
import pandas as pd
from src.cleaning import clean_data

def test_clean_data_basic():
    # Sample dirty data
    data = {
        "Name": [" alice ", "BOB"],
        "Age": ["30", None],
        "Gender": ["male", "FEMALE"],
        "BillingAmount": ["100.5", "abc"]
    }
    df = pd.DataFrame(data)
    df_clean = clean_data(df)

    # Assertions
    assert df_clean["Name"].iloc[0] == "Alice"
    assert df_clean["Name"].iloc[1] == "Bob"
    assert df_clean["Age"].iloc[1] == 0  # missing age filled
    assert df_clean["Gender"].iloc[0] == "Male"
    assert df_clean["BillingAmount"].iloc[1] == 0.0
