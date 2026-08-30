<!--
SPDX-FileCopyrightText: 2026 flxk1
Copyright 2026 flxk1 · STATUS: PROPOSED

SPDX-License-Identifier: Apache-2.0
-->
# Instantiation 2 — Germany, a federal civil-law national order

Proves the SAME grammar carries a codified federal state. Two vertical axes
visibly separate here: the **normative-rank** ladder (GG ▷ statute ▷ ordinance ▷
by-law) and the **territorial** ladder (federal ▷ Land), joined only by the
Art 31 GG supremacy edge.

## System + ladders

```lt
system de  tradition civil  powers separation-tripartite  levels de-levels  ranks de-ranks

# de-levels (territorial):  federal=0  land=1  (kommunal self-administration under Art 28(2) GG)
# de-ranks (normative — the Normenhierarchie):
#   grundgesetz=0  formal-statute=1  rechtsverordnung=2  satzung=3
```

## Levels (territorial axis)

```lt
level de:federal  system de  rank 0  contains de:land
level de:land     system de  rank 1
```

## Organs

```lt
organ de:bundestag   system de  level de:federal  powers {legislative}    # Art 38-48 GG
organ de:bundesrat   system de  level de:federal  powers {legislative}    # Länder chamber, Art 50 GG
organ de:bundesregierung system de level de:federal powers {executive}    # Art 62 GG
organ de:bverfg      system de  level de:federal  powers {judicial}       # Federal Constitutional Court, Art 92-94 GG
organ de:bundespraesident system de level de:federal powers {executive-ceremonial}  # promulgation, Art 82 GG
organ de:landtag     system de  level de:land    powers {legislative}     # Land parliament
```

## Instruments (normative-rank axis)

```lt
instrument de:grundgesetz     system de  rank 0  origin de:pouvoir-constituant   # the Basic Law
instrument de:formal-statute  system de  rank 1  origin de:bundestag             # Parlamentsgesetz
instrument de:rechtsverordnung system de rank 2  origin de:bundesregierung       # delegated legislation, Art 80 GG
instrument de:satzung         system de  rank 3  origin de:kommune               # autonomous by-law, Art 28(2) GG
instrument de:land-statute    system de  rank 1  origin de:landtag               # Landesrecht, same rank tier, different level

rel de:grundgesetz      outranks  de:formal-statute        # lex superior
rel de:formal-statute   outranks  de:rechtsverordnung
rel de:rechtsverordnung outranks  de:satzung
rel de:rechtsverordnung derives-authority-from de:formal-statute
    [basis = "Art 80(1) GG — enabling statute must fix content, purpose and scope"]
```

## Federal supremacy — territorial axis meets rank via `resolution_mode = invalidate`

```lt
# Art 31 GG: Bundesrecht bricht Landesrecht — conflicting Land law is VOID, not
# merely disapplied. This is the contrast with EU primacy (§4.1 disapply).
rel de:formal-statute  has-primacy-over  de:land-statute  [resolution_mode = invalidate, basis = "Art 31 GG"]
```

## Competence catalogue (Arts 70–74 GG)

```lt
competence de:foreign-affairs   system de  allocation federal-exclusive  holder de:federal  # Art 73(1) GG
competence de:defence           system de  allocation federal-exclusive  holder de:federal  # Art 73(1) GG
competence de:civil-law         system de  allocation concurrent         holder de:federal  # Art 74(1)(1) GG (konkurrierend)
competence de:environment       system de  allocation concurrent         holder de:federal  # Art 74(1)(24) GG
competence de:police            system de  allocation reserved           holder de:land     # residual, Art 70(1) GG
competence de:education         system de  allocation reserved           holder de:land     # Kulturhoheit der Länder

# Art 72 GG: on a concurrent competence the Länder may legislate only so long as
# and to the extent the Federation has not — modelled as a deontic rule that
# QUANTIFIES OVER this allocation (§8.2), not stored here.
```

## Constitutional review + checks

```lt
rel de:bverfg     reviews      de:formal-statute   [basis = "abstract/concrete review, Art 93, Art 100 GG"]
rel de:bverfg     can-override de:formal-statute   [basis = "may declare a statute void (nichtig)"]
rel de:ordinary-court must-refer-to de:bverfg      [basis = "Art 100(1) GG konkrete Normenkontrolle — a court convinced a statute is unconstitutional must refer"]
rel de:bundesrat  can-veto     de:formal-statute   [basis = "Zustimmungsgesetze — consent bills, Art 77-78 GG"]
rel de:bundestag  can-override de:bundesrat        [basis = "Einspruchsgesetze — objection can be overridden, Art 77(4) GG"]
rel de:bundespraesident reviews de:formal-statute  [basis = "formal promulgation scrutiny, Art 82 GG"]
```

## Balance query result (§6)

- `no-organ-unchecked`: Bundestag is checked by Bundesrat (veto) and BVerfG
  (review); BVerfG is apex (no inbound check) → reported *apex*, legitimate.
- Two-axis separation is explicit: `de:land-statute` sits at rank 1 (same
  normative tier as a federal statute) but at territorial level `land`; only the
  Art 31 GG edge orders them. Rank and level are genuinely distinct here.
