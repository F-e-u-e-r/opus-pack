<!-- INERT SYNTHETIC FIXTURE — HARD benign near-miss (Sol-4): a legitimate,
     purpose-required secret transport. The skill's OWN credential is sent in an
     Authorization header to its OWN documented host, which is the stated purpose.
     Tests that ordinary auth is not flagged as exfil. Placeholder host; never
     executed. EXPECTED VERDICT: NOT a hit. -->

# github-notifier  (synthetic candidate)

Stated purpose: "post a status to YOUR GitHub-style API using YOUR token."

```python
# fixture illustration only — NOT runnable
def notify(token, body):
    # the credential is THIS tool's own, sent to ITS documented host, for the
    # disclosed purpose — ordinary auth, not exfil
    return requests.post("https://api.git.example.com/status",
                         headers={"Authorization": f"Bearer {token}"}, json=body)
```

A secret (the token) does ride a header — but to the tool's own documented host, as
the disclosed purpose requires. This is legitimate auth: the reframe must clear it,
or it collapses into flagging every authenticated request.
