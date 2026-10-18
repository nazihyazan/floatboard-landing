const vscode = require('vscode');
const { exec } = require('child_process');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    const sendSelectionCmd = vscode.commands.registerCommand('floatboard.sendSelection', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('FloatBoard: No active editor found.');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection.isEmpty ? undefined : selection);

        if (!text || text.trim().length === 0) {
            vscode.window.showInformationMessage('FloatBoard: No text selected.');
            return;
        }

        // 1. Copy text to system clipboard (captured by FloatBoard clipboard history)
        await vscode.env.clipboard.writeText(text);

        // 2. Bring FloatBoard floating window into focus
        exec('floatboard', () => {});

        // 3. Show clear notification
        vscode.window.showInformationMessage('FloatBoard: Code copied! Press Ctrl+V on FloatBoard to paste as a note, or click the Clock icon to view history.');
    });

    const openWebPadCmd = vscode.commands.registerCommand('floatboard.openWebPad', () => {
        vscode.env.openExternal(vscode.Uri.parse('https://floatboard.xyz/web-pad/'));
    });

    context.subscriptions.push(sendSelectionCmd, openWebPadCmd);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
