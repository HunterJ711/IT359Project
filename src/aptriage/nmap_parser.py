"""Nmap XML parsing and validation."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from .models import Host, ScanResult, Service


class NmapParseError(ValueError):
    """Raised when an input file is missing, malformed, or not Nmap XML."""


def _timestamp(value: str | None) -> str:
    if not value:
        return ""
    try:
        from datetime import datetime, timezone

        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return value


def parse_nmap_xml(path: str | Path) -> ScanResult:
    """Parse an Nmap XML file into normalized Python models.

    Only open services are retained because APTriage reports reachable attack
    surface. Raw evidence remains available in the original XML file.
    """

    source = Path(path)
    if not source.is_file():
        raise NmapParseError(f"Nmap XML file does not exist: {source}")

    try:
        root = ET.parse(source).getroot()
    except ET.ParseError as exc:
        raise NmapParseError(f"Malformed XML in {source}: {exc}") from exc
    except OSError as exc:
        raise NmapParseError(f"Unable to read {source}: {exc}") from exc

    if root.tag != "nmaprun":
        raise NmapParseError(
            f"Expected an Nmap <nmaprun> document, found <{root.tag}> in {source}"
        )

    finished = root.find("./runstats/finished")
    result = ScanResult(
        source_file=str(source),
        scanner=root.get("scanner", "nmap"),
        scanner_version=root.get("version", ""),
        command_line=root.get("args", ""),
        started_at=_timestamp(root.get("start")),
        finished_at=_timestamp(finished.get("time") if finished is not None else ""),
    )

    for host_element in root.findall("host"):
        status_element = host_element.find("status")
        status = status_element.get("state", "unknown") if status_element is not None else "unknown"

        addresses = host_element.findall("address")
        preferred = next(
            (item.get("addr") for item in addresses if item.get("addrtype") in {"ipv4", "ipv6"}),
            None,
        )
        address = preferred or next((item.get("addr") for item in addresses), "unknown")

        host = Host(
            address=address or "unknown",
            status=status,
            hostnames=[
                item.get("name", "")
                for item in host_element.findall("./hostnames/hostname")
                if item.get("name")
            ],
            os_matches=[
                item.get("name", "")
                for item in host_element.findall("./os/osmatch")
                if item.get("name")
            ],
        )

        for port_element in host_element.findall("./ports/port"):
            state_element = port_element.find("state")
            state = state_element.get("state", "unknown") if state_element is not None else "unknown"
            if state != "open":
                continue

            service_element = port_element.find("service")
            attrs = service_element.attrib if service_element is not None else {}
            try:
                port = int(port_element.get("portid", "0"))
            except ValueError:
                port = 0

            host.services.append(
                Service(
                    port=port,
                    protocol=port_element.get("protocol", "unknown"),
                    state=state,
                    name=attrs.get("name", "unknown"),
                    product=attrs.get("product", ""),
                    version=attrs.get("version", ""),
                    extra_info=attrs.get("extrainfo", ""),
                )
            )

        host.services.sort(key=lambda item: (item.protocol, item.port))
        result.hosts.append(host)

    return result

