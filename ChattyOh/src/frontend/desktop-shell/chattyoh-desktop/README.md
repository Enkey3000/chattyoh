# ChattyOh Desktop (Electron)

Desktop build of the ChattyOh Inc app. The UI is one file: `renderer/index.html`.

## Run
```bash
npm install
npm start          # launches the app
npm run dist       # builds an installer into dist/ (dmg / nsis / AppImage)
```
Requires Node.js 18+. Build installers on the OS you are targeting.

## What's desktop-specific
- **Native menu** (File / Edit / View / Window / Help) with shortcuts: Ctrl/Cmd+N new project, Ctrl/Cmd+Shift+N new chat, Ctrl/Cmd+H home, Ctrl/Cmd+D dark mode.
- **Native Save / Open dialogs** for every Export, Backup and Restore.
- **Real AI**: Help → API Key… stores your Anthropic key encrypted with the OS keychain (`safeStorage`). Requests run in the main process, not the page. Default model `claude-sonnet-5-5`; change it by creating `config.json` in the app's userData folder: `{"model":"<model-id>"}`. Replies are not streamed yet.
- Window size/position remembered, single-instance lock, external links open in your browser, in-app navigation to remote sites is blocked.
- Security: `contextIsolation`, `sandbox`, no Node in the page; the page only sees the small API in `preload.js`, and IPC handlers only answer our own `file://` page.

## Where data lives
App data (projects, chats, etc.) is in the renderer's local storage inside Electron's userData folder, per workspace. Use File → Export Backup regularly.

## Revising and testing without Electron
Open `chattyoh-desktop-preview.html` (the same page as `renderer/index.html`) in any browser: it shows a simulated menu bar and uses browser downloads and a browser-stored test key. Edit that file, test, then copy it over `renderer/index.html`.

## Not included yet
Auto-update, code signing/notarization, tray icon, streaming AI replies. Simulated by design: deployments, test runs and "connection OK" in the app do not run real tools.
