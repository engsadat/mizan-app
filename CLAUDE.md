# Claude — Mizan operating rules

Read `STATUS.md` first. Then do **one** task. Stop.

This file is the contract. A chat memo is not a handoff and must not be used.

## 1. One Mizan only

**Canonical repo:** `github.com/engsadat/mizan-app` (`master`)
**Live:** https://southmizan.pythonanywhere.com
**Server dir:** `/home/southMizan/mizan-app`
**Laptop dir:** `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan`

If the open folder is not this repo, **stop**. Tell the user to open `mizan-app`. Do not continue in `Claude-Projects`, `hr_webapp`, or `nwc-mizan-webapp`.

### Dead copies — do not open, edit, pull, push, deploy, or “sync”

Delete these locally this session if they still exist (after confirming the canonical clone is intact):

| Location | What to do |
|---|---|
| `C:\Users\engsa\OneDrive\Desktop\AI\hr_webapp` | Delete the folder |
| `Claude-Projects/HR/hr_webapp` | Delete that folder only — keep the rest of Claude-Projects |
| Any second clone named `mizan`, `mizan-app`, `nwc-mizan-webapp` | Delete it |
| PythonAnywhere `~/Claude-Projects` | Do not `git pull`. Do not run Mizan from there |

GitHub leftovers (do **not** merge, do **not** keep developing):

- `engsadat/nwc-mizan-webapp` — old Flask copy. Archive the repo. Not live.
- `engsadat/Claude-Projects` PR #1 — already **merged** (2026-08-23). Ignore it.
- `engsadat/Claude-Projects` PR #2 (SCD Type 2 / V2 models) — **close without merging**. Mizan has no SCD.
- Branch `feature/mizan-v2-task2-sqlalchemy-models` — delete after PR #2 is closed.

Never mention Azure. `mizan.azurewebsites.net` is a different product.

Finding a second Mizan is a bug. Do not copy files between copies. Do not “reconcile.” The only code is this repo.

## 2. Status lives in git, not in a memo

**Forbidden:** “save to memo”, Claude memory, session notes, a status dump in chat treated as source of truth.

**Required, every session:**

1. **Start:** `git pull origin master`, then read `STATUS.md`.
2. **Work:** one task from `STATUS.md` → Next.
3. **End:** edit `STATUS.md` with facts checked **this** session only:
   - date
   - live URL still up? (yes/no)
   - `origin/master` SHA
   - SHA you believe is on PythonAnywhere (only if you pulled/reloaded there)
   - login test result (do **not** write passwords)
   - what changed
   - **one** next task
4. `git add STATUS.md` (and any code), `git commit`, `git push origin master`.

If you cannot push, say so. A STATUS.md that exists only on the laptop is the same failure as a memo.

Do not invent PRs, employee counts, passwords, or SHAs. If you did not check it this session, write `not checked`.

## 3. Product (this app)

Home cards: الموظفون، التقارير، الإعدادات.

- Settings = job codes + users
- Roles: `admin` | `editor` | `viewer`
- Login = `User.username` (not `emp_id`)
- Reports include BI charts, filter report, and finance (`/reports/finance`) — already on live
- No SCD, no `/admin`, no second app, no V2 rewrite

Do not start a parallel Mizan. Improve this one.

## 4. Deploy (only this path)
