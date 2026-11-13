from pathlib import Path
import unittest

from aptriage.classifier import classify_scan
from aptriage.nmap_parser import parse_nmap_xml


ROOT = Path(__file__).resolve().parents[1]


class ClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = classify_scan(parse_nmap_xml(ROOT / "samples" / "demo_scan.xml"))

    def test_produces_one_finding_per_open_service(self):
        self.assertEqual(len(self.findings), 5)

    def test_telnet_is_high(self):
        finding = next(item for item in self.findings if item.port == 23)
        self.assertEqual(finding.rule_id, "INSECURE_TELNET")
        self.assertEqual(finding.severity, "High")

    def test_database_is_medium_and_does_not_claim_vulnerability(self):
        finding = next(item for item in self.findings if item.port == 3306)
        self.assertEqual(finding.rule_id, "EXPOSED_DATABASE")
        self.assertEqual(finding.severity, "Medium")
        self.assertIn("does not prove", finding.rationale)

    def test_findings_are_sorted_by_severity(self):
        self.assertEqual(self.findings[0].severity, "High")


if __name__ == "__main__":
    unittest.main()

