# 모델 라우팅

Hermes 내부 위임에 적용하는 사용자 지정 정책이다. 외부 Claude Code·Codex 설정과 현재 대화 모델은 변경하지 않는다. 정확한 모델 ID·순서·추론·fallback은 선택한 프리셋 JSON을 정본으로 삼는다.

## 버전 선택

- [Claude 넉넉형](../routing-presets/claude-generous.json)
- [GPT(코덱스) 넉넉형](../routing-presets/gpt-generous.json)

설치 기본은 Claude 넉넉형이며 GPT(코덱스) 넉넉형은 선택사항이다. [routing-snapshot.json](../routing-snapshot.json)은 Claude형 호환 사본이며 적용 요청에는 프리셋을 명시한다. 설치·전환 요청 없이 기존 환경의 라우팅을 자동 변경하지 않는다.

| 분류 | Claude 넉넉형 | GPT(코덱스) 넉넉형 | 추론 |
|---|---|---|---|
| 화면·프론트엔드 | Fable → Opus → Astra | Fable → Astra → Opus | high |
| 창의적 작업 | Fable → Opus → Astra | Fable → Astra → Opus | high |
| 범용 작업 | Fable → Opus → Sonnet → Astra | Fable → Astra → Opus → Sonnet | medium |
| 길고 까다로운 작업 | Fable → Opus → Astra | Astra → Fable → Opus | high |
| 글·문서 | Opus → Sol | Sol → Opus | medium |

표는 두 버전이 다른 분류만 보여준다. 나머지 분류·추론·공통 fallback은 같다. GPT형도 화면·창의·범용 작업은 Fable로 시작한다.

## 적용 기준

- GPT·Claude 후보만 사용한다. Kimi·Qwen·Gemini·GLM·DeepSeek를 추가하지 않으며 계정·인증·제공자 연결은 보존한다.
- OMH 분류별 후보와 Hermes 실행 fallback은 별개다. 전역 fallback은 Opus, 자식 공통 fallback은 Fable → Astra → Sonnet → Opus이며 분류 변경으로 공통 순서를 바꾸지 않는다.
- 주 모델이 사용 가능하면 유지한다. 이미 시도한 모델·사용 불가능한 후보는 건너뛴다. 모델별 제한·계정 전체 제한·인증·통신 오류를 구분하고 사용 제한 기록은 초기화하지 않는다.
- 추론은 작업 분류별로 유지하며 전역 모델별 고정으로 대체하지 않는다. 이 프리셋을 최신 모델 목록으로 취급하지 않는다.

선택한 프로필의 로그인·모델 가용성을 확인하고 프리셋의 모든 분류를 적용한다. OMH는 연결된 후보를 앞으로 모을 수 있으므로 저장 후 순서·추론과 실제 자식 fallback을 다시 읽는다.

```sh
omh model-chains show --json
```

공통 fallback 적용 명령:

```sh
hermes config set fallback_providers '[{"provider":"anthropic","model":"claude-opus-5-5"}]'
hermes config set delegation.fallback_providers '[{"provider":"anthropic","model":"claude-fable-5-1"},{"provider":"openai-codex","model":"gpt-6-astra"},{"provider":"anthropic","model":"claude-sonnet-5-5"},{"provider":"anthropic","model":"claude-opus-5-5"}]'
```

## fallback 순서·추론 보존

설치된 소스에서 fallback 순서·추론 보존이 필요한지 확인한다. 아래는 플러그인이 아닌 소스 호환 패치다.

- `configure_delegation_reasoning.py`: fallback 시 자식에게 배정한 추론을 유지한다.
- `configure_gpt_fallback.py`: GPT 시작 자식에서 Fable을 처음, Opus를 마지막에 둔다. Claude 시작 자식과 공통 설정은 보존한다.

```sh
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_delegation_reasoning.py --source-root <확인한-Hermes-소스-루트> --apply
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트>
python3 scripts/configure_gpt_fallback.py --source-root <확인한-Hermes-소스-루트> --apply
```

실제 import 경로의 소스 루트를 지정하고 미리보기 후 호환될 때만 적용한다. 변경된 관리 구간·다른 함수 구조·심볼릭 링크는 거부하며 같은 패치는 건너뛴다. 새 프로세스에서 반영을 확인한다. 전환 모델이 추론을 지원하지 않으면 오류를 알리고 수준을 조용히 낮추지 않는다.

## 완료 확인

작업 분류에 맞는 `omh_delegate_route` 적용 직후 `delegate_task`로 최소 실제 위임을 실행한다. 응답과 `session_model_usage`의 모델·`billing_provider`·API 호출 수를 대조하며, 추론이 관측되지 않으면 배정값과 구분한다. 오류가 포함된 `completed`나 대체 모델의 성공을 원래 모델의 성공으로 보고하지 않는다.

fallback 순서와 추론 유지는 실제 한도를 소진하거나 제한을 초기화하지 않고 통제된 시험으로 확인한다. 설정 대조·mock 전환·실제 제공자 호출은 따로 기록한다. 현재 확인 범위와 과거 근거는 [검증 상태](verification.md)에 있다.

## AI에게 적용 요청

아래는 쉘 명령이 아니라 AI 채팅에 붙여 넣는 요청이다. 둘 중 하나만 사용한다.

### Claude 넉넉형 요청

