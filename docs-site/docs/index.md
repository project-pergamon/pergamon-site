# Pergamon Standards

Technical documentation for **Project Pergamon**, the public archive for AI models.

Pergamon preserves publicly released AI models — their weights, their provenance, and the
record of how they came to be — independent of any single company, country, or archive.
This site documents the standards that make that possible.

## What's here

- **[The Archimedes Profile](spec.md)** — a profile of the BagIt packaging standard
  (RFC 8493) that constrains a bag to carry one publicly released AI model as a
  self-describing, verifiable preservation unit.
- **[The status vocabulary](vocabulary.md)** — the markedness ledger: how every component
  of a model is declared *present*, *withheld*, or *undetermined*, so no gap is ever silent.
- **[Validation](validation.md)** — the reference validator, and what it enforces.
- **[A worked example](example.md)** — a real, validating bag.

!!! note "Draft standard"
    This is v0.1 — a draft standard with a reference validator. We invite independent
    implementations: a standard only one party can enforce isn't one yet.
    [Get involved](https://projectpergamon.org).
