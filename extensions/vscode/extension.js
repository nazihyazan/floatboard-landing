const vscode = require('vscode');

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

        // FloatBoard monitors the OS clipboard. Writing text places it directly on the floating board.
        await vscode.env.clipboard.writeText(text);

        vscode.window.setStatusBarMessage('$(pinned) Sent to FloatBoard floating board!', 3000);
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
