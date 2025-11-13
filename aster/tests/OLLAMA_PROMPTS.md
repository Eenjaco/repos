# Ollama Prompt Optimization for mdclean_universal

## Overview

Different document types require different prompts to achieve optimal results. This guide provides specialized prompts for each content type based on the test files.

## General Principles

1. **Preserve Structure**: Don't flatten hierarchical content
2. **Maintain Accuracy**: Don't "improve" facts, names, or dates
3. **Language Awareness**: Detect and preserve multilingual content
4. **Format Consistency**: Use consistent markdown formatting
5. **Context Awareness**: Understand document type and adjust accordingly

## Content Type Prompts

### 1. Religious/Theological Content (Afrikaans)

**Test Files:**
- `11 APRIL 2025 NUUSBRIEF.pdf` (Church newsletter)
- `A S Verslag. Missionale Aard van die kerk.docx` (Missional church report)
- `Biddae en Feesdae.pdf` (Prayer days and feast days)
- `NG Kerk Alma.docx` (Church document)
- `Tuis - Kerkbode.html` (Church website)

**Optimal Prompt:**
```
Clean and structure this Afrikaans religious text for knowledge management.

CRITICAL RULES:
- Preserve ALL proper nouns exactly as written (church names, people, places)
- Keep theological terminology in original language (e.g., "Missionale", "NG Kerk")
- Maintain liturgical formatting (prayers, responses, liturgy)
- Keep date formats as-is (e.g., "11 April 2025")
- Preserve section headings and hierarchy
- Keep biblical references intact (e.g., "Matteus 5:1-12")
- Do not translate or anglicize Afrikaans terms

FORMATTING:
- Use proper heading levels (# ## ###)
- Keep bullet points and numbered lists
- Preserve paragraph structure
- Maintain any quoted material

WHAT TO FIX:
- Basic punctuation and capitalization
- Obvious OCR errors (but verify with context)
- Consistent spacing between sections
- Remove excessive blank lines

OUTPUT: Clean, structured markdown preserving all Afrikaans content and theological terminology.
```

### 2. Books and Long Documents

**Test Files:**
- `Cal Newport - Deep Work.pdf` (Productivity book)
- `First 90 Days.pdf` (Leadership book)
- `Anthony de Mello - Sadhana - A Way to God.pdf` (Spiritual book)
- `Tiyo Soga (1829–1871) at the intersection of 'universes in collision'.epub` (Biography)

**Optimal Prompt:**
```
Clean and structure this book content for knowledge management.

CRITICAL RULES:
- Detect chapter boundaries and use # Chapter Titles
- Preserve heading hierarchy (chapters → sections → subsections)
- Keep author's original structure and flow
- Maintain footnotes and references
- Preserve quotes exactly as written (including attribution)
- Keep key concepts and frameworks intact
- Don't paraphrase or summarize - preserve full content

FORMATTING:
- Chapter: # Chapter N: Title
- Section: ## Section Title
- Subsection: ### Subsection Title
- Quotes: > Quoted material
- Lists: Preserve bullet points and numbering
- Emphasis: Preserve *italics* and **bold**

WHAT TO FIX:
- Page headers/footers (remove)
- Page numbers (remove)
- Hyphenated words split across lines
- OCR errors in body text
- Excessive blank lines
- Inconsistent spacing

PRESERVE:
- All content (don't summarize)
- Chapter structure
- References and footnotes
- Author's voice and style
- Key terminology and concepts

OUTPUT: Clean, hierarchical markdown maintaining full book content and structure.
```

### 3. Newsletter and Articles

**Test Files:**
- `11 APRIL 2025 NUUSBRIEF.pdf` (Monthly newsletter)
- `02 Jun 2024.pptx` (Presentation)

