const remote = require('electron').remote;
function createLoginMessage(user){

        var loginMessageDiv = document.createElement("div")
        loginMessageDiv.setAttribute("id", "loginMessageDiv")
        loginMessageDiv.setAttribute("width","500px")
        loginMessageDiv.setAttribute("height","100px")
        loginMessageDiv.setAttribute("style", "text-align=center;")
    //이미지 생성
    if(user != 'NULL'){

        loginMessageDiv.innerHTML=  '<h2>' + user + '님 환영합니다.</h2>'  
       // remote.getCurrentWindow().loadFile('index.html');
        
    }
    else{
        loginMessageDiv.innerHTML=  "<h2>등록된 사용자가 아닙니다.</h2>"
    }
   
    var div = document.getElementById("loginMessage")
    div.appendChild(loginMessageDiv)
}

module.exports = createLoginMessage
