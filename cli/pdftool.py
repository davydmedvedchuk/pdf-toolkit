#!/usr/bin/env python3
"""PDF toolkit, command-line version (Python + pypdf).

  python3 pdftool.py merge a.pdf b.pdf -o all.pdf
  python3 pdftool.py extract all.pdf 1-3,7 -o part.pdf     # pages 1,2,3 and 7
  python3 pdftool.py split all.pdf -o pages/               # one PDF per page
  python3 pdftool.py rotate all.pdf 90 -p 2,4 -o turned.pdf
  python3 pdftool.py images 1.jpg 2.png -o photos.pdf      # photos to A4 pages
  python3 pdftool.py info all.pdf
"""
import argparse, sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit("pypdf is missing. Install it with:  pip install -r requirements.txt")


def parse_pages(spec, total):
    """'1-3,7' -> [0, 1, 2, 6]  (1-based in, 0-based out). 'all' or empty means every page."""
    if not spec or spec == "all":
        return list(range(total))
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a or 1), int(b or total)
        else:
            a = b = int(part)
        if a < 1 or b > total or a > b:
            sys.exit(f"Pages out of range: '{part}' (the file has {total} pages)")
        out.extend(range(a - 1, b))
    return out


def open_pdf(path):
    r = PdfReader(path)
    if r.is_encrypted:
        sys.exit(f"{path} is password-protected. Remove the password first.")
    return r


def save(writer, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"saved {out}  ({len(PdfReader(str(out)).pages)} pages, {out.stat().st_size // 1024} KB)")


def cmd_merge(a):
    w = PdfWriter()
    for f in a.files:
        for p in open_pdf(f).pages:
            w.add_page(p)
    save(w, a.out)


def cmd_extract(a):
    r = open_pdf(a.file)
    w = PdfWriter()
    for i in parse_pages(a.pages, len(r.pages)):
        w.add_page(r.pages[i])
    save(w, a.out)


def cmd_split(a):
    r = open_pdf(a.file)
    out = Path(a.out)
    pad = len(str(len(r.pages)))
    for i, p in enumerate(r.pages, 1):
        w = PdfWriter()
        w.add_page(p)
        save(w, out / f"{Path(a.file).stem}-{str(i).zfill(pad)}.pdf")


def cmd_rotate(a):
    if a.degrees % 90:
        sys.exit("Degrees must be 90, 180 or 270.")
    r = open_pdf(a.file)
    chosen = set(parse_pages(a.p, len(r.pages)))
    w = PdfWriter()
    for i, p in enumerate(r.pages):
        if i in chosen:
            p.rotate(a.degrees)
        w.add_page(p)
    save(w, a.out)


def cmd_images(a):
    from PIL import Image, ImageOps
    A4, M = (595.28, 841.89), 24
    w = PdfWriter()
    import io
    for f in a.files:
        try:
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        except Exception:
            sys.exit(f"{f} is not an image Pillow can open.")
        land = im.width > im.height
        pw, ph = (A4[1], A4[0]) if land else A4
        k = min((pw - 2 * M) / im.width, (ph - 2 * M) / im.height)
        # one PDF page per image, picture centred, JPEG-compressed
        buf = io.BytesIO()
        canvas = Image.new("RGB", (round(pw), round(ph)), "white")
        small = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        canvas.paste(small, ((canvas.width - small.width) // 2, (canvas.height - small.height) // 2))
        canvas.save(buf, "PDF", resolution=72.0)
        buf.seek(0)
        w.add_page(PdfReader(buf).pages[0])
    save(w, a.out)


def cmd_info(a):
    r = open_pdf(a.file)
    print(f"{a.file}: {len(r.pages)} pages")
    for i, p in enumerate(r.pages, 1):
        print(f"  {i:>3}  {float(p.mediabox.width):.0f} x {float(p.mediabox.height):.0f} pt  rotate {p.get('/Rotate', 0)}")


def main():
    ap = argparse.ArgumentParser(description="Merge, split, extract, rotate PDFs and turn photos into a PDF.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("merge", help="join PDFs in the order given"); s.add_argument("files", nargs="+"); s.add_argument("-o", "--out", default="merged.pdf"); s.set_defaults(f=cmd_merge)
    s = sub.add_parser("extract", help="keep only some pages"); s.add_argument("file"); s.add_argument("pages", help="e.g. 1-3,7"); s.add_argument("-o", "--out", default="extract.pdf"); s.set_defaults(f=cmd_extract)
    s = sub.add_parser("split", help="one PDF per page"); s.add_argument("file"); s.add_argument("-o", "--out", default="pages"); s.set_defaults(f=cmd_split)
    s = sub.add_parser("rotate", help="rotate pages"); s.add_argument("file"); s.add_argument("degrees", type=int); s.add_argument("-p", default="all", help="pages, e.g. 2,4 (default all)"); s.add_argument("-o", "--out", default="rotated.pdf"); s.set_defaults(f=cmd_rotate)
    s = sub.add_parser("images", help="photos to a PDF, one per A4 page"); s.add_argument("files", nargs="+"); s.add_argument("-o", "--out", default="photos.pdf"); s.set_defaults(f=cmd_images)
    s = sub.add_parser("info", help="page count and sizes"); s.add_argument("file"); s.set_defaults(f=cmd_info)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
