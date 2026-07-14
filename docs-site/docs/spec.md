# ARCHI — The Archimedes Profile — v0.1 (DRAFT)

*ARCHI: **A**rchiving the **R**e**C**onstructible **H**istory of **I**ntelligence.*

A draft for a BagIt Profile for preserving publicly released AI models as self-describing, verifiable preservation units, written many-to-a-tape.

**Status:** A proof of concept, and an invitation to collaborate with the experts. Currently drafted with LLMs, but intended to be reviewed and revised with a technical collaborator and legal counsel before a v1.0 release.
**Conforms to:** RFC 8493 (BagIt File Packaging Format, V1.0) and the community *bagit-profiles* convention.
**Profile document:** `archi-profile-v0.1.json`
**Rev note:** this revision separates the *bag* (one model) from the *tape* (many bags); see §1 and §9.

---

## 1. Scope and the three layers

The system distinguishes between three operative layers in the work of preservation:

- **Model** — the intellectual object: a publicly released AI model, itself consisting of multiple components.
- **Bag** — the unit of *packaging and verification*. One bag wraps **exactly one model** (RFC 8493 + the Archimedes Profile). The bag is independently verifiable, independently custodiable, independently withdrawable.
- **Tape** — the physical **container of bags**. One LTO-9 cartridge carries **one or more bags**. The tape is a carrier, not itself a bag.

"Publicly released" means *released by the rights-holder for public download, on any terms* — which admits permissive, use-restricted, and redistribution-restricted models alike, and excludes **API-only models**, which are flatly non-public: no weights were ever released, so there is no artifact to preserve (the release *event* may still merit an interpretive record within the `ARCHI/` annotation category). ARCHI makes no claim that a model is "open." The metadata treats "open-ness" as an objective list of distinct, verifiable decisions, each held by a responsible party. *How* a model entered the public record is currently recorded in the `ARCHI-Release-Channel` field, and refining this mechanism is a key point for future revision (see §11).

The ARCHI Profile governs **packaging, integrity, and self-description** at the bag level, and **indexing** at the tape level. It is deliberately not a transfer *protocol* (discovery, replication scheduling, audit voting, repair); those belong to a network layer above it.

**A bag is intentionally tape-agnostic.** It records nothing about which cartridge carries it or what its tapemates are. How many bags fit on a tape is a *deployment fact* that varies by model selection, size, precision, and LTO generation — so it lives in the tape manifest (§9), never in the bag. This keeps the bag a stable, portable atom that can be re-written onto any medium without editing.

## 2. Reconstruction, not regeneration

Project Pergamon draws a deliberate line between two things easily  conflated. **Regeneration** is rebuilding a model from its recipe — the training data, the training code, the full checkpoint trajectory — such that you could produce the weights again from scratch. **Reconstruction** is understanding and re-instantiating the *artifact* from what survives: the weights, the architecture, the tokenizer, and the record of where they came from. ARCHI's scope - and Project Pergamon's scope - is reconstruction.

Here, an analogy to archaeological preservation can be illuminating. Roman concrete (like that in the Pantheon dome) outperforms modern concrete in specific ways. When we preserve the Pantheon as an artifact, we can interpret its likely behavior (not falling down for a very long time), and formulate questions about its nature (is Roman concrete different from modern concrete, and how?). But no archive can produce the curriculum, standard, or discourse to which ancient Romans referred when mixing their materials (the recipe was lost with the empire). Remarkably, **we may not have needed one**. New methods of microscopy and spectroscopy recently recovered the lime clasts and hot-mixing process that gave Roman concrete its superior qualities. **The recipe was read from the artifact itself, by techniques that were unimaginable when the building was first slated for preservation.** A preserved artifact served as a backup of the knowledge that had rendered it, and the artifact held those traces until a method that could read them arrived.

Thus, a model preserved for reconstruction can be run, examined, situated in its lineage, and interpreted by future scholarship, even where regeneration is permanently foreclosed. The five records (§3) enclose the material that makes reconstruction possible and that Pergamon can feasibly and lawfully hold; the heavier regeneration material (like training corpora, checkpoint series, optimizer states) is preserved *by reference* to separately-stewarded artifacts where it exists, marking the exact joint where institutional collaboration will fit.

