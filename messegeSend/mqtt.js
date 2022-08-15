const mqtt = require('mqtt');
const axios= require('axios');
const fs = require('fs')
const options = {
    host: '127.0.0.1',
    port: 1883
  };

const client = mqtt.connect(options);

let options2 ={
  encoding: 'utf-8',  // utf-8 인코딩 방식으로
  flag: 'r' // 읽기
}
const getDataFromFilePromise = (filePath) => {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, options2, (err, data) => {
      if (err) {
        reject(err);
      } else {  // 에러가 나지 않은 경우 resolve 메소드 실행 -> 파일 정보 읽어옴
        resolve(data);
      }
    });
  });
}
client.subscribe("capture/byteFile");
client.subscribe("capture")

client.on('message', async (topic, message, packet) => {
    console.log("message is "+ message);
    console.log("topic is "+ topic);
    let data1

    if(topic == 'capture'){
      document.location.href = './message'
    }
    //전송할 사진 찍기가 완료되면 받음
    //msg는 이미지의 바이트 코드
    if(topic == 'capture/byteFile'){
      filePath = 'media/test.jpg'
 
      var c = document.createElement('canvas');
      var img = document.getElementById('Img1');
      img.src = filePath 
      //c.height = img.naturalHeight;
      //c.width = img.naturalWidth;
      var ctx = c.getContext('2d');

      ctx.drawImage(img, 0, 0, c.width, c.height);
      var base64String = c.toDataURL();
      console.log(base64String)
            // fs.open('messegeSend/media/test.jpg', "r+", (error, fd) =>{
      //   fs.readFile('messegeSend/media/test.jpg','utf8', function(error, data) {
      //     if(error){
      //       //response.writeHead(500, {'Content-Type':'text/html'});
      //       console.log('500 Internal Server '+error);
      //     }else{
      //       // 6. Content-Type 에 4번에서 추출한 mime type 을 입력
      //       data1 = data.toString(8);
      //       console.log('data1 : ' +data1);
      //     }
      //   });
      // })
       
      axios({
        url: 'http://localhost:3000/send/images', // 통신할 웹문서
        method: 'post', // 통신할 방식
        data: { // 인자로 보낼 데이터
          content: base64String
        }
      });
     // document.getElementById('content').value = byteFile   
    }
})

module.exports = client