import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

UNGD_happiness = Path(__file__).parent.parent / "data" / "processed" / "UNGD_happiness.csv"
UNGD_pre_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_pre_covid.csv"
UNGD_post_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_post_covid.csv"

#function which automatically does bootstraping, for example see use below
nboot = 1000 #change value of itterations
def bootstrap(x, nboot, statsfunc):
    x = np.array(x)

    resampled_stats = []
    for i in range(nboot):
        index = np.random.randint(0,len(x), len(x))
        sample = x[index]
        bstatistic = statsfunc(sample)
        resampled_stats.append(bstatistic)

    return np.array(resampled_stats)

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


summary_bootstrap = bootstrap(summary, nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Summary mean: \n", np.mean(summary))
print("Summary bootstrap mean: \n", np.mean(summary_bootstrap))
print("Summary bootstrap median \n", np.median(summary_bootstrap))
print("Summary bootstrap std: \n", np.std(summary_bootstrap))

# histogram for the summary dataframe
plt.figure()
plt.hist(summary_bootstrap, bins=50)
plt.tight_layout()
plt.savefig("Hedonometer/output/figures/UNGD_summary_bootstrap.png")
plt.close()

# gitwe can do the same for pre and post covid dataframes
src_folder = Path(__file__).resolve().parent
ROOT = src_folder.parent

data_path = ROOT / "data" / "processed"

pre_covid_df = pd.read_csv(data_path / "UNGD_pre_covid.csv")
post_covid_df = pd.read_csv(data_path / "UNGD_post_covid.csv")

print(pre_covid_df["year"].unique())
print(post_covid_df["year"].unique())

print(pre_covid_df["year"].value_counts().sort_index())
print(post_covid_df["year"].value_counts().sort_index())

# function to summarize happiness stats for a given dataframe and label
def summarize_happiness(df, label):

    stats = {
        "label": label,
        "sample_size": len(df),
        "mean": df["happiness_average"].mean(),
        "median": df["happiness_average"].median(),
        "std_dev": df["happiness_average"].std()
    }

    return stats

# calculate stats for pre and post covid dataframes
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

# rename columns for better presentation
results_df = results_df.rename(columns={
    "label": "Period",
    "sample_size": "Speeches",
    "mean": "Mean Happiness",
    "median": "Median Happiness",
    "std_dev": "Std Dev"
})

# round the values to 4 decimal places for better presentation
results_df["Mean Happiness"] = results_df["Mean Happiness"].round(4)
results_df["Median Happiness"] = results_df["Median Happiness"].round(4)
results_df["Std Dev"] = results_df["Std Dev"].round(4)

output_folder = ROOT / "data" / "processed"
results_df.to_csv(output_folder / "happiness_pre_post_comparison.csv", index=False)
