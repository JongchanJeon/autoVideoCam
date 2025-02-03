# autoVideoCam2
 쓰레드를 나눠 모션인식이 된 캠을 영상(mp4), 사진(jpg)로 인코딩 하여 S3에 저장
1. **프로젝트 소개**
관람객들이 전시를 즐기며 방해받지 않고, **자동화된 모션 인식**을 통해 추억을 저장할 수 있도록 하기 위함.
    
    ![KakaoTalk_20250115_105822215.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/47232d81-ada6-4467-887d-7cff5b6d37e4/37811fb4-5483-4d32-8f70-b06a096d24a7/KakaoTalk_20250115_105822215.png)
    
2. **팀 인원** : 8명(개발 인원 1명)
3. **개발 기간** : 2023.11 ~ 2024.02
4. **기술 스택** : `Python`, `S3`, `mariaDB`, `php`, `Lightsail`
5. **GitHub**
    1. **AI를 사용한 모션 인식 프로젝트 :** https://github.com/JongchanJeon/autoVideoCam
    2. **유저 입력을 처리하는 프론트엔드 프로젝트 :** https://github.com/JongchanJeon/jakly
6. **주요 기능**
    1. opencv-python, 웹캠을 활용한 사람 **자동 모션인식 후 영상 및 사진을 S3에 저장**
    2. 여러 카메라의 구성을 위한 **python 스레딩(threading)** 적용
    3. 유저의 정보를 저장하기 위한 **MariaDB 사용**
    4. php 화면 구성,  API 요청 및 Python 파일 실행 트리거 역할
    5. Lightsail을 이용한 간단한 php 배포
