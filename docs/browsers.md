# 브라우저

Hermes의 격리 브라우저와 사용자가 로그인한 브라우저는 다르다. 새 브라우저에 로그인이 없다고 기존 계정이 로그아웃됐다고 판단하지 않는다.
직접 조작·자체 AI 위임 금지·프로젝트별 프로필 경계는 [Aside 규칙](../templates/aside-browser.md)을 따른다. 설치는 [전역 규칙 안내](global-rules.md)에 있다.

## Aside

[공식 사이트](https://aside.com)에서 macOS 앱을 설치하고 [개발자 안내](https://docs.aside.com/help/developers)에 따라 CLI를 준비한다. 설치·Aside 로그인·브라우저 프로필 가져오기·Hermes 연결은 각각 확인한다.

1. 원본 Chrome·Edge 프로필과 가져오기 메뉴에서 실제 지원하는 프로필을 대조한다.
2. 원본 프로필 하나마다 대상 프로필 하나를 만든다. 이름만으로 계정을 추정하지 않는다.
3. Aside의 기본 가져오기 메뉴를 사용한다. Keychain·로그인·복구키 화면은 사용자가 직접 처리한다.
4. 가져오기 완료 표시와 대상 사이트의 실제 계정을 확인한다. 미지원 브라우저는 가져오기 완료로 기록하지 않는다.

CLI와 MCP 연결 중 필요한 경로를 선택한다. MCP에서는 JavaScript를 실행하는 `repl` 도구만 허용하고 에이전트 위임 도구는 노출하지 않는다. 가능하면 서버의 include 필터를 `[repl]`로 제한하고 실제 등록된 도구를 확인한다.

```sh
aside --help
aside repl "const page = await openTab('https://example.com'); console.log(await page.title())"
hermes mcp add aside --command aside --args mcp
hermes mcp test aside
```

CLI가 PATH에 없다면 `command -v aside`로 실행 경로를 확인한다. 기존 MCP는 비교 후 연결하며, `repl` 오류는 연결·프로필·호출 코드를 진단해 복구한다. 자체 AI로 우회하지 않는다.

설치 검증은 새 Hermes 세션에서 실제 도구 호출이 `repl`인지 확인하고, 선택한 프로필로 이동·입력·결과 읽기를 수행한다. 자체 에이전트가 호출되지 않았는지도 호출 기록으로 확인한다.

## 기존 Chrome·Edge·Safari

기존 브라우저는 프로필 가져오기 원본으로 보존한다. 앱은 `/Applications/`에 설치하며 사용 중인 브라우저를 종료하거나 기본 브라우저를 바꾸지 않는다. 사용자가 선택한 프로필의 데이터는 Aside의 기본 가져오기 기능으로 로컬에 이전한다. 쿠키·비밀번호·복구키를 Git 저장소나 공개 자료에 넣지 않으며 계정 권한을 우회하지 않는다. Safari를 Chrome CDP 방식으로 연결하지 않는다.

브라우저 조작은 Aside를 사용한다. 이 브라우저 설치 절차에서 `computer-use` 설치나 입력 검사를 요구하지 않는다. `computer-use`는 브라우저와 별개인 네이티브 앱 작업용 스킬이다.

## 자료

[Hermes 브라우저](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser) · [Aside 개발자 안내](https://docs.aside.com/help/developers)
