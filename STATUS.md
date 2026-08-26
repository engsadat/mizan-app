# Mizan — current status (2026-08-26)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-26)

- URL: https://southmizan.pythonanywhere.com — **up**
- Login page: Arabic ميزان / المنطقة الجنوبية, CSRF on, session cookie Secure + HttpOnly + SameSite=Lax
- `/` `/employees/` `/reports/` `/settings/` `/reports/finance` → redirect to `/auth/login` (routes exist)
- Login (admin user, password reset on PA): **succeeded** (2026-08-26)
- Inside app (home cards, 575 employees, finance numbers): **not checked** (login works, content not verified)

## Code

- Canonical: `engsadat/mizan-app` `master` @ `67504bf` (2026-08-25, finance report + Excel→DB load)
- PythonAnywhere HEAD: `a7b43c8` (checked 2026-08-26 after pull attempt, login + all routes working)
- GitHub master: `5251712` (PA has not pulled recent STATUS updates)
- Local laptop: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` tracking `origin/master` only

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Reports: BI + filter + finance. No SCD, no V2, no second codebase.

## One version — delete leftovers

See `CLAUDE.md` §1. Dead: `hr_webapp` folders, `nwc-mizan-webapp`, Claude-Projects Mizan PRs/branches. Close PR #2 without merging.

## Next (one task)

1. Check PA git status: `cd ~/mizan-app && git status && git log --oneline -3 && git remote -v`. Report output.
