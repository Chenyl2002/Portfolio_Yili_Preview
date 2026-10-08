# 陈宜理 · 独立作品集技术预览

This repository publishes a separate portfolio preview through GitHub Pages. It does not modify `Chenyl2002/Portfolio_Yili` or `chenyili.fun`. No custom domain or CNAME is configured.

The static preview adapts Bruno Simon's scene and preserves original attribution and third-party licenses in the published `licenses/` directory and visible page credit.

This art-integration technical preview adds newly authored CHEN YILI lettering and a Voyage navigation kiosk; these are portfolio props, not exports from the owner's UE5 project. The original interactive map and upstream world remain. The final-I collider alone is narrowed from 1.375374436378479 to 0.35772550106048584 scene units to remove an invisible margin; all other 239 colliders are preserved. Static checks, build, and offline model review do not establish live 3D rendering, driving, collision/reset behavior, audio, map interaction, mobile usability, or GPU performance. Those checks remain outstanding.

## Exact, offline deployment

The nine existing `preview.zip.partNN` files retain the approved baseline archive from commit `93b16facda9ed4abc903ba749b4e88e4f8ab7afd`. `manifest.json` is unchanged. The small `preview-delta.zip` contains only added or changed public assets, while `release-manifest.json` specifies exact removals and every final file's size and SHA-256.

From a clean checkout with no `dist/` directory, run:

```sh
python3 extract_preview.py
```

No package installation or network access is needed. The extractor verifies the pinned baseline, delta checksum, safe archive paths and types, exact change/deletion sets, preserved license files, and the complete final output manifest. It builds in a temporary directory and exposes `dist/` only after all checks pass. It refuses an existing `dist/` rather than mixing in stale files. For a repeat run, use a new clean checkout.

The original pinned official GitHub Actions workflow publishes that verified `dist/` to GitHub Pages. Serve `dist/` with any static web server for local review.

Only built public assets are packaged. Development sources, credentials, private configurations, and custom-domain settings are excluded. This public preview contains the portfolio owner's approved portfolio and contact content.
