# SPDX-FileCopyrightText: 2026 flxk1
# SPDX-License-Identifier: Apache-2.0
"""Shared plane descriptor contract v1 for the Topos plane."""

from __future__ import annotations

import ast
import copy
import importlib
import json
import os
import re
from importlib.metadata import entry_points
from pathlib import Path

import pytest

import loomground_topos
from loomground_topos import artifacts
from loomground_topos.plane import AXES, build_nd_system, nd_system, plane, produce

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "src" / "loomground_topos"
EXPECTED_AXES = {"rank", "level", "organ", "competence", "scope", "reception"}
OPEN_REASONS = {
    "reception": "the grammar publishes no reception vocabulary; "
                 "reception mode is per-system policy data",
}
#: One illustrative grounded-style reception mode (not copied from any grounded file).
GROUNDED_STYLE_RECEPTION = "monist"
VERSUM_REASON = "versum is not installed in this environment; install loomground-versum to run"


def _source(**axes):
    return {"source": {"id": "example:source-1", **axes}}


def _versum(module: str):
    return pytest.importorskip(module, reason=VERSUM_REASON)


def _topos_entry_point_descriptor() -> dict:
    eps = [ep for ep in entry_points(group="loomground.planes") if ep.name == "topos"]
    assert len(eps) == 1
    return eps[0].load()()


# --- 3: entry point ---------------------------------------------------------------


def test_entry_point_topos_in_group():
    eps = [ep for ep in entry_points(group="loomground.planes") if ep.name == "topos"]
    assert len(eps) == 1
    assert eps[0].value == "loomground_topos.plane:plane"
    descriptor = eps[0].load()()
    assert descriptor["plane"] == "topos"
    assert set(descriptor) >= {"plane", "language_version", "nd_system", "binding", "produce"}
    assert callable(descriptor["produce"])


def test_package_imports():
    assert loomground_topos.plane is not None
    assert loomground_topos.__version__


# --- 4: nD system valid for versum.nd --------------------------------------------


def test_nd_system_validates_in_versum():
    nd = _versum("versum.nd")
    d = plane()["nd_system"]
    system = nd.NDSystem.from_dict(d).validate()
    assert set(system.axes) == EXPECTED_AXES
    assert len(system.axes) == 6
    assert system.version == plane()["language_version"]
    assert system.unknown_values == "reject"
    for axis in system.axes.values():
        assert axis.vocabulary_mode == "open"


def test_nd_system_shape_without_versum():
    d = nd_system()
    assert set(d) >= {"id", "namespace", "version", "axes", "bindings", "validation"}
    assert list(d["axes"]) == list(AXES)
    assert set(d["axes"]) == EXPECTED_AXES
    assert "jurisdiction" not in d["axes"]
    assert d["version"] == plane()["language_version"]
    assert d["validation"]["unknown_values"] == "reject"
    assert not any(k.endswith("_5d_version") for k in d)
    for b in d["bindings"]:
        assert set(b["allowed_axes"]) <= EXPECTED_AXES


def test_language_version_from_artifacts():
    grammar = (ROOT / "grammar" / "topos.ebnf").read_text(encoding="utf-8")
    spec = (ROOT / "spec" / "SPEC.md").read_text(encoding="utf-8")
    g = re.search(r"STATUS:\s*RATIFIED\s*\(v([\d.]+)\)", grammar).group(1)
    s = re.search(r"\*\*Status: ratified, v([\d.]+)\.\*\*", spec).group(1)
    assert g == s == plane()["language_version"]


def test_version_disagreement_fails_closed():
    grammar = artifacts.read_artifact(artifacts.GRAMMAR)
    spec = artifacts.read_artifact(artifacts.SPEC).replace(
        "**Status: ratified, v0.1.**", "**Status: ratified, v9.9.**")
    with pytest.raises(ValueError, match="disagree"):
        artifacts.language_version(grammar, spec)


# --- 5: every axis is open, with its reason recorded in the axes data -------------


def test_every_axis_is_open_and_carries_no_vocabulary():
    axes = nd_system()["axes"]
    for name in EXPECTED_AXES:
        assert axes[name]["vocabulary_mode"] == "open", name
        assert "vocabulary" not in axes[name], name