**Optimal Prompt:**
```
Clean and structure this newsletter/article content for knowledge management.

CRITICAL RULES:
- Keep article titles as ## headers
- Preserve dates and attribution
- Maintain contact information
- Keep event details (date, time, location) intact
- Preserve names of people and organizations exactly
- Keep URLs and email addresses
- Maintain announcement structure

FORMATTING:
- Newsletter title: # Title - Date
- Articles: ## Article Title
- Sections: ### Section Heading
- Events: Use consistent format
- Contacts: Preserve phone/email/address

WHAT TO FIX:
- Inconsistent formatting
- OCR errors in names/dates
- Extra blank lines
- Header/footer repetition

PRESERVE:
- All dates and times
- Names and titles
- Contact information
- Event details
- URLs and links

OUTPUT: Clean markdown with clear article separation and all information intact.
```

### 4. Financial Documents (CSV/Excel)

**Test Files:**
- `Year A 2022-2023.xlsx` (Liturgical calendar - likely has dates/events)

**Optimal Prompt:**
```
Analyze this financial/calendar data and provide insights.

ANALYSIS TO PROVIDE:
- Identify patterns and trends
- Calculate key metrics (totals, averages, percentages)
- Highlight notable items or outliers
- Provide context for the numbers
- Suggest insights or observations

CRITICAL RULES:
- Verify all calculations
- Preserve exact amounts and dates
- Don't invent or extrapolate data
- State assumptions clearly
- Use conservative language for insights

FORMATTING:
- Summary statistics at top
- Clear categorization
- Use Obsidian math format: `$= formula`
- Preserve table structure
- Add explanatory notes

OUTPUT: Concise analysis with verified calculations and actionable insights.
```

### 5. Technical Documents

**Test Files:**
- (None in current test set, but adding for completeness)

**Optimal Prompt:**
```
Clean and structure this technical document for knowledge management.

CRITICAL RULES:
- Preserve code blocks exactly as-is
- Keep technical terminology unchanged
- Maintain API endpoints, commands, and syntax
- Preserve version numbers and specifications
- Keep error messages and logs intact
- Maintain configuration examples
- Don't "improve" technical accuracy

FORMATTING:
- Code blocks: ```language
- Commands: `inline code`
- File paths: Preserve exactly
- URLs/endpoints: Keep intact
- Lists: Use bullet points or numbering
- Diagrams: Describe or preserve ASCII art

WHAT TO FIX:
- Line wrapping issues
- OCR errors in body text (not code)
- Inconsistent formatting in prose sections

PRESERVE:
- All code (exact syntax)
- Commands and CLI examples
- Configuration files
- Error messages
- Technical specifications
- Version numbers

OUTPUT: Clean markdown with properly formatted code blocks and technical content preserved.
```

### 6. Musical Scores

**Test Files:**
- `VONKK 0023 OB Full Score.pdf`
- `VONKK 0203 OB.pdf`

**Special Note:**
Musical scores are primarily graphical and will extract poorly as text. Consider:

**Alternative Approach:**
```
This appears to be a musical score. Text extraction from musical notation is not reliable.

RECOMMENDATIONS:
1. Use OCR on the title page for metadata
2. Extract composer, title, opus number, instrumentation
3. Keep as image/PDF for actual score
4. Create descriptive metadata markdown:
   - Title
   - Composer
   - Instrumentation
   - Key/tempo markings visible
   - Number of movements/sections

OUTPUT: Metadata only, with note that full score requires image format.
```

### 7. Images with Text (OCR)

**Test Files:**
- `Ron Kraybill.jpeg` (Portrait/document photo)
- `The Post-Individual.jpeg` (Large image - likely infographic)

**Optimal Prompt:**
```
Clean this OCR-extracted text and structure it properly.

CRITICAL RULES:
- Fix obvious OCR errors (1→I, 0→O, etc.)
- Reconstruct broken words and sentences
- Identify and preserve structure (if visible in layout)
- Keep proper nouns even if unusual
- Preserve URLs, emails, dates
- Note if text is fragmentary or incomplete

FORMATTING:
- Reconstruct headings from size/emphasis
- Use bullet points for lists
- Separate distinct sections
- Note any illegible portions: [illegible]

