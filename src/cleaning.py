import pandas as pd
import numpy as np
from pathlib import Path

coding_humanities = Path(__file__).resolve().parent
ROOT = coding_humanities.parent

print_section = ("1.1")
dataset_path = ROOT / "data" / "raw" / "Data_Set_S1.txt"

df = pd.read_csv(dataset_path, sep="\t", skiprows=3, dtype=str)

df = df.replace("--", np.nan)
df["word"] = df["word"].str.strip().str.lower()

num_cols = df.columns.difference(["word"])
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
df[num_cols] = df[num_cols].astype(float)

df["word"] = df["word"].astype("string")
print(df.head(10).to_csv(sep="\t", index=False))

print("1.2 Data dictionary")

col_dtypes = df.dtypes.astype(str).reset_index()
col_dtypes.columns = ["column", "dtype"]

missing = df.isna().sum().reset_index()
missing.columns = ["column", "n_missing"]


data_dictionary = col_dtypes.merge(missing, on="column")

print(data_dictionary.to_string(index=False))
data_dictionary.to_csv("data/processed/data_dictionary.csv", index=False)
    
print("\n1.3 Sanity checks")

print("Duplicated words:", df["word"].duplicated().sum())

sample_15 = df.sample(15, random_state=42)
print("\nRandom sample (15 rows):")
print(sample_15)
sample_15.to_csv("data/processed/random_sample_15_rows.csv", index=False)

show_cols = ["word", "happiness_average", "happiness_standard_deviation"]


sorted_df = df.sort_values("happiness_average")
top_10_positive = sorted_df.tail(10)[show_cols]
top_10_negative = sorted_df.head(10)[show_cols]

print("\nTop 10 positive words:")
print(top_10_positive)

print("\nTop 10 negative words:")
print(top_10_negative)

top_10_positive.to_csv("data/processed/top_10_positive_words.csv", index=False)
top_10_negative.to_csv("data/processed/top_10_negative_words.csv", index=False)






