"""Optional, fail-safe AI enhancement through the ISU Sushi server."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from typing import Any

from .models import Finding


DEFAULT_BASE_URL = "http://sushi.it.ilstu.edu:8080"
DEFAULT_MODEL = "llama3.1:latest"


class AIEnhancementError(RuntimeError):
    """Raised when Sushi cannot return a usable enhancement."""


@dataclass(slots=True)
class AIEnhancementResult:
    findings: list[Finding]
    enhanced_count: int
    warnings: list[str]
    model: str


class SushiClient:
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 300,
        session: Any = None,
    ) -> None:
        if not api_key.strip():
            raise ValueError("SUSHI_API_KEY is missing")
        self.api_key = api_key.strip()
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        if session is None:
            try:
                import requests
            except ImportError as exc:
                raise ValueError("AI mode requires the 'requests' package") from exc
            session = requests
        self.session = session

    def enhance(self, finding: Finding) -> tuple[str, str]:
        system_prompt = (
            "You assist with an authorized penetration-testing report. Use only the supplied "
            "facts. Do not invent vulnerabilities, exploitation, credentials, CVEs, or scan "
            "results. Do not change severity or evidence. Return only valid JSON with exactly "
            "two string fields: rationale and recommendation. Keep each under 90 words."
        )
        finding_data = {
            "rule_id": finding.rule_id,
            "title": finding.title,
            "severity": finding.severity,
            "host": finding.host,
            "port": finding.port,
            "protocol": finding.protocol,
            "service": finding.service,
            "evidence": finding.evidence,
            "existing_rationale": finding.rationale,
            "existing_recommendation": finding.recommendation,
        }
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(finding_data)},
            ],
        }
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        except Exception as exc:
            raise AIEnhancementError(f"Sushi request failed: {exc}") from exc

        try:
            parsed = json.loads(_strip_code_fence(str(content)))
            rationale = parsed["rationale"].strip()
            recommendation = parsed["recommendation"].strip()
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as exc:
            raise AIEnhancementError("Sushi returned invalid structured output") from exc
        if not rationale or not recommendation:
            raise AIEnhancementError("Sushi returned an empty enhancement")
        return rationale, recommendation


def _strip_code_fence(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def enhance_findings(findings: list[Finding], client: SushiClient) -> AIEnhancementResult:
    enhanced: list[Finding] = []
    warnings: list[str] = []
    enhanced_count = 0
    for finding in findings:
        try:
            rationale, recommendation = client.enhance(finding)
            enhanced.append(
                replace(
                    finding,
                    rationale=rationale,
                    recommendation=recommendation,
                    analysis_source=(
                        f"Sushi AI enhancement ({client.model}); severity and evidence retained "
                        "from deterministic rule"
                    ),
                )
            )
            enhanced_count += 1
        except AIEnhancementError as exc:
            warnings.append(f"{finding.rule_id} on {finding.host}:{finding.port}: {exc}")
            enhanced.append(finding)
    return AIEnhancementResult(enhanced, enhanced_count, warnings, client.model)
