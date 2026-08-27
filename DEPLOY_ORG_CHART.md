# Org Chart Deployment to PythonAnywhere

## What Changed
- Replaced simple data-list org chart with **professional A3 landscape org charts**
- 4 regions × 1-4 pages each + cover page = complete organizational structure
- Pre-generated HTML files (no real-time rendering needed)

## Deployment Steps

### 1. Pull Latest Code
```bash
cd /home/southMizan/mizan-app
git pull origin master
```

### 2. Deploy Data (Excel Files + Logos)

**Option A: Copy Files (Simpler)**
```bash
# Create data folder structure
mkdir -p data/source data/Organize "data/NWC layout/img"

# Copy Excel files from laptop HR project (or use provided zip)
cp -r ~/mizan-data/source/* data/source/
cp -r ~/mizan-data/Organize/* data/Organize/
cp -r ~/mizan-data/"NWC layout"/* "data/NWC layout"/
```

**Option B: Use Symlinks (Better)**
If data is on shared drive:
```bash
# Create symlinks to shared Excel sources
ln -s /shared/HR/Organize/emp_sort.xlsx data/Organize/
ln -s /shared/HR/Organize/Office-RE.xlsx data/Organize/
ln -s /shared/HR/source/employees\ data\ source.xlsx data/source/
ln -s /shared/HR/source/project_2026_database_ver1_updated.xlsx data/source/
```

### 3. Verify Files Exist
```bash
ls -lh app/static/org_charts/09*  # Should show 4 HTML files (3.4MB total)
ls -lh data/source/
ls -lh data/Organize/
```

### 4. Reload Web App
- Go to PythonAnywhere dashboard
- Click "Web" tab
- Click "Reload" for your web app
- Wait 10 seconds

### 5. Test in Browser
```
https://southmizan.pythonanywhere.com/reports/org-chart
```

Should show:
- Region selector page (4 region cards)
- Click any region → displays professional org chart
- Can print/save as PDF (right-click → Print → Save as PDF)

## File Structure
```
mizan-app/
├── scripts/gen_org_chart.py              # Script to regenerate charts
├── data/
│   ├── source/
│   │   ├── employees data source.xlsx
│   │   └── project_2026_database_ver1_updated.xlsx
│   ├── Organize/
│   │   ├── emp_sort.xlsx
│   │   ├── Office-RE.xlsx
│   │   └── exception shorten names.txt
│   └── NWC layout/img/
│       ├── Alamro_Logo.png
│       └── NWC_Logo.png
├── app/static/org_charts/
│   ├── 09_OrgChart_Asir.html    (1.4 MB, 4 pages + cover)
│   ├── 10_OrgChart_Jizan.html   (808 KB, 2 pages + cover)
│   ├── 11_OrgChart_Baha.html    (793 KB, 2 pages + cover)
│   └── 12_OrgChart_Najran.html  (531 KB, 1 page + cover)
└── app/blueprints/reports/
    └── routes.py                # Added /reports/org-chart routes
```

## Regenerating Charts (If Data Changes)

If Excel data is updated, regenerate HTML files:

```bash
cd /home/southMizan/mizan-app
python scripts/gen_org_chart.py
```

Output: `app/static/org_charts/09-12_OrgChart_*.html` (refreshed)

No web app reload needed — files are already served.

## Troubleshooting

### "Excel files not found" error
- Check paths in `scripts/gen_org_chart.py` line 27-30
- Verify `data/source/` and `data/Organize/` folders exist
- Copy/symlink files as needed

### "Logos not found" warning
- Script falls back to SVG placeholders
- Not critical for functionality
- Place `.png` files in `data/NWC layout/img/` to fix

### Org charts show but no styling
- Check Browser Console (F12) for errors
- Verify CSS is inline in HTML (should be)
- Cairo font from Google Fonts may need CDN access

### Can't access /reports/org-chart
- Verify code was pulled: `git log --oneline | head -1` should show `482530e`
- Reload web app again
- Check app logs in PythonAnywhere dashboard

## Notes
- Pre-generated HTML means fast loading (no database queries)
- All data frozen at generation time (run script to update)
- A3 landscape print format optimized for PDF export
- Cairo font (Arabic RTL support) from Google Fonts CDN
- ~3.4 MB total for all 4 regions (reasonable)
