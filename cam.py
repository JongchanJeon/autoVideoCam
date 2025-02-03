import cv2
import os
import mediapipe as mp
import time
import asyncio
from s3 import s3_connection
from rds import getEnteranceUser
from slack import msgSend
def upload_to_s3(file_name, bucket_name, object_name=None):
    """S3 버킷에 파일 업로드"""
    if object_name is None:
        object_name = file_name
    try:
        s3 = s3_connection()
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"{file_name} 업로드 성공")
    except Exception as e:
        print(e)

async def setEntranceTime():
    await time.sleep(5)
    global countEntrance
    countEntrance = -1


def useCamera(camera_index):
    try:
        # Mediapipe Pose 모델 초기화
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        mp_drawing = mp.solutions.drawing_utils

        # 웹캠 캡처 시작
        cap = cv2.VideoCapture(cv2.CAP_DSHOW+camera_index)

        # 해상도 설정 (웹캠 지원 해상도에 맞게 조정)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # 프레임 속도 및 해상도 확인
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        frame_rate = 10  # 웹캠의 실제 프레임 속도에 맞춰 조정

        out = None
        recording = False
        
        # 입장 후 3분만 카운트 
        countEntrance = 0

        # 영상 사진 저장 여부 0 이면 저장 -1 이면 저장 안함 
        entranceSave = -1

        count = 0 # 저장될 영상 숫자 카운팅
        photoCount = 0 # 저장될 사진 숫자 카운팅
        last_photo_time = time.time()  
        photo_interval = 5  # 추가된 부분 (10초 간격)
        last_db_query_time = time.time()
        db_query_interval = 10
        print(f"{camera_index}번 카메라가 켜졌습니다.")
        msgSend(f"{camera_index}번 카메라가 켜졌습니다.")
        user = getEnteranceUser()['username']
        msgSend(f"현재 입장된 유저는 : {user}")
        saveUser = user
        while cap.isOpened():
            print(f"entranceSave{entranceSave}")
            print(f"countEntrance{countEntrance}")
            current_time = time.time()
            if current_time - last_db_query_time >= db_query_interval:
                user = getEnteranceUser()['username']
                if(user != saveUser):
                    count = 0
                    photoCount = 0
                    saveUser = user
                    msgSend(f"현재 입장된 유저는 : {user}")
                    entranceSave = 0
                    countEntrance = 0
                last_db_query_time = current_time

            if(countEntrance > 850 or entranceSave != 0):
                entranceSave = -1
                time.sleep(5)
                countEntrance = 0
                continue
            countEntrance += 1
            if not os.path.exists(user):
                os.makedirs(user)
            success, image = cap.read()
            if not success:
                print("웹캠 읽기 실패.")
                msgSend("웹캠 읽기 실패.")
                break
            # 이미지 처리
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # 포즈 인식
            results = pose.process(image)

            # 이미지에 결과 그리기
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.pose_landmarks:
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                if not recording:
                    try:
                        video_filename = os.path.join(user, f'{user}_{camera_index}_{count}.mp4')
                        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'X264'), frame_rate, (frame_width, frame_height))
                        recording = True
                    
                    except Exception as e:
                        print(e)
            else:
                if recording:
                    out.release()
                    s3 = s3_connection()
                    s3_filename = video_filename.replace("\\", "/")
                    s3.upload_file(video_filename,"jakly",s3_filename)
                    print(f"{video_filename} 업로드 성공")
                    count += 1
                    recording = False
                    
            if recording:
                out.write(image)
                
            # 10초 간격으로 사진 찍기
            if recording:
                current_time = time.time()
                if current_time - last_photo_time >= photo_interval:
                    photo_filename = os.path.join(user, f'{user}_{camera_index}_{photoCount}_photo.jpg')
                    cv2.imwrite(photo_filename, image)
                    upload_to_s3(photo_filename, "jakly", photo_filename.replace("\\", "/"))
                    print(f"{photo_filename} 업로드 성공")
                    last_photo_time = current_time
                    photoCount += 1

            cv2.imshow(f'MediaPipe Pose Camera {camera_index}', image)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        if recording:
            out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(e)
        raise Exception(e)
    

