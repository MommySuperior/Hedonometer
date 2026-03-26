import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

UNGD_happiness = Path(__file__).parent.parent / "data" / "processed" / "UNGD_happiness.csv"
UNGD_pre_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_pre_covid.csv"
UNGD_post_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_post_covid.csv"

#-----------------------------------------------------
# Groups comparison
#-----------------------------------------------------

# gitwe can do the same for pre and post covid dataframes
src_folder = Path(__file__).resolve().parent
ROOT = src_folder.parent

df = pd.read_csv(UNGD_happiness)
df = df[(df["year"] >= 2015) & (df["year"] <= 2025)]
df_pre = pd.read_csv(UNGD_pre_covid)
df_post = pd.read_csv(UNGD_post_covid)

print(df_pre["year"].unique())
print(df_post["year"].unique())

print(df_pre["year"].value_counts().sort_index())
print(df_post["year"].value_counts().sort_index())

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
pre_stats = summarize_happiness(df_pre, "Pre-COVID (2015–2019)")
post_stats = summarize_happiness(df_post, "Post-COVID (2020–2025)")

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


#-----------------------------------------------------
# Bootstrapping function
#-----------------------------------------------------

nboot = 2000 #change value of iterations
def bootstrap(x, nboot, statsfunc):
    x = np.array(x)

    resampled_stats = []
    for i in range(nboot):
        index = np.random.randint(0,len(x), len(x)) 
        sample = x[index]
        bstatistic = statsfunc(sample)
        resampled_stats.append(bstatistic)

    return np.array(resampled_stats)

#-----------------------------------------------------
# UNGD_happiness summary, bootstrap, and histogram
#-----------------------------------------------------
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

range_bootstrap = bootstrap(df["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Range mean: \n", np.mean(df["happiness_average"]))
print("Range bootstrap mean: \n", np.mean(range_bootstrap))
print("Range bootstrap median: \n", np.median(range_bootstrap))
print("Range bootstrap std: \n", np.std(range_bootstrap))

ci_range = np.percentile(range_bootstrap, [2.5, 97.5])
print("95% confidence interval range:", ci_range)

# histogram for the summary dataframe
plt.figure()
plt.hist(range_bootstrap, bins=50)
plt.title("Range Summary happiness (bootstrapped)")
plt.xlabel("Happiness average")
plt.ylabel("Frequency/Iterations")
plt.tight_layout()
plt.savefig("output/figures/UNGD_summary_bootstrap.png")
plt.close()

#-----------------------------------------------------
# UNGD_pre_covid summary, bootstrap, and histogram
#-----------------------------------------------------
print("Pre-COVID head:") # this can go
print(df_pre.head()) # this too
print("Pre-COVID description:")
print(df_pre.describe())

summary_pre = df_pre.groupby("year")["happiness_average"].agg(
    mean="mean",
    median="median",
    standard_deviation ="std",
    occurrence="count" # how many times this year occurs in column "year"
)

print("Pre-COVID summary:")
print(summary_pre)

range_pre_bootstrap = bootstrap(df_pre["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Pre-COVID mean: \n", np.mean(df_pre["happiness_average"]))
print("Pre-COVID bootstrap mean: \n", np.mean(range_pre_bootstrap))
print("Pre-COVID bootstrap median: \n", np.median(range_pre_bootstrap))
print("Pre-COVID bootstrap std: \n", np.std(range_pre_bootstrap))

# histogram for the pre covid dataframe
plt.figure()
plt.hist(range_pre_bootstrap, bins=50)
plt.title("Pre-COVID happiness (bootstrapped)")
plt.xlabel("Happiness average")
plt.ylabel("Frequency/Iterations")
plt.ylim(0, 140)
plt.xlim(5.440, 5.458)
plt.tight_layout()
plt.savefig("output/figures/UNGD_pre_covid_bootstrap.png")
plt.close()

ci_pre = np.percentile(range_pre_bootstrap, [2.5, 97.5])
print("95% confidence interval pre-COVID:", ci_pre)

#-----------------------------------------------------
# UNGD_post_covid summary, bootstrap, and histogram
#-----------------------------------------------------
print("Post-COVID head:") # this can go
print(df_post.head()) # this too
print("Post-COVID description:")
print(df_post.describe())

summary_post = df_post.groupby("year")["happiness_average"].agg(
    mean="mean",
    median="median",
    standard_deviation ="std",
    occurrence="count" # how many times this year occurs in column "year"
)

print("Post-COVID summary:")
print(summary_post)

range_post_bootstrap = bootstrap(df_post["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Post-COVID mean: \n", np.mean(df_post["happiness_average"]))
print("Post-COVID bootstrap mean: \n", np.mean(range_post_bootstrap))
print("Post-COVID bootstrap median: \n", np.median(range_post_bootstrap))
print("Post-COVID bootstrap std: \n", np.std(range_post_bootstrap))

# histogram for the post covid dataframe
plt.figure()
plt.hist(range_post_bootstrap, bins=50)
plt.title("Post-COVID happiness (bootstrapped)")
plt.xlabel("Happiness average")
plt.ylabel("Frequency/Iterations")
plt.ylim(0, 140)
plt.xlim(5.440, 5.458)
plt.tight_layout()
plt.savefig("output/figures/UNGD_post_covid_bootstrap.png")
plt.close()

ci_post = np.percentile(range_post_bootstrap, [2.5, 97.5])
print("95% confidence interval post-COVID:", ci_post)
ci_difference = np.percentile(range_post_bootstrap - range_pre_bootstrap, [2.5, 97.5])

print("\n95% confidence interval difference:", ci_difference, "\n")

# Scatter plot for the full range of the data:

plt.figure()
plt.scatter(
    df["happiness_average"],
    df["happiness_standard_deviation"],
    s=10,
    alpha=0.35,
    marker='1',
)
plt.title("Post and Pre COVID happiness")
plt.xlabel("Happiness average")
plt.ylabel("Happiness standard deviation")
plt.tight_layout
plt.savefig("output/figures/UNGD_Full_Range_Scatter.png")
plt.close()

# Comparison histograms for both pre and post COVID

plt.figure()
plt.hist(df_pre["happiness_average"], bins=50, label="Pre COVID", alpha=0.5)
plt.hist(df_post["happiness_average"], bins=50, label="Post COVID", alpha=0.5)
plt.legend(loc="best")
plt.title("Happiness difference in pre and post COVID UNGDs")
plt.xlabel("Average happiness")
plt.ylabel("Frequency")
plt.tight_layout
plt.savefig("output/figures/UNGD_pre_post_comparison.png")
plt.close()

# Comparison scatter plot for both pre and post COVID

plt.figure()
plt.scatter(
    df_pre["happiness_average"],
    df_pre["happiness_standard_deviation"],
    label="Pre COVID",
    s=10,
    alpha=0.45,
    marker='1',
)
plt.scatter(
    df_post["happiness_average"],
    df_post["happiness_standard_deviation"],
    label="Post COVID",
    s=10,
    alpha=0.45,
    marker='1',
)
plt.legend(loc=0)
plt.title("Happiness avg vs std in pre and post COVID UNGDs")
plt.xlabel("Happiness average")
plt.ylabel("Happiness standard deviation")
plt.tight_layout
plt.savefig("output/figures/UNGD_pre_post_COVID_Scatter.png")
plt.close()

print("Statistical uncertainty (post/pre):")
print((np.max(df_pre["happiness_average"]) - np.min(df_pre["happiness_average"]))/2)
print((np.max(df_post["happiness_average"]) - np.min(df_post["happiness_average"]))/2)