# SPDX-FileCopyrightText: 2026 flxk1
# SPDX-License-Identifier: Apache-2.0
"""The Topos plane descriptor (shared plane descriptor contract v1).

``plane()`` returns::

    {"plane": "topos",
     "language_version": <from grammar/topos.ebnf + spec/SPEC.md>,
     "nd_system": <dict accepted by versum.nd.NDSystem.from_dict(d).validate()>,
     "binding": {},            # D4 default: nD-only, read from data/binding.json
     "produce": produce,       # pure, deterministic
     "examples": [{"sentence", "context", "expected": [claim]}]}

Axes: rank, level, organ, competence, scope, reception. Jurisdiction is a
source-level axis of the core versum system and is not declared here. Every axis is
open: the grammar and spec publish no closed set for any of them (ladders, organs and
competences are per-system policy data, SPEC.md section 7). In particular the grammar
publishes no reception vocabulary; reception mode is per-system policy data. The
grammar's ``coupling-rel`` rule names inter-order edge relations, not reception modes,
and is not a source for this axis. Each axis records the reason it is open in
``data/axes.json``.

This module never imports the versum (A1: planes are data-only).
"""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from .artifacts import GRAMMAR, SPEC, read_artifact, read_data
from .artifacts import language_version as _parse_version

PLANE = "topos"
AXES = ("rank", "level", "organ", "competence", "scope", "reception")
RELATION = "topos.position"


# --- nD system ----------------------------------------------------------------------


def build_nd_system(ebnf: str, spec: str, shape: Mapping[str, Any]) -> dict:
    """Pure: derive the nD-system document from artifact texts and the axis shapes."""
    version = _parse_version(ebnf, spec)
    axes: dict[str, dict] = {}
    for name, raw in shape["axes"].items():
        axis = {
            "value_type": raw["value_type"],
            "cardinality": raw["cardinality"],
            "primitives": list(raw["primitives"]),
        }
        vocab = raw["vocabulary"]
        reason = vocab.get("open") if isinstance(vocab, Mapping) else None
        if set(vocab) != {"open"} or not isinstance(reason, str) or not reason.strip():
            # The grammar publishes no closed vocabulary for any topos axis, so every
            # axis must be open and must record why (fail closed on anything else).
            raise ValueError(f"axis {name!r}: vocabulary must be open with a recorded reason")
        axis["vocabulary_mode"] = "open"
        axes[name] = axis
    if tuple(axes) != AXES:
        raise ValueError(f"axis data declares {tuple(axes)}, expected {AXES}")
    return {
        "id": shape["id"],
        "namespace": shape["namespace"],
        "version": version,
        "describes": shape["describes"],
        "axes": axes,
        "bindings": [
            {"form_slot": b["form_slot"], "allowed_axes": list(b["axes"])}
            for b in shape["bindings"]
        ],
        "validation": dict(shape["validation"]),
    }


@lru_cache(maxsize=1)
def _nd_system_cached() -> str:
    doc = build_nd_system(read_artifact(GRAMMAR), read_artifact(SPEC),
                          json.loads(read_data("axes.json")))
    return json.dumps(doc)


def nd_system() -> dict:
    """The grammar-level nD system (a fresh copy on every call)."""
    return json.loads(_nd_system_cached())


def language_version() -> str:
    return _parse_version(read_artifact(GRAMMAR), read_artifact(SPEC))


def binding() -> dict:
    """The 5D binding, read from its single data file (D4 default: empty, nD-only)."""
    data = json.loads(read_data("binding.json"))
    if not isinstance(data, dict):
        raise ValueError("binding.json must hold a JSON object")
    return data


# --- producer -----------------------------------------------------------------------


def _coordinate(name: str, axis: Mapping[str, Any], value: Any) -> Any:
    """Check one metadata value against its axis; reject, never repair (rule 6)."""
    many = axis["cardinality"] == "many"
    if many:
        if isinstance(value, str) or not isinstance(value, (list, tuple)) or not value:
            raise ValueError(f"topos axis {name!r} takes a non-empty list of identifiers")
        values = list(value)
    else:
        values = [value]
    for v in values:
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"topos axis {name!r}: {v!r} is not an identifier")
        if axis["vocabulary_mode"] == "closed" and v not in axis["vocabulary"]:
            raise ValueError(
                f"topos axis {name!r}: {v!r} is outside the closed vocabulary")
    return values if many else values[0]


