# 모델 라우팅

Hermes 내부 위임은 OMH 기본 분류를 따른다. Claude Code·Codex 외부 실행기의 설정과 섞지 않는다. 아래는 2026-10-07 확인한 GPT·Claude 연결 환경의 기본 체인이다. 제공자 연결에 따라 순서가 달라질 수 있으며, 설치 때 `omh model-chains show --json`으로 다시 확인한다. 모델 이름은 계정에서 실제 제공하는지 검사한다.

| 하는 일 | OMH 분류 | 모델 라우팅 순서·추론 |
|---|---|---|
| 최고 난도 추론 | `ultrabrain` | `gpt-6-astra` xhigh |
| 심층 분석 | `deep` | `gpt-6.1-sol` high → `deepseek-flash` high (추가 제공자 필요) |
| 시스템 설계 | `architect` | `claude-fable-5-1` xhigh → `gpt-6-astra` xhigh → `kimi-k3` xhigh (추가 제공자 필요) |
| 고난도 일반 작업 | `unspecified-high` | `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) |
| 저난도 일반 작업 | `unspecified-low` | `claude-opus-5-5` low → `glm-5.3` low (추가 제공자 필요) → `deepseek-flash` low (추가 제공자 필요) |
| 짧은 확인·수정 | `quick` | `gpt-6-luna` low → `claude-fable-5-1` low → `glm-5.3-flash` low (추가 제공자 필요) → `kimi-k3` low (추가 제공자 필요) |
| 글·문서 | `writing` | `kimi-k3` medium (추가 제공자 필요) → `qwen3-coder` medium (추가 제공자 필요) → `gemini-3.1-pro` medium (추가 제공자 필요) |
| 화면·프론트엔드 | `visual-engineering` | `claude-fable-5-1` high → `kimi-k3` high (추가 제공자 필요) |
| 창의적 작업 | `artistry` | `claude-fable-5-1` high → `gemini-3.1-pro` high (추가 제공자 필요) → `kimi-k3` high (추가 제공자 필요) |
| 범용 작업 | `capable` | `claude-fable-5-1` medium → `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) → `glm-5.3` medium (추가 제공자 필요) |
| 단순 정리 | `simple-work` | `gpt-6-luna` low → `claude-haiku-4-5` low → `deepseek-flash` low (추가 제공자 필요) |
| 길고 까다로운 작업 | `deep-work` | `gpt-6-astra` high |

## 기본 옵션

작업 분류·추론은 OMH 설정을 따른다. 위 표는 조사 당시의 기본 체인이고, 아래 Claude 확인 순서는 2026-10-07 사용자 요청으로 추가한 설치 기준이다. 현재 대화 모델과 외부 Codex·Claude Code 설정은 바꾸지 않는다.

**Claude 확인 순서: 사용 가능한 최신 Fable → 최신 Opus → 최신 Sonnet.** 모델 ID는 설치 당시 Hermes 제공자 카탈로그와 실제 응답으로 확인한다. 이번 검증에서 사용한 ID는 `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5`다. 이 목록을 미래의 최신 모델 목록으로 취급하지 않는다.

로그인 성공, OMH의 후보 목록, Hermes가 실행에 사용하는 `delegation.fallback_providers`는 별개다. Fable만 한도에 도달했어도 계정은 로그인 상태일 수 있다. OMH 후보에 Opus가 있다는 이유만으로 Hermes가 자동으로 Opus를 호출한다고 보고하지 않는다.

```sh
omh model-chains show --json
```

설치 AI는 아래를 한 흐름으로 수행한다.

1. 선택한 프로필의 GPT·Claude 로그인과 모델별 사용 제한 상태를 확인한다. 인증값은 출력하지 않으며 사용 제한 기록을 초기화하지 않는다.
2. Claude 확인에 사용하는 OMH 분류의 후보 순서와 각 모델의 `anthropic` 연결을 확인한다. Fable 다음에 Opus·Sonnet을 두며 다른 작업 분류·기존 후보는 임의로 제거하지 않는다.
3. Hermes의 자식 fallback도 Opus → Sonnet 순서가 되도록 `hermes config set delegation.fallback_providers`로 적용한다. 기존 다른 제공자 fallback은 별도 사용자 지시가 없으면 뒤에 보존한다. OMH 설정만 바꾸거나 fallback을 무조건 `[]`로 비우지 않는다. 현재 대화의 전역 fallback은 별도 범위다.
4. 통제된 모델별 제한으로 Fable 제한 → Opus, Fable·Opus 제한 → Sonnet을 검사한다. 실제 계정 한도를 소진시키거나 제한을 해제하지 않는다.
5. 최소 실제 위임을 실행해 응답과 `session_model_usage`의 모델·`billing_provider`·API 호출 수를 대조한다. 준비된 배정, fallback 선언, 실제 호출 성공을 따로 기록한다.

모든 Claude 후보를 사용할 수 없으면 기존 다른 제공자 fallback을 사용했는지 또는 중단했는지 명시한다. 성공한 fallback을 원래 배정 모델의 실행 성공으로 쓰지 않는다. 모델별 추론을 일괄 고정하거나 Sol을 모든 작업의 마지막에 새로 강제하지 않는다.

## 확인

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 실행 모델·provider·응답을 대조한다.
- 오류 시 실제 Hermes fallback과 OMH 후보 순서를 함께 확인한다. 로그인 성공만으로 모델 사용 가능을 확정하지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

2026-10-07 Fable 제한 상태에서 수정한 자식 경로가 Opus 5.5로 전환되어 실제 응답 1회와 `billing_provider=anthropic`을 확인했다. 격리된 합성 인증·제한 시험에서 Opus → Sonnet → 기존 GPT 순서와 사용 제한 기록 보존도 확인했다. Sonnet의 실제 호출 성공은 이 검사에서 확인하지 않았다. 개인 `omh-auto-routing` 플러그인은 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)
