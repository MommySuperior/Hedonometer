import pandas as pd
import numpy as np
import pathlib as path

print_section = ("1.1")
path = "/Users/leosong/Documents/coding-humanities/Hedonometer/data/raw/Data_Set_S1.txt"

df = pd.read_csv(path, sep="\t", skiprows=3, dtype=str)

df = df.replace("--", np.nan)
df["word"] = df["word"].str.strip().str.lower()

num_cols = df.columns.difference(["word"])
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
df[num_cols] = df[num_cols].astype(float)

df["word"] = df["word"].astype("string")
print(df.head(10).to_csv(sep="\t", index=False))
    





