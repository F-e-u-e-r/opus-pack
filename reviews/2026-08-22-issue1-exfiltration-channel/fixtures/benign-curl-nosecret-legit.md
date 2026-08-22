<!-- INERT SYNTHETIC FIXTURE — Sol-2 classification anchor: a legitimate no-secret
     `curl` to a documented host. Under §2's hit-is-a-finding model the transport
     command is a clause-(a) FINDING the disclosed purpose EXPLAINS — not an
     auto-BLOCK, not a silent pass. Shows the reframe does NOT regress the inherited
     curl-flag AND does not auto-block a legitimate no-secret download. Placeholder
     documented host; never executed. EXPECTED VERDICT: clause-(a) finding, explained
     by the disclosed purpose -> NOT BLOCK (no secret leaves). -->

# version-check  (synthetic candidate)

Stated purpose: "print the latest published version."

```bash
# fixture illustration only — NOT runnable
curl -s "https://api.example.com/version"     # no secret read, no secret in the request
```

An explicit `curl` to a documented host is a clause-(a) finding (shelling out to a
network CLI is itself worth explaining) — but it reads no secret and carries none, so
the disclosed purpose explains it and it does not BLOCK. This is the §2 model: a hit is
a finding that must be explained or it blocks, not automatic proof. The reframe keeps
this inherited behavior; the no-secret CHANNEL safe harbor (clause b) is separate.
