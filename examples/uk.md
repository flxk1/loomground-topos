<!--
SPDX-FileCopyrightText: 2026 flxk1
Copyright 2026 flxk1 · STATUS: PROPOSED

SPDX-License-Identifier: Apache-2.0
-->
# Instantiation 4 — the United Kingdom, a common-law order

The stress test for jurisdiction-neutrality. The UK has **no codified
constitution**, **parliamentary sovereignty** rather than a norm outranking
statute, and a **changed post-Brexit** relationship to EU law. The claim to
prove: the same grammar carries this *without special-casing* — the differences
show up as different *values*, not different *machinery*.

## System + ladders

```lt
system uk  tradition common  powers separation-tripartite-fused  levels uk-levels  ranks uk-ranks

# uk-levels: uk-parliament=0  devolved=1  (Scotland/Wales/NI)  local=2
# uk-ranks — the key difference: NO supreme written constitution at rank 0.
#   The apex instrument IS the Act of Parliament.
#     act-of-parliament=0   statutory-instrument=1   by-law=2
#   "constitutional statutes" are Acts flagged, not a separate higher rank
#   (Thoburn v Sunderland [2002] EWHC 195; HS2 [2014] UKSC 3).
```

## Organs (note the FUSED powers — a different separation profile)

```lt
organ uk:parliament   system uk  level uk:uk-parliament  powers {legislative}
    # Crown-in-Parliament: the sovereign law-maker (Dicey). No organ outranks it.
organ uk:government    system uk  level uk:uk-parliament  powers {executive}
    # drawn FROM Parliament — powers are fused, not separated; the "-fused"
    # power_catalogue profile is why this needs no special machinery
organ uk:uksc          system uk  level uk:uk-parliament  powers {judicial}
    # UK Supreme Court — reviews executive action, but historically CANNOT
    # strike an Act of Parliament (contrast BVerfG / SCOTUS)
organ uk:scottish-parliament system uk level uk:devolved powers {legislative}  # Scotland Act 1998
```

## Instruments — sovereignty means the apex is a statute, at rank 0

```lt
instrument uk:act-of-parliament   system uk  rank 0  origin uk:parliament
instrument uk:statutory-instrument system uk rank 1  origin uk:government   # delegated legislation
instrument uk:by-law              system uk  rank 2  origin uk:local-authority

rel uk:act-of-parliament   outranks  uk:statutory-instrument
rel uk:statutory-instrument outranks uk:by-law
rel uk:statutory-instrument derives-authority-from uk:act-of-parliament
    [basis = "delegated under a parent Act; ultra-vires SIs are quashable"]
```

## What differs, and why NO special-casing is needed

1. **No rank-0 constitution.** The `rank_ladder` simply puts
   `act-of-parliament` at rank 0. The grammar never assumed a constitution sat
   there — that was always a *policy* value (§7.3). Germany fills rank 0 with
   `grundgesetz`; the UK fills it with the Act. Same slot, different value.

2. **Sovereignty = an apex organ, a legitimate balance finding, not a defect.**

```lt
# The UKSC reviews executive action but not primary legislation:
rel uk:uksc  reviews  uk:government            [basis = "judicial review of executive action, GCHQ [1985]"]
rel uk:uksc  reviews  uk:statutory-instrument  [basis = "SIs may be quashed as ultra vires"]
# NOTE: there is deliberately NO `uk:uksc reviews uk:act-of-parliament` edge.
```
   Balance query `no-organ-unchecked` reports `uk:parliament` as **apex /
   unchecked** — and that is the *correct* description of parliamentary
   sovereignty (Dicey; *R (Jackson) v Attorney General* [2005] UKHL 56), exactly
   as §6 anticipates an apex organ as a finding, not an error.

3. **The post-Brexit relationship change is an edge rewrite, not new machinery.**

```lt
# PRE-Brexit (historical, for contrast): EU law had primacy and could disapply
# an Act of Parliament — Factortame (No 2) [1991] UKHL 7 — via the European
# Communities Act 1972. Modelled exactly as the EU-DE primacy edge:
#   rel eu:regulation has-primacy-over uk:act-of-parliament [resolution_mode = disapply, basis = "ECA 1972; Factortame (No 2)"]

# POST-Brexit: the primacy edge is REMOVED. EU law that remained became
# "retained EU law", now "assimilated law", SUBORDINATE to Acts of Parliament.
instrument uk:assimilated-law  system uk  rank 1  origin uk:parliament
    [basis = "EU(Withdrawal) Act 2018; Retained EU Law (Revocation and Reform) Act 2023"]
rel uk:act-of-parliament  outranks  uk:assimilated-law
    [basis = "s.5 European Union (Withdrawal) Act 2018 disapplied EU-law supremacy for post-IP-completion-day law; REUL Act 2023 ended supremacy generally"]
# The coupling edge to eu:* is gone; sovereignty reaffirmed by s.38 of the
# European Union (Withdrawal Agreement) Act 2020.
```
   The Brexit transition is: delete one `has-primacy-over` coupling edge, add one
   `outranks` intra-order edge. No node class, relation type, or resolution mode
   was added. The grammar carried a supranational-primacy order and a
   restored-sovereignty order with the same parts.

## Comparison the model now makes queryable across all four instantiations

| feature | EU | Germany | UK |
|---|---|---|---|
| rank-0 instrument | treaty:eu | grundgesetz | act-of-parliament |
| apex organ (unchecked) | cjeu | bverfg | parliament |
| supremacy `resolution_mode` | disapply (over national) | invalidate (Art 31, over Land) | (none post-Brexit) |
| can a court void primary law? | n/a | yes (BVerfG) | no |
| powers catalogue | separation-extended (+monetary/audit/prosecutorial) | separation-tripartite | separation-tripartite-fused |

Every row is a *value* in a policy-supplied ladder or catalogue. The machinery —
nodes, typed relations, assertion wrapper, precedence rule, balance queries — is
identical. That identity is the neutrality claim, demonstrated.
