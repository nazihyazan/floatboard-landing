const { _electron: electron } = require('/home/mou/Videos/carrer/node_modules/playwright');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

async function run() {
  const executablePath = '/home/mou/Videos/carrer/squashfs-root/floatboard';
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'floatboard-final-snap-'));
  const env = { 
    ...process.env, 
    XDG_CONFIG_HOME: path.join(profile, 'config'),
    DISPLAY: process.env.DISPLAY || ':0',
    XAUTHORITY: process.env.XAUTHORITY || path.join(os.homedir(), '.Xauthority')
  };
  delete env.ELECTRON_RUN_AS_NODE;

  console.log('Launching FloatBoard native app...');
  const app = await electron.launch({
    executablePath,
    args: ['--no-sandbox', '--disable-gpu', `--user-data-dir=${profile}`],
    env,
    timeout: 30000
  });

  const page = await app.firstWindow({ timeout: 25000 });
  await page.waitForFunction(() => window.floatingBoard && document.querySelector('#board'));

  // Resize window to perfect 780 x 520
  await app.evaluate(({ BrowserWindow }) => {
    const win = BrowserWindow.getAllWindows()[0];
    win.setSize(780, 520);
    win.center();
    win.show();
    win.focus();
  });

  const landingAssets = '/home/mou/Documents/floatboard-landing/blog/assets';
  const imgFiles = [
    { file: 'gif-1-poster.jpg', name: 'app-workflow.jpg' },
    { file: 'gif-2-poster.jpg', name: 'image-references.jpg' },
    { file: 'gif-3-poster.jpg', name: 'preview-grid.jpg' },
    { file: 'code-and-image-references.jpg', name: 'code-and-mockup.jpg' }
  ];

  const importedMedia = [];
  for (const item of imgFiles) {
    const sourcePath = path.join(landingAssets, item.file);
    const media = await page.evaluate(async ({ sourcePath, name }) => {
      return await window.floatingBoard.importMedia({
        sourcePath,
        kind: 'image',
        name,
        mime: 'image/jpeg'
      });
    }, { sourcePath, name: item.name });
    if (media) importedMedia.push(media);
  }

  console.log('Imported media count:', importedMedia.length);

  await page.evaluate(async (mediaItems) => {
    const textItems = [
      {
        id: 'note-1',
        text: 'REST API & Auth Tokens:\nBase: https://api.floatboard.xyz/v1\nAuth: Bearer sec_live_9942a781\nContent-Type: application/json\nRate-Limit: 120 req/min (US-East / EU)',
        createdAt: new Date().toISOString()
      },
      {
        id: 'note-2',
        text: 'Single-Monitor Dev Workflow:\n[x] Always-on-top pinned (No Alt-Tab)\n[x] Auto-capture curl requests & JSON\n[x] 100% Offline storage (GDPR safe)\n[ ] Test webhook signature verification',
        createdAt: new Date().toISOString()
      },
      {
        id: 'note-3',
        text: 'Dev Scratchpad & CLI Commands:\n• git cherry-pick b227f30..c8dc339\n• docker compose up -d postgres redis\n• VS Code shortcut: Ctrl+Shift+Alt+B\n• Lifetime license: $5.99 (DEVTO50)',
        createdAt: new Date().toISOString()
      }
    ];

    state = normalizeLoadedBoard({
      version: 1,
      sections: [
        { type: 'text', items: textItems },
        { type: 'image', items: mediaItems }
      ]
    });
    await saveNow();
    render();
  }, importedMedia);

  await page.waitForTimeout(1000);
  console.log('Board populated with developer notes and reference images.');

  // Give 4s for image thumbnails and layout rendering
  await page.waitForTimeout(4000);

  const targetPng = '/home/mou/Documents/floatboard-landing/blog/assets/developer-floating-notes-workspace.png';
  const targetJpg = '/home/mou/Documents/floatboard-landing/blog/assets/developer-floating-notes-workspace.jpg';

  await page.screenshot({ path: targetPng });
  console.log('Saved clean screenshot to:', targetPng);

  // Convert to JPG
  execSync(`ffmpeg -i "${targetPng}" -q:v 2 "${targetJpg}" -y`);
  console.log('Converted to JPG:', targetJpg);

  await page.waitForTimeout(1500);
  await app.close();
  fs.rmSync(profile, { recursive: true, force: true });
  console.log('Finished capture successfully.');
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
