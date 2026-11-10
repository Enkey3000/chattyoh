const { app, BrowserWindow, Menu, dialog, ipcMain, shell, safeStorage } = require('electron');
const path = require('path'), fs = require('fs');

const P = (n) => path.join(app.getPath('userData'), n);
const readJSON = (n, d) => { try { return JSON.parse(fs.readFileSync(P(n), 'utf8')); } catch { return d; } };
const writeJSON = (n, v) => { try { fs.writeFileSync(P(n), JSON.stringify(v)); } catch {} };
const trusted = (e) => !!(e.senderFrame && e.senderFrame.url.startsWith('file://')); // only our own page may call IPC
let win;

function createWindow() {
  const bounds = readJSON('window.json', { width: 1360, height: 860 });
  win = new BrowserWindow({
    ...bounds, minWidth: 900, minHeight: 600, title: 'ChattyOh', show: false,
    backgroundColor: '#0A5BD9', icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false, sandbox: true, webSecurity: true }
  });
  win.once('ready-to-show', () => win.show());
  const saveBounds = () => { if (!win.isMaximized() && !win.isMinimized()) writeJSON('window.json', win.getBounds()); };
  win.on('resize', saveBounds); win.on('move', saveBounds);
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https:\/\//.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('file://')) e.preventDefault(); });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

const send = (a) => () => win && win.webContents.send('menu', a);
const menu = () => [
  ...(process.platform === 'darwin' ? [{ role: 'appMenu' }] : []),
  { label: 'File', submenu: [
    { label: 'New Project', accelerator: 'CmdOrCtrl+N', click: send('new-project') },
    { label: 'New Chat', accelerator: 'CmdOrCtrl+Shift+N', click: send('new-chat') },
    { type: 'separator' },
    { label: 'Import Backup…', click: send('import-backup') },
    { label: 'Export Backup…', click: send('export-backup') },
    { type: 'separator' },
    process.platform === 'darwin' ? { role: 'close' } : { role: 'quit' } ] },
  { role: 'editMenu' },
  { label: 'View', submenu: [
    { label: 'Home', accelerator: 'CmdOrCtrl+H', click: send('home') },
    { label: 'Toggle Dark Mode', accelerator: 'CmdOrCtrl+D', click: send('toggle-theme') },
    { label: 'Expand All Menus', click: send('expand-all') },
    { label: 'Collapse All Menus', click: send('collapse-all') },
    { type: 'separator' },
    { role: 'reload' }, { role: 'toggleDevTools' }, { type: 'separator' },
    { role: 'resetZoom' }, { role: 'zoomIn' }, { role: 'zoomOut' }, { role: 'togglefullscreen' } ] },
  { role: 'windowMenu' },
  { label: 'Help', submenu: [
    { label: 'API Key…', click: send('api-key') },
    { label: 'About ChattyOh', click: () => dialog.showMessageBox(win, { type: 'info', title: 'ChattyOh', message: 'ChattyOh Inc', detail: `Version ${app.getVersion()}\nElectron ${process.versions.electron}` }) } ] }
];

// ---- IPC ----
ipcMain.handle('file:save', async (e, name, text) => {
  if (!trusted(e) || typeof text !== 'string' || text.length > 20e6) return { ok: false };
  const r = await dialog.showSaveDialog(win, { defaultPath: path.basename(String(name || 'export.txt')) });
  if (r.canceled || !r.filePath) return { ok: false, canceled: true };
  await fs.promises.writeFile(r.filePath, text, 'utf8');
  return { ok: true, path: r.filePath };
});
ipcMain.handle('file:open', async (e) => {
  if (!trusted(e)) return null;
  const r = await dialog.showOpenDialog(win, { properties: ['openFile'], filters: [{ name: 'JSON / text', extensions: ['json', 'txt', 'md', 'csv'] }] });
  if (r.canceled || !r.filePaths[0]) return null;
  const st = await fs.promises.stat(r.filePaths[0]);
  if (st.size > 5e6) return { error: 'File is larger than 5 MB' };
  return { name: path.basename(r.filePaths[0]), text: await fs.promises.readFile(r.filePaths[0], 'utf8') };
});
// API key is encrypted with the OS keychain via safeStorage; never stored in plain text.
const readKey = () => { try { return safeStorage.decryptString(fs.readFileSync(P('key.bin'))); } catch { return ''; } };
ipcMain.handle('key:has', (e) => trusted(e) && !!readKey());
ipcMain.handle('key:set', (e, k) => {
  if (!trusted(e) || typeof k !== 'string' || !safeStorage.isEncryptionAvailable()) return false;
  try { k.trim() ? fs.writeFileSync(P('key.bin'), safeStorage.encryptString(k.trim())) : fs.rmSync(P('key.bin'), { force: true }); return true; } catch { return false; }
});
ipcMain.handle('ai:complete', async (e, messages, system) => {
  if (!trusted(e) || !Array.isArray(messages)) return { ok: false, error: 'Request rejected' };
  const key = readKey(); if (!key) return { ok: false, error: 'no-key' };
  const model = (readJSON('config.json', {}).model) || 'claude-sonnet-5-5'; // edit config.json in the userData folder to change
  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model, max_tokens: 1024, system: typeof system === 'string' ? system : undefined,
        messages: messages.slice(-20).map((m) => ({ role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content).slice(0, 20000) })) })
    });
    const j = await r.json();
    if (!r.ok) return { ok: false, error: (j.error && j.error.message) || 'HTTP ' + r.status };
    return { ok: true, text: (j.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('') };
  } catch (err) { return { ok: false, error: String((err && err.message) || err) }; }
});

// ---- lifecycle ----
if (!app.requestSingleInstanceLock()) { app.quit(); }
else {
  app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });
  app.whenReady().then(() => {
    Menu.setApplicationMenu(Menu.buildFromTemplate(menu()));
    createWindow();
    app.on('activate', () => { if (!BrowserWindow.getAllWindows().length) createWindow(); });
  });
  app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
}
