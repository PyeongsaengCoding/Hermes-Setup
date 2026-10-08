# Hermes-Setup

이 저장소는 macOS용 Hermes 설치 가이드와 설치 원본이다.

- 사용자 문서는 짧은 한국어로 쓴다. 설치 목록은 `INSTALL-LIST.md` 한 표로 관리한다.
- 경로는 `~`, `$HERMES_HOME`, 프로젝트 상대경로로 쓴다. 개인 계정·절대 홈 경로·인증·대화·브라우저 데이터를 넣지 않는다.
- 스킬, 프로젝트 지침, 플러그인, 외부 도구를 구별한다.
- Hermes 작업은 Hermes/OMH 설정을 따른다. 외부 Codex·Claude Code를 실행할 때만 해당 실행기의 모델 정책을 따른다.
- 기존 설치·프로필·스킬을 임의로 덮어쓰지 않는다. 로그인과 OS 권한은 사용자가 직접 승인한다.
- 설치 코드 변경 후 `python3 scripts/check.py`와 `python3 -m unittest discover -s tests -v`를 실행한다.
