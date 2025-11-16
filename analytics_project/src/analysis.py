"""
Advanced analysis module for YouTube Statistics.

Provides statistical insights, trend analysis, and automated reporting.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from pathlib import Path


class YouTubeAnalyzer:
    """Advanced analytics for YouTube statistics data."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize analyzer with dataframe."""
        self.df = df
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis."""
        # Convert numeric columns
        numeric_cols = ['subscribers', 'video views', 'uploads']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Clean column names
        self.df.columns = self.df.columns.str.strip()
    
    def get_top_performers(self, metric: str = 'subscribers', n: int = 10) -> pd.DataFrame:
        """Get top N performers by specified metric."""
        if metric not in self.df.columns:
            raise ValueError(f"Metric '{metric}' not found in dataset")
        
        return self.df.nlargest(n, metric)[['Youtuber', 'category', metric]]
    
    def category_analysis(self) -> Dict[str, Any]:
        """Analyze statistics by category."""
        if 'category' not in self.df.columns:
            return {}
        
        category_stats = {}
        
        for col in ['subscribers', 'video views', 'uploads']:
            if col in self.df.columns:
                category_stats[col] = {
                    'mean': self.df.groupby('category')[col].mean().sort_values(ascending=False),
                    'median': self.df.groupby('category')[col].median().sort_values(ascending=False),
                    'total': self.df.groupby('category')[col].sum().sort_values(ascending=False),
                    'count': self.df.groupby('category')[col].count()
                }
        
        return category_stats
    
    def country_analysis(self) -> Dict[str, Any]:
        """Analyze statistics by country."""
        if 'Country' not in self.df.columns:
            return {}
        
        country_stats = {
            'total_channels': self.df['Country'].value_counts(),
            'avg_subscribers': self.df.groupby('Country')['subscribers'].mean().sort_values(ascending=False) if 'subscribers' in self.df.columns else None,
            'total_subscribers': self.df.groupby('Country')['subscribers'].sum().sort_values(ascending=False) if 'subscribers' in self.df.columns else None,
        }
        
        return country_stats
    
    def engagement_metrics(self) -> Dict[str, float]:
        """Calculate engagement metrics."""
        metrics = {}
        
        if 'subscribers' in self.df.columns and 'video views' in self.df.columns:
            # Views per subscriber
            self.df['views_per_subscriber'] = self.df['video views'] / self.df['subscribers']
            metrics['avg_views_per_subscriber'] = self.df['views_per_subscriber'].mean()
            metrics['median_views_per_subscriber'] = self.df['views_per_subscriber'].median()
        
        if 'uploads' in self.df.columns and 'video views' in self.df.columns:
            # Views per upload
            self.df['views_per_upload'] = self.df['video views'] / self.df['uploads']
            metrics['avg_views_per_upload'] = self.df['views_per_upload'].mean()
            metrics['median_views_per_upload'] = self.df['views_per_upload'].median()
        
        if 'uploads' in self.df.columns and 'subscribers' in self.df.columns:
            # Subscribers per upload
            self.df['subs_per_upload'] = self.df['subscribers'] / self.df['uploads']
            metrics['avg_subs_per_upload'] = self.df['subs_per_upload'].mean()
            metrics['median_subs_per_upload'] = self.df['subs_per_upload'].median()
        
        return metrics
    
    def correlation_analysis(self) -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].corr()
    
    def outlier_detection(self, column: str, method: str = 'iqr') -> Tuple[pd.DataFrame, Dict]:
        """Detect outliers in specified column."""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        data = self.df[column].dropna()
        
        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
            
            stats = {
                'method': 'IQR',
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'n_outliers': len(outliers),
                'pct_outliers': (len(outliers) / len(self.df)) * 100
            }
        else:
            # Z-score method
            mean = data.mean()
            std = data.std()
            z_scores = np.abs((data - mean) / std)
            outliers = self.df[np.abs((self.df[column] - mean) / std) > 3]
            
            stats = {
                'method': 'Z-score',
                'threshold': 3,
                'n_outliers': len(outliers),
                'pct_outliers': (len(outliers) / len(self.df)) * 100
            }
        
        return outliers, stats
    
    def generate_report(self) -> str:
        """Generate a comprehensive text report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("YOUTUBE STATISTICS ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Dataset overview
        report_lines.append("DATASET OVERVIEW")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Channels: {len(self.df):,}")
        report_lines.append(f"Features: {len(self.df.columns)}")
        report_lines.append("")
        
        # Top performers
        if 'subscribers' in self.df.columns:
            report_lines.append("TOP 5 CHANNELS BY SUBSCRIBERS")
            report_lines.append("-" * 80)
            top5 = self.get_top_performers('subscribers', 5)
            for idx, row in top5.iterrows():
                report_lines.append(f"{row['Youtuber']:30s} {row['subscribers']:>15,} subscribers")
            report_lines.append("")
        
        # Category insights
        if 'category' in self.df.columns:
            report_lines.append("CATEGORY INSIGHTS")
            report_lines.append("-" * 80)
            cat_counts = self.df['category'].value_counts().head(5)
            report_lines.append("Top 5 Categories by Channel Count:")
            for cat, count in cat_counts.items():
                report_lines.append(f"  {cat:30s} {count:>5,} channels")
            report_lines.append("")
        
        # Engagement metrics
        metrics = self.engagement_metrics()
        if metrics:
            report_lines.append("ENGAGEMENT METRICS")
            report_lines.append("-" * 80)
            for key, value in metrics.items():
                label = key.replace('_', ' ').title()
                report_lines.append(f"{label:40s} {value:>15,.2f}")
            report_lines.append("")
        
        # Country distribution
        if 'Country' in self.df.columns:
            report_lines.append("TOP 5 COUNTRIES")
            report_lines.append("-" * 80)
            top_countries = self.df['Country'].value_counts().head(5)
            for country, count in top_countries.items():
                pct = (count / len(self.df)) * 100
                report_lines.append(f"{country:30s} {count:>5,} channels ({pct:.1f}%)")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def export_insights(self, output_path: str):
        """Export insights to text file."""
        report = self.generate_report()
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report exported to: {output_path}")