def test_axes_data_records_why_each_axis_is_open():
    shape = json.loads(artifacts.read_data("axes.json"))
    for name, axis in shape["axes"].items():
        assert set(axis["vocabulary"]) == {"open"}, name
        assert axis["vocabulary"]["open"].strip(), name
    assert shape["axes"]["reception"]["vocabulary"]["open"] == OPEN_REASONS["reception"]


def test_reception_is_not_derived_from_the_grammar():
    """Reception is not taken from any grammar rule (coupling-rel names edges)."""
    data = (PKG / "data" / "axes.json").read_text(encoding="utf-8")
    assert "closed_from_grammar_rule" not in data
    assert "coupling-rel" not in data
    for path in PKG.rglob("*.py"):
        code = [n.value for n in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
                if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        assert "coupling-rel" not in code, path
    assert "closed_enum" not in (PKG / "plane.py").read_text(encoding="utf-8")


@pytest.mark.parametrize("vocabulary", [
    {"closed_from_grammar_rule": "relation"},
    {"open": ""},
    {"open": "reason", "closed": ["x"]},
    {},
])
def test_axis_that_is_not_open_with_a_reason_fails_closed(vocabulary):
    grammar = artifacts.read_artifact(artifacts.GRAMMAR)
    spec = artifacts.read_artifact(artifacts.SPEC)
    shape = json.loads(artifacts.read_data("axes.json"))
    shape["axes"]["reception"]["vocabulary"] = vocabulary
    with pytest.raises(ValueError, match="open with a recorded reason"):
        build_nd_system(grammar, spec, shape)


def test_non_enum_rule_fails_closed():
    grammar = artifacts.read_artifact(artifacts.GRAMMAR)
    with pytest.raises(ValueError):
        artifacts.closed_enum(grammar, "relation")
    with pytest.raises(KeyError):
        artifacts.closed_enum(grammar, "no-such-rule")


# --- 6: binding ---------------------------------------------------------------------


def test_binding_is_empty_and_read_from_one_data_file(monkeypatch):
    assert plane()["binding"] == {}
    path = PKG / "data" / "binding.json"
    assert json.loads(path.read_text(encoding="utf-8")) == {}
    seen = []
    real = artifacts.read_data

    def spy(name):
        seen.append(name)
        return real(name)

    plane_mod = importlib.import_module("loomground_topos.plane")
    monkeypatch.setattr(plane_mod, "read_data", spy)
    assert plane_mod.binding() == {}
    assert seen == ["binding.json"]


# --- 7: produce -------------------------------------------------------------------


@pytest.mark.parametrize("context", [
    None, {}, {"source": None}, {"source": {}}, {"source": {"id": "x"}},
    {"source": {"jurisdiction": "example:j"}}, {"other": {"rank": "example:r"}},
])
def test_produce_without_metadata_returns_empty(context):
    assert produce("A sentence.", context) == []


def test_produce_with_metadata_stays_within_vocabularies():
    ctx = _source(rank="example:rank-a", level="example:level-a",
                  organ="example:organ-a", competence=["example:domain-a"],
                  scope=["example:domain-a", "example:domain-b"],
                  reception="example:reception-a", jurisdiction="example:j")
    sentence = "The example body may adopt the example act."
    claims = produce(sentence, ctx)
    assert len(claims) == 1
    claim = claims[0]
    assert set(claim) == {"relation", "span", "coordinates", "slots", "method", "source"}
    assert claim["span"] == [0, len(sentence)]
    assert claim["slots"] == {}
    assert set(claim["coordinates"]) == EXPECTED_AXES
    axes = nd_system()["axes"]
    for name, value in claim["coordinates"].items():
        values = value if axes[name]["cardinality"] == "many" else [value]
        if axes[name]["vocabulary_mode"] == "closed":
            assert set(values) <= set(axes[name]["vocabulary"])
    assert plane()["language_version"] in claim["method"]
    assert claim["source"] == "example:source-1"


def test_produce_validates_through_versum_assignments():
    nd = _versum("versum.nd")
    system = nd.NDSystem.from_dict(nd_system()).validate()
    claims = produce("S.", _source(organ="example:organ-a", reception="example:reception-a"))
    for name, value in claims[0]["coordinates"].items():
        assert system.axes[name].validate_value(value) == []


def test_grounded_style_reception_accepted_by_produce():
    claims = produce("S.", _source(reception=GROUNDED_STYLE_RECEPTION))
    assert len(claims) == 1
    assert claims[0]["coordinates"] == {"reception": GROUNDED_STYLE_RECEPTION}
    assert claims[0]["span"] == [0, 2]


def test_grounded_style_reception_accepted_by_versum_validation():
    nd = _versum("versum.nd")
    planes = _versum("versum.planes")
    system = nd.NDSystem.from_dict(nd_system()).validate()
    assert system.axes["reception"].validate_value(GROUNDED_STYLE_RECEPTION) == []
    adapter = planes.DescriptorPlane.from_descriptor(_topos_entry_point_descriptor(),
                                                     entry_name="topos")
    claims = adapter.produce("S.", _source(reception=GROUNDED_STYLE_RECEPTION))
    value = claims[0]["coordinates"]["reception"]
    assert adapter.nd_system().axes["reception"].validate_value(value) == []


def test_produce_is_deterministic_and_pure():
    ctx = _source(level="example:level-a", scope=["example:b", "example:a"],
                  reception="example:reception-a")
    before = json.dumps(ctx, sort_keys=True)
    first, second = produce("S.", ctx), produce("S.", ctx)
    assert first == second
    assert json.dumps(ctx, sort_keys=True) == before
    first[0]["coordinates"]["scope"].append("mutated")
    assert produce("S.", ctx) == second


@pytest.mark.parametrize("bad", [
    {"reception": ""},
    {"reception": [GROUNDED_STYLE_RECEPTION]},
    {"scope": "example:not-a-list"},
    {"competence": []},
    {"rank": ""},
    {"organ": 3},
])
def test_produce_rejects_out_of_vocabulary_or_malformed(bad):
    with pytest.raises(ValueError):
        produce("S.", _source(**bad))


def test_every_example_carries_expected_claims():
    examples = plane()["examples"]
    assert examples
    for ex in examples:
        assert isinstance(ex["sentence"], str) and ex["sentence"]
        assert isinstance(ex["expected"], list)
        for claim in ex["expected"]:
            assert set(claim) == {"relation", "span", "coordinates", "slots", "method",
                                  "source"}
    assert any(ex["expected"] for ex in examples)


def test_examples_round_trip():
    """A fresh produce() call reproduces each published ``expected`` field for field."""
    for ex in plane()["examples"]:
        assert produce(ex["sentence"], copy.deepcopy(ex["context"])) == ex["expected"]


def test_first_example_expected_matches_a_literal():
    """G3: the published expectation is pinned by a literal written in this test."""
    ex = plane()["examples"][0]
    version = plane()["language_version"]
    assert ex["expected"] == [{
        "relation": "topos.position",
        "span": [0, len(ex["sentence"])],
        "coordinates": {"rank": "example:rank-a", "level": "example:level-a",
                        "organ": "example:organ-a", "competence": ["example:domain-a"],
                        "scope": ["example:domain-a"], "reception": "example:reception-a"},
        "slots": {},
        "method": f"loomground-topos:source-metadata:v{version}",
        "source": "example:source-1",
    }]


def test_versum_descriptor_validation_accepts_the_topos_plane():
    """G2: versum.planes validates the descriptor loaded via the entry point."""
    planes = _versum("versum.planes")
    adapter = planes.DescriptorPlane.from_descriptor(_topos_entry_point_descriptor(),
                                                     entry_name="topos")
    assert adapter.plane_id == "topos"
    examples = adapter.examples()
    assert examples and all(isinstance(ex["expected"], list) for ex in examples)
    for ex in examples:
        assert adapter.produce(ex["sentence"], copy.deepcopy(ex.get("context"))) == ex["expected"]
    discovered = {p.plane_id for p in planes.discover_planes()}
    assert "topos" in discovered


def test_examples_index_through_versum_entries():
    """Published examples are indexable by versum (claim contract), in memory only."""
    planes = _versum("versum.planes")
    adapter = planes.DescriptorPlane.from_descriptor(_topos_entry_point_descriptor(),
                                                     entry_name="topos")
    for i, ex in enumerate(adapter.examples()):
        built = planes.build_source_entries(ex["sentence"], f"urn:example:topos:{i}",
                                            [adapter], context=ex["context"])
        assert [c["claim"] for c in built.claims] == ex["expected"]
        got = {(a.axis_id, a.value) for a in built.assignments}
        want = {(axis, v) for claim in ex["expected"]
                for axis, value in claim["coordinates"].items()
                for v in (value if isinstance(value, list) else [value])}
        assert got == want


def test_grounded_style_reception_indexes_through_versum():
    planes = _versum("versum.planes")
    adapter = planes.DescriptorPlane.from_descriptor(_topos_entry_point_descriptor(),
                                                     entry_name="topos")
    built = planes.build_source_entries(
        "One sentence. Two sentences.", "urn:example:topos:grounded-style", [adapter],
        context=_source(reception=GROUNDED_STYLE_RECEPTION))
    values = [(a.axis_id, a.value) for a in built.assignments]
    assert values == [("reception", GROUNDED_STYLE_RECEPTION)] * 2


# --- grounded loader (local path only) ---------------------------------------------


def test_load_grounded_requires_explicit_path(tmp_path):
    from loomground_topos import load_grounded
    with pytest.raises(ValueError):
        load_grounded("")
    doc = {"nd_system": {"id": "t", "axes": {
        "level": {"value_type": "controlled_identifier", "cardinality": "one",
                  "vocabulary": ["example:l1"]},
        "jurisdiction": {"value_type": "controlled_identifier"}}}}
    p = tmp_path / "grounded.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    assert load_grounded(p)["axes"]["level"]["vocabulary"] == ["example:l1"]
    doc["nd_system"]["axes"]["level"]["cardinality"] = "many"
    p.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ValueError):
        load_grounded(p)


