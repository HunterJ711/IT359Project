"""Transparent, deterministic rules for prioritizing exposed services."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .models import Finding, ScanResult, Service


@dataclass(frozen=True, slots=True)
class Rule:
    rule_id: str
    title: str
    severity: str
    matches: Callable[[Service], bool]
    rationale: str
    recommendation: str


def _service_is(*names: str) -> Callable[[Service], bool]:
    expected = {name.lower() for name in names}
    return lambda service: service.name.lower() in expected


def _port_is(*ports: int) -> Callable[[Service], bool]:
    expected = set(ports)
    return lambda service: service.port in expected


RULES: tuple[Rule, ...] = (
    Rule(
        "INSECURE_TELNET",
        "Telnet service exposed",
        "High",
        lambda service: _service_is("telnet")(service) or _port_is(23)(service),
        "Telnet commonly transmits credentials and session content without encryption.",
        "Disable Telnet and use SSH with strong authentication and network access controls.",
    ),
    Rule(
        "EXPOSED_REDIS",
        "Redis service exposed",
        "High",
        lambda service: _service_is("redis", "redis-server")(service) or _port_is(6379)(service),
        "A network-reachable Redis service may expose sensitive data or administrative operations if authentication and binding controls are weak.",
        "Restrict Redis to trusted hosts, require authentication, use TLS where available, and apply least-privilege firewall rules.",
    ),
    Rule(
        "EXPOSED_DATABASE",
        "Database service exposed",
        "Medium",
        lambda service: _service_is(
            "mongodb", "mongod", "mysql", "postgresql", "postgres", "ms-sql-s", "oracle"
        )(service)
        or _port_is(1433, 1521, 27017, 3306, 5432)(service),
        "The database is reachable over the network, increasing attack surface. The scan alone does not prove missing authentication or a vulnerability.",
        "Restrict database access to required application hosts, enforce strong authentication, encrypt connections, and keep the service updated.",
    ),
    Rule(
        "INSECURE_FTP",
        "FTP service exposed",
        "Medium",
        lambda service: _service_is("ftp")(service) or _port_is(21)(service),
        "Traditional FTP does not protect credentials or file contents in transit. Anonymous access cannot be determined from port evidence alone.",
        "Replace FTP with SFTP or FTPS, disable anonymous access unless explicitly required, and restrict access by network policy.",
    ),
    Rule(
        "EXPOSED_SMB",
        "SMB file-sharing service exposed",
        "Medium",
        lambda service: _service_is("microsoft-ds", "netbios-ssn", "smb")(service)
        or _port_is(139, 445)(service),
        "SMB can expose files, authentication services, and administrative interfaces if shares or permissions are misconfigured.",
        "Limit SMB to trusted networks, disable legacy SMB versions, require authentication, and review share permissions.",
    ),
    Rule(
        "EXPOSED_RDP",
        "Remote Desktop service exposed",
        "Medium",
        lambda service: _service_is("ms-wbt-server", "rdp")(service) or _port_is(3389)(service),
        "Remote Desktop is a high-value authentication surface when reachable from untrusted networks.",
        "Restrict RDP through VPN or approved management networks, require MFA and Network Level Authentication, and monitor login attempts.",
    ),
    Rule(
        "EXPOSED_RSYNC",
        "rsync daemon exposed",
        "Medium",
        lambda service: _service_is("rsync")(service) or _port_is(873)(service),
        "An rsync daemon may expose readable or writable modules if access controls are weak. Module permissions require separate validation.",
        "Restrict TCP 873, disable anonymous modules, use least-privilege filesystem permissions, and prefer encrypted transport.",
    ),
    Rule(
        "WEB_SERVICE",
        "Web service discovered",
        "Low",
        lambda service: _service_is("http", "https", "http-proxy", "ssl/http")(service)
        or _port_is(80, 443, 8000, 8080, 8443)(service),
        "A reachable web service requires application-level review; an open port alone does not establish a vulnerability.",
        "Confirm the service is required, enforce HTTPS, patch the application stack, and perform authorized web testing.",
    ),
    Rule(
        "REMOTE_SSH",
        "SSH service discovered",
        "Low",
        lambda service: _service_is("ssh")(service) or _port_is(22)(service),
        "SSH is an administrative interface. Its presence is not inherently vulnerable but warrants access-control review.",
        "Restrict SSH to approved sources, prefer key-based authentication, disable direct root login, and monitor authentication events.",
    ),
)


SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Informational": 3}


def classify_scan(scan: ScanResult) -> list[Finding]:
    """Apply the first matching rule to every open service."""

    findings: list[Finding] = []
    for host in scan.hosts:
        for service in host.services:
            rule = next((candidate for candidate in RULES if candidate.matches(service)), None)
            if rule is None:
                rule = Rule(
                    "OPEN_SERVICE",
                    "Open network service discovered",
                    "Low",
                    lambda _: True,
                    "The service is reachable and contributes to the host's attack surface. Its security posture requires additional validation.",
                    "Confirm the service is required, restrict it to trusted networks, and keep the software patched.",
                )

            evidence = (
                f"Nmap reported {service.port}/{service.protocol} open with service "
                f"'{service.display_name}'."
            )
            findings.append(
                Finding(
                    rule_id=rule.rule_id,
                    title=rule.title,
                    severity=rule.severity,
                    host=host.address,
                    port=service.port,
                    protocol=service.protocol,
                    service=service.display_name,
                    evidence=evidence,
                    rationale=rule.rationale,
                    recommendation=rule.recommendation,
                )
            )

    return sorted(
        findings,
        key=lambda item: (SEVERITY_ORDER.get(item.severity, 99), item.host, item.port),
    )

