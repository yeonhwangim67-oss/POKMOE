# 코블버스 도감 — Claude Code 작업 지침

마인크래프트 모드팩 COBBLEVERSE의 포켓몬 출현 정보와 아이템 획득 경로를 한국어로 보여주는 정적 웹페이지다. 화면 위쪽 탭으로 포켓몬 도감과 아이템 도감을 바꿔 본다.
`src/`의 파일을 `build.py`가 합쳐서 `dist/index.html` 한 파일을 만든다. 서버나 외부 라이브러리는 없다.

## 반드시 지킬 규칙

1. **출현 데이터의 출처는 공식 위키만 쓴다.** `https://www.cobbleverse.wiki/spawns/gen1` ~ `gen9` 페이지만 사용한다. 다른 위키, 블로그, 코블몬 기본 데이터로 채우거나 추측하지 않는다. 위키에 없는 포켓몬은 넣지 않고 `NOTES.md`에 적는다.
2. 출처 규칙의 예외는 세 가지뿐이다.
   - 포켓몬 한국어 이름: 공식 한국어 이름을 쓴다.
   - 종족값: 원작 게임 기준(최신 세대 값)을 쓴다.
   - 출현 시점 안내(`UNLOCK`): LUMYVERSE 공식 사이트(lumyverse.com)에 적힌 경우만 넣고, 주석에 출처를 적는다.
   - 아이템 도감(`items.js`)은 별도 출처를 쓴다(아래 "아이템 도감" 참고).
3. 위키 카드 하나를 `e(...)` 항목 하나로 옮긴다. 카드를 합치거나 빼지 않는다. 바이옴 목록은 위키에 적힌 그대로 옮기고, 비슷하다고 다른 목록으로 대충 바꾸지 않는다.
4. UI와 디자인(`shell.html`, `app.js`, `items_app.js`)은 요청이 없으면 바꾸지 않는다. 데이터 파일만 늘린다.
5. 확실하지 않은 것(번역, 종족값, 위키 표기 이상 등)은 지어내지 말고 `NOTES.md`에 목록으로 남긴다.

## 파일 구조

- `src/data_core.js`: 공통 도우미 `e`, `B`, `S`, `OW`, `add`, 조건 사전 `K`, 자주 쓰는 바이옴 묶음(JUNGLE, MOUNT, FOREST 등), `UNLOCK`.
- `src/data_gen1.js`, `src/data_gen2.js`: 세대별 데이터. **새 세대는 `src/data_gen3.js` … `src/data_gen9.js`로 만든다.** build.py가 번호 순서대로 자동으로 읽는다.
- `src/i18n.js`: `CATS`(바이옴 한국어 이름과 분류), `STRUCT_KO`(구조물 한국어 이름).
- `src/stats.js`: `STAT_RAW`(도감 번호 순 종족값), `FORM_STATS`(리전폼), `MEGA`(메가진화).
- `src/items.js`: 아이템 도감 데이터 `ITEMS`.
- `src/app.js`(포켓몬 화면), `src/items_app.js`(아이템 화면), `src/shell.html`: 화면. 요청이 없으면 건드리지 않는다.
- `tests/check.js`: 데이터 검사. `build.py`: 빌드.

## 데이터 형식

```js
add(도감번호, "한국어이름", "English Name", 폼한국어|null, [
  e("희귀도", "레벨", ["조건키", ...], 장소),
]);
```

