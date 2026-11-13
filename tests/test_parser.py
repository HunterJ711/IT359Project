from pathlib import Path
import tempfile
import unittest

from aptriage.nmap_parser import NmapParseError, parse_nmap_xml


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "samples" / "demo_scan.xml"


class NmapParserTests(unittest.TestCase):
    def test_parses_host_services_and_metadata(self):
        result = parse_nmap_xml(DEMO)

        self.assertEqual(result.scanner, "nmap")
        self.assertEqual(result.scanner_version, "7.95")
        self.assertEqual(len(result.hosts), 1)
        self.assertEqual(result.hosts[0].address, "192.168.56.101")
        self.assertEqual(result.hosts[0].hostnames, ["training-target.local"])
        self.assertEqual(result.hosts[0].os_matches, ["Linux 5.15"])
        self.assertEqual([item.port for item in result.hosts[0].services], [21, 22, 23, 80, 3306])
        self.assertEqual(result.open_service_count, 5)

    def test_ignores_closed_ports(self):
        result = parse_nmap_xml(DEMO)
        self.assertNotIn(9999, [item.port for item in result.hosts[0].services])

    def test_rejects_malformed_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.xml"
            path.write_text("<nmaprun><host>", encoding="utf-8")
            with self.assertRaises(NmapParseError):
                parse_nmap_xml(path)

    def test_rejects_non_nmap_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "other.xml"
            path.write_text("<document />", encoding="utf-8")
            with self.assertRaisesRegex(NmapParseError, "Expected an Nmap"):
                parse_nmap_xml(path)

    def test_rejects_missing_file(self):
        with self.assertRaises(NmapParseError):
            parse_nmap_xml(ROOT / "samples" / "missing.xml")


if __name__ == "__main__":
    unittest.main()

