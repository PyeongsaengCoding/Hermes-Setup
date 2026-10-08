# 문서 정리 전 검증 기록

기존 문서의 과거 검증 설명을 보존한다. 현재 설치 기준과 확인 범위는 [검증 상태](../docs/verification.md)를 따른다. 아래 내용은 당시 기록이며 이번 문서 정리에서 다시 실행한 결과가 아니다. 이동한 문서의 상대 링크만 새 위치에 맞췄다.

## 기존 검증 상태 문서

# 검증 상태

2026-10-07 기준. 이 저장소 공개와 새 컴퓨터의 전체 설치 성공은 별개다.

## 확인한 환경

- Hermes CLI가 실행되며 `provider-usage`가 활성 목록에 있다.
- 비-OMH 스킬 61개를 원본과 대조했다. 공식 58개·커스텀 3개다.
- `omh-auto-routing`은 설치되어 있으나 비활성이다.
- 개인 Sol 최종 fallback과 모델별 Medium 고정을 제거했다. OMH 분류별 체인은 모두 기본값이다.
- cua-driver 진단에서 접근성·화면 권한과 연결을 확인했다.

## 저장소 검사

문서·경로·설치표 검사를 통과했다. 설치 도구 테스트 9개가 통과했고, 공식 고정 원본과 일반화한 커스텀 스킬을 격리 홈에 실제로 설치했다. 미리보기는 파일을 쓰지 않았으며, 첫 적용은 61개 추가, 반복 적용은 61개 변경 없음이었다. 실행 중인 Hermes 설정은 변경하지 않았다.

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

## 전역 문체 규칙 추가 검증 — 과거 기록

보고서 규칙의 배포 원본과 `SOUL.md` 추가 도구를 마련했다. 격리 홈에서 미리보기·첫 적용·반복 적용·기존 내용 보존·충돌 중단·프로필 홈 선택을 검사했다. 현재 기본 프로필의 읽기 전용 미리보기는 같은 규칙이 이미 있어 `unchanged`였다. 실제 사용 중인 `SOUL.md`는 수정하지 않았다. 새 프로필에서 모델이 Humanizer를 로드해 보고서를 검토하는 흐름은 아직 별도로 실행하지 않았다.

현재 설치기는 보고서 규칙을 새로 주입하지 않고 사용자 의도·정정 반영과 Aside 전역 규칙을 설치한다. 기존 SOUL.md의 보고서 내용은 자동 삭제하지 않는다. 위 문단은 이전 배포의 검증 기록이며 현재 설치 기능을 뜻하지 않는다.

## 사용자 의도·정정 반영 규칙 — 2026-10-08

배포 원본과 현재 기본 프로필의 SOUL.md에 동일한 규칙을 추가했다. 설치기의 중복 방지·기존 내용 보존·충돌 시 쓰기 중단과 전체 단위시험, 저장소 문서 검사를 통과했다. 새 세션 로딩과 실제 정정 상황의 행동 변화는 아직 미검증이다. [적용 결과와 근거](../reports/2026-10-08-user-intent.md)에 확인 범위를 정리했다.

## Desktop UI 맞춤 안내

기존 ChatGPT·Claude 앱을 기준으로 창 크기·UI 배율·채팅 글자 크기를 맞추는 절차를 설치 요청문·설치 목록·설치 단계·완료 기준에 추가했다. 기준 선택과 포커스 보존, 앱 없음·권한 부족 처리 기준은 [UI 안내](../docs/desktop-ui.md)에 있다. 이번 변경은 설치 AI의 수행 기준이며, 실제 앱 크기 조정과 재실행 후 설정 유지 검증은 수행하지 않았다.

## 사용량 표시 제한 검증

[표시 어댑터](../docs/provider-usage.md)를 설치 원본과 Desktop 복사본에 적용하고 파일을 다시 읽어 일치 여부와 JavaScript 구문을 확인했다. 반복 미리보기와 적용은 `unchanged`로 처리한다. 저장소 테스트 28개 중 표시 어댑터 테스트는 9개다.

설치된 실제 플러그인 모듈을 React 렌더러로 실행해 상태바·툴팁·상세 패널에 GPT·Claude만 남는지 검사했다. 합성 입력을 사용한 알림 검사에서도 두 제공자의 알림만 생성됐다. 원본 플러그인의 React key 경고는 남아 있으며 관련 없는 마크업은 변경하지 않았다. 실제 Desktop 화면에서는 상태바의 `gpt`·`claude` 표시를 확인했다. 상세 팝업·실제 한도 알림·앱 재실행 후 유지는 아직 실제 화면에서 검증하지 않았다. 인증과 원본 백엔드 조회 기능은 수정하지 않았다.