def produce(sentence: str, context: Mapping[str, Any] | None = None) -> list[dict]:
    """Pure, deterministic producer.

    Derives topos coordinates for ``sentence`` from ``context['source']`` metadata:
    a mapping whose keys are topos axis names (rank, level, organ, competence,
    scope, reception). Returns ``[]`` when there is no sentence or no such metadata.
    All topos axes are open, so any non-empty identifier is accepted (including a
    grounded system's own reception mode); a value of the wrong shape raises
    ``ValueError`` (fail-closed), as would a value outside a closed vocabulary if a
    system document ever declared one. Keys that are not topos axes are ignored (they belong to other
    systems, e.g. the core jurisdiction axis).
    """
    if not isinstance(sentence, str) or not sentence.strip():
        return []
    source = (context or {}).get("source") if isinstance(context, Mapping) else None
    if not isinstance(source, Mapping):
        return []
    system = nd_system()
    coordinates = {
        name: _coordinate(name, system["axes"][name], source[name])
        for name in AXES
        if name in source and source[name] is not None
    }
    if not coordinates:
        return []
    claim: dict[str, Any] = {
        "relation": RELATION,
        # versum claim contract: span is [start, end] into the sentence; slots map one
        # form slot to one axis. The coordinates describe the whole source, so no form
        # slot of the sentence is bound and ``slots`` stays empty.
        "span": [0, len(sentence)],
        "coordinates": copy.deepcopy(coordinates),
        "slots": {},
        "method": f"loomground-topos:source-metadata:v{system['version']}",
    }
    for key in ("id", "urn", "canonical_urn"):
        if isinstance(source.get(key), str) and source[key]:
            claim["source"] = source[key]
            break
    return [claim]


# --- grounded instances (optional, local only) --------------------------------------


def load_grounded(path: str | Path) -> dict:
    """Load a grounded topos nD-system document from a caller-supplied local path.

    There is no default path: grounded instances stay local to the caller. The file
    must be JSON (optionally wrapped in ``{"nd_system": ...}``); every grammar-level
    axis it declares must agree with this plane's value_type and cardinality. Axes the
    grammar level does not declare (e.g. a source-level jurisdiction) pass through.
    """
    if path is None or str(path) == "":
        raise ValueError("load_grounded needs an explicit local path")
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    root = raw.get("nd_system", raw) if isinstance(raw, dict) else None
    if not isinstance(root, dict) or not isinstance(root.get("axes"), dict):
        raise ValueError("grounded document has no nD-system axes")
    ours = nd_system()["axes"]
    for name, axis in root["axes"].items():
        if name not in ours:
            continue
        for key in ("value_type", "cardinality"):
            if axis.get(key, ours[name][key]) != ours[name][key]:
                raise ValueError(
                    f"grounded axis {name!r} {key} {axis.get(key)!r} "
                    f"disagrees with the grammar-level {ours[name][key]!r}")
    return root


# --- descriptor ---------------------------------------------------------------------


def _examples(version: str) -> list[dict]:
    """Published examples: each carries its ``expected`` claims, written out here.

    ``expected`` is stated literally (not computed by calling ``produce``), so a
    consumer comparing it with a fresh ``produce(sentence, context)`` call checks the
    producer against an independent statement. Identifiers are synthetic.
    """
    sentence = "An example sentence from a source placed in an example order."
    method = f"loomground-topos:source-metadata:v{version}"
    return [
        {
            "sentence": sentence,
            "context": {"source": {
                "id": "example:source-1",
                "rank": "example:rank-a",
                "level": "example:level-a",
                "organ": "example:organ-a",
                "competence": ["example:domain-a"],
                "scope": ["example:domain-a"],
                "reception": "example:reception-a",
            }},
            "expected": [{
                "relation": "topos.position",
                "span": [0, 61],
                "coordinates": {
                    "rank": "example:rank-a",
                    "level": "example:level-a",
                    "organ": "example:organ-a",
                    "competence": ["example:domain-a"],
                    "scope": ["example:domain-a"],
                    "reception": "example:reception-a",
                },
                "slots": {},
                "method": method,
                "source": "example:source-1",
            }],
            "note": f"synthetic identifiers only; language v{version}",
        },
        {
            "sentence": "A sentence whose source carries no topos metadata.",
            "context": {"source": {"id": "example:source-2"}},
            "expected": [],
            "note": "no topos metadata, no claim (absence is preserved, not invented)",
        },
    ]


def plane() -> dict:
    """Zero-argument entry point target for group ``loomground.planes``, name ``topos``."""
    system = nd_system()
    version = system["version"]
    return {
        "plane": PLANE,
        "language_version": version,
        "nd_system": system,
        "binding": binding(),
        "produce": produce,
        "examples": _examples(version),
    }