WHAT TO FIX:
- OCR character errors
- Broken word splits
- Missing punctuation
- Case errors (all caps → proper case where appropriate)

CAUTION:
- OCR may be incomplete or inaccurate
- Preserve uncertain content with note: [?]
- Don't invent content to "fix" gaps
- Note image type (infographic, document, etc.)

OUTPUT: Best-effort cleaned text with notes about OCR quality and any gaps.
```

## Model-Specific Settings

### For llama3.2:1b (Recommended for Speed)

**Optimal Settings:**
```python
{
    'temperature': 0.2,  # Low for accuracy
    'top_p': 0.9,
    'repeat_penalty': 1.1,
    'num_ctx': 4096      # Context window
}
```

**Best For:**
- Quick cleanup tasks
- Basic formatting fixes
- Simple restructuring
- Financial calculations

**Limitations:**
- May struggle with very long documents
- Less nuanced language understanding
- May need verification for complex content

### For llama3.2:3b (Better Quality)

**Optimal Settings:**
```python
{
    'temperature': 0.3,
    'top_p': 0.9,
    'repeat_penalty': 1.1,
    'num_ctx': 8192
}
```

**Best For:**
- Complex documents
- Multilingual content
- Theological/technical terminology
- Nuanced formatting decisions

### For Larger Models (llama2:13b, mixtral:8x7b)

**Optimal Settings:**
```python
{
    'temperature': 0.4,
    'top_p': 0.95,
    'repeat_penalty': 1.05,
    'num_ctx': 8192
}
```

**Best For:**
- Books and long documents
- Complex multilingual content
- Highly technical material
- Maximum accuracy requirements

## Integration with mdclean_universal

To use these prompts in your code:

```python
# In mdclean_universal.py, modify the LLMCleaner class

def detect_content_type(self, text: str, file_type: str) -> str:
    """Detect specific content type for prompt selection"""
    # Afrikaans religious content
    if any(word in text.lower() for word in ['kerk', 'biddae', 'gebed', 'gemeente']):
        return 'afrikaans_religious'

    # Check for chapter markers (books)
    if 'chapter' in text.lower() or re.search(r'^chapter \d+', text, re.MULTILINE):
        return 'book'

    # Newsletter/article markers
    if 'newsletter' in text.lower() or 'bulletin' in text.lower():
        return 'newsletter'

    # Default by file type
    return file_type

def get_prompt_for_content_type(self, content_type: str) -> str:
    """Return appropriate prompt for content type"""
    prompts = {
        'afrikaans_religious': "Clean and structure this Afrikaans religious text...",
        'book': "Clean and structure this book content...",
        'newsletter': "Clean and structure this newsletter/article content...",
        # etc.
    }
    return prompts.get(content_type, self.default_prompt)
```

## Testing and Validation

After applying prompts, validate:

1. **Accuracy**: Compare key facts/names/dates with original
2. **Structure**: Verify heading hierarchy is logical
3. **Completeness**: Check no content was removed
4. **Formatting**: Ensure markdown is valid
5. **Language**: Confirm multilingual content preserved

## Continuous Improvement

As you process more documents:

1. **Document failures**: Note where prompts don't work
2. **Collect examples**: Save before/after samples
3. **Refine prompts**: Adjust based on results
4. **A/B testing**: Try prompt variations
5. **Model comparison**: Test different Ollama models

## Quick Reference

| Content Type | Key Focus | Temperature | Model |
|--------------|-----------|-------------|-------|
| Afrikaans Religious | Preserve proper nouns | 0.2 | 1b/3b |
| Books | Maintain structure | 0.3 | 3b/13b |
| Newsletter | Keep dates/contacts | 0.2 | 1b |
| Financial | Accurate calculations | 0.1 | 1b |
| Technical | Preserve code | 0.2 | 3b |
| OCR Text | Fix errors carefully | 0.3 | 3b |

## Next Steps

1. Implement content-type detection in mdclean_universal.py
2. Add prompt templates for each type
3. Run tests with specialized prompts
4. Compare results with generic prompts
5. Document improvements
