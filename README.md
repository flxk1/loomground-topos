<!--
SPDX-FileCopyrightText: 2026 flxk1
SPDX-License-Identifier: CC-BY-4.0
-->
# loomground-topos

**Loomground Topos** — the **legal-system topology** language for the Loomground
family: the formal vocabulary for the *structure* of legal authority. It models who
holds which power, at which level, and how those powers constrain one another —
independently of what any of them permits or forbids.

It is a parallel nD language pack, a peer to
[`loomground-deontic`](https://github.com/flxk1/loomground-deontic) and
`loomground-governance`. Where deontic is the language of *norms* (what is permitted /
obliged / forbidden) and a source graph is the language of *sources* (what a text
provides), Topos is the language of *structure* (which organ may make, rank, or apply
which norm, and which checks which). The three are separate planes: Topos supplies the
structure the deontic plane quantifies over and within which a source graph positions
its statutes.

Topos is **universal** — it carries any legal system (federal or unitary, common or
civil, secular or customary, supranational or national, and the couplings between
them). It is **consume-only**: downstream consumers read it; none owns it.

## What's here

| File | Role |
|---|---|
| [`spec/SPEC.md`](spec/SPEC.md) | the language definition — model, neutrality principles, conflict-resolution precedence, inter-system coupling, the contested-relation mechanism, and the plane seams |
| [`grammar/topos.ebnf`](grammar/topos.ebnf) | the `.lt` netlist grammar (EBNF, in the loomground family idiom) plus an abstract-graph JSON interchange |
| [`examples/`](examples) | worked instantiations — the EU order, Germany, the EU↔Germany coupling, and the UK (common-law proof) — each a concrete node/edge listing |
| [`GROUNDING-NOTES.md`](GROUNDING-NOTES.md) | grounding provenance: what was read, the legal doctrines cited, and the honest open questions and caveats |

## The model in one screen

- **Nodes** — `organ` (a power-holding body), `level` (a vertical stratum),
  `instrument` (a norm-type carrying a rank), `competence` (a subject-matter domain),
  inside a `system` frame.
- **Edges** — *vertical* (`outranks`, `derives-authority-from`, `level-contains`,
  `has-primacy-over`), *horizontal check* (`reviews`, `can-veto`, `can-override`,
  `appoints`, `dissolves`, `may`/`must-refer-to`), and *coupling* (the same relations
  between distinct systems).
- **Two vertical axes**, kept separate — the territorial `level_rank` and the normative
  `instrument.rank`.
- **Powers are a parameter** — the organ-type catalogue is declared per system, never
  a hardcoded three branches.
- **Conflict resolution is first-class** — cross-order primacy → *lex superior* → *lex
  specialis* → *lex posterior*, remappable.
- **Contested relations** — a relation one organ asserts and another denies is carried
  as paired (or lone) assertions, represented and never silently resolved.
- **Balance** is an emergent query (`no-organ-unchecked`), not a stored flag.

## Status

Ratified design, **v0.1**. Honest caveats (see [`GROUNDING-NOTES.md`](GROUNDING-NOTES.md)):
some pinpoint citations are flagged for verification against an authoritative reporter
before durable external citation; the temporal axis is a point (interval support is
future work); and the relation vocabulary is a closed enum in v0.1, so a few treaty
relations (accession, reservation, denunciation) are carried only implicitly.

## Licence

Dual, following the Loomground family: the language-definition prose (`README.md`,
`spec/SPEC.md`) is CC-BY-4.0; the grammar, worked examples, grounding notes, and repository
files are Apache-2.0. See [`LICENSES/`](LICENSES) and [`NOTICE`](NOTICE).
