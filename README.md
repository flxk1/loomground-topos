# loomground-topos
Experimental: legal-system topology language for the Loomground family — authority, hierarchy, competence, inter-system relations.

## Problem
Which source outranks which is a lookup table per project. A language for authority, hierarchy and competence between legal systems. Experimental.

## Read
[`spec/SPEC.md`](spec/SPEC.md) · [`grammar/topos.ebnf`](grammar/topos.ebnf) · [`examples/`](examples)

## Usage
```lt
organ de:bverfg  system de  level de:federal  powers {judicial}
```
Every `.lt` block under `examples/` is parsed by the CI job in `.github/workflows/main.yml`.

## Example
```
in : organ de:bverfg  system de  level de:federal  powers {judicial}
     rel   eu:regulation  has-primacy-over  de:formal-statute
out: parsed examples/readme.md: 2 statements
     2 statements, 0 errors
```

## Language
`lt` expresses the structure of legal authority: systems, levels, organs with powers, instrument ranks, competences, and their relations.
Forms: `system` · `level` · `organ` · `instrument` · `competence` · `rel a <relation> b [props]` · `assert <organ> : [NOT] a <relation> b`.
```lt
level  de:federal  system de  rank 0  contains de:land           # contains the Länder
organ  de:bverfg   system de  level de:federal  powers {judicial}   # judicial power
instrument eu:regulation  system eu  rank 1  directly-applicable    # normative rank 1
rel eu:regulation  has-primacy-over  de:formal-statute  [resolution_mode = disapply]   # the statute is set aside
assert de:bverfg : NOT eu:primary-law has-primacy-over de:grundgesetz  [status = contested]   # a denial, recorded
```
`rank` on a level is territorial; on an instrument, normative. Card: [`docs/language-card.md`](docs/language-card.md).

## Contracts
Nodes: `system`, `organ`, `level`, `instrument`, `competence`. Edges: 16 relations; `assert` carries contested relations.

## Family
Legal-system topology language (authority, hierarchy, competence, inter-system relations). Experimental. Peer of loomground-deontic. Consumed by loomground-versum profiles.

## Status
v0.1 · 4 examples · CI parses every `.lt` block · [`GROUNDING-NOTES.md`](GROUNDING-NOTES.md) · [`docs/model.md`](docs/model.md)

## License
CC-BY-4.0 (spec, README) · Apache-2.0 (grammar, examples) — `LICENSES/`, `NOTICE`.
