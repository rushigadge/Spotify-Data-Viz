import pandas as pd
import json
import os
import sys

"""Prepare a compact dataset for the interactive visual story.
The script reads 'spotify dataset.csv', trims outliers on key numeric columns
using the 0.5 and 99.5 percentile, samples up to 5000 rows (seed 42) and
writes the result to 'scatter_data.json'. It prints the resulting byte size."""

def main():
    src = 'spotify dataset.csv'
    if not os.path.exists(src):
        print(f"{src} not found", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(src)

    # Map relevant columns to simpler names
    df = df.rename(columns={'duration_ms': 'pages',
                            'tempo': 'reviews',
                            'popularity': 'rating'})
    df['blurb'] = df['track_name'].astype(str).str.len()
    df['explicit'] = df['explicit'].astype(bool)
    df['genre'] = df['track_genre']

    keep = ['pages', 'blurb', 'reviews', 'rating',
            'danceability', 'energy', 'valence', 'acousticness']
    for col in keep:
        q_low, q_hi = df[col].quantile([0.005, 0.995])
        df = df[df[col].between(q_low, q_hi)]

    sample = df.sample(min(len(df), 5000), random_state=42).sort_values('pages')
    out = sample[keep + ['explicit', 'genre']]
    with open('scatter_data.json', 'w') as f:
        json.dump(out.to_dict('records'), f, separators=(',', ':'), ensure_ascii=False)

    print(os.path.getsize('scatter_data.json'))

if __name__ == '__main__':
    main()
