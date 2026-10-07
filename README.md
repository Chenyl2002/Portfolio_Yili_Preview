# 陈宜理 · 独立作品集技术预览

This repository publishes a separate technical preview through GitHub Pages. It does not modify `Chenyl2002/Portfolio_Yili` or `chenyili.fun`.

The static preview uses an adapted Bruno Simon scene with 陈宜理 portfolio content. Original attribution and third-party licenses are preserved inside the published site's `licenses/` directory and visible page credit.

## Reproducible deployment

The approved built website is stored as nine `preview.zip.partNN` files. `manifest.json` records each part's size and SHA-256, plus the reassembled ZIP checksum. `extract_preview.py` verifies all checksums and rejects unsafe paths before writing `dist/`.

Run `python3 extract_preview.py` with Python 3 to reproduce the exact static artifact locally. No package installation or network access is required. Serve the extracted `dist/` directory using a static web server.

The pinned official GitHub Actions workflow publishes the verified artifact to GitHub Pages. Repository settings use **GitHub Actions** as the Pages source. No custom domain or CNAME is configured.

This preview is public. The website contains the portfolio owner's approved name, portfolio content, and contact information. The repository contains built public assets rather than development credentials or private configuration.
