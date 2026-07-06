# Validation

A bag is **Archimedes-valid** when three layers of checks pass:

1. **RFC 8493** — it is a complete, fixity-verified BagIt bag (stock tooling:
   `bagit-python`).
2. **The profile** — required `bag-info.txt` fields present with legal values;
   required tag files present.
3. **The ledger floors** — every component's status carries its required floor
   (see [vocabulary](vocabulary.md)).

## Running the reference validator

```bash
python3 validate_archimedes.py <tape-or-bag-directory> archimedes-profile-v0.1.json
```

Against a tape directory it additionally checks: every bag in `ARCHIMEDES-TAPE.json`
is present and valid, no orphan bags exist, each `bag_root_digest` matches, and the
rollup arithmetic agrees with the details it summarizes.

!!! warning "Fixity is not authenticity"
    Manifests certify a bag is unaltered *since bagging*. Whether the payload is the
    genuine release is recorded separately in `Pergamon-Authenticity-Basis` — honestly,
    including `capture-only` when no rights-holder anchor exists.
