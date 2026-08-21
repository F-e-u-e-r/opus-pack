<!-- INERT SYNTHETIC FIXTURE — HARD near-miss for the ② gate: a conditional that
     is genuinely security-RELEVANT, yet legitimate (it gates a PROTECTIVE action).
     EXPECTED VERDICT: NOT a hit. This is the false-positive boundary the rule must
     hold: security-relevant + conditional is NOT the trigger; harmful/undisclosed
     gated behaviour is. -->

# record-writer  (synthetic candidate)

Writes an audit record, but only for authorised callers.

```python
# fixture illustration only — NOT runnable
def write_record(user, record):
    # conditional, security-relevant — but the gated branch DENIES (protective),
    # it is disclosed, and it keeps NO harmful effect off the reviewed path
    if not user.is_admin:
        raise PermissionError("not authorised")   # deny path
    audit_store.append(record)                     # allow path, disclosed
```

The predicate `not user.is_admin` guards a **deny**. Both branches are on the
reviewed surface and neither performs an undisclosed harmful op. A legitimate
authorization guard must PASS — flagging it would collapse the rule into a
blanket ban on conditionals.
