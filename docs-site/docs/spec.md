# The Archimedes Profile — v0.1 (DRAFT)

A BagIt Profile for preserving publicly released AI models as self-describing, verifiable preservation units, written many-to-a-tape.

**Status:** Draft, pre-network. Intended to be hardened with a technical collaborator and legal counsel before first custody transfer.
**Conforms to:** RFC 8493 (BagIt File Packaging Format, V1.0) and the community *bagit-profiles* convention.
**Profile document:** `archimedes-profile-v0.1.json`
**Rev note:** this revision separates the *bag* (one model) from the *tape* (many bags); see §1 and §8.

---

## 1. Scope and the three layers

The system distinguishes three things the earlier draft had wrongly collapsed into one:

- **Model** — the intellectual object: a publicly released AI model.
- **Bag** — the unit of *packaging and verification*. One bag wraps **exactly one model** (RFC 8493 + the Archimedes Profile). The bag is the atom: independently verifiable, independently custodiable, independently withdrawable.
- **Tape** — the physical **container of bags**. One LTO-9 cartridge carries **one or more bags**. The tape is a carrier, not itself a bag.

"Publicly released" means *released by the rights-holder for public download, on any terms* — which admits permissive, use-restricted, and redistribution-restricted models alike, and excludes leaks (no rights-holder release) and API-only models (no weights released). The Profile makes no claim that a model is "open"; openness is recorded per-item as metadata, not enforced at the door.

The Profile governs **packaging, integrity, and self-description** at the bag level, and **indexing** at the tape level. It is deliberately not a transfer *protocol* (discovery, replication scheduling, audit voting, repair); those belong to a network layer above it.

**A bag is intentionally tape-agnostic.** It records nothing about which cartridge carries it or what its tapemates are. How many bags fit on a tape is a *deployment fact* that varies by model selection, size, precision, and LTO generation — so it lives in the tape manifest (§8), never in the bag. This keeps the bag a stable, portable atom that can be re-written onto any medium without editing.

## 2. The payload / annotation split

BagIt treats the payload as opaque octets and does not interpret it. The Archimedes Profile uses that property as a discipline:

- **`data/`** holds the model **exactly as the rights-holder released it** — weights, the lab's own config files, tokenizer, the original `LICENSE`, the original model card. These bytes are *never edited* by Pergamon. The payload manifests verify that this artifact is byte-identical to what a third party would obtain from the source.
- **`pergamon/`** holds Pergamon's **authored interpretive layer** as tag files — provenance, the completeness ledger, custodian documentation, and normalized descriptors that *point into* `data/` without modifying it.

This mirrors the OAIS distinction between Content Information (the release) and Preservation Description Information (the annotations), and it keeps the released artifact independently checkable, separate from any commentary on it.

## 3. Bag layout (one model)

```
archimedes-<model-id>/
├── bagit.txt                     # BagIt declaration (version + encoding)
├── bag-info.txt                  # bag + model metadata (§4)
├── manifest-sha256.txt           # payload checksums
├── manifest-sha512.txt           # payload checksums (algorithm diversity)
├── tagmanifest-sha256.txt        # tag-file checksums
├── tagmanifest-sha512.txt
├── pergamon/                     # Pergamon interpretive layer (tag files)
│   ├── README.txt                # [Cat 5] plain-UTF-8 bootstrap; root of the recursion
│   ├── MODEL.json                # [Cat 1] identity + weight-file descriptor
│   ├── ARCHITECTURE.json         # [Cat 2] normalized architecture record
│   ├── TOKENIZER.json            # [Cat 3] tokenizer descriptor
│   ├── PROVENANCE.json           # [Cat 4] capture chain + integrity/authenticity
│   ├── COMPLETENESS.json         # the null/withheld ledger (§6)
│   └── CUSTODIAN.txt             # [Cat 5] narrative docs + gap explanations
└── data/                         # released bytes, unaltered
    └── model/
        ├── <weight files as released>          # [Cat 1]
        ├── config.json / generation_config.json # [Cat 2, as released]
        ├── tokenizer.json / vocab / merges      # [Cat 3, as released]
        ├── LICENSE                              # as released
        └── README.md (model card)               # as released
```

