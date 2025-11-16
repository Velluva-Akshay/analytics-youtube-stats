"""
Example usage demonstrating all features of the YouTube Analytics toolkit.

Run this script to see a complete analysis workflow with all modules.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.load_data import load_csv, summarize, basic_cleaning
from src.eda import run_basic_eda
from src.analysis import YouTubeAnalyzer
from src.validation import DataValidator
from src.config import get_config
import logging


def main():
    """Run complete analysis workflow."""
    
    # Initialize configuration
    config = get_config()
    logging.info("Starting YouTube Statistics Analysis")
    
    print("=" * 80)
    print("YOUTUBE STATISTICS ANALYTICS - COMPLETE WORKFLOW DEMO")
    print("=" * 80)
    print()
    
    # Step 1: Load data
    print("📂 Step 1: Loading data...")
    csv_path = Path("../Global YouTube Statistics.csv")
    
    try:
        df = load_csv(csv_path)
        print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return 1
    
    print()
    
    # Step 2: Data summary
    print("📊 Step 2: Data summary...")
    summary_info = summarize(df)
    print(f"Shape: {summary_info['shape']}")
    print(f"Columns: {len(summary_info['columns'])}")
    missing_total = summary_info['missing_counts'].sum()
    print(f"Total missing values: {missing_total:,}")
    print()
    
    # Step 3: Data validation
    print("✅ Step 3: Running data quality checks...")
    validator = DataValidator(df)
    
    # Run individual checks
    missing_check = validator.check_missing_values(threshold=0.5)
    dup_check = validator.check_duplicates()
    
    print(f"Missing values check: {'✅ PASSED' if missing_check.passed else '❌ FAILED'}")
    if missing_check.issues:
        for issue in missing_check.issues[:3]:
            print(f"  - {issue}")
    
    print(f"Duplicates found: {dup_check.stats['n_duplicates']}")
    print()
    
    # Generate quality report
    quality_report_path = Path("outputs/quality_report.txt")
    quality_report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(quality_report_path, 'w', encoding='utf-8') as f:
        f.write(validator.generate_quality_report())
    print(f"📄 Quality report saved to: {quality_report_path}")
    print()
    
    # Step 4: Data cleaning
    print("🧹 Step 4: Cleaning data...")
    df_clean = basic_cleaning(df)
    rows_removed = len(df) - len(df_clean)
    print(f"Removed {rows_removed} duplicate rows")
    print(f"Clean dataset: {len(df_clean):,} rows")
    print()
    
    # Step 5: Advanced analysis
    print("🔬 Step 5: Running advanced analysis...")
    analyzer = YouTubeAnalyzer(df_clean)
    
    # Top performers
    top5_subs = analyzer.get_top_performers('subscribers', n=5)
    print("\nTop 5 channels by subscribers:")
    for idx, (_, row) in enumerate(top5_subs.iterrows(), 1):
        print(f"  {idx}. {row['Youtuber']}: {row['subscribers']:,.0f}")
    
    # Engagement metrics
    metrics = analyzer.engagement_metrics()
    print("\nEngagement metrics:")
    for key, value in list(metrics.items())[:3]:
        print(f"  {key}: {value:,.2f}")
    
    # Generate and save analysis report
    report_path = Path("outputs/analysis_report.txt")
    analyzer.export_insights(str(report_path))
    print(f"\n📄 Analysis report saved to: {report_path}")
    print()
    
    # Step 6: Generate visualizations
    print("📈 Step 6: Generating visualizations...")
    try:
        run_basic_eda(csv_path, output_dir="outputs")
        print("✅ All visualizations generated successfully")
        print("   Check the outputs/ directory for PNG files")
    except Exception as e:
        print(f"⚠️  Some visualizations may have failed: {e}")
    print()
    
    # Summary
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated outputs:")
    print("  • outputs/quality_report.txt - Data quality assessment")
    print("  • outputs/analysis_report.txt - Statistical insights")
    print("  • outputs/*.png - 11 visualizations")
    print("\nNext steps:")
    print("  • Review the quality and analysis reports")
    print("  • Examine visualizations in the outputs/ directory")
    print("  • Run specific analyses using the CLI: python -m src.cli --help")
    print("  • Explore interactively in notebooks/EDA.ipynb")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
