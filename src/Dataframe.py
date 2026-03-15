import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

src_folder = Path(__file__).resolve().parent
ROOT = src_folder.parent

data_path = ROOT / "data" / "processed"

pre_covid_df = pd.read_csv(data_path / "UNGD_pre_covid.csv")
post_covid_df = pd.read_csv(data_path / "UNGD_post_covid.csv")

print(pre_covid_df["year"].unique())
print(post_covid_df["year"].unique())

print(pre_covid_df["year"].value_counts().sort_index())
print(post_covid_df["year"].value_counts().sort_index())

def summarize_happiness(df, label):

    stats = {
        "label": label,
        "sample_size": len(df),
        "mean": df["happiness_average"].mean(),
        "median": df["happiness_average"].median(),
        "std_dev": df["happiness_average"].std()
    }

    return stats

pre_stats = summarize_happiness(pre_covid_df, "Pre-COVID (2015–2019)")
post_stats = summarize_happiness(post_covid_df, "Post-COVID (2020–2025)")

results_df = pd.DataFrame([pre_stats, post_stats])

difference = post_stats["mean"] - pre_stats["mean"]

print("\nPre-COVID statistics")
print(pre_stats)

print("\nPost-COVID statistics")
print(post_stats)

print("\nDifference in mean happiness (post - pre):", round(difference,4))

results_df = pd.DataFrame([pre_stats, post_stats])

results_df = results_df.rename(columns={
    "label": "Period",
    "sample_size": "Speeches",
    "mean": "Mean Happiness",
    "median": "Median Happiness",
    "std_dev": "Std Dev"
})

results_df["Mean Happiness"] = results_df["Mean Happiness"].round(4)
results_df["Median Happiness"] = results_df["Median Happiness"].round(4)
results_df["Std Dev"] = results_df["Std Dev"].round(4)

output_folder = ROOT / "data" / "processed"
results_df.to_csv(output_folder / "happiness_pre_post_comparison.csv", index=False)