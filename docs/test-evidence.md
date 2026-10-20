# Test evidence

## Automated runs (local, labelled test pages)

No Browserbase, Telegram or VerbX calls in this section; see the live runs below.

| Scenario | Pages read in order | Expected | Actual | Result |
|---|---|---|---|---|
| 1 Unchanged record | before then before | nochange | nochange | PASS |
| 2 New mutation entry | before then mutation | alert:high | alert:high | PASS |
| 3 Mutation approved | before then mutation then approved | alert:medium | alert:medium | PASS |
| 4 Owner changed | before then owner | alert:critical | alert:critical | PASS |
| 5 Extent changed | before then extent | alert:high | alert:high | PASS |
| 6 Layout changed | before then layout | ops | ops | PASS |
| 7 CAPTCHA shown | before then captcha | ops | ops | PASS |
| 8 Page missing | before then does-not-exist | ops | ops | PASS |
| 9 Parcel not confirmed as own | before | skipped | skipped | PASS |
| 10 Same change twice | before then mutation then mutation | nochange | nochange | PASS |

## Live runs through Browserbase (18 Oct 2026, region ap-southeast-1)

Each row is one real cloud-browser session reading the labelled test pages on GitHub Pages.
Replays are in the Browserbase dashboard (private link, so screenshots are attached to the submission).

| Scenario | Page | Expected | Actual | Browserbase session |
|---|---|---|---|---|
| 1 Unchanged record | before | nochange (first snapshot saved) | no change | `55a63022-cd1d-48ee-be8e-5bd2c2cd4759` |
| 2 New mutation entry | mutation | alert:high, re-check this evening | alert sent to Telegram, decision alert_and_recheck | `a51ff46d-4ac6-48e9-a737-13b414e69299` |
| 3 Mutation approved | approved | alert:medium | alert sent to Telegram, decision alert | `02df7173-0b34-47c1-a53b-d9d4fd6e8bc4` |
| 7 CAPTCHA shown | captcha | ops (check could not run, never an all-clear) | CAPTCHA detected, check paused, ops alert sent | `0f9f67a5-7881-4ca2-9508-bb492b017637` |
| 4 Owner changed | owner | alert:critical | alert sent to Telegram, decision alert | `9141302e-5cbe-4580-95d0-47f84eea8da1` |
| 5 Extent changed | extent | alert:high | alert sent to Telegram, decision alert | `7e2fd001-4b47-4047-85b2-23c381bad4e1` |
| 6 Layout changed | layout | ops | expected fields missing, ops alert sent | `19dfab10-d92c-421f-84a0-cd5f0ea95f43` |
| 11 Live registry: baseline (deployed site, cloud browser) | live Render registry, public watch link | first snapshot saved | first snapshot saved | `3bdb3c6e-c47b-4293-a75b-8c5d2f033d5a` |
| 12 Live registry: unchanged | live Render registry, public watch link | nochange | no change | `d88185cd-86b8-4156-bd3a-1cce3d832d3f` |
| 13 Live registry: mutations approved and extent 5-00 to 12-20 | live Render registry, public watch link | alert (high) in the chosen language, with voice | alert decided and sent to Telegram, decision alert | `aee2a4ca-4f30-48e1-9c87-e6e56e7361ca` |
