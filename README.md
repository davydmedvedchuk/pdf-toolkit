# PDF toolkit

Website: https://davydmedvedchuk.github.io/pdf-toolkit/about/

Merge, split, reorder, rotate, delete and edit PDF pages. Add text, a stamp or a signature, fill forms, compress. Turn photos into a PDF. It runs in your browser, so your documents never leave your device.

**[Open the app](https://davydmedvedchuk.github.io/pdf-toolkit/)**

Drop PDFs and photos onto the page. Every page shows up as a thumbnail. Drag to reorder, rotate or delete pages, tap ✎ to edit one, select the ones you want, and save. No account, no ads, no install.

## What it does

- **Merge.** Add several PDFs, and photos too. They become one list of pages.
- **Reorder.** Drag a page, or use the arrows on each card.
- **Rotate and delete** single pages.
- **Edit a page (✎).** Add text (bold, any colour, Latin, Cyrillic, Greek), change a line of the existing text, put on a stamp (APPROVED, PAID, DRAFT or your own words, with a date if you like), draw a signature, white out an area, or crop the page. Undo is there.
- **Save a page as an image.** Tick the box in the editor and the page is flattened, so the old text underneath is really gone. The page can no longer be selected as text.
- **Fill in forms.** If a PDF has fillable fields, "Fill form" lists them. Values are written into the pages and the form is flattened.
- **Protected PDFs.** Enter the password and the pages are opened. Because the file cannot be copied page by page, they are saved as images.
- **Options.** File size (Smaller 150 dpi, Smallest 100 dpi: every page becomes an image), page numbers, and a watermark.

**About editing.** Without "Save this page as an image", changed text and white-out boxes are drawn on top of the page. The original text stays in the file underneath and can still be copied. New text is set in Inter, so it will not match the original font exactly. Added text covers Latin, Cyrillic and Greek. In one form field, mixed scripts are not supported (a Cyrillic field shows only Cyrillic letters).

**What it does not do.** OCR for scans, HEIC photos, rotated text editing, real digital (certificate) signatures, redaction tools beyond flattening the page.

## Command line (Python)

The same operations for scripts and whole folders. Uses `pypdf` and Pillow.

```
pip install -r cli/requirements.txt
python3 cli/pdftool.py merge a.pdf b.pdf -o all.pdf
python3 cli/pdftool.py extract all.pdf 1-3,7 -o part.pdf
python3 cli/pdftool.py split all.pdf -o pages/
python3 cli/pdftool.py rotate all.pdf 90 -p 2,4 -o turned.pdf
python3 cli/pdftool.py images 1.jpg 2.png -o photos.pdf
python3 cli/pdftool.py info all.pdf
```

## How it works

A single `index.html`. Pages are read and drawn with [pdf.js](https://mozilla.github.io/pdf.js/) (thumbnails) and written with [pdf-lib](https://pdf-lib.js.org/) (merging, rotating, photos). [fontkit](https://github.com/foliojs/fontkit) and the Inter font are used for the text you add. All are included in `vendor/`. The ZIP writer is hand-written. Nothing is sent anywhere.

## Credits

Made by Davyd Medvedchuk. Libraries: pdf-lib (MIT), pdf.js (Apache-2.0), fontkit (MIT). Font: Inter (SIL OFL 1.1). Licences are in `vendor/`.

MIT licence.