`README.txt` MUST be plain UTF-8 prose that describes this layout in human language, so a person with only a hex editor can bootstrap everything else. It is where the representation-information recursion terminates.

## 4. `bag-info.txt` fields

Colon-separated `Key: Value`, UTF-8, one element per line (RFC 8493 §2.2.2). Standard reserved fields plus a `Pergamon-` namespace. Note: there is deliberately **no tape or count field here** (§1).

| Field | Req | Meaning | Example |
|---|---|---|---|
| `Source-Organization` | ✓ | Contributing custodian/archivist | `Project Pergamon` |
| `Contact-Email` | ✓ | Accountable contact | `tk@projectpergamon.org` |
| `External-Identifier` | ✓ | Stable ID for this bag | `pergamon:archimedes:deepseek-llm-67b-base:v1` |
| `External-Description` | ✓ | One-line human description | `DeepSeek LLM 67B base, released 2023-11-29` |
| `Bagging-Date` | ✓ | Date the bag was made | `2026-06-29` |
| `Payload-Oxum` | ✓ | `octetCount.streamCount` quick check | `134217728000.12` |
| `Pergamon-Profile-Version` | ✓ | Profile version | `0.1` |
| `Pergamon-Model-Identifier` | ✓ | Canonical model id | `deepseek-ai/deepseek-llm-67b-base` |
| `Pergamon-Model-Family` | ✓ | Human family name | `DeepSeek LLM` |
| `Pergamon-Parameter-Count` | ✓ | Parameters (integer or band) | `67000000000` |
| `Pergamon-Weight-Precision` | ✓ | Released precision | `BF16` |
| `Pergamon-Release-Date` | ✓ | Original public release | `2023-11-29` |
| `Pergamon-Rights-Holder` | ✓ | Releasing entity | `DeepSeek` |
| `Pergamon-Origin-Jurisdiction` | ✓ | ISO country of lead developer | `CN` |
| `Pergamon-License-Identifier` | ✓ | SPDX id or named license | `DeepSeek-License` |
| `Pergamon-License-Class` | ✓ | `permissive` \| `restricted-use` \| `restricted-redistribution` \| `undetermined` | `restricted-redistribution` |
| `Pergamon-Regenerable` | ✓ | Recipe-reproducible? `yes`\|`partial`\|`no`\|`undetermined` | `no` |
| `Pergamon-Completeness` | ✓ | `complete`\|`partial`\|`weights-only` | `weights-only` |
| `Pergamon-Capture-Source` | ✓ | Where captured, with revision | `hf.co/deepseek-ai/...@<commit>` |
| `Pergamon-Authenticity-Basis` | ✓ | Strongest anchor available (§5) | `capture-only` |

`License-Class` and `Regenerable` are **independent axes** — license openness and process openness are different questions, and the Profile records both rather than collapsing them.

## 5. Integrity and authenticity (the honest part)

Two different guarantees, kept separate so neither is oversold:

- **Internal integrity** — the dual `manifest-sha256` / `manifest-sha512` files certify that this bag's contents are complete and unaltered *since bagging*. Algorithm diversity hedges a future break in either hash. This catches decay and accidental corruption. Per RFC 8493, BagIt fixity is **not designed to defend against active attack** — an adversary who can rewrite a file can rewrite its checksum.

- **Source authenticity** — whether the payload is the *genuine release* (not a fork) is a separate, harder question that fixity alone cannot answer, especially for non-regenerable models. `PROVENANCE.json` records the strongest anchor that actually exists, and `Pergamon-Authenticity-Basis` names it honestly:
  - `rights-holder-signature` — the release was cryptographically signed by the rights-holder; strongest.
  - `rights-holder-hash` — the rights-holder published a checksum at release that the payload matches.
  - `capture-only` — no independent anchor; integrity asserted from a documented capture event only. **This is an honest admission, not a defect** — it tells a future scholar exactly how far the authenticity claim extends.
  - `undetermined` — our review could not establish an anchor (carries a review reference).

