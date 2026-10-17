# FloatBoard for VS Code

Pin code snippets, error traces, and documentation notes directly to your [FloatBoard](https://floatboard.xyz) floating desktop overlay.

---

## Features

- **Right-Click Context Menu:** Highlight any code block, right-click, and select **FloatBoard: Send Selection to Floating Board**.
- **Keyboard Shortcut:** Press `Ctrl+Alt+F` (or `Cmd+Alt+F` on macOS) to instantly send highlighted code to your floating board.
- **Always on Top:** Pinned code stays floating above your full-screen editor or terminal so you never have to split screens or Alt-Tab.
- **WebPad Access:** Quick command to open the free online Document Picture-in-Picture [FloatBoard WebPad](https://floatboard.xyz/web-pad/).

---

## Requirements

Requires [FloatBoard Desktop](https://floatboard.xyz) (Windows, macOS, or Linux) running in the background.

---

## Publishing to VS Code Marketplace

1. Install `vsce`:
   ```bash
   npm install -g @vscode/vsce
   ```
2. Log in with your Personal Access Token from [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage):
   ```bash
   vsce login nazihyazan
   ```
3. Package and publish:
   ```bash
   vsce publish
   ```
