import tempfile
import unittest
from pathlib import Path
from dataguard.core import audit_rows, audit_csv
from dataguard.report import html_report

class TestDataGuard(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(audit_rows([])["finding_count"], 0)

    def test_required_missing(self):
        result = audit_rows([{"id": ""}], required=["id"])
        self.assertEqual(result["rules"]["required"], 1)

    def test_duplicate(self):
        result = audit_rows([{"id": "1"}, {"id": "1"}], unique=["id"])
        self.assertEqual(result["findings"][0]["row"], 3)

    def test_numeric_invalid(self):
        result = audit_rows([{"amount": "oops"}], numeric=["amount"])
        self.assertEqual(result["rules"]["numeric"], 1)

    def test_nonfinite(self):
        result = audit_rows([{"amount": "nan"}], numeric=["amount"])
        self.assertEqual(result["rules"]["numeric"], 1)

    def test_outlier(self):
        values = [10, 11, 11, 12, 12, 13, 13, 14, 15, 500]
        result = audit_rows([{"amount": str(v)} for v in values], numeric=["amount"])
        self.assertIn("outlier", result["rules"])

    def test_html_escaped(self):
        result = audit_rows([{"<script>": ""}], required=["<script>"])
        html = html_report(result)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_csv_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.csv"
            path.write_text("id,amount\n1,9\n2,11\n", encoding="utf-8")
            self.assertEqual(audit_csv(path, numeric=["amount"])["rows"], 2)

    def test_no_header(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit_csv(path)

if __name__ == "__main__":
    unittest.main()
