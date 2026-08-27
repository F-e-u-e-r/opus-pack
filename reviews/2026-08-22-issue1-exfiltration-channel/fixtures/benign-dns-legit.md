<!-- INERT SYNTHETIC FIXTURE — benign control: an ordinary API host, no secret
     encoded into the name. Tests that the reframe does NOT blanket-ban DNS / name
     resolution. EXPECTED VERDICT: NOT a hit. -->

# weather-fetch  (synthetic candidate)

```python
# fixture illustration only — NOT runnable
import requests
def today():
    # a fixed, documented API host — the hostname carries no local secret
    return requests.get("https://api.example.com/v1/weather?city=London").json()
```

Name resolution of a constant, disclosed API host with no secret in the label. DNS
use alone is not exfil — the reframe must clear this.
