# KakaoRecovery 🔍

카카오톡에서 만료되어 사라진 파일들을 되찾아드립니다! 🚀

<div align="center">
    <img src="asset/KakaoRecovery.png" alt="KakaoRecovery" width=400>
</div>

## 소개 📝

KakaoRecovery는 카카오톡의 만료된 파일을 `Android\data\com.kakao.talk\contents` 폴더에서 복구해주는 무료 오픈소스 도구입니다.

> 유튜브 가이드 -> https://www.youtube.com/watch?v=m23KHWat6u8

## 사용 방법 🎯

1. [GitHub 릴리즈 페이지](https://github.com/tionlab/KakaoRecovery/releases/latest)에서 KakaoRecovery.zip 최신버전(v0.0.2) 다운로드 및 압축해제
2. KakaoRecovery 실행
3. '원본 contents 폴더' 경로 지정
4. '시작' 버튼 클릭

> result 폴더가 자동으로 생성되고 그 안에 파일들이 복구됩니다.

## 주요 기능 ✨

-   🎯 간단한 GUI 인터페이스
-   📅 날짜별 자동 정렬
-   🗂️ 파일 형식 자동 감지
-   ⏸️ 진행 중 중지 가능
-   📊 실시간 진행률 표시
-   🔔 작업 완료 알림

## 실행 방법 💿

```bash
# 실행 파일 다운로드 (GUI)
최신 릴리즈에서 KakaoRecovery.zip 다운로드 및 압축해제 후 KakaoRecovery 실행

# 또는 소스코드 실행 (No GUI)
pip install tqdm filetype
python main.py

# (GUI)
cd gui
pip install ttkbootstrap filetype playsound
python gui.py
```

## 주의사항 ⚠️

-   원본 contents 폴더 내 파일을 수정하지 마세요.
-   충분한 디스크 공간을 확보하세요.
-   이 프로젝트는 (주)카카오의 게시 중단 요청 또는 삭제 요청이 있을 시 즉시 레포지토리가 삭제됩니다.

## 라이선스 ⚖️

본 소프트웨어는 비상업적 용도로만 사용할 수 있으며, 저작권자의 명시적 동의 없이 상업적 이용은 금지됩니다.  
저작권 정보 및 저작자 이름은 수정 없이 유지되어야 하며, 이와 같은 조건 하에서만 수정 및 배포가 허용됩니다.

이 프로젝트는 GNU Affero General Public License v3.0 with Non-Commercial Clause 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---
