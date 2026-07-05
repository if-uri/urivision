# Author: Tom Sapletta · Part of the ifURI solution.
"""Small URI utilities used by the URI runtime layer.

The runtime treats functions as addressable capabilities. A URI such as
``input://local/keyboard/command/type`` is not merely a string; it is the stable
contract used by the LLM, CLI and process runner to select an implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, unquote, urlparse


@dataclass(frozen=True)
class UriParts:
    raw: str
    scheme: str
    authority: str
    path: str
    segments: tuple[str, ...]
    query: dict[str, list[str]]

    @property
    def kind(self) -> str:
        """Return the segment before the last one, conventionally query/command/event."""
        return self.segments[-2] if len(self.segments) >= 2 else ""

    @property
    def name(self) -> str:
        """Return the last path segment, conventionally the verb/name."""
        return self.segments[-1] if self.segments else ""

    @property
    def area(self) -> str:
        """Return the first path segment, conventionally resource area."""
        return self.segments[0] if self.segments else ""


def parse_uri(uri: str) -> UriParts:
    if not isinstance(uri, str) or "://" not in uri:
        raise ValueError(f"URI must contain scheme://authority/path: {uri!r}")
    parsed = urlparse(uri)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Bad URI: {uri!r}")
    segments = tuple(unquote(s) for s in parsed.path.split("/") if s)
    return UriParts(
        raw=uri,
        scheme=parsed.scheme,
        authority=parsed.netloc,
        path=parsed.path,
        segments=segments,
        query=parse_qs(parsed.query, keep_blank_values=True),
    )


def normalize_uri(uri: str) -> str:
    p = parse_uri(uri)
    path = "/".join(p.segments)
    return f"{p.scheme}://{p.authority}/{path}" if path else f"{p.scheme}://{p.authority}"


def _match_segment(pattern: str, value: str, captures: dict[str, str]) -> bool:
    if pattern == "*":
        return True
    if pattern.startswith("{") and pattern.endswith("}"):
        name = pattern[1:-1].strip()
        if not name:
            return False
        existing = captures.get(name)
        if existing is not None and existing != value:
            return False
        captures[name] = value
        return True
    return pattern == value


def match_uri(pattern: str, uri: str) -> dict[str, str] | None:
    """Match URI against a capability pattern.

    Supported wildcards:
    - ``{target}`` captures one segment or authority.
    - ``*`` matches one segment.

    Example:
    >>> match_uri('input://{target}/keyboard/command/type', 'input://local/keyboard/command/type')
    {'target': 'local'}
    """
    pp = parse_uri(pattern)
    up = parse_uri(uri)
    if pp.scheme != up.scheme:
        return None
    captures: dict[str, str] = {}
    if not _match_segment(pp.authority, up.authority, captures):
        return None
    if len(pp.segments) != len(up.segments):
        return None
    for a, b in zip(pp.segments, up.segments):
        if not _match_segment(a, b, captures):
            return None
    return captures
