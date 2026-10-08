# 모델 라우팅

Hermes 내부 위임은 OMH 작업 분류를 따른다. Claude Code·Codex 외부 실행기의 설정과 섞지 않는다. 아래는 2026-10-08 적용한 GPT·Claude 환경의 체인이다. Fable 시작 작업은 Fable → Astra → Opus, GPT 시작 작업은 기존 GPT → Fable → Opus 순서이며 작업별 추론은 유지한다. 설치 때 `omh model-chains show --json`과 계정에서 제공하는 모델을 확인한다.

| 하는 일 | OMH 분류 | 모델 라우팅 순서·추론 |
|---|---|---|
| 최고 난도 추론 | `ultrabrain` | `gpt-6-astra` xhigh → `claude-fable-5-1` xhigh → `claude-opus-5-5` xhigh |
| 심층 분석 | `deep` | `gpt-6.1-sol` high → `claude-fable-5-1` high → `claude-opus-5-5` high → `deepseek-flash` high (추가 제공자 필요) |
| 시스템 설계 | `architect` | `claude-fable-5-1` xhigh → `gpt-6-astra` xhigh → `claude-opus-5-5` xhigh → `kimi-k3` xhigh (추가 제공자 필요) |
| 고난도 일반 작업 | `unspecified-high` | `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) |
| 저난도 일반 작업 | `unspecified-low` | `claude-opus-5-5` low → `glm-5.3` low (추가 제공자 필요) → `deepseek-flash` low (추가 제공자 필요) |
| 짧은 확인·수정 | `quick` | `gpt-6-luna` low → `claude-fable-5-1` low → `claude-opus-5-5` low → `gpt-6-astra` low → `glm-5.3-flash` low (추가 제공자 필요) → `kimi-k3` low (추가 제공자 필요) |
| 글·문서 | `writing` | `kimi-k3` medium (추가 제공자 필요) → `qwen3-coder` medium (추가 제공자 필요) → `gemini-3.1-pro` medium (추가 제공자 필요) |
| 화면·프론트엔드 | `visual-engineering` | `claude-fable-5-1` high → `gpt-6-astra` high → `claude-opus-5-5` high → `kimi-k3` high (추가 제공자 필요) |
| 창의적 작업 | `artistry` | `claude-fable-5-1` high → `gpt-6-astra` high → `claude-opus-5-5` high → `gemini-3.1-pro` high (추가 제공자 필요) → `kimi-k3` high (추가 제공자 필요) |
| 범용 작업 | `capable` | `claude-fable-5-1` medium → `gpt-6-astra` medium → `claude-opus-5-5` medium → `claude-sonnet-5-5` medium → `kimi-k3` medium (추가 제공자 필요) → `glm-5.3` medium (추가 제공자 필요) |
| 단순 정리 | `simple-work` | `gpt-6-luna` low → `claude-fable-5-1` low → `claude-opus-5-5` low → `claude-haiku-4-5` low → `deepseek-flash` low (추가 제공자 필요) |
| 길고 까다로운 작업 | `deep-work` | `gpt-6-astra` high → `claude-fable-5-1` high → `claude-opus-5-5` high |

## 기본 옵션

작업 분류·추론은 OMH 설정을 따른다. 위 표의 교차 제공자 경로는 사용자 지정 체인이며 OMH 전체의 기본값으로 취급하지 않는다. 기존 주 모델과 추론 수준, Opus 기본 배정은 유지한다. 현재 대화 모델과 외부 Codex·Claude Code 설정도 바꾸지 않는다.

설치된 OMH 원본에서 `ultrabrain`은 Astra xhigh 하나, `deep-work`는 Astra high 하나였다. GPT → Fable → Opus는 이번에 추가했다. Sol은 원래 `deep`의 주 모델이었다(Sol high → DeepSeek high). 이 배정은 OMH의 추천 설정이며 Sol만 수행할 수 있는 작업이라는 뜻은 아니다.

**Fable 시작 작업은 Fable → Astra → Opus, GPT 시작 작업은 해당 GPT → Fable → Opus 순서다.** 기본 모델이 사용 가능한데 임의로 교체하지 않는다. 모델별 소진과 GPT 계정 전체 소진을 구분하며, 같은 계정 전체가 소진됐으면 Astra·Sol·Luna끼리 바꿔서 회복된다고 간주하지 않는다. 인증 실패·통신 오류를 한도 소진으로 보고하지 않으며, Hermes가 다른 오류로 fallback한 경우 원인을 구분한다. 모델 ID는 설치 당시 제공자 카탈로그와 실제 응답으로 확인하며 이 표를 미래의 최신 모델 목록으로 취급하지 않는다.

Kimi는 구독·연결이 확인됐을 때만 사용한다. 미구독 환경에서는 건너뛰지만 후보를 삭제하거나 인증 정보를 바꾸지 않는다. 표의 다른 미연결 제공자도 같다.

로그인 성공, OMH의 후보 목록, Hermes가 실행에 사용하는 `delegation.fallback_providers`는 별개다. Fable만 한도에 도달했어도 계정은 로그인 상태일 수 있다. OMH 후보에 Opus가 있다는 이유만으로 Hermes가 자동으로 Opus를 호출한다고 보고하지 않는다.

```sh
omh model-chains show --json
```

설치 AI는 아래를 한 흐름으로 수행한다.

1. 선택한 프로필의 GPT·Claude 로그인과 모델별 사용 제한 상태를 확인한다. 인증값은 출력하지 않으며 사용 제한 기록을 초기화하지 않는다.
2. 표의 Fable 시작 네 분류와 GPT 시작 다섯 분류를 `omh model-chains set`으로 적용한다. 모델마다 해당 분류의 기존 추론 수준을 명시하고, Kimi 등 기존 나머지 후보는 뒤에 보존한다. 다른 분류는 유지한다.
3. `hermes config set delegation.fallback_providers`로 공통 자식 fallback을 Fable → Astra → Opus → 기존 나머지 후보 순서로 맞춘다. 아래 GPT 호환 패치는 GPT 시작 자식에만 Fable → Opus를 앞세운다. 현재 주 모델과 동일한 후보는 Hermes가 건너뛴다. 공통 목록·자식의 실제 목록·분류별 OMH 후보 목록을 구분한다. 현재 대화의 전역 fallback은 별도 범위다.
4. 아래 호환 패치를 확인·적용한 뒤 통제된 한도 소진 시험에서 양방향 전환과 기존 추론 유지를 검사한다. 실제 계정 한도를 소진시키거나 제한을 해제하지 않는다.
5. 최소 실제 위임을 실행해 응답과 `session_model_usage`의 모델·`billing_provider`·API 호출 수를 대조한다. 준비된 배정, fallback 선언, 실제 호출 성공을 따로 기록한다.

사용 가능한 후보가 없으면 중단 원인을 명시한다. 성공한 fallback을 원래 배정 모델의 실행 성공으로 쓰지 않는다. 모델별 추론을 전역 고정하지 않으며 기존 공통 fallback의 Sonnet·Sol은 보존한다.

## fallback 순서·추론 보존

검사한 Hermes는 자동 fallback 때 추론을 전역 설정에서 다시 읽어, 작업의 high·xhigh가 medium으로 바뀔 수 있었다. `scripts/configure_delegation_reasoning.py`는 자식에게 이미 배정한 추론을 유지한다. `scripts/configure_gpt_fallback.py`는 GPT 모델·제공자를 지정한 자식에만 Fable → Opus를 먼저 배정하고, Claude 시작 자식과 공통 설정은 바꾸지 않는다. 둘 다 소스 호환 패치이며 플러그인이나 스킬이 아니다.

```sh
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트> --apply
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트> --apply
```

실행 중인 Hermes의 import 경로를 확인해 소스 루트를 지정한다. 첫 명령은 미리보기이며, 다른 함수 구조·변경된 관리 구간·심볼릭 링크는 거부한다. 반복 적용은 변경하지 않는다. 실행 중인 프로세스는 재시작 후 반영되므로 소스 수정만으로 현재 세션 적용을 완료했다고 보고하지 않는다. Hermes 업데이트 후에는 호환 여부를 다시 검사한다. 전환 모델이 추론 수준을 지원하지 않으면 오류를 표시하고 수준을 조용히 낮추지 않는다.

## 확인

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 실행 모델·provider·응답을 대조한다.
- 오류 시 실제 Hermes fallback과 OMH 후보 순서를 함께 확인한다. 로그인 성공만으로 모델 사용 가능을 확정하지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

2026-10-07 이전 경로에서는 Fable 제한 → Opus 실제 응답을 확인했다. 이 결과는 이번 Astra 우선 경로의 실제 호출 증거가 아니다. 2026-10-08 새 프로세스에서 native fallback을 통제해 Fable → Astra → Opus와 low·medium·high·xhigh 유지를 확인했다. 이 시험의 제공자 클라이언트는 mock이다. 별도 실제 자식은 Fable low로 배정했고 Fable의 `ROUTING_OK` 응답, `billing_provider=anthropic`, API 호출 1회를 확인했다. 실제 한도를 소진시키지 않았으며 이번 실제 호출에서 Astra·Opus 전환은 발생하지 않았다. 기존 Desktop 프로세스는 재시작하지 않았다. [검증 근거](../project-records/2026-10-08-model-routing.json). 개인 `omh-auto-routing` 플러그인은 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)

같은 날 GPT 시작 다섯 분류도 새 프로세스의 native fallback으로 검사했다. 제공자 클라이언트·인증 풀을 mock으로 격리해 GPT → Fable → Opus, 기존 추론 유지, Claude 시작 경로 보존을 확인했다. 실제 GPT 사용 한도 소진 전환은 이 검사에서 실행하지 않았다. [GPT 경로 검증](../project-records/2026-10-08-gpt-fallback.json).
