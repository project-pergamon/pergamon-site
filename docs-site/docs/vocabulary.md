# The markedness vocabulary 

Every component of a preserved model carries an explicit label that denotes the status of Pergamon's review. There is deliberately no `unknown` — a gap with no assigned accountability fails validation. Our epistemology follows the principle that humans make decisions about what we do or don't know, and that a system becomes more truthful when decision-makers must link their reputation as a custodian their decisions. The methodological standards for what constitues a comprehensive investigation will surely change over time, and, in any event, our intial standard must be written with preservation experts. For now, our custodial responsibility dictates that all claims we make about history remain marked, and that all the things we **don't know** remain marked as well. 

| Status | Means | Accountability | Required floor |
|---|---|---|---|
| `present` | Captured and in the bag | inward (governance and practices) | `path` or `external_ref` |
| `withheld` | Existed; the rights-holder chose not to release it | outward | `evidence` of intent + `reason` |
| `not-applicable` | Never existed for this model | structural | `reason` |
| `unrecoverable` | Was public; Pergamon could not capture it | inward (capture failure) | `reason` |
| `undetermined` | Pergamon's review ran and was inconclusive | inward (handed forward) | `review` reference with date |

## Gaps in the record come with marked responsibility

**`withheld` requires evidence of intent.** Asserting that a rights-holder *chose* to
withhold something is a claim about their decision. When intent cannot be evidenced,
the honest status is `undetermined`.

**`undetermined` has to show it looked.** Every `undetermined` carries a review
reference — which process ran, and when — so "we did our best" is checkable, and a
later determination reads as a dated improvement rather than a contradiction.

## Example

```json
"training_data": {
  "status": "withheld",
  "evidence": "Release shipped weights, config, and tokenizer but no corpus.",
  "reason": "Training corpus was never publicly released by the rights-holder.",
  "custodian_note": "ARCHI/CUSTODIAN.txt#training-data"
}
```

The only derived summary is `ARCHI-Ledger-Resolution` (`resolved` | `unresolved`): whether any component remains `undetermined`. It summarizes the state of the review, never the model. Everything else is read, not graded.

---
