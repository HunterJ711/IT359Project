from pathlib import Path
import unittest

from aptriage.classifier import classify_scan
from aptriage.nmap_parser import parse_nmap_xml
from aptriage.report_generator import render_markdown_report


ROOT = Path(__file__).resolve().parents[1]


class ReportTests(unittest.TestCase):
    def test_report_contains_evidence_findings_and_limitations(self):
        scan = parse_nmap_xml(ROOT / "samples" / "demo_scan.xml")
        report = render_markdown_report(scan, classify_scan(scan))

        self.assertIn("# APTriage Penetration Testing Analysis", report)
        self.assertIn("192.168.56.101", report)
        self.assertIn("Telnet service exposed", report)
        self.assertIn("Deterministic APTriage rule", report)
        self.assertIn("AI enhancement was not enabled", report)
        self.assertIn("does not prove exploitation", report)


if __name__ == "__main__":
    unittest.main()

