import pandas as pd
import json
import os
import sys

"""Preprocess Spotify dataset for scatter plots.
Reads 'spotify dataset.csv', filters numeric columns by percentile,
randomly samples up to 5k rows (seed=42) and writes 'scatter_data.json'.
Prints the resulting file size in bytes."""

def main():
    src='spotify dataset.csv'
    if not os.path.exists(src):
        print(f"{src} not found", file=sys.stderr)
        sys.exit(1)

    df=pd.read_csv(src)

    df=df.rename(columns={'duration_ms':'pages','tempo':'reviews','popularity':'rating'})
    df['blurb']=df['track_name'].astype(str).str.len()
    cols=['pages','blurb','reviews','rating']

    for c in cols:
        q=df[c].quantile([0.005,0.995])
        df=df[df[c].between(q.iloc[0], q.iloc[1])]

    sample=df.sample(n=min(len(df),5000), random_state=42).sort_values('pages')
    with open('scatter_data.json','w') as f:
        json.dump(sample[cols].to_dict('records'), f, separators=(',', ':'), ensure_ascii=False)

    print(os.path.getsize('scatter_data.json'))

if __name__=='__main__':
    main()
