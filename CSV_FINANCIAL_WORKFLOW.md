# CSV Financial Management Workflow

**Use Case:** Local, private financial planning and analysis using Obsidian + Ollama
**Privacy:** All data stays local - never uploaded to cloud services
**AI Analysis:** Ollama 3.2 1B for calculations and insights

---

## Why This Workflow?

**Privacy First:**
- ✅ All financial data stays on your machine
- ✅ No cloud uploads (unlike Google Sheets, Excel Online)
- ✅ Local AI analysis with Ollama (no API calls)
- ✅ Encrypted vault with Obsidian

**Knowledge Management:**
- ✅ Link budgets to notes and goals
- ✅ Add context and commentary
- ✅ Track over time in your vault
- ✅ Search across all financial records

**AI-Powered:**
- ✅ Automatic calculations with Ollama
- ✅ Budget analysis and insights
- ✅ Trend detection
- ✅ Natural language queries

---

## Workflow Overview

```
CSV (bank export, budget template)
  ↓
mdclean_universal --csv-mode financial
  ↓
Markdown with:
  - Formatted tables
  - Obsidian math notation
  - AI-generated summaries
  - Category totals
  ↓
Edit in Obsidian:
  - Add notes
  - Link to goals
  - Query with Ollama
  ↓
Export:
  - PDF (print from Obsidian)
  - CSV (back to sheets if needed)
```

---

## Step-by-Step Guide

### Step 1: Export CSV from Bank/Sheets

**From Bank:**
- Download transaction history as CSV
- Typical columns: Date, Description, Amount, Category

**From Google Sheets:**
- File → Download → CSV
- Or create budget template in sheets first

**Example CSV structure:**
```csv
Date,Description,Amount,Category
2025-11-01,Grocery Store,-125.50,Food
2025-11-02,Salary Deposit,3500.00,Income
2025-11-03,Electric Bill,-89.23,Utilities
2025-11-05,Coffee Shop,-4.50,Food
2025-11-08,Rent,-1200.00,Housing
```

### Step 2: Convert to Obsidian Markdown

```bash
./mdclean_universal.py transactions_nov_2025.csv \
  --csv-mode financial \
  --analyze \
  --output ~/Vault/Finances/
```

**Output:** `transactions_nov_2025.md`

```markdown
---
source: transactions_nov_2025.csv
date_processed: 2025-11-13T15:00:00
type: financial_csv
period: November 2025
tags: [finance, budget, transactions, 2025-11]
---

# Transactions - November 2025

## Summary

**Total Income:** $3,500.00
**Total Expenses:** $1,419.23
**Net:** $2,080.77

**Category Breakdown:**
- Income: $3,500.00
- Housing: -$1,200.00
- Food: -$130.00
- Utilities: -$89.23

## Transactions

| Date | Description | Amount | Category | Balance |
|------|-------------|--------|----------|---------|
| 2025-11-01 | Grocery Store | -$125.50 | Food | $3,374.50 |
| 2025-11-02 | Salary Deposit | $3,500.00 | Income | $6,874.50 |
| 2025-11-03 | Electric Bill | -$89.23 | Utilities | $6,785.27 |
| 2025-11-05 | Coffee Shop | -$4.50 | Food | $6,780.77 |
| 2025-11-08 | Rent | -$1,200.00 | Housing | $5,580.77 |

## AI Analysis

Based on your November spending patterns:

**Insights:**
- Housing represents 34% of income (within recommended 30-35% range)
- Food spending is low at 3.7% - mostly home cooking
- Utilities are reasonable for this season

**Recommendations:**
- Consider setting aside $500/month for emergency fund
- Food budget has room - average is 10-15% of income
- On track to save $2,080 this month

**Trends:**
- Net positive month: +$2,080.77
- Spending below income by 40%
- Savings rate: 59% (excellent!)

## Math Notes

Starting balance: $0
Ending balance: `$= 3500 - 1419.23`
Savings rate: `$= (2080.77 / 3500) * 100`%

Housing ratio: `$= (1200 / 3500) * 100`% = 34.3%
Food ratio: `$= (130 / 3500) * 100`% = 3.7%

## Links

- [[Emergency Fund Goal]]
- [[2025 Budget Plan]]
- [[Savings Goals]]
```

