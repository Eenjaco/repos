# Training Data & Prompt Optimization Guide

## Overview

This guide explains how to add more training documents, analyze results, and iteratively improve prompts for better output quality.

## Why More Training Data?

**Current Test Suite:** 16 diverse documents
- 7 PDFs (books, newsletters, music scores)
- 2 DOCX (Afrikaans church documents)
- 2 JPEG images
- 1 each: HTML, EPUB, XLSX, WMA, PPTX

**Adding More Documents Helps:**
1. **Test edge cases** - Unusual layouts, formats, languages
2. **Validate prompts** - Ensure prompts work across variations
3. **Identify patterns** - Find common issues to address
4. **Build confidence** - More examples = more reliability
5. **Create prompt library** - Specialized prompts for each use case

---

## How to Add Training Documents

### Step 1: Organize Your Documents

**Create category folders:**
```bash
cd /Users/mac/Documents/Applications/repos/mdclean_universal/tests/

# Create organized structure
mkdir -p training_data/{books,newsletters,religious,financial,technical,academic,personal}

# Add your documents
cp ~/Documents/your-book.pdf training_data/books/
cp ~/Documents/newsletter.pdf training_data/newsletters/
cp ~/Church/document.docx training_data/religious/
```

**Recommended Structure:**
```
tests/
├── training_data/
│   ├── books/           # Long-form books
│   │   ├── fiction/
│   │   ├── non-fiction/
│   │   └── technical/
│   ├── newsletters/     # Periodic publications
│   │   ├── church/
│   │   ├── work/
│   │   └── community/
│   ├── religious/       # Theological content
│   │   ├── afrikaans/
│   │   ├── english/
│   │   └── liturgy/
│   ├── financial/       # Money-related docs
│   │   ├── statements/
│   │   ├── budgets/
│   │   └── reports/
│   ├── technical/       # Code, APIs, manuals
│   │   ├── documentation/
│   │   ├── specs/
│   │   └── guides/
│   ├── academic/        # Papers, research
│   │   ├── papers/
│   │   ├── theses/
│   │   └── notes/
│   └── personal/        # Your notes, journals
│       ├── meetings/
│       ├── journal/
│       └── handwritten/
└── outputs/             # Processed results
```

---

### Step 2: Create Test Metadata

**For each document, create a metadata file:**

```yaml
# training_data/books/deep-work.yaml
document:
  path: "training_data/books/Cal Newport - Deep Work.pdf"
  type: book
  language: english
  size_mb: 0.7
  pages: 296

content_characteristics:
  - chapter_structure
  - references
  - index
  - technical_terminology
  - quotes

expected_challenges:
  - Chapter detection
  - Reference preservation
  - Quote attribution
  - Multi-column layout

quality_criteria:
  - All chapters detected as H1
  - References preserved
  - Quotes in blockquote format
  - Technical terms not "corrected"

optimal_prompt: book
model_recommendation: llama3.2:3b
temperature: 0.3

notes: |
  This is a productivity book with extensive references.
  Important to preserve author's voice and citations.
```

---

### Step 3: Run Batch Processing

**Process all training documents:**
```bash
cd /Users/mac/Documents/Applications/repos/mdclean_universal

# Process entire training set
python3 tests/process_training_data.py
```

