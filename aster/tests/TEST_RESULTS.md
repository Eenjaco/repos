# Test Results Report

Generated: 2025-11-13 12:18:30

## Summary

- **Total Files Tested**: 16
- **Successful**: 0 (0.0%)
- **Failed**: 16 (100.0%)
- **Success Rate**: ❌ POOR

## Results by Category

### Audio
- Files: 1
- Success: 0/1 (0%)
- Avg Time: 0.11s
- Status: ❌

### Document
- Files: 2
- Success: 0/2 (0%)
- Avg Time: 0.11s
- Status: ❌

### Ebook
- Files: 1
- Success: 0/1 (0%)
- Avg Time: 0.10s
- Status: ❌

### Image
- Files: 2
- Success: 0/2 (0%)
- Avg Time: 0.11s
- Status: ❌

### Pdf
- Files: 7
- Success: 0/7 (0%)
- Avg Time: 0.11s
- Status: ❌

### Presentation
- Files: 1
- Success: 0/1 (0%)
- Avg Time: 0.11s
- Status: ❌

### Spreadsheet
- Files: 1
- Success: 0/1 (0%)
- Avg Time: 0.10s
- Status: ❌

### Web
- Files: 1
- Success: 0/1 (0%)
- Avg Time: 0.10s
- Status: ❌

## Individual Test Results

### ❌ 01 Track 1.wma

- **Category**: audio
- **Size**: 157.3 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ A S Verslag. Missionale Aard van die kerk.docx

- **Category**: document
- **Size**: 67.5 KB
- **Time**: 0.1s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ NG Kerk Alma.docx

- **Category**: document
- **Size**: 5947.3 KB
- **Time**: 0.12s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Tiyo Soga (1829–1871) at the intersection of ‘universes in collision’.epub

- **Category**: ebook
- **Size**: 193.9 KB
- **Time**: 0.1s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Ron Kraybill.jpeg

- **Category**: image
- **Size**: 62.5 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ The Post-Individual.jpeg

- **Category**: image
- **Size**: 3749.7 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ 11 APRIL 2025 NUUSBRIEF.pdf

- **Category**: pdf
- **Size**: 321.6 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Anthony de Mello - Sadhana - A Way to God.pdf

- **Category**: pdf
- **Size**: 1473.6 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Biddae en Feesdae.pdf

- **Category**: pdf
- **Size**: 54.0 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Cal Newport - Deep Work.pdf

- **Category**: pdf
- **Size**: 726.2 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ First 90 Days.pdf

- **Category**: pdf
- **Size**: 1958.6 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ VONKK 0023 OB Full Score.pdf

- **Category**: pdf
- **Size**: 100.0 KB
- **Time**: 0.1s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ VONKK 0203 OB.pdf

- **Category**: pdf
- **Size**: 331.5 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ 02 Jun 2024.pptx

- **Category**: presentation
- **Size**: 50.8 KB
- **Time**: 0.11s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Year A 2022-2023.xlsx

- **Category**: spreadsheet
- **Size**: 16.7 KB
- **Time**: 0.1s
- **Status**: FAILED
- **Error**: Output file not created

### ❌ Tuis - Kerkbode.html

- **Category**: web
- **Size**: 488.2 KB
- **Time**: 0.1s
- **Status**: FAILED
- **Error**: Output file not created

## Recommendations

### Format Support Issues

### Ollama Prompt Optimization Needed
Based on test results, create specialized prompts for:

1. **Religious/Theological Content** (Afrikaans)
   - Preserve proper nouns (church names, people, places)
   - Maintain theological terminology
   - Respect formatting of prayers and liturgical texts

2. **Books and Long Documents**
   - Better chapter detection
   - Preserve heading hierarchy
   - Maintain references and footnotes

3. **Technical Documents**
   - Preserve code blocks
   - Maintain list formatting
   - Keep technical terminology

4. **Multilingual Content**
   - Detect language and adjust accordingly
   - Preserve language-specific characters
   - Don't over-correct proper nouns

### Performance Improvements
- Add progress indicators for large files:
  - Anthony de Mello - Sadhana - A Way to God.pdf (1473.6 KB took 0.11s)
  - Cal Newport - Deep Work.pdf (726.2 KB took 0.11s)
  - First 90 Days.pdf (1958.6 KB took 0.11s)
  - NG Kerk Alma.docx (5947.3 KB took 0.12s)
  - The Post-Individual.jpeg (3749.7 KB took 0.11s)

### Next Steps

1. Fix format support issues
2. Create specialized Ollama prompts
3. Add automated quality validation
4. Implement progress indicators for large files
5. Create pytest suite for regression testing

## Raw Data

Full test results saved to: `test_results.json`
