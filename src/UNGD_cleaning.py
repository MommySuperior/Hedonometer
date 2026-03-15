import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import shutil as sh

raw = Path(__file__).parent.parent / "data" / "raw" / "TXT"
out = Path(__file__).parent.parent / "data" / "raw" / "range"

out.mkdir(parents=True, exist_ok=True)
print(f"Converting sessions 1-80 from {raw} to CSV")

folders = []
for file in raw.iterdir():
    if file.is_dir() and not file.name.startswith("."):
        folders.append(file)

converted = []
not_found = []

for num in range(1, 81):
    num = str(num).zfill(2)
    print(f"\nSession {num}:")

    found = None
    for file in folders:
        if file.name.startswith(f"Session {num} -"):
            found = file
            break

    if not found:
            print(f"  Not found")
            not_found.append(num)
            continue

    out_folder = out / found.name
    out_folder.mkdir(exist_ok=True)

    count = 0
    for file in found.iterdir():
        if file.suffix == '.txt' and not file.name.startswith('.'):
            dest_file = out_folder / (file.stem + '.txt')
            #try:
            #df = pd.read_csv(file, sep=' ', engine='python')
            #df.to_csv(csv_file, sep='=', index=False) # csvs use semicolons instead of commas
            #count += 1
            #print(f"  Converted: {file.name} -> {csv_file.name}")
            #except:
            #    print(f"  Error: Could not convert {file.name}")
            result= sh.copy2(file, dest_file)
            print(result)

    #if count > 0:
    #    converted.append(found.name)
    #    print(f" Done: {count} files converted")

raw_range = out

labmt_clean = Path(__file__).parent.parent / "data" / "processed" / "Data_Set_S1_clean.csv"
labmt_df = pd.read_csv(labmt_clean)
labmt_dict = dict(zip(labmt_df["word"], labmt_df["happiness_average"]))
labmt_words = set(labmt_dict.keys())

# function to tokenize and clean txt, not tested yet
PUNCT = ".,;:?!/()&$"
def tok_clean(txt):
     txt = txt.strip().lower()
     for ch in PUNCT:
          txt = txt.replace(ch, "")
     return txt.split()

# iteration loop UNGD raw_range
UNGD_rows = []
for txt_file in raw_range.rglob("*.txt"):
    name = txt_file.stem  # removes .txt
    country, session, year = name.split("_") 

    text = txt_file.read_text(encoding="utf-8")
    tokens = tok_clean(text)

    scores = []

    for token in tokens:
         if token in labmt_words:
                scores.append(labmt_dict[token])
    avg_score = np.mean(scores)

    UNGD_rows.append({
    "year": year,
    "country": country,
    "session": session,
    "happiness_average": avg_score
    })

df = pd.DataFrame(UNGD_rows)
df.to_csv("data/processed/UNGD_happiness.csv", index=False)
 