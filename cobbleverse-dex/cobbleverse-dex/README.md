# 코블버스 도감

COBBLEVERSE 공식 위키(cobbleverse.wiki)의 포켓몬 출현 정보와, 코블몬 공식 위키·LUMYVERSE의 아이템 획득 경로를 한국어로 정리한 페이지예요. 위쪽 탭으로 포켓몬/아이템을 바꿔 볼 수 있어요.

## 바로 보기
`dist/index.html` 파일을 브라우저로 열면 돼요.

## 파일 설명
- `src/` : 원본 파일. 세대별 데이터는 `data_gen1.js`, `data_gen2.js` …, 아이템 데이터는 `items.js`
- `build.py` : `src/`를 합쳐서 `dist/index.html`을 만들어요. (`python build.py`)
- `tests/check.js` : 데이터에 빠진 번역이나 종족값이 없는지 검사해요. (`node tests/check.js`)
- `CLAUDE.md` : Claude Code가 읽는 작업 규칙이에요.
- `PROMPT.md` : Claude Code에 처음 보낼 메시지예요.
- `NOTES.md` : 확인이 필요한 항목을 Claude Code가 적어 두는 곳이에요.

## 인터넷 주소로 공개하기 (선택)
GitHub 레포지토리의 Settings → Pages에서 브랜치를 고르고 저장하면,
`https://아이디.github.io/cobbleverse-dex/dist/` 주소로 친구들과 볼 수 있어요.
