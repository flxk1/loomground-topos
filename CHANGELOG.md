# Changelog

## Unreleased

- Python package `loomground_topos` (`pyproject.toml`, `src/`, `tests/`): the plane descriptor under entry-point group `loomground.planes` (`topos`), with the grammar-level nD system (rank, level, organ, competence, scope, reception) derived at runtime from `grammar/topos.ebnf` and `spec/SPEC.md`, an empty 5D binding (D4 open), a pure source-metadata producer, and an optional loader for grounded instances from a caller-supplied local path. See `docs/plane.md`.
- Layout: `SPEC.md` moved to `spec/SPEC.md`; `grammar-sketch.ebnf` moved to `grammar/topos.ebnf`; added `CHANGELOG.md` and a CI workflow that parses the `.lt` blocks in `examples/`.
