# SPDX-FileCopyrightText: 2026 flxk1
# SPDX-License-Identifier: Apache-2.0
"""Read and parse the repository's own published artifacts.

Rule 1 (single source): every closed vocabulary and the language version come from
``grammar/topos.ebnf`` and ``spec/SPEC.md`` at runtime. Nothing here restates a
vocabulary as a literal; the parser only knows the EBNF notation.
"""

from __future__ import annotations

import re
from importlib import resources
from pathlib import Path

GRAMMAR = "grammar/topos.ebnf"
SPEC = "spec/SPEC.md"

# A wheel carries the artifacts as package data under ``published/`` (see
# pyproject.toml); a source checkout or editable install reads them in place.
_SOURCE_ROOT = Path(__file__).resolve().parents[2]


def read_artifact(rel: str) -> str:
    """Return the text of a published artifact (``grammar/...`` or ``spec/...``)."""
    packaged = resources.files(__package__).joinpath("published", *rel.split("/"))
    if packaged.is_file():
        return packaged.read_text(encoding="utf-8")
    checkout = _SOURCE_ROOT.joinpath(*rel.split("/"))
    if checkout.is_file():
        return checkout.read_text(encoding="utf-8")
    raise FileNotFoundError(f"published artifact {rel!r} is not available")


def read_data(name: str) -> str:
    """Return the text of one package data file under ``loomground_topos/data``."""
    return resources.files(__package__).joinpath("data", name).read_text(encoding="utf-8")


# --- EBNF -------------------------------------------------------------------------


def strip_comments(text: str) -> str:
    """Remove ISO 14977 ``(* ... *)`` comments, honouring nesting and quotes."""
    out: list[str] = []
    depth = 0
    quote = ""
    i = 0
    while i < len(text):
        two = text[i:i + 2]
        ch = text[i]
        if depth == 0 and quote:
            out.append(ch)
            if ch == quote:
                quote = ""
            i += 1
            continue
        if two == "(*":
            depth += 1
            i += 2
            continue
        if depth and two == "*)":
            depth -= 1
            i += 2
            continue
        if depth == 0:
            if ch in "\"'":
                quote = ch
            out.append(ch)
        i += 1
    if depth:
        raise ValueError("unterminated EBNF comment in grammar")
    return "".join(out)


def productions(ebnf: str) -> dict[str, str]:
    """Map each production name to its right-hand side (comments removed)."""
    body = strip_comments(ebnf)
    rules: dict[str, str] = {}
    buf: list[str] = []
    quote = ""
    for ch in body:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            continue
        if ch == ";":
            stmt = "".join(buf).strip()
            buf = []
            if not stmt:
                continue
            name, sep, rhs = stmt.partition("=")
            if not sep:
                raise ValueError(f"malformed EBNF rule: {stmt[:60]!r}")
            key = " ".join(name.split())
            if key in rules:
                raise ValueError(f"EBNF rule {key!r} defined twice")
            rules[key] = " ".join(rhs.split())
            continue
        buf.append(ch)
    return rules


_TERMINAL = re.compile(r'^"([^"]+)"$')


def closed_enum(ebnf: str, rule: str) -> tuple[str, ...]:
    """The terminals of ``rule`` when it is a pure alternation of quoted terminals.

    Raises ``KeyError`` when the grammar has no such rule and ``ValueError`` when the
    rule is not a closed enumeration (fail-closed: never guess a vocabulary).
    """
    rhs = productions(ebnf)[rule]
    values: list[str] = []
    for alt in (a.strip() for a in rhs.split("|")):
        m = _TERMINAL.match(alt)
        if not m:
            raise ValueError(f"EBNF rule {rule!r} is not a closed enumeration: {alt!r}")
        if m.group(1) in values:
            raise ValueError(f"EBNF rule {rule!r} repeats {m.group(1)!r}")
        values.append(m.group(1))
    return tuple(values)


# --- version ----------------------------------------------------------------------

_RATIFIED = re.compile(r"STATUS:\s*RATIFIED\s*\(v(\d+(?:\.\d+)*)\)")
_SPEC_STATUS = re.compile(r"\*\*Status:\s*ratified,\s*v(\d+(?:\.\d+)*)\.\*\*")
_GRAPH_ID = re.compile(r"urn:loomground:topos:(\d+(?:\.\d+)*):graph")


def _one(pattern: re.Pattern, text: str, where: str) -> str:
    found = set(pattern.findall(text))
    if len(found) != 1:
        raise ValueError(f"{where}: expected exactly one language version, found {sorted(found)}")
    return found.pop()


def language_version(ebnf: str, spec: str) -> str:
    """The ratified language version, required to agree across grammar and spec.

    Sources: the grammar's ``STATUS: RATIFIED (vX)`` header, its interchange-schema
    ``$id`` (``urn:loomground:topos:X:graph``), the spec's status header and its
    ``**Status: ratified, vX.**`` line. A disagreement stops the port (fail-closed).
    """
    seen = {
        "grammar status": _one(_RATIFIED, ebnf, GRAMMAR),
        "grammar schema $id": _one(_GRAPH_ID, ebnf, GRAMMAR),
        "spec status header": _one(_RATIFIED, spec, SPEC),
        "spec status line": _one(_SPEC_STATUS, spec, SPEC),
    }
    if len(set(seen.values())) != 1:
        raise ValueError(f"grammar and spec disagree on the language version: {seen}")
    return next(iter(seen.values()))
