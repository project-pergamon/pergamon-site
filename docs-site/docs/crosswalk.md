# OAIS ↔ Pergamon Crosswalk — v0.1

**Source of truth:** OAIS Reference Model, CCSDS 650.0-M-2 (= ISO 14721).
**Verdict vocabulary:** `conformant` · `conformant-with-extension` · `out-of-model` · `deferred` · `—` (reframe, no verdict)

> **Orienting metaphor.** OAIS was written for a *library of readable records* — objects you
> preserve by rendering them for a future reader. Pergamon is closer to a *museum of working
> machines*: objects with structure, meaning, provenance, and — for some — a behavior they
> once enacted. Pergamon conforms to OAIS almost everywhere. The one genuinely new room it
> adds to the building is the place where a preserved object *does something* rather than
> *depicts something*.

---

## A. Information Model

| OAIS term | OAIS definition | Pergamon construct | Verdict |
|---|---|---|---|
| **SIP** — Submission Information Package | What arrives at ingest from the Producer | The **release as captured** — weights pulled from the source at a revision, on a date, by an agent, *before* wrapping and normalization; fossilized in `PROVENANCE.json`'s capture block | conformant-with-extension — the submitter is usually non-cooperative, so the SIP is *forensically assembled*, not *submitted* |
| **AIP** — Archival Information Package | The package preserved long-term | The Archimedes **bag** (one model), verified and marked | conformant |
| **DIP** — Dissemination Information Package | What a Consumer receives on request | The **marked accession record served per-jurisdiction**: different custodians compute different DIPs from the same AIP — full artifact, or record-without-operative-weights under lawful restriction | conformant-with-extension — separable holdings; access computed at dissemination, extended to jurisdictional control |
| **Content Data Object** | The bits being preserved | The released weights/config/tokenizer in `data/model/` | conformant |
| **Representation Information** | What turns bits into meaning | `ARCHITECTURE.json` / `TOKENIZER.json` / format records | conformant-with-extension *(see the third mode below)* |
| → **Structure RepInfo** | How to *parse the format* (syntax) | Format + shard-layout records in `MODEL.json`; the tokenizer/config file formats | conformant |
| → **Semantic RepInfo** | What the parsed structure *means* | `ARCHITECTURE.json` — what the tensors and config fields *are* | conformant |
| → **Behavioral RepInfo** *(no OAIS subtype)* | — | **What the model *does* when executed.** OAIS assumes meaning is recovered by *rendering*; a model's meaning is recovered by *executing and comparing*. This is **the task of a future machine philology**: the runtime/reconstruction record, deployment-archiving, and recovery-by-comparison across the corpus | **out-of-model — frontier.** The one new room. Not claimed as solved. |
| **PDI** — Preservation Description Information | Everything needed to preserve & trust Content over time | the `pergamon/` layer | conformant |
| → Provenance | History/origin of the Content | `PROVENANCE.json` capture chain + authenticity basis | conformant-with-extension — often forensically reconstructed & honestly partial (`capture-only`) |
| → Context | How it relates to other objects & environments | **Lineage** (base → fine-tune → distillation genealogy) and **situation** (what a release responded to; its place in the landscape) | conformant-with-extension — extended with deployment/uptake context |
| → Reference | Identifiers that name & cite the object | `External-Identifier`, `Pergamon-Model-Identifier`, canonical `org/model`, version, `bag_root_digest` | conformant *(identity can be contested for leaked/orphaned models — see frontier notes)* |
| → Fixity | Integrity / error-protection evidence | dual SHA-256 / SHA-512 manifests | conformant |
| → Access Rights | Permissions & restrictions on use | `License-Class`, `Origin-Jurisdiction`, the markedness ledger | conformant-with-extension — adds the *redistribution-restriction* axis OAIS doesn't model |
| **Packaging Information** | Binds Content + PDI into the package | BagIt (RFC 8493) structure | conformant |
| **Descriptive Information** | Metadata supporting discovery & access | `CUSTODIAN.txt` — acquisition narrative, significance statement, the human-facing testimony | conformant-with-extension — carries testimony about the *acquisition itself* (capture circumstances, orphan status) a donation model wouldn't need |

*Museum reading of the RepInfo split: Structure = "oil on canvas, these pigments"; Semantic = "this depicts the Annunciation"; Behavioral = the instrument that, beyond wood and tuning, **makes a sound when played** — and the sound is why it matters.*

## B. Functional Model (the six entities)

