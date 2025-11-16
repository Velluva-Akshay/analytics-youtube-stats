from pathlib import Path
import pandas as pd


def load_csv(path):
    """Load CSV into a pandas DataFrame. Returns DataFrame.

    Args:
        path (str or Path): path to CSV file
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    # try common encodings and fallback
    try:
        df = pd.read_csv(p)
    except Exception:
        df = pd.read_csv(p, encoding='latin-1')
    return df


def summarize(df):
    """Return a small summary dict for quick inspection."""
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isnull().sum().to_dict(),
    }


def basic_cleaning(df):
    """Perform lightweight cleaning on the DataFrame and return a cleaned copy.

    Actions:
    - strip column names
    - convert 'subscribers' and 'video views' to numeric columns (if present)
    - drop exact duplicate rows
    """
    df = df.copy()
    # normalize column names
    df.columns = [c.strip() for c in df.columns]

    # numeric conversion examples
    if 'subscribers' in df.columns:
        df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')
    # some files use 'video views' with a space
    if 'video views' in df.columns:
        df['video_views'] = pd.to_numeric(df['video views'], errors='coerce')
    if 'video_views' in df.columns and 'video views' in df.columns:
        # keep both for backward compatibility; callers can drop duplicates later
        pass

    # drop exact duplicates
    df = df.drop_duplicates()
    return df


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "Global YouTube Statistics.csv"
    print(f"Loading: {path}")
    df = load_csv(path)
    s = summarize(df)
    print("shape:", s['shape'])
    print("first columns:", s['columns'][:10])
    print("missing (top 10):")
    for k, v in list(s['missing_counts'].items())[:10]:
        print(k, v)