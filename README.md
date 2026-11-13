# APTriage

APTriage is a Python-based penetration-testing support tool that converts authorized Nmap XML output into structured, explainable findings and a readable Markdown report.

The project separates three kinds of information:

1. **Scan evidence** — host, port, service, and version information reported by Nmap.
2. **Deterministic analysis** — transparent APTriage rules that assign severity and explain why a service deserves review.
3. **AI-assisted analysis** — an optional enhancement layer planned for the next milestone. It will never replace or modify the original evidence.

> **Authorized use only:** Use APTriage only with scans of systems you own or have explicit permission to test. An open port does not by itself prove a vulnerability.

## Current Status

Version `0.1.0` implements the complete offline foundation:

- Nmap XML validation and parsing
- Host, hostname, OS, port, service, and version extraction
- Transparent Low/Medium/High classification rules
- Evidence-based remediation guidance
- Markdown report generation
- Command-line interface
- Synthetic demonstration data
- Automated parser, classifier, and report tests

Optional AI integration and HTML output are planned for the next milestone.

## Requirements

- Python 3.10 or newer
- Nmap only if producing a new authorized scan
- Git for source control

The offline application currently uses only the Python standard library.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd aptriage
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install APTriage in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

For development tests:

```bash
python -m pip install -r requirements-dev.txt
```

## Quick Start

Analyze the included synthetic scan:

```bash
aptriage analyze samples/demo_scan.xml --output reports/demo-report.md
```

The equivalent module command is:

```bash
python -m aptriage analyze samples/demo_scan.xml --output reports/demo-report.md
```

APTriage prints a terminal summary and writes the full Markdown report to the requested path.

## Creating an Authorized Nmap XML File

Run Nmap only against an authorized lab target:

```bash
nmap -sV -O -oX authorized_scan.xml 192.168.56.101
```

Then analyze it:

```bash
aptriage analyze authorized_scan.xml --output reports/authorized-report.md
```

APTriage does not need root access to read an existing XML file. Some Nmap scan options, including reliable OS detection, may require elevated privileges.

## How It Works

```text
Nmap XML
    |
    v
Validation and parsing
    |
    v
Normalized host/service models
    |
    v
Transparent classification rules
    |
    v
Markdown report
```

### Parser

`src/aptriage/nmap_parser.py` uses Python's XML parser to extract only open services. Closed ports remain available in the original XML evidence but do not contribute to the reachable attack-surface report.

### Classification

`src/aptriage/classifier.py` applies the first matching rule to every open service. Current rules cover:

- Telnet
- Redis
- Network-reachable database services
- FTP
- SMB
- RDP
- rsync
- Web services
- SSH
- Other open services

The rules deliberately avoid claiming that exposure proves exploitation, missing authentication, or a confirmed vulnerability.

### Report Generation

`src/aptriage/report_generator.py` produces:

- Executive summary
- Scan metadata
- Host and service inventory
- Prioritized findings
- Original evidence statements
- Security rationale
- Recommended remediation
- Limitations and analysis-source labels

## Testing

Run the dependency-free test suite:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Or install the development dependency and run:

```bash
pytest -q
```

The test suite verifies:

- Correct parsing of hosts and open services
- Exclusion of closed ports
- Malformed and non-Nmap XML errors
- Severity-rule behavior
- Evidence and limitation language in reports

## Repository Layout

```text
aptriage/
├── src/aptriage/          # application package
├── tests/                 # automated tests
├── samples/               # synthetic or authorized sample XML
├── reports/               # generated reports (ignored by Git)
├── docs/                  # final report and presentation PDF
├── .env.example           # safe configuration template
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Limitations

- Nmap detection may be incomplete or inaccurate.
- Rules prioritize exposed services; they do not calculate CVSS.
- An open service is not automatically a vulnerability.
- The tool does not exploit systems, test credentials, or bypass controls.
- Findings require authorized manual validation.
- AI analysis is not yet implemented in version `0.1.0`.

## Team Responsibilities

### Hunter Jackson

- Repository structure and integration
- Nmap XML parsing
- CLI and input validation
- Test environment and sample data
- README and setup documentation

### Tyler Werner

- Classification-rule review
- AI integration and prompts
- Remediation-output review
- Report templates and testing

### Shared

- Architecture and code review
- Functional testing
- Final report and presentation
- Live demonstration and questions

## License

MIT License. See [LICENSE](LICENSE).

