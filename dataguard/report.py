"""Export audit summaries as self-contained safe HTML."""
from html import escape


def html_report(report):
    trs = "".join("<tr>" + "".join(f"<td>{escape(str(f[k]))}</td>" for k in ("row", "field", "rule", "severity", "message")) + "</tr>" for f in report["findings"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DataGuard Audit</title><style>body{{font:16px system-ui;margin:3rem auto;max-width:1050px;padding:0 1rem;color:#162338}}h1{{color:#176a7d}}.metrics{{display:flex;gap:2rem;padding:1rem;background:#eff8fb;border-radius:12px}}table{{width:100%;border-collapse:collapse;margin-top:1rem}}th,td{{padding:.75rem;text-align:left;border-bottom:1px solid #ddd}}th{{background:#e5f2f6}}tr:hover{{background:#f6fafb}}</style></head><body><h1>DataGuard · Quality Audit</h1><div class="metrics"><div><b>Rows</b><p>{report['rows']}</p></div><div><b>Columns</b><p>{len(report['columns'])}</p></div><div><b>Findings</b><p>{report['finding_count']}</p></div></div><h2>Findings</h2><table><thead><tr><th>CSV row</th><th>Field</th><th>Rule</th><th>Severity</th><th>Explanation</th></tr></thead><tbody>{trs}</tbody></table><p>Outliers are statistical indicators, not proven errors. Row numbers include the header.</p></body></html>'''