# --- 9: containment of the package code ---------------------------------------------


def test_package_never_imports_versum():
    for path in PKG.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            assert not any(n == "versum" or n.startswith("versum.") for n in names), path


def test_no_old_project_name_in_new_files():
    banned = "fed" + "er"
    files = [*PKG.rglob("*.py"), *PKG.rglob("*.json"), *Path(__file__).parent.rglob("*.py"),
             ROOT / "pyproject.toml", ROOT / "docs" / "plane.md"]
    for path in files:
        assert banned not in path.read_text(encoding="utf-8").lower(), path


# --- 8: moat (only with a caller-supplied grounded file; no default path) ----------


def _grounded_strings(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("vocabulary", "ontology_relations"):
                _collect(v, out)
            else:
                _grounded_strings(v, out)
    elif isinstance(node, list):
        for v in node:
            _grounded_strings(v, out)


def _collect(node, out):
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            if k != "axis":
                _collect(v, out)
    elif isinstance(node, list):
        for v in node:
            _collect(v, out)


def test_moat_no_grounded_values_in_package():
    path = os.environ.get("LOOMGROUND_TOPOS_GROUNDED")
    if not path:
        pytest.skip("set LOOMGROUND_TOPOS_GROUNDED to a local grounded file to run")
    grounded: set[str] = set()
    _grounded_strings(json.loads(Path(path).read_text(encoding="utf-8")), grounded)
    grounded -= EXPECTED_AXES | {"jurisdiction", "disjoint", "equal", "contains",
                                 "contained_by", "overlaps", "precedes", "succeeds"}
    files = [*PKG.rglob("*.py"), *PKG.rglob("*.json"),
             *(p.resolve() for p in Path(__file__).parent.rglob("*.py")),
             ROOT / "pyproject.toml", ROOT / "docs" / "plane.md"]
    token = re.compile(r"[A-Za-z0-9_.:#/-]+")
    for f in files:
        tokens = set(token.findall(f.read_text(encoding="utf-8")))
        tokens |= {t.strip(".:-/") for t in tokens}
        hits = grounded & tokens
        if f == Path(__file__).resolve():
            # the one illustrative grounded-style literal, allowed in this test file only
            hits -= {GROUNDED_STYLE_RECEPTION}
        assert not hits, (f, len(hits))


def test_nd_system_is_named_like_the_other_loomground_planes():
    """The topos nD system follows the family's naming: id loomground-<plane>, namespace <plane>."""
    system = plane()["nd_system"]
    assert system["id"] == "loomground-topos"
    assert system["namespace"] == "topos"
