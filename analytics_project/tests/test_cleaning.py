from pathlib import Path
import sys
import pandas as pd

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.load_data import basic_cleaning


def test_basic_cleaning_numeric_and_dedup():
    # build a small sample DataFrame
    data = {
        ' rank ': [1, 1, 2],
        'Youtuber': ['A', 'A', 'B'],
        'subscribers': ['1000', '1000', '2000'],
        'video views': ['10000', '10000', '25000'],
    }
    df = pd.DataFrame(data)
    cleaned = basic_cleaning(df)
    # column names should be stripped
    assert 'rank' in cleaned.columns
    # subscribers should be numeric
    assert pd.api.types.is_numeric_dtype(cleaned['subscribers'])
    # video_views should exist and be numeric
    assert 'video_views' in cleaned.columns
    assert pd.api.types.is_numeric_dtype(cleaned['video_views'])
    # duplicates dropped (original had two identical rows)
    assert cleaned.shape[0] == 2
