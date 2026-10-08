# 모델 라우팅

Hermes 내부 위임은 OMH 작업 분류를 따른다. Claude Code·Codex 외부 실행기의 설정과 섞지 않는다. 아래 표는 2026-10-08의 OMH 분류별 후보다. Hermes의 실제 공통 fallback은 별도이며 마지막 모델을 Opus로 변경했다. 작업별 추론은 유지한다. 설치 때 `omh model-chains show --json`과 계정에서 제공하는 모델을 확인한다.

| 하는 일 | OMH 분류 | 모델 라우팅 순서·추론 |
|---|---|---|
| 최고 난도 추론 | `ultrabrain` | `gpt-6-astra` xhigh → `claude-fable-5-1` xhigh → `claude-opus-5-5` xhigh |
| 심층 분석 | `deep` | `gpt-6.1-sol` high → `claude-fable-5-1` high → `claude-opus-5-5` high → `deepseek-flash` high (추가 제공자 필요) |
| 시스템 설계 | `architect` | `claude-fable-5-1` xhigh → `gpt-6-astra` xhigh → `claude-opus-5-5` xhigh → `kimi-k3` xhigh (추가 제공자 필요) |
| 고난도 일반 작업 | `unspecified-high` | `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) |
| 저난도 일반 작업 | `unspecified-low` | `claude-opus-5-5` low → `glm-5.3` low (추가 제공자 필요) → `deepseek-flash` low (추가 제공자 필요) |
| 짧은 확인·수정 | `quick` | `gpt-6-luna` low → `claude-fable-5-1` low → `claude-opus-5-5` low → `gpt-6-astra` low → `glm-5.3-flash` low (추가 제공자 필요) → `kimi-k3` low (추가 제공자 필요) |
| 글·문서 | `writing` | `kimi-k3` medium (추가 제공자 필요) → `qwen3-coder` medium (추가 제공자 필요) → `gemini-3.1-pro` medium (추가 제공자 필요) |
| 화면·프론트엔드 | `visual-engineering` | `claude-fable-5-1` high → `claude-opus-5-5` high → `gpt-6-astra` high → `kimi-k3` high (추가 제공자 필요) |
| 창의적 작업 | `artistry` | `claude-fable-5-1` high → `claude-opus-5-5` high → `gpt-6-astra` high → `gemini-3.1-pro` high (추가 제공자 필요) → `kimi-k3` high (추가 제공자 필요) |
| 범용 작업 | `capable` | `claude-fable-5-1` medium → `claude-opus-5-5` medium → `claude-sonnet-5-5` medium → `gpt-6-astra` medium → `kimi-k3` medium (추가 제공자 필요) → `glm-5.3` medium (추가 제공자 필요) |
| 단순 정리 | `simple-work` | `gpt-6-luna` low → `claude-fable-5-1` low → `claude-opus-5-5` low → `claude-haiku-4-5` low → `deepseek-flash` low (추가 제공자 필요) |
| 길고 까다로운 작업 | `deep-work` | `claude-fable-5-1` high → `claude-opus-5-5` high → `gpt-6-astra` high |

## 기본 옵션

작업 분류·추론은 OMH 설정을 따른다. 위 표는 사용자 지정 체인이며 OMH 전체의 기본값으로 취급하지 않는다. 화면·창의·범용·긴 고난도 작업 네 분류만 Fable → Opus 우선으로 바꾸고 Astra는 연결된 후보의 마지막에 둔다. 범용 작업의 Sonnet과 미연결 후보는 보존한다. OMH는 연결된 후보를 앞으로 모으므로 미연결 후보는 Astra 뒤에 표시될 수 있다. 추론 수준·다른 분류·현재 대화 모델·외부 Codex·Claude Code 설정은 바꾸지 않는다.

설치된 OMH 원본에서 `ultrabrain`은 Astra xhigh 하나, `deep-work`는 Astra high 하나였다. GPT → Fable → Opus는 이번에 추가했다. Sol은 원래 `deep`의 주 모델이었다(Sol high → DeepSeek high). 이 배정은 OMH의 추천 설정이며 Sol만 수행할 수 있는 작업이라는 뜻은 아니다.

**현재 대화의 전역 fallback은 Opus, 자식 공통 fallback은 Fable → Astra → Sonnet → Opus다.** 네 분류의 후보 변경과 별개로 공통 fallback의 마지막 Opus는 유지한다. GPT 시작 자식도 Fable을 먼저, Opus를 마지막에 둔다. 주 모델과 같은 후보·사용 불가능한 후보는 건너뛴다. Opus가 주 모델인 작업에서 이미 소진된 Opus를 마지막에 다시 호출한다는 뜻은 아니다. `deep`의 Sol high 주 모델 배정은 유지했다. 글·문서의 Luna → Sonnet → Opus는 제안만 했으며 적용하지 않았다.

기본 모델이 사용 가능한데 임의로 교체하지 않는다. 모델별 소진과 GPT 계정 전체 소진을 구분하며, 같은 계정 전체가 소진됐으면 Astra·Sol·Luna끼리 바꿔서 회복된다고 간주하지 않는다. 인증 실패·통신 오류를 한도 소진으로 보고하지 않으며 다른 오류로 전환한 경우 원인을 구분한다. 이 표를 미래의 최신 모델 목록으로 취급하지 않는다.

Kimi는 구독·연결이 확인됐을 때만 사용한다. 미구독 환경에서는 건너뛰지만 후보를 삭제하거나 인증 정보를 바꾸지 않는다. 표의 다른 미연결 제공자도 같다.

로그인 성공, OMH의 후보 목록, Hermes가 실행에 사용하는 `delegation.fallback_providers`는 별개다. Fable만 한도에 도달했어도 계정은 로그인 상태일 수 있다. OMH 후보에 Opus가 있다는 이유만으로 Hermes가 자동으로 Opus를 호출한다고 보고하지 않는다.

```sh
omh model-chains show --json
```

설치 AI는 아래를 한 흐름으로 수행한다.

1. 선택한 프로필의 GPT·Claude 로그인과 모델별 사용 제한 상태를 확인한다. 인증값은 출력하지 않으며 사용 제한 기록을 초기화하지 않는다.
2. 표의 각 분류를 `omh model-chains set`으로 적용한다. 이미 같은 설정이면 변경하지 않는다. 모델마다 해당 분류의 추론 수준을 명시하고 미연결 후보도 보존한다. 연결 상태에 따라 표시 순서가 달라질 수 있으므로 적용 후 다시 읽는다.
3. 아래 명령으로 전역 fallback은 Opus, 공통 자식 fallback은 Fable → Astra → Sonnet → Opus로 맞춘다. GPT 호환 패치도 Opus를 마지막에 둔다. 공통 목록·자식의 실제 목록·분류별 OMH 후보를 구분한다.
4. 아래 호환 패치를 확인·적용한 뒤 통제된 한도 소진 시험에서 양방향 전환과 기존 추론 유지를 검사한다. 실제 계정 한도를 소진시키거나 제한을 해제하지 않는다.
5. 최소 실제 위임을 실행해 응답과 `session_model_usage`의 모델·`billing_provider`·API 호출 수를 대조한다. 준비된 배정, fallback 선언, 실제 호출 성공을 따로 기록한다.

사용 가능한 후보가 없으면 중단 원인을 명시한다. 성공한 fallback을 원래 배정 모델의 실행 성공으로 쓰지 않는다. 모델별 추론을 전역 고정하지 않는다.

```sh
hermes config set fallback_providers '[{"provider":"anthropic","model":"claude-opus-5-5"}]'
hermes config set delegation.fallback_providers '[{"provider":"anthropic","model":"claude-fable-5-1"},{"provider":"openai-codex","model":"gpt-6-astra"},{"provider":"anthropic","model":"claude-sonnet-5-5"},{"provider":"anthropic","model":"claude-opus-5-5"}]'
```

## fallback 순서·추론 보존

검사한 Hermes는 자동 fallback 때 추론을 전역 설정에서 다시 읽어, 작업의 high·xhigh가 medium으로 바뀔 수 있었다. `scripts/configure_delegation_reasoning.py`는 자식에게 이미 배정한 추론을 유지한다. `scripts/configure_gpt_fallback.py`는 GPT 모델·제공자를 지정한 자식에만 Fable을 처음, Opus를 마지막에 둔다. Claude 시작 자식과 공통 설정은 바꾸지 않는다. 기존의 정확한 관리 패치는 새 순서로 업그레이드하고 임의 변경된 패치는 거부한다. 둘 다 소스 호환 패치이며 플러그인이나 스킬이 아니다.

```sh
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트> --apply
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트> --apply
```

실행 중인 Hermes의 import 경로를 확인해 소스 루트를 지정한다. 첫 명령은 미리보기이며, 다른 함수 구조·변경된 관리 구간·심볼릭 링크는 거부한다. 반복 적용은 변경하지 않는다. 실행 중인 프로세스는 재시작 후 반영되므로 소스 수정만으로 현재 세션 적용을 완료했다고 보고하지 않는다. Hermes 업데이트 후에는 호환 여부를 다시 검사한다. 전환 모델이 추론 수준을 지원하지 않으면 오류를 표시하고 수준을 조용히 낮추지 않는다.

## 확인

네 분류의 Fable → Opus 우선, Astra 후순위와 공통 fallback 보존은 [분류별 검증](../project-records/2026-10-08-category-routing.json)을 따른다. 이 기록은 설정 대조이며 실제 모델 전환을 실행한 기록은 아니다. 분류별 OMH 후보 순서가 공통 native fallback 순서까지 바꾼다고 간주하지 않는다.

마지막 Opus 정책은 [최종 fallback 검증](../project-records/2026-10-08-opus-final.json)을 따른다. 아래 이전 시험은 당시 경로의 기록이며 새 경로의 실제 호출 증거가 아니다.

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 실행 모델·provider·응답을 대조한다.
- 오류 시 실제 Hermes fallback과 OMH 후보 순서를 함께 확인한다. 로그인 성공만으로 모델 사용 가능을 확정하지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

2026-10-07 이전 경로에서는 Fable 제한 → Opus 실제 응답을 확인했다. 이 결과는 이번 Astra 우선 경로의 실제 호출 증거가 아니다. 2026-10-08 새 프로세스에서 native fallback을 통제해 Fable → Astra → Opus와 low·medium·high·xhigh 유지를 확인했다. 이 시험의 제공자 클라이언트는 mock이다. 별도 실제 자식은 Fable low로 배정했고 Fable의 `ROUTING_OK` 응답, `billing_provider=anthropic`, API 호출 1회를 확인했다. 실제 한도를 소진시키지 않았으며 이번 실제 호출에서 Astra·Opus 전환은 발생하지 않았다. 기존 Desktop 프로세스는 재시작하지 않았다. [검증 근거](../project-records/2026-10-08-model-routing.json). 개인 `omh-auto-routing` 플러그인은 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)

같은 날 GPT 시작 다섯 분류도 새 프로세스의 native fallback으로 검사했다. 제공자 클라이언트·인증 풀을 mock으로 격리해 GPT → Fable → Opus, 기존 추론 유지, Claude 시작 경로 보존을 확인했다. 실제 GPT 사용 한도 소진 전환은 이 검사에서 실행하지 않았다. [GPT 경로 검증](../project-records/2026-10-08-gpt-fallback.json).

## AI에게 적용 요청

아래는 쉘 명령이 아니라 AI 채팅에 붙여 넣는 요청이다.

```text
https://github.com/PyeongsaengCoding/Hermes-Setup 의 main에서 docs/model-routing.md와 routing-snapshot.json을 읽고, 내 현재 Hermes 프로필의 OMH 분류별 모델 순서·추론과 Hermes 전역·자식 공통 fallback을 GitHub 기준으로 맞춰줘. 분류별 후보와 공통 fallback은 구분하고, 공통 fallback의 마지막 Opus를 유지해줘. 로그인·구독·미연결 후보와 다른 프로필은 임의로 변경하지 말고, 필요한 호환 패치까지 확인·적용한 뒤 설정 대조와 실제 동작 검증을 구분해서 결과를 알려줘.
```

## 업데이트

```sh
hermes update --check
hermes update --backup
omh update --dry-run --no-omh-tui
omh update --no-omh-tui
```

`--no-omh-tui`는 OMH 업데이트 때 기존 화면·스킨을 유지한다. 업데이트 후 fallback 설정과 OMH 후보를 다시 읽고 소스 호환 패치 두 개를 미리보기·검증한다. 호환될 때만 적용한 뒤 Desktop을 재시작한다. 업데이트 명령 성공만으로 커스텀 라우팅 보존을 완료했다고 보고하지 않는다.
