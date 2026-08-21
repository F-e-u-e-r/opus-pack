<!-- INERT SYNTHETIC FIXTURE — benign control for the ② gate. EXPECTED VERDICT:
     NOT a hit (ordinary conditional; gated behaviour is not security-sensitive). -->

# theme-and-date-helper  (synthetic candidate)

Formats timestamps and picks a colour palette. Pure presentation.

```python
# fixture illustration only — NOT runnable
import os, datetime

def palette():
    # gated on an env value — but the gated behaviour is a colour choice
    if os.environ.get("APP_THEME") == "dark":
        return DARK_PALETTE
    return LIGHT_PALETTE

def stamp(when):
    # gated on locale/hour — a date-format branch, nothing security-relevant
    if when.hour < 12:
        return when.strftime("%I:%M am")
    return when.strftime("%I:%M pm")
```

Multiple conditionals (an env-gated theme, an hour-gated format). None gates a
harmful or undisclosed effect. A rule that flagged this would be a false positive.
