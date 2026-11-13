"""Data models shared by the parser, classifier, and report generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class Service:
    """One open network service reported by Nmap."""

    port: int
    protocol: str
    state: str
    name: str = "unknown"
    product: str = ""
    version: str = ""
    extra_info: str = ""

    @property
    def display_name(self) -> str:
        details = " ".join(
            part.strip() for part in (self.product, self.version, self.extra_info) if part.strip()
        )
        return f"{self.name} ({details})" if details else self.name


@dataclass(slots=True)
class Host:
    """A host and its open services."""

    address: str
    status: str
    hostnames: list[str] = field(default_factory=list)
    os_matches: list[str] = field(default_factory=list)
    services: list[Service] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Finding:
    """A deterministic finding produced by an APTriage classification rule."""

    rule_id: str
    title: str
    severity: str
    host: str
    port: int
    protocol: str
    service: str
    evidence: str
    rationale: str
    recommendation: str


@dataclass(slots=True)
class ScanResult:
    """Normalized scan data and associated metadata."""

    source_file: str
    scanner: str = "nmap"
    scanner_version: str = ""
    command_line: str = ""
    started_at: str = ""
    finished_at: str = ""
    hosts: list[Host] = field(default_factory=list)
    parsed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    )

    @property
    def open_service_count(self) -> int:
        return sum(len(host.services) for host in self.hosts)

