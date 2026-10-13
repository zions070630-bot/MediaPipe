import cv2
import mediapipe as mp

# MediaPipe 얼굴 감지 모듈 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(
    model_selection=0,  # 0: 근거리(2m 이내), 1: 원거리(5m 이내)
    min_detection_confidence=0.5
)

# 카메라가 없으므로 제공된 face.mp4 동영상 사용
cap = cv2.VideoCapture("face.mp4")

print("📷 Face Detection 시작 - ESC를 눌러 종료합니다.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("⚠️ 프레임을 읽지 못했습니다.")
        break

    # 좌우 반전 및 BGR -> RGB 변환
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 얼굴 검출 수행
    results = face_detection.process(image_rgb)

    # 검출된 얼굴 바운딩 박스 및 주요 특징점 그리기
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

    cv2.imshow("MediaPipe Face Detection", image)

    # ESC 키(27) 누르면 종료
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()