# 설치 목록

`H`는 `${HERMES_HOME:-$HOME/.hermes}`다. 기본은 `~/.hermes/`, 이름 있는 프로필은 `~/.hermes/profiles/<이름>/`이다. `$(brew --prefix)`는 Apple Silicon에서 보통 `/opt/homebrew`, Intel에서 `/usr/local`이다. npm·uv·Go 실행 파일 위치는 각 관리자의 설정을 따른다.

비-OMH 스킬 61개를 기준으로 한다. 공식 원본 58개와 일반화한 커스텀 3개다. 스킬 문서는 설치하지만 CLI·라이브러리·서비스 권한은 해당 작업을 사용할 때 준비한다. 로컬에서 수정된 공식 스킬 3개는 수정본 대신 고정 공식 원본을 설치한다. OMH 스킬은 OMH 설치기로 별도 관리한다.

| 종류 | 항목 | 용도 | 설치 기준·추가 준비 | 일반 설치 경로 | 추가 도구·설정 경로 |
|---|---|---|---|---|---|
| 앱·CLI | Hermes | 주 작업 에이전트 | 필수; 공식 Desktop/CLI 설치 | `H/` | Desktop 앱은 `/Applications/`; 소스 방식 checkout은 `H/hermes-agent/` |
| 앱 | Aside | 로그인 브라우저 작업·프로필 가져오기 | 필수; 공식 앱·CLI·자신의 로그인 | `/Applications/Aside.app` | CLI는 공식 설치기 경로 확인; macOS 프로필은 `~/Library/Application Support/Aside/` |
| 앱 | Chrome·Edge·Safari | 기존 로그인 브라우저 활용 | 사용하는 브라우저만; 프로필 가져오기는 지원 여부 확인 | `/Applications/` | `~/Library/Application Support/Google/Chrome/`, `~/Library/Application Support/Microsoft Edge/`, Safari는 OS 관리 |
| 확장·스킬팩 | OMH | 작업 분류·라우팅·검증 지침 | 필수; 공식 install·setup | `~/.omh/`; `~/.local/share/omh/` | Hermes 등록 `H/plugins/omh/`; 스킬 실제 경로는 `skills.external_dirs` 확인 |
| Hermes 플러그인 | provider-usage | 계정 사용량·잔여 한도·리셋 시간 | 필수; 설치·활성화·실제 조회 | `H/plugins/provider-usage/` | Desktop UI `H/desktop-plugins/provider-usage/`; 인증은 사용자의 로컬 저장소 |
| Hermes 플러그인 | omh-auto-routing | 개인 자동 라우팅 강제 실험 | 기존 설치본은 비활성; 기본 배포하지 않음 | `H/plugins/omh-auto-routing/` (기존 설치만) | 공식 OMH 기능이 아님 |
| Hermes UI 확장 | OMH Desktop·TUI | 상태·작업 표시 | OMH setup에서 선택한 UI 연결 | `H/desktop-plugins/omh/`; `H/tui-widgets/omh-status.mjs` | 설치 여부·표시는 별도 확인 |
| 프로젝트 지침 | AGENTS.md | 저장소 작업 규칙 | 이 저장소에 포함; 스킬 아님 | `Hermes-Setup/AGENTS.md` | 다른 프로젝트는 각 프로젝트 루트 |
| 스킬 | apple-notes | Apple 메모 읽기·검색·작성 | 공식 원본; memo; macOS Automation 승인 | `H/skills/apple/apple-notes/` | `$(brew --prefix)/bin/memo` |
| 스킬 | apple-reminders | Apple 미리 알림 관리 | 공식 원본; remindctl; 미리 알림 승인 | `H/skills/apple/apple-reminders/` | `$(brew --prefix)/bin/remindctl` |
| 스킬 | findmy | 나의 찾기 기기·AirTag 확인 | 공식 원본; 나의 찾기·iCloud; 화면 권한 | `H/skills/apple/findmy/` | macOS 기본 앱 |
| 스킬 | imessage | iMessage·SMS 조회·전송 | 공식 원본; imsg; Messages 로그인·권한 | `H/skills/apple/imessage/` | `$(brew --prefix)/bin/imsg` |
| 스킬 | claude-code | 외부 Claude Code에 코딩 위임 | 공식 원본; Claude Code CLI·로그인 | `H/skills/autonomous-ai-agents/claude-code/` | npm 전역 bin; `~/.claude/` |
| 스킬 | codex | 외부 Codex CLI에 코딩 위임 | 공식 원본; Codex CLI·로그인 | `H/skills/autonomous-ai-agents/codex/` | npm 전역 bin; `~/.codex/` |
| 스킬 | computer-use | 네이티브 앱 화면·입력 제어 | 공식 원본; cua-driver; 접근성·화면 권한 | `H/skills/autonomous-ai-agents/computer-use/` | `H/tools/` (Hermes 관리) |
| 스킬 | hermes-agent | Hermes 사용·설정·문제 해결 | 공식 원본; Hermes CLI | `H/skills/autonomous-ai-agents/hermes-agent/` | Hermes 설치 방식에 따름 |
| 스킬 | opencode | 외부 OpenCode에 코딩 위임 | 공식 원본; OpenCode CLI·로그인 | `H/skills/autonomous-ai-agents/opencode/` | npm 전역 bin 또는 `$(brew --prefix)/bin/` |
| 스킬 | architecture-diagram | 아키텍처 다이어그램 작성 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/creative/architecture-diagram/` | — |
| 스킬 | ascii-video | 영상·오디오를 ASCII 영상으로 변환 | 공식 원본; Python·NumPy·Pillow·ffmpeg | `H/skills/creative/ascii-video/` | 프로젝트 `.venv/`; `$(brew --prefix)/bin/ffmpeg` |
| 스킬 | baoyu-infographic | 정보를 인포그래픽으로 구성 | 공식 원본; 이미지 생성 도구는 사용할 때 연결 | `H/skills/creative/baoyu-infographic/` | Hermes 제공자 설정 |
| 스킬 | claude-design | 일회성 HTML 화면·발표·프로토타입 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/creative/claude-design/` | — |
| 스킬 | design-md | DESIGN.md 디자인 토큰 작성·검사 | 공식 원본; Node; `@google/design.md`를 npx로 실행 | `H/skills/creative/design-md/` | `~/.npm/_npx/` |
| 스킬 | humanizer | 과장·군더더기·AI 문체 제거 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/creative/humanizer/` | — |
| 스킬 | manim-video | Manim 수학·알고리즘 영상 | 공식 원본; Manim·LaTeX·ffmpeg | `H/skills/creative/manim-video/` | 프로젝트 `.venv/`; `/Library/TeX/`; Homebrew bin |
| 스킬 | p5js | p5.js 생성형 그래픽·인터랙션 | 공식 원본; 브라우저·p5.js; 영상 출력은 Node·ffmpeg | `H/skills/creative/p5js/` | 프로젝트 HTML·`node_modules/` |
| 스킬 | popular-web-designs | 실제 디자인 시스템 참고 화면 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/creative/popular-web-designs/` | — |
| 스킬 | songwriting-and-ai-music | 작사·작곡 방향·음악 생성 요청 | 공식 원본; 음악 생성 서비스는 선택 | `H/skills/creative/songwriting-and-ai-music/` | 서비스 계정; 별도 로컬 도구 없음 |
| 스킬 | desktop-app-provisioning | 앱 설치·브라우저 프로필 이전 | 일반화한 커스텀; macOS 설치·GUI 도구·OS 승인 | `H/skills/desktop-app-provisioning/` | `/Applications/`; `H/tools/` |
| 스킬 | sdlc-review | Kanban 작업 결과 검토 | 공식 원본; Hermes Kanban worker 작업 | `H/skills/devops/sdlc-review/` | Hermes 기능; 별도 CLI 없음 |
| 스킬 | email-inbox-triage | 메일 우선순위·답장 초안 | 공식 원본; 연결된 메일 도구·계정 | `H/skills/email/email-inbox-triage/` | 선택한 메일 도구 설정 |
| 스킬 | himalaya | IMAP·SMTP 메일 CLI 작업 | 공식 원본; himalaya·IMAP/SMTP 로그인 | `H/skills/email/himalaya/` | `$(brew --prefix)/bin/himalaya`; `~/.config/himalaya/` |
| 스킬 | gif-search | Tenor GIF 검색·다운로드 | 공식 원본; curl·jq·Tenor API key | `H/skills/media/gif-search/` | `$(brew --prefix)/bin/jq`; key는 `H/.env` |
| 스킬 | songsee | 오디오 스펙트럼 분석 | 공식 원본; Go·songsee; ffmpeg 선택 | `H/skills/media/songsee/` | `$(go env GOPATH)/bin/songsee` |
| 스킬 | youtube-content | YouTube 자막을 요약·콘텐츠로 변환 | 공식 원본; youtube-transcript-api; Hermes PM extra | `H/skills/media/youtube-content/` | Hermes PM 관리 환경 또는 격리 helper `.venv/` |
| 스킬 | naver-blog-production | 네이버 블로그 제작·예약 검증 | 일반화한 커스텀; 자신의 블로그 로그인·운영 지침 | `H/skills/naver-blog-production/` | 브라우저 개인 프로필; 프로젝트 `AGENTS.md` |
| 스킬 | obsidian | Obsidian vault 노트 작업 | 공식 원본; Obsidian 앱·본인 vault | `H/skills/note-taking/obsidian/` | `/Applications/Obsidian.app`; 선택한 vault |
| 스킬 | airtable | Airtable 레코드 조회·수정 | 공식 원본; curl·Airtable PAT | `H/skills/productivity/airtable/` | macOS curl; PAT는 `H/.env` |
| 스킬 | box | Box 파일·권한·메타데이터 관리 | 공식 원본; Box CLI·OAuth | `H/skills/productivity/box/` | `H/tools/box-cli/` |
| 스킬 | document-to-action-items | 문서에서 의무·기한·할 일 추출 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/productivity/document-to-action-items/` | — |
| 스킬 | docx | Word 문서 작성·편집 | 공식 원본; python-docx | `H/skills/productivity/docx/` | 프로젝트 `.venv/` |
| 스킬 | google-workspace | Gmail·Calendar·Drive·Docs·Sheets | 공식 원본; Google OAuth·Hermes Google extra; gws 선택 | `H/skills/productivity/google-workspace/` | Hermes 관리 환경; 토큰은 `H/` |
| 스킬 | maps | 위치·경로·시간대 조회 | 공식 원본; Python 표준 라이브러리·네트워크 | `H/skills/productivity/maps/` | 추가 패키지 없음 |
| 스킬 | meeting-action-items | 회의에서 결정·담당·할 일 추출 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/productivity/meeting-action-items/` | — |
| 스킬 | notion | Notion 페이지·DB 작업 | 공식 원본; Notion token; ntn 선택 | `H/skills/productivity/notion/` | npm 전역 bin; token은 `H/.env` |
| 스킬 | pdf | PDF 읽기·작성·병합·OCR | 공식 원본; pypdf·reportlab·pdfplumber; 렌더링/OCR 도구 선택 | `H/skills/productivity/pdf/` | 프로젝트 `.venv/`; Poppler·OCR은 Homebrew |
| 스킬 | powerpoint | PowerPoint 작성·편집·렌더링 | 공식 원본; python-pptx; 렌더링은 LibreOffice·Poppler | `H/skills/productivity/powerpoint/` | 프로젝트 `.venv/`; `/Applications/LibreOffice.app`; Homebrew |
| 스킬 | product-price-monitor | 상품·항공권·매물 가격 감시 | 공식 원본; 검색/브라우저·예약 기능 | `H/skills/productivity/product-price-monitor/` | Hermes cron·브라우저 설정 |
| 스킬 | teams-meeting-pipeline | Teams 회의 자막·요약 파이프라인 | 공식 원본; Hermes Teams pipeline·Graph 권한 | `H/skills/productivity/teams-meeting-pipeline/` | Hermes plugin; 설정은 `H/.env` |
| 스킬 | weekly-review-planning | 주간 회고·다음 주 계획 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/productivity/weekly-review-planning/` | — |
| 스킬 | xlsx | Excel·CSV 작성·분석 | 공식 원본; openpyxl; 재계산은 LibreOffice 선택 | `H/skills/productivity/xlsx/` | 프로젝트 `.venv/`; `/Applications/LibreOffice.app` |
| 스킬 | read-model-performance-safety | 조회 모델 성능·권한 안전성 검토 | 일반화한 커스텀; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/read-model-performance-safety/` | — |
| 스킬 | arxiv | arXiv 논문 검색·조회 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/research/arxiv/` | — |
| 스킬 | competitor-news-monitor | 경쟁사 뉴스 감시·근거 정리 | 공식 원본; 검색·예약 기능 | `H/skills/research/competitor-news-monitor/` | Hermes 제공자·cron 설정 |
| 스킬 | grounded-citations | 검증 가능한 인용·출처 관리 | 공식 원본; Python 표준 라이브러리·검색 도구 | `H/skills/research/grounded-citations/` | 추가 패키지 없음 |
| 스킬 | llm-wiki | Markdown 지식 위키 구축 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/research/llm-wiki/` | — |
| 스킬 | xurl | X 검색·게시·메시지 CLI | 공식 원본; xurl·X OAuth | `H/skills/social-media/xurl/` | `~/.local/bin/` 또는 패키지 관리자 bin |
| 스킬 | codebase-inspection | 언어·코드량·구성 조사 | 공식 원본; pygount | `H/skills/software-development/codebase-inspection/` | uv tool 환경·bin 또는 프로젝트 `.venv/` |
| 스킬 | dogfood | 웹 앱 탐색 QA·오류 증거 | 공식 원본; 브라우저 도구·검사 URL | `H/skills/software-development/dogfood/` | Hermes 브라우저 설정 |
| 스킬 | github | GitHub 저장소·PR·이슈 작업 | 공식 원본; gh·GitHub 로그인 | `H/skills/software-development/github/` | `$(brew --prefix)/bin/gh`; `~/.config/gh/` |
| 스킬 | hermes-agent-skill-authoring | Hermes 스킬 작성·검증 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/software-development/hermes-agent-skill-authoring/` | — |
| 스킬 | inspecting-hermes-desktop-dom | Hermes Desktop DOM·CSS 검사 | 공식 원본; Hermes Desktop 개발용 CDP | `H/skills/software-development/inspecting-hermes-desktop-dom/` | Hermes 개발 checkout; 기본 사용자 설치에 필수 아님 |
| 스킬 | node-inspect-debugger | Node.js 디버깅 | 공식 원본; Node; CDP 라이브러리 선택 | `H/skills/software-development/node-inspect-debugger/` | Node bin; 프로젝트 `node_modules/` |
| 스킬 | python-debugpy | Python pdb·debugpy 디버깅 | 공식 원본; Python; 원격 디버깅은 debugpy | `H/skills/software-development/python-debugpy/` | 대상 프로젝트 개발 `.venv/` |
| 스킬 | requesting-code-review | 변경 검토·품질 검사 | 공식 원본; Git·프로젝트 검사 도구·위임 | `H/skills/software-development/requesting-code-review/` | 프로젝트 의존 도구; Hermes delegation |
| 스킬 | simplify-code | 최근 코드 변경 정리 | 공식 원본; Git·프로젝트 검사·위임 | `H/skills/software-development/simplify-code/` | 프로젝트 의존 도구; Hermes delegation |
| 스킬 | spike | 짧은 실험으로 가정 검증 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/software-development/spike/` | — |
| 스킬 | systematic-debugging | 재현·원인 확인 후 수정 | 공식 원본; 프로젝트의 테스트·진단 도구 | `H/skills/software-development/systematic-debugging/` | 대상 프로젝트 환경 |
| 스킬 | test-driven-development | 실패 테스트부터 구현 | 공식 원본; 별도 설치 없음; 작업에 맞는 기본 도구 | `H/skills/software-development/test-driven-development/` | — |
| 스킬 | blocked-page-recovery | 차단·로그인 벽 페이지 접근 복구 | 공식 원본; 허용된 브라우저/검색 경로 | `H/skills/web/blocked-page-recovery/` | Hermes 브라우저·제공자 설정 |

출처와 설치 기준은 [manifest.json](manifest.json), 실행 방법은 [설치 안내](INSTALL_FOR_AGENTS.md)에 있다. Hermes 기본 내장 플러그인을 전부 복제하지 않는다.
