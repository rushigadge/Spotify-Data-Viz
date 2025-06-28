import pandas as pd
import numpy as np
import json
from pathlib import Path
import argparse


def main():
    p = argparse.ArgumentParser(description="Prepare Goodreads data for scatter plots")
    p.add_argument("csv", nargs="?", default="GoodReads_100k_books.csv", help="Input CSV file")
    p.add_argument("--out", default="scatter_data.json", help="Output JSON file")
    p.add_argument("--sample", type=int, default=5000, help="Maximum number of rows")
    args = p.parse_args()

    df = pd.read_csv(args.csv)

    df["blurb"] = df["desc"].astype(str).str.len()
    cols = ["pages", "blurb", "reviews", "rating"]
    df = df.dropna(subset=cols)

    for c in cols:
        q_low, q_hi = df[c].quantile([0.005, 0.995])
        df = df[(df[c] >= q_low) & (df[c] <= q_hi)]

    df = df.sample(min(len(df), args.sample), random_state=42)

    data = df[cols].to_dict(orient="records")
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    size = Path(args.out).stat().st_size
    print(size)


if __name__ == "__main__":
    main()
