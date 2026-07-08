ARCHIMEDES TAPE 0001 — "Archimedes I"
=====================================
A single LTO-9 cartridge (LTFS) carrying one or more Archimedes bags. Each
subdirectory named below is a complete, standalone bag; read its own
ARCHI/README.txt to understand it. Membership and count are recorded ONLY
here, in ARCHIMEDES-TAPE.json — the bags themselves do not know they share a
cartridge.

BAGS ON THIS TAPE
  archimedes-olmo-7b/   allenai/OLMo-7B  (permissive, regenerable, US)

This is a demonstration tape: it holds one bag whose large binaries are
stand-ins. The format, manifests, ledger, and tape index are real.

VERIFY
  Per bag:  bagit.py --validate archimedes-<model>/
  Per tape: every bag in ARCHIMEDES-TAPE.json is present and valid; no bag is
            present that the manifest omits; each bag_root_digest matches the
            SHA-256 of that bag's tagmanifest-sha256.txt.
