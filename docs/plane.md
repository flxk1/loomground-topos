<!--
SPDX-FileCopyrightText: 2026 flxk1
SPDX-License-Identifier: CC-BY-4.0
-->
# The Topos plane package

`loomground-topos` ships as a Python package (`src/loomground_topos`) that publishes the
plane as data under the shared plane descriptor contract v1. It depends on nothing
outside the standard library and never imports the versum.

## Descriptor

Entry-point group `loomground.planes`, name `topos`, target `loomground_topos.plane:plane`.
`plane()` takes no arguments and returns:

| key | value |
|---|---|
| `plane` | `"topos"` |
| `language_version` | read from `grammar/topos.ebnf` (status header and interchange-schema `$id`) and `spec/SPEC.md` (status header and status line); all four must agree or loading fails |
| `nd_system` | the grammar-level nD system: `id` (`loomground-topos`), `namespace` (`topos`), `version` (equal to `language_version`), `axes`, `bindings`, `validation` with `unknown_values: reject` |
| `binding` | the 5D binding, read from the single data file `src/loomground_topos/data/binding.json`; empty (see D4) |
| `produce` | `produce(sentence, context=None)`, pure and deterministic |
| `examples` | synthetic examples (placeholder identifiers only), each `{sentence, context, expected, note}`; `expected` is the list of claims `produce(sentence, context)` returns, stated literally rather than computed, as `versum.planes` requires |

## Axes

| axis | cardinality | vocabulary |
|---|---|---|
| `rank` | one | open: rank ladders are per-system policy data (SPEC §7.3); the grammar's `rank-value` is any number or `null` |
| `level` | one | open: level ladders are per-system policy data (SPEC §7.2) |
| `organ` | one | open: a jurisdiction supplies its organs (SPEC §2, §9) |
| `competence` | many | open: competence domains and allocation vocabularies are per-system policy data (SPEC §7.4) |
| `scope` | many | open: the grammar publishes no scope vocabulary |
| `reception` | one | open: the grammar publishes no reception vocabulary; reception mode is per-system policy data |

Jurisdiction is source-level and already a core versum axis, so this plane does not
declare it. Axis shapes (value type, cardinality, primitives) live in
`src/loomground_topos/data/axes.json`, which records for every axis why it is open.
No axis is closed: the grammar publishes no closed vocabulary for any of them. The
grammar's `coupling-rel` rule (`has-primacy-over`, `applies-directly-in`, ...) names
edge relations between legal orders, not reception modes, so it is not a vocabulary
for `reception`; a grounded system supplies its own reception modes as policy data.

## Producer

`produce` reads `context["source"]`, a mapping whose keys are topos axis names. With no
such metadata it returns `[]`. Otherwise it returns one claim in the versum claim
shape, `{relation, span: [0, len(sentence)], coordinates, slots: {}, method}`, plus
`source` (the source's `id`, `urn` or `canonical_urn`) when the metadata carries one.
The coordinates describe the whole source, so no form slot of the sentence is bound. Every axis
is open, so any non-empty identifier is accepted; a value of the wrong shape for its
cardinality (an empty string, a list where one value is expected, an empty list)
raises `ValueError`: it is rejected, never dropped or repaired.

## Grounded instances

Grounded ladders, organs and competences of real legal orders are not part of this
package. `load_grounded(path)` reads such a document only from a path the caller
supplies; there is no default path. It checks that the grammar-level axes it declares
agree in value type and cardinality.

## 5D binding: D4 is open

The spec describes this plane as carrying only *structural capacity*, "the standing to
create, rank, and apply norms" (SPEC §0, `spec/SPEC.md` lines 36-52). No formal binding
of topos relations to a 5D dimension is published. Decision D4 (structural, or
nD-only) is left open; until it is taken the package applies the nD-only default and
`binding.json` is empty.