**Create the processor script:**
```python
#!/usr/bin/env python3
# tests/process_training_data.py

import yaml
from pathlib import Path
import subprocess
import json
from datetime import datetime

class TrainingProcessor:
    def __init__(self, training_dir: Path, output_dir: Path):
        self.training_dir = training_dir
        self.output_dir = output_dir
        self.results = []

    def find_documents(self):
        """Find all documents with metadata files"""
        metadata_files = list(self.training_dir.rglob("*.yaml"))
        documents = []

        for meta_file in metadata_files:
            with open(meta_file) as f:
                meta = yaml.safe_load(f)
            documents.append((meta_file, meta))

        return documents

    def process_document(self, meta_file: Path, meta: dict):
        """Process single document with its metadata"""
        doc_path = self.training_dir / meta['document']['path']
        doc_name = doc_path.stem

        # Get optimal settings from metadata
        preset = meta.get('optimal_prompt', 'auto')
        model = meta.get('model_recommendation', 'llama3.2:1b')

        # Create output paths
        output_md = self.output_dir / f"{doc_name}.md"
        output_meta = self.output_dir / f"{doc_name}_result.json"

        print(f"\n{'='*80}")
        print(f"Processing: {doc_name}")
        print(f"  Preset: {preset}")
        print(f"  Model: {model}")
        print(f"{'='*80}\n")

        # Run docforge
        start_time = datetime.now()
        try:
            result = subprocess.run([
                './mdclean_universal.py',
                str(doc_path),
                '-o', str(output_md),
                '--preset', preset,
                '--model', model
            ], capture_output=True, text=True, timeout=600)

            elapsed = (datetime.now() - start_time).total_seconds()

            # Check quality criteria
            quality_score = self.assess_quality(
                output_md,
                meta.get('quality_criteria', [])
            )

            result_data = {
                'document': doc_name,
                'success': result.returncode == 0,
                'elapsed_seconds': elapsed,
                'preset': preset,
                'model': model,
                'quality_score': quality_score,
                'output_size_kb': output_md.stat().st_size / 1024 if output_md.exists() else 0,
                'metadata': meta
            }

            # Save result
            with open(output_meta, 'w') as f:
                json.dump(result_data, f, indent=2)

            self.results.append(result_data)

            print(f"✓ Complete in {elapsed:.1f}s")
            print(f"  Quality Score: {quality_score}/10")

        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout after 10 minutes")
        except Exception as e:
            print(f"❌ Error: {e}")

    def assess_quality(self, output_file: Path, criteria: list) -> float:
        """Assess output quality against criteria"""
        if not output_file.exists():
            return 0.0

        with open(output_file) as f:
            content = f.read()

        score = 10.0
        checks = len(criteria)

        if checks == 0:
            return 8.0  # Default if no criteria

        points_per_check = 10.0 / checks

        for criterion in criteria:
            if not self._check_criterion(content, criterion):
                score -= points_per_check

        return max(0, score)

    def _check_criterion(self, content: str, criterion: str) -> bool:
        """Check if criterion is met"""
        checks = {
            'All chapters detected as H1': lambda: content.count('\n# ') >= 3,
            'References preserved': lambda: 'reference' in content.lower(),
            'Quotes in blockquote format': lambda: content.count('\n> ') >= 1,
            'Has frontmatter': lambda: content.startswith('---'),
            'Has headings': lambda: '#' in content,
            'Has lists': lambda: '- ' in content or '* ' in content,
            'Has tables': lambda: '|' in content,
        }

        check_func = checks.get(criterion)
        if check_func:
            return check_func()

        return True  # Unknown criteria pass by default

    def generate_report(self):
        """Generate comprehensive training report"""
        report_path = self.output_dir / "TRAINING_REPORT.md"

        # Calculate statistics
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        avg_quality = sum(r['quality_score'] for r in self.results) / total if total > 0 else 0
        avg_time = sum(r['elapsed_seconds'] for r in self.results) / total if total > 0 else 0

        # Group by category
        by_type = {}
        for result in self.results:
            doc_type = result['metadata']['document']['type']
            if doc_type not in by_type:
                by_type[doc_type] = []
            by_type[doc_type].append(result)

        # Write report
        with open(report_path, 'w') as f:
            f.write(f"# Training Data Processing Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write(f"## Summary\n\n")
            f.write(f"- **Total Documents**: {total}\n")
            f.write(f"- **Successful**: {successful} ({successful/total*100:.1f}%)\n")
            f.write(f"- **Avg Quality Score**: {avg_quality:.1f}/10\n")
            f.write(f"- **Avg Processing Time**: {avg_time:.1f}s\n\n")

            f.write(f"## Results by Type\n\n")
            for doc_type, results in sorted(by_type.items()):
                avg_quality_type = sum(r['quality_score'] for r in results) / len(results)
                f.write(f"### {doc_type.title()}\n\n")
                f.write(f"- Documents: {len(results)}\n")
                f.write(f"- Avg Quality: {avg_quality_type:.1f}/10\n\n")

                for result in results:
                    status = "✅" if result['success'] else "❌"
                    f.write(f"- {status} **{result['document']}** ")
                    f.write(f"({result['quality_score']:.1f}/10, {result['elapsed_seconds']:.1f}s)\n")

                f.write("\n")

            f.write(f"## Prompt Effectiveness\n\n")
            # Analyze which presets/prompts work best
            by_preset = {}
            for result in self.results:
                preset = result['preset']
                if preset not in by_preset:
                    by_preset[preset] = []
                by_preset[preset].append(result['quality_score'])

            for preset, scores in sorted(by_preset.items()):
                avg = sum(scores) / len(scores)
                f.write(f"- **{preset}**: {avg:.1f}/10 avg ({len(scores)} docs)\n")

            f.write("\n")

            f.write(f"## Recommendations\n\n")

            # Find low-quality documents
            low_quality = [r for r in self.results if r['quality_score'] < 7.0]
            if low_quality:
                f.write(f"### Documents Needing Attention\n\n")
                for result in sorted(low_quality, key=lambda x: x['quality_score']):
                    f.write(f"- **{result['document']}** ")
                    f.write(f"(Score: {result['quality_score']:.1f}/10)\n")
                    f.write(f"  - Review output: `outputs/{result['document']}.md`\n")
                    f.write(f"  - Check criteria: {result['metadata'].get('quality_criteria', [])}\n")
                    f.write(f"  - Consider adjusting prompt or model\n\n")

            # Find best performers
            high_quality = [r for r in self.results if r['quality_score'] >= 9.0]
            if high_quality:
                f.write(f"### Excellent Results\n\n")
                for result in sorted(high_quality, key=lambda x: -x['quality_score']):
                    f.write(f"- **{result['document']}** ")
                    f.write(f"(Score: {result['quality_score']:.1f}/10)\n")
                    f.write(f"  - Preset: {result['preset']}\n")
                    f.write(f"  - Model: {result['model']}\n\n")

        print(f"\n📊 Report generated: {report_path}")

    def run(self):
        """Run full training pipeline"""
        documents = self.find_documents()
        print(f"\n🔍 Found {len(documents)} documents with metadata\n")

        for meta_file, meta in documents:
            self.process_document(meta_file, meta)

        self.generate_report()
        print(f"\n✅ Training complete! Check outputs/ for results.\n")


if __name__ == '__main__':
    training_dir = Path('tests/training_data')
    output_dir = Path('tests/training_outputs')
    output_dir.mkdir(exist_ok=True)

    processor = TrainingProcessor(training_dir, output_dir)
    processor.run()
```

