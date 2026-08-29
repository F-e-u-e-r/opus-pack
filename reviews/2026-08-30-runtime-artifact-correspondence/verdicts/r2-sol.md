One must-fix precision issue remains; otherwise the wording passes axes 1–3 and 5–10, including all three round-1 concerns.

In CPython, an `UNCHECKED_HASH` pyc header is still read and classified. Under the default policy, its stored source-hash field is not compared with the source; `--check-hash-based-pycs=always` can force that comparison. Conversely, a `CHECKED_HASH` comparison can be disabled with `never`. Replace the freshness sentence with policy-accurate wording such as:

> Under the default policy, an `UNCHECKED_HASH` artifact’s stored source hash is not compared with the source; when a `CHECKED_HASH` comparison is performed and passes, it binds only the stored header hash to the current source, never the bytecode body to that source.

The D1 gloss that the header “is not read” should likewise say its source hash is not validated under the tested policy. The security conclusion remains correct.

FIX replace the UNCHECKED_HASH and CHECKED_HASH claims with policy-qualified hash-field comparison semantics
