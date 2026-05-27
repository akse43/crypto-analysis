import pandas as pd
import numpy as np

df = pd.read_csv(r"G:\Downloads\crypto\data\combined.csv")
# tinh trung binh 7 ngay
WINDOW = 7

def fill_zeros_for_coin(series):
    vals   = series.to_list()
    filled = [np.nan] * len(vals)
    pool   = []

    for i, v in enumerate(vals):
        if not np.isnan(v):
            filled[i] = v
            pool.append(v)
        else:
            known  = list(pool)
            needed = WINDOW - len(known)
            if needed > 0:
                future_reals = [x for x in vals[i+1:] if not np.isnan(x)]
                known += future_reals[:needed]
            if len(known) == 0:
                filled[i] = np.nan
            else:
                avg = round(np.mean(known[:WINDOW]), 6)
                filled[i] = avg
                pool.append(avg)

    return pd.Series(filled, index=series.index)

df['mcap_num'] = pd.to_numeric(df['market_cap'], errors='coerce')
df.loc[df['mcap_num'] == 0, 'mcap_num'] = np.nan
df['date_parsed'] = pd.to_datetime(df['date'], format='ISO8601')
df = df.sort_values(['coin_name', 'date_parsed']).reset_index(drop=True)




parts = []
for coin, group in df.groupby('coin_name', sort=False):
    g = group.copy().reset_index(drop=True)
    g['mcap_num'] = fill_zeros_for_coin(g['mcap_num'])
    parts.append(g)

df_clean = pd.concat(parts).sort_values(['coin_name', 'date_parsed']).reset_index(drop=True)
df_clean['market_cap'] = df_clean['mcap_num'].fillna(0)


df_clean['coin_name'] = df_clean['coin_name'].str.capitalize()

df_out = df_clean[['date', 'price', 'total_volume', 'market_cap', 'coin_name']]
df_out.to_csv(r"G:\Downloads\crypto\data_cleaned.csv", index=False)