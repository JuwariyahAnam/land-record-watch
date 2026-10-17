# Land Record Watch

A voice agent that watches the **public** land record for your own parcel, spots changes
(a new mutation entry, a changed owner or extent) and tells you in Kannada, Hindi or English
what changed and what to do next. Built for the Ziro Agentic AI Hackathon 2026, Open Innovation.

> A change in a record does not prove anything is wrong. Every alert says to check with the
> local land records office.

## How it works
Scheduler -> Browserbase (cloud browser, read only) -> parser -> differ -> agent decisions
-> VerbX (speaks the alert) -> Telegram (voice note and text). SQLite keeps fingerprints only.

Agent decisions:
- Rules: severity (critical, high, medium), 3 fetch attempts, and a failed-check alert instead of an
  all-clear when a page changes layout, shows a CAPTCHA or cannot be reached.
- Model (`src/decide.py`): after a change is found, a language model chooses the next action
  (`alert` or `alert_and_recheck` this evening) and gives a one-line reason, stored with the alert.
  Guardrails: critical and high changes are always alerted, the model sees only change types, ids,
  dates, statuses and extents (never owner names), it never writes the alert text, and if it is
  missing, slow or answers badly the rules decide.

## Privacy and safety
- Own land only: a parcel is never looked up until the user confirms it is theirs. No search by name.
- No title deeds or documents are uploaded. Owner names become hashes at once and raw pages are not stored.
- Read only. No logins, no form submissions beyond the public parcel fields.
- No CAPTCHA bypass. Browserbase CAPTCHA solving is switched off and the agent stops and reports instead.
- Alerts only quote values that appear in the detected change.

## Setup (Windows PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then fill in the keys
python -m pytest -q
```
Turn on GitHub Pages for this repo so `fixtures/` is public (Browserbase cannot reach localhost),
and set `FIXTURE_BASE` in `.env`.

## Run
```
python -m src.get_chat_id          # after messaging your Telegram bot once
python -m src.add_parcel           # add your own parcel (public identifiers only)
python -m src.main --once          # first run saves a snapshot
python -m src.main --once --scenario mutation   # test page with a new mutation entry
python -m src.main --schedule      # daily scheduler
python -m src.report               # writes docs/test-evidence.md
```
Set `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` in `.env` to turn on the model step (any provider with an
OpenAI-style `/chat/completions` endpoint; otherwise edit only `src/llm.py`). Leave them empty to use rules only.

Development switches in `.env`: `DEV_NO_BROWSER=1` reads fixtures from disk, `DRY_RUN=1` prints
instead of calling Telegram and VerbX. Turn both off for the demo and the submission.

## Status of each part
| Part | Status |
|---|---|
| Differ, severity, messages, safety rules | Done and tested |
| Test pages and scenario tests | Done and tested locally |
| Browserbase fetch | Written, **not yet run against a real session** |
| VerbX client | **Empty: paste the call from the VerbX docs** |
| Telegram delivery | Written, **not yet run with a real bot** |
| Model decision step | Written and tested with a fake model, **not yet run against a real model** |
| Live portal adapter | **Empty: fill in from your notes of the real pages** |
| Kannada and Hindi messages | **Need a native speaker to review the text and the audio** |

## Limitations (keep this section honest)
- The labelled test pages stand in for a record that changes, because a real record cannot be changed on demand.
- Say which real portal fields and parcels were tested, and what happens at a CAPTCHA.
- Add the organisers' answer about automated reads of the public portal here.

## Test evidence
See `docs/test-evidence.md`, and add the Browserbase replay links per scenario.
