# Validation

A bag is **ARCHI-valid** when three layers of checks pass:

1. **RFC 8493** — it is a complete, fixity-verified BagIt bag (stock tooling:
   `bagit-python`).
2. **The profile** — required `bag-info.txt` fields present with legal values;
   required tag files present.
3. **The ledger floors** — every component's status carries its required floor
   (see [vocabulary](vocabulary.md)).

## Running the reference validator

```bash
python3 validate_archimedes.py <tape-or-bag-directory> archi-profile-v0.1.json
```

Against a tape directory it additionally checks: every bag in `ARCHIMEDES-TAPE.json`
is present and valid, no orphan bags exist, each `bag_root_digest` matches, and the
rollup arithmetic agrees with the details it summarizes.

!!! warning "Fixity cannot guarantee authenticity"
    Manifests certify a bag is unaltered *since bagging*. Whether the payload is the
    genuine release is recorded separately in `ARCHI-Authenticity-Basis` — and
     `capture-only` lets acquisition agents take an honest stance when archiving models that fail to meet all other standards. 
     
---
