# 설치

지원 기준은 Apple Silicon macOS다. 현재 공식 Desktop 설치판은 Intel Mac을 지원하지 않는다. 다른 OS·아키텍처에서는 공식 지원 여부와 경로를 확인한 뒤 별도로 검증한다. 기존 환경에서는 먼저 설치·프로필·로그인을 확인하고 완료된 단계를 반복하지 않는다.

## 1. Hermes와 계정

[공식 설치 안내](https://hermes-agent.nousresearch.com/docs/getting-started/installation)를 읽는다. Desktop 설치판을 사용하거나 공식 소스 설치기로 CLI를 준비한다.

```sh
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes desktop
hermes doctor
```

사용자가 GPT·Claude 계정에 직접 로그인한다. `hermes auth`에서 연결하고 사용 가능한 모델을 확인한다. 인증 파일을 저장소에 복사하지 않는다. 새 작업 프로필이 필요하면 `hermes profile create <이름>`을 사용한다. 개인 default 전체를 내보내 공개하지 않는다.

## Desktop UI 크기

Hermes Desktop을 준비한 뒤 [UI 크기 안내](docs/desktop-ui.md)에 따라 기존 ChatGPT·Claude 앱의 창 크기와 글자·UI 배율을 확인해 맞춘다. 이 단계도 설치 요청 한 번에 수행한다. 두 앱의 크기가 다르고 기준이 지정되지 않았으면 주 사용 앱만 확인한다. 기준 앱이 없으면 현재 Hermes 설정이나 새 설치 기본값을 유지한다. 참고 앱은 변경하지 않으며 사용자 포커스·입력 대상·커서를 보존한다.

## 2. 스킬

설치할 목록은 [한 표](INSTALL-LIST.md)에 있다. 공식 스킬은 `manifest.json`의 고정 원본에서, 커스텀 스킬은 `skills/`의 일반화된 버전에서 가져온다. 실행 코드와 참고자료도 함께 설치한다.

```sh
python3 scripts/install_skills.py
python3 scripts/install_skills.py --apply
```

첫 명령은 미리보기다. 실제 적용은 없는 스킬만 추가하며 기존 다른 파일은 덮어쓰지 않는다. 스킬 설치가 외부 CLI·Python 라이브러리·서비스 로그인까지 설치한다는 뜻은 아니다. 필요한 추가 도구는 해당 작업을 사용할 때 표와 스킬 원문에 따라 준비한다. Python 라이브러리는 프로젝트 `.venv/`, CLI는 해당 패키지 관리자의 위치에 둔다. Hermes 런타임에 임의로 pip 설치하지 않는다.

Humanizer는 스킬 설치기에 포함된 필수 문장 검토 스킬이다. AI 슬롭 제거용 `omh-ai-slop-cleaner`는 아래 OMH 설치로 준비한다. 둘 다 Hermes에서 실제로 불러올 수 있는지 확인한다. 스킬 설치와 프로젝트별 사용 기준은 별개이며, 문장 검토를 코드 자동 정리로 확대하지 않는다.

## 전역 규칙

스킬을 준비한 뒤 [전역 규칙](docs/global-rules.md)에 따라 선택한 프로필의 `SOUL.md`에 사용자 의도·정정 반영과 Aside 브라우저 직접 조작 규칙을 적용한다.

```sh
python3 scripts/install_global_rules.py
python3 scripts/install_global_rules.py --apply
```

첫 명령은 읽기 전용 미리보기다. 기본 대상은 `${HERMES_HOME:-$HOME/.hermes}`이며 다른 프로필에는 `--home`으로 정확한 홈을 지정한다. 같은 규칙은 건너뛰고 다른 기존 규칙이나 변경된 관리 구간은 충돌로 중단한다. 다른 문체·제품·모델 규칙은 덮어쓰지 않는다.

## 3. OMH

[공식 INSTALL_FOR_AGENTS.md](https://github.com/rlaope/oh-my-hermes/blob/main/INSTALL_FOR_AGENTS.md)를 읽고 설치할 commit을 고정한다. 설치기와 안내를 같은 commit으로 사용한다. 공식 절차로 설치·setup하고 연결한 GPT·Claude 제공자를 반영한다.

```sh
omh setup
omh doctor
omh model-chains show
```

라우팅은 **Claude 넉넉형**(`routing-presets/claude-generous.json`) 또는 **GPT(코덱스) 넉넉형**(`routing-presets/gpt-generous.json`)을 선택한다. 지정하지 않았으면 현재 설정을 유지하고 사용자에게 선택을 확인한다. Claude형은 네 분류에서 Fable → Opus 우선, Astra 후순위이며 GPT형은 네 분류의 Astra 순위를 변경 전으로 복원한다. 글·문서는 Claude형 Opus → Sol, GPT형 Sol → Opus이며 둘 다 medium이다. 나머지 일곱 분류와 모든 추론 수준은 같다. 두 버전 모두 전역 fallback은 Opus, 자식 공통 fallback은 Fable → Astra → Sonnet → Opus다. 분류별 후보 변경을 공통 fallback 변경으로 확대하지 않는다. GPT·Claude 계열 외 후보는 모든 분류에서 제거한다. Kimi·Qwen·Gemini·GLM·DeepSeek를 다시 추가하지 않는다. 로그인·계정·제공자 연결은 삭제하지 않는다. OMH 후보와 실제 자식 fallback을 대조하고 순서·추론 호환 패치도 검사한다. 전체 라우팅·버전별 AI 요청문·CLI 전환 명령은 [모델 안내](docs/model-routing.md)를 따른다. 기존 로컬 라우팅 플러그인을 자동 복사하지 않는다.

## 4. 사용량 플러그인

`provider-usage`는 필수다. 설치본 기준 v0.2.0, Hermes >=0.21.0.

```sh
hermes plugins install PhoeniXAbhisheK/hermes-plugin-provider-usage --ref 753dfbd35c9ed8fec3127ce48e5521d986d3aabe --enable
```

이미 설치되어 있으면 버전·활성 상태를 확인한다. Desktop의 플러그인 활성 상태도 확인하고 필요할 때 다시 연다. GPT·Claude 사용량과 리셋 시간, 새로고침이 실제로 응답하는지 검사한다. 빈 카드나 오류를 사용량 0으로 취급하지 않는다. [원본 안내](https://github.com/PhoeniXAbhisheK/hermes-plugin-provider-usage)

[표시 제한 안내](docs/provider-usage.md)에 따라 GPT(`openai-codex`)·Claude(`anthropic`)만 상태바·툴팁·상세 패널·한도 알림에 표시한다. 원본의 눈 버튼만으로는 상세 패널과 알림을 숨기지 못하므로 설치 후 표시 어댑터를 적용한다. 인증·모델·fallback은 변경하지 않는다.

```sh
python3 scripts/configure_provider_usage.py
python3 scripts/configure_provider_usage.py --apply
```

## 5. 브라우저

[브라우저 안내](docs/browsers.md)에 따라 Aside를 설치하고 사용자가 선택한 프로필을 가져온다. Hermes 모델이 MCP `repl` 또는 `aside repl`로 직접 조작하도록 연결한다. Aside 자체 AI 에이전트·`aside exec`·자연어 작업 위임은 사용하지 않고 MCP에서도 해당 위임 도구는 노출하지 않는다. 기존 브라우저나 기본 브라우저 설정을 임의로 바꾸지 않는다. 쿠키·비밀번호·복구키는 복사하거나 공개하지 않는다.

## 완료 기준

- Hermes Desktop에서 실제 질문이 응답한다.
- 기존 ChatGPT·Claude 앱이 있으면 기준 앱과 Hermes의 창·글자·UI 크기를 실제로 비교하고 설정 유지 여부를 확인한다. 기준 앱 없음·권한 부족·재실행 미확인은 적용 완료와 구분한다.
- GPT·Claude 내부 자식의 실제 모델·provider·응답을 확인한다. 연결한 제공자만 검사한다.
- 전역·자식 fallback의 마지막 Opus와 기존 추론 유지를 검사한다. 실제 한도를 소진시키거나 사용 제한을 초기화하지 않는다. 패치는 새 프로세스에서 확인하고 실제 호출의 모델·billing provider도 별도로 확인한다.
- 사용량 패널의 실제 조회·새로고침을 확인하고, GPT·Claude 외 제공자가 상태바·툴팁·상세 패널·알림에 나타나지 않는지 검사한다.
- 프로젝트 규칙의 Aside 프로필로 Hermes가 `repl`을 통해 이동·입력·결과 읽기를 수행하고 원래 앱·키보드 대상·커서가 유지된다. 호출 기록에서 Aside 자체 AI 에이전트·`exec`·자연어 작업 위임이 없음을 확인한다.
- 기존 프로필·스킬·브라우저 데이터가 보존된다.
- Humanizer와 `omh-ai-slop-cleaner`를 Hermes에서 실제로 불러올 수 있다. 파일 존재와 스킬 로드 확인을 구분한다.
- 새 Hermes 세션에서 선택한 프로필의 `SOUL.md` 규칙 로딩과 Aside repl 직접 조작을 실제로 확인한다. 파일 설치와 실제 적용 확인은 구분한다.

진단·설치 테스트와 위의 실제 사용자 흐름은 따로 기록한다. 로그인이나 OS 권한에서 멈추면 완료한 단계부터 이어간다.