### Step 3: Edit and Enhance in Obsidian

**Add context:**
```markdown
## Notes

This was a good month. I cooked at home more, which explains
the low food costs. The salary deposit included a bonus.

### Action Items
- [ ] Set up automatic transfer to savings account
- [ ] Review insurance premiums next month
- [ ] Plan for holiday expenses in December
```

**Link to other notes:**
```markdown
Working toward [[House Down Payment Goal]]. At this savings
rate, will reach target in `$= 50000 / 2080.77`$ months.
```

### Step 4: Query with Ollama in Obsidian

**Using Obsidian plugins or terminal:**

```bash
# Ask questions about your finances
ollama run llama3.2:1b "Based on this budget data: [paste table],
  what's my biggest expense category percentage-wise?"

# Get advice
ollama run llama3.2:1b "I'm saving $2080/month. I need $50,000
  for a house down payment. When can I afford it?"

# Compare months
ollama run llama3.2:1b "Compare these two months: [paste data].
  What changed and should I be concerned?"
```

### Step 5: Export Options

**A) Export as PDF (Obsidian):**
```
- Open note in Obsidian
- Cmd/Ctrl + P → "Export to PDF"
- Save for records
```

**B) Export back to CSV:**
```bash
# Convert markdown table back to CSV for sheets
./mdclean_universal.py transactions_nov_2025.md \
  --export-csv \
  --output transactions_nov_2025_updated.csv
```

**C) Keep in vault:**
- Link from daily notes
- Reference in planning sessions
- Track over time

---

## Use Case Examples

### Example 1: Monthly Budget Tracking

**Input:** Bank export CSV

**Process:**
```bash
# Convert with analysis
./mdclean_universal.py bank_statement_nov.csv \
  --csv-mode financial \
  --analyze \
  --output ~/Vault/Finances/2025/November/
```

**Result:** Markdown with:
- Formatted transaction table
- Category summaries
- AI insights
- Math formulas for calculations
- Links to budget goals

**In Obsidian:**
- Add commentary
- Link to [[Monthly Review Nov 2025]]
- Compare with [[Budget Plan 2025]]
- Track progress toward [[Financial Goals]]

### Example 2: Budget Planning

**Input:** Budget template CSV

```csv
Category,Budgeted,Actual,Difference
Housing,1200,1200,0
Food,400,130,270
Transport,300,0,300
Utilities,150,89.23,60.77
Entertainment,200,0,200
Savings,500,2080.77,1580.77
Total,2750,3500,750
```

**Process:**
```bash
./mdclean_universal.py budget_nov_2025.csv \
  --csv-mode budget \
  --analyze \
  --output ~/Vault/Finances/Budgets/
```

**Result:** Markdown with:
- Budget vs actual comparison
- Variance analysis
- AI recommendations
- Visual indicators (✅ under budget, ⚠️ over budget)

### Example 3: Investment Tracking

**Input:** Portfolio CSV

```csv
Asset,Shares,Cost_Basis,Current_Value,Gain_Loss,Percent
VTSAX,100,10000,11500,1500,15%
VBTLX,50,5000,4900,-100,-2%
Cash,1,15000,15000,0,0%
```

**Process:**
```bash
./mdclean_universal.py portfolio_2025_11.csv \
  --csv-mode portfolio \
  --analyze \
  --output ~/Vault/Finances/Investments/
```

**Result:** Markdown with:
- Portfolio allocation table
- Gain/loss calculations
- AI analysis of diversification
- Rebalancing suggestions

### Example 4: Debt Payoff Tracking

**Input:** Debt tracker CSV

```csv
Debt,Balance,Interest_Rate,Min_Payment,Extra_Payment,Payoff_Date
Credit_Card_A,3500,18.99%,100,200,2026-05
Student_Loan,25000,4.5%,250,50,2032-08
Car_Loan,12000,5.2%,350,0,2028-03
```

**Process:**
```bash
./mdclean_universal.py debt_tracker.csv \
  --csv-mode debt \
  --analyze \
  --output ~/Vault/Finances/Debt/
```

**Result:** Markdown with:
- Debt snowball/avalanche analysis
- Interest cost calculations
- Payoff timeline
- AI optimization suggestions

---

## Advanced Features

