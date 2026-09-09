<!--
SPDX-FileCopyrightText: 2026 flxk1

SPDX-License-Identifier: CC-BY-4.0
-->
<!-- Copyright 2026 flxk1 -->
<!-- STATUS: RATIFIED (v0.1) — published as loomground-topos. -->

# Loomground Topos — the legal-system topology grammar

**A jurisdiction-neutral language for the STRUCTURE of legal authority:** who
holds which power, at which level, through which instruments, over which
subject matter, and how those powers check one another — flexible enough to
carry any legal system and the couplings between systems.

> **Status: ratified, v0.1.** Published as the standalone Loomground-plane grammar
> [`loomground-topos`](https://github.com/flxk1/loomground-topos). Where the design
> depends on a not-yet-sequenced loomground change (the temporal-interval axis, and the
> `law_eu` / mrl rank-ladder projection), that dependency is called out inline and again
> in `GROUNDING-NOTES.md`.

---

## 0. Where this sits in the plane family

The loomground family separates planes as a first principle. This grammar
occupies the **structure** plane and is deliberately thin:

| plane | question it answers | artifact |
|---|---|---|
| **topology** (this grammar) | *who may make / unmake / apply which norms, at which level, and how do they check each other?* | a legal-order graph |
| **deontic** (`loomground-deontic`) | *what is permitted / obliged / forbidden WITHIN that structure?* | `O`/`P`/`F` statements |
| **versum** (`loomground-versum`) | *what does a given source actually provide?* | a claim graph (Source→Claim→Concept) |

The three never merge. This document specifies the **seams** between them
(§8), it does not absorb their content. Topology carries no `O`/`P`/`F`
*conduct* modality (that is deontic) and stores no statute text or claim spans
(that is versum's, and the corpus text stays local — the moat). It carries only
*structural capacity*: the standing to create, rank, and apply norms.

> **On the `may-refer-to` / `must-refer-to` distinction (resolved here).** The
> referral edges (§3.2, §4.6) carry a *may* vs *must* that looks deontic but is
> not an `O`/`P`/`F` conduct norm. It is a **structural** property of the
> organ–channel pairing: *is the referral channel merely available to this organ,
> or is its use a condition of the organ's own competence to decide?* — the
> Hohfeld power/liability texture of the channel itself (§8.2), fixed by the
> constitutive rule (Art 267(2) vs 267(3) TFEU), not a rule about how anyone
> *ought to behave*. A deontic statement may then quantify over that structural
> fact (e.g. `O(court-of-last-instance : refer)` referencing the `must-refer-to`
> edge). So §0's "no `O`/`P`/`F`" stands for conduct modality; the referral
> may/must is a structural capacity marker, and this is the single place the
> apparent tension is resolved.

### 0.1 Conventions inherited from the family

Read alongside `loomground-governance/standard/`. This grammar mirrors its
conventions deliberately so it reads as one family:

- **Nodes + typed edges.** The governance language is *nodes* (`actor`,
  `human`, `gate`, `master`) plus typed *cords* (`authority`, `pipe`,
  `egress`). This grammar is *nodes* (§2) plus typed *relations* (§3), the
  same shape.
- **Policy owns the vocabulary; the language owns the comparison.** Exactly the
  `vocabulary/grades.json` pattern: *"policy supplies the levels, their
  meanings, and their order (remappable); the language owns only the comparison
  rule."* Here, **a jurisdiction supplies its organs, levels, instrument ranks,
  and competence catalogue; this language owns only the conflict-resolution
  comparison** (§5) and the balance/well-formedness queries (§6).
- **Parse-vs-apply split.** As in `loomground.ebnf`, the concrete grammar
  parses leniently (any `id` is accepted); membership in a closed set and the
  structural invariants are checked at *apply*, not at *parse*. An off-ladder
  rank or an unknown organ parses and is rejected at apply, exactly as an
  off-domain risk value is in governance.
- **Remappable vocabulary as data.** Ladders and catalogues ship as JSON
  companions (§7), the way `grades.json`, `risk.json`, `roles.json` do.
- **URN identity.** `urn:<ns>:<scheme>:<id>`, reusing the versum `dls`
  namespace for legal sources (§8.1).
- **Litmus.** The governance litmus (*regulation names it → language;
  deployment chooses values → policy; runtime does it → host*) applies here
  unchanged (§9).

---

## 1. The core idea

A **legal order** (a `system`) is a directed graph of four node kinds and a
small set of typed relations. The relations split into three families —
**vertical** (hierarchy), **horizontal** (separation and mutual check), and
**coupling** (inter-order) — plus one meta-mechanism, **assertion**, that lets
any relation be *claimed* by a named organ rather than stated as settled fact
(§4). Balance is not a stored node; it is an emergent, queryable property of
the check-edge subgraph (§6).

Nothing about branches, ranks, or levels is hardcoded. "Three powers,"
"constitution above statute," "supranational above national" are all
*instantiations* a jurisdiction declares — never constants of the language
(§0.1, §5.6). This is what lets one grammar carry the EU order, a federal
civil-law state, and an uncodified common-law constitution without
special-casing (§7 of the task; the worked instantiations are in `examples/`).

---

## 2. Nodes

Four node classes carry the structure, inside a fifth enclosing frame, the
`system`. (Compare governance's four classes with `master` as the singleton
frame; here `system` is the frame.)

| class | is | key properties |
|---|---|---|
| `system` | a distinct legal order (a frame + a node addressable by coupling edges) | `id`, `tradition` (civil / common / customary / religious / hybrid — a label, not a switch), `power_catalogue` (ref §7.1), `level_ladder` (ref §7.2), `rank_ladder` (ref §7.3) |
| `organ` | a power-holding body | `system`, `level` (ref to a `level` node), `powers` (set of power-labels from the system's catalogue — the *parameterised* branch, §5.6), `party` (optional, who currently occupies it) |
| `level` | a vertical territorial stratum | `system`, `level_rank` (ordinal in the territorial ladder), `contains` (the stratum immediately below) |
| `instrument` | a norm-type that carries a rank | `system`, `rank` (ordinal in the normative-rank ladder), `origin_organ` (which organ enacts it), `direct_effect` (optional: `none`/`vertical`/`horizontal`, §4.5), `directly_applicable` (optional bool, §4.2) |
| `competence` | a subject-matter domain | `system`, `allocation` (a value of the system's allocation vocabulary, e.g. `exclusive`/`shared`/`supporting`/`reserved`), `holder` (organ or level the domain is allocated to) |

Two vertical axes live on two different nodes on purpose (neutrality principle
2, §5.6): the **territorial** axis is the `level_rank` on `level`; the
**normative-rank** axis is the `rank` on `instrument`. They are never the same
field and are often, but not always, aligned.

> **Surface keyword note.** In the abstract model the two fields are named
> distinctly (`level_rank` vs `rank`). The concrete `.lt` surface writes *both*
> with the keyword `rank` (a `rank` on a `level` decl vs a `rank` on an
> `instrument` decl); **the enclosing node class disambiguates** — `rank` under
> `level …` sets `level_rank`, `rank` under `instrument …` sets the normative
> rank. They remain two separate fields; only the surface keyword is shared.

`organ`, `instrument`, `level`, and `competence` all name their `system`, so a
graph may hold several orders at once and the coupling edges (§4) run between
them.

---

## 3. Relations (typed edges)

A relation is a directed, typed edge. Direction is *from the active/superior
party to the passive/inferior party* by convention (the checker points at the
checked; the higher rank points at the lower). Three families:

### 3.1 Vertical (hierarchy)

| relation | from → to | meaning | grounding |
|---|---|---|---|
| `outranks` | instrument → instrument | lex-superior: the source instrument defeats the target on conflict, within one order | normative-rank ladder |
| `derives-authority-from` | instrument\|organ → instrument | the source's validity flows from the target (delegated/derived legislation) | e.g. Art 80 GG (Rechtsverordnung ← enabling statute) |
| `level-contains` | level → level | territorial containment | territorial ladder |
| `has-primacy-over` | instrument → instrument | supremacy/preemption: conflicting target is set aside; carries `resolution_mode` (§4.1) | Art 31 GG; US Art VI cl.2; EU primacy |

### 3.2 Horizontal (separation + check)

| relation | from → to | meaning |
|---|---|---|
| `co-equal-with` | organ → organ | peers in the separation-of-powers sense (symmetric) |
| `reviews` | organ → organ\|instrument | may examine the validity/legality of the target's acts |
| `can-veto` | organ → organ\|instrument | may block a target act before it takes effect |
| `can-override` | organ → organ\|instrument | may defeat a target's block/act (e.g. legislative override of a veto) |
| `appoints` | organ → organ | staffs the target |
| `dissolves` | organ → organ | may terminate the target |
| `may-refer-to` / `must-refer-to` | organ → organ | court-dialogue check: discretionary/obligatory reference of a question upward (Art 267 TFEU; Art 100 GG) |

Check-edges are the raw material of balance (§6). A relation with no inbound
check-edge marks an *unchecked* organ — a queryable defect, not an error.

### 3.3 Coupling (inter-order) — see §4 for the full model

`has-primacy-over`, `applies-directly-in`, `must-be-transposed-by`,
`confers-competence`, `has-direct-effect`, `may/​must-refer-to` also run
*between* systems. When both endpoints share a `system` the edge is
intra-order; when they differ it is a coupling edge. The same relation
vocabulary serves both, which is why EU↔national coupling needs no new node
kinds (§4).

### 3.4 Relation properties

Every relation may carry: `basis` (the doctrine/provision that grounds it, as
free text + optionally a source URN, §8.1), `resolution_mode` (§4.1), and the
assertion wrapper (§4.7). Nothing else is stored on an edge; anything
computable (whether an organ is checked, whether a cycle of mutual constraint
exists) is *queried*, never stored (§6), mirroring governance's
`well_formedness` invariants which are computed at apply, not authored.

### 3.5 Bound — the relation vocabulary is CLOSED (honest scope limit)

Unlike the powers, levels, ranks, and allocation vocabularies — which are
**data**, parameterised per system (§7), and the basis of the "any legal system"
claim for those axes — the **relation types are a fixed enum** (the
`vertical-rel`/`horizontal-rel`/`coupling-rel` lists in `grammar/topos.ebnf`).
The "any legal system" claim is therefore **bounded for relation *types* the enum
does not name.** A legal relation with no dedicated relation type is representable
only *implicitly*, as the **presence, direction, and `basis` of an edge** drawn
from the nearest existing type, not as a first-class named relation. Known
implicit-only cases include:

- **Treaty consent / ratification** (a state's act of binding itself) — carried
  only as the presence of a `derives-authority-from`/coupling edge plus a
  `basis`, not as a `consents-to` relation.
- **Accession** (a state joining an order) — carried as the appearance of the
  coupling edges to the joined system, not as an `accedes-to` relation.
- **Reservation / opt-out / derogation** (a state binding itself *except* as to
  some part) — carried, at best, as a contested/qualified assertion in `basis`
  text, not as a typed `reserves-against` relation with a scoped exception.
- **Denunciation / withdrawal** — carried as edge *removal* (as the UK Brexit
  example does, `examples/uk.md`), not as a typed `withdraws-from` event.

This is a deliberate v0.1 boundary: a closed enum keeps conflict-resolution and
balance queries well-defined (§5, §6). Widening it is a **ratified vocabulary
change**, and whether the four cases above earn first-class relation types is an
open question for the owner (see `GROUNDING-NOTES.md` §4). Until then, treat them
as *representable but unnamed* — the model does not silently pretend they are
absent, and it does not fabricate a type for them.

---

## 4. Inter-system coupling — EU ↔ national as the proving case

Coupling is modelled as **typed edges between distinct legal orders**, each
grounded in a named doctrine. This is the hard part; it is worked here against
EU law because EU↔national is the richest real coupling in force.

### 4.1 Primacy / primauté — `has-primacy-over` with `resolution_mode`

*Costa v ENEL* (Case 6/64) and *Simmenthal* (Case 106/77) establish that a
directly-applicable EU norm takes precedence over a conflicting national norm,
and that the national court must **set the national norm aside** — it is
*disapplied*, not annulled. This is the crucial contrast with federal
invalidation, and the model carries it as a property on the edge:

```
rel eu:regulation  has-primacy-over  de:statute  [resolution_mode = disapply]
```

`resolution_mode ∈ {disapply, invalidate, void}`:
- **`disapply`** — the target keeps its formal validity but is not applied to
  the case (EU primacy over national law; *Simmenthal*).
- **`invalidate`** — the target is struck from the order (German Art 31 GG
  *Bundesrecht bricht Landesrecht* renders conflicting Land law void; US
  Supremacy Clause preemption voids conflicting state law).
- **`void`** — target was never validly enacted (ultra-vires / competence
  defect).

The distinction is not cosmetic: it is exactly where the EU order and a federal
order differ, and encoding it on the edge is what lets one grammar carry both.

### 4.2 Direct applicability — `applies-directly-in`

Art 288 TFEU: a **Regulation** "shall be binding in its entirety and directly
applicable in all Member States." Modelled as a coupling edge from the EU
instrument to each member-state system, and as the `directly_applicable = true`
property on the instrument node:

```
rel eu:regulation  applies-directly-in  de:system
rel eu:regulation  applies-directly-in  fr:system
```

No national instrument is spawned; the norm is present in the national order as
itself.

### 4.3 Transposition — `must-be-transposed-by` spawns a derived instrument

Art 288 TFEU: a **Directive** "shall be binding, as to the result to be
achieved… but shall leave to the national authorities the choice of form and
methods." This is modelled as **two linked nodes**: the EU directive, and a
*derived national instrument* it obliges into being, joined by
`must-be-transposed-by` carrying a `deadline` and a `state`:

```
instrument eu:directive-2019-790  system eu  rank 1  origin_organ eu:parliament-council
instrument de:transposition-u234   system de  rank 2  derives-authority-from eu:directive-2019-790
rel eu:directive-2019-790  must-be-transposed-by  de:system
    [deadline = 2021-06-07, state = transposed]      # state ∈ {pending, transposed, gap, partial}
```

The `state = gap` (non-transposition after deadline) is a first-class, queryable
condition — it is the structural precondition for *Francovich* state liability
(Cases C-6/90 & C-9/90) and for the vertical direct effect of an unimplemented
directive (§4.5). The two-node shape (EU directive + derived national
instrument) means the coupling survives transposition: the national instrument
persists with a `derives-authority-from` edge back to its directive.

### 4.4 Competence conferral — `confers-competence` + `competence.allocation`

Arts 2–6 TFEU catalogue Union competence as **exclusive** (Art 3), **shared**
(Art 4), and **supporting** (Art 6); Art 5 TEU adds **conferral** (the Union
acts only within competences conferred), **subsidiarity**, and
**proportionality** as constraints on *exercise*. Modelled with `competence`
nodes whose `allocation` field takes the system's allocation vocabulary, and a
`confers-competence` edge from the conferring instrument:

```
competence eu:customs-union      system eu  allocation exclusive   holder eu:union
competence eu:internal-market    system eu  allocation shared      holder eu:union
competence eu:culture            system eu  allocation supporting  holder eu:union
rel eu:tfeu  confers-competence  eu:customs-union
```

Allocation *gates whether the Union may act on a domain at all*; subsidiarity
and proportionality are constraints on the *exercise* of a shared competence
and belong to the **deontic** plane (they are `O`/`P`/`F` over an act), with the
`competence.allocation` fact supplied from here (§8.2). This is a clean seam:
topology says *the domain is shared*; deontic says *the Union may act only if
the objective cannot be sufficiently achieved by the states* (subsidiarity).

### 4.5 Direct effect — a property on a norm, `has-direct-effect`

*Van Gend en Loos* (Case 26/62): a Treaty provision can create rights
individuals may invoke in a national court. Modelled as the
`direct_effect ∈ {none, vertical, horizontal}` property on the instrument, and
optionally as an edge into the national forum where invoked. The vertical /
horizontal split is load-bearing and grounded:

- **Vertical** direct effect of a directive against the state — *Van Duyn v
  Home Office* (Case 41/74), conditional on non-transposition (§4.3 `gap`).
- **No horizontal** direct effect of a directive between private parties —
  *Marshall* (Case 152/84), confirmed *Faccini Dori* (Case C-91/92).

```
instrument eu:directive-x  direct_effect vertical   # against the state only, once in `gap`
```

Direct effect is a *capacity* fact (can this norm be invoked, and by/against
whom) — structural, hence here. Whether invoking it is *permitted or obliged*
in a given case is deontic.

### 4.6 Preliminary reference — `may-refer-to` / `must-refer-to`

Art 267 TFEU: a national court **may** refer a question of EU law to the CJEU;
a court of last instance **must**. This is a cross-level court-dialogue
check-edge:

```
rel de:ordinary-court     may-refer-to   eu:cjeu   [basis = "Art 267(2) TFEU"]
rel de:federal-court-last must-refer-to  eu:cjeu   [basis = "Art 267(3) TFEU"]
```

It is a *check*-family edge (§3.2): it is the structural channel by which the
CJEU's reading constrains national application, and by which national courts
feed the CJEU. It participates in balance queries (§6).

### 4.7 Contested relations — the assertion wrapper (neutrality principle 4)

A relation the CJEU asserts and a national constitutional court denies is
**two conflicting assertions**, not one settled edge. Any relation may be
wrapped:

```
assert eu:cjeu   : eu:primary-law has-primacy-over de:grundgesetz
                   [status = asserted, basis = "Costa 6/64; Internationale Handelsgesellschaft 11/70"]
assert de:bverfg : NOT eu:primary-law has-primacy-over de:grundgesetz
                   [status = contested, basis = "Solange II BVerfGE 73,339; Lisbon BVerfGE 123,267; Art 79(3) GG"]
```

The `NOT` scopes the whole triple by position; the assertion surface defines no
parenthesis terminal (`assert id ":" [NOT] endpoint relation-type endpoint`,
`grammar/topos.ebnf`), so the negation is written **without parentheses**.

**Two well-formed shapes of a contested edge:**

1. **Paired (preferred).** Two opposite-polarity assertions over the *same
   triple* by *different claimants* — e.g. the BVerfG asserting
   `de:bverfg reviews eu:regulation` (ultra-vires competence) against the CJEU
   asserting `NOT de:bverfg reviews eu:regulation` (**Foto-Frost**, Case 314/85:
   only the CJEU may declare an EU act invalid). This is the form to use whenever
   the counter-assertion is itself doctrinally explicit.
2. **Lone reservation-assertion.** A single `status = contested` assertion
   standing against the order's *default settled position*, which need not be
   separately authored (e.g. a constitutional-identity reservation asserted
   against a background of unconditional primacy). Permitted so a reservation can
   be recorded before, or without, an explicit opposing ruling.

Either way the grammar **does not resolve** the conflict — mirroring the deontic
algebra, which "flags candidate conflicts, never resolving them," and the versum
principle that provenance/claims "never silently move or merge." A settled edge
(`rel …`) is sugar for a single uncontested assertion by the order's own
competent organ.

The real disagreements this must carry (all grounded, none resolved):
- **Solange I / II** (BVerfGE 37,271, 1974; BVerfGE 73,339, 1986) — the BVerfG's
  fundamental-rights review reservation over EU acts.
- **Ultra-vires review** — *Honeywell* (BVerfGE 126,286, 2010) sets the manifest
  + structurally-significant test; *PSPP/Weiss* (BVerfG 2 BvR 859/15, 5 May
  2020) applied it against the ECB and the CJEU's *Weiss* ruling (Case
  C-493/17), the first time the BVerfG declared an EU act ultra vires.
- **Constitutional-identity review** — the *Lisbon* judgment (BVerfGE 123,267,
  2009) anchored in the Art 79(3) GG eternity clause.

These are `status = contested` assertions by `de:bverfg` standing against
`status = asserted` assertions by `eu:cjeu`. The model represents the standoff;
the ratifying humans decide nothing here about who is right.

---

## 5. Conflict-resolution rules (first-class, with precedence)

The canons are first-class objects, not implicit. The **language owns the
precedence rule**; a policy may remap it (a system that orders the equal-rank
canons differently declares so), exactly as `grades.json` lets policy own the
ladder while the language owns the comparison.

### 5.1 The default precedence

Given two norms in conflict, resolve in this order; stop at the first that
decides:

1. **Cross-order primacy / supremacy / preemption** (`has-primacy-over`). If a
   coupling or supremacy edge relates the two norms' orders, it decides *which
   order's norm applies* before any intra-order canon runs. (*Costa*; Art 31 GG;
   US Art VI cl.2.) `resolution_mode` (§4.1) determines whether the loser is
   disapplied, invalidated, or void.
2. **Lex superior** (`outranks`, normative-rank ladder). Within one order, the
   higher-ranked instrument wins regardless of time or specificity. (*lex
   superior derogat legi inferiori*.)
3. **Lex specialis** (specificity). Between norms of equal rank, the more
   specific governs the general. (*lex specialis derogat legi generali*; and
   *lex posterior generalis non derogat legi priori speciali* — a later general
   norm does not displace an earlier special one, which is why specialis
   precedes posterior.)
4. **Lex posterior** (time). Between norms of equal rank and equal specificity,
   the later enacted wins. (*lex posterior derogat legi priori*.) **This canon
   depends on the temporal axis** (§8.1, §GROUNDING) — it needs each norm's
   validity interval or at least an ordered enactment date. Under today's
   point-in-time-only stamping it can order two dated norms but cannot reason
   about overlapping validity windows or repeal-with-savings; that is deferred
   to the pending interval axis.

### 5.2 Why this order, and its honesty

The precedence 1→2 (primacy, then rank) is uncontroversial. The 3-before-4
ordering (specialis before posterior at equal rank) follows the classical maxim
but is **genuinely contested in legal theory** for the mixed case (a *later
general* vs an *earlier special*), where systems and scholars diverge. The
default encodes the classical *lex posterior generalis non derogat priori
speciali*; a policy that wants the opposite declares it. The language's job is
to *make the choice explicit and comparable*, not to pretend the theory is
settled. Where two canons genuinely deadlock (equal rank, neither more special,
same date), the resolver returns **unresolved** and hands off — it never invents
a winner. This mirrors deontic's "flag, never resolve" discipline.

### 5.3 Ungrounded rank ⇒ not-yet-grounded, never permissive

If a norm's `rank` (or the relevant coupling edge) is **unknown** — the
statute-dominant grounding today has not ingested that source-class (case-law
and soft-law are not yet ingested; case-law is source-licensing-gated) — the
comparison returns **not-yet-grounded** and the norm is *quarantined from
winning*. It is treated as neither top nor bottom of the ladder; it simply
cannot be asserted to defeat a grounded norm. This is the direct analogue of
today's `INSTRUMENT_RANK["case-law:cjeu"] = None` (an unranked, not a
zero-ranked, class) and honours the contract rule *an ungrounded source-class
is not-yet-grounded, never permissive*.

---

## 6. Balance — an emergent, queried property

Balance is **not** a node or a stored flag. It is a family of queries over the
check-edge subgraph (§3.2), computed at apply the way governance computes its
`well_formedness` invariants:

- **`no-organ-unchecked`** — every `organ` in a system has at least one inbound
  check-edge (`reviews`/`can-veto`/`can-override`/`appoints`/`dissolves`/
  `must-refer-to`), *or* lies on a cycle of mutual constraint. An organ failing
  this is reported as *unchecked* (a defect to surface, not an error to reject —
  some organs genuinely are apex, e.g. a sovereign parliament, §UK example).
- **`mutual-constraint cycle`** — a directed cycle in the check-edge graph
  (A reviews B, B can-veto C, C appoints A …) is a locus of balance;
  enumerating cycles answers "who ultimately checks whom."
- **`separation`** — no single organ holds the full `powers` set of its system
  (the parameterised branches, §5.6) without an inbound check.

These are read-only graph queries. The grammar defines *what the queries mean*;
it stores no verdict, exactly as governance stores no verdict on a policy graph
until a transport evaluates it.

### 5.6 (neutrality principle 1) Powers/branches are a PARAMETER

`powers` on an organ is a *set of labels drawn from the system's declared
`power_catalogue`* (§7.1), never the fixed triple {legislative, executive,
judicial}. Defended:

- Classic tripartite separation (Montesquieu) is **one** catalogue
  `{legislative, executive, judicial}` — an instantiation, not the schema.
- Systems with a **distinct monetary power** (an independent central bank — the
  ECB under Arts 127–133 TFEU; the Bundesbank) need a `monetary` label.
- Systems with a **distinct audit power** (the EU Court of Auditors, a national
  Rechnungshof / Cour des comptes) need `audit`; a distinct **prosecutorial**
  power (a public ministry, the EPPO) needs `prosecutorial`; an **electoral**
  power needs `electoral`.
- **Customary / hybrid / religious** orders carry entirely different catalogues
  (a `traditional-authority` label for a chieftaincy; a `religious-review`
  label for a body like Iran's Guardian Council). The grammar carries them
  because the catalogue is data.

Hardcoding three branches would make the grammar a Western-liberal template,
not a jurisdiction-neutral one. The catalogue-as-data design is the defence.

---

## 7. Vocabulary companions (remappable, per the family pattern)

Ship as JSON data files beside the grammar, mirroring `vocabulary/grades.json`
etc. Each is *policy*-owned; the language owns only how they are compared.

### 7.1 `power_catalogue.json` (per system)
The set of power-labels an organ may hold, and — optionally — a partial order if
some powers dominate others. Default profiles: `separation-tripartite`,
`separation-extended` (adds monetary/audit/prosecutorial/electoral).

### 7.2 `level_ladder.json` (per system)
The ordered territorial strata, e.g. `["supranational","national","regional","local"]`
with `order` a total order — the direct analogue of `grades.json`'s `levels` +
`order`. Owns the `level_rank` values on `level` nodes.

### 7.3 `rank_ladder.json` (per system)
The ordered instrument ranks — **the generalisation of today's hardcoded
`law_eu.INSTRUMENT_RANK`** (§8.1). A dict of `instrument-class → rank` plus an
`order`. `null` rank = *not-yet-grounded* (§5.3), preserving the semantics of
`INSTRUMENT_RANK["case-law:cjeu"] = None`.

### 7.4 `allocation_vocab.json` (per system)
The closed set of competence-allocation values, e.g. EU
`{exclusive, shared, supporting}` (Arts 3–6 TFEU); a federal state
`{federal-exclusive, concurrent, reserved}` (Arts 71–74 GG); the language owns
only how allocation gates action, not the labels.

### 7.5 `resolution_modes.json`
The closed set for `resolution_mode` (§4.1): `{disapply, invalidate, void}`.
Language-owned (this is the comparison semantics), unlike 7.1–7.4 which are
policy-owned.

---

## 8. The two plane-seams

### 8.1 versum seam — source topological coordinates

Today versum stamps each source with `{jurisdiction, time (a point — a
detected year), instrument-rank (via the profile's `INSTRUMENT_RANK` dict)}`
(seen in `versum/sync.py` nd-context and `profiles/law_eu.py`). This grammar
**extends that stamping** so each source additionally carries **topological
coordinates**:

```
{ system, organ_of_origin, instrument (→ its rank node), territorial_level }
```

Concretely:

1. **`INSTRUMENT_RANK` becomes a projection of the topology**, not a hardcoded
   dict. `law_eu.py`'s `INSTRUMENT_RANK = {"treaty:eu":0, "regulation:eu":1, …,
   "case-law:cjeu": None}` is exactly the `rank_ladder.json` (§7.3) of the
   `eu` system's instrument nodes. The profile references
   `topology://eu#instruments` instead of restating the dict; the `None`
   (not-yet-grounded) semantics carry over unchanged.
2. **New nD axes** under a `versum.topology.*` namespace, sitting beside the
   existing `versum.context` axes (`jurisdiction`, `time`, `instrument`,
   `domain` — see `versum/nd.py` `_CORE_SYSTEM`): `topology.system`,
   `topology.organ`, `topology.level`, with the topology graph as their
   controlled-identifier vocabulary. The stamping is a *ref into the topology
   graph*, not a copy — the two planes stay separate.
3. **Each `system` node carries its inter-system relations** (§4), so a
   consumer receiving `claim + span + source URN + jurisdiction + point_in_time
   + source_class` *plus* these coordinates can locate the source in the
   authority structure, not merely tag it. This is the concrete hand-off to the
   grounding plane.
4. **Identity** stays `urn:<ns>:<scheme>:<id>` with the `dls` namespace for
   legal sources; the topology's own node ids are a parallel `urn:topo:<system>:<class>:<id>`
   scheme (proposed; §GROUNDING open question).
5. **Temporal dependency.** `topology.time` inherits versum's current
   **point** stamping (a year), so lex-posterior (§5.1 step 4) and any
   temporal-validity reasoning on norms are **capped at point precision** until
   the pending interval axis lands. Flagged here and in `GROUNDING-NOTES.md`.

### 8.2 deontic seam — structural facts the deontic layer quantifies over

A deontic statement (`operator(bearer : proposition)`) references **structural
facts supplied by this grammar**: the bearer's `organ`/`competence`, and a
norm's `rank`. Topology says *who can*; deontic says *what they may/must*.
Examples:

- Subsidiarity (§4.4) is deontic — `if [shared competence] then P(union : act)
  unless [objective sufficiently achievable by states]` — where
  `shared competence` is the `competence.allocation` fact from topology.
- A conferral limit — `F(union : act outside [conferred competence])` (Art 5(2)
  TEU) — quantifies over the topology's competence catalogue.

The tie to Hohfeld is clean and grounding-backed: the deontic pack states
plainly that *"'Right' is not a modality — it lives in the incident layer"* and
covers the duty/right and privilege/no-right pairs. **This topology grammar is
the natural home for Hohfeld's *power* plane** — the competence to *change*
legal relations (power–liability, immunity–disability) — which is structural
capacity, not deontic modality. Topology owns *power/competence*; deontic owns
*duty/liberty*; the seam is that a deontic rule *quantifies over* a competence
this grammar declares. Coupling is by string agreement (a topology node id
appears as a bearer/scope reference in a deontic statement), exactly the
loose-coupling discipline the deontic README uses toward the solver.

---

## 9. Litmus (inherited)

Applying the governance litmus to this plane:

- **A regulation names a structural feature as a kind of authority relation →
  language.** (Primacy, direct effect, conferral, transposition are relation
  types the language defines.)
- **A jurisdiction chooses its organs, ladders, and catalogue values →
  policy.** (The `eu`/`de`/`uk` instantiations in `examples/` are policy.)
- **A runtime walks the graph and answers a conflict/balance query → host.**
  (Resolution and balance queries are host operations over the language's
  definitions.)
- A conflict-resolution comparison ranges only over declared node/edge
  properties (rank, level, allocation, basis), never a computed verdict; the
  ladders and their order are policy (remappable, §7), and the language owns
  only the precedence rule (§5) evaluated at conflict time.

---

## 10. Well-formedness (checked at apply, not parse)

Mirroring governance's `well_formedness` list:

1. Every relation endpoint names a declared node of a permitted class for that
   relation (e.g. `outranks` joins two `instrument`s; `level-contains` joins two
   `level`s).
2. `level-contains` is acyclic within a system (the territorial ladder is a
   tree/DAG); `outranks` is acyclic within a system (no rank cycles).
3. `derives-authority-from` is acyclic (no norm derives its authority from
   itself, transitively).
4. Every `organ`, `instrument`, `competence` names an existing `system`; a
   coupling edge names two *distinct* systems.
5. A contested relation is EITHER a *pair* of assertions with different claimants
   and opposite polarity on the same triple (the preferred form, §4.7 shape 1),
   OR a lone `status = contested` assertion standing against the order's default
   settled position (§4.7 shape 2); a settled `rel` is a single uncontested
   assertion by the order's competent organ. A `status = contested` assertion is
   never silently promoted to a settled edge.
6. An `instrument.rank` outside the system's `rank_ladder` parses but is rejected
   at apply (parse-vs-apply, §0.1); a `null` rank is *accepted* and means
   not-yet-grounded (§5.3).
7. `no-organ-unchecked`, `separation`, and `mutual-constraint` (§6) are
   *reported*, never *rejected* — an apex organ is a legitimate finding, not an
   ill-formed graph.

---

## 11. What this grammar deliberately does NOT do

- It does not carry norm *content* or claim spans (versum's).
- It does not carry `O`/`P`/`F` modality (deontic's).
- It does not *resolve* contested relations or deadlocked canons — it represents
  and flags them (§4.7, §5.2).
- It does not fabricate rank for ungrounded source-classes (§5.3).
- It does not measure or store time; it *references* versum's temporal axis and
  inherits its current point precision (§8.1).
- It does not carry an *open* relation vocabulary: the relation types are a
  closed enum (§3.5), so treaty consent, accession, reservation, and withdrawal
  are representable only *implicitly* (edge presence/removal + `basis`), not as
  first-class named relations, until a ratified vocabulary change adds them.

---

*See `grammar/topos.ebnf` for the concrete surface and the abstract-graph JSON
schema; `examples/` for the four instantiations; `GROUNDING-NOTES.md` for exactly
what was read, which doctrines were relied on, and the open questions for the
loomground owner and Felix.*
