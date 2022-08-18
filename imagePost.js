let mirrorDB = require('./mirror_db');
mirrorDB.userId = 1001;//receivedData;

const axios= require('axios');

let sender= 2002;
let contents = '1660631179465.jpg';

const fs = require('fs');

axios({
        url: 'http://localhost:3000/get/image', // 통신할 웹문서
        method: 'get', // 통신할 방식
        data : { // 인자로 보낼 데이터
          fileName : '1660840019907.txt',
          
        }
      })
.then( response =>{
    console.log(response);
    time = new Date().getTime();
     var file =  './image/server/' + time + '.jpg';
    url = response.data;
   
    var bstr = atob(url);
    var n = bstr.length;
    // base64 인코딩을 바이트 코드로 변환
    var u8arr = new Uint8Array(n);
    
    fs.writeFile(file, u8arr, 'utf8', function(error){
        if(error)
         throw(error);
    });
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

})
