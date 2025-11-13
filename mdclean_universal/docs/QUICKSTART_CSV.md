# CSV Financial Management - Quick Start

**Get started with local, private financial tracking in 5 minutes!**

---

## 1. Install Dependencies

```bash
cd ~/repos

# Python package for CSV handling
pip install pandas

# Already installed from previous setup:
# - ollama (with llama3.2:1b model)
# - unstructured
# - pytesseract
```

---

## 2. Test with Sample Data

```bash
# Convert the sample CSV to markdown
python3 csv_handler.py sample_transactions.csv --mode financial

# Check the output
cat sample_transactions_converted.md
```

**You should see:**
- Summary with income/expenses/net
- Category breakdown
- Full transaction table with running balance
- Math notes with Obsidian formulas
- Placeholder for AI analysis

---

## 3. Get AI Insights with Ollama

The CSV handler generates a prompt for Ollama. Use it like this:

```bash
# Start ollama if not running
ollama serve &

# Get AI analysis
ollama run llama3.2:1b "Analyze this financial data and provide insights:

Total Income: $4,000.00
Total Expenses: $1,863.28
Net: $2,136.72

Category spending:
- Income: $4,000.00
- Housing: -$1,200.00
- Food: -$414.05
- Utilities: -$204.23
- Transport: -$45.00

Provide:
1. Key insights about spending patterns
2. Recommendations for improvement
3. Any concerning trends
4. Savings suggestions

Keep response concise and actionable."
```

**Example AI response:**
```
Key Insights:
1. Excellent savings rate at 53.4% - well above recommended 20%
2. Housing at 30% of income is ideal
3. Food spending is very low at 10.4% - good cost control

Recommendations:
1. Maintain current spending discipline
2. Consider increasing emergency fund allocation
3. Food budget has room - ensure adequate nutrition

Trends:
No concerning patterns - spending is well-balanced

Savings:
- Emergency fund: Allocate $500/month
- Long-term savings: Invest remaining $1,600+
```

---

## 4. Your First Real Budget

**Export from your bank:**
1. Log into online banking
2. Download transactions as CSV
3. Save to `~/Downloads/bank_statement_nov.csv`

**Convert to markdown:**
```bash
python3 csv_handler.py ~/Downloads/bank_statement_nov.csv --mode financial
```

**Move to Obsidian:**
```bash
# Copy to your vault
cp bank_statement_nov_converted.md ~/Documents/Vault/Finances/2025/November/
```

**Edit in Obsidian:**
- Add the AI analysis section
- Add your own notes
- Link to goals: `[[Emergency Fund Goal]]`
- Add math calculations

---

## 5. Create a Budget Plan

**Create budget CSV:** `budget_2025_12.csv`
```csv
Category,Budgeted,Actual
Housing,1200,0
Food,400,0
Transport,300,0
Utilities,150,0
Entertainment,200,0
Savings,750,0
```

**Convert:**
```bash
python3 csv_handler.py budget_2025_12.csv --mode budget
```

**Track through the month:**
- Update Actual column as expenses occur
- Re-convert to see variance
- Get AI budget analysis

---

## 6. Advanced: Portfolio Tracking

**Create portfolio CSV:** `portfolio_2025_11.csv`
```csv
Asset,Shares,Cost_Basis,Current_Value,Gain_Loss,Percent
VTSAX,100,10000,11500,1500,15%
VBTLX,50,5000,4900,-100,-2%
Cash,1,15000,15000,0,0%
Total,,,31400,1400,4.7%
```

**Convert:**
```bash
python3 csv_handler.py portfolio_2025_11.csv --mode portfolio
```

---

## 7. Export Back to CSV

**When you need to share with accountant or import to sheets:**

```bash
# Convert markdown table back to CSV
python3 csv_handler.py transactions_nov_2025_converted.md --export-csv
```

This extracts the table from markdown and saves as CSV.

---

## 8. Obsidian Integration

**Recommended plugins:**
```
1. Dataview - Query financial data
2. Charts - Visualize spending trends
3. Templater - Budget templates
4. Calendar - Date-based tracking
```

**Folder structure:**
```
Vault/
└── Finances/
    ├── 2025/
    │   ├── November/
    │   │   └── transactions_2025_11.md
    │   └── December/
    ├── Budgets/
    │   └── budget_2025_12.md
    ├── Goals/
    │   └── emergency_fund.md
    └── Portfolio/
        └── portfolio_2025_11.md
```

---

## 9. Privacy Best Practices

**✅ DO:**
- Keep financial data in encrypted vault
- Use local Ollama for AI analysis
- Delete original CSVs after conversion
- Backup vault to encrypted drive

**❌ DON'T:**
- Upload financial CSVs to cloud services
- Use online AI (ChatGPT, etc.) with financial data
- Store in unencrypted folders
- Share financial markdown files unencrypted

---

## 10. Next Integration: mdclean_universal

**Coming soon:** CSV support integrated into main tool

```bash
# Will work like this:
./mdclean_universal.py transactions.csv --csv-mode financial --analyze
```

**For now, use standalone:**
```bash
python3 csv_handler.py your_file.csv --mode financial
```

---

## Quick Reference

**Convert financial transactions:**
```bash
python3 csv_handler.py transactions.csv --mode financial
```

**Convert budget:**
```bash
python3 csv_handler.py budget.csv --mode budget
```

**Auto-detect type:**
```bash
python3 csv_handler.py file.csv --mode auto
```

**Get AI analysis:**
```bash
# The tool prints the prompt - copy and paste to Ollama
ollama run llama3.2:1b "[paste prompt here]"
```

**Export to CSV:**
```bash
python3 -c "from csv_handler import markdown_table_to_csv; \
  from pathlib import Path; \
  markdown_table_to_csv(Path('input.md'), Path('output.csv'))"
```

---

## Example Workflow: Monthly Review

**Week 1:** Export bank CSV
```bash
python3 csv_handler.py bank_nov.csv --mode financial
mv bank_nov_converted.md ~/Vault/Finances/2025/November/
```

**Week 2:** Review in Obsidian
- Add AI analysis from Ollama
- Add notes and commentary
- Link to goals

**Week 3:** Compare to budget
- Update budget CSV with actual numbers
- Convert and review variance
- Adjust next month's plan

**Week 4:** Archive
- Export final version as PDF
- Update net worth tracker
- Plan for next month

---

## Troubleshooting

**"Module 'pandas' not found"**
```bash
pip install pandas
```

**"No table found in markdown file"** (when exporting)
- Make sure file contains a markdown table
- Table must start with `|` characters

**CSV not parsing correctly**
- Check for proper headers
- Ensure amounts are numeric (remove $, commas)
- Use --mode to specify type explicitly

---

## Full Documentation

See **CSV_FINANCIAL_WORKFLOW.md** for:
- Complete use cases
- Advanced features
- Portfolio tracking
- Debt payoff planning
- Net worth calculations
- Obsidian queries
- Security best practices

---

**Status:** ✅ Ready to use!
**Privacy:** 🔒 100% local
**AI:** 🤖 Ollama 3.2 1B

Start with `sample_transactions.csv` to see it in action!
