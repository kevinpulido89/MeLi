"""Dummy file to test the GHA."""

import pandas as pd

print("Running train.py...")
df = pd.read_csv("data.csv")

print(df.head())
