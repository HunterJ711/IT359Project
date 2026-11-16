"""Command-line interface for APTriage."""

from __future__ import annotations

import argparse
from collections import Counter
import os
from pathlib import Path
import sys

from .ai_client import DEFAULT_BASE_URL, DEFAULT_MODEL, SushiClient, enhance_findings
from .classifier import classify_scan
from .nmap_parser import NmapParseError, parse_nmap_xml
from .report_generator import render_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aptriage",
        description="Analyze authorized Nmap XML and generate a triage report.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="analyze an Nmap XML file")
    analyze.add_argument("input", type=Path, help="path to Nmap XML")
    analyze.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("reports/aptriage-report.md"),
        help="Markdown report destination (default: reports/aptriage-report.md)",
    )
    analyze.add_argument(
        "--ai",
        action="store_true",
        help="optionally enhance explanations through the ISU Sushi server",
    )
    analyze.add_argument(
        "--ai-model",
        default=os.environ.get("SUSHI_MODEL", DEFAULT_MODEL),
        help=f"Sushi model name (default: {DEFAULT_MODEL})",
    )
    return parser


def _run_analyze(
    input_path: Path,
    output_path: Path,
    *,
    use_ai: bool = False,
    ai_model: str = DEFAULT_MODEL,
) -> int:
    try:
        scan = parse_nmap_xml(input_path)
    except NmapParseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    findings = classify_scan(scan)
    ai_warnings: list[str] = []
    if use_ai:
        api_key = os.environ.get("SUSHI_API_KEY", "")
        if not api_key:
            ai_warnings.append(
                "SUSHI_API_KEY was not set; all findings used deterministic fallback guidance."
            )
        else:
            client = SushiClient(
                api_key=api_key,
                model=ai_model,
                base_url=os.environ.get("SUSHI_BASE_URL", DEFAULT_BASE_URL),
            )
            result = enhance_findings(findings, client)
            findings = result.findings
            ai_warnings.extend(result.warnings)
    report = render_markdown_report(
        scan,
        findings,
        ai_requested=use_ai,
        ai_model=ai_model,
        ai_warnings=ai_warnings,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    counts = Counter(item.severity for item in findings)
    print("APTriage analysis complete")
    print(f"Hosts: {len(scan.hosts)}")
    print(f"Open services: {scan.open_service_count}")
    print(
        "Findings: "
        f"{len(findings)} (High: {counts['High']}, Medium: {counts['Medium']}, Low: {counts['Low']})"
    )
    print(f"Report: {output_path.resolve()}")
    if ai_warnings:
        print(f"AI fallback notes: {len(ai_warnings)} (see report)")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        return _run_analyze(
            args.input,
            args.output,
            use_ai=args.ai,
            ai_model=args.ai_model,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