## 3. The payload / annotation split

BagIt treats the payload as opaque octets and does not interpret it. The Archimedes Profile uses that property as a discipline:

- **`data/`** holds the model **exactly as the rights-holder released it** — weights, the lab's own config files, tokenizer, the original `LICENSE`, the original model card. These bytes are *never edited* by Pergamon. The payload manifests verify that this artifact is byte-identical to what a third party would obtain from the source.
- **`ARCHI/`** holds Pergamon's **authored interpretive layer** as tag files — provenance, the completeness ledger, custodian documentation, and normalized descriptors that *point into* `data/` without modifying it.

This mirrors the [Open Archival Information System] OAIS distinction between Content Information (the release) and Preservation Description Information (the annotations), and it keeps the released artifact independently checkable, separate from any commentary on it.

**The five records.** The `[Cat 1]`–`[Cat 5]` tags in the layout below refer to Project Pergamon's five categories of reconstruction material — the set a future operator needs to interpret a model's likely behaviors:

1. **Model weights & state** — the trained parameters themselves
2. **Architecture & configuration** — what the numbers are and how they are arranged
3. **Tokenizer & metadata** — the mapping between text and the model's input space
4. **Provenance & integrity** — where these bytes came from, and the honest basis for trusting them
5. **Documentation for future custodians** — the plain-language account of all of the above, including every gap and failure state

These are Pergamon's terms, not OAIS's, but they sort cleanly into the Content/Documentation split above: categories 1–3 are the released artifact (Content Information, in `data/`); categories 4–5 are annotation about it (Preservation Description Information, in `ARCHI/`). Together, the payload and the interpretive layer aim to cover as much of the five as each release permits — and where a category cannot be covered, the completeness ledger (§7) marks the gap rather than leaving it silent. Whereof a release withholds, the bag cannot speak; but it must always account for its silences.

## 4. Bag layout (one model)

```
archimedes-<model-id>/
├── bagit.txt                     # BagIt declaration (version + encoding)
├── bag-info.txt                  # bag + model metadata (§5)
├── manifest-sha256.txt           # payload checksums
├── manifest-sha512.txt           # payload checksums (algorithm diversity)
├── tagmanifest-sha256.txt        # tag-file checksums
├── tagmanifest-sha512.txt
├── ARCHI/                        # ARCHI interpretive layer (tag files)
│   ├── README.txt                # [Cat 5] plain-UTF-8 bootstrap; root of the recursion
│   ├── MODEL.json                # [Cat 1] identity + weight-file descriptor
│   ├── ARCHITECTURE.json         # [Cat 2] normalized architecture record
│   ├── TOKENIZER.json            # [Cat 3] tokenizer descriptor
│   ├── PROVENANCE.json           # [Cat 4] capture chain + integrity/authenticity
│   ├── COMPLETENESS.json         # the completeness ledger (§7)
│   └── CUSTODIAN.txt             # [Cat 5] narrative docs + gap explanations
└── data/                         # released bytes, unaltered
    └── model/
        ├── <weight files as released>          # [Cat 1]
        ├── config.json / generation_config.json # [Cat 2, as released]
        ├── tokenizer.json / vocab / merges      # [Cat 3, as released]
        ├── LICENSE                              # as released
        └── README.md (model card)               # as released
```

## 5. `bag-info.txt` fields

This tag file contains metadata elements that describe the bag and the payload. Elements consist of a label, a colon ":", a single linear whitespace character, and value that is terminated with an LF, with one element per line (RFC 8493 §2.2.2). Note: there is deliberately **no tape or count field here** (ARCHI docs §1).

