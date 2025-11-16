from pathlib import Path
import sys
import pandas as pd

# ensure project root is on sys.path when pytest runs from analytics_project/
HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.load_data import load_csv, summarize


def test_load_csv_real_file():
    csv_path = PROJECT_ROOT.parent / 'Global YouTube Statistics.csv'
    assert csv_path.exists(), f"CSV not found at {csv_path}"
    df = load_csv(csv_path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0


def test_summarize_keys():
    csv_path = PROJECT_ROOT.parent / 'Global YouTube Statistics.csv'
    df = load_csv(csv_path)
    s = summarize(df)
    assert 'shape' in s and 'columns' in s and 'missing_counts' in s
