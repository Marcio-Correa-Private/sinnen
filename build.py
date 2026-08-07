#!/usr/bin/env python3
"""Gera dist/ a partir de src/app.html.

O supabase-js e' embutido no proprio HTML para a app funcionar tambem
offline e abrindo o ficheiro directamente (file://), sem CDN.

    npm install
    python3 build.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "app.html"
DIST = ROOT / "dist"
LIB = ROOT / "node_modules" / "@supabase" / "supabase-js" / "dist" / "umd" / "supabase.js"

CDN_TAG = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'


def main() -> None:
    if not LIB.exists():
        raise SystemExit("falta o supabase-js — corre `npm install` primeiro")

    html = SRC.read_text(encoding="utf-8")
    if CDN_TAG not in html:
        raise SystemExit(f"nao encontrei o script do CDN em {SRC}")

    lib = LIB.read_text(encoding="utf-8")
    out = html.replace(CDN_TAG, "<script>\n" + lib + "\n</script>")

    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(out, encoding="utf-8")
    # 200.html: fallback de SPA no Netlify/surge
    shutil.copy(DIST / "index.html", DIST / "200.html")
    shutil.copy(ROOT / "brand" / "icon.svg", DIST / "icon.svg")

    kb = len(out.encode()) / 1024
    print(f"dist/index.html  {kb:.0f} KB")


if __name__ == "__main__":
    main()
