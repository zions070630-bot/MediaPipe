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
        # 프로토콜이 https이고 영상(vcodec != none)인 스트림 주소 탐색
        formats = info.get('formats', [])
        for f in reversed(formats):
            if f.get('vcodec') != 'none' and f.get('url', '').startswith('http'):
                return f['url']
        return info.get('url')

# YouTube 영상 주소 (강의자료 추천 실습 영상)
youtube_url = "https://www.youtube.com/watch?v=udeQhZHx-00"

print("📡 YouTube 스트림 URL을 가져오는 중...")
try:
    video_stream_url = get_youtube_stream(youtube_url)
    if not video_stream_url:
        raise ValueError("재생 가능한 비디오 스트림 URL을 찾지 못했습니다.")
    print("✅ 스트림 URL 추출 완료")
except Exception as e:
    print(f"❌ YouTube URL 추출 실패: {e}")
    exit()

# MediaPipe 손 인식 모듈 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# YouTube 스트림 연결
cap = cv2.VideoCapture(video_stream_url)

if not cap.isOpened():
    print("❌ YouTube 영상을 열 수 없습니다.")
    exit()

print("📷 YouTube 스트림 재생 시작 - ESC를 눌러 종료합니다.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("⚠️ 영상 스트림이 끝났거나 프레임을 읽지 못했습니다.")
        break

    # 좌우 반전 및 BGR -> RGB 변환
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 손 검출 수행
    result = hands.process(image_rgb)

    # 손 랜드마크 표시
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

    # 결과 화면 표시
    cv2.imshow("MediaPipe Hand Detector (YouTube)", image)

    if cv2.waitKey(5) & 0xFF == 27:
        print("👋 종료합니다.")
        break

cap.release()
cv2.destroyAllWindows()