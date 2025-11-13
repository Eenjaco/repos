#!/usr/bin/env python3
"""
CSV Handler for mdclean_universal
Converts CSV to markdown tables with financial analysis
"""

import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class CSVHandler:
    """Handle CSV to Markdown conversion with financial analysis"""

    def __init__(self, csv_mode='auto'):
        """
        Initialize CSV handler.

        Args:
            csv_mode: 'auto', 'financial', 'budget', 'portfolio', 'debt', or 'generic'
        """
        self.csv_mode = csv_mode

    def read_csv(self, csv_path: Path) -> tuple[List[str], List[List[str]]]:
        """
        Read CSV file and return headers and rows.

        Returns:
            (headers, rows)
        """
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)

        return headers, rows

    def detect_csv_type(self, headers: List[str]) -> str:
        """
        Auto-detect CSV type based on column headers.

        Returns: 'financial', 'budget', 'portfolio', 'debt', or 'generic'
        """
        headers_lower = [h.lower() for h in headers]

        # Financial transactions
        if any(x in headers_lower for x in ['amount', 'transaction', 'description', 'date']):
            return 'financial'

        # Budget
        if any(x in headers_lower for x in ['budgeted', 'actual', 'variance', 'category']):
            return 'budget'

        # Portfolio/investments
        if any(x in headers_lower for x in ['shares', 'cost_basis', 'current_value', 'gain']):
            return 'portfolio'

        # Debt tracking
        if any(x in headers_lower for x in ['balance', 'interest_rate', 'payment', 'debt']):
            return 'debt'

        return 'generic'

    def parse_amount(self, value: str) -> float:
        """Parse amount string to float (handles $, commas, etc.)"""
        if not value or value.strip() == '':
            return 0.0

        # Remove currency symbols and commas
        cleaned = re.sub(r'[,$€£¥]', '', value.strip())

        # Handle parentheses as negative (accounting format)
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]

        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def format_amount(self, amount: float, is_currency=True) -> str:
        """Format amount for display"""
        if is_currency:
            if amount < 0:
                return f"-${abs(amount):,.2f}"
            else:
                return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f}"

    def analyze_financial_transactions(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze financial transaction CSV.

        Expected columns: Date, Description, Amount, Category (optional)
        """
        # Find column indices
        headers_lower = [h.lower() for h in headers]

        date_idx = next((i for i, h in enumerate(headers_lower) if 'date' in h), 0)
        desc_idx = next((i for i, h in enumerate(headers_lower) if 'desc' in h), 1)
        amount_idx = next((i for i, h in enumerate(headers_lower) if 'amount' in h), 2)
        category_idx = next((i for i, h in enumerate(headers_lower) if 'category' in h or 'cat' in h), None)

        # Analyze transactions
        total_income = 0.0
        total_expenses = 0.0
        category_totals = {}
        running_balance = 0.0
        transactions = []

        for row in rows:
            if len(row) <= amount_idx:
                continue

            amount = self.parse_amount(row[amount_idx])
            category = row[category_idx] if category_idx and len(row) > category_idx else 'Uncategorized'

            if amount > 0:
                total_income += amount
            else:
                total_expenses += abs(amount)

            # Category totals
            if category not in category_totals:
                category_totals[category] = 0.0
            category_totals[category] += amount

            # Running balance
            running_balance += amount

            # Store transaction
            transactions.append({
                'date': row[date_idx] if len(row) > date_idx else '',
                'description': row[desc_idx] if len(row) > desc_idx else '',
                'amount': amount,
                'category': category,
                'balance': running_balance
            })

        net = total_income - total_expenses

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': net,
            'category_totals': category_totals,
            'transactions': transactions,
            'transaction_count': len(rows)
        }

    def analyze_budget(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> Dict[str, Any]:
        """
        Analyze budget CSV.

        Expected columns: Category, Budgeted, Actual, Difference (optional)
        """
        headers_lower = [h.lower() for h in headers]

        cat_idx = next((i for i, h in enumerate(headers_lower) if 'category' in h), 0)
        budgeted_idx = next((i for i, h in enumerate(headers_lower) if 'budget' in h), 1)
        actual_idx = next((i for i, h in enumerate(headers_lower) if 'actual' in h), 2)

        total_budgeted = 0.0
        total_actual = 0.0
        categories = []

        for row in rows:
            if len(row) <= actual_idx:
                continue

            category = row[cat_idx] if len(row) > cat_idx else 'Unknown'
            budgeted = self.parse_amount(row[budgeted_idx])
            actual = self.parse_amount(row[actual_idx])
            difference = budgeted - actual

            total_budgeted += budgeted
            total_actual += actual

            status = '✅' if difference >= 0 else '⚠️'

            categories.append({
                'category': category,
                'budgeted': budgeted,
                'actual': actual,
                'difference': difference,
                'status': status
            })

        variance = total_budgeted - total_actual

        return {
            'total_budgeted': total_budgeted,
            'total_actual': total_actual,
            'variance': variance,
            'categories': categories
        }

    def convert_to_markdown_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        analysis: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Convert CSV data to markdown table.

        Args:
            headers: Column headers
            rows: Data rows
            analysis: Optional analysis data for special formatting

        Returns: Markdown table string
        """
        # Start table
        table = []

        # Header row
        table.append('| ' + ' | '.join(headers) + ' |')

        # Separator row
        table.append('|' + '|'.join(['---' for _ in headers]) + '|')

        # Data rows
        for row in rows:
            # Pad row if needed
            while len(row) < len(headers):
                row.append('')

            # Format cells
            formatted_row = []
            for i, cell in enumerate(row):
                formatted_row.append(cell)

            table.append('| ' + ' | '.join(formatted_row) + ' |')

        return '\n'.join(table)

    def generate_financial_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate summary section for financial transactions"""
        summary = []
        summary.append("## Summary\n")

        summary.append(f"**Total Income:** {self.format_amount(analysis['total_income'])}")
        summary.append(f"**Total Expenses:** {self.format_amount(analysis['total_expenses'])}")
        summary.append(f"**Net:** {self.format_amount(analysis['net'])}\n")

        summary.append("**Category Breakdown:**")
        for category, total in sorted(analysis['category_totals'].items(), key=lambda x: x[1], reverse=True):
            summary.append(f"- {category}: {self.format_amount(total)}")

        return '\n'.join(summary)

    def generate_budget_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate summary section for budget"""
        summary = []
        summary.append("## Budget Summary\n")

        summary.append(f"**Total Budgeted:** {self.format_amount(analysis['total_budgeted'])}")
        summary.append(f"**Total Actual:** {self.format_amount(analysis['total_actual'])}")

        variance = analysis['variance']
        variance_str = self.format_amount(variance)
        status = "✅ Under budget" if variance >= 0 else "⚠️ Over budget"

        summary.append(f"**Variance:** {variance_str} {status}\n")

        # Category status
        summary.append("**Category Status:**")
        for cat in analysis['categories']:
            summary.append(f"{cat['status']} {cat['category']}: "
                         f"{self.format_amount(cat['actual'])} / "
                         f"{self.format_amount(cat['budgeted'])}")

        return '\n'.join(summary)

    def generate_ai_analysis_prompt(
        self,
        csv_type: str,
        analysis: Dict[str, Any]
    ) -> str:
        """
        Generate prompt for Ollama to analyze financial data.

        Returns: Prompt string for LLM
        """
        if csv_type == 'financial':
            return f"""Analyze this financial data and provide insights:

Total Income: {self.format_amount(analysis['total_income'])}
Total Expenses: {self.format_amount(analysis['total_expenses'])}
Net: {self.format_amount(analysis['net'])}

Category spending:
{chr(10).join([f"- {cat}: {self.format_amount(amt)}" for cat, amt in analysis['category_totals'].items()])}

Provide:
1. Key insights about spending patterns
2. Recommendations for improvement
3. Any concerning trends
4. Savings suggestions

Keep response concise and actionable."""

        elif csv_type == 'budget':
            return f"""Analyze this budget and provide insights:

Total Budgeted: {self.format_amount(analysis['total_budgeted'])}
Total Actual: {self.format_amount(analysis['total_actual'])}
Variance: {self.format_amount(analysis['variance'])}

Categories:
{chr(10).join([f"- {cat['category']}: Budgeted {self.format_amount(cat['budgeted'])}, Actual {self.format_amount(cat['actual'])}" for cat in analysis['categories']])}

Provide:
1. Assessment of budget adherence
2. Categories needing attention
3. Recommendations for next month
4. Overall budget health

Keep response concise and actionable."""

        else:
            return "Analyze this data and provide brief insights."

    def convert_csv_to_markdown(
        self,
        csv_path: Path,
        analyze: bool = True
    ) -> tuple[str, Optional[str]]:
        """
        Main conversion function: CSV → Markdown

        Args:
            csv_path: Path to CSV file
            analyze: Whether to include AI analysis

        Returns:
            (markdown_content, ai_prompt)
        """
        # Read CSV
        headers, rows = self.read_csv(csv_path)

        # Detect or use specified CSV type
        if self.csv_mode == 'auto':
            csv_type = self.detect_csv_type(headers)
        else:
            csv_type = self.csv_mode

        # Analyze based on type
        analysis = None
        if csv_type == 'financial':
            analysis = self.analyze_financial_transactions(headers, rows)
        elif csv_type == 'budget':
            analysis = self.analyze_budget(headers, rows)

        # Build markdown content
        content = []

        # Title
        title = csv_path.stem.replace('_', ' ').replace('-', ' ').title()
        content.append(f"# {title}\n")

        # Summary (if analyzed)
        if analysis:
            if csv_type == 'financial':
                content.append(self.generate_financial_summary(analysis))
            elif csv_type == 'budget':
                content.append(self.generate_budget_summary(analysis))
            content.append("")

        # Table section
        if csv_type == 'financial' and analysis:
            content.append("## Transactions\n")
            # Enhanced table with running balance
            table_headers = headers + ['Balance']
            table_rows = []
            for trans in analysis['transactions']:
                row = [
                    trans['date'],
                    trans['description'],
                    self.format_amount(trans['amount']),
                    trans['category'],
                    self.format_amount(trans['balance'])
                ]
                table_rows.append(row)
            content.append(self.convert_to_markdown_table(table_headers, table_rows))
        else:
            content.append("## Data\n")
            content.append(self.convert_to_markdown_table(headers, rows))

        content.append("")

        # AI analysis section placeholder
        if analyze and analysis:
            content.append("## AI Analysis\n")
            content.append("*AI insights will be added by Ollama...*\n")

        # Math notes section
        if csv_type in ['financial', 'budget']:
            content.append("## Math Notes\n")
            if csv_type == 'financial' and analysis:
                content.append(f"Total income: `$= {analysis['total_income']:.2f}`")
                content.append(f"Total expenses: `$= {analysis['total_expenses']:.2f}`")
                content.append(f"Net: `$= {analysis['net']:.2f}`")
                content.append(f"Savings rate: `$= ({analysis['net']:.2f} / {analysis['total_income']:.2f}) * 100`%")

        # Generate AI prompt if requested
        ai_prompt = None
        if analyze and analysis:
            ai_prompt = self.generate_ai_analysis_prompt(csv_type, analysis)

        return '\n'.join(content), ai_prompt


def markdown_table_to_csv(markdown_path: Path, output_csv: Path):
    """
    Convert markdown table back to CSV.

    Extracts first table found in markdown and converts to CSV.
    """
    content = markdown_path.read_text(encoding='utf-8')

    # Find table
    lines = content.split('\n')
    table_lines = []
    in_table = False

    for line in lines:
        if line.strip().startswith('|'):
            in_table = True
            # Skip separator line
            if not line.strip().startswith('|---'):
                table_lines.append(line)
        elif in_table:
            break  # End of table

    if not table_lines:
        raise ValueError("No table found in markdown file")

    # Parse table
    rows = []
    for line in table_lines:
        # Remove leading/trailing |
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|'):
            line = line[:-1]

        # Split by |
        cells = [cell.strip() for cell in line.split('|')]
        rows.append(cells)

    # Write CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


# ============================================================================
# CLI for testing
# ============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python csv_handler.py input.csv [--mode financial|budget|generic]")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    # Parse mode
    mode = 'auto'
    if len(sys.argv) > 2 and sys.argv[2] == '--mode':
        mode = sys.argv[3]

    # Convert
    handler = CSVHandler(csv_mode=mode)
    markdown, ai_prompt = handler.convert_csv_to_markdown(csv_path, analyze=True)

    # Output
    output_path = csv_path.parent / f"{csv_path.stem}_converted.md"
    output_path.write_text(markdown, encoding='utf-8')

    print(f"✓ Converted: {output_path}")

    if ai_prompt:
        print(f"\n📋 AI Analysis Prompt:")
        print(ai_prompt)
