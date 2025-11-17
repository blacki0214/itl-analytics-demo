import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
n = 500  # Number of vehicles to generate

records = []
for i in range(n):
    vehicle_id = f"T{i+1:03d}"
    mileage_km = random.randint(20000, 150000)
    engine_hours = random.randint(400, 3000)
    last_service_date = fake.date_between(start_date='-6M', end_date='today')
    breakdowns_last_6m = np.random.poisson(lam=1.2)
    depot = random.choice(["North", "South", "Central", "East", "West"])
    fuel_efficiency = round(random.uniform(5.0, 10.0), 1)
    
    records.append([
        vehicle_id, mileage_km, engine_hours, last_service_date,
        breakdowns_last_6m, fuel_efficiency, depot
    ])

df = pd.DataFrame(records, columns=[
    "vehicle_id", "mileage_km", "engine_hours", "last_service_date",
    "breakdowns_last_6m", "fuel_efficiency", "depot"
])

df.to_csv("./data/fleet_data_large.csv", index=False)
print("Generated", len(df), "records in ./data/fleet_data_large.csv")
