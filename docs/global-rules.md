# 전역 문체 규칙

이 저장소는 보고서 문체와 Humanizer 사용 규칙만 관리한다. 제품의 버튼·오류·위험 행동 안내는 제품 UX writing 기준에서 관리하고, 코드 정리용 `omh-ai-slop-cleaner`를 매 작업마다 실행하도록 강제하지 않는다. Humanizer는 설치 목록의 공식 스킬이며 OMH 스킬은 OMH 설치로 준비한다.

## 원본과 적용 위치

- 배포 원본: [templates/report-writing.md](../templates/report-writing.md).
- 적용 파일: 선택한 Hermes 프로필의 `SOUL.md`.
- 기본 홈: `${HERMES_HOME:-$HOME/.hermes}`. 이름 있는 프로필은 해당 프로필 홈을 명시한다.

```sh
python3 scripts/install_global_rules.py
python3 scripts/install_global_rules.py --apply
```

다른 프로필을 선택했다면 두 명령 모두 `--home "$HOME/.hermes/profiles/<이름>"`을 붙인다. 실행 전에 실제 프로필을 확인하며 다른 프로필에 일괄 적용하지 않는다.

미리보기는 파일을 쓰지 않는다. 적용 시 기존 내용을 보존하고 관리 마커 안에 규칙을 한 번만 추가한다. 같은 규칙이 마커 없이 이미 있어도 추가하지 않는다. 기존 보고서 규칙이 다르거나 관리 구간이 수정·손상돼 있으면 중단하고 차이를 사용자에게 확인한다. 해당 도구는 기존 규칙의 자동 업데이트나 덮어쓰기를 하지 않는다.

## 확인

적용 후 정확한 대상 파일을 읽어 규칙이 한 번만 있으며 기존 내용이 보존됐는지 확인한다. 이어서 선택한 프로필로 새 Hermes 세션을 시작해 `SOUL.md`가 로드되는지, 짧은 작업 보고서에서 Humanizer를 실제로 로드하고 검토하는지 확인한다. 파일 설치 성공만으로 모델의 규칙 준수까지 확인했다고 보고하지 않는다.

Hermes 문맥 파일과 SOUL.md의 역할은 [공식 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)를 따른다. 진행 중인 세션에 파일 변경이 즉시 주입된다고 가정하지 않는다.
