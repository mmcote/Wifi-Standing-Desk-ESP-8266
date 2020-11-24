const { app, BrowserWindow } = require('electron');
const Store = require('electron-store');

const STANDING = "standing";
const SITTING = "sitting";
const IP = "ip";

function init() {
    const store = new Store();
    store.set(STANDING, 70);
    store.set(SITTING, 50);

    global.db = store;

    const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true
    }
  });

  win.loadFile('index.html');
  win.webContents.openDevTools();
}

app.whenReady().then(init)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    init()
  }
})