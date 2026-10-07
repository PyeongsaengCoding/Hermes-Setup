# 브라우저

Hermes의 격리 브라우저와 사용자가 로그인한 브라우저는 다르다. 새 브라우저에 로그인이 없다고 기존 계정이 로그아웃됐다고 판단하지 않는다.

## Aside

[공식 사이트](https://aside.com)에서 macOS 앱을 설치하고 [개발자 안내](https://docs.aside.com/help/developers)에 따라 CLI를 준비한다. 설치·Aside 로그인·브라우저 프로필 가져오기·Hermes 연결은 각각 확인한다.

1. 원본 Chrome·Edge 프로필과 가져오기 메뉴에서 실제 지원하는 프로필을 대조한다.
2. 원본 프로필 하나마다 대상 프로필 하나를 만든다. 이름만으로 계정을 추정하지 않는다.
3. Aside의 기본 가져오기 메뉴를 사용한다. Keychain·로그인·복구키 화면은 사용자가 직접 처리한다.
4. 가져오기 완료 표시와 대상 사이트의 실제 계정을 확인한다. 미지원 브라우저는 가져오기 완료로 기록하지 않는다.

CLI와 MCP 연결 중 필요한 경로를 선택한다.

```sh
aside --help
aside repl "const page = await openTab('https://example.com'); console.log(await page.title())"
hermes mcp add aside --command aside --args mcp
hermes mcp test aside
```

CLI가 PATH에 없다면 `command -v aside`로 확인한 실행 경로를 사용한다. 기존 이름의 MCP가 있으면 먼저 비교한다. MCP 등록 자체는 인증·프로필 선택·실제 조작 성공이 아니다.

## 기존 Chrome·Edge·Safari

앱 설치는 `/Applications/`에 한다. Hermes의 기본 headless 세션, 사용자 프로필을 연결한 CDP, macOS GUI 제어를 구별한다. 사용 중인 브라우저를 종료하거나 열린 프로필을 자동 복제하지 않는다. Safari는 Chrome CDP 연결 방식으로 처리하지 않는다. 계정 접근에 필요한 권한을 우회하지 않는다.

```sh
hermes computer-use install
hermes computer-use doctor
```

권한 통과 후에도 실제 입력과 포커스 보존을 확인한다. 백그라운드 입력이 안 되면 사용자가 허용하기 전에는 전면 조작으로 바꾸지 않는다. 검사할 때 만든 탭만 정리한다.

## 자료

[Hermes 브라우저](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser) · [Aside 개발자 안내](https://docs.aside.com/help/developers)
