"""
Tests for the analysis module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis import YouTubeAnalyzer


@pytest.fixture
def sample_data():
    """Create sample YouTube data for testing."""
    return pd.DataFrame({
        'Youtuber': ['Channel A', 'Channel B', 'Channel C', 'Channel D', 'Channel E'],
        'subscribers': [1000000, 500000, 2000000, 750000, 1500000],
        'video views': [10000000, 5000000, 25000000, 8000000, 18000000],
        'uploads': [100, 50, 200, 80, 150],
        'category': ['Music', 'Gaming', 'Music', 'Entertainment', 'Gaming'],
        'Country': ['US', 'UK', 'US', 'CA', 'US']
    })


def test_analyzer_initialization(sample_data):
    """Test analyzer can be initialized with dataframe."""
    analyzer = YouTubeAnalyzer(sample_data)
    assert analyzer.df is not None
    assert len(analyzer.df) == 5


def test_get_top_performers(sample_data):
    """Test getting top performers by metric."""
    analyzer = YouTubeAnalyzer(sample_data)
    top3 = analyzer.get_top_performers('subscribers', n=3)
    
    assert len(top3) == 3
    assert top3.iloc[0]['Youtuber'] == 'Channel C'  # Highest subscribers
    assert top3.iloc[0]['subscribers'] == 2000000


def test_category_analysis(sample_data):
    """Test category analysis."""
    analyzer = YouTubeAnalyzer(sample_data)
    cat_stats = analyzer.category_analysis()
    
    assert 'subscribers' in cat_stats
    assert 'mean' in cat_stats['subscribers']
    assert len(cat_stats['subscribers']['mean']) > 0


def test_engagement_metrics(sample_data):
    """Test engagement metrics calculation."""
    analyzer = YouTubeAnalyzer(sample_data)
    metrics = analyzer.engagement_metrics()
    
    assert 'avg_views_per_subscriber' in metrics
    assert 'avg_views_per_upload' in metrics
    assert metrics['avg_views_per_subscriber'] > 0


def test_correlation_analysis(sample_data):
    """Test correlation matrix generation."""
    analyzer = YouTubeAnalyzer(sample_data)
    corr_matrix = analyzer.correlation_analysis()
    
    assert corr_matrix is not None
    assert 'subscribers' in corr_matrix.columns
    assert 'video views' in corr_matrix.columns


def test_generate_report(sample_data):
    """Test report generation."""
    analyzer = YouTubeAnalyzer(sample_data)
    report = analyzer.generate_report()
    
    assert isinstance(report, str)
    assert 'YOUTUBE STATISTICS ANALYSIS REPORT' in report
    assert 'DATASET OVERVIEW' in report
    assert 'Total Channels: 5' in report
