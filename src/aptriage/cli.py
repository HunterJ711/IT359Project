"""Command-line interface for APTriage."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

from .classifier import classify_scan
from .nmap_parser import NmapParseError, parse_nmap_xml
from .report_generator import render_markdown_report
from .AI_Enhance import *


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
    return parser


def _run_analyze(input_path: Path, output_path: Path) -> int:
    try:
        scan = parse_nmap_xml(input_path)
    except NmapParseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    findings = classify_scan(scan)
    findings = AI_Enhancement(findings)
    report = render_markdown_report(scan, findings)
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
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        return _run_analyze(args.input, args.output)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

