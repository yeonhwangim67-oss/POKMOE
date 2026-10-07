# 모드팩 데이터 → 도감 데이터 변환 도구

출현(`src/data_gen1..9.js`)과 특성·드롭(`src/poke_extra.js`)을 COBBLEVERSE 모드팩 안의 실제 데이터로 만든다.

## 준비 (작업 폴더 하나에)

- `mrpack/x/`: 모드팩 `.mrpack`을 푼 폴더 (`overrides/datapacks/COBBLEVERSE-DP-v31.zip`, `overrides/datapacks/extra/*.zip`)
- `mrpack/jars/`: 모드 jar (`modrinth.index.json`의 주소로 받음). 코블몬, Mega Showdown, cobblemon-additions, fabric convention tags v1·v2, 마인크래프트 클라이언트 jar(`mc-client-1.21.1.jar`) 포함
- `species/1.7.3/*.json`: 코블몬 jar의 `data/cobblemon/species/**` 를 한 폴더에 모은 것
- `cw/mc_en.json`, `cw/mc_ko.json`: 마인크래프트 언어 파일, `cw/ko_kr.json`: 코블몬 한국어, `msd/ko.json`: Mega Showdown 한국어
- `ref.json`의 `ko`: 도감번호 → 공식 한국어 이름
- `cur_wiki.json`: 예전 위키 기반 데이터를 `node dump.js src`로 뽑은 것 (장소가 없는 전설·되살리기 머신 항목만 가져다 씀)

## 순서

```
python3 -I dp_collect.py          # dpwork/spawns.json: 유효 출현 파일(코블몬 < cobblemon-additions < 데이터팩)과 프리셋
python3 -I dp_tags.py             # dpwork/tags.json
python3 -I dp_conv.py             # dpwork/cards.json, 못 옮긴 조건 목록 출력
node core_consts.js <src>/data_core.js > dpwork/core_consts.json
python3 -I dp_gen.py <src>        # data_gen1..9.js (맨 끝 UNLOCK 줄은 그대로 남김)
node dump.js <src> > new.json
python3 -I pex_gen.py <src>/poke_extra.js
```

도구는 작업 폴더에서 `tools/` 아래에 두고 실행한다고 가정한다(`sys.path.insert(0,'tools')`).

## 규칙 요약

- 낚시 출현은 뺀다. 빈티나·밀로틱처럼 낚시로만 나오는 종은 넣는다(`fish`).
- 설치되지 않은 모드(aether, biomesoplenty, byg, betternether 등)의 바이옴만 있는 항목은 실제로 나올 수 없어서 뺀다.
- 바이옴 태그는 Terralith 데이터팩이 태그에 더한 값을 빼고 푼다(예전 위키와 같은 방식).
- 화면에 똑같이 보이는 항목은 한 줄로 합친다.