### 1. Recurring Transactions

**Add to markdown:**
```markdown
## Recurring Expenses

| Item | Amount | Frequency | Annual Cost |
|------|--------|-----------|-------------|
| Rent | $1,200 | Monthly | `$= 1200 * 12` |
| Phone | $50 | Monthly | `$= 50 * 12` |
| Netflix | $15 | Monthly | `$= 15 * 12` |
| **Total** | | | **`$= (1200 + 50 + 15) * 12`** |
```

### 2. Goal Tracking

**Link to goals:**
```markdown
## Progress Toward Goals

### Emergency Fund
Target: $10,000
Current: $5,000
Monthly savings: $500
Months to goal: `$= (10000 - 5000) / 500` = 10 months

### House Down Payment
Target: [[House Savings Goal]] $50,000
Current: $15,000
Monthly savings: $2,080
Months to goal: `$= (50000 - 15000) / 2080` ≈ 17 months
```

### 3. Tax Planning

**Track deductions:**
```markdown
## Tax Deductible Expenses 2025

| Date | Description | Amount | Category |
|------|-------------|--------|----------|
| 2025-11-15 | Charity donation | $500 | Charitable |
| 2025-11-20 | Medical expense | $200 | Medical |
| 2025-11-25 | Home office supply | $150 | Business |

Total deductions: `$= 500 + 200 + 150` = $850

Link to: [[Tax Planning 2025]]
```

### 4. Net Worth Tracking

**Monthly snapshots:**
```markdown
## Net Worth - November 2025

### Assets
- Checking: $5,000
- Savings: $15,000
- Investment account: $31,400
- 401k: $45,000
**Total Assets:** `$= 5000 + 15000 + 31400 + 45000` = **$96,400**

### Liabilities
- Credit card: -$3,500
- Student loan: -$25,000
- Car loan: -$12,000
**Total Liabilities:** `$= 3500 + 25000 + 12000` = **-$40,500**

### Net Worth
`$= 96400 - 40500` = **$55,900**

Previous month: $54,200
Change: `$= 55900 - 54200` = +$1,700 ✅

Chart: [[Net Worth Tracker]]
```

---

## AI-Powered Analysis Queries

### Ask Ollama About Your Finances

**Budget optimization:**
```bash
ollama run llama3.2:1b "I spend $1,200/month on rent,
  $400 on food, $300 on transport. My income is $3,500.
  What percentage should I save? Am I on track?"
```

**Debt strategy:**
```bash
ollama run llama3.2:1b "I have 3 debts:
  Credit card: $3,500 at 18.99%
  Student loan: $25,000 at 4.5%
  Car: $12,000 at 5.2%
  I can pay extra $200/month. Which to focus on first?"
```

**Goal planning:**
```bash
ollama run llama3.2:1b "I want to save $50,000 for a house.
  I currently have $15,000 and can save $2,000/month.
  When will I reach my goal? Should I invest the savings?"
```

**Spending patterns:**
```bash
ollama run llama3.2:1b "Analyze my last 3 months of spending:
  [paste monthly totals by category]
  What trends do you see? Any concerns?"
```

---

## Privacy & Security Best Practices

### 1. Keep Data Local
```bash
# ✅ Good: Local vault
~/Vault/Finances/

# ❌ Avoid: Cloud synced folders (unless encrypted)
~/Dropbox/Finances/
~/Google Drive/Finances/
```

### 2. Encrypt Your Vault
```bash
# Use Obsidian community plugins:
- Folder Note Encryption
- Self-hosted Obsidian Sync

# Or system-level encryption:
- FileVault (macOS)
- BitLocker (Windows)
- LUKS (Linux)
```

### 3. Secure Your CSVs
```bash
# Delete original CSVs after conversion
rm bank_statement.csv

# Or move to encrypted archive
mv *.csv ~/Vault/.archive/raw_csvs/
```

### 4. Use Ollama Locally
```bash
# ✅ Local inference (no internet)
ollama run llama3.2:1b

# ❌ Avoid sending financial data to APIs
# Don't use: ChatGPT, Claude API, etc. for sensitive data
```

---

## Sample Folder Structure

