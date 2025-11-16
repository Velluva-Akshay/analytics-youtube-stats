"""
Data validation and quality checks module.

Provides utilities to validate data quality, detect issues,
and generate quality reports.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Container for validation results."""
    passed: bool
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


class DataValidator:
    """Validate YouTube statistics data quality."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize validator with dataframe."""
        self.df = df
        self.results = ValidationResult(passed=True)
    
    def check_missing_values(self, threshold: float = 0.5) -> ValidationResult:
        """Check for excessive missing values."""
        result = ValidationResult(passed=True)
        
        missing_pct = (self.df.isnull().sum() / len(self.df))
        high_missing = missing_pct[missing_pct > threshold]
        
        if len(high_missing) > 0:
            result.passed = False
            result.issues.append(f"Found {len(high_missing)} columns with >{threshold*100}% missing values")
            for col, pct in high_missing.items():
                result.issues.append(f"  - {col}: {pct*100:.1f}% missing")
        
        result.stats['total_missing'] = self.df.isnull().sum().sum()
        result.stats['columns_with_missing'] = (missing_pct > 0).sum()
        
        return result
    
    def check_duplicates(self) -> ValidationResult:
        """Check for duplicate rows."""
        result = ValidationResult(passed=True)
        
        n_duplicates = self.df.duplicated().sum()
        
        if n_duplicates > 0:
            result.warnings.append(f"Found {n_duplicates} duplicate rows ({n_duplicates/len(self.df)*100:.1f}%)")
        
        result.stats['n_duplicates'] = n_duplicates
        
        return result
    
    def check_data_types(self, expected_types: Dict[str, str] = None) -> ValidationResult:
        """Validate data types of columns."""
        result = ValidationResult(passed=True)
        
        if expected_types:
            for col, expected_type in expected_types.items():
                if col in self.df.columns:
                    actual_type = str(self.df[col].dtype)
                    if expected_type not in actual_type:
                        result.issues.append(f"Column '{col}' has type '{actual_type}', expected '{expected_type}'")
                        result.passed = False
        
        # Check for object columns that could be numeric
        for col in self.df.select_dtypes(include='object').columns:
            # Try to convert to numeric
            try:
                numeric_vals = pd.to_numeric(self.df[col], errors='coerce')
                non_null_pct = numeric_vals.notna().sum() / len(self.df)
                
                if non_null_pct > 0.9:  # If >90% can be converted
                    result.warnings.append(f"Column '{col}' is object type but could be numeric ({non_null_pct*100:.1f}% convertible)")
            except:
                pass
        
        return result
    
    def check_value_ranges(self, ranges: Dict[str, Tuple[float, float]] = None) -> ValidationResult:
        """Check if numeric values are within expected ranges."""
        result = ValidationResult(passed=True)
        
        if ranges:
            for col, (min_val, max_val) in ranges.items():
                if col in self.df.columns:
                    out_of_range = ((self.df[col] < min_val) | (self.df[col] > max_val)).sum()
                    if out_of_range > 0:
                        result.warnings.append(f"Column '{col}' has {out_of_range} values outside range [{min_val}, {max_val}]")
        
        # Check for negative values in columns that should be positive
        positive_cols = ['subscribers', 'video views', 'uploads']
        for col in positive_cols:
            if col in self.df.columns:
                negative = (self.df[col] < 0).sum()
                if negative > 0:
                    result.issues.append(f"Column '{col}' has {negative} negative values")
                    result.passed = False
        
        return result
    
    def check_required_columns(self, required: List[str]) -> ValidationResult:
        """Check if required columns are present."""
        result = ValidationResult(passed=True)
        
        missing = set(required) - set(self.df.columns)
        
        if missing:
            result.passed = False
            result.issues.append(f"Missing required columns: {', '.join(missing)}")
        
        return result
    
    def validate_all(self, 
                     required_cols: List[str] = None,
                     expected_types: Dict[str, str] = None,
                     value_ranges: Dict[str, Tuple[float, float]] = None,
                     missing_threshold: float = 0.5) -> ValidationResult:
        """Run all validation checks."""
        all_results = []
        
        # Required columns
        if required_cols:
            all_results.append(self.check_required_columns(required_cols))
        
        # Missing values
        all_results.append(self.check_missing_values(missing_threshold))
        
        # Duplicates
        all_results.append(self.check_duplicates())
        
        # Data types
        all_results.append(self.check_data_types(expected_types))
        
        # Value ranges
        all_results.append(self.check_value_ranges(value_ranges))
        
        # Aggregate results
        final_result = ValidationResult(passed=True)
        
        for res in all_results:
            if not res.passed:
                final_result.passed = False
            final_result.issues.extend(res.issues)
            final_result.warnings.extend(res.warnings)
            final_result.stats.update(res.stats)
        
        return final_result
    
    def generate_quality_report(self) -> str:
        """Generate a data quality report."""
        lines = []
        lines.append("=" * 80)
        lines.append("DATA QUALITY REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Basic stats
        lines.append("DATASET OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"Rows: {len(self.df):,}")
        lines.append(f"Columns: {len(self.df.columns)}")
        lines.append(f"Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        lines.append("")
        
        # Missing values
        lines.append("MISSING VALUES")
        lines.append("-" * 80)
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            for col, count in missing[missing > 0].items():
                pct = (count / len(self.df)) * 100
                lines.append(f"{col:30s} {count:>8,} ({pct:>6.2f}%)")
        else:
            lines.append("No missing values detected")
        lines.append("")
        
        # Duplicates
        n_dup = self.df.duplicated().sum()
        lines.append("DUPLICATES")
        lines.append("-" * 80)
        lines.append(f"Duplicate rows: {n_dup:,} ({n_dup/len(self.df)*100:.2f}%)")
        lines.append("")
        
        # Data types
        lines.append("DATA TYPES")
        lines.append("-" * 80)
        dtype_counts = self.df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            lines.append(f"{str(dtype):20s} {count:>3} columns")
        lines.append("")
        
        # Numeric column stats
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            lines.append("NUMERIC COLUMN STATISTICS")
            lines.append("-" * 80)
            lines.append(f"{'Column':<30} {'Min':>12} {'Max':>12} {'Mean':>12} {'Std':>12}")
            lines.append("-" * 80)
            for col in numeric_cols[:10]:  # Show first 10
                stats = self.df[col].describe()
                lines.append(f"{col:<30} {stats['min']:>12,.0f} {stats['max']:>12,.0f} {stats['mean']:>12,.0f} {stats['std']:>12,.0f}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
