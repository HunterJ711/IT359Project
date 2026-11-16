import json
from pathlib import Path
import unittest

from aptriage.ai_client import SushiClient, enhance_findings
from aptriage.classifier import classify_scan
from aptriage.nmap_parser import parse_nmap_xml


ROOT = Path(__file__).resolve().parents[1]


class FakeResponse:
    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return {"choices": [{"message": {"content": self.content}}]}


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if self.error:
            raise self.error
        return self.response


class AIClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scan = parse_nmap_xml(ROOT / "samples" / "demo_scan.xml")
        cls.finding = classify_scan(scan)[0]

    def test_valid_json_enhances_only_text_fields(self):
        content = json.dumps(
            {
                "rationale": "AI explanation grounded in the supplied evidence.",
                "recommendation": "Restrict the service and validate the configuration.",
            }
        )
        session = FakeSession(FakeResponse(content))
        client = SushiClient("private-test-key", session=session)
        result = enhance_findings([self.finding], client)
        enhanced = result.findings[0]

        self.assertEqual(1, result.enhanced_count)
        self.assertEqual(self.finding.evidence, enhanced.evidence)
        self.assertEqual(self.finding.severity, enhanced.severity)
        self.assertTrue(enhanced.analysis_source.startswith("Sushi AI"))
        self.assertTrue(session.calls[0][1]["json"]["stream"] is False)
        self.assertEqual(300, session.calls[0][1]["timeout"])

    def test_request_failure_keeps_deterministic_finding(self):
        session = FakeSession(error=TimeoutError("server timed out"))
        client = SushiClient("private-test-key", session=session)
        result = enhance_findings([self.finding], client)

        self.assertEqual(0, result.enhanced_count)
        self.assertEqual(self.finding, result.findings[0])
        self.assertEqual(1, len(result.warnings))

    def test_invalid_json_keeps_deterministic_finding(self):
        client = SushiClient("private-test-key", session=FakeSession(FakeResponse("not json")))
        result = enhance_findings([self.finding], client)

        self.assertEqual(0, result.enhanced_count)
        self.assertEqual(self.finding, result.findings[0])


if __name__ == "__main__":
    unittest.main()