- 희귀도: Common → `"C"`, Uncommon → `"U"`, Rare → `"R"`, Ultra Rare → `"X"`.
- 레벨: 위키 그대로 문자열 (`"5-32"`, `"60"`).
- 같은 종, 같은 폼의 카드는 한 번의 `add()` 안에 순서대로 넣는다. 폼이 다르면 `add()`를 따로 한다.
- 장소:
  - `B([...바이옴 영어 이름])`: BIOMES / LOCATIONS
  - `S([...구조물 영어 이름])`: STRUCTURES
  - `{b:[...], s:[...]}`: BIOMES & STRUCTURES (둘 다 있는 카드)
  - `OW(["제외"])`: 🌍 Overworld (All Biomes). 🚫 제외 항목이 바이옴 이름이면 영어 그대로(`"Deep Dark"`), "~ Biomes" 같은 묶음이면 한국어 `"OO 계열"`로 쓴다.
  - `NETH`: 🔥 Nether (All Biomes), `END`: 🔮 The End (All Biomes)
- 이미 쓴 묶음 표기: Forest Biomes → `"숲 계열"`, Swamp Biomes → `"늪 계열"`, Freezing Biomes → `"얼음 계열"`, Arid Biomes → `"건조 계열"`, Taiga Biomes → `"타이가 계열"`, Desert Biomes → `"사막 계열"`, Ocean Biomes → `"바다 계열"`, Lush Biomes → `"무성한 계열"`, Volcanic Biomes → `"화산 계열"`, Warm Ocean Biomes → `"따뜻한 바다 계열"`. 새 묶음도 같은 방식으로 만든다.
- 바이옴 목록이 기존 묶음(data_core.js, data_gen2.js의 상수)과 **완전히 같을 때만** 재사용한다. 다르면 세대 파일 위쪽에 새 상수를 만든다.

### 폼 이름 번역

Alolan → `알로라`, Galarian → `가라르`, Hisuian → `히스이`, Paldean → `팔데아`, Valencian → `발렌시아`, `OO Bias` → `OO 계열`(예: Alolan Bias → `알로라 계열`). 그 밖의 폼은 공식 한국어 폼 이름을 쓰고, 없으면 뜻을 살려 옮긴 뒤 NOTES.md에 적는다. 안농처럼 같은 장소에 글자 폼이 여러 개면 기존 2세대처럼 묶어서 한 줄로 만든다.

### 조건 키 (`K`, data_core.js)

위키 표기 → 키: Sky Light 8-15 → `sky`, Sky Light 0-7 → `dim`, Sky Light 0 → `sky0`, Light 0 → `light0`, Clear Weather → `clear`, Day → `day`, Night → `night`, Rain → `rain`, Thunderstorm → `storm`, Nearby Water → `water`, Flowing Water → `flow`, Water (Submerged) → `sub`, Water (Surface) → `surf`, Water (Seafloor) → `floor`, In Water → `inwater`, Must See Sky → `seeSky`, Indoors/Underground → `indoor`, Lava → `inlava`, Special Encounter → `special`, Min/Max Y → `minY0`, `maxY0`, `maxY32`, `maxY48`, `minY48`, `maxY62`, `shipY`(-41~9), `subY`(-60~13), 배율 → `t2`, `t25`, `t5`, `twi`, `twi5`, `n15`, `n025`, `n5`, `d15`, `d025`, `storm33`, `day33`, `rain33`, `lava5`, `water5`, 근처 블록 → `lily`, `redstone`, `rod`, `leek`, `iron`, `lava`, `apri`, `sacch`, `nosacch`, `nowater`, `cobweb`, `sunflower`, `coral`, `deadcoral`, `quartz`, `wool`, `slime`, `moon`.
**새 조건이 나오면 `K`에 키를 추가**하고 값은 짧은 한국어로 쓴다(예: `x2.0 in Snow` → `snow2:"눈 올 때 ×2"`).

### 번역 사전 (i18n.js)

- 새 바이옴은 `CATS`의 알맞은 분류에 `"영어":"한국어"`로 추가한다. 바닐라 바이옴은 마인크래프트 공식 한국어 이름을 쓴다.
- 새 구조물은 `STRUCT_KO`에 추가한다. 지방이 붙은 구조물은 `"Sky Pillar (Hoenn)":"하늘기둥 (호연)"`처럼 괄호 형식을 지킨다. 화면이 괄호 안의 지방 이름으로 "호연 전용 구조물" 표시를 자동으로 만든다.