검증 근거: [실행 결과](../project-records/2026-10-07-provider-usage-filter.json). 개인 대화가 포함된 화면 캡처는 저장소에 넣지 않았다.

## 남은 실제 검사

Hermes 없는 새 Mac 전체 설치, 새 사용자 로그인, GPT·Claude 실제 위임과 OMH 기본 fallback, 사용량 패널 새로고침, Aside 전체 프로필 가져오기, 브라우저 입력·동시 작업·포커스 보존, 기존 앱 기준 UI 크기 비교와 설정 유지는 이번 공개 작업에서 새로 확인하지 않았다. 설치 요청을 실행하는 컴퓨터에서 완료 기준을 검사한다.

## 기존 모델 라우팅 변경·검증 기록


최종 후보는 GPT·Claude 계열만 남겼다. 현재 프로필·두 프리셋·호환 스냅샷을 대조했고 기존 순서·추론·공통 fallback은 유지했다. 테스트 49개가 통과했으며 이번 후보 제거에서는 실제 모델 호출을 추가하지 않았다. [GPT·Claude 전용 검증](../project-records/2026-10-08-gpt-claude-only.json).

Kimi·Qwen·Gemini 제거와 글·문서의 Sol/Opus 배정은 [후보 정리 검증](../project-records/2026-10-08-routing-candidate-cleanup.json)을 따른다. 현재 default 프로필의 GPT형 열두 분류 대조와 테스트 49개가 통과했다. 글·문서에 Sol medium을 배정한 실제 자식은 Sol의 `ROUTING_OK` 응답과 `openai-codex` API 호출 1회를 확인했다. 실제 한도 소진이나 Opus 전환은 실행하지 않았고, 실제 추론 수준은 사용량 기록에 없어 배정값과 구분한다.

두 프리셋의 현재 차이는 Astra 위치가 다른 네 분류와 글·문서의 Opus/Sol 순서다. 추론·남은 후보·공통 fallback은 같다. [이전 프리셋 검증](../project-records/2026-10-08-routing-presets.json)은 글·문서 변경 전 네 분류 전환과 공통 fallback 통제 시험 기록이며, 당시 실제 제공자 호출이나 한도 소진은 실행하지 않았다.

네 분류의 Fable → Opus 우선, Astra 후순위와 공통 fallback 보존은 [분류별 검증](../project-records/2026-10-08-category-routing.json)을 따른다. 이 기록은 설정 대조이며 실제 모델 전환을 실행한 기록은 아니다. 분류별 OMH 후보 순서가 공통 native fallback 순서까지 바꾼다고 간주하지 않는다.

마지막 Opus 정책은 [최종 fallback 검증](../project-records/2026-10-08-opus-final.json)을 따른다. 아래 이전 시험은 당시 경로의 기록이며 새 경로의 실제 호출 증거가 아니다.

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 실행 모델·provider·응답을 대조한다.
- 오류 시 실제 Hermes fallback과 OMH 후보 순서를 함께 확인한다. 로그인 성공만으로 모델 사용 가능을 확정하지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

2026-10-07 이전 경로에서는 Fable 제한 → Opus 실제 응답을 확인했다. 이 결과는 이번 Astra 우선 경로의 실제 호출 증거가 아니다. 2026-10-08 새 프로세스에서 native fallback을 통제해 Fable → Astra → Opus와 low·medium·high·xhigh 유지를 확인했다. 이 시험의 제공자 클라이언트는 mock이다. 별도 실제 자식은 Fable low로 배정했고 Fable의 `ROUTING_OK` 응답, `billing_provider=anthropic`, API 호출 1회를 확인했다. 실제 한도를 소진시키지 않았으며 이번 실제 호출에서 Astra·Opus 전환은 발생하지 않았다. 기존 Desktop 프로세스는 재시작하지 않았다. [검증 근거](../project-records/2026-10-08-model-routing.json). 개인 `omh-auto-routing` 플러그인은 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)

같은 날 GPT 시작 다섯 분류도 새 프로세스의 native fallback으로 검사했다. 제공자 클라이언트·인증 풀을 mock으로 격리해 GPT → Fable → Opus, 기존 추론 유지, Claude 시작 경로 보존을 확인했다. 실제 GPT 사용 한도 소진 전환은 이 검사에서 실행하지 않았다. [GPT 경로 검증](../project-records/2026-10-08-gpt-fallback.json).
