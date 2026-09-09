# loomground-topos
Experimental: legal-system topology language for the Loomground family — authority, hierarchy, competence, inter-system relations.

## Read
[`spec/SPEC.md`](spec/SPEC.md) · [`grammar/topos.ebnf`](grammar/topos.ebnf) · [`examples/`](examples)

## Usage
```lt
organ de:bverfg  system de  level de:federal  powers {judicial}
```

## Contracts
Nodes: `system`, `organ`, `level`, `instrument`, `competence`. Edges: 16 relations; `assert` carries contested relations.

## Family
Legal-system topology language (authority, hierarchy, competence, inter-system relations). Experimental. Peer of loomground-deontic. Consumed by loomground-versum profiles.

## Status
v0.1 · 4 examples · CI parses every `.lt` block · [`GROUNDING-NOTES.md`](GROUNDING-NOTES.md) · [`docs/model.md`](docs/model.md)

## License
CC-BY-4.0 (spec, README) · Apache-2.0 (grammar, examples) — `LICENSES/`, `NOTICE`.
