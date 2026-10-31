"""Interactive Streamlit dashboard."""
import csv
import io
import json
import streamlit as st
from dataguard.core import audit_rows
from dataguard.report import html_report

st.set_page_config(page_title="DataGuard", page_icon="🔎", layout="wide")
st.title("🔎 DataGuard | CSV Quality Monitor")
st.caption("Audit missing values, duplicates, numeric validity, and statistical outliers. Local, transparent, no AI API key required.")
uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
if not uploaded:
    st.info("Try samples/orders.csv from the project folder.")
    st.stop()
try:
    content = uploaded.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        raise ValueError("A header row is required")
    fields = list(reader.fieldnames)
    rows = list(reader)
except (UnicodeDecodeError, ValueError, csv.Error) as exc:
    st.error(f"Unable to read CSV: {exc}")
    st.stop()
col1, col2, col3 = st.columns(3)
with col1:
    required = st.multiselect("Required columns", fields, default=fields[:1])
with col2:
    unique = st.multiselect("Unique columns", fields, default=fields[:1])
with col3:
    numeric = st.multiselect("Numeric columns", fields)
report = audit_rows(rows, required, unique, numeric)
a, b, c = st.columns(3)
a.metric("Rows", report["rows"])
b.metric("Columns", len(fields))
c.metric("Findings", report["finding_count"])
st.subheader("Quality findings")
if report["findings"]:
    st.dataframe(report["findings"], use_container_width=True, hide_index=True)
else:
    st.success("No issues detected for the selected rules.")
st.download_button("Download HTML report", html_report(report), "dataguard-report.html", "text/html")
st.download_button("Download JSON results", json.dumps(report, indent=2), "dataguard-results.json", "application/json")
st.caption("This is a rule-based quality checker, not a trained machine-learning model.")
