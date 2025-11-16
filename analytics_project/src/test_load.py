import sys
from pathlib import Path

# Ensure the analytics_project root is on sys.path so `from src...` works
HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]  # analytics_project/
sys.path.insert(0, str(PROJECT_ROOT))

from src.load_data import load_csv, summarize


def main():
    # default: CSV in workspace root (one level above analytics_project)
    default_csv = PROJECT_ROOT.parent / 'Global YouTube Statistics.csv'
    path = str(default_csv)
    print(f"Trying to load: {path}")
    df = load_csv(path)
    print('shape:', df.shape)
    print('columns:', df.columns.tolist()[:20])
    print('\n--- sample rows ---\n')
    print(df.head(5).to_string(index=False))


if __name__ == '__main__':
    main()