The Profile never lets a manifest match *masquerade* as proof of authenticity. Cross-tape Byzantine quorum (a network-layer concern, above this Profile) is what defends the constellation against tampering; per-bag manifests defend the copy against decay.

## 6. The completeness ledger — `COMPLETENESS.json`

The centerpiece. Bare `null` is forbidden, because it conflates "the lab never released this" with "Pergamon failed to record it" — and the difference between documenting the field's secrecy and documenting your own gaps is the whole point. Every component carries an explicit **status** from a controlled vocabulary; any non-`present` status MUST carry a reason and SHOULD link to a `CUSTODIAN.txt` anchor.

**Status vocabulary**

| Status | Means | Accountability | Required floor | Example |
|---|---|---|---|---|
| `present` | Captured and in the bag | — | path | weights, config |
| `withheld` | Existed; the rights-holder chose not to release it | outward (lab's decision) | `evidence` of intent + reason | closed training data |
| `not-applicable` | Never existed for this model | structural | reason | no merges file for a byte-level tokenizer |
| `unrecoverable` | Was publicly released but Pergamon could not capture it | inward (capture failure) | reason | eval card offline at capture |
| `undetermined` | Pergamon's review ran and was inconclusive | inward (knowledge limit, handed forward) | `review` reference with date | training logs of indeterminate status |

There is deliberately **no `unknown`**. "Unknown" is a shrug that assigns no accountability; every gap here points somewhere. `withheld` documents *the rights-holder's* decision; `unrecoverable` and `undetermined` document *Pergamon's* limits — the first a capture failure (we know it existed; we couldn't get it), the second a knowledge failure (our review could not establish it). A future historian can always tell which is which.

**The two floors that keep the vocabulary honest:**

- **`withheld` requires evidence of intent.** Asserting that a rights-holder *chose* to withhold something is a claim about their decision, and an unevidenced claim of intent is itself an unmarked guess. `withheld` is legal only when the choice can be evidenced (the lab said so; the release included everything *but* this; the license implies it). When intent cannot be evidenced, the honest status is `undetermined` — about the gap's very nature.
- **`undetermined` has to show it looked.** A bare `undetermined` decays into `unknown` with better PR. Every `undetermined` carries a `review` reference — which review process ran, and when ("v0.1 review, 2026-06") — so the claim "we did our best" is checkable, and so a later determination reads as a dated improvement to the record rather than a contradiction of it. `undetermined` is process-relative and expected to change; the date is what marks *when we looked*.

**Descriptive-field escape hatch.** The bag-info fields most vulnerable to orphaned or provenance-broken models — `Pergamon-Origin-Jurisdiction`, `Pergamon-Release-Date`, `Pergamon-Parameter-Count`, `Pergamon-Weight-Precision` — MAY take the literal value `undetermined` rather than forcing a guess entered as fact. A confident fiction is worse than a marked gap.

**Example**

```json
{
  "schema": "pergamon-completeness/0.1",
  "model_id": "deepseek-ai/deepseek-llm-67b-base",
  "components": {
    "weights":                 { "status": "present", "path": "data/model/", "files": 12,
                                 "bytes": 134217728000 },
    "architecture_config":     { "status": "present", "path": "data/model/config.json" },
    "tokenizer":               { "status": "present", "path": "data/model/tokenizer.json" },
    "original_license":        { "status": "present", "path": "data/model/LICENSE" },
    "model_card":              { "status": "present", "path": "data/model/README.md" },

    "training_data":           { "status": "withheld",
                                 "evidence": "Release shipped weights, config, and tokenizer but no corpus; model card names the data only in aggregate terms.",
                                 "reason": "Training corpus was never publicly released by the rights-holder.",
                                 "custodian_note": "pergamon/CUSTODIAN.txt#training-data" },
    "training_code":           { "status": "withheld",
                                 "evidence": "Repository contains inference code only; no training scripts in any release artifact.",
                                 "reason": "No training code accompanied the release." },
    "intermediate_checkpoints":{ "status": "not-applicable",
                                 "reason": "Only final weights were part of this release." },
    "training_logs":           { "status": "undetermined",
                                 "review": "v0.1 review, 2026-06",
                                 "reason": "Our review could not establish whether logs exist internally." },
    "evaluation_results":      { "status": "unrecoverable",
                                 "reason_code": "source-removed",
                                 "reason": "Benchmark card linked from the release was offline at capture (2026-06-29).",
                                 "custodian_note": "pergamon/CUSTODIAN.txt#eval" }
  },
  "rollup": { "completeness": "weights-only", "regenerable": "no" }
}
```

`Pergamon-Completeness` and `Pergamon-Regenerable` in `bag-info.txt` are the human-facing roll-up of this ledger; the ledger is the auditable detail behind them.

## 7. Other tag-file schemas (sketch)

- **`MODEL.json`** [Cat 1] — identity (id, family, params, precision), and the weight-file inventory: each file's role, byte size, format (`safetensors`/`gguf`/…), shard index, and SHA-256 (duplicating the manifest for self-containment of the descriptor).
- **`ARCHITECTURE.json`** [Cat 2] — normalized architecture record: family/type, layer/width/head counts, context length, position-encoding, activation, plus a pointer to the as-released `config.json`. Pergamon's normalization sits *beside* the original, never replacing it.
- **`TOKENIZER.json`** [Cat 3] — tokenizer type (BPE/SentencePiece/byte-level), vocab size, special tokens, and pointers to the as-released tokenizer files. Flags whether the tokenizer is reconstructible from the payload alone.
- **`PROVENANCE.json`** [Cat 4] — capture chain (source URL, repo revision/commit, capture timestamp, capturing agent), any rights-holder-published hashes/signatures, and the authenticity basis (§5).
- **`CUSTODIAN.txt`** [Cat 5] — plain-language narrative for a future custodian: what this model is, why it was preserved, every gap from `COMPLETENESS.json` explained in prose, and any handling notes. Anchors (e.g. `#training-data`) are referenced from the ledger.

## 8. The tape layer — many bags per cartridge

A tape is an LTFS filesystem whose root holds one or more complete bags plus a tape manifest. **The bags do not know they share a cartridge; the tape manifest is the only place membership and count are recorded.** This is the clean, low-coupling choice for v0.1 (see the deferred coupling question in §10).

**Tape layout**

```
<LTFS volume root>/
├── TAPE-README.txt              # plain-UTF-8 bootstrap for the whole cartridge
├── ARCHIMEDES-TAPE.json         # tape manifest: which bags, order, rollup
├── archimedes-olmo-7b/          # a complete, standalone bag
│   └── (bagit.txt, bag-info.txt, manifest-*, tagmanifest-*, pergamon/, data/)
├── archimedes-pythia-12b/       # another complete bag
└── archimedes-bloom-176b/       # another
```

Each subdirectory is a fully valid Archimedes bag on its own. The tape manifest is an index over them, not a bag itself, and is **not** governed by BagIt — it is a Pergamon construct.

**`ARCHIMEDES-TAPE.json`** — the count lives in `rollup.bag_count`; the membership lives in `bags[]`; nothing here is duplicated inside the bags.

```json
{
  "schema": "pergamon-tape/0.1",
  "tape_id": "pergamon:archimedes:tape:0001",
  "tape_title": "Archimedes I",
  "series": "Archimedes",
  "medium": { "type": "LTO-9", "native_capacity_bytes": 18000000000000, "ltfs": true },
  "written": { "date": "2026-06-29", "agent": "Project Pergamon", "host_jurisdiction": "US" },
  "selection_rationale": "First proof: permissive, regenerable Western models with low custody risk.",
  "bags": [
    { "path": "archimedes-olmo-7b",
      "model_id": "allenai/OLMo-7B",
      "payload_oxum": "13958643712.4",
      "license_class": "permissive",
      "regenerable": "yes",
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

**`bag_root_digest`** gives the tape a way to commit to each bag without coupling the bag to the tape. It is the SHA-256 of the bag's `tagmanifest-sha256.txt`. Because that tag manifest checksums the payload manifests, which in turn checksum every payload file, a single digest transitively commits to the entire bag (a Merkle-style root). The tape vouches for its bags; the bags remain unaware of the tape.

**`TAPE-README.txt`** MUST be plain UTF-8 and is the cartridge-level bootstrap: what this tape is, the human-readable list of bags, the instruction that each subdirectory is a standalone bag whose own `pergamon/README.txt` explains it, the selection rationale, and a contact. It terminates the representation-information recursion at the cartridge level, one rung above each bag's own README.

**Serialization and write order.**
- **Serialization is forbidden** at the bag level: a bag lives inside LTFS as a real directory tree, not a `.zip`/`.tar`, preserving direct file access and letting a custodian validate without unpacking.
- **Non-normative write recommendation:** write the LTFS index, then `TAPE-README.txt` and `ARCHIMEDES-TAPE.json`, then the bags — so a custodian mounting the cartridge can read the orientation docs and the inventory from the front without winding to the end. LTO is linear; this is an access-time concern, not a capacity one. The entire annotation layer (every `pergamon/` tree plus the tape manifest) is plain text and adds a negligible fraction of the cartridge.

## 9. Validation

**Bag-valid** iff:
1. It is a *valid* RFC 8493 bag (complete; every payload and tag checksum verifies).
2. It satisfies `archimedes-profile-v0.1.json` (required `bag-info.txt` fields present with allowed values; required tag files present; serialization absent; BagIt version 1.0).
3. Every `COMPLETENESS.json` component is `present` or carries a reason; every custodian-note pointer resolves.

Steps 1–2 run on stock tooling (`bagit-python` + a `bagit-profiles` validator). Step 3 is Archimedes-specific.

**Tape-valid** iff:
4. Every subdirectory named in `ARCHIMEDES-TAPE.json` `bags[]` is present and is itself Bag-valid.
5. No bag is present on the tape that is absent from the manifest (no orphans).
6. Each `bag_root_digest` matches the SHA-256 of the corresponding bag's `tagmanifest-sha256.txt`.
7. `rollup.bag_count` equals `len(bags)`.

## 10. Open questions for v0.2

- **Bag↔tape coupling (deferred — a partnership question, by design).** v0.1 keeps bags tape-unaware: a bag records nothing about which cartridge(s) carry it; membership and count live only in the tape manifest. This is the clean, low-coupling choice for launch. But a mature replication layer — which institution holds which copy, on what medium, verified when — needs the inverse mapping (bag → tapes → custodians). The right design for that is a question for archivists and librarians who actually run live preservation networks, not one Pergamon should settle unilaterally before it has those partners. **This is exactly the kind of decision Pergamon needs institutional partners to make well — and a concrete reason the project seeks them.**
- Edge cases of "publicly released" (click-through gating, post-release withdrawal, research-access-only) — needs a one-line FAQ ruling and possibly a `Pergamon-Release-Channel` field.
- Whether `MODEL.json` should carry rights-holder-published hashes inline or only in `PROVENANCE.json`.
- Multi-tape models that exceed one cartridge: a bag larger than a tape needs either a `Bag-Group-Identifier` split across tapes or an explicit "spanned bag" rule — interacts with the coupling question above.
- Legal-counsel review of `Pergamon-Origin-Jurisdiction` and `License-Class` as the fields a custodian's risk office reads first, and of the per-bag withdrawal mechanism that risk-segmentation depends on.
- **`accession-decision` event type (separable-holdings protocol).** When a copy is transferred to an external (e.g. OAIS) archive carrying the *record* but not the operative weights, the omission must be logged as a first-class, structured provenance event — not left as a silent gap (the same `null`-vs-`withheld` discipline, one level up). Proposed shape in `PROVENANCE.json`: `event: payload-not-accessioned`, with `actor`, `date`, `basis` (legal instrument / institutional-capacity decision / Pergamon policy), `reason_code`, `narrative_pointer` → `CUSTODIAN.txt`, and crucially `full_holding_persists: <constellation reference>`. The status describes *this holding*, never the model's existence; the persistence pointer is what keeps federation honest (records "not *here*", not "gone"). Needs partner/counsel input on who may invoke it and on what showing.
