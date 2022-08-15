from venv import create
import cv2
import sys
import paho.mqtt.client as mqtt
capture_on = False
createImageFalg = False
def on_connect(client, userdata, flag, rc):
    print("Connect with result code:"+ str(rc))
    client.subscribe('capture')


def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print("topic : " + msg.topic) 
    print("payload : " + str(message))

    #미러앱에서 사진보내기 클릭하면 해당 토픽의 메시지가 발행
    #사진 찍어서 바이트코드로 이미지 정보 보내주기
    if(msg.topic == 'capture'):
        global createImageFalg
        createImageFalg = True
       

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정
print('broker_ip : ' + broker_ip)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883)
client.loop_start()


def on_mouse(event, x, y, flags, param):
     if event == cv2.EVENT_LBUTTONDOWN:
         global capture_on
         capture_on = True

def createImage():
    # 노트북 웹캠에서 받아오는 영상을 저장하기
    global capture_on
    # 기본 카메라 객체 생성
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_mouse)
    # 열렸는지 확인
    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    # 웹캠의 속성 값을 받아오기
    # 정수 형태로 변환하기 위해 round
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적

    # fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')

    # 1프레임과 다음 프레임 사이의 간격 설정
    delay = round(1000/fps)

    # 웹캠으로 찰영한 영상을 저장하기
    # cv2.VideoWriter 객체 생성, 기존에 받아온 속성값 입력
    out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

    # 제대로 열렸는지 확인
    if not out.isOpened():
        print('File open failed!')
        cap.release()
        sys.exit()
    # 프레임을 받아와서 저장하기
    while True:                 # 무한 루프
        ret, frame = cap.read() # 카메라의 ret, frame 값 받아오기

        if not ret:             #ret이 False면 중지
            break
        #edge = cv2.Canny(frame, 50, 150) # 윤곽선

        # 윤곽선은 그레이스케일 영상이므로 저장이 안된다. 컬러 영상으로 변경
    # edge_color = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        #out.write(frame) # 영상 데이터만 저장. 소리는 X

        cv2.imshow('frame', frame)
    # cv2.imshow('inversed', inversed)
    #마우스 클릭하면 사진 찍힘
        if(capture_on):
            file_name_path =  'test' + '.jpg'
            #크롭된 이미지 저장
            cv2.imwrite('media' + '/'+file_name_path, frame)
            capture_on = False
            # 저장한 파일이름을 보냄
            client.publish('capture/byteFile','media/' +file_name_path)
            #sendByteImage(file_name_path)
            break
        if cv2.waitKey(delay) == 27: # esc를 누르면 강제 종료
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def sendByteImage(file_name_path):
    #저장된 이미지를 바이트 코드로
    #바로 mqtt로 보내기 미러js에게
    #sender, receiver를 여기서 알수 없으니깐 js에서 합쳐서 서버에게 보냄
    byteArr = list()
    f = open('media/' +file_name_path,"rb")
    filecontent = f.read()
    #byteArr.append(bytearray(filecontent))
   # byteFile = bytes(filecontent)
   # print(byteFile)
    


stopFlag = False
while True :
    if(createImageFalg):
        createImage()
        #stopFlag = True
        createImageFalg = False
    if (stopFlag):
        break
   
print('끝내기')
client.loop_stop()
client.disconnect()