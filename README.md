# 🌸 MediaPipe 예제 모음

Google MediaPipe 라이브러리를 활용한 컴퓨터 비전 실습 프로젝트입니다.

## 📌 포함된 파일 및 기능
- **`hand_detector.py`**: 동영상 파일 기반 실시간 손 및 손가락 관절 랜드마크 인식
- **`face_detector.py`**: 동영상 파일 기반 얼굴 위치(바운딩 박스) 및 주요 랜드마크 감지
- **`hand_detector_youtube.py`**: YouTube 온라인 스트리밍 영상을 입력으로 활용한 실시간 얼굴 인식
- **`selfie_segmentation.py`**: 인물과 배경을 분리하고 배경에 가우시안 블러(Gaussian Blur) 효과 적용

## 🛠️ 실행 환경 및 설치 방법
- Python 3.12 (가상환경)

```bash
# 가상환경 활성화 후 패키지 설치
pip install -r requirements.txt