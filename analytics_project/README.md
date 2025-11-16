# Analytics project — Global YouTube Statistics

[![Python Tests](https://github.com/Velluva-Akshay/analytics-youtube-stats/actions/workflows/python-tests.yml/badge.svg)](https://github.com/Velluva-Akshay/analytics-youtube-stats/actions/workflows/python-tests.yml)

A data analytics project analyzing the Global YouTube Statistics dataset (995 channels, 28 features). Includes EDA visualizations, data cleaning utilities, and automated testing.

## Features

- 📊 **Comprehensive EDA**: 11 publication-ready visualizations covering distributions, correlations, and top channels
- 🧹 **Data Cleaning**: Robust CSV loader with encoding fallbacks and cleaning utilities
- ✅ **Tested**: pytest suite with 3 passing tests
- 📓 **Interactive Notebook**: Jupyter notebook for exploratory analysis
- 🔄 **CI/CD**: GitHub Actions workflow running tests on every push

## Structure

```
analytics_project/
├── src/              # Core Python modules
│   ├── load_data.py  # CSV loader, summarizer, cleaning functions
│   ├── eda.py        # EDA script generating 11 visualizations
│   └── test_load.py  # Quick verification script
├── tests/            # pytest test suite
├── notebooks/        # Jupyter notebooks for exploration
├── outputs/          # Generated visualizations (11 PNG files)
└── requirements.txt  # Python dependencies
```

## Dataset

The project analyzes `Global YouTube Statistics.csv` containing:
- 995 YouTube channels
- 28 features: subscribers, video views, category, country, uploads, channel type, etc.
- Top channels include T-Series, YouTube Movies, MrBeast, Cocomelon

## Quick start (Windows / PowerShell)

### 1. Clone and setup

```powershell
git clone https://github.com/Velluva-Akshay/analytics-youtube-stats.git
cd analytics-youtube-stats
python -m venv analytics_project\.venv
.\analytics_project\.venv\Scripts\Activate.ps1
pip install -r analytics_project\requirements.txt
```

### 2. Run EDA script (generates 11 PNG visualizations)

```powershell
cd analytics_project
python src\eda.py
# Output: 11 PNG files saved to outputs/
```

### 3. Run tests

```powershell
cd analytics_project
pytest tests\ -v
# Expected: 3 passed
```

### 4. Explore interactively

```powershell
cd analytics_project
jupyter notebook notebooks\EDA.ipynb
```

## Visualizations Generated

The EDA script produces 11 visualizations:
1. **top_categories.png** - Distribution of channels by category
2. **subscribers_dist.png** - Subscriber count distribution (log scale)
3. **top20_by_subscribers.png** - Top 20 channels by subscribers
4. **subs_vs_video_views_scatter.png** - Correlation scatter plot (log-log)
5. **correlation_heatmap.png** - Feature correlation matrix
6. **top_countries.png** - Channels by country
7. **uploads_distribution.png** - Upload count distribution
8. **median_subs_by_category.png** - Median subscribers per category
9. **subs_boxplot_by_category.png** - Subscriber distribution by category (log)
10. **top20_by_video_views.png** - Top 20 channels by video views
11. **created_year_counts.png** - Channel creation timeline

## Testing

```powershell
cd analytics_project
pytest tests\ -v
```

**Test coverage:**
- `test_load_data.py` - CSV loading and data summary
- `test_cleaning.py` - Data cleaning and type conversion

## License

MIT License - see [LICENSE](../LICENSE) file

## Contributing

Pull requests welcome! Please ensure tests pass before submitting.

---

**Note**: Requires `Global YouTube Statistics.csv` at workspace root. The project uses pandas, matplotlib, seaborn, and pytest.
