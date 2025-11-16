# Analytics project — Global YouTube Statistics

This small data analytics project demonstrates how to load and explore the `Global YouTube Statistics.csv` dataset.

Structure
- notebooks/ - Jupyter notebook with exploratory data analysis (EDA)
- src/ - helper scripts: `load_data.py`, `eda.py`, `test_load.py`
- data/ - (not required) the original CSV is in the workspace root: `Global YouTube Statistics.csv`

Quick start (Windows / PowerShell):

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r analytics_project\requirements.txt
```

2. Run a quick load test:

```powershell
python analytics_project\src\test_load.py
```

3. Open `analytics_project\notebooks\EDA.ipynb` in Jupyter / VS Code to run the interactive notebook.

Notes
- The project scripts expect the CSV at the workspace root `Global YouTube Statistics.csv`. You can pass an absolute path to the scripts if you moved the file.
- Follow-up suggestions: add unit tests, more visualizations, and parameterize scripts for reproducible outputs.
