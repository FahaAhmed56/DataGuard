"""CSV quality checks using only the Python standard library."""
import csv
import math
import statistics
from collections import Counter
from pathlib import Path


def _blank(value):
    return value is None or not str(value).strip()


def audit_rows(rows, required=None, unique=None, numeric=None):
    """Return an explainable summary and findings for a list of dict records."""
    required, unique, numeric = required or [], unique or [], numeric or []
    columns = list(dict.fromkeys(k for r in rows for k in r))
    for field in required + unique + numeric:
        if field not in columns:
            columns.append(field)
    findings = []
    n = len(rows)
    for field in required:
        for i, row in enumerate(rows, 2):
            if _blank(row.get(field)):
                findings.append(dict(row=i, field=field, rule="required", severity="high", message="Required value is missing"))
    for field in unique:
        seen = {}
        for i, row in enumerate(rows, 2):
            val = str(row.get(field, "")).strip()
            if not val:
                continue
            if val in seen:
                findings.append(dict(row=i, field=field, rule="unique", severity="high", message=f"Duplicate value (first seen at CSV row {seen[val]})"))
            else:
                seen[val] = i
    for field in numeric:
        samples = []
        for i, row in enumerate(rows, 2):
            val = row.get(field)
            if _blank(val):
                continue
            try:
                number = float(val)
                if not math.isfinite(number):
                    raise ValueError("Non-finite number")
                samples.append((i, number))
            except (ValueError, TypeError):
                findings.append(dict(row=i, field=field, rule="numeric", severity="medium", message="Expected a finite number"))
        # Tukey fences, only when a column has sufficient spread and sample count.
        if len(samples) >= 8:
            values = sorted(v for _, v in samples)
            mid = len(values) // 2
            lower = values[:mid]
            upper = values[mid:] if len(values) % 2 == 0 else values[mid + 1:]
            q1, q3 = statistics.median(lower), statistics.median(upper)
            iqr = q3 - q1
            if iqr > 0:
                low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                for i, value in samples:
                    if value < low or value > high:
                        findings.append(dict(row=i, field=field, rule="outlier", severity="low", message=f"Potential outlier: {value:g} (IQR range {low:g}–{high:g})"))
    counts = Counter(f["rule"] for f in findings)
    return {"rows": n, "columns": columns, "finding_count": len(findings), "rules": dict(counts), "findings": sorted(findings, key=lambda x: (x["row"], x["field"], x["rule"]))}


def audit_csv(path, required=None, unique=None, numeric=None):
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header")
        rows = list(reader)
    return audit_rows(rows, required, unique, numeric)
