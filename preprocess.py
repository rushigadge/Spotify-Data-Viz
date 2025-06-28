import pandas as pd
import json
import os
import sys

# CLI script to preprocess dataset

def main():
    csv_file = 'spotify dataset.csv'
    if not os.path.exists(csv_file):
        print(f"{csv_file} not found", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(csv_file)

    # Map dataset columns to required ones
    # 'pages' from duration_ms
    df['pages'] = df['duration_ms']
    # 'blurb' length from track_name
    df['blurb'] = df['track_name'].astype(str).str.len()
    # 'reviews' from tempo
    df['reviews'] = df['tempo']
    # 'rating' from popularity
    df['rating'] = df['popularity']

    cols = ['pages', 'blurb', 'reviews', 'rating']

    # Filter rows within 0.5-99.5 percentile for each numeric column
    for c in cols:
        lower = df[c].quantile(0.005)
        upper = df[c].quantile(0.995)
        df = df[(df[c] >= lower) & (df[c] <= upper)]

    # Sample at most 5000 rows
    df_sample = df.sample(n=min(len(df), 5000), random_state=42)

    records = df_sample[cols].to_dict(orient='records')

    out_file = 'scatter_data.json'
    with open(out_file, 'w') as f:
        json.dump(records, f, separators=(',', ':'), ensure_ascii=False)

    size = os.path.getsize(out_file)
    print(size)

if __name__ == '__main__':
    main()
