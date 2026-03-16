import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

UNGD_happiness = Path(__file__).parent.parent / "data" / "processed" / "UNGD_happiness.csv"
UNGD_pre_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_pre_covid.csv"
UNGD_post_covid = Path(__file__).parent.parent / "data" / "processed" / "UNGD_post_covid.csv"

#function which automatically does bootstraping, for example see use below
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

range_bootstrap = bootstrap(df["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Range mean: \n", np.mean(df["happiness_average"]))
print("Range bootstrap mean: \n", np.mean(range_bootstrap))
print("Range bootstrap median: \n", np.median(range_bootstrap))
print("Range bootstrap std: \n", np.std(range_bootstrap))

ci = np.percentile(range_bootstrap, [2.5, 97.5])
print("95% confidence interval:", ci)

# histogram for the summary dataframe
plt.figure()
plt.hist(range_bootstrap, bins=50)
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

range_pre_bootstrap = bootstrap(df_pre["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Pre-COVID mean: \n", np.mean(df_pre["happiness_average"]))
print("Pre-COVID bootstrap mean: \n", np.mean(range_pre_bootstrap))
print("Pre-COVID bootstrap median: \n", np.median(range_pre_bootstrap))
print("Pre-COVID bootstrap std: \n", np.std(range_pre_bootstrap))

# histogram for the summary dataframe
plt.figure()
plt.hist(range_pre_bootstrap, bins=50)
plt.tight_layout()
plt.savefig("output/figures/UNGD_pre_covid_bootstrap.png")
plt.close()

ci = np.percentile(range_pre_bootstrap, [2.5, 97.5])
print("95% confidence interval:", ci)

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

range_post_bootstrap = bootstrap(df_post["happiness_average"], nboot, np.mean) # example of bootstrap function feel free to change var name

# important stats for analysis, repeat for following data frames
print("Post-COVID mean: \n", np.mean(df_post["happiness_average"]))
print("Post-COVID bootstrap mean: \n", np.mean(range_post_bootstrap))
print("Post-COVID bootstrap median: \n", np.median(range_post_bootstrap))
print("Post-COVID bootstrap std: \n", np.std(range_post_bootstrap))

# histogram for the summary dataframe
plt.figure()
plt.hist(range_post_bootstrap, bins=50)
plt.tight_layout()
plt.savefig("output/figures/UNGD_post_covid_bootstrap.png")
plt.close()

ci = np.percentile(range_post_bootstrap, [2.5, 97.5])
print("95% confidence interval:", ci)

# note: histograms still need defined x/y-axes + labels!