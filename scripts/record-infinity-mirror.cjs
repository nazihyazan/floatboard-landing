const { _electron: electron } = require('/home/mou/Videos/carrer/node_modules/playwright');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

async function run() {
  const executablePath = '/home/mou/Videos/carrer/squashfs-root/floatboard';
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'floatboard-mirror-run-'));
  const videoDir = path.join(profile, 'video');
  fs.mkdirSync(videoDir, { recursive: true });

  const env = { 
    ...process.env, 
    XDG_CONFIG_HOME: path.join(profile, 'config'),
    DISPLAY: process.env.DISPLAY || ':0',
    XAUTHORITY: process.env.XAUTHORITY || path.join(os.homedir(), '.Xauthority')
  };
  delete env.ELECTRON_RUN_AS_NODE;

  console.log('Launching FloatBoard for video recording...');
  const app = await electron.launch({
    executablePath,
    args: ['--no-sandbox', '--disable-gpu', `--user-data-dir=${profile}`],
    env,
    recordVideo: {
      dir: videoDir,
      size: { width: 960, height: 540 }
    },
    timeout: 40000
  });

  const page = await app.firstWindow({ timeout: 25000 });
  await page.waitForFunction(() => window.floatingBoard && document.querySelector('#board'));

  // Sized cleanly to 840x520
  await app.evaluate(({ BrowserWindow }) => {
    const win = BrowserWindow.getAllWindows()[0];
    win.setSize(840, 520);
    win.center();
    win.show();
    win.focus();
  });

  // Switch to Dark theme
  await page.click('#theme-toggle-btn');
  await page.waitForTimeout(600);

  // Pin button
  const pinBtn = await page.$('#pin-btn');
  if (pinBtn) await pinBtn.click();
  await page.waitForTimeout(500);

  const mediaItems = [];
  const textItems = [
    {
      id: 'mirror-spec-1',
      text: 'Instant Floating Screenshot Pin:\n• Snipping / Screenshot -> Auto-Pinned\n• Zero file clutter on desktop\n• Always visible above active IDE & apps\n• GDPR safe / 100% offline local memory',
      createdAt: new Date().toISOString()
    },
    {
      id: 'mirror-spec-2',
      text: 'Recursive Mirror Loop:\n[x] Capture 1: Initial window state\n[x] Capture 2: Pinned screenshot in board\n[x] Capture 3: Recursive nested frame\n[x] Capture 4: Infinite reference tunnel',
      createdAt: new Date().toISOString()
    }
  ];

  // Set initial text cards
  await page.evaluate(({ textItems, mediaItems }) => {
    state = normalizeLoadedBoard({
      version: 1,
      sections: [
        { type: 'text', items: textItems },
        { type: 'image', items: mediaItems }
      ]
    });
    saveNow();
    render();
  }, { textItems, mediaItems });

  console.log('Initial state displayed.');
  await page.waitForTimeout(2500);

  // Perform 4 sequential screenshot capture & insert steps
  for (let i = 1; i <= 4; i++) {
    console.log(`Iteration ${i}: Taking screenshot...`);
    const snapFile = path.join(profile, `mirror_step_${i}.png`);
    await page.screenshot({ path: snapFile });
    await page.waitForTimeout(600);

    console.log(`Iteration ${i}: Importing screenshot into FloatBoard...`);
    const media = await page.evaluate(async ({ sourcePath, name }) => {
      return await window.floatingBoard.importMedia({
        sourcePath,
        kind: 'image',
        name,
        mime: 'image/png'
      });
    }, { sourcePath: snapFile, name: `screenshot-loop-${i}.png` });

    if (media) {
      mediaItems.push(media);
      await page.evaluate(({ textItems, mediaItems }) => {
        state = normalizeLoadedBoard({
          version: 1,
          sections: [
            { type: 'text', items: textItems },
            { type: 'image', items: mediaItems }
          ]
        });
        saveNow();
        render();
      }, { textItems, mediaItems });
    }

    console.log(`Iteration ${i} complete. Current image count: ${mediaItems.length}`);
    await page.waitForTimeout(2800);
  }

  // Hover over the final image card to show the active preview
  console.log('Focusing final recursive card...');
  const cardSelector = '.image-section .board-item:last-child, .image-section img:last-child';
  try {
    const lastCard = await page.$(cardSelector);
    if (lastCard) {
      await lastCard.hover();
      await page.waitForTimeout(1000);
    }
  } catch (e) {
    console.log('Hover notice:', e.message);
  }

  // Final hold so viewer can appreciate the infinite mirror
  await page.waitForTimeout(3500);

  // Capture the final poster
  const targetPng = '/home/mou/Documents/floatboard-landing/blog/assets/infinity-mirror-screenshot-reference.png';
  const targetJpg = '/home/mou/Documents/floatboard-landing/blog/assets/infinity-mirror-screenshot-reference.jpg';
  await page.screenshot({ path: targetPng });
  console.log('Saved final poster PNG to:', targetPng);

  // Gracefully close to finish webm recording
  await page.waitForTimeout(1000);
  await app.close();
  console.log('App closed. Locating video file...');

  const videoFiles = fs.readdirSync(videoDir).filter(f => f.endsWith('.webm'));
  if (videoFiles.length === 0) {
    throw new Error('No recorded video file found in ' + videoDir);
  }

  const rawVideo = path.join(videoDir, videoFiles[0]);
  const targetMp4 = '/home/mou/Documents/floatboard-landing/blog/assets/infinity-mirror-screenshot-demo.mp4';

  console.log('Converting', rawVideo, 'to MP4:', targetMp4);
  execSync(`ffmpeg -i "${rawVideo}" -c:v libx264 -pix_fmt yuv420p -movflags +faststart -r 30 -vf "scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2" -y "${targetMp4}"`);
  console.log('MP4 created successfully:', targetMp4);

  // Convert poster PNG to high-quality JPG (780x520)
  execSync(`ffmpeg -i "${targetPng}" -q:v 2 -vf "scale=780:520:force_original_aspect_ratio=decrease,pad=780:520:(ow-iw)/2:(oh-ih)/2" -y "${targetJpg}"`);
  console.log('Poster JPG created successfully:', targetJpg);

  fs.rmSync(profile, { recursive: true, force: true });
  console.log('Infinity mirror video recording finished.');
}

run().catch(err => {
  console.error('Error during recording:', err);
  process.exit(1);
});
