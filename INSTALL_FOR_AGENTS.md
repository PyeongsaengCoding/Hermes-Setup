# 설치

설치 대상은 **Apple Silicon(M 시리즈, ARM64) 맥북**이다. Intel Mac과 다른 OS는 이 안내의 설치 대상이 아니다. 기존 환경에서는 먼저 설치·프로필·로그인을 확인하고 완료된 단계를 반복하지 않는다.

## 1. Hermes와 계정

[공식 설치 안내](https://hermes-agent.nousresearch.com/docs/getting-started/installation)를 읽는다. Desktop 설치판을 사용하거나 공식 소스 설치기로 CLI를 준비한다.

```sh
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes desktop
hermes doctor
```

사용자가 GPT·Claude 계정에 직접 로그인한다. `hermes auth`에서 연결하고 사용 가능한 모델을 확인한다. 인증 파일과 개인 default 프로필은 로컬에 두고 Git 저장소에 넣지 않는다. 새 작업 프로필이 필요하면 `hermes profile create <이름>`을 사용한다.

## Desktop UI 크기

[UI 크기 안내](docs/desktop-ui.md)에 따라 기존 ChatGPT·Claude 앱을 기준으로 창·글자·UI 크기를 맞춘다. 두 앱의 크기가 다르면 기준 앱을 확인하고, 둘 다 없으면 현재 설정이나 새 설치 기본값을 유지한다.

## 2. 스킬

설치할 목록은 [한 표](INSTALL-LIST.md)에 있다. 공식 스킬은 `manifest.json`의 고정 원본에서, 커스텀 스킬은 `skills/`의 일반화된 버전에서 가져온다. 실행 코드와 참고자료도 함께 설치한다.

```sh
python3 scripts/install_skills.py
python3 scripts/install_skills.py --apply
```

첫 명령은 미리보기이며 적용은 없는 스킬만 추가한다. 외부 도구·서비스 권한은 필요한 작업을 사용할 때 준비한다. Python 라이브러리는 프로젝트 `.venv/`, CLI는 패키지 관리자의 위치에 두고 Hermes 런타임에 임의로 pip 설치하지 않는다.

## 전역 규칙

[전역 규칙](docs/global-rules.md)에 따라 선택한 프로필의 `SOUL.md`에 Aside 직접 조작과 문서 전달 시 폴더 카드 제공·앱 자동 실행 금지 규칙을 적용한다.

```sh
python3 scripts/install_global_rules.py
python3 scripts/install_global_rules.py --apply
```

기본 대상은 `${HERMES_HOME:-$HOME/.hermes}`이며 다른 프로필은 `--home`으로 지정한다. 미리보기에서 충돌이 없을 때 적용한다.

## 3. OMH

[공식 INSTALL_FOR_AGENTS.md](https://github.com/rlaope/oh-my-hermes/blob/main/INSTALL_FOR_AGENTS.md)를 읽고 설치할 commit을 고정한다. 설치기와 안내를 같은 commit으로 사용한다. 공식 절차로 설치·setup하고 연결한 GPT·Claude 제공자를 반영한다.

```sh
omh setup
omh doctor
omh model-chains show
```

[모델 안내](docs/model-routing.md)에 따라 기본은 Claude 넉넉형을 적용하고, 사용자가 지정하면 GPT(코덱스) 넉넉형을 적용한다. 필요한 호환 패치도 확인한다. 최종 라우팅은 선택한 프리셋을 기준으로 맞춘다. 개인 실험용 라우팅 플러그인은 설치 대상이 아니다.

## 4. 사용량 플러그인

`provider-usage`는 필수다. 설치본 기준 v0.2.0, Hermes >=0.21.0.

```sh
hermes plugins install PhoeniXAbhisheK/hermes-plugin-provider-usage --ref 753dfbd35c9ed8fec3127ce48e5521d986d3aabe --enable
```

이미 설치되어 있으면 버전과 CLI·Desktop 활성 상태를 확인한다. [원본 안내](https://github.com/PhoeniXAbhisheK/hermes-plugin-provider-usage).

[표시 제한 안내](docs/provider-usage.md)에 따라 GPT·Claude만 보이도록 표시 어댑터를 적용한다.

```sh
python3 scripts/configure_provider_usage.py
python3 scripts/configure_provider_usage.py --apply
```

## 5. 브라우저

[브라우저 안내](docs/browsers.md)에 따라 Aside를 설치하고 선택한 프로필을 가져와 Hermes의 `repl` 직접 조작을 연결한다. 자체 AI 위임 금지와 프로젝트별 프로필 경계는 [배포 규칙](templates/aside-browser.md)을 따른다.

## 보존과 완료 기준

선택한 프로필의 설치·라우팅·UI 설정을 적용하며, 기존 파일과 충돌하면 차이를 확인한 뒤 처리한다. 다른 프로필·설치 대상 외의 설정·기존 브라우저 데이터와 사용자 포커스·입력 대상·커서를 보존한다. 로그인·OS 권한은 사용자가 처리한다. 완료된 단계부터 이어간다.

설치 확인 항목:

- Desktop 질문 응답, 연결한 제공자의 실제 자식 모델·provider·응답, 라우팅 문서의 fallback·추론 검증.
- 새 Hermes 세션의 전역 규칙 로딩과 문서 전달 시 실제 폴더 카드 제공·앱 미실행.
- 사용량 조회·리셋 시간·새로고침과 상태바·툴팁·상세 패널·알림의 GPT·Claude 표시 제한.
- 프로젝트별 Aside 프로필에서 `repl` 이동·입력·결과 읽기, 자체 AI 미호출과 포커스 보존.
- 기준 앱이 있으면 창·글자·UI 크기 비교와 설정 유지. 재실행 확인 전에는 미확인으로 남긴다.
