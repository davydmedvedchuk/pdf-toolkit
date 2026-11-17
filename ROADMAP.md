# Roadmap

Written 17 Nov 2026. What is left to build, in order.

## Next in this project

1. **HEIC photos.** Accept iPhone photos. Photo shrinker already bundles `heic2any`, reuse the same file.
2. **Make a scan searchable (OCR).** Run Tesseract.js on image pages, add an invisible text layer so text can be selected and searched. Languages: English, Portuguese, Russian, Ukrainian. Files are staged for the Local OCR project and can be shared.
3. **Translate a PDF.** Pick a target language, get a translated copy and download it. Plan, from private to less private:
   - Chrome's built-in Translator API: runs on the device, Chrome 138+ and Edge 148+ on desktop only, no Firefox or Safari, fixed list of languages. Check Portuguese and Russian in the current list before promising them.
   - Offline translation models in WebAssembly (for example Bergamot): works in any browser, but each language pair is a download of tens of MB. To be tested.
   - An online translation service, only if the user switches it on, with a clear warning that the text leaves the device.
   - Layout: for every text line, white out the original and set the translation in the same box, shrinking the size to fit. Scans go through OCR first. Also offer "download as plain text".
4. **Small gaps.** Mixed scripts in one form field. Editing rotated text. Check touch drag on a real phone. Try very large PDFs.

## After this

- **Local OCR** as its own page: C++ preprocessing (deskew, binarise) compiled to WebAssembly, then Tesseract.js, plus a Python command line. Prepared files: tesseract.js 7.0.0, core 6.1.2 and trained data for eng, por, rus, ukr.
- **MCP server.**
- Site checker, Contact kit, Agent rules.
