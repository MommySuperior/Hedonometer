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

print("2.3 Corpus comparison: rank coverage + overlaps")

rank_cols = ["twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"]

coverage_rows = []
for col in rank_cols:
    n_present = int(df[col].notna().sum())
    coverage_rows.append(
        {
        "rank_column": col,
        "n_words_with_rank": n_present,
        "share_of_lexicon": n_present / len(df),
        }
)

coverage = pd.DataFrame(coverage_rows)
print(coverage.to_string(index=False))
coverage.to_csv("data/processed/corpus_rank_coverage.csv", index=False)

plt.figure
plt.bar(coverage["rank_column"], coverage["n_words_with_rank"])
plt.title("How many labMT words appear in each corpus top-5000?")
plt.xlabel("Rank column")
plt.ylabel("Number of words in 5000")
plt.tight_layout()
plt.savefig("output/figures/corpus_rank_coverage_bar.png")
plt.close()

flags = pd.DataFrame(
    {
        "Twitter": df["twitter_rank"].notna(),
        "Google" : df["google_rank"].notna(),
        "Nyt" : df["nyt_rank"].notna(),
        "Lyrics" : df["lyrics_rank"].notna()
    }
)

labels = ["Twitter", "Google", "Nyt", "Lyrics"]
patterns = flags.apply(lambda row: "+".join([lab for lab in labels if row[lab]]) or "none", axis=1)

pattern_counts = patterns.value_counts().reset_index()

print("\nOverlap of words over platforms:")
print(pattern_counts.head(12).to_string(index=False))
pattern_counts.to_csv("data/processed/corpus_overlap_patterns.csv", index=False)

pairs = []
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        a, b = labels[i], labels[j]
        pairs.append({"pair": f"{a}+{b}", "n_words_in_both": int((flags[a] & flags[b]).sum())})

pairwise_overlap = pd.DataFrame(pairs).sort_values("pair")
pairwise_overlap.to_csv("data/processed/pairwise_overlap_counts.csv", index=False)

twitter_common_nyt_missing = (
    df[(df["twitter_rank"].notna()) & (df["nyt_rank"].isna())]
    .sort_values("twitter_rank")
    .head(20)[["word", "twitter_rank", "happiness_average"]]
)

print("\nExample words frequent on Twitter but missing in NYT top-5000 (top 20 by twitter_rank):")
print(twitter_common_nyt_missing.to_string(index=False))
twitter_common_nyt_missing.to_csv("data/processed/twitter_common_nyt_missing_top20.csv", index=False)

both_twitter_nyt = df.dropna(subset=["twitter_rank", "nyt_rank"])

plt.figure()
plt.scatter(both_twitter_nyt["twitter_rank"], both_twitter_nyt["nyt_rank"], s=10, alpha=0.35)
plt.title("Twitter rank vs NYT rank (words present in both)")
plt.xlabel("twitter_rank (1 = most frequent)")
plt.ylabel("nyt_rank (1 = most frequent)")
plt.tight_layout()
plt.savefig("output/figures/twitter_rank_vs_nyt_rank_scatter.png")
plt.close()
