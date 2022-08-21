let mirrorDB = require('../mirror_db');
mirrorDB.userId = 1001;//receivedData;

const axios= require('axios');

let sender= 2002;
let contents = '1660631179465.jpg';

const fs = require('fs');
mirror_db = require('../mirror_db');

//받은 메시지가 이미지이면 서버에 해당 파일을 요청하여
//해당 미러에 폴더를 저장
axios({
        url: 'http://localhost:9000/get/image', // 통신할 웹문서
        method: 'get', // 통신할 방식
        data : { // 인자로 보낼 데이터
          fileName : '1661002225663.txt' ,
          ok : 'ok'      
        }
      })
      //받아온 파일 저장
.then( response => new Promise((resolve, reject) =>{
  console.log(response);
    time = new Date().getTime();
    var file =  time + '.jpg';
    url = response.data;
   
    var bstr = atob(url);
    var n = bstr.length;
    // base64 인코딩을 바이트 코드로 변환
    var u8arr = new Uint8Array(n);
    
    fs.writeFile(file, u8arr, 'utf8', function(error){
    });
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    resolve(file);
    //mesaage DB에 저장
  }).then(file =>{
    //본인의 id는 어떻게 알아낼지
      let data = {
            sender : sender,
            receiver : '1001',
            content : file,
            type : 'image'
        };
        mirror_db.createColumns('message', data);

  })

)
