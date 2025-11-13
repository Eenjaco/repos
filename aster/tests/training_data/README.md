# Training Data Organization

Drop your training documents into these folders based on category:

## 📚 `/books/`
- PDF books, EPUB files
- Long-form content
- Example: Philosophy, self-help, technical books

## 📰 `/newsletters/`
- Newsletter PDFs
- Church bulletins
- Community announcements
- Example: Monthly newsletters, announcements

## ⛪ `/religious/`
- Church documents (especially Afrikaans)
- Theological content
- Liturgical texts, prayers
- Example: Synod reports, sermons, devotionals

## 💰 `/financial/`
- CSV files with transactions
- Budget spreadsheets
- Receipts
- Bank statements
- Example: Monthly budgets, expense tracking

## 🔧 `/technical/`
- Technical documentation
- Code documentation
- How-to guides
- Example: Software manuals, API docs

## 📝 `/personal/`
- Personal notes
- Journals
- Letters
- Example: Daily notes, project planning

## 🎵 `/audio/`
- MP3, WMA recordings
- Voice memos
- Lectures, sermons
- Example: Meeting recordings, audio notes

## 📷 `/images/`
- Photos of handwritten notes
- Receipts
- Whiteboard captures
- Scanned documents
- Example: Handwritten meeting notes, receipts

---

## Quick Start

1. **Add documents** to appropriate folders
2. **Process all** with the batch script:
   ```bash
   python3 tests/process_training_data.py
   ```
3. **Review outputs** in `tests/training_outputs/`
4. **Iterate** - adjust prompts, reprocess, compare quality

## Tips

- Keep original filenames descriptive
- Mixed languages? → Use appropriate category
- Unsure? → Put in `/personal/` and organize later
- Large files (>10MB) → May take longer to process
