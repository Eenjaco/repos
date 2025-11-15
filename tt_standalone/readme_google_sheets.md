# Google Sheets Import Guide

Your time tracking data has been exported and is ready to import into Google Sheets!

## 📊 Exported Files

1. **time-tracking-export.csv** - All 288 detailed time entries
2. **summary-by-category.csv** - Breakdown by category (Sermon, Operations, etc.)
3. **summary-by-month.csv** - Monthly summaries
4. **summary-by-week.csv** - Weekly summaries (18 weeks)

## 🚀 Two Import Methods

### Method 1: Manual Import (Recommended - Easiest!)

**This is the simplest method and works immediately:**

1. **Open Google Sheets** in your browser
   - Go to: https://sheets.google.com
   - Click "Blank" to create a new spreadsheet

2. **Import the first file:**
   - Go to **File > Import > Upload**
   - Click "Browse" and select `time-tracking-export.csv`
   - Choose "Replace spreadsheet" for the first file
   - Click "Import data"

3. **Add the other sheets:**
   - Go to **File > Import > Upload** again
   - Select `summary-by-category.csv`
   - Choose **"Insert new sheet(s)"**
   - Click "Import data"
   - Repeat for `summary-by-month.csv` and `summary-by-week.csv`

4. **Rename the sheets:**
   - Right-click each sheet tab at the bottom
   - Rename them to: "All Data", "By Category", "By Month", "By Week"

**Done!** You now have all your data in Google Sheets.

---

### Method 2: Automated Script (Advanced)

**This requires one-time Google Cloud setup but then automates everything:**

#### Prerequisites:
1. Go to https://console.cloud.google.com
2. Create a new project (or select existing)
3. Enable the **Google Sheets API**
4. Create **OAuth 2.0 credentials** (Desktop app type)
5. Download credentials as `credentials.json`
6. Save to: `/Users/mac/Documents/Terminal/Claude/Time Keeping/credentials.json`

#### Run the script:
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node auto-create-sheet.js
```

The script will:
- Ask you to authorize (opens browser)
- Automatically create a new Google Sheet
- Upload all 4 tabs with formatted headers
- Open the sheet in your browser

---

## 📈 Your Data Summary

- **Total Time Tracked:** 918h 22m (over 4 months)
- **Period:** June 30 - October 27, 2025
- **Total Entries:** 288 time entries
- **Categories:** 7 categories
  - Sermon: 500h 37m (54.5%)
  - Operations: 146h 30m (16.0%)
  - Pastoral & Community: 119h 4m (13.0%)
  - Admin: 60h 58m (6.6%)
  - Sinod: 54h 37m (5.9%)
  - Communication: 33h 57m (3.7%)
  - Prayer: 2h 39m (0.3%)

## 💡 Tips for Using Your Google Sheet

1. **Freeze the header row** - View > Freeze > 1 row
2. **Create charts** - Insert > Chart
3. **Use filters** - Data > Create a filter
4. **Share with others** - Share button (top right)
5. **Download as Excel** - File > Download > Microsoft Excel

## 🔄 Re-export Data

If you add more time tracking data, just run:
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node export-to-csv.js
node create-summaries.js
```

Then import the new CSV files into Google Sheets.

---

## 📞 Need Help?

- **Manual import issues?** Make sure you're selecting "Insert new sheet(s)" for files 2-4
- **Automated script issues?** Try the manual method - it's simpler!
- **Data looks wrong?** Check that you imported all 4 files

Enjoy analyzing your time tracking data! 📊
