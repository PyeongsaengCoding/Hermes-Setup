# 전역 규칙

Aside 직접 조작과 문서 전달 규칙을 선택한 프로필에 설치한다. 규칙 본문은 아래 템플릿이 정본이다.

## 원본과 적용 위치

- 배포 원본: [Aside 브라우저 규칙](../templates/aside-browser.md).
- 배포 원본: [문서 전달 규칙](../templates/document-delivery.md). 실제 문서 폴더를 선택 가능한 카드로 제공하며 Finder·편집기·미리보기를 자동 실행하지 않는다.
- 적용 파일: 선택한 Hermes 프로필의 `SOUL.md`.
- 기본 홈: `${HERMES_HOME:-$HOME/.hermes}`. 이름 있는 프로필은 해당 프로필 홈을 명시한다.

```sh
python3 scripts/install_global_rules.py
python3 scripts/install_global_rules.py --apply
```

다른 프로필을 선택했다면 두 명령 모두 `--home "$HOME/.hermes/profiles/<이름>"`을 붙인다. 실행 전에 실제 프로필을 확인하며 다른 프로필에 일괄 적용하지 않는다.

미리보기는 읽기 전용이다. 적용은 기존 내용을 보존하고 없는 규칙만 관리 마커 안에 추가한다. 마커 없이 같은 내용이 있어도 건너뛰며, 다른 규칙이나 손상된 관리 구간은 충돌로 중단한다.

기존 관리 규칙의 갱신은 원본과 대조하고 승인 후 해당 구간만 수정한다. 이전 보고서 규칙은 `legacy_report_policy: present_preserved`로 알리고 보존하며 개인 문구를 자동 삭제하지 않는다. 브라우저 연결은 [브라우저 안내](browsers.md)를 따른다.

## 확인

적용 파일에서 중복 없음·기존 내용 보존을 확인한다. 새 Hermes 세션에서는 SOUL.md 로딩, 프로젝트별 Aside 프로필의 `repl` 직접 조작, 문서 전달 시 폴더 카드 제공·앱 미실행을 확인한다.

Hermes 문맥 파일과 SOUL.md의 역할은 [공식 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)를 따른다. 진행 중인 세션에 파일 변경이 즉시 주입된다고 가정하지 않는다.