---

### Step 4: Analyze Results

**Review the training report:**
```bash
cat tests/training_outputs/TRAINING_REPORT.md
```

**Look for patterns:**
1. **Low quality scores** - Which document types struggle?
2. **Prompt effectiveness** - Which presets work best?
3. **Processing time** - Are some types too slow?
4. **Common failures** - What consistently goes wrong?

---

### Step 5: Iterate on Prompts

**Example: Improving Afrikaans Religious Content**

**Original prompt (generic):**
```
Clean up this text by adding punctuation and capitalization.
```

**After analyzing 10 Afrikaans church documents:**
```
Clean and structure this Afrikaans religious text.

CRITICAL RULES:
- Preserve ALL proper nouns (NG Kerk, names, places)
- Keep theological terms in Afrikaans
- Maintain liturgical formatting
- Keep date formats as-is
- Preserve biblical references

WHAT TO FIX:
- Basic punctuation
- OCR errors (verify with context)
- Consistent spacing
```

**Test the improvement:**
```bash
# Before
./mdclean_universal.py "church-doc.pdf" -o before.md

# After (with new prompt)
./mdclean_universal.py "church-doc.pdf" --preset afrikaans_religious -o after.md

# Compare
diff before.md after.md
```

---

## Creating Custom Presets

### Step 1: Define Your Use Case

**Example: Academic Papers**

**Characteristics:**
- Citations and references
- Figures and tables
- Abstract and sections
- LaTeX equations (sometimes)
- Multiple authors

**Challenges:**
- Reference format preservation
- Figure captions
- Equation formatting
- Citation integrity

### Step 2: Create Preset Configuration

```python
# In presets.py or config file
PRESETS = {
    "academic": {
        "model": "llama3.2:3b",  # Need larger model
        "temperature": 0.2,       # Very conservative
        "chunk_size": 8000,
        "preserve_references": True,
        "detect_figures": True,
        "detect_tables": True,
        "latex_support": True,
        "custom_prompt": """
Clean this academic paper while preserving all scholarly elements.

CRITICAL - DO NOT MODIFY:
- Citations (any format: APA, MLA, Chicago, etc.)
- References section
- Author names and affiliations
- Figure and table captions
- Equations and formulas
- Statistical notation

STRUCTURE TO DETECT:
- Abstract (usually first section)
- Introduction, Methods, Results, Discussion
- References/Bibliography (usually last)
- Figures and Tables (often separate)

WHAT TO FIX:
- OCR errors in body text
- Paragraph breaks
- Heading hierarchy
- Remove page numbers and headers

OUTPUT FORMAT:
- Title: # {Title}
- Authors: **Authors:** {names}
- Abstract: > {abstract text}
- Sections: ## {Section Name}
- Figures: ![Figure N](...) {caption}
- References: ## References, then list

Be extremely careful with citations and references.
"""
    }
}
```

