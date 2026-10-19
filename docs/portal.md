# Demo registry (website) quick start

A small working website with logins. It is a **demo registry with fictional data**, not an official record, and it does not imitate any government site. Land Record Watch can watch a record on it through a real cloud browser.

## Roles
| Role | Can do |
|---|---|
| Landlord | Create an account, register land (survey details, extent), file a mutation request, get a private watch link |
| Buyer | Create an account, search by district + survey number (+ more), see extent, mutation status and history. Owner name is masked |
| Registrar (demo staff) | Approve or reject mutations, correct the extent, record an ownership transfer |

## Run it on your computer
```
pip install -r requirements.txt
python -m src.portal.admin create-registrar registrar@demo.example "Demo Registrar"
python -m src.portal
```
Open http://localhost:5000. Choose landlord or buyer, create an account, and try it. Log in as the registrar at `/login?role=registrar`.

## Connect the agent to it
1. Log in as a landlord, register a land, open it, copy the **Alerts link** (looks like `http://localhost:5000/public/XXXX`).
2. In `.env` set `SOURCE=portal` and `PORTAL_BASE=http://localhost:5000` (use the public https address once it is deployed).
3. `python -m src.set_source <the alerts link>`
4. For a local test without a cloud browser set `DEV_NO_BROWSER=1`. The cloud browser cannot reach `localhost`, so for real Browserbase runs the site must be deployed.
5. `python -m src.main --once` saves the baseline. Then in the site: landlord files a mutation, registrar approves it. Run `python -m src.main --once` again and Telegram gets the alert.

## Security built in
- Passwords hashed with scrypt, never stored or shown. Minimum 10 characters with letters and numbers.
- Login lockout after 5 wrong tries (5 minutes), same message for wrong email or wrong password.
- CSRF token on every form, HttpOnly + SameSite cookies, strict Content-Security-Policy, no inline scripts.
- Roles enforced on the server. A landlord cannot open another landlord's land or approve anything.
- Buyers see the owner masked, with a short reference code that changes if the owner changes.
- The watch link is unlisted and random. Anyone with it sees the masked record, so keep it private.

## Limits (be honest in the demo)
- Fictional data only. There is no identity check, so do not use it for real land.
- The free SQLite file is lost when a free host restarts. Use a host with a persistent disk, or re-seed.
- English only for now.
