# DataGuard — CSV Quality Monitor

A lightweight, GitHub-ready Python project for auditing CSV files. Find missing required fields, duplicate IDs, invalid numeric values, and potential outliers using IQR fences. Includes a Streamlit dashboard, CLI, safe self-contained HTML reports, JSON export, sample data, and unit tests.

**No API key or database required.** The core engine uses only Python's standard library. This is a transparent rule-based data-quality utility, **not a trained AI model**.

## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Open http://localhost:8501. Upload `samples/orders.csv`, select `order_id` as **Unique**, `customer_id` as **Required**, and `amount` as **Numeric**.

## CLI (works without installing dependencies)

```bash
python -m dataguard.cli samples/orders.csv --required customer_id --unique order_id --numeric amount --html report.html --json report.json
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Structure

```
dataguard/
  core.py          # detection rules
  report.py        # safe HTML formatting
  cli.py           # CLI
  __init__.py
dashboard.py       # Streamlit UI
samples/orders.csv # intentionally flawed demo dataset
tests/             # unit tests
.github/workflows/ # CI
```

## Method and limitations

- **Required:** reports blank or missing cells for selected fields.
- **Unique:** reports repeated nonblank values in selected columns.
- **Numeric:** reports values that cannot be parsed as finite floating-point numbers.
- **Outlier:** uses a 1.5 × IQR rule when at least eight finite numeric observations exist and the IQR is nonzero. Outliers may be valid.
- Row numbers refer to CSV rows with the header as row 1.
- The rules selected by the user determine the output; unselected fields are not checked.
- Designed for small and medium local CSV files, not streaming or huge datasets.
- Avoid uploading confidential data to public deployments of the dashboard.

## GitHub repository

Suggested name: `DataGuard-CSV`.

Suggested description: `Python CSV quality monitor with duplicate detection, missing-value checks, outlier analysis, Streamlit dashboard, and HTML/JSON reports.`

License: MIT.
