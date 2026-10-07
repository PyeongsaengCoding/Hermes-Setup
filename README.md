# Hermes-Setup

macOS에서 Hermes Desktop, OMH, 사용량 플러그인, 스킬과 브라우저 작업 환경을 구성한다. 계정·인증·대화·브라우저 데이터는 포함하지 않는다.

## 설치 요청

Hermes가 아직 없으면 로컬 파일과 명령을 사용할 수 있는 AI에 다음 요청을 보낸다.

> https://github.com/PyeongsaengCoding/Hermes-Setup 을 `~/Downloads/Hermes-Setup`에 받아 내 Mac에 구성해줘. Hermes Desktop, OMH, 사용량 플러그인과 설치 목록의 스킬을 준비하고, Aside에 내가 선택한 브라우저 프로필을 가져와줘. 연결한 계정으로 모델·추론·fallback 모두 OMH 기본 옵션을 사용해줘. 기존 설정을 보존하고 로그인·권한만 나에게 요청해줘. 실제 위임, 사용량 조회, 브라우저 작업과 포커스 보존을 확인한 뒤 완료·미완료만 알려줘.

이 저장소는 설치 가이드와 스킬 설치 도구다. 로그인·프로필 가져오기·브라우저 연결까지 무인으로 끝내는 설치기는 아니다.

## 문서

- [설치 목록](INSTALL-LIST.md): 플러그인·스킬·추가 도구와 설치 경로를 한 표로 정리
- [설치](INSTALL_FOR_AGENTS.md): Hermes 없는 상태부터 시작
- [모델 라우팅](docs/model-routing.md): OMH 기본 모델·추론·fallback
- [브라우저](docs/browsers.md): Aside·Chrome·Edge·Safari 연결과 프로필 가져오기
- [검증 상태](docs/verification.md): 확인한 결과와 남은 검사

스킬은 작업 방법을 가르치는 문서와 보조 파일이다. `AGENTS.md`는 프로젝트 규칙이다. 플러그인은 특정 프로그램의 확장이다. 여기의 `provider-usage`는 Hermes용이므로 Codex나 Claude Code에 그대로 설치하지 않는다. 외부 CLI·MCP는 지원하는 다른 프로그램에서도 사용할 수 있다.

## 유지관리

사용 중인 설정은 `${HERMES_HOME:-~/.hermes}`에 있다. 이 저장소를 지워도 설치한 스킬은 남는다. 스킬 재설치는 같은 파일을 건너뛰고, 다른 기존 파일은 충돌로 보고한다. 업데이트는 설치 시점의 공식 문서와 계정에서 제공하는 모델을 다시 확인한다.