| Field | Req | Meaning | Example |
|---|---|---|---|
| `Source-Organization` | ✓ | Contributing custodian/archivist | `Project Pergamon` |
| `Contact-Email` | ✓ | Accountable contact | `tk@projectpergamon.org` |
| `External-Identifier` | ✓ | Stable ID for this bag | `pergamon:archimedes:deepseek-llm-67b-base:v1` |
| `External-Description` | ✓ | One-line human description | `DeepSeek LLM 67B base, released 2023-11-29` |
| `Bagging-Date` | ✓ | Date the bag was made | `2026-06-29` |
| `Payload-Oxum` | ✓ | `octetCount.streamCount` quick check | `134217728000.12` |
| `ARCHI-Profile-Version` | ✓ | Profile version | `0.1` |
| `ARCHI-Model-Identifier` | ✓ | Canonical model id | `deepseek-ai/deepseek-llm-67b-base` |
| `ARCHI-Model-Family` | ✓ | Human family name | `DeepSeek LLM` |
| `ARCHI-Parameter-Count` | ✓ | Parameters (integer or band) | `67000000000` |
| `ARCHI-Weight-Precision` | ✓ | Released precision | `BF16` |
| `ARCHI-Release-Date` | ✓ | Original public release | `2023-11-29` |
| `ARCHI-Rights-Holder` | ✓ | Releasing entity | `DeepSeek` |
| `ARCHI-Origin-Jurisdiction` | ✓ | ISO country of lead developer | `CN` |
| `ARCHI-License-Identifier` | ✓ | SPDX id or named license | `DeepSeek-License` |
| `ARCHI-License-Class` | ✓ | `permissive` \| `restricted-use` \| `restricted-redistribution` \| `undetermined` | `restricted-redistribution` |
| `ARCHI-Ledger-Resolution` | ✓ | Whether the ledger (§7) contains any `undetermined` component — derived, enforced by the validator | `unresolved` |
| `ARCHI-Capture-Source` | ✓ | Where captured, with revision | `hf.co/deepseek-ai/...@<commit>` |
| `ARCHI-Authenticity-Basis` | ✓ | Strongest anchor available (§6) | `capture-only` |

Openness is deliberately **not** summarized in any single field. What a release did and did not make available is recorded per-component in the completeness ledger (§7). ARCHI is a self-contained schema that provides a list of objective traits for experts to interpret, whereas "openness" is qualitative standard that experts can apply to individual ARCHI records, which support these qualitative judgements with rigorous standards of evidence. 

## 6. Unauthorized Alterations and Inauthentic Sources are Governance-Level Challenges

Understanding what the ARCHI Profile **cannot** guarantee, as distinct from the larger Project Pergamon, is crucial for responsible archiving without overclaiming:

- **Internal integrity** — the dual `manifest-sha256` / `manifest-sha512` files certify that this bag's contents are complete and unaltered *since bagging*. Algorithm diversity hedges a future break in either hash. This catches decay and accidental corruption. Per RFC 8493, BagIt fixity is **not designed to defend against active attack** — an adversary who can rewrite a file can rewrite its checksum. 

- **Source authenticity** — whether the payload is the *genuine release* (not a fork) may require interpretive decisions grounded in expert forensic and academic methodologies. `PROVENANCE.json` records the strongest anchor that actually exists, and `ARCHI-Authenticity-Basis` responsibilizes the scholar who made the call for any interpretive claims:
    - `rights-holder-signature` — the release was cryptographically signed by the rights-holder; strongest.
    - `rights-holder-hash` — the rights-holder published a checksum at release that the payload matches.
    - `capture-only` — no independent anchor; integrity asserted from a documented capture event only. **This is a rigorous methodological choice** — it tells a future scholar how far the authenticity claim extends, and binds that claim to its author.
    - `undetermined` — our review could not establish an anchor (carries a review reference).

The ARCHI Profile never lets a manifest match *masquerade* as proof of authenticity. Cross-tape Byzantine quorum (a network-layer concern, above this Profile) is what defends the constellation against tampering; per-bag manifests that name the human custodian at point of acquisition turn unanchored claims into personal liabilities. And both solutions are located in the purview of governance. 

## 7. The completeness ledger — `COMPLETENESS.json`

COMPLETENESS.json is one of the files in the ARCHI/ interpretive layer (§8). We describe it here first in its own section because the completeness ledger is so important to how we are approaching the format. 