```text
https://github.com/PyeongsaengCoding/Hermes-Setup 의 main에서 docs/model-routing.md와 routing-presets/claude-generous.json을 읽고, 내 현재 Hermes 프로필을 Claude 넉넉형으로 맞춰줘. OMH 분류별 모델 순서·추론과 Hermes 전역·자식 공통 fallback을 구분하고 공통 fallback의 마지막 Opus를 유지해줘. GPT·Claude 계열 외 후보는 모든 분류에서 제거하고, 로그인·구독·다른 프로필은 변경하지 말고, 필요한 호환 패치까지 확인·적용한 뒤 설정 대조와 실제 동작 검증을 구분해서 결과를 알려줘.
```

### GPT(코덱스) 넉넉형 요청

```text
https://github.com/PyeongsaengCoding/Hermes-Setup 의 main에서 docs/model-routing.md와 routing-presets/gpt-generous.json을 읽고, 내 현재 Hermes 프로필을 GPT(코덱스) 넉넉형으로 맞춰줘. OMH 분류별 모델 순서·추론과 Hermes 전역·자식 공통 fallback을 구분하고 공통 fallback의 마지막 Opus를 유지해줘. GPT·Claude 계열 외 후보는 모든 분류에서 제거하고, 로그인·구독·다른 프로필은 변경하지 말고, 필요한 호환 패치까지 확인·적용한 뒤 설정 대조와 실제 동작 검증을 구분해서 결과를 알려줘.
```

## 선택적 CLI 전환

선택한 버전의 열두 분류를 적용하는 명령이다. 기존 환경에서도 제거한 후보가 남지 않도록 전체 분류를 명시한다. 새 설치는 위 AI 요청으로 전체 프리셋과 호환 패치까지 맞춘다. 현재 프로필을 확인한 뒤 둘 중 한 블록만 실행한다. 미연결 후보를 연결하거나 로그인하지 않는다.

### claude-generous CLI

```sh
omh model-chains set ultrabrain 'gpt-6-astra:xhigh, claude-fable-5-1:xhigh, claude-opus-5-5:xhigh'
omh model-chains set deep 'gpt-6.1-sol:high, claude-fable-5-1:high, claude-opus-5-5:high'
omh model-chains set architect 'claude-fable-5-1:xhigh, gpt-6-astra:xhigh, claude-opus-5-5:xhigh'
omh model-chains set unspecified-high 'claude-opus-5-5:medium'
omh model-chains set unspecified-low 'claude-opus-5-5:low'
omh model-chains set quick 'gpt-6-luna:low, claude-fable-5-1:low, claude-opus-5-5:low, gpt-6-astra:low'
omh model-chains set writing 'claude-opus-5-5:medium, gpt-6.1-sol:medium'
omh model-chains set visual-engineering 'claude-fable-5-1:high, claude-opus-5-5:high, gpt-6-astra:high'
omh model-chains set artistry 'claude-fable-5-1:high, claude-opus-5-5:high, gpt-6-astra:high'
omh model-chains set capable 'claude-fable-5-1:medium, claude-opus-5-5:medium, claude-sonnet-5-5:medium, gpt-6-astra:medium'
omh model-chains set simple-work 'gpt-6-luna:low, claude-fable-5-1:low, claude-opus-5-5:low, claude-haiku-4-5:low'
omh model-chains set deep-work 'claude-fable-5-1:high, claude-opus-5-5:high, gpt-6-astra:high'
omh model-chains show --json
```

### gpt-generous CLI

```sh
omh model-chains set ultrabrain 'gpt-6-astra:xhigh, claude-fable-5-1:xhigh, claude-opus-5-5:xhigh'
omh model-chains set deep 'gpt-6.1-sol:high, claude-fable-5-1:high, claude-opus-5-5:high'
omh model-chains set architect 'claude-fable-5-1:xhigh, gpt-6-astra:xhigh, claude-opus-5-5:xhigh'
omh model-chains set unspecified-high 'claude-opus-5-5:medium'
omh model-chains set unspecified-low 'claude-opus-5-5:low'
omh model-chains set quick 'gpt-6-luna:low, claude-fable-5-1:low, claude-opus-5-5:low, gpt-6-astra:low'
omh model-chains set writing 'gpt-6.1-sol:medium, claude-opus-5-5:medium'
omh model-chains set visual-engineering 'claude-fable-5-1:high, gpt-6-astra:high, claude-opus-5-5:high'
omh model-chains set artistry 'claude-fable-5-1:high, gpt-6-astra:high, claude-opus-5-5:high'
omh model-chains set capable 'claude-fable-5-1:medium, gpt-6-astra:medium, claude-opus-5-5:medium, claude-sonnet-5-5:medium'
omh model-chains set simple-work 'gpt-6-luna:low, claude-fable-5-1:low, claude-opus-5-5:low, claude-haiku-4-5:low'
omh model-chains set deep-work 'gpt-6-astra:high, claude-fable-5-1:high, claude-opus-5-5:high'
omh model-chains show --json
```

## 업데이트

```sh
hermes update --check
hermes update --backup
omh update --dry-run --no-omh-tui
omh update --no-omh-tui
```

`--no-omh-tui`는 OMH 업데이트 때 기존 화면·스킨을 유지한다. 업데이트 후 fallback 설정과 OMH 후보를 다시 읽고 소스 호환 패치 두 개를 미리보기·검증한다. 호환될 때만 적용한 뒤 Desktop을 재시작한다. 업데이트 명령 성공만으로 커스텀 라우팅 보존을 완료했다고 보고하지 않는다.
