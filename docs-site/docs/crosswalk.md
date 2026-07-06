# OAIS ↔ Pergamon Crosswalk — notes scaffold (v0.1)

**Source of truth:** OAIS Reference Model, CCSDS 650.0-M-2 (= ISO 14721). Cite the standard, not paraphrases.
**Verdict vocabulary:** `conformant` · `conformant-with-extension` · `out-of-model` · `n/a`
**How to use:** fill columns 3–4 as you go. Column 4 is the load-bearing one — it's where divergences land in *specific cells* instead of as loose claims.

Legend for pre-seeded cells: ★ = verdict we've already argued for; (blank) = for you to fill.

---

## A. Information Model

| OAIS term (as named in the standard) | OAIS one-line definition | Pergamon construct | Verdict |
|---|---|---|---|
| **SIP** — Submission Information Package | What a Producer hands the archive at ingest | _your note_ | _(see Ingest — typically forensic capture, not cooperative submission)_ |
| **AIP** — Archival Information Package | The package the archive preserves long-term | The Archimedes **bag** (one model) | conformant ★ |
| **DIP** — Dissemination Information Package | What a Consumer receives on access | _your note_ | _fill_ |
| **Content Information** | The target object + the RepInfo needed to understand it | `data/` (released bytes) + descriptors | conformant ★ |
| → **Content Data Object** | The bits being preserved | The released weights/config/tokenizer in `data/model/` | conformant ★ |
| → **Representation Information** | What turns the bits into something meaningful | `ARCHITECTURE.json` / `TOKENIZER.json` + format info | conformant-with-extension ★ _(see behavior gap below)_ |
| ⮑ Structure RepInfo | How the bits are formatted | safetensors/format records in `MODEL.json` | _fill_ |
| ⮑ Semantic RepInfo | What the data *means* | architecture/tokenizer semantics | _fill_ |
| ⮑ **(no OAIS subtype: behavioral)** | — | **Executable behavior of the model** (runtime, distillation-as-regen, deployment-archiving) | **out-of-model** ★ — OAIS RepInfo renders passive objects; a model *executes*. This is the frontier cell. |
| **PDI** — Preservation Description Information | Everything needed to preserve & trust the Content over time | the `pergamon/` layer | conformant ★ |
| → Provenance | History/origin of the Content | `PROVENANCE.json` (capture chain) | conformant-with-extension ★ — provenance is often *forensically reconstructed & partial*, not supplied at ingest |
| → Context | How it relates to other objects/environments | _your note_ (lineage, tape membership?) | _fill_ |
| → Reference | Identifiers that name the object | `External-Identifier`, `Pergamon-Model-Identifier` | _fill_ |
| → Fixity | Integrity/error-protection evidence | dual SHA-256/512 manifests | conformant ★ |
| → Access Rights | Permissions & restrictions on use | `License-Class`, `Origin-Jurisdiction`, withheld-ledger | conformant-with-extension ★ — adds the *redistribution-restriction* axis OAIS doesn't model |
| **Packaging Information** | Binds Content + PDI into the package | BagIt (RFC 8493) structure | conformant ★ |
| **Descriptive Information** | Metadata supporting Access/discovery | `bag-info.txt` + tape manifest rollups | _fill_ |

## B. Functional Model (the six entities)

| OAIS entity | OAIS one-line role | Pergamon construct | Verdict |
|---|---|---|---|
| **Ingest** | Accept SIPs, generate AIPs | Forensic **capture** of publicly-released (often orphaned) weights | conformant-with-extension ★ — Producer frequently absent/non-cooperative |
| **Archival Storage** | Store, maintain, retrieve AIPs | **Distributed multi-institution quorum** (not one store) | conformant-with-extension ★ — unit of integrity is the *constellation*, not the node |
| **Data Management** | Maintain descriptive DB + system info | _your note_ | _fill_ |
| **Preservation Planning** | Monitor environment, plan migrations | _your note_ (format/runtime-rot watch; architecture-as-hedge) | _fill_ |
| **Access** | Serve DIPs to Consumers | _your note_ | _fill_ |
| **Administration** | Day-to-day operation of the archive | _your note_ | _fill_ |

## C. Environment / Actors

| OAIS actor | OAIS one-line role | Pergamon reality | Verdict |
|---|---|---|---|
| **Producer** | Supplies the information to be preserved | Often the lab — frequently *non-cooperative or defunct*; weights captured, not donated | conformant-with-extension ★ |
| **Consumer** | Requests & receives preserved information | researchers, historians, future custodians | _fill_ |
| → **Designated Community** | The audience the archive commits to keep it usable *for* | _your note_ — define explicitly | _fill (important)_ |
| **Management** | The authority that sets archive policy | **Itself part of the threat model** (capture, seizure, defunding) → answered by distribution | conformant-with-extension ★ |

## D. Trustworthiness layer (adjacent standards, not OAIS proper)

| Construct | Source | Pergamon stance | Verdict |
|---|---|---|---|
| Trustworthy repository audit | ISO 16363 / CoreTrustSeal | per-*institution* audit; Pergamon adds *cross-institution* quorum above it | conformant-with-extension |
| — | — | _your note_ | _fill_ |

---

### The three divergences, pinned to cells (for the FAQ to point at)
1. **Executable behavior** → *out-of-model* at Representation Information (A). The novel/frontier claim. Do **not** mark as "solved."
2. **Distribution & trust** → *extension* at Archival Storage + Management (B, C). Already built (quorum).
3. **Orphaned / partial provenance** → *extension* at Ingest + Producer + PDI/Provenance (A, B, C). Already built (capture-only basis, withheld-vs-unknown ledger).

### Framing reminders
- OAIS *predates* the executable object; it didn't "fail to get AI." Silence = evidence for the thesis, not a flaw.
- "Publicly released" = scope (verifiable event). "Open" = per-item metadata (contested property). Different jobs, not a ranking.
- Conformant cells first (the handshake); divergences second (earned, not asserted).
