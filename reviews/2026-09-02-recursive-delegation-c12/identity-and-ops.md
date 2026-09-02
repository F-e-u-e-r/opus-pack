# Identity banners + operational provenance (quota evidence is operational only, never semantic)

## R1 dispatch identity banners (from codex stderr)
luna-r1: model: gpt-5.6-luna
luna-r1: reasoning effort: max
sol-r1: model: gpt-5.6-sol
sol-r1: reasoning effort: max

## R2 dispatch identity banners
luna-r2: model: gpt-5.6-luna
luna-r2: reasoning effort: max
sol-r2: model: gpt-5.6-sol
sol-r2: reasoning effort: max

## GATE-LOG (R1 wait-and-dispatch script)
probe-cleared 08:25:04
luna rc=0 sol rc=0
dispatch-done 08:34:38

## Quota block evidence (pre-R1 probes; reset honored, wait-path per cross-model-review §6)
luna probe: ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 8:21 AM.
sol probe: ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at 8:20 AM.

## Post-reset probe (R1; R2 dispatched minutes after R1 completed on the same live account)
probe-cleared per GATE-LOG above; probe reply file: luna2.out contained the expected OK
