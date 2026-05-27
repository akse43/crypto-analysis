import pandas as pd
import glob

all_files = glob.glob(r"G:\Downloads\crypto\data\*.csv")

print(all_files)

dfs = []

for f in all_files:
    df = pd.read_csv(f)
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

combined.to_csv(r"G:\Downloads\crypto\data\combined.csv", index=False)

