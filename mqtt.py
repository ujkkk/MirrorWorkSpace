from re import T
import paho.mqtt.client as mqtt
from crop import createCropImage
import os
from keras.models import load_model
import byteList
global client

curDir = os.path.dirname(os.path.realpath(__file__))
    #curDir = '.' + os.path.sep + 'faceRecognition'
os.chdir(curDir)

new_account_flag = False
login_flag = False
loginCamera_flag = False
def on_connect(client, userdata, flag, rc):
	print("Connect with result code:"+ str(rc))
	client.subscribe('loginCamera')

def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    print("receiving ", msg.topic, " ", str(msg.payload))
    if(msg.topic == 'loginCamera'):
        global loginCamera_flag
        loginCamera_flag = True
       

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정
print('broker_ip : ' + broker_ip)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883)
client.loop_start()

stopFlag = False
while True :
    if (loginCamera_flag):
        print('while - loginCamera')
       # curDir = os.path.dirname(os.path.realpath(__file__))
        #os.chdir(curDir)
    # 카메라로 사진 찍어서 얼굴부분만 크롭해서 저장
        dir_name1 = os.path.join('face','login')
        dir_name2 = os.path.join('face','login','user')
        createCropImage('user',  dir_name1, 10)
        # 사진 넘겨주기
        imagelist = byteList.load_image(dir_name2)
        for i in range(10) :
            pp = imagelist.pop()
            print("sending %s" % pp)
            client.publish('login', pp)
            print("sending %s" % 'login')
        loginCamera_flag = False
    if (stopFlag):
        break
   
print('끝내기')
client.loop_stop()
client.disconnect()
