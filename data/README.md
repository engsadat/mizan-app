# Finance Data Sources

This folder contains Excel files for the Finance Report.

## Required Files

1. **po_master.xlsx** — PO 1-5 data
   - Sheet: `Sheet1`
   - Source: `C:\Users\engsa\OneDrive\Desktop\Dell_5066\04_Dell_Inv\2025\PO 1_2_3_4\tot PO.xlsx`

2. **invoices.xlsx** — All invoices (original + variation)
   - Sheet: `إجمالي المستخلصات_`
   - Source: `C:\Users\engsa\OneDrive\Desktop\AI\HR\Invoices\Inv_Data_total for ai pro2.xlsx`

3. **po6_detail.xlsx** — PO 6 job details
   - Sheet: `ToTal_From PO_6_underway`
   - Source: `C:\Users\engsa\OneDrive\Desktop\AI\HR\Invoices\2026_PO6for ai_.xlsx`

4. **variations.xlsx** — Variation budgets per job
   - Sheet: `1`
   - Source: `C:\Users\engsa\OneDrive\Desktop\AI\HR\Invoices\PO_2026.xlsx`

## Setup

### Local Development
Copy the Excel files from sources to this folder:
```bash
cp "/c/Users/engsa/OneDrive/Desktop/Dell_5066/04_Dell_Inv/2025/PO 1_2_3_4/tot PO.xlsx" po_master.xlsx
cp "/c/Users/engsa/OneDrive/Desktop/AI/HR/Invoices/Inv_Data_total for ai pro2.xlsx" invoices.xlsx
cp "/c/Users/engsa/OneDrive/Desktop/AI/HR/Invoices/2026_PO6for ai_.xlsx" po6_detail.xlsx
cp "/c/Users/engsa/OneDrive/Desktop/AI/HR/Invoices/PO_2026.xlsx" variations.xlsx
```

### Production (PythonAnywhere)
Set environment variables to point to source files:
```bash
export EXCEL_PO_MASTER="/home/southMizan/sources/po_master.xlsx"
export EXCEL_INVOICES="/home/southMizan/sources/invoices.xlsx"
export EXCEL_PO6="/home/southMizan/sources/po6_detail.xlsx"
export EXCEL_VARIATIONS="/home/southMizan/sources/variations.xlsx"
```

Or copy files to this folder and commit them (use git-lfs for large files).

## Update Workflow

1. Update source Excel files
2. Run: `python scripts/load_finance_data.py` (loads Excel → database)
3. All reports automatically use updated data from database

This approach ensures:
- ✅ Cross-environment compatibility
- ✅ Version control friendly
- ✅ Easy data updates
- ✅ Fast report queries (database, not file I/O)
