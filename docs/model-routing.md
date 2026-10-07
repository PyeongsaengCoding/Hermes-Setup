# 모델 라우팅

Hermes 내부 위임은 OMH 기본 분류를 따른다. Claude Code·Codex 외부 실행기의 설정과 섞지 않는다. 아래는 2026-10-07 확인한 GPT·Claude 연결 환경의 기본 체인이다. 제공자 연결에 따라 순서가 달라질 수 있으며, 설치 때 `omh model-chains show --json`으로 다시 확인한다. 모델 이름은 계정에서 실제 제공하는지 검사한다.

| 하는 일 | OMH 분류 | 모델 라우팅 순서·추론 | 마지막 fallback |
|---|---|---|---|
| 최고 난도 추론 | `ultrabrain` | `gpt-6-astra` xhigh | GPT Sol Medium |
| 심층 분석 | `deep` | `gpt-6.1-sol` high → `deepseek-flash` high (추가 제공자 필요) | GPT Sol Medium |
| 시스템 설계 | `architect` | `claude-fable-5-1` xhigh → `gpt-6-astra` xhigh → `kimi-k3` xhigh (추가 제공자 필요) | GPT Sol Medium |
| 고난도 일반 작업 | `unspecified-high` | `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) | GPT Sol Medium |
| 저난도 일반 작업 | `unspecified-low` | `claude-opus-5-5` low → `glm-5.3` low (추가 제공자 필요) → `deepseek-flash` low (추가 제공자 필요) | GPT Sol Medium |
| 짧은 확인·수정 | `quick` | `gpt-6-luna` low → `claude-fable-5-1` low → `glm-5.3-flash` low (추가 제공자 필요) → `kimi-k3` low (추가 제공자 필요) | GPT Sol Medium |
| 글·문서 | `writing` | `kimi-k3` medium (추가 제공자 필요) → `qwen3-coder` medium (추가 제공자 필요) → `gemini-3.1-pro` medium (추가 제공자 필요) | GPT Sol Medium |
| 화면·프론트엔드 | `visual-engineering` | `claude-fable-5-1` high → `kimi-k3` high (추가 제공자 필요) | GPT Sol Medium |
| 창의적 작업 | `artistry` | `claude-fable-5-1` high → `gemini-3.1-pro` high (추가 제공자 필요) → `kimi-k3` high (추가 제공자 필요) | GPT Sol Medium |
| 범용 작업 | `capable` | `claude-fable-5-1` medium → `claude-opus-5-5` medium → `kimi-k3` medium (추가 제공자 필요) → `glm-5.3` medium (추가 제공자 필요) | GPT Sol Medium |
| 단순 정리 | `simple-work` | `gpt-6-luna` low → `claude-haiku-4-5` low → `deepseek-flash` low (추가 제공자 필요) | GPT Sol Medium |
| 길고 까다로운 작업 | `deep-work` | `gpt-6-astra` high | GPT Sol Medium |

## 개인 최종 fallback

OMH 분류별 순서는 유지한다. 최종 구제 정책은 `openai-codex / gpt-6.1-sol / medium`이다. 모든 작업을 처음부터 이 모델로 보내는 정책은 아니다.

확인한 설정은 다음과 같다. 새 환경에서는 기존 값을 먼저 비교한 뒤 공식 설정 명령으로 적용한다.

```sh
hermes config set delegation.fallback_providers '[{"provider":"openai-codex","model":"gpt-6.1-sol"}]'
hermes config set agent.reasoning_overrides.gpt-6.1-sol medium
```

`agent.reasoning_overrides`는 모델별 설정이므로 해당 모델을 직접 사용할 때도 영향을 줄 수 있다. OMH에서 Sol High로 배정한 작업과 fallback Medium을 실제 실행 기록에서 구별한다. 전역 `delegation.reasoning_effort=medium`으로 모든 분류를 덮어쓰지 않는다.

OMH의 `omh_delegate_route(action="fallback")`는 분류 체인의 다음 후보로 넘어가는 절차다. Hermes의 `delegation.fallback_providers`는 자식 모델 호출의 구제 설정이다. 두 경로가 같은 순서로 자동 실행된다고 가정하지 않는다. 체인이 소진됐을 때의 복구까지 실제 검사한다.

## 확인

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 API 실행 모델·provider·응답을 대조한다.
- 통제된 rate-limit 오류로 마지막 구제와 Medium을 검사한다. 실제 계정 한도를 소진시키지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

현재는 설정과 소스를 확인했다. 이번 저장소 제작에서 실제 fallback 호출을 새로 검증하지는 않았다. 이전 개인 `omh-auto-routing` 플러그인은 설치되어 있으나 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)
