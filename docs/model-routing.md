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

모델·추론·fallback 모두 OMH 기본 옵션을 사용한다. 특정 모델을 최종 fallback으로 추가하거나 모델별 추론을 고정하지 않는다. 표는 조사 당시의 참고 기록이며 설치용 override가 아니다. 설치된 OMH 버전과 연결한 제공자에 따른 현재 기본값을 확인한다.

```sh
omh model-chains show --json
```

이 저장소의 이전 설정을 적용한 환경만 다음 명령으로 개인 구제 설정을 비운다. 다른 개인 설정이 있으면 먼저 비교하고 관련 항목만 제거한다.

```sh
hermes config set delegation.fallback_providers '[]'
hermes config set agent.reasoning_overrides '{}'
```

OMH 기본 체인 안에 Sol이 있으면 그대로 둔다. 제거 대상은 모든 작업의 마지막에 Sol Medium을 강제하던 개인 설정이다. 현재 대화 모델과 외부 Codex·Claude Code 설정은 바꾸지 않는다.

## 확인

- 분류에 맞게 `omh_delegate_route` 적용 직후 `delegate_task`를 실행한다.
- 요청한 모델·추론과 실제 실행 모델·provider·응답을 대조한다.
- 오류 시 OMH 기본 fallback 절차를 따른다. 실제 계정 한도를 소진시키지 않는다.
- `completed` 안에 오류가 있으면 정상 위임으로 기록하지 않는다.

개인 설정 제거와 OMH 체인의 기본값 유지는 확인했다. 실제 fallback 호출을 새로 검사한 것은 아니다. 개인 `omh-auto-routing` 플러그인은 비활성이며 기본 설치에 넣지 않는다.

[Hermes fallback 안내](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers) · [OMH 원본](https://github.com/rlaope/oh-my-hermes)
