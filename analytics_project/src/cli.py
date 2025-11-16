"""
Command-line interface for YouTube Statistics Analytics.

Provides a user-friendly CLI for running analysis, generating reports,
and managing data processing workflows.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from src.load_data import load_csv, summarize, basic_cleaning
from src.eda import run_basic_eda


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="YouTube Statistics Analytics Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full EDA and generate all visualizations
  python -m src.cli analyze --csv "../Global YouTube Statistics.csv"
  
  # Generate specific visualizations
  python -m src.cli analyze --csv data.csv --output custom_output/
  
  # Show dataset summary
  python -m src.cli summary --csv data.csv
  
  # Clean and export data
  python -m src.cli clean --csv data.csv --output cleaned_data.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Run full EDA and generate visualizations')
    analyze_parser.add_argument('--csv', required=True, help='Path to the CSV file')
    analyze_parser.add_argument('--output', default='outputs', help='Output directory for visualizations (default: outputs)')
    analyze_parser.add_argument('--format', choices=['png', 'svg', 'pdf'], default='png', help='Output format for plots')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Display dataset summary statistics')
    summary_parser.add_argument('--csv', required=True, help='Path to the CSV file')
    summary_parser.add_argument('--verbose', action='store_true', help='Show detailed summary')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean dataset and export')
    clean_parser.add_argument('--csv', required=True, help='Path to the CSV file')
    clean_parser.add_argument('--output', required=True, help='Output path for cleaned CSV')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'analyze':
            return cmd_analyze(args)
        elif args.command == 'summary':
            return cmd_summary(args)
        elif args.command == 'clean':
            return cmd_clean(args)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_analyze(args) -> int:
    """Execute analyze command."""
    print(f"📊 Analyzing: {args.csv}")
    print(f"📁 Output directory: {args.output}")
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run EDA
    run_basic_eda(args.csv, output_dir=str(output_path))
    
    print(f"✅ Analysis complete! Visualizations saved to {args.output}/")
    return 0


def cmd_summary(args) -> int:
    """Execute summary command."""
    print(f"📊 Loading: {args.csv}")
    
    df = load_csv(args.csv)
    summary = summarize(df)
    
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Shape: {summary['shape'][0]} rows × {summary['shape'][1]} columns")
    print(f"\nColumns ({len(summary['columns'])}):")
    for col in summary['columns']:
        print(f"  • {col}")
    
    if args.verbose:
        print("\nData Types:")
        for col, dtype in summary['dtypes'].items():
            print(f"  {col}: {dtype}")
        
        print("\nMissing Values:")
        missing = summary['missing_counts']
        if missing.sum() > 0:
            for col, count in missing[missing > 0].items():
                pct = (count / summary['shape'][0]) * 100
                print(f"  {col}: {count} ({pct:.1f}%)")
        else:
            print("  No missing values")
    
    print("\nFirst 3 rows:")
    print(df.head(3).to_string())
    print("="*60)
    
    return 0


def cmd_clean(args) -> int:
    """Execute clean command."""
    print(f"🧹 Cleaning: {args.csv}")
    
    df = load_csv(args.csv)
    original_shape = df.shape
    
    df_clean = basic_cleaning(df)
    
    print(f"Original: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"Cleaned: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
    print(f"Removed: {original_shape[0] - df_clean.shape[0]} rows")
    
    # Save cleaned data
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    
    print(f"✅ Cleaned data saved to: {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
