#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import yt_dlp

# YouTube 스트림 URL 추출 함수
def get_youtube_stream(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for f in reversed(formats):
            if f.get('vcodec') != 'none' and f.get('url', '').startswith('http'):
                return f['url']
        return info.get('url')

# 쇼츠 영상 링크
youtube_url = "https://www.youtube.com/shorts/w_xq4RebwiY"

print("📡 YouTube 스트림 URL을 가져오는 중...")
try:
    video_stream_url = get_youtube_stream(youtube_url)
    if not video_stream_url:
        raise ValueError("재생 가능한 비디오 스트림 URL을 찾지 못했습니다.")
    print("✅ 스트림 URL 추출 완료")
except Exception as e:
    print(f"❌ YouTube URL 추출 실패: {e}")
    exit()

# MediaPipe 얼굴 감지(Face Detection) 초기화
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(
    model_selection=0,  # 0: 2m 이내 근거리 영상용
    min_detection_confidence=0.5
)

# 비디오 캡처 연결
cap = cv2.VideoCapture(video_stream_url)

if not cap.isOpened():
    print("❌ YouTube 영상을 열 수 없습니다.")
    exit()

print("📷 YouTube 얼굴 인식 시작 - ESC를 눌러 종료합니다.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("⚠️ 영상 스트림이 끝났거나 프레임을 읽지 못했습니다.")
        break

    # 글자가 뒤집히지 않도록 cv2.flip(image, 1) 제거
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 얼굴 검출 수행
    results = face_detection.process(image_rgb)

    # 얼굴 바운딩 박스 및 랜드마크(눈, 코, 입, 귀 점) 표시
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

    # 결과 화면 출력
    cv2.imshow("MediaPipe Face Detection (YouTube)", image)

    # ESC(27) 누르면 종료
    if cv2.waitKey(5) & 0xFF == 27:
        print("👋 종료합니다.")
        break

cap.release()
cv2.destroyAllWindows()