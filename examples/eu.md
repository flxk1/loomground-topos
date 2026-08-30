<!--
SPDX-FileCopyrightText: 2026 flxk1
Copyright 2026 flxk1 · STATUS: PROPOSED

SPDX-License-Identifier: Apache-2.0
-->
# Instantiation 1 — the EU legal order

Concrete node/edge listing in the `.lt` netlist surface. Policy, not language
(§9): every value here is a jurisdiction's choice. Grounding citations in `#`
comments.

## System + ladders

```lt
system eu  tradition hybrid  powers separation-extended  levels eu-levels  ranks eu-ranks

# eu-levels (level_ladder.json):  supranational=0  (single-level at EU tier;
#   national/regional/local belong to the member-state systems, reached by coupling)
# eu-ranks (rank_ladder.json), generalising law_eu.INSTRUMENT_RANK:
#   treaty:eu=0  charter:eu=0
#   regulation:eu=1  directive:eu=1  decision:eu=1
#   recommendation:eu=2  opinion:eu=2
#   case-law:cjeu=null                 # not-yet-grounded (§5.3), NOT rank 0
```

## Organs (powers are a PARAMETER — §5.6)

```lt
organ eu:european-parliament  system eu  level eu:supranational  powers {legislative}       # co-legislator, Art 14 TEU
organ eu:council              system eu  level eu:supranational  powers {legislative}       # co-legislator, Art 16 TEU
organ eu:commission           system eu  level eu:supranational  powers {executive, legislative-initiative}  # Art 17 TEU
organ eu:cjeu                 system eu  level eu:supranational  powers {judicial}           # Art 19 TEU
organ eu:ecb                  system eu  level eu:supranational  powers {monetary}           # Arts 127-133 TFEU — the "monetary" label is why powers must be a parameter
organ eu:court-of-auditors    system eu  level eu:supranational  powers {audit}              # Art 285 TFEU — an "audit" power
organ eu:eppo                 system eu  level eu:supranational  powers {prosecutorial}       # Reg 2017/1939 — a "prosecutorial" power
```

## Instruments (normative-rank axis — separate from the territorial axis)

```lt
instrument eu:primary-law   system eu  rank 0  origin eu:member-states     # TEU/TFEU/Charter
instrument eu:regulation    system eu  rank 1  origin eu:parliament-council  directly-applicable
instrument eu:directive     system eu  rank 1  origin eu:parliament-council  direct-effect vertical
instrument eu:decision      system eu  rank 1  origin eu:commission
instrument eu:recommendation system eu rank 2  origin eu:commission          # soft law — NOT yet grounded in versum
instrument eu:cjeu-judgment system eu  rank null origin eu:cjeu              # case-law: source-licensing-gated, not-yet-grounded
```

## Internal vertical order

```lt
rel eu:primary-law  outranks  eu:regulation      # primary ▷ secondary
rel eu:primary-law  outranks  eu:directive
rel eu:primary-law  outranks  eu:decision
rel eu:regulation   outranks  eu:recommendation  # binding ▷ soft
```

## Competence catalogue (Arts 2–6 TFEU)

```lt
competence eu:customs-union      system eu  allocation exclusive   holder eu:union   # Art 3(1)(a)
competence eu:competition-rules  system eu  allocation exclusive   holder eu:union   # Art 3(1)(b)
competence eu:monetary-policy    system eu  allocation exclusive   holder eu:union   # Art 3(1)(c), euro area
competence eu:internal-market    system eu  allocation shared      holder eu:union   # Art 4(2)(a)
competence eu:environment        system eu  allocation shared      holder eu:union   # Art 4(2)(e)
competence eu:culture            system eu  allocation supporting  holder eu:union   # Art 6(c)
competence eu:tourism            system eu  allocation supporting  holder eu:union   # Art 6(d)

rel eu:primary-law  confers-competence  eu:customs-union
rel eu:primary-law  confers-competence  eu:internal-market
rel eu:primary-law  confers-competence  eu:culture
```

## Horizontal checks + court dialogue

```lt
rel eu:european-parliament  co-equal-with  eu:council             # ordinary legislative procedure, Art 294 TFEU
rel eu:cjeu     reviews    eu:commission                          # judicial review of acts, Art 263 TFEU
rel eu:cjeu     reviews    eu:regulation                          # annulment action, Art 263 TFEU
rel eu:european-parliament  can-veto  eu:commission               # motion of censure, Art 234 TFEU (dissolves the College)
rel eu:european-parliament  appoints  eu:commission                # consent to the College, Art 17(7) TEU
```

## Balance query result (§6) — illustrative

- `no-organ-unchecked`: `eu:commission` is checked (Parliament censure + CJEU
  review); `eu:cjeu` has **no inbound check-edge** → reported *unchecked / apex*
  (a finding to surface, not an error — a supreme court commonly is apex).
- `mutual-constraint cycle`: Parliament ⇄ Commission (appoints / can-veto) is a
  two-node balance cycle.
