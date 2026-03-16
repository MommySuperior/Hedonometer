import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

UNGD_happiness = Path(__file__).parent.parent / "data" / "processed" / "UNGD_happiness.csv"
UNGD_pre_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_pre_covid.csv"
UNGD_post_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_post_covid.csv"

#function which automatically does bootstraping, for example see use below
nboot = 2000 #change value of itterations
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
plt.savefig("output/figures/UNGD_summary_bootstrap.png")
plt.close()

#-----------------------------------------------------
# UNGD_pre_covid summary, bootstrap, and histogram
#-----------------------------------------------------
df_pre = pd.read_csv(UNGD_pre_covid)
df_pre = df_pre[(df_pre["year"] >= 2015) & (df_pre["year"] <= 2019)]
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

summary_pre_bootstrap = bootstrap(summary_pre, nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Summary mean: \n", np.mean(summary_pre))
print("Summary bootstrap mean: \n", np.mean(summary_pre_bootstrap))
print("Summary bootstrap median \n", np.median(summary_pre_bootstrap))
print("Summary bootstrap std: \n", np.std(summary_pre_bootstrap))

# histogram for the summary dataframe
plt.figure()
plt.hist(summary_pre_bootstrap, bins=50)
plt.tight_layout()
plt.savefig("output/figures/UNGD_pre_covid_bootstrap.png")
plt.close()

#-----------------------------------------------------
# UNGD_post_covid summary, bootstrap, and histogram
#-----------------------------------------------------
df_post = pd.read_csv(UNGD_post_covid)
df_post = df_post[(df_post["year"] >= 2020) & (df_post["year"] <= 2025)]
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

summary_post_bootstrap = bootstrap(summary_post, nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Summary mean: \n", np.mean(summary_post))
print("Summary bootstrap mean: \n", np.mean(summary_post_bootstrap))
print("Summary bootstrap median \n", np.median(summary_post_bootstrap))
print("Summary bootstrap std: \n", np.std(summary_post_bootstrap))

# histogram for the summary dataframe
plt.figure()
plt.hist(summary_post_bootstrap, bins=50)
plt.tight_layout()
plt.savefig("output/figures/UNGD_post_covid_bootstrap.png")
plt.close()