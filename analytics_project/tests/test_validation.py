"""
Tests for the validation module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.validation import DataValidator, ValidationResult


@pytest.fixture
def clean_data():
    """Create clean sample data."""
    return pd.DataFrame({
        'Youtuber': ['Channel A', 'Channel B', 'Channel C'],
        'subscribers': [1000000, 500000, 2000000],
        'video views': [10000000, 5000000, 25000000],
        'uploads': [100, 50, 200]
    })


@pytest.fixture
def messy_data():
    """Create messy sample data with issues."""
    return pd.DataFrame({
        'Youtuber': ['Channel A', 'Channel B', 'Channel C', 'Channel A'],
        'subscribers': [1000000, np.nan, 2000000, 1000000],
        'video views': [-100, 5000000, 25000000, -100],
        'uploads': [100, 50, 200, 100]
    })


def test_validator_initialization(clean_data):
    """Test validator can be initialized."""
    validator = DataValidator(clean_data)
    assert validator.df is not None
    assert len(validator.df) == 3


def test_check_missing_values_clean(clean_data):
    """Test missing value check on clean data."""
    validator = DataValidator(clean_data)
    result = validator.check_missing_values()
    
    assert result.passed is True
    assert result.stats['total_missing'] == 0


def test_check_missing_values_messy(messy_data):
    """Test missing value check on messy data."""
    validator = DataValidator(messy_data)
    result = validator.check_missing_values(threshold=0.1)
    
    assert result.stats['total_missing'] > 0


def test_check_duplicates_clean(clean_data):
    """Test duplicate check on clean data."""
    validator = DataValidator(clean_data)
    result = validator.check_duplicates()
    
    assert result.stats['n_duplicates'] == 0


def test_check_duplicates_messy(messy_data):
    """Test duplicate check on messy data."""
    validator = DataValidator(messy_data)
    result = validator.check_duplicates()
    
    assert result.stats['n_duplicates'] > 0


def test_check_required_columns(clean_data):
    """Test required columns check."""
    validator = DataValidator(clean_data)
    result = validator.check_required_columns(['Youtuber', 'subscribers'])
    
    assert result.passed is True


def test_check_required_columns_missing():
    """Test required columns check with missing columns."""
    df = pd.DataFrame({'col1': [1, 2, 3]})
    validator = DataValidator(df)
    result = validator.check_required_columns(['col1', 'col2', 'col3'])
    
    assert result.passed is False
    assert len(result.issues) > 0


def test_check_value_ranges_negative(messy_data):
    """Test value range check with negative values."""
    validator = DataValidator(messy_data)
    result = validator.check_value_ranges()
    
    # Should detect negative video views
    assert result.passed is False
    assert any('negative' in issue.lower() for issue in result.issues)


def test_generate_quality_report(clean_data):
    """Test quality report generation."""
    validator = DataValidator(clean_data)
    report = validator.generate_quality_report()
    
    assert isinstance(report, str)
    assert 'DATA QUALITY REPORT' in report
    assert 'DATASET OVERVIEW' in report
