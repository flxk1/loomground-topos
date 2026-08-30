<!--
SPDX-FileCopyrightText: 2026 flxk1
Copyright 2026 flxk1

SPDX-License-Identifier: Apache-2.0
-->
# Grounding notes — Loomground Topos (legal-system topology grammar)

**STATUS: RATIFIED (v0.1), published as [`loomground-topos`](https://github.com/flxk1/loomground-topos).**
All loomground reads during authoring were read-only; no other plane was edited. The
per-jurisdiction *grounded* instances that consume this grammar stay local (the moat);
this repository is the grammar — the invariants — only.

---

## 1. What I read for grounding (paths + what each gave me)

All under `/Users/rafelixkrone/Documents/Claude/Projects/loomground-repos/`.

| path | what it gave the design |
|---|---|
| `loomground-governance/standard/grammar/loomground.ebnf` | the netlist idiom I mirrored: ISO/IEC 14977 EBNF, nodes + typed cords, the parse-vs-apply split, `id` lexeme rules, `[grant clause]`/`prop`-style trailers |
| `loomground-governance/standard/schema/patch.schema.json` | the abstract-graph JSON shape (nodes[] with `class`, cords[] with `from`/`to`/`type`) that my appended interchange schema mirrors |
| `loomground-governance/standard/schema/observation.schema.json` | the projection discipline (some fields materialised on projection; canonical member ordering) |
| `loomground-governance/standard/vocabulary/grades.json` | **the load-bearing pattern**: *"policy supplies the levels, their meanings, and their order (remappable); the language owns only the comparison rule."* My whole §5/§7 ladder-vs-comparison split is this pattern applied to legal rank/level |
| `loomground-governance/standard/vocabulary/node-classes.json` | the 4-class + singleton-frame shape (actor/human/gate/master); I reused it as system(frame)+organ/level/instrument/competence |
| `loomground-governance/standard/language-card.json` | the litmus (language/policy/host), `well_formedness` list style, `out_of_scope` list style, URN form — mirrored in §9/§10/§11 |
| `loomground-governance/standard/companions/claim-axes/COMPANION.md` | the "companion vocabulary, tool-owned adapters, string-agreement coupling" discipline that governs my §8 seams |
| `loomground-deontic/README.md` + `src/deontic/artifacts/grammar/deontic.ebnf` | the plane boundary: deontic owns `O`/`P`/`F` and *"flags candidate conflicts, never resolving them"*; and the explicit line *"'Right' is not a modality — it lives in the incident layer"* → my §8.2 Hohfeld-power seam |
| `loomground-versum/README.md` | claim graph Source→Claim→Concept; profile-supplied closed vocabulary; Federation-5D; *"provenance and claims never silently move or merge"* → my §4.7/§5.3 non-merge discipline |
| `loomground-versum/src/versum/profiles/law_eu.py` | **the anchor I generalise**: `INSTRUMENT_RANK = {"treaty:eu":0,…,"case-law:cjeu":None}` — a single hardcoded vertical rank slice, with `None` = not-yet-grounded. §7.3/§8.1 turn this into a `rank_ladder` projection |
| `loomground-versum/src/versum/profile.py` | the `Profile` dataclass carrying `instrument_rank`, `namespace` (`dls`), `source_identifiers` (URN scheme), `predicate_dimensions` — the seam surface I extend in §8.1 |
| `loomground-versum/src/versum/nd.py` (`_CORE_SYSTEM`) | the `versum.context` nD axes (`jurisdiction`, `time`, `instrument`, `domain`, …) I extend with `versum.topology.*` in §8.1 |
| `loomground-versum/src/versum/sync.py` (nd-context stamping) | **confirmed the temporal reality**: stamping is `"time": prov.get("detected_year")` — a scalar YEAR (a point), even though `nd.py` declares the `time` axis `value_type:"interval"`. This gap is the §8.1/§5.1 temporal caveat |
| `loomground-versum/src/versum/write.py` | the source sidecar/registry fields (`urn`, `verification`, `library`, `canonical_urn`) — the concrete stamp record §8.1 extends |

---

## 2. Legal doctrines relied on (real citations)

Citations are given by case name + docket/number and, where used, the German
`BVerfGE` volume,page or UK neutral citation. **I am confident in the case
names, numbers, and holdings; exact reporter page numbers and dates should be
verified against an authoritative reporter before ratification** (see §3).

**EU primacy / effect / competence**
- *Costa v ENEL*, Case 6/64 — primacy of EU law over national law.
- *Internationale Handelsgesellschaft*, Case 11/70 — primacy even over national
  constitutional (fundamental-rights) provisions.
- *Simmenthal*, Case 106/77 — national court must **set aside** (disapply)
  conflicting national law; the disapply-not-annul point (§4.1).
- *Van Gend en Loos*, Case 26/62 — direct effect (rights invocable nationally).
- *Van Duyn v Home Office*, Case 41/74 — vertical direct effect of a directive.
- *Marshall v Southampton AHA*, Case 152/84 — **no** horizontal direct effect of
  a directive; *Faccini Dori*, Case C-91/92 — confirmed.
- *Francovich and Bonifaci*, Cases C-6/90 & C-9/90 — state liability for
  non-transposition (my §4.3 `gap` state).
- **TFEU**: Art 288 (regulation directly applicable / directive binding as to
  result); Art 267 (preliminary reference); Arts 2–6 (exclusive/shared/
  supporting competence); Art 263 (annulment); Art 234 (censure motion); Arts
  14/16/17/19 TEU (Parliament/Council/Commission/CJEU); Art 5 TEU (conferral,
  subsidiarity, proportionality); Arts 127–133 TFEU (ECB/monetary); Art 285
  (Court of Auditors); Reg 2017/1939 (EPPO).

**Germany**
- **Grundgesetz**: Art 20 (federal, democratic, rule-of-law state); Art 28(2)
  (municipal self-administration → Satzung); Art 31 (*Bundesrecht bricht
  Landesrecht* → `invalidate`); Arts 70–74 (federal/concurrent/reserved
  competence); Art 72 (Länder legislate on concurrent competence only absent
  federal use); Art 80(1) (Rechtsverordnung needs content/purpose/scope in the
  enabling statute); Art 79(3) (eternity clause); Arts 92–94 (BVerfG); Art 93
  (abstract review); Art 100(1) (concrete review / *Richtervorlage*); Arts 77–78
  (Zustimmungs-/Einspruchsgesetze); Art 82 (promulgation).
- *Solange I*, BVerfGE 37, 271 (1974); *Solange II*, BVerfGE 73, 339 (1986) —
  fundamental-rights review reservation over EU acts.
- *Honeywell*, BVerfGE 126, 286 (2010) — ultra-vires review test (manifest +
  structurally significant).
- *PSPP / Weiss*, BVerfG 2 BvR 859/15 et al., 5 May 2020 — first BVerfG
  ultra-vires finding, against the ECB and CJEU *Weiss* (Case C-493/17;
  preceded by *Gauweiler*, Case C-62/14).
- *Lisbon*, BVerfGE 123, 267 (2009) — constitutional-identity review.

**United Kingdom**
- Parliamentary sovereignty — A.V. Dicey, *Introduction to the Study of the Law
  of the Constitution* (1885); *R (Jackson) v Attorney General* [2005] UKHL 56.
- Constitutional statutes not impliedly repealable — *Thoburn v Sunderland CC*
  [2002] EWHC 195 (Admin) (Laws LJ); *R (HS2) v Secretary of State* [2014] UKSC 3.
- Judicial review of executive action — *Council of Civil Service Unions v
  Minister for the Civil Service (GCHQ)* [1985] AC 374.
- EU-law supremacy pre-Brexit — European Communities Act 1972; *R v Secretary of
  State ex p Factortame (No 2)* [1991] UKHL 7 (disapplication of an Act).
- Brexit — *R (Miller) v Secretary of State* [2017] UKSC 5; European Union
  (Withdrawal) Act 2018 (**s.5** disapplied the supremacy of EU law for
  post-IP-completion-day law, and defined retained EU law); European Union
  (Withdrawal Agreement) Act 2020 (**s.38** reaffirming parliamentary
  sovereignty); Retained EU Law
  (Revocation and Reform) Act 2023 (ended EU-law supremacy generally; "retained"
  → "assimilated" law).

**United States** (used only as inline contrast, not a full instantiation)
- Supremacy Clause, US Const. Art. VI, cl. 2 (conflicting state law **void** —
  contrast EU disapply); *Marbury v Madison*, 5 U.S. (1 Cranch) 137 (1803)
  (judicial review); *McCulloch v Maryland*, 17 U.S. (4 Wheat.) 316 (1819);
  Tenth Amendment (reserved powers); *Youngstown Sheet & Tube v Sawyer*, 343
  U.S. 579 (1952) (separation of powers).

**Conflict canons** — *lex superior derogat legi inferiori*; *lex specialis
derogat legi generali*; *lex posterior derogat legi priori*; and the mixed-case
maxim *lex posterior generalis non derogat legi priori speciali* (§5.2). These
are classical maxims of legal method, not statutory provisions.

---

## 3. What I was UNCERTAIN about (flagged, not papered over)

1. **Exact reporter pages / dates AND statute section numbers.** Case *names,
   numbers, and holdings* I am confident in. The precise `BVerfGE volume, page`,
   the exact dates of some decisions, **and the section numbers of UK statutes**
   are from memory and should be checked against an authoritative source before
   this is cited in any durable artifact. Specifically verify: Solange II page
   (339), Honeywell page (286), Lisbon page (267), the full PSPP docket, and — on
   the UK side — that **s.5 of the European Union (Withdrawal) Act 2018** carries
   the disapplication of EU-law supremacy (corrected here from an earlier draft
   that mis-attributed it to the 2020 Act) and that **s.38 of the European Union
   (Withdrawal Agreement) Act 2020** carries the sovereignty affirmation.
   **Do not treat the pinpoint citations or section numbers as verified.**
2. **The 3-before-4 canon precedence (specialis before posterior) is genuinely
   contested legal theory** for the *later-general vs earlier-special* case
   (§5.2). I did not invent a resolution; I made the default explicit and
   remappable and made deadlock return `unresolved`. This is a design choice to
   be ratified, not a settled legal truth.
3. **`source_class` as a named field.** The contract facts speak of
   `source_class` anchored to `law_eu.INSTRUMENT_RANK`. In the versum code I read,
   the concrete anchor is the `INSTRUMENT_RANK` dict and its `instrument`
   nD-axis / profile field; I did **not** find a literal `source_class` column in
   the versum core I read. I have treated "source_class" as the instrument-class
   key of that ladder (e.g. `regulation:eu`). If `source_class` is a distinct
   field elsewhere (e.g. in the legal-dept `dls` profile or a consumer contract I
   did not read), the §8.1 mapping should be re-checked against it.
4. **The `time` axis mismatch.** `nd.py` declares `time` as `value_type:
   "interval"` with a `precedes` primitive, but `sync.py` stamps a scalar year.
   I read this as: the interval *schema slot* exists but the *stamping* is a
   point — consistent with the contract fact that interval support is
   "pending, not-yet-landed." If interval stamping has in fact landed since, §5.1
   step 4 and §8.1 point-precision caveats can be relaxed.
5. **Tradition labels.** I labelled the EU `hybrid`, Germany `civil`, UK
   `common`. These are coarse and only a non-functional label in the model (they
   switch nothing). Flagged so no one reads legal weight into them.
6. **US as contrast only.** I instantiated UK (not US) as the required common-law
   system, and used US only for the void-vs-disapply contrast. If a full US
   instantiation is wanted, it is straightforward but not written here.

---

## 4. Open questions for the loomground owner + Felix

1. **Sibling repo vs companion — RESOLVED.** Placed as the standalone Loomground-plane
   repo `loomground-topos` (plane-parity with deontic/versum, over the claim-axes
   companion precedent), per `PLACEMENT.md`.
2. **URN scheme for topology nodes.** I proposed `urn:topo:<system>:<class>:<id>`
   alongside the legal-source `urn:dls:<scheme>:<id>`. Does the family want a
   single namespace registry entry, and which version tag (`urn:loomground:topos:0.1:…`)?
3. **Where does the `rank_ladder` live** — does `law_eu.py`'s `INSTRUMENT_RANK`
   get *replaced* by a reference into a topology artifact (my §8.1 proposal), or
   does the topology graph *import* the profile's dict? Direction of dependency
   between versum-profile and topology must be set to respect
   `repo-standards/topology.md` plane rules (I did not modify anything to find out).
4. **Interval temporal axis.** Should Topos *block* on the pending interval axis
   for lex-posterior/temporal-validity, or ship with point-precision and upgrade?
   I designed for the latter (graceful cap) but flagged the dependency.
5. **Contested-edge consumers.** Who reads a `status = contested` pair — the
   solver? a `policy-compliance` lens? The model represents the standoff; the
   *consumption* contract (how a downstream reasoner is expected to behave on an
   unresolved edge) is out of scope here and needs its own agreement.
6. **Deontic coupling surface.** §8.2 couples by string agreement (a topology
   node id appears as a deontic bearer/scope). The exact reference syntax should
   be co-designed with the deontic pack owner before either surface is frozen,
   exactly as deontic co-designs its `SolverProjection` with solver.
7. **Case-law / soft-law grounding.** The model treats ungrounded source-classes
   as not-yet-grounded (§5.3). Confirm this is the desired failure mode for a
   `policy-compliance` gate (fail-closed / quarantine, never permissive) — it
   matches the RVND posture but should be ratified for this plane.
8. **Closed relation enum (§3.5).** Relation *types* are a fixed enum (unlike the
   data-parameterised powers/levels/ranks/allocation), so treaty consent,
   accession, reservation, and withdrawal are representable only implicitly
   (edge presence/removal + `basis`). Should any of these earn first-class named
   relation types, and if so which — a `consents-to`/`accedes-to`/
   `reserves-against`/`withdraws-from` set — or does the implicit encoding
   suffice for v1? A ratified vocabulary change either way.

---

## 5. Files in this proposal

```
legal-topology-grammar/
├── SPEC.md                    the full specification (model, 4 neutrality
│                              principles, conflict precedence, coupling model,
│                              contested-relation mechanism, two plane-seams)
├── grammar-sketch.ebnf        concrete .lt netlist EBNF (family idiom) +
│                              appended abstract-graph JSON interchange schema;
│                              header states why EBNF was chosen as primary
├── examples/
│   ├── eu.md                  the EU order (organs, ranks, competence)
│   ├── de.md                  federal civil-law Germany (GG▷statute▷VO▷Satzung, Art 31/70-74 GG)
│   ├── eu-de-coupling.md      the §4 coupling edges incl. the contested BVerfG↔CJEU edge
│   └── uk.md                  common-law UK (sovereignty, no codified constitution, post-Brexit)
└── GROUNDING-NOTES.md         this file
```

This grammar is **ratified and published** as `loomground-topos` (a standalone
Loomground-plane repo). The §4 questions that remain open after ratification — the URN
scheme, the rank-ladder projection direction, and the interval temporal axis — stay
with the loomground owner and Felix.