```
Vault/
├── Finances/
│   ├── 2025/
│   │   ├── November/
│   │   │   ├── transactions_2025_11.md
│   │   │   ├── budget_review_2025_11.md
│   │   │   └── monthly_summary_2025_11.md
│   │   ├── December/
│   │   └── Annual_Review_2025.md
│   ├── Budgets/
│   │   ├── Budget_Plan_2025.md
│   │   └── Budget_Template.md
│   ├── Goals/
│   │   ├── Emergency_Fund_Goal.md
│   │   ├── House_Down_Payment_Goal.md
│   │   └── Retirement_Planning.md
│   ├── Investments/
│   │   ├── Portfolio_Tracker.md
│   │   └── Investment_Strategy.md
│   ├── Debt/
│   │   └── Debt_Payoff_Plan.md
│   └── Net_Worth/
│       └── Net_Worth_Tracker.md
```

---

## Markdown → CSV Export

**When you need to go back to sheets:**

```bash
# Extract table from markdown and convert to CSV
./mdclean_universal.py transactions_2025_11.md \
  --export-csv \
  --output transactions_updated.csv
```

**Result:** Clean CSV that can be:
- Imported to Google Sheets
- Opened in Excel
- Shared with accountant
- Archived for taxes

---

## Obsidian Plugins to Enhance Workflow

**Essential:**
- **Dataview** - Query your financial data
- **Templater** - Budget templates
- **Calendar** - Date-based tracking
- **Charts** - Visualize spending trends

**Recommended:**
- **Advanced Tables** - Easy table editing
- **Natural Language Dates** - Quick date entry
- **Folder Note** - Organize finances by month
- **QuickAdd** - Fast transaction logging

**Math/Calculations:**
- **Obsidian Math** - LaTeX math support
- **Calculations** - Inline calculations
- **Spreadsheet** - Embedded mini-sheets

---

## Example Queries with Dataview

**Monthly spending summary:**
```dataview
TABLE sum(amount) as Total
FROM "Finances/2025"
WHERE type = "transaction"
GROUP BY month
```

**Category breakdown:**
```dataview
TABLE sum(amount) as Total, count(rows) as Count
FROM "Finances/2025/November"
WHERE type = "transaction"
GROUP BY category
SORT Total DESC
```

**Track goal progress:**
```dataview
TABLE target, current, (current/target)*100 as "Progress %"
FROM "Finances/Goals"
WHERE status = "active"
```

---

## Complete Example Workflow

### Week 1: Setup
1. Export bank transactions → CSV
2. Convert to markdown: `./mdclean_universal.py bank.csv --csv-mode financial`
3. Review in Obsidian
4. Add notes and links

### Week 2: Analysis
1. Ask Ollama for spending insights
2. Compare to budget plan
3. Update goals if needed

### Week 3: Planning
1. Create next month's budget
2. Set spending targets
3. Link to financial goals

### Week 4: Review
1. Create monthly summary note
2. Track net worth change
3. Export PDF for records
4. Archive raw CSVs

---

## Benefits Summary

**Privacy:**
- ✅ All data stays local
- ✅ No cloud uploads
- ✅ Encrypted vault
- ✅ Local AI analysis

**Flexibility:**
- ✅ CSV in, markdown out
- ✅ Markdown back to CSV
- ✅ PDF export
- ✅ Full control over data

**AI-Enhanced:**
- ✅ Automatic calculations
- ✅ Spending insights
- ✅ Budget recommendations
- ✅ Natural language queries

**Knowledge Management:**
- ✅ Link to goals and notes
- ✅ Track over time
- ✅ Full-text search
- ✅ Context and commentary

---

## Next Steps

1. **Install dependencies:**
   ```bash
   pip install pandas  # CSV handling
   ```

2. **Update mdclean_universal.py with CSV handler**
   (Implementation in next commit)

3. **Test with your financial data:**
   ```bash
   ./mdclean_universal.py sample_budget.csv --csv-mode financial
   ```

4. **Set up Obsidian vault structure**
   Create folders for finances

5. **Start tracking!**
   Export monthly, convert, analyze

---

**Status:** 📋 Workflow documented, implementation next
**Privacy Level:** 🔒 Completely local and private
**AI:** 🤖 Ollama 3.2 1B (local, fast, secure)

#finance #privacy #ollama #obsidian #csv #budgeting
