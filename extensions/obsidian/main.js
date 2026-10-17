const { Plugin, Notice } = require('obsidian');

module.exports = class FloatBoardPlugin extends Plugin {
    async onload() {
        // Ribbon Icon
        this.addRibbonIcon('pin', 'FloatBoard: Pin to Floating Board', () => {
            this.sendActiveNote();
        });

        // Command: Send current note
        this.addCommand({
            id: 'send-active-note',
            name: 'Pin current note to FloatBoard floating board',
            callback: () => this.sendActiveNote()
        });

        // Command: Send selected text
        this.addCommand({
            id: 'send-selection',
            name: 'Send selected text to FloatBoard',
            editorCallback: (editor) => {
                const selection = editor.getSelection();
                if (selection && selection.trim().length > 0) {
                    navigator.clipboard.writeText(selection).then(() => {
                        new Notice('Selected text sent to FloatBoard floating board!');
                    });
                } else {
                    new Notice('FloatBoard: No text selected in editor.');
                }
            }
        });

        // Command: Open WebPad
        this.addCommand({
            id: 'open-webpad',
            name: 'Open FloatBoard Online Floating WebPad',
            callback: () => {
                window.open('https://floatboard.xyz/web-pad/', '_blank');
            }
        });
    }

    sendActiveNote() {
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('FloatBoard: No active note found.');
            return;
        }

        this.app.vault.read(activeFile).then((content) => {
            navigator.clipboard.writeText(content).then(() => {
                new Notice(`Pinned "${activeFile.basename}" to FloatBoard!`);
            });
        });
    }
};
