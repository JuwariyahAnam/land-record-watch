# Deploy (free)

Two parts: the **registry website** on Render, and the **daily check** on GitHub Actions.
Everything here uses fictional data. Keep secrets in the dashboards, never in the repo.

## 1. Push the code
GitHub Desktop: commit and push. `.env` and `data/` are ignored, so no secrets go up. Check that `.env` is not in the changes list.

## 2. Website on Render
1. render.com, sign up with GitHub, New, Blueprint, pick this repo. It reads `render.yaml`.
2. When asked for `PORTAL_DEMO_TOKEN`, paste a long random value. Make one with:
   `python -c "import secrets; print(secrets.token_urlsafe(24))"`
3. After it deploys, open the Render page for the service, Environment, copy `PORTAL_SETUP_CODE`.
4. Open `https://YOUR-SERVICE.onrender.com/setup`, enter the setup code, create the registrar.
5. The agent's watch link is `https://YOUR-SERVICE.onrender.com/public/<PORTAL_DEMO_TOKEN>`.

Free Render sleeps when idle (first load takes about a minute) and forgets its files on restart.
The demo land is recreated on every start with the same link, so the agent keeps working.
Accounts and mutations you added by hand are lost on restart. Register again before a demo.

## 3. Daily check on GitHub Actions
Repo, Settings, Secrets and variables, Actions. Add these secrets:

| Name | Value |
|---|---|
| PORTAL_BASE | `https://YOUR-SERVICE.onrender.com` |
| PARCEL_SOURCE_REF | the watch link from step 2.5 |
| PARCEL_CHAT_ID | your Telegram chat id |
| TELEGRAM_BOT_TOKEN | the bot token |
| BROWSERBASE_API_KEY | from Browserbase |
| BROWSERBASE_PROJECT_ID | from Browserbase |

Optional variables: `PARCEL_LANGUAGE` (en, kn, hi), `DEV_NO_BROWSER` (set 1 to skip Browserbase).
Run it from the Actions tab: daily-land-check, Run workflow. It also runs daily at 07:00 IST (every parcel) and at 19:00 IST (only parcels with a pending mutation). A first step wakes the free Render site before the check, because it sleeps when idle. Add the secret `VERBX_API_KEY` for voice notes. The three `LLM_*` secrets are optional; without them the agent decides with its rules.

The owner picks the alert language on the registry website (land page, Alert language). The agent reads it from the watch page on each check, so no setting is needed here.
The first run saves a snapshot. Change something on the website, run again, and the alert arrives.

## 4. Check as soon as a record changes (optional)
The registry can start the daily-land-check workflow right after a change (a mutation is filed or decided, the extent or the owner is changed), so the alert arrives about a minute later instead of at the next scheduled run. The agent still opens the record in a cloud browser, compares it and decides; the registry only wakes it up.

1. GitHub, Settings, Developer settings, Fine-grained tokens, Generate new token. Repository access: only land-record-watch. Permission: Actions, Read and write. Nothing else. Choose a short expiry.
2. In Render, Environment, add `GITHUB_DISPATCH_TOKEN` (the token) and `GITHUB_REPO` (for example `JuwariyahAnam/land-record-watch`). Save; Render redeploys.
3. Change something on the registry. In the repo, Actions tab, a run named daily-land-check starts by itself within a minute (its title says "Manually run by" because the registry uses the same call as the Run workflow button).

Pings are sent 20 seconds after the last change, so a burst of edits starts one check. If the ping fails, the scheduled checks still run. A real government portal would not push changes like this, so scheduled checks remain the main method; the ping is for the demo registry.

The free Render site forgets its data when it restarts, and the demo land comes back with the default alert language (Kannada). Set `PORTAL_DEMO_LANGUAGE` in Render to `kn`, `hi` or `en` so the demo land always comes back in the language you want. An uptime pinger (for example UptimeRobot on `/healthz` every 5 minutes) also stops the site from sleeping and restarting.
