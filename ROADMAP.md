# Roadmap

Updated 17 Nov 2026.

**Rule for everything: data never leaves the device. No cloud services, no online fallbacks.**

## Done in this project

- HEIC photos (heic2any).
- Make scans searchable: Tesseract.js, English, Portuguese, Russian, Ukrainian.
- Translate pages with text through the browser's own on-device Translator (Chrome 138+, Edge 148+, desktop). Firefox has no API for sites; Mozilla's translation lives inside the browser only.
- Page fonts are served from this site, no request to Google.

## Still open (small)

- Mixed scripts in one form field.
- Editing rotated text.
- Touch drag on a real phone.
- Very large PDFs.
- Translating scans (needs OCR lines, then the same cover-and-set step).

## After this

- **Local OCR** as its own page: C++ preprocessing (deskew, binarise) compiled to WebAssembly, then Tesseract.js, plus a Python command line. Prepared files: tesseract.js 7.0.0, core 7.0.0, trained data for eng, por, rus, ukr.
- **MCP server.**
- Site checker, Contact kit, Agent rules.
