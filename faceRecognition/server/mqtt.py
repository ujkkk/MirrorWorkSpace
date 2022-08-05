from asyncio.windows_events import NULL
from pydoc import cli
from re import T
import paho.mqtt.client as mqtt
from login import login
from createAccount import createAccoount
import os
from keras.models import load_model

curDir = os.path.dirname(os.path.realpath(__file__))
    #curDir = '.' + os.path.sep + 'faceRecognition'
os.chdir(curDir)
embeddingModel = load_model('facenet_keras.h5')

create_account_flag = False
login_flag = False
user_id = 0

def on_connect(client, userdata, flag, rc):
    print("Connect with result code:"+ str(rc))
    client.subscribe('login')
    client.subscribe('createAccount/start')
    client.subscribe('createAccount/image')
count= 0
def on_message(client, userdata, msg):
    global count
    #command = msg.payload.decode("utf-8")
   # print("receiving ", msg.topic, " ", str(msg.payload))
    if(msg.topic == 'login'):  
        count = (count +1)%10
       # print('imagelist 받아오기')
        f = open('face' +  os.sep + 'login' + os.sep + 'user' + os.sep + str(count) +'.jpg','wb')
        f.write(msg.payload)
        f.close()
        print('image received')
        if not (count):
             global login_flag
             login_flag = True

    # 받아온 user_id로 폴더 생성
    if(msg.topic == 'createAccount/start'):
        global user_id
        user_id = int(msg.payload)
        print('user_id : ' +  str(user_id))
        if not (user_id == 0):
            dir_name = 'face' + os.sep + 'train' + os.sep + str(user_id)
            #폴더가 없다면 만들고 있으면 안만들기
            if not (os.path.exists(dir_name)):
                os.mkdir(dir_name)
                print(dir_name + '폴더 생성')

    if(msg.topic == 'createAccount/image'):
        count = (count +1)%20
        print('user 아이디 : ' + str(user_id) + ', 사진 받아오기')
        path = 'face' + os.sep + 'train' + os.sep + str(user_id)
        #폴더 생성
        if (os.path.exists(path)):
            f = open(path +  os.sep + str(count) +'.jpg','wb')
            f.write(msg.payload)
            f.close()
            if not (count):
                global create_account_flag
                create_account_flag = True
        

broker_ip = '192.168.137.14' # 현재 이 컴퓨터를 브로커로 설정

#broker_ip = 'localhost'
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

stopFlag = False
while True :
    if (login_flag):
        print('while - login')
        loginCheck = login(embeddingModel)
        client.publish('loginCheck', loginCheck)
       # print("sending %s" % loginCheck)
        login_flag = False

    if (create_account_flag):
        print('while - createAccount')
        # 1은 pi 에서 받아온 유저아이디
        check = createAccoount(embeddingModel, '1')
        client.publish('createAccount/check', check)
        print("sending %s" % check)
        create_account_flag = False
    if (stopFlag):
        break
   
print('끝내기')
client.loop_stop()
client.disconnect()
