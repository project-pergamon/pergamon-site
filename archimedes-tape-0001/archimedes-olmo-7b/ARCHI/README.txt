ARCHIMEDES BAG — plain-text bootstrap
=====================================
This directory is one Archimedes bag: a single publicly released AI model,
packaged per RFC 8493 (BagIt) and ARCHI (the Archimedes Profile) v0.1.

Model:        OLMo-7B (base), released 2024-02-01 by the Allen Institute for AI.
License:      Apache-2.0 (permissive).  Process: fully open (regenerable).

WHAT IS WHERE
  data/model/      The model exactly as the rights-holder released it
                   (weights, config, tokenizer, LICENSE, model card).
                   NOTE: in THIS demonstration bag the large binaries are
                   clearly-marked *.PLACEHOLDER stand-ins; the metadata layer
                   below is real and complete.
  ARCHI/           Project Pergamon's interpretive layer (this directory):
    MODEL.json         identity + weight-file inventory
    ARCHITECTURE.json  normalized architecture record
    TOKENIZER.json     tokenizer descriptor
    PROVENANCE.json    where these bytes came from + authenticity basis
    COMPLETENESS.json  what is present / withheld / unknown (the ledger)
    CUSTODIAN.txt      narrative notes for a future custodian (read this)
  manifest-*.txt       checksums of every payload file
  tagmanifest-*.txt    checksums of every tag file

TO VERIFY
  Any RFC 8493 tool (e.g. `bagit.py --validate .`) confirms completeness and
  fixity. The ARCHI Profile additionally requires the ARCHI/ files
  above and the bag-info fields in ../bag-info.txt.

This text is intentionally plain UTF-8 so it is readable with no tools at all.
