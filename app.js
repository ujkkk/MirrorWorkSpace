/* Section1. 필요 모듈 require */
var express = require('express');
const logger = require('morgan'); // 서버 접속 연결 확인 도와주는 모듈
const path = require('path')


var app = express() // express 는 함수이므로, 반환값을 변수에 저장한다.
app.set('port', process.env.PORT || 3000);
app.use(logger('dev'));
/* req.body에 접근하기 위해 필요한 미들웨어 - 파싱도 해줌 */
app.use(express.json()); //req.body가 json 형태일때 사용
app.unsubscribe(express.urlencoded({extended: false}));



// 3000 포트로 서버 오픈
app.listen(app.get('port'), function() { //포트 연결 및 서버 실행
    console.log(app.get('port'), '번 포트에서 대기 중');

});

const multer = require('multer');
const { pathToFileURL } = require('url');
const { nextTick } = require('process');

const upload = multer({
    storage: multer.diskStorage({
        //어디에 저장할지
        destination(req, file, done){
            done(null, 'uploas/');
        },
        //저장할 파일이름
        filename(req, file, done){
            const ext = path.extname(file.originalname);
            //req나 file의 데이터를 가공해서 done으로 넘긴다
            done(null, path.basename(file.originalname, ext) + Date.now() + ext);
        }
    }),
    //파일크기 5MB로 제한
    limits: {fileSize:5*1024*1024}
})
// const msgInsertDB = (req,res)=>{

//     console.log("func msgInserDB: Request Post Success");
//     // json 파싱 과정
//     let reqBody = req.body;
//     var data = {"sender":reqBody.sender,"receiver":reqBody.receiver,"content":reqBody.content}

//     //db insert
//     _db.createColumns('message',data);

//     //response 보냄(echo)
//     res.json(reqBody);
// }

const checkUpdate = (req,res)=>{
    console.log("func checkUpdate: Request Get Success");
    

}

app.get('/',(req, res)=>{
    
    res.sendFile(path.join(__dirname, 'messageSend.html'))
});
//app.post('/send',msgInsertDB);
app.get('/check/:id',checkUpdate);
//single 미들웨어를 먼저 실행하면 req.file 객체를 만들어줌
//single 매개변수는 input의 name이나 form id
app.post('/send/vedio', upload.single('video'), (req, res, next)=>{
    console.log(req.file, req.body);
    res.send('ok');
    //다음 미들웨어에 데이터 넘겨주기
    req.data =req.body;
    next();
},(req, res) =>{
    console.log(req.data);
})
