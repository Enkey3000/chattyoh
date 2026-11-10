// Runs in a sandboxed context. Exposes ONLY this small, explicit API to the page.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('desktop', {
  isElectron: true,
  platform: process.platform,
  saveFile: (name, text) => ipcRenderer.invoke('file:save', name, text),
  openFile: () => ipcRenderer.invoke('file:open'),
  hasKey: () => ipcRenderer.invoke('key:has'),
  setKey: (k) => ipcRenderer.invoke('key:set', k),
  complete: (messages, system) => ipcRenderer.invoke('ai:complete', messages, system),
  onMenu: (cb) => ipcRenderer.on('menu', (_e, action) => cb(action))
});