### Step 3: Test and Refine

**Test with 5-10 papers:**
```bash
./mdclean_universal.py paper1.pdf --preset academic -o output1.md
./mdclean_universal.py paper2.pdf --preset academic -o output2.md
# ... etc
```

**Check each output:**
- ✅ All citations intact?
- ✅ References preserved?
- ✅ Figures/tables detected?
- ✅ Equations handled properly?
- ✅ Author names correct?

**Adjust prompt based on failures**

---

## Prompt Engineering Best Practices

### 1. Be Specific and Explicit

**Bad:**
```
Clean this text.
```

**Good:**
```
Clean this Afrikaans church document by:
1. Fixing OCR errors (but verify with context)
2. Adding proper punctuation
3. Maintaining paragraph structure

DO NOT:
- Change proper nouns (church names, people, places)
- Translate or anglicize Afrikaans terms
- Alter theological terminology
- Modify dates or biblical references
```

### 2. Provide Examples

```
Clean this financial CSV data.

Example transformations:
- "$1234.56" → Keep as is
- "(500.00)" → Recognize as negative: -$500.00
- "12/01/2025" → Keep date format
- "Amazon" → Merchant name, don't change

Categories to detect:
- Food: groceries, restaurants, dining
- Transport: gas, uber, parking
- Housing: rent, utilities, maintenance
```

### 3. Use Positive and Negative Instructions

```
DO:
- Preserve all content (don't summarize)
- Fix obvious OCR errors
- Add proper capitalization

DO NOT:
- Remove any information
- Paraphrase or rewrite
- Add content not in original
- "Improve" technical terms
```

### 4. Consider Model Limitations

**For llama3.2:1b (fast but limited):**
- Simple, clear instructions
- One task at a time
- Short context windows

**For llama3.2:3b or larger:**
- More complex instructions
- Multiple objectives
- Nuanced understanding

### 5. Test Prompts Systematically

**A/B Testing:**
```bash
# Prompt A
./mdclean_universal.py doc.pdf --prompt-file prompts/version_a.txt -o output_a.md

# Prompt B
./mdclean_universal.py doc.pdf --prompt-file prompts/version_b.txt -o output_b.md

# Compare
diff output_a.md output_b.md
# Which is better? Use that!
```

---

## Building a Prompt Library

**Create organized prompt files:**

```
tests/prompts/
├── general/
│   ├── default.txt
│   ├── quick.txt
│   └── detailed.txt
├── languages/
│   ├── afrikaans.txt
│   ├── multilingual.txt
│   └── english_formal.txt
├── content_types/
│   ├── book.txt
│   ├── academic_paper.txt
│   ├── newsletter.txt
│   ├── financial.txt
│   ├── technical_doc.txt
│   ├── meeting_notes.txt
│   └── journal_entry.txt
├── special_cases/
│   ├── religious_afrikaans.txt
│   ├── handwritten_ocr.txt
│   ├── scanned_poor_quality.txt
│   └── multi_column_layout.txt
└── experimental/
    ├── v1_test.txt
    ├── v2_test.txt
    └── notes.md
```

**Track performance:**
```yaml
# tests/prompts/performance.yaml
prompts:
  - name: book
    file: content_types/book.txt
    tested_documents: 15
    avg_quality_score: 9.2
    best_model: llama3.2:3b
    notes: Excellent for long-form content

  - name: afrikaans_religious
    file: special_cases/religious_afrikaans.txt
    tested_documents: 8
    avg_quality_score: 8.8
    best_model: llama3.2:1b
    notes: Good preservation of proper nouns
```

---

## Quality Metrics

### Objective Metrics (Automated)

