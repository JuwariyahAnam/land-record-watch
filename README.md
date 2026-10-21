# Land Record Watch

An agent that watches the **public** land record of your own parcel, spots changes (a new mutation
entry, a changed owner or extent) and tells you in **Kannada, Hindi or English**, as a Telegram text
and a voice note, what changed and what to do next. Built for the Ziro Agentic AI Hackathon 2026
(Open Innovation).

- **Live demo registry:** https://land-record-registry.onrender.com (fictional data, clearly labelled; the free host can take about a minute to wake)
- **Deployed agent:** GitHub Actions workflow `daily-land-check` (07:00 IST, 19:00 IST, and instantly after a change on the registry)

> A change in a record does not prove anything is wrong. Every alert says to check with the
> local land records office.

## How it works
```
Registry change ─┐
Schedule (cron) ─┴─> GitHub Actions ─> Browserbase cloud browser (read only) ─> parser ─> differ
   ─> decisions (rules, optional model) ─> fixed kn/hi/en templates ─> Telegram text ─> VerbX voice note
```
SQLite keeps fingerprints only (owner names are hashed on arrival).

Three parts:
1. **Demo registry** (`src/portal`, Flask + SQLite, on Render): landlord, buyer and registrar roles.
   The landlord chooses the alert language on the parcel page. The site itself is available in
   English, Kannada and Hindi. After a landlord or registrar change, it asks GitHub to run the agent
   within about 20 seconds (`src/portal/trigger.py`).
2. **Agent** (`src/main.py`, Python 3.12, on GitHub Actions): reads the registry's public watch page
   through Browserbase, diffs it with the last snapshot, and alerts. It follows the alert language
   set on the registry.
3. **Tools:** Browserbase (browser), VerbX (Kannada/Hindi/English speech), Telegram Bot API (delivery).

Agent decisions:
- Rules: severity (critical, high, medium), 3 fetch attempts, and a "check could not run" alert instead of an
  all-clear when a page changes layout, shows a CAPTCHA or cannot be reached.
- Optional model step (`src/decide.py`): chooses `alert` or `alert_and_recheck` this evening and gives a
  one-line reason. Critical and high changes are always alerted, the model never sees owner names, never
  writes the alert text, and if it is missing, slow or answers badly the rules decide.
- Messages come from fixed templates with a grounding check, so an alert only contains facts from the detected change.
- If a Telegram send fails, the snapshot is rolled back so the next run retries.

## Privacy and safety
- Own land only: a parcel is never looked up until the user confirms it is theirs. No search by name.
- No title deeds or documents are uploaded. Owner names become hashes at once; raw pages are not stored.
- Read only. No logins, no form submissions beyond the public parcel fields.
- No CAPTCHA bypass. Browserbase CAPTCHA solving is off; the agent stops and reports instead.
- The live Karnataka portal is **not** used. Only the labelled demo registry is read.

## Setup (Windows PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then fill in the keys
python -m pytest -q         # 68 tests
```

## Run
```
python -m src.portal               # start the demo registry locally
python -m src.get_chat_id          # after messaging your Telegram bot once
python -m src.add_parcel           # add a parcel (use the /public/<token> link from the registry)
python -m src.main --once          # one check
python -m src.main --once --closely  # evening check, only parcels with a pending mutation
python -m src.main --schedule      # local daily scheduler
python -m src.report               # writes docs/test-evidence.md
```
Deployment (Render, GitHub Actions secrets, instant trigger): `docs/deploy.md`.
Registry details: `docs/portal.md`. Demo script: `docs/demo-script.md`.

Optional model step: set `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` (any OpenAI-style `/chat/completions`
endpoint). Leave empty to use rules only.
Development switches: `DEV_NO_BROWSER=1` reads fixtures from disk, `DRY_RUN=1` prints instead of calling
Telegram and VerbX. Turn both off for real runs.

## Status
| Part | Status |
|---|---|
| Differ, severity, messages, safety rules | Done, tested |
| Browserbase fetch | Done, real sessions run on test pages and the deployed registry |
| VerbX voice (Kannada, Hindi, English) | Done, verified on Telegram |
| Telegram delivery (voice note and text) | Done, verified |
| Demo registry with language choice and instant trigger | Done, deployed on Render |
| Scheduled agent on GitHub Actions | Done, runs green |
| Model decision step | Written and tested; runs only if the `LLM_*` secrets are set, otherwise rules decide |
| Live Karnataka portal adapter | Not built, on purpose (see limitations) |
| Kannada and Hindi wording | First draft, native-speaker review recommended |

## Limitations
- The demo registry stands in for a record that changes, because a real record cannot be changed on demand.
- The free Render site sleeps and resets its demo data on restart; the workflow wakes it before each check.
- Status words and the parcel label stay in English inside Kannada and Hindi alerts.
- Read-only checks of the real portal are not done until organisers confirm they are acceptable.

## Test evidence
68 automated tests. Scenario report: `docs/test-evidence.md`. Real Browserbase sessions and Telegram
alerts in all three languages are shown in the presentation.
