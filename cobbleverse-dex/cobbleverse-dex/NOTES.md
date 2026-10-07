# 확인 필요 목록

Claude Code가 작업하면서 확실하지 않은 번역, 종족값, 위키 표기 이상을 여기에 적어요.

## 공통
- 포켓몬 한국어 이름과 종족값은 npm 패키지 `pokemon`(공식 다국어 이름)과 `@pkmn/dex`(원작 최신 세대 종족값)로 확인했어요. 이 두 자료는 기존 1~2세대 251종의 이름·종족값과 모두 일치했어요.
- 모드 바이옴(Terralith 등)과 모드 구조물은 공식 한국어 이름이 없어서 뜻을 살려 옮겼어요. 아래 세대별 목록에 적었어요.
- 메가진화는 원작 6세대(X·Y, 오메가루비·알파사파이어) 것만 넣었어요. Legends Z-A에서 새로 나온 메가진화와 원시회귀(가이오가·그란돈)는 넣지 않았어요.
- `app.js`의 지방 전용 구조물 표시는 관동·성도·호연·신오·네더·엔드만 알아봐요. 하나·칼로스·알로라·가라르·팔데아 구조물은 이름에 괄호 지방이 있어도 "OO 전용 구조물" 표시가 붙지 않아요(화면 코드는 고치지 않았어요).

## 기존 데이터(1세대)에서 발견한 것
- 77 포니타, 78 날쌩마: 위키 카드의 바이옴 목록에는 `Sunflower Plains`가 없는데 data_gen1.js에는 들어 있어요(`RAT` 상수 사용). 이번 작업 범위가 아니라 고치지 않았어요.

## 3세대
- 384 레쿠쟈: 위키에 기본 폼 카드가 없고 두 장뿐이에요.
  - "Shiny" + "⚠️ Only 1 per Player!" 배지 카드(엔드 출구, Lv.100) → 폼 이름 `색이 다른 개체 (플레이어당 1마리)`로 옮김.
  - "Mega" 배지 카드(하늘기둥, Lv.70-80) → 폼 이름 `메가`. 종족값이 달라서 `FORM_STATS["384|메가"]`에 메가레쿠쟈 값을 넣었어요.
- 351 캐스퐁 폼: Sunny/Rainy/Snowy → 공식 이름 `태양의 모습`/`빗방울의 모습`/`설운의 모습`.
- 327 얼루기 "Special Pattern" → 1세대 아보와 같은 `특수 무늬`로 옮김.
- 새 조건 번역: `Sky Light: 1-15` → "하늘빛 1–15", `x5.0 during Full Moon` → "보름달 때 ×5", `Bell` → "종 근처", `Coal Ores` → "석탄 광석 근처", `Deep Ocean Biomes` → "깊은 바다 계열".
- 모드 바이옴 의미 번역: Sulfur Caves 유황 동굴, Andesite Caves 안산암 동굴, Desert Caves 사막 동굴, Diorite Caves 섬록암 동굴, Granite Caves 화강암 동굴.
- 구조물 의미 번역: Secret Garden (Hoenn) 비밀 정원, Luna/Sol Henge Ruins 루나/솔 헨지 유적, Regirock/Regice/Registeel Temple 레지락/레지아이스/레지스틸 신전, Kyogre Dome 가이오가 돔, Groudon Volcano 그란돈 화산, Wish Cave 소원 동굴, Deoxys Meteorite 테오키스 운석.
- `End Podium`(엔드 드래곤을 잡으면 나오는 출구 차원문 받침대)의 마인크래프트 공식 한국어 이름을 확인하지 못해서 `엔드 출구 차원문`으로 적었어요.
- 메가진화 제외: 358 치렁(메가치렁), 359 앱솔의 메가앱솔 Z는 Legends Z-A 신규라 넣지 않았어요.

## 4세대
- 489 피오네: 위키 카드에 장소 없이 "Breeding Only↗"(교배로만 얻음)만 적혀 있어요. 카드를 빼지 않으려고 장소 없이 `e("X","1",["breed","special"],{})`로 넣었고, `tests/check.js`에 이 경우만 "장소가 비어 있음" 검사에서 빼는 예외를 넣었어요.
- 474 폴리곤Z: 공식 한국어 이름에 라틴 문자 Z가 있어서 `tests/check.js`의 "영어가 섞임" 검사에 예외로 넣었어요.
- 폼 이름(공식): 도롱충이·도롱마담 초목도롱/모래땅도롱/슈레도롱, 체리꼬 네거티브폼/포지티브폼, 깝질무·트리토돈 동쪽바다의 모습/서쪽바다의 모습. 도롱마담 모래땅도롱·슈레도롱은 종족값이 달라 `FORM_STATS`에 넣었어요.
- 새 조건 번역: `X > 0`/`X < 0` → "X 좌표 0보다 큼/작음", `Bee Nest` → "벌집 근처", `Flowers, Saccharine Trees`(둘 중 하나) → "꽃/사카린 나무 근처", 로토무의 긴 블록 목록(레드스톤 블록·중계기·PC·모니터·회복 머신·복원 탱크·화석 분석기 등) → 한 키 "레드스톤 장치·PC·회복 머신 등 근처"로 줄였어요.
- 새 묶음: Badlands Biomes 악지 계열, Floral Biomes 꽃 계열, Mountain Biomes 산 계열.
- 구조물: 바닐라 Jungle Pyramid 정글 사원, Desert Pyramid 사막 사원, Ancient City 고대 도시. 원작 지명은 진실호수(Verity)·예지호수(Acuity)·입지호수(Valor), 창기둥, 깨어진 세계, 만월섬, 신월섬, 꽃의 낙원으로 옮겼어요.
- 확신이 없는 구조물 번역: `Stark Mountain (Nether)` → "하드마운틴 (네더)", `Snowpoint Temple (Sinnoh)` → "선단 신전 (신오)"(선단시티 = Snowpoint City로 봄), `Temple of Sinnoh` → "신오 신전", `Temple of the Sea` → "바다의 신전", `Cobblemon Ruins` → "코블몬 유적", `Crumbling/Rooted Arch Ruins` → "무너진/뿌리 내린 아치 유적".
- 메가진화 제외(Legends Z-A 신규): 398 찌르호크, 478 눈여아, 485 히드런, 491 다크라이, 445 한카리아스·448 루카리오의 메가 Z.
