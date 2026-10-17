# FloatBoard for Obsidian

Pin your active Obsidian markdown notes, code blocks, and selected text into an always-on-top desktop overlay using [FloatBoard](https://floatboard.xyz).

---

## Features

- **Ribbon Pin Button:** Click the pin icon in the Obsidian ribbon to pin the active note.
- **Command Palette:**
  - `FloatBoard: Pin current note to FloatBoard floating board`
  - `FloatBoard: Send selected text to FloatBoard`
  - `FloatBoard: Open FloatBoard Online Floating WebPad`
- **Zero Configuration:** Works seamlessly with your running [FloatBoard Desktop](https://floatboard.xyz) application.

---

## Manual Installation

1. Create a directory named `floatboard` inside your vault:
   ```bash
   <vault>/.obsidian/plugins/floatboard/
   ```
2. Copy `manifest.json` and `main.js` into that directory.
3. Reload Obsidian and enable **FloatBoard** in **Settings -> Community plugins**.

---

## Submitting to Obsidian Community Plugins

1. Fork [obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases).
2. Add your repository to `community-plugins.json`:
   ```json
   {
     "id": "floatboard",
     "name": "FloatBoard",
     "author": "Nazih Yazan",
     "description": "Pin active notes, code blocks, and selected text into FloatBoard always-on-top desktop board above all windows.",
     "repo": "nazihyazan/obsidian-floatboard"
   }
   ```
3. Open a Pull Request on `obsidianmd/obsidian-releases`.
