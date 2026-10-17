# FloatBoard - Flathub Submission Guide

App ID: `xyz.floatboard.FloatBoard`

This directory contains all packaging files needed to publish FloatBoard on **Flathub**.

---

## Included Files

- `xyz.floatboard.FloatBoard.yml`: Flatpak manifest.
- `xyz.floatboard.FloatBoard.desktop`: FreeDesktop application entry.
- `xyz.floatboard.FloatBoard.metainfo.xml`: AppStream metadata (OARS 1.1 compliant).
- `xyz.floatboard.FloatBoard.png`: 256x256 application icon.

---

## Submission Steps to Flathub

1. **Fork the Flathub Repository:**
   Visit [https://github.com/flathub/flathub](https://github.com/flathub/flathub) and click **Fork**.

2. **Clone your fork locally:**
   ```bash
   git clone git@github.com:<your-username>/flathub.git
   cd flathub
   ```

3. **Create a branch for the new app:**
   ```bash
   git checkout -b new-pr/xyz.floatboard.FloatBoard
   ```

4. **Copy the manifest and assets:**
   Copy the 4 files from `packaging/flathub/` into the root of your branch:
   - `xyz.floatboard.FloatBoard.yml`
   - `xyz.floatboard.FloatBoard.desktop`
   - `xyz.floatboard.FloatBoard.metainfo.xml`
   - `xyz.floatboard.FloatBoard.png`

5. **Commit and Push:**
   ```bash
   git add xyz.floatboard.FloatBoard.*
   git commit -m "Add xyz.floatboard.FloatBoard"
   git push origin new-pr/xyz.floatboard.FloatBoard
   ```

6. **Open a Pull Request:**
   Go to [https://github.com/flathub/flathub](https://github.com/flathub/flathub) and submit a Pull Request.
   The Flathub build bot (`flathubbot`) will trigger a test build automatically.

7. **Verify Domain Badge (Verified App):**
   Because the ID is `xyz.floatboard.FloatBoard` and you control `floatboard.xyz`, you can verify ownership directly in the Flathub developer portal via DNS TXT record or HTTP token.
