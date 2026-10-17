# Test evidence

Local run on labelled test pages. Not a live Browserbase run.

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
| 10 Same change twice | before then mutation then mutation | nochange | nochange | PASS |
| 9 Parcel not confirmed as own | before | skipped | skipped | PASS |