### 종족값 (stats.js)

- `STAT_RAW`에 도감 번호 순서대로 `"HP 공격 방어 특공 특방 스피드"`를 `|`로 이어서 추가한다. 번호가 하나라도 밀리면 전부 틀어지니 반드시 순서를 지킨다.
- 리전폼처럼 종족값이 다른 폼은 `FORM_STATS["도감번호|폼한국어"]`에 넣는다. 폼 한국어 이름은 data 파일의 폼 이름과 정확히 같아야 한다. 종족값이 같은 폼은 넣지 않는다.
- 메가진화는 `MEGA[도감번호]=[["메가 OO","..."], ...]`. 원작 6세대(X·Y, 오메가루비·알파사파이어)의 메가진화만 넣는다. 메가진화 합계는 보통 기본보다 +100이다.

## 아이템 도감 (items.js)

- 출처
  - 일반 아이템의 획득 경로와 사용법: 코블몬 공식 위키(wiki.cobblemon.com)의 `Category:Item` 문서, 그리고 분류가 빠져 있지만 아이템·블록 정보 상자가 있는 문서(민트, 민트 잎, 민트 씨앗, TM 머신, 진화의돌 광석 등). 위키 문서 하나를 `itm({...})` 하나로 옮긴다.
  - 코블버스 전용 아이템: LUMYVERSE `special-items-where-find-them` 표. 관장 소환 아이템: `signature-items` 페이지.
  - 아이템·재료 이름과 효과 설명: 코블몬, Mega Showdown, 마인크래프트의 게임 안 한국어 번역 파일(ko_kr.json)을 그대로 쓴다. 번역 파일에 없는 코블버스 전용 이름은 뜻을 살려 옮기고 NOTES.md에 적는다.
- 형식: `itm({en, ko, cat, src, mod?, subs:[[영어, 한국어, 효과]], how:[경로...], use?:[사용법...]})`
  - `cat`: held(지닌 물건), evo(진화), med(회복·성장), ball(몬스터볼·낚싯대), food(요리·음식), tm(기술머신·주얼), plant(작물·열매), block(블록·설비), etc(재료·기타), cv(코블버스 전용), leader(관장 소환)
  - 경로 `m`: craft/cook(`g`: 3×3 칸 9개, `s`: 양념 칸, `free`: 모양 무관), brew/smelt/smith/input(`in` → `out`), drop(`rows`: [도감번호, 폼, 확률, 개수]), text(`t`), table(`hdr`, `rows`). `h`는 소제목.
  - 사용법 `use`: 위키 "Usage" 절의 text/table과, 이 아이템을 재료로 만드는 결과물 목록 `{m:"made", list:[...]}`.
- 위키 문장은 획득 방법(`how`)과 사용법(`use`)만 옮긴다. 한 줄 효과는 게임 번역의 툴팁을 쓴다.

## 작업 순서 (세대 하나마다)

1. `https://www.cobbleverse.wiki/spawns/genN` 을 읽는다. 페이지가 길면 나눠 읽되 **도감 번호가 빠지지 않게** 끝까지 확인한다.
2. `src/data_genN.js`를 만든다. 파일 맨 위에 `// ---- N세대 (cobbleverse.wiki/spawns/genN) ----` 주석을 단다.
3. 새 조건 키, 바이옴, 구조물 번역을 추가한다.
4. 종족값, 리전폼, 메가진화를 추가한다.
5. `node tests/check.js` 가 "검사 통과"가 될 때까지 고친다.
6. `python build.py` 로 `dist/index.html`을 만든다.
7. 커밋한다: `feat: N세대 출현 데이터 추가`.

다 끝나면 세대별 종 수, 새로 추가한 번역 개수, `NOTES.md`의 확인 필요 목록을 요약해서 보고한다.
