from dataclasses import dataclass


@dataclass(frozen=True)
class SoftwareQuery:
    vendor: str
    software: str
    os_name: str
    os_version: str
    cpu_arch: str
    version: str | None = None


@dataclass(frozen=True)
class ReleaseInfo:
    release_notes_url: str
    download_url: str
    version: str
