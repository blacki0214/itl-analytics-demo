import pandas as pd
import os

def test_data_columns():
    assert os.path.exists("data/fleet_data_large.csv"), "CSV file missing"
    df = pd.read_csv("data/fleet_data_large.csv")
    expected = {"vehicle_id", "mileage_km", "engine_hours", "last_service_date"}
    assert expected.issubset(df.columns), "Missing required columns"
