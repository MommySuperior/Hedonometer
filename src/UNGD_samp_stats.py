import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

UNGD_happiness = Path(__file__).parent.parent / "data" / "processed" / "UNGD_happiness.csv"

df = pd.read_csv(UNGD_happiness)
df = df[(df["year"] >= 2015) & (df["year"] <= 2025)]
print("Dataset head:") # this can go
print(df.head()) # this too
print("Dataset description:")
print(df.describe())

summary = df.groupby("year")["happiness_average"].agg(
    mean="mean",
    median="median",
    standard_deviation ="std",
    occurrence="count" # how many times this year occurs in column "year"
)

print("Range summary:")
print(summary)

# not sure if we're using the stuff below
yr_2015 = df[df["year"] == "2015"]["happiness_average"]
yr_2016 = df[df["year"] == "2016"]["happiness_average"]
yr_2017 = df[df["year"] == "2017"]["happiness_average"]
yr_2018 = df[df["year"] == "2018"]["happiness_average"]
yr_2019 = df[df["year"] == "2019"]["happiness_average"]
yr_2020 = df[df["year"] == "2020"]["happiness_average"]
yr_2021 = df[df["year"] == "2021"]["happiness_average"]
yr_2022 = df[df["year"] == "2022"]["happiness_average"]
yr_2023 = df[df["year"] == "2023"]["happiness_average"]
yr_2024 = df[df["year"] == "2024"]["happiness_average"]
yr_2025 = df[df["year"] == "2025"]["happiness_average"]


