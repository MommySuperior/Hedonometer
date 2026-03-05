import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

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

df.to_csv("data/processed/Data_Set_S1_clean.csv", index=False)

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

print("\n2.1 Distribution of happiness_average")

h = df["happiness_average"].dropna()
stats_summary = pd.DataFrame(
    {
        "Metric": [
            "count",
            "mean",
            "median",
            "std",
            "p05",
            "p95",
        ],
        "Value": [
            float(h.shape[0]),
            float(h.mean()),
            float(h.median()),
            float(h.std()),
            float(h.quantile(0.05)),
            float(h.quantile(0.95)),
        ],
    }
)

print(stats_summary.to_string(index=False))
stats_summary.to_csv("data/processed/happiness_average_summary_stats.csv", index=False)

plt.figure()
plt.hist(h, bins=40, edgecolor="black")
plt.title("Distrubution of average happiness")
plt.xlabel("Happiness average")
plt.ylabel("# Words")
plt.tight_layout()
plt.savefig("output/figures/happiness_average_hist.png")
plt.close()

print("2.2 Disagreement: happiness_standard_deviation")

plt.figure()
plt.scatter(
    df["happiness_average"],
    df["happiness_standard_deviation"],
    s=10,
    alpha=0.35,
    marker='1',
)
plt.title("Disagreement vs score: happiness_average vs happiness_standard_deviation")
plt.xlabel("Happiness average")
plt.ylabel("Happineess standard distribution")
plt.tight_layout()
plt.savefig("output/figures/happiness_vs_std_scatter.png")
plt.close()

most_contested_15 = df.sort_values("happiness_standard_deviation", ascending=False).head(15)
print("Top 15 most 'contested' words (highest standard deviation):")
print(most_contested_15.to_string(index=False))
most_contested_15.to_csv("data/processed/top_15_contested_words.csv", index=False)


BASE = Path(__file__).resolve().parent
csv_path = ROOT / "data" / "processed" / "Data_Set_S1_clean.csv"

df = pd.read_csv(csv_path)

pos5 = df.sort_values("happiness_average", ascending=False).head(5).copy()
pos5["category"] = "very positive"

neg5 = df.sort_values("happiness_average", ascending=True).head(5).copy()
neg5["category"] = "very negative"

con5 = df.sort_values("happiness_standard_deviation", ascending=False).head(5).copy()
con5["category"] = "highly contested"

rank_cols = ["twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"]
df["rank_spread"] = df[rank_cols].max(axis=1, skipna=True) - df[rank_cols].min(axis=1, skipna=True)

weird5 = df.sort_values("rank_spread", ascending=False).head(5).copy()
weird5["category"] = "weird/corpus-specific"

exhibit = pd.concat([pos5, neg5, con5, weird5], ignore_index=True)

exhibit = exhibit[[
    "category", "word",
    "happiness_average", "happiness_standard_deviation",
    "twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"
]].sort_values(["category", "happiness_average"], ascending=[True, False])

out_csv = ROOT / "data" / "processed" / "exhibit_words_task3.csv"
exhibit.to_csv(out_csv, index=False)