```python
def calculate_quality_metrics(original_file, output_file):
    """Automated quality checks"""
    metrics = {}

    with open(output_file) as f:
        content = f.read()

    # Basic structure
    metrics['has_frontmatter'] = content.startswith('---')
    metrics['has_headings'] = content.count('\n#') >= 1
    metrics['heading_levels'] = {
        'h1': content.count('\n# '),
        'h2': content.count('\n## '),
        'h3': content.count('\n### ')
    }

    # Content preservation
    metrics['char_count'] = len(content)
    metrics['word_count'] = len(content.split())
    metrics['line_count'] = len(content.split('\n'))

    # Markdown validity
    metrics['has_lists'] = '- ' in content or '* ' in content
    metrics['has_blockquotes'] = '> ' in content
    metrics['has_code_blocks'] = '```' in content

    # Size comparison (should not shrink dramatically)
    original_size = Path(original_file).stat().st_size
    output_size = len(content.encode())
    metrics['size_ratio'] = output_size / original_size

    return metrics
```

### Subjective Metrics (Manual Review)

**Rating Scale (1-10):**

1. **Accuracy** - Is content preserved correctly?
2. **Structure** - Are headings and hierarchy logical?
3. **Formatting** - Is markdown clean and valid?
4. **Readability** - Is output easy to read?
5. **Completeness** - Is all content captured?

**Review Checklist:**
```markdown
## Document Review: [filename]

### Content
- [ ] All major sections present
- [ ] No content missing or truncated
- [ ] Proper nouns preserved correctly
- [ ] Numbers and dates accurate

### Structure
- [ ] Heading hierarchy makes sense
- [ ] Lists formatted correctly
- [ ] Tables (if any) preserved
- [ ] Quotes properly formatted

### Formatting
- [ ] Valid markdown
- [ ] Frontmatter present and correct
- [ ] No artifacts or junk text
- [ ] Clean paragraph breaks

### Special Elements
- [ ] References/citations intact
- [ ] Code blocks preserved
- [ ] Images referenced
- [ ] Links working

**Overall Score:** ___/10

**Notes:**
[What worked well? What needs improvement?]
```

---

## Continuous Improvement Workflow

### Week 1: Baseline
1. Add 20-30 diverse documents
2. Process with default settings
3. Manually review 10 outputs
4. Calculate average quality score

### Week 2: Optimize
5. Identify common issues
6. Create specialized prompts
7. Re-process same documents
8. Compare before/after scores

### Week 3: Expand
9. Add 30 more documents
10. Test new prompts
11. Fine-tune based on results
12. Document best practices

### Ongoing:
- Add 5-10 new documents weekly
- Test edge cases
- Refine prompts monthly
- Share findings with community

---

## Example: Complete Training Cycle

**Day 1: Collect Documents**
```bash
# Add 25 church documents
cp ~/Church/*.pdf tests/training_data/religious/afrikaans/

# Create metadata files
for f in tests/training_data/religious/afrikaans/*.pdf; do
  create_metadata.py "$f"
done
```

**Day 2: Baseline Test**
```bash
# Process with default settings
./mdclean_universal.py --batch tests/training_data/religious/afrikaans/

# Manual review of 5 random outputs
# → Note: Proper nouns being changed!
# → Note: Date formats inconsistent
# → Note: Biblical references mangled
```

**Day 3: Create Specialized Prompt**
```bash
# Write tests/prompts/afrikaans_religious.txt
# Based on observed issues

# Test on same 25 documents
./mdclean_universal.py --batch \
  tests/training_data/religious/afrikaans/ \
  --preset afrikaans_religious
```

**Day 4: Compare Results**
```bash
# Generate comparison report
python3 tests/compare_outputs.py \
  tests/outputs_baseline/ \
  tests/outputs_specialized/

# Results:
# - Proper noun preservation: 65% → 95%
# - Date accuracy: 70% → 100%
# - Biblical references: 80% → 98%
# - Overall quality: 7.2/10 → 9.1/10
```

**Day 5: Deploy Improvement**
```bash
# Add to official presets
vim presets.py  # Add afrikaans_religious preset

# Update documentation
vim docs/OLLAMA_PROMPTS.md

# Commit changes
git add presets.py docs/OLLAMA_PROMPTS.md tests/prompts/
git commit -m "Add optimized Afrikaans religious prompt"
```

---

## Next Steps

1. **Start small**: Add 10-20 documents in one category
2. **Process and review**: Check quality manually
3. **Identify patterns**: What works? What doesn't?
4. **Create prompts**: Write specialized prompts
5. **Test and measure**: Compare before/after
6. **Scale up**: Add more documents and categories
7. **Share findings**: Document what you learn

The more documents you process, the better the prompts become!
