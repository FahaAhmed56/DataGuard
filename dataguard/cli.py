"""CLI: python -m dataguard.cli samples/orders.csv --required customer_id ..."""
import argparse
import json
from pathlib import Path
from .core import audit_csv
from .report import html_report


def main():
    parser = argparse.ArgumentParser(description="Audit CSV data quality")
    parser.add_argument("csv_file")
    parser.add_argument("--required", nargs="*", default=[])
    parser.add_argument("--unique", nargs="*", default=[])
    parser.add_argument("--numeric", nargs="*", default=[])
    parser.add_argument("--html", help="Write HTML findings report")
    parser.add_argument("--json", help="Write machine-readable JSON results")
    args = parser.parse_args()
    result = audit_csv(args.csv_file, args.required, args.unique, args.numeric)
    if args.html:
        Path(args.html).write_text(html_report(result), encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Audited {result['rows']} records; detected {result['finding_count']} findings")
    for rule, count in sorted(result["rules"].items()):
        print(f"  {rule}: {count}")


if __name__ == "__main__":
    main()
