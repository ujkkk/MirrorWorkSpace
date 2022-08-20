

const { app, BrowserWindow } = require("electron");

function createWindow() {
    let options = {
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        enableRemoteModule: true
    },
    backgroundColor:"#000000"
    }
   // options.fullscreen = true;
    options.autoHideMenuBar = true;
    const win = new BrowserWindow(options);
    
    //win.webContents.openDevTools();  
    //win.loadFile("addFriend/list.html");
    //win.loadFile("addFriend/list.html");
    win.loadFile("message_module/message.html");
    //win.loadFile("message_module/messegeSend/testMain.html");
}

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});