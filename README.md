# Hermes-Setup

macOS에서 Hermes Desktop, OMH, 사용량 플러그인, 스킬과 브라우저 작업 환경을 구성한다. 계정·인증·대화·브라우저 데이터는 포함하지 않는다.

## 설치 요청

Hermes가 아직 없으면 로컬 파일과 명령을 사용할 수 있는 AI에 다음 요청을 보낸다.

> https://github.com/PyeongsaengCoding/Hermes-Setup 을 `~/Downloads/Hermes-Setup`에 받아 내 Mac에 구성해줘. Hermes Desktop, OMH, 사용량 플러그인과 설치 목록의 스킬을 준비하고, 사용량 플러그인의 상태바·상세 패널·알림에는 GPT와 Claude만 표시해줘. 선택한 Hermes 프로필에 보고서 문체·Humanizer 사용 및 모든 브라우저 작업의 Aside 사용 전역 규칙을 중복 없이 적용해줘. 기존에 쓰던 ChatGPT·Claude 앱이 있으면 그 앱의 창 크기와 글자·UI 크기에 Hermes Desktop을 맞춰줘. Aside에 내가 선택한 브라우저 프로필을 가져와줘. 브라우저 작업의 Aside 프로필은 각 프로젝트 규칙을 따르게 해줘. 모델 라우팅은 docs/model-routing.md의 Claude 넉넉형 또는 GPT(코덱스) 넉넉형 중 내가 지정한 프리셋으로 맞추고, 지정하지 않았다면 선택만 확인해줘. 기존 설정과 내 포커스를 보존하고 로그인·권한, 두 앱의 크기가 다를 때 기준 앱 선택, 기존 규칙 충돌만 나에게 확인해줘. 새 Hermes 세션의 전역 규칙 로딩과 보고서 검토, UI 크기 비교·설정 유지, 실제 위임, 사용량 조회와 GPT·Claude 외 표시 제외, Aside 브라우저 작업과 포커스 보존을 확인한 뒤 완료·미완료만 알려줘.

라우팅은 [모델 안내](docs/model-routing.md)의 **Claude 넉넉형** 또는 **GPT(코덱스) 넉넉형**을 지정한다. 위 설치 요청의 모델 설정에는 선택한 프리셋을 사용하며 OMH 원본 그대로로 초기화하지 않는다. 이미 설치했다면 모델 안내의 버전별 AI 요청문으로 라우팅만 전환한다. 두 버전 모두 공통 fallback의 마지막은 Opus다.

이 저장소는 설치 가이드와 스킬·전역 문체 규칙 설치 도구다. 위 문장은 AI에 복사해 보내는 설치 요청문이며 단일 셸 명령이 아니다. 로그인·프로필 가져오기·브라우저 연결까지 무인으로 끝내는 설치기는 아니다.

## 문서

- [설치 목록](INSTALL-LIST.md): 플러그인·스킬·추가 도구와 설치 경로를 한 표로 정리
- [설치](INSTALL_FOR_AGENTS.md): Hermes 없는 상태부터 시작
- [모델 라우팅](docs/model-routing.md): Claude 넉넉형 / GPT(코덱스) 넉넉형, 버전별 AI 요청문·CLI 전환 명령
- [전역 규칙](docs/global-rules.md): 보고서 문체와 Aside 브라우저 사용을 선택한 프로필의 SOUL.md에 중복 없이 적용
- [Desktop UI 크기](docs/desktop-ui.md): 기존 ChatGPT·Claude 앱 기준으로 창·글자·UI 배율 맞춤
- [사용량 표시 제한](docs/provider-usage.md): GPT·Claude만 상태바·패널·알림에 표시
- [브라우저](docs/browsers.md): Aside·Chrome·Edge·Safari 연결과 프로필 가져오기
- [검증 상태](docs/verification.md): 확인한 결과와 남은 검사

스킬은 작업 방법을 가르치는 문서와 보조 파일이다. `AGENTS.md`는 프로젝트 규칙이다. 플러그인은 특정 프로그램의 확장이다. 여기의 `provider-usage`는 Hermes용이므로 Codex나 Claude Code에 그대로 설치하지 않는다. 외부 CLI·MCP는 지원하는 다른 프로그램에서도 사용할 수 있다.

## 유지관리

사용 중인 설정은 `${HERMES_HOME:-~/.hermes}`에 있다. 이 저장소를 지워도 설치한 스킬은 남는다. 스킬 재설치는 같은 파일을 건너뛰고, 다른 기존 파일은 충돌로 보고한다. 업데이트는 설치 시점의 공식 문서와 계정에서 제공하는 모델을 다시 확인한다.
