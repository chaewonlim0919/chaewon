# chaewon
README: 자율 주행 시스템

프로젝트 개요

이 프로젝트는 Jetson Xavier NX, 카메라, ESP32 기반의 모터 드라이버를 활용하여 흰색 차선을 따라 자율 주행하는 시스템입니다.
카메라에서 입력된 영상을 처리하여 차선을 감지하고, Pure Pursuit 알고리즘을 적용하여 조향각을 계산한 후,
ESP32를 통해 모터 드라이버를 제어하여 실제 주행을 수행합니다.

<설치 및 설정>

1️⃣ 필수 패키지 설치
Jetson Xavier NX에서 아래 명령어를 실행하여 필요한 패키지를 설치하세요:

sudo apt update && sudo apt upgrade -y
sudo apt install python3-opencv python3-numpy -y
pip3 install pyserial

2️⃣ 하드웨어 연결
카메라는 USB 포트를 통해 연결합니다.
ESP32는 Jetson Xavier NX의 USB 포트에 연결합니다.
모터 드라이버는 ESP32에 연결하여 PWM 신호로 모터를 제어합니다.

1️⃣ 카메라 및 ESP32 연결 확인
먼저 카메라와 ESP32가 정상적으로 인식되는지 확인하세요:

ls /dev/video*    # 카메라가 정상적으로 연결되었는지 확인
ls /dev/ttyUSB*   # ESP32가 정상적으로 인식되는지 확인

2️⃣ 모터 제어 테스트 (hardware.py 실행)
ESP32가 모터 드라이버와 정상적으로 통신하는지 확인하려면 다음 명령을 실행하세요:

from hardware import MotorController
motor = MotorController()
motor.send_command(50, 0)  # 속도 50, 조향 0 (직진 주행)

3️⃣ 카메라 테스트  (camera.py 실행)
카메라가 정상적으로 작동하는지 확인하려면 다음 명령을 실행하세요:

from camera import Camera
cam = Camera()
frame = cam.get_frame()
cv2.imshow("카메라 테스트", frame)
cv2.waitKey(0)

카메라 영상이 정상적으로 표시되면 준비가 완료된 것입니다.
4️⃣ 전체 시스템 실행 (main.py)
카메라와 ESP32가 정상적으로 연결되었으면, 다음 명령어를 실행하여 시스템을 구동하세요:

python3 main.py

이 스크립트를 실행하면:
카메라에서 영상을 받아와 차선을 감지합니다.
Pure Pursuit 알고리즘을 적용하여 적절한 조향각을 계산합니다.
ESP32로 속도 및 조향각 명령을 전송하여 차량을 주행시킵니다.

<시스템 동작 원리>
1. 차선 감지
OpenCV를 활용하여 흰색 차선을 감지합니다.
2. 투시 변환(Perspective Transform)을 사용하여 차선을 직선화합니다.
Sliding Window 및 다항식 피팅 기법을 적용하여 차선 곡률을 추적합니다.
3. 조향 제어 (Pure Pursuit 알고리즘 적용)
감지된 차선을 바탕으로 차량의 조향각을 계산합니다.
한쪽 차선만 감지될 경우 도로 폭을 고려하여 중앙선을 추정하고 보정합니다.
4. 모터 제어 (ESP32 통신)
UART 통신을 통해 ESP32로 속도 및 조향각 명령을 전송합니다.
ESP32는 이 명령을 모터 드라이버에 전달하여 차량을 주행시킵니다.

<문제 해결 방법>
1. 카메라가 인식되지 않음
>연결 확인 후 ls /dev/video* 명령어 실행
2. ESP32가 응답하지 않음
>ls /dev/ttyUSB* 명령어로 장치 확인 후 재부팅
3. 차선이 올바르게 감지되지 않음
>조명 환경 조정 및 Preprocessor.py 내 필터 설정 확인
4. 차량이 움직이지 않음
>모터 드라이버와 ESP32 간 연결 점검

