# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-16

### Added
- **Core Features**
  - CSV data loader with encoding fallback support
  - Data cleaning and preprocessing utilities
  - Comprehensive EDA script generating 11 visualizations
  - Interactive Jupyter notebook for exploration

- **Advanced Analysis**
  - `YouTubeAnalyzer` class for statistical insights
  - Category and country analysis
  - Engagement metrics calculation
  - Outlier detection (IQR and Z-score methods)
  - Automated report generation

- **Data Validation**
  - `DataValidator` class for quality checks
  - Missing value detection
  - Duplicate row identification
  - Data type validation
  - Value range checks
  - Quality report generation

- **Configuration System**
  - YAML-based configuration
  - Customizable visualization settings
  - Logging configuration
  - Output format options

- **Command-Line Interface**
  - `analyze` command for full EDA workflow
  - `summary` command for dataset overview
  - `clean` command for data cleaning
  - Flexible output options

- **Testing Infrastructure**
  - pytest test suite with 9+ tests
  - Tests for all major modules
  - Sample data fixtures
  - 80%+ code coverage

- **Documentation**
  - Comprehensive README with badges
  - Setup and usage instructions
  - CLI examples
  - Contributing guidelines
  - MIT License

- **CI/CD**
  - GitHub Actions workflow for automated testing
  - Python 3.13 support

### Visualizations Generated
1. Category distribution bar chart
2. Subscriber count histogram (log scale)
3. Top 20 channels by subscribers
4. Subscribers vs video views scatter plot (log-log)
5. Feature correlation heatmap
6. Top countries bar chart
7. Upload count distribution
8. Median subscribers by category
9. Subscriber boxplot by category (log scale)
10. Top 20 channels by video views
11. Channel creation timeline

### Technical Details
- Python 3.13 support
- Dependencies: pandas, matplotlib, seaborn, pyyaml, pytest, numpy
- Robust error handling and logging
- Configurable output formats (PNG, SVG, PDF)
- Modular architecture for extensibility

## [0.1.0] - 2025-11-16

### Added
- Initial project scaffold
- Basic CSV loader
- Simple EDA notebook
- README with quick start guide
