import pandas as pd
import numpy as np
import pathlib as path

print_section = ("1.1")
path = "Hedonometer/data/raw/Data_Set_S1.txt"

df = pd.read_csv(path, sep="\t", skiprows=3, dtype=str)

df = df.replace("--", np.nan)
df["word"] = df["word"].str.strip().str.lower()

num_cols = df.columns.difference(["word"])
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
df[num_cols] = df[num_cols].astype(float)

df["word"] = df["word"].astype("string")
# print(df.head(10).to_csv(sep="\t", index=False))
    
print("1.3 Sanity checks")

print("Duplicated words:", df["word"].duplicated().sum())

sample_15 = df.sample(15, random_state=42)
print("\nRandom sample (15 rows):")
print(sample_15)
# sample_15.to_csv("random_sample_15_rows.csv", index=False)

show_cols = ["word", "happiness_average", "happiness_standard_deviation"]


sorted_df = df.sort_values("happiness_average")
top_10_positive = sorted_df.tail(10)[show_cols]
top_10_negative = sorted_df.head(10)[show_cols]

print("\nTop 10 positive words:")
print(top_10_positive)

print("\nTop 10 negative words:")
print(top_10_negative)

# top_10_positive.to_csv("top_10_positive_words.csv", index=False)
# top_10_negative.to_csv("top_10_negative_words.csv", index=False)






