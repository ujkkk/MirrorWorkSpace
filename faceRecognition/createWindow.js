const {BrowserWindow} = require("electron").remote
-


function createWindow(){
    let options = {
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
        backgroundColor:"#000000",
        //fullscreen : true,
        autoHideMenuBar : true
    }
    const win = new BrowserWindow(options)
    win.on("close", () =>{
        win = null
    })
    return win
}

module.exports =  createWindow