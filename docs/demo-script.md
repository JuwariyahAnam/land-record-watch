# 3-minute demo script

Total: 3:00. Record the screen with a free recorder (Win + G, or OBS) and keep your face optional.
Before you start: Telegram open on the left, terminal open in the project folder, `python -m src.server` running, Browserbase Sessions page in a tab, the deck open. Delete `data\watch.db` and re-add the parcel so the first run is clean.

| Time | What you show | What you say |
|---|---|---|
| 0:00 to 0:20 | Deck slide 1 then 2 | "Land records change quietly and nobody tells the owner. Land Record Watch is a voice agent that watches the public record of your own land and tells you in Kannada when it changes. Everything you will see uses labelled fictional test pages." |
| 0:20 to 0:40 | Deck slide 4 (how one check runs) | "A cloud browser reads the page, the agent compares it with the last snapshot, decides how serious it is, and sends a reviewed message." |
| 0:40 to 1:10 | Terminal: `python -m src.main --once --scenario before` | "First run: it saves the baseline. No change, no alert." Show the `browserbase session:` line. |
| 1:10 to 1:50 | Terminal: `python -m src.main --once --scenario mutation`, then Telegram | "Now the record has a new mutation entry. The agent alerts and decides to re-check this evening because it is still pending." Show the Kannada message arriving. Read one line aloud. |
| 1:50 to 2:10 | Browserbase Sessions page, open that session's replay | "That was a real cloud browser. Here is the replay of the page it read." |
| 2:10 to 2:40 | Terminal: `python -m src.main --once --scenario captcha`, then Telegram | "Now the page shows a CAPTCHA. The agent does not try to get past it. It stops and sends: the check could not run. It never says all-clear." |
| 2:40 to 3:00 | Web UI at localhost:8000, switch EN / ಕನ್ನಡ / हिं, then deck slide 10 | "Same data in three languages. Seven live runs and 24 tests are in the evidence file. Next: VerbX voice notes and a hosted schedule. Thank you." |

## If something fails during the recording
- Browserbase slow: say "the cloud browser takes a few seconds", wait, do not cut away.
- Telegram message late: show the terminal output line, then the message when it lands.
- Run a second take. Judges see the final recording, so redo it.

## Checklist before recording
- `.env` has `DRY_RUN=0` and `DEV_NO_BROWSER=0`.
- Today's Browserbase sessions are well under the daily cap of 20.
- Close tabs showing keys or `.env`. Hide your email and bot token.
- Update slide 10 so it only lists things that really work.
