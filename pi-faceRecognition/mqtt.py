from re import T
import paho.mqtt.client as mqtt
import json
from camera import createCropImage
import os
import camera
global client

curDir = os.path.dirname(os.path.realpath(__file__))
    #curDir = '.' + os.path.sep + 'faceRecognition'
os.chdir(curDir)

new_account_flag = False
login_flag = False
loginCamera_flag = False
createAccountCamera_flag = False
exist_flag = False
delete_login_flag = False

user_id = 0
def on_connect(client, userdata, flag, rc):
    print("Connect with result code:"+ str(rc))
    client.subscribe('loginCamera')
    client.subscribe('createAccountCamera')
    client.subscribe('exist')
    client.subscribe('closeCamera')
    client.subscribe('delete/camera')


def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print("payload : " + str(message))

    if(msg.topic == 'closeCamera'):
        camera.closeCam()
    #삭제 버튼 누른 유저가 삭제할 수 있는지 얼굴인식 서버에게
    #로그인 해서 id 가져오기
    elif(msg.topic =='delete/camera'):
        client.publish('delete/login', 'ok')
        global delete_login_flag
        delete_login_flag = True

    elif(msg.topic == 'loginCamera'):
        print("topic : " + msg.topic)
        if(str(message) == 'login'):
            global loginCamera_flag
            loginCamera_flag = True
            
    elif(msg.topic == 'createAccountCamera'):
        print("topic : " + msg.topic)
        global user_id
        user_id = str(message)
        global createAccountCamera_flag
        createAccountCamera_flag = True

    elif(msg.topic == 'existingUser'):
        client.publish('exist', 'ok')
        global exist_flag
        exist_flag = True

            
       
broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정
print('broker_ip : ' + broker_ip)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883)
client.loop_start()




# 디렉토리 안의 모든 이미지를 불러오고 이미지에서 얼굴 추출
def load_image(directory):
    byteArr = list()
    count = 0
    for filename in os.listdir(directory):
        count = count + 1
        path = directory +os.sep + filename 
        f = open(path,"rb")
        filecontent = f.read()
        byteArr.append(bytearray(filecontent))
    return byteArr
        
#로그인하기 위해 사진찍기 시작
def Camera_login(count):
    #카메라 키기
    camera.onCam()
    print('while - loginCamera')
    # 카메라로 사진 찍어서 얼굴부분만 크롭해서 저장
    dir_name = os.path.join('face','login')
    # dir_name1 폴더안에 10장의 얼굴 이미지를 저장
    saved_dir_name = createCropImage('user', dir_name, count)
    # 사진 넘겨주기
    imagelist = load_image(saved_dir_name)
    for i in range(count) :
        imageByte = imagelist.pop()
        print(imageByte)
        #result = str(imageByte, 'utf-16')
        # imageByte = imageByte.decode('utf-16')
        data = json.dumps({ 'mirror_id' : '100', 
                            'file' : imageByte.decode('utf-16','ignore')})
        # 얼굴인식 서버에게 찍은 사진을 보냄
        client.publish('login', data)


def Camera_createAccount(username, count):
    camera.onCam()
    # 사진 넘겨주기
    imagelist = load_image(dir_name2)
    for i in range(count) :
        imageByte = imagelist.pop()
        imageByte_list = imageByte.split("'")
        # 서버에 보냄   
        client.publish('createAccount/image', imageByte_list[1])

def existingUsers():
    Camera_login(10)



stopFlag = False
while True :
    if(exist_flag):
        print('기존 유저인지 확인하는중')
        # 카메라로 사진 찍어서 얼굴부분만 크롭해서 저장
        dir_name1 = os.path.join('face','login')
        dir_name2 = os.path.join('face','login','user')
        createCropImage('user',  dir_name1, 10)
        # 사진 넘겨주기
        imagelist = load_image(dir_name2)
        for i in range(10) :
            imageByte = imagelist.pop()
            client.publish('login', imageByte)
        exist_flag = False

    if(delete_login_flag):
        print('삭제버튼을 누른유저가 삭제권한이 있는지 확인')
        # 카메라로 사진 찍어서 얼굴부분만 크롭해서 저장
        dir_name1 = os.path.join('face','login')
        dir_name2 = os.path.join('face','login','user')
        createCropImage('user',  dir_name1, 10)
        # 사진 넘겨주기
        imagelist = load_image(dir_name2)
        for i in range(10) :
            imageByte = imagelist.pop()
            client.publish('login', imageByte)
        delete_login_flag = False
    
    #유저가 로그인버튼을 누르면 사진 10장을 찍고 
    #얼굴인식하는 서버에 사진을 보내서 유저를 식별함
    if (loginCamera_flag):
        Camera_login(10)
        loginCamera_flag = False

    if(createAccountCamera_flag):
        
        if not (user_id == 0):
            print('user : ' + user_id)
            # 시퀀스 받아와서 id 주기
            # 파이에게 계정 생성하라고 pub
            client.publish('createAccount/start', int(user_id))
            print('while - createAccount')
            # 카메라로 사진 찍어서 얼굴부분만 크롭해서 저장
            dir_name1 = os.path.join('face','train')
            dir_name2 = os.path.join('face','train', 'user')
            createCropImage('user', dir_name1, 20)


            Camera_createAccount('user', 20)
            createAccountCamera_flag = False
    if (stopFlag):
        break
   
print('끝내기')
client.loop_stop()
client.disconnect()