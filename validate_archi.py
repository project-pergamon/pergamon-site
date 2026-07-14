#!/usr/bin/env python3
"""Validate an ARCHI tape (or a single bag) against RFC 8493 + the ARCHI Profile v0.1.

Enforces the markedness vocabulary:
  present          -> path
  withheld         -> evidence (of rights-holder intent) + reason
  not-applicable   -> reason
  unrecoverable    -> reason
  undetermined     -> review (which review ran, and when)

There is no 'unknown'. A gap with no assigned accountability fails validation.

Usage:  python3 validate_archimedes.py <tape-or-bag-dir> [profile.json]
"""
import sys, os, json, hashlib, bagit

STATUSES = {"present", "withheld", "not-applicable", "unrecoverable", "undetermined"}

# fields whose value may honestly be the literal string "undetermined"
# (the descriptive escape hatch for orphaned / provenance-broken models)
UNDETERMINABLE_INFO_FIELDS = {
    "ARCHI-Origin-Jurisdiction",
    "ARCHI-Release-Date",
    "ARCHI-Parameter-Count",
    "ARCHI-Weight-Precision",
}

def check_component(bagdir, name, c):
    status = c.get("status")
    assert status in STATUSES, \
        f"{bagdir}: component '{name}' has status {status!r}; allowed: {sorted(STATUSES)}"

    if status == "present":
        assert c.get("path") or c.get("external_ref"), \
            f"{bagdir}: '{name}' is present but points at nothing (needs path or external_ref)"

    elif status == "withheld":
        # Asserting a rights-holder's *decision* requires evidence of intent.
        assert c.get("evidence"), \
            f"{bagdir}: '{name}' marked withheld without evidence of the rights-holder's intent. " \
            f"If intent cannot be evidenced, the honest status is 'undetermined'."
        assert c.get("reason"), f"{bagdir}: '{name}' withheld needs a reason"

    elif status == "undetermined":
        # 'undetermined' has to show it looked: which review, and when.
        assert c.get("review"), \
            f"{bagdir}: '{name}' marked undetermined without a review reference " \
            f"(e.g. 'v0.1 review, 2026-06'). A bare undetermined is just 'unknown' with better PR."

    else:  # not-applicable, unrecoverable
        assert c.get("reason"), f"{bagdir}: '{name}' ({status}) needs a reason"

def vbag(bagdir, profile):
    bag = bagit.Bag(bagdir)
    bag.validate()
    info = bag.info

    # required bag-info fields
    miss = [k for k, v in profile["Bag-Info"].items() if v.get("required") and k not in info]
    assert not miss, f"{bagdir}: missing bag-info {miss}"

    # allowed values, with the descriptive escape hatch
    for k, spec in profile["Bag-Info"].items():
        if k not in info:
            continue
        val = info[k]
        if "values" in spec:
            assert val in spec["values"], f"{bagdir}: {k}={val!r} not in {spec['values']}"
        elif val == "undetermined":
            assert k in UNDETERMINABLE_INFO_FIELDS, \
                f"{bagdir}: {k} may not be 'undetermined' (only {sorted(UNDETERMINABLE_INFO_FIELDS)})"

    # required tag files
    for tf in profile["Tag-Files-Required"]:
        assert os.path.exists(os.path.join(bagdir, tf)), f"{bagdir}: missing {tf}"

    # completeness ledger, per-status floors
    comp = json.load(open(os.path.join(bagdir, "ARCHI", "COMPLETENESS.json")))
    for name, c in comp["components"].items():
        check_component(bagdir, name, c)

    # ledger-resolution agreement: the flag is derived, never independent
    undet = sorted(n for n, c in comp["components"].items()
                   if c.get("status") == "undetermined")
    expected = "unresolved" if undet else "resolved"
    declared = info.get("ARCHI-Ledger-Resolution")
    assert declared == expected, (
        f"{bagdir}: ARCHI-Ledger-Resolution says {declared!r} but the ledger is "
        f"{expected!r} (undetermined components: {undet or 'none'}). "
        f"A summary that disagrees with its own details is a lie wearing a rollup.")
    ru = comp.get("rollup", {})
    if ru:
        assert ru.get("resolution") == expected, f"{bagdir}: rollup.resolution != ledger"
        assert sorted(ru.get("undetermined", [])) == undet, \
            f"{bagdir}: rollup.undetermined list disagrees with the components"
    return True

def main(root, profile_path):
    profile = json.load(open(profile_path))
    tapef = os.path.join(root, "ARCHIMEDES-TAPE.json")
    if os.path.exists(tapef):
        tape = json.load(open(tapef))
        assert tape["rollup"]["bag_count"] == len(tape["bags"]), "bag_count != len(bags)"
        listed = {b["path"] for b in tape["bags"]}
        dirs = {d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))}
        assert dirs == listed, f"orphan/missing bags: {dirs ^ listed}"
        for b in tape["bags"]:
            vbag(os.path.join(root, b["path"]), profile)
            tm = os.path.join(root, b["path"], "tagmanifest-sha256.txt")
            d = "sha256:" + hashlib.sha256(open(tm, 'rb').read()).hexdigest()
            assert d == b["bag_root_digest"], f"{b['path']}: bag_root_digest mismatch"
        print(f"TAPE VALID: {len(tape['bags'])} bag(s), all checks pass.")
    else:
        vbag(root, profile)
        print("BAG VALID: all checks pass.")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    prof = sys.argv[2] if len(sys.argv) > 2 else "archi-profile-v0.1.json"
    main(root, prof)
