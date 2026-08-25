# Mizan — current status (2026-08-25)

Update this file at the end of a session. Next chat: `@mizan/STATUS.md` + one task.

## Live
- https://southmizan.pythonanywhere.com
- Code: `engsadat/mizan-app` @ `b02ef93` → server `/home/southMizan/mizan-app`
- DB: `/home/southMizan/mizan-app/instance/mizan.db` (~320 KB, Excel import, not the old PA file)
- Local: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` tracks `origin/master`

## Product (do not expand)
Three home cards: الموظفون، التقارير، الإعدادات. Settings = job codes + users. Roles: admin | editor | viewer. Login = `User.username`. No SCD, invoices, `/admin`, or `emp_id` login.

## Do not touch
`HR/hr_webapp` (dead V2), `Desktop\AI\hr_webapp`, Claude-Projects on PythonAnywhere (quota). Never `git pull` the HR monorepo on PA.

## Deploy
`HR/mizan` → `git push origin master` → PA Bash `cd ~/mizan-app && git pull origin master` → Web **Reload**. Do not upload laptop `mizan_dev.db` over live (wipes users). Excel full refresh: backup live db, then import script (it aborts if employees already exist).

## Excel
Day-to-day edits on the site. Master file: `HR/source/employees data source.xlsx`. Spec: `docs/superpowers/specs/2026-08-25-mizan-clean-rebuild-design.md`.
