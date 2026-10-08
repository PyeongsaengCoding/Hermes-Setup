# 검증 상태

2026-10-08까지의 검증 기록 요약이다. 새 Mac 전체 설치 성공을 뜻하지 않는다. 현재 라우팅은 [사용자 지정 프리셋](model-routing.md)이며 과거 OMH 기본값 검증과 구분한다.

## 확인한 범위

| 항목 | 확인한 결과 | 근거 |
|---|---|---|
| 저장소·스킬 설치 | 문서·경로 검사와 단위시험 통과. 격리 홈의 설치·반복 적용·원본 대조 확인 | [전체 검토](../reports/2026-10-08-full-review.md) |
| 모델 라우팅 | 두 프리셋·호환 사본·명령 대조. Fable과 Sol 실제 응답 확인. fallback 순서·추론은 mock 시험으로 확인 | [기존 검증 기록](../project-records/document-verification-history.md) |
| 전역 규칙 | 사용자 의도 규칙 파일 반영 확인. 문서 전달 규칙은 현재 배포 원본·설치기에 포함하며 새 세션의 실제 동작은 별도 확인 | [의도 규칙](../reports/2026-10-08-user-intent.md), [현재 배포 기준](global-rules.md) |
| 사용량 표시 | 원본·Desktop 복사본 어댑터 반영, React 렌더링·합성 알림 검사, 실제 상태바 GPT·Claude 표시 확인 | [실행 결과](../project-records/2026-10-07-provider-usage-filter.json) |
| 브라우저·권한 | cua-driver 진단의 권한·연결 확인과 Aside 직접 조작 규칙의 문서·템플릿·시험 반영 확인 | [과거 기록](../project-records/document-verification-history.md), [전체 검토](../reports/2026-10-08-full-review.md) |

## 다시 검사할 때

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

실제 사용자 흐름은 [설치 완료 기준](../INSTALL_FOR_AGENTS.md)을 설치 대상 컴퓨터에서 확인한다.

## 남은 확인

- 새 Mac 전체 설치·새 사용자 로그인과 새 세션의 규칙 로딩·정정 반영 행동.
- 현재 fallback 경로의 실제 제공자 전환과 실제 추론 수준. 기록된 mock 성공은 실제 한도 소진 전환의 증거가 아니다.
- 실행 중인 Desktop의 상세 패널·새로고침·실제 한도 알림과 재실행 후 유지. 기존 React key 경고도 남아 있다.
- Aside 전체 프로필 가져오기·실제 계정·입력·동시 작업·포커스 보존.
- 기준 앱과 Hermes의 창·글자·UI 크기 비교와 설정 유지.

이전 시험 수·당시 라우팅·전역 보고서 규칙 검증은 [과거 기록](../project-records/document-verification-history.md)에 보존한다. 현재 설치기는 보고서 문체·스킬 기준을 배포하지 않으며 문서 전달 시 폴더 카드 제공·앱 자동 실행 금지만 배포한다.
