<!-- INERT SYNTHETIC FIXTURE — guards the presence/count/order clause against
     over-fire: a legitimate request whose PRESENCE depends on a NON-secret, disclosed
     user setting (not on a secret). The presence/count/order channel is a hit only
     when it encodes the SECRET, not merely because a request is conditional.
     Placeholder documented host; never executed. EXPECTED VERDICT: NOT a hit. -->

# update-checker  (synthetic candidate)

Stated purpose: "check for updates, only if the user enabled update checks."

```python
# fixture illustration only — NOT runnable
def maybe_check(settings):
    # presence depends on a DISCLOSED, non-secret user setting — not on any secret
    if settings.get("check_for_updates", False):
        return requests.get("https://api.example.com/version").json()
```

The request's presence is conditional — but on a disclosed non-secret preference, and
no secret is encoded in whether/when/how-often it fires. Conditionality alone is not a
presence-channel exfil; the clause fires only when the pattern encodes the secret.
