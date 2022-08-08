const remote = require('electron').remote;
function createLoginMessage(user){

    var loginMessageDiv
    if(document.getElementById("loginMessageDiv") == null){
        loginMessageDiv = document.createElement("div")
        loginMessageDiv.setAttribute("id", "loginMessageDiv")
        loginMessageDiv.setAttribute("width","500px")
        loginMessageDiv.setAttribute("height","100px")
        loginMessageDiv.setAttribute("style", "text-align=center;")
    }
    else
        loginMessageDiv = document.getElementById("loginMessageDiv") 
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

function createMessage(msg){

    var loginMessageDiv
    if(document.getElementById("loginMessageDiv") == null){
        loginMessageDiv = document.createElement("div")
        loginMessageDiv.setAttribute("id", "loginMessageDiv")
        loginMessageDiv.setAttribute("width","500px")
        loginMessageDiv.setAttribute("height","100px")
        loginMessageDiv.setAttribute("style", "text-align=center;")
    }
    else
        loginMessageDiv = document.getElementById("loginMessageDiv") 
//이미지 생성

    loginMessageDiv.innerHTML=  '<h2>' + msg + '</h2>'  


    var div = document.getElementById("loginMessage")
    div.appendChild(loginMessageDiv)
}

module.exports = {createLoginMessage, createMessage}