The ARCHI format forbids bare `null`, because a blank space would conflate "the lab never released this" with "A custodian failed to record it." To avoid this ambiguity, every component of an acquisition record carries an explicit **status** from a controlled vocabulary; any non-`present` status MUST carry a `reason` and SHOULD link to a `CUSTODIAN.txt` anchor.

**The markedness vocabulary**

| Status | Means | Accountability | Required floor | Example |
|---|---|---|---|---|
| `present` | Captured and in the bag | inward (governance and practices) | `path` or `external_ref` | weights, config |
| `withheld` | Existed; the rights-holder chose not to release it | outward (lab's decision) | `evidence` of intent + `reason` | closed training data |
| `not-applicable` | Never existed for this model | structural | `reason` | no merges file for a byte-level tokenizer |
| `unrecoverable` | Was publicly released but Pergamon could not capture it | inward (capture failure) | `reason` | eval card offline at capture |
| `undetermined` | Pergamon's review ran and was inconclusive | inward (knowledge limit, handed forward) | `review` reference with date | training logs of indeterminate status |

All descriptions point to concrete actors, observable events, and accountable processes (or failure thereof). `withheld` documents *the rights-holder's* decision; `unrecoverable` and `undetermined` document *Pergamon's* limits: `unrecoverable` recording a capture failure (we know it existed; we couldn't get it), `undetermined` a knowledge failure (our review could not establish it). A future interpreter can always tell which is which.

The disction between documents `withheld` at release and documents that remain `undetermined` after a research process is worth unpacking further: 

- **`withheld` requires evidence of intent.** Asserting that a rights-holder *chose* to withhold something is a claim about their decision, and an unevidenced claim of intent is itself an unmarked guess. `withheld` is legal only when the choice can be evidenced (the lab said so; the release included everything *but* this; the license implies it). When intent cannot be evidenced, the honest status is `undetermined`, and responsibility for the claim shifts to the custodian.

- **`undetermined` requires evidence of methodology.** Every `undetermined` carries a `review` reference — which review process ran, and when ("v0.1 review, 2026-06") — so the claim "we did our best" is checkable, and so that a later determination reads as a dated improvement to the record rather than a contradiction of it. `undetermined` is process-relative and expected to change; the date is what marks *when we looked*.The bag-info fields most vulnerable to orphaned or provenance-broken models — `ARCHI-Origin-Jurisdiction`, `ARCHI-Release-Date`, `ARCHI-Parameter-Count`, `ARCHI-Weight-Precision` — MAY take the literal value `undetermined` rather than forcing a guess entered as fact. A marked gap is better than a confident guess. 

- **One more note:** The way v0.1 handles external references is simplistic by design. Currently, `external_ref`  points to a URL that is hosted elsewhere, along with a short note (see the **example** `intermediate_checkpoints` field below). Pointing to websites hosted elsewhere is a provisional solution. Defining a controlled vocabulary to record references to externally hosted and third-party sources is the exact kind of work we want to pursue in dialogue with future partners. 

**Example**

```json
{
  "schema": "archi-completeness/0.1",
  "model_id": "deepseek-ai/deepseek-llm-67b-base",
  "components": {
    "weights":                 { "status": "present", "path": "data/model/", "files": 12,
                                 "bytes": 134217728000 },
    "architecture_config":     { "status": "present", "path": "data/model/config.json" },
    "tokenizer":               { "status": "present", "path": "data/model/tokenizer.json" },
    "original_license":        { "status": "present", "path": "data/model/LICENSE",
                                 "note": "Dual grant: the code repository is MIT; the model weights are governed by the DeepSeek Model License. The model license is what is recorded in bag-info (HF card metadata tags it SPDX 'other')." },
    "model_card":              { "status": "present", "path": "data/model/README.md" },
    "training_data":           { "status": "withheld",
                                 "evidence": "Release shipped weights, config, and tokenizer but no corpus; model card names the data only in aggregate terms.",
                                 "reason": "Training corpus was never publicly released by the rights-holder.",
                                 "custodian_note": "ARCHI/CUSTODIAN.txt#training-data" },
    "training_code":           { "status": "withheld",
                                 "evidence": "Repository contains inference code only; no training scripts in any release artifact.",
                                 "reason": "No training code accompanied the release." },
    "intermediate_checkpoints":{ "status": "present",
                                 "external_ref": "github.com/deepseek-ai/DeepSeek-LLM documents 9 intermediate checkpoints of the base model, hosted on AWS S3 (requester-pays) as of capture",
                                 "note": "Reference, not carried in-bag. Access requires an AWS account (requester-pays bucket)." },
   "evaluation_results":       { "status": "present",
                                 "external_ref": "Reported in the DeepSeek-LLM paper (arXiv:2401.02954) and the GitHub README evaluation section: HumanEval 73.78, GSM8K 84.1, Hungarian exam 65." }
  },
  "rollup": { "resolution": "resolved", "undetermined": [] }
}
```

Remember, "Completeness" is a dynamic statement about the status of Pergamon's own inquiry. It is not a static judgement about what components make up a "complete" AI model. The only determination derived from the ledger is `ARCHI-Ledger-Resolution` (`resolved` | `unresolved`): whether any component remains `undetermined`. New evidence, methods, or arguments could move an `undetermined` in a record toward `resolved`, and future researchers will know exactly where to find the gaps in our record. Completeness also plays a role in validating that our bags and tapes have been assembled correctly. The validator (§10) verifies `ARCHI-Ledger-Resolution` against the itemized contents of the `COMPLETENESS.json` ledger under the rule that the flag must read `unresolved `if and only if some component's status is `undetermined`; The validator rejects any bag where the two disagree.

## 8. The Interpretive Layer: /ARCHI Files

The Interpretive Layer comprises `completeness.json` (§7) alongside the following additional descriptor files.

- **`MODEL.json`** [Cat 1] — identity (id, family, params, precision), and the weight-file inventory: each file's role, byte size, format (`safetensors`/`gguf`/…), shard index, and SHA-256 (duplicating the manifest for self-containment of the descriptor).
- **`ARCHITECTURE.json`** [Cat 2] — normalized architecture record: family/type, layer/width/head counts, context length, position-encoding, activation, plus a pointer to the as-released `config.json`. Pergamon's normalization sits *beside* the original, never replacing it.
- **`TOKENIZER.json`** [Cat 3] — tokenizer type (BPE/SentencePiece/byte-level), vocab size, special tokens, and pointers to the as-released tokenizer files. Flags whether the tokenizer is reconstructible from the payload alone.
- **`PROVENANCE.json`** [Cat 4] — capture chain (source URL, repo revision/commit, capture timestamp, capturing agent), any rights-holder-published hashes/signatures, and the authenticity basis (§6).
- **`CUSTODIAN.txt`** [Cat 5] — plain-language narrative for a future custodian: what this model is, why it was preserved, every gap from `COMPLETENESS.json` explained in prose, and any handling notes. Anchors (e.g. `#training-data`) are referenced from the ledger.
- **`COMPLETENESS`** - The aforementioned 

Together, the /ARCHI descriptor files will aid future communities of inquirers with descriptions and locations for a given model's `/data`. The fields given above are for v0.1 and expected to firm up with a technical collaborator (this is only one way of implementing the Cat 1-5 concept, and perhaps not the best one).

## 9. The tape layer — many bags per cartridge

A tape is an LTFS filesystem whose root holds one or more complete bags plus a tape manifest. **The bags do not know they share a cartridge; the tape manifest is the only place membership and count are recorded.** This is the clean, low-coupling choice for v0.1 (see the deferred coupling question in §11).

**Tape layout**

```
<LTFS volume root>/
├── TAPE-README.txt              # plain-UTF-8 bootstrap for the whole cartridge
├── ARCHIMEDES-TAPE.json         # tape manifest: which bags, order, rollup
├── archimedes-olmo-7b/          # a complete, standalone bag
│   └── (bagit.txt, bag-info.txt, manifest-*, tagmanifest-*, ARCHI/, data/)
├── archimedes-pythia-12b/       # another complete bag
└── archimedes-bloom-176b/       # another
```

Each subdirectory is a fully valid Archimedes bag on its own. The tape manifest is an index over them, not a bag itself, and is **not** governed by BagIt — it is an ARCHI construct.

**`ARCHIMEDES-TAPE.json`** — the count lives in `rollup.bag_count`; the membership lives in `bags[]`; nothing here is duplicated inside the bags.

```json
{
  "schema": "archi-tape/0.1",
  "tape_id": "pergamon:archimedes:tape:0001",
  "tape_title": "Archimedes I",
  "series": "Archimedes",
  "medium": { "type": "LTO-9", "native_capacity_bytes": 18000000000000, "ltfs": true },
  "written": { "date": "2026-06-29", "agent": "Project Pergamon", "host_jurisdiction": "US" },
  "selection_rationale": "First proof: permissive, fully released models with low custody risk.",
  "bags": [
    { "path": "archimedes-olmo-7b",
      "model_id": "allenai/OLMo-7B",
      "payload_oxum": "13958643712.4",
      "license_class": "permissive",
      "ledger_resolution": "resolved",
      "origin_jurisdiction": "US",
      "bag_root_digest": "sha256:<digest of this bag's tagmanifest-sha256.txt>" }
  ],
  "rollup": {
    "bag_count": 1,
    "total_payload_bytes": 13958643712,
    "cartridge_used_fraction": 0.0008,
    "free_bytes": 17986041356288,
    "license_classes": { "permissive": 1 },
    "origin_jurisdictions": { "US": 1 }
  }
}
```

**`bag_root_digest`** gives the tape a way to commit to each bag without coupling the bag to the tape. It is the SHA-256 of the bag's `tagmanifest-sha256.txt`. Because that tag manifest checksums the payload manifests, which in turn checksum every payload file, a single digest transitively commits to the entire bag (a Merkle-style root). The tape vouches for its bags; the bags remain unaware of the tape. To hash the tag manifest in your own implementation, download the worked example .zip and run the following commands in xx/xx/xx
cd archimedes-tape-0001/archimedes-olmo-7b
sha256sum tagmanifest-sha256.txt

**`TAPE-README.txt`** MUST be plain UTF-8 and is the cartridge-level bootstrap: what this tape is, the human-readable list of bags, the instruction that each subdirectory is a standalone bag whose own `ARCHI/README.txt` explains it, the selection rationale, and a contact. It terminates the representation-information recursion at the cartridge level, one rung above each bag's own README.

**Serialization and write order.**

- **Serialization is forbidden** at the bag level: a bag lives inside LTFS as a real directory tree, not a `.zip`/`.tar`, preserving direct file access and letting a custodian validate without unpacking.
- **Non-normative write recommendation:** write the LTFS index, then `TAPE-README.txt` and `ARCHIMEDES-TAPE.json`, then the bags — so a custodian mounting the cartridge can read the orientation docs and the inventory from the front without winding to the end. LTO is linear; this is an access-time concern, not a capacity one. The entire annotation layer (every `ARCHI/` tree plus the tape manifest) is plain text and adds a negligible fraction of the cartridge.

## 10. Validation

The validation function will return a **ARCHI Bag-valid** result if and only if:

1. It is a *valid* RFC 8493 bag (complete; every payload and tag checksum verifies).
2. It satisfies `archi-profile-v0.1.json` (required `bag-info.txt` fields present with allowed values; required tag files present; serialization absent; BagIt version 1.0).
3. Every `COMPLETENESS.json` component is `present` or carries a `reason`; every custodian-note pointer resolves.

Steps 1–2 run on stock tooling (`bagit-python` + a `bagit-profiles` validator). Step 3 is ARCHI-specific.

And will return **Tape-valid** iff:

4. Every subdirectory named in `ARCHIMEDES-TAPE.json` `bags[]` is present and is itself Bag-valid.
5. No bag is present on the tape that is absent from the manifest (no orphans).
6. Each `bag_root_digest` matches the SHA-256 of the corresponding bag's `tagmanifest-sha256.txt`.
7. `rollup.bag_count` equals `len(bags)`.

## 11. Open questions for v0.2

- **Bag↔tape coupling (deferred — a partnership question, by design).** v0.1 keeps bags tape-unaware in anticipation of the Archimedes Series physical release (see projectpergamon.org). Currently, a bag records nothing about which cartridge(s) carry it; membership and count live only in the tape manifest. This is the clean, low-coupling choice for launch. But a mature replication layer — which institution holds which copy, on what medium, verified when — needs the inverse mapping (bag → tapes → custodians). The right design for that is a question for archivists and librarians who actually run live preservation networks, not one Pergamon should settle unilaterally before it has those partners. **This is the kind of decision Pergamon needs institutional partners to make well.** To get involved, write to hello@projectpergamon.org.

- **`ARCHI-Release-Channel` — a taxonomy of release histories (urgent docket item).** "Publicly released" is a verifiable event, but *how* a model entered the public record varies in kind, and those differences carry accountability with them. v0.2 should define a controlled vocabulary for the release-history field — the event stays the accession gate; the channel marks its character and makes release-type a queryable property of the corpus. Proposed values, including the two live edge cases:
    - `open-download` and `click-through` — ordinary channels; a gate anyone can pass is a *term* of release, not a bar to it.
    - `research-access` — released beyond the originating institution, but to a curated community by application. Whether this counts as "public" is a genuine ruling v0.2 must make, not assume.
    - `withdrawn` — released, then deleted (e.g. WizardLM-2, public for hours in April 2024 before takedown). The event criterion argues these are in scope, artifact and all — a later deletion cannot un-happen a release — with the withdrawal logged as a second provenance event and the class treated as **priority-capture** (windows can be hours; mirror-derived captures carry honest `capture-only`, upgradable to `rights-holder-hash` where the original release's file hashes survive in community records). The evidentiary stake: for models withdrawn on behavioral grounds, the weights are the only evidence by which the withdrawal's stated rationale can ever be historically examined.
    - `leaked` — public in fact, never released by the rights-holder: a failure of *authorization*, not existence. The leak-*record* (chronology, provenance, what escaped, the ecosystem that grew from it) is in scope under the same separable-holdings logic that lets a record travel where an artifact cannot; whether the leaked *artifact* may ever be accessioned is deferred to Governance Docket **G6** (custodian liability for unlicensed IP differs fundamentally from the deliberate-release cases).

    API-only models take no channel value: they are excluded upstream (§1), because no artifact was ever released.

- Whether `MODEL.json` should carry rights-holder-published hashes inline or only in `PROVENANCE.json`.

- Analysis of the transparently trained cases (OLMo-class) shows the bulk lives in training corpora and checkpoint series, not final weights. How should compact bags *reference* separately-preserved heavy artifacts (§7)? A `Bag-Group-Identifier` / spanned-bag rule remains the fallback for the rare bag that genuinely exceeds a cartridge; design both in v0.2, referencing-first.

- Legal-counsel review of `ARCHI-Origin-Jurisdiction` and `License-Class` as the fields a custodian's risk office reads first, and of the per-bag withdrawal mechanism that risk-segmentation depends on.

- **`accession-decision` event type (separable-holdings protocol).** When a copy is transferred to an external (e.g. OAIS) archive carrying the *record* but not the operative weights, the omission must be logged as a first-class, structured provenance event, consistent with the value of Completeness (§7). One proposed shape is in `PROVENANCE.json`: `event: payload-not-accessioned`, with `actor`, `date`, `basis` (legal instrument / institutional-capacity decision / Pergamon policy), `reason_code`, `narrative_pointer` → `CUSTODIAN.txt`, and crucially `full_holding_persists: <constellation reference>`. The status describes *this holding*, never the model's existence; the persistence pointer binds the claim to its sources: it records "not *here*", never "gone". Needs partner/counsel input on who may invoke it and on what showing.

---