| OAIS entity | OAIS role | Pergamon construct | Verdict |
|---|---|---|---|
| **Ingest** | Accept SIPs, generate AIPs | Forensic **capture** of publicly-released (often orphaned) weights → wrap, normalize, mark, manifest | conformant-with-extension — Producer frequently absent/non-cooperative |
| **Archival Storage** | Store, maintain, retrieve AIPs | **Distributed multi-institution quorum** — the unit of integrity is the constellation, not the node | conformant-with-extension |
| **Data Management** | Maintain descriptive DB + system info | The tape manifests + bag-info as the queryable catalogue layer | conformant |
| **Preservation Planning** | Monitor environment, plan migrations | Substrate-migration discipline (LTO obsolescence schedule); architecture-as-hedge for runtime rot | conformant-with-extension — plans for *behavioral*/runtime obsolescence, not just format |
| **Access** | Serve DIPs to Consumers | Per-jurisdiction DIP computation (see A) | conformant-with-extension |
| **Administration** | Day-to-day operation of the archive | Federation membership & the shared standard (ARCHI) | conformant-with-extension — administration is *distributed across members*, not centralized |

## C. Environment / Actors

| OAIS actor | OAIS role | Pergamon reality | Verdict |
|---|---|---|---|
| **Producer** | Supplies the information to be preserved | Often the lab — frequently *non-cooperative or defunct*; weights captured, not donated | conformant-with-extension |
| **Consumer** | Submits a request, receives a DIP | Researchers, historians, custodians requesting access to preserved models | conformant |
| → **Designated Community** | The audience the archive commits to keep the object usable *for* — and therefore the knowledge-baseline the archive may presuppose | This is OAIS's deliberate wiggle room: the standard wisely refuses to legislate the community, because the choice is constitutive, not technical. Pergamon makes the same refusal **explicit**. Nominally: a technically literate future reader with access to the surrounding corpus but not the original lab. Structurally: a *single* fixed community is inadequate for an archive built for the collapse of the assumed knowledge-environment, so Pergamon **layers baselines** — near-zero at the root (`README.txt` in plain UTF-8, assuming only a literate human), richer inward (`ARCHITECTURE.json` assuming ML literacy) — *marking what each layer presupposes*. Whom the archive ultimately serves is a values question the semantics cannot settle | **deferred — governance** *(see docket G1)*; layered-baseline mechanism itself: conformant-with-extension |
| **Management** | The authority that sets archive policy | **Itself part of the threat model** (capture, seizure, defunding) → answered by federation: sovereign-at-the-copy, plural-across-the-constellation | conformant-with-extension |

## D. Trustworthiness layer (adjacent standards)

| Construct | Source | Pergamon stance | Verdict |
|---|---|---|---|
| Trustworthy-repository audit | ISO 16363 / CoreTrustSeal | These audit whether a *single repository* is trustworthy. Pergamon's trust is **cross-institutional** — the federation/quorum — which sits *above* single-node audit and is not something these standards were built to certify | **deferred — governance** *(see docket G2)*. Marked, not blank. |

---

### The three divergences, pinned to cells
1. **Behavioral RepInfo** → *out-of-model, frontier* at Representation Information (A). The task of a future machine philology. Not claimed as solved.
2. **Distribution & trust** → *extension* at Archival Storage + Administration + Management (B, C), and docket item G2 (D). Partly built (quorum), partly a partnership decision.
3. **Orphaned / partial provenance** → *extension* at SIP + Ingest + Producer + PDI/Provenance (A, B, C). Built (forensic capture, `capture-only` basis, the markedness ledger).

### The Governance Docket

The deferred cells above are not unfinished format work — they are questions about people
and power that no schema can settle, and they are deliberately kept out of the format so
that neither layer pretends to be the other. The format specifies what can be specified;
governance owns what is chosen. Collected, they form the founding agenda of the Pergamon
consortium — the constitution its institutional partners exist to write:

- **G1 — Whom does the archive serve?** The Designated Community decision: what
  knowledge-baseline may the archive presuppose, and for whom is usability guaranteed.
  The format supplies the layered-baseline mechanism; the community choice is a value.
- **G2 — How does a federation certify trust?** Single-repository audit standards
  (ISO 16363 / CoreTrustSeal) were not built to certify trust *across* mutually
  independent members. The federation's trust model is a constitutional design.
- **G3 — Who may invoke restriction, and on what showing?** The `accession-decision`
  event type gives restriction an honest, logged form; who is entitled to trigger it,
  under what process, is a governance question.
- **G4 — Custody tracking (bag↔tape coupling).** v0.1 keeps bags tape-unaware; a mature
  replication layer needs the inverse map (bag → tapes → custodians), and its design
  belongs to those who run live preservation networks.
- **G5 — Access testimony.** Whether disseminations may carry a voluntary, marked
  statement of purpose — enriching the uptake record without building a consultation-
  surveillance gate. Double-edged; requires the privacy judgment of memory institutions.

Each item points at what gets built next — including, in time, the tooling for partners
to do this work themselves.

### Framing reminders
- OAIS **predates** the executable object; it did not "fail to get AI." Its silence on behavior is *evidence for* the thesis, not a flaw.
- Library of records vs. museum of working machines: conform in every room but one; name the new room honestly.
- Conformant cells first (the handshake); divergences second (earned, not asserted).
