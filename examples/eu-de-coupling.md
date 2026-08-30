<!--
SPDX-FileCopyrightText: 2026 flxk1
Copyright 2026 flxk1 · STATUS: PROPOSED

SPDX-License-Identifier: Apache-2.0
-->
# Instantiation 3 — the EU ↔ Germany coupling

The proving case. Uses the `eu` order (`eu.md`) and the `de` order (`de.md`) and
joins them with the §4 coupling edges. Every coupling edge is between two
**distinct** systems (well-formedness §10.4). The contested BVerfG ↔ CJEU edge is
represented, **not resolved**.

## Primacy — `disapply`, not `invalidate` (§4.1)

```lt
# Costa v ENEL (Case 6/64); Simmenthal (Case 106/77): a directly-applicable EU
# norm is applied in preference; the conflicting national norm is SET ASIDE by
# the national court — disapplied, not annulled. Contrast Art 31 GG (invalidate).
rel eu:regulation   has-primacy-over  de:formal-statute
    [resolution_mode = disapply, basis = "Costa 6/64; Simmenthal 106/77"]
rel eu:primary-law  has-primacy-over  de:formal-statute
    [resolution_mode = disapply, basis = "Internationale Handelsgesellschaft 11/70"]
```

## Direct applicability — Regulation (Art 288 TFEU)

```lt
rel eu:regulation  applies-directly-in  de:system
    [basis = "Art 288(2) TFEU — binding in its entirety and directly applicable"]
```

## Transposition — Directive spawns a derived national instrument (§4.3)

```lt
# Art 288(3) TFEU: a directive binds as to result, leaving form and methods to
# the state. Two linked nodes + a coupling edge carrying deadline + state.
instrument eu:directive-2019-790  system eu  rank 1  origin eu:parliament-council  # DSM Directive (example)
instrument de:urhdag              system de  rank 1  origin de:bundestag
    # the German transposing statute; derives-authority-from the directive
rel de:urhdag  derives-authority-from  eu:directive-2019-790
rel eu:directive-2019-790  must-be-transposed-by  de:system
    [deadline = 2021-06-07, state = transposed, basis = "Art 288(3) TFEU"]

# A non-transposition case would read state = gap, which is the structural
# precondition for Francovich liability (C-6/90, C-9/90) and for vertical direct
# effect of the unimplemented directive (Van Duyn 41/74).
```

## Direct effect — vertical yes, horizontal no (§4.5)

```lt
rel eu:directive-2019-790  has-direct-effect  de:administrative-court
    [status = asserted, basis = "vertical only: Van Duyn 41/74; NO horizontal effect: Marshall 152/84, Faccini Dori C-91/92"]
```

## Preliminary reference — the court-dialogue check (§4.6)

```lt
rel de:ordinary-court        may-refer-to   eu:cjeu  [basis = "Art 267(2) TFEU — discretionary"]
rel de:bundesgerichtshof     must-refer-to  eu:cjeu  [basis = "Art 267(3) TFEU — court of last instance"]
```

## THE CONTESTED EDGE — represented, never resolved (§4.7)

```lt
# The CJEU asserts unconditional primacy even over national constitutional law.
assert eu:cjeu : eu:primary-law  has-primacy-over  de:grundgesetz
    [status = asserted,
     basis = "Costa 6/64; Internationale Handelsgesellschaft 11/70 — primacy even over constitutional rights"]

# The BVerfG DENIES unconditional primacy over the Grundgesetz. Three reservations,
# each a distinct contested assertion. (No parenthesised form: the NOT scopes the
# whole triple by position — matches the EBNF `assert id ":" [NOT] endpoint
# relation-type endpoint`, which defines no "(" terminal.)
assert de:bverfg : NOT eu:primary-law has-primacy-over de:grundgesetz
    [status = contested,
     basis = "Solange I BVerfGE 37,271 (1974); Solange II BVerfGE 73,339 (1986) — fundamental-rights reservation"]

# Ultra-vires review — a GENUINE PAIR (§4.7 preferred form), opposite polarity,
# same triple, different claimants:
assert de:bverfg : de:bverfg  reviews  eu:regulation
    [status = contested,
     basis = "ultra-vires review: Honeywell BVerfGE 126,286 (2010) test; PSPP/Weiss 2 BvR 859/15 (5 May 2020) applied it against ECB + CJEU Weiss C-493/17"]
assert eu:cjeu : NOT de:bverfg reviews eu:regulation
    [status = asserted,
     basis = "Foto-Frost, Case 314/85 — the CJEU alone may declare an EU act invalid; a national court has no competence to review/disapply a regulation"]

# Constitutional-identity review — stands as a LONE reservation-assertion (§4.7
# lone form) against the order's default settled position; its doctrinal counter is
# the CJEU primacy assertion above.
assert de:bverfg : de:bverfg  reviews  eu:primary-law
    [status = contested,
     basis = "constitutional-identity review: Lisbon BVerfGE 123,267 (2009); anchored in Art 79(3) GG eternity clause"]
```

The `eu:cjeu`-affirming and `de:bverfg`-denying assertions over the same triple
form a **contested edge** — the ultra-vires triple above is the clean paired case
(BVerfG `reviews eu:regulation` vs CJEU `NOT … reviews …`, Foto-Frost). A resolver
walking the graph (§5) returns `contested / unresolved` on the pair and hands off;
the grammar records the standoff faithfully and decides nothing. This is exactly
the representable disagreement the task requires: one relation, two conflicting
claimants.

## What the two `resolution_mode` values buy

- EU → national conflict: `disapply` (national norm survives, is not applied).
- Federal → Land conflict (`de.md`): `invalidate` (Land norm is void, Art 31 GG).

One grammar, one relation type (`has-primacy-over`), two grounded modes — no
special-casing.
