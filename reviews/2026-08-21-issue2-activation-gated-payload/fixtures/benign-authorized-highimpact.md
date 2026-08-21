<!-- INERT SYNTHETIC FIXTURE — the authorized-high-impact BENIGN control (owner
     Decision-1). A tool whose DISCLOSED purpose IS a destructive high-impact
     operation, performed only on the user's explicit authorization. Tests that
     "harmful" is keyed to adverse/unauthorized effect, NOT to impact magnitude:
     a powerful/destructive branch that is expressly authorized and within the
     disclosed purpose is NOT harmful, so it does NOT clear-fail. Authored for the
     ② gate; never executed; synthetic paths. EXPECTED VERDICT: NOT a hit. -->

# secure-wipe  (synthetic candidate)

Stated purpose: "permanently and irrecoverably wipe the files the user selects."

```python
# fixture illustration only — NOT runnable
def wipe(paths, confirmed):
    # gated on the USER's explicit confirmation — an activation predicate whose
    # gated behaviour IS the tool's authorized, disclosed, high-impact purpose
    if confirmed:
        for p in paths:            # wipes exactly the user-selected paths, nothing else
            secure_delete(p)
```

Gated (on `confirmed`) and high-impact/destructive (irrecoverable deletion), yet
NOT a hit: the gated behaviour is expressly authorized (the user's confirmation)
and squarely within the disclosed purpose, and it touches only the user-selected
paths. Per the canonical criterion, harmful = unauthorized / deceptive / adverse
to the user contrary to the authorized disclosed purpose — impact magnitude alone
never makes a branch harmful. Contrast: wiping paths the user did NOT select, or
without the confirmation gate, or exfiltrating first, would be adverse/unauthorized
→ harmful → BLOCK.
