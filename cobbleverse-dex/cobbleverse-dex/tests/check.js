// 사용법: node tests/check.js  (build.py와 같은 순서로 src를 읽어서 검사)
const fs=require("fs"),path=require("path"),vm=require("vm");
const src=path.join(__dirname,"..","src");
const gens=fs.readdirSync(src).filter(f=>/^data_gen\d+\.js$/.test(f)).sort((a,b)=>+a.match(/\d+/)[0]-+b.match(/\d+/)[0]);
const code=["data_core.js",...gens,"i18n.js","stats.js","items.js","poke_extra.js"].map(f=>fs.readFileSync(path.join(src,f),"utf8")).join("\n")+"\n;({P,UNLOCK,CATS,STRUCT_KO,BASE,FORM_STATS,MEGA,ITEMS,PEX,PEX_FORM,ABIL})";
const {P,CATS,STRUCT_KO,BASE,MEGA,ITEMS,PEX,PEX_FORM,ABIL}=vm.runInNewContext(code,{console});
let err=0;const bad=m=>{err++;console.log("오류:",m);};
const GENS=[[1,151],[152,251],[252,386],[387,493],[494,649],[650,721],[722,809],[810,905],[906,1025]];
const dex=new Set(P.map(p=>p.d));
GENS.forEach(([a,b],i)=>{const have=[...dex].filter(d=>d>=a&&d<=b).length;if(have===0)return;const miss=[];for(let d=a;d<=b;d++)if(!dex.has(d))miss.push(d);
 console.log(`${i+1}세대: ${have}/${b-a+1}종`+(miss.length?` (위키에 없음 또는 빠짐: ${miss.join(",")})`:""));});
const bmap={};CATS.forEach(([c,o])=>Object.keys(o).forEach(k=>bmap[k]=c));
// 예외: 공식 한국어 이름에 라틴 문자가 들어간 경우(폴리곤Z), 위키에 장소 없이 "Breeding Only"만 적힌 카드(피오네)
const KO_LATIN_OK=new Set(["폴리곤Z"]);
P.forEach(p=>{ if(!p.ko||(/[A-Za-z]/.test(p.ko)&&!KO_LATIN_OK.has(p.ko)))bad(`${p.d} ${p.en}: 한국어 이름이 없거나 영어가 섞임`);
 if(!BASE[p.d])bad(`${p.d} ${p.en}: 종족값 없음`);
 p.entries.forEach(e=>{ if(!"CURX".includes(e.r)||e.r.length!==1)bad(`${p.d} 희귀도 코드 ${e.r}`);
  if(e.c.some(x=>x===undefined))bad(`${p.d} ${p.en}: 조건 키가 K에 없음`);
  (e.b||[]).forEach(b=>{if(!bmap[b])bad(`바이옴 번역 없음: ${b}`)});
  (e.s||[]).forEach(s=>{if(!STRUCT_KO[s])bad(`구조물 번역 없음: ${s}`)});
  if(!e.b&&!e.s&&!e.all&&!e.c.includes("교배로만 얻음"))bad(`${p.d} ${p.en}: 장소가 비어 있음`);});});
Object.entries(BASE).forEach(([d,s])=>{if(s.length!==6||s.some(isNaN))bad(`종족값 형식 ${d}`)});
Object.entries(MEGA).forEach(([d,ms])=>ms.forEach(([n,s])=>{if(!BASE[d])return bad(`${n}: 기본 종족값 없음`);const t=s.reduce((a,b)=>a+b),b=BASE[d].reduce((a,c)=>a+c);if(t-b!==100)console.log(`확인 필요: ${n} 합계 차이 ${t-b} (보통 +100)`)}));
// 아이템 검사: 번역이 빠진 곳은 생성기가 "?영어"로 남긴다
const ICATS=new Set(["held","evo","med","ball","food","tm","plant","block","etc","cv","leader"]);
ITEMS.forEach(it=>{const s=JSON.stringify([it.ko,it.subs.map(x=>[x[1],x[2]]),it.how.map(h=>[h.h,h.t,h.out,h.g,h.in,h.s,h.hdr,h.rows]),(it.use||[]).map(h=>[h.h,h.t,h.list,h.hdr,h.rows])]);
 if(!it.ko||/[A-Za-z]{3,}/.test(it.ko.replace(/DNA/g,"")))bad(`아이템 ${it.en}: 한국어 이름이 없거나 영어가 섞임`);
 if(/"\?[A-Za-z(]/.test(s))bad(`아이템 ${it.en}: 번역 빠짐`);
 if(!ICATS.has(it.cat))bad(`아이템 ${it.en}: 분류 ${it.cat}`);
 if(!it.how.length)bad(`아이템 ${it.en}: 획득 경로 없음`);
 it.how.filter(h=>h.m==="drop").forEach(h=>h.rows.forEach(r=>{if(!dex.has(r[0])&&!BASE[r[0]])bad(`아이템 ${it.en}: 드롭 포켓몬 번호 ${r[0]}`)}));});
// 특성·드롭 검사
for(let d=1;d<=1025;d++)if(!PEX[d])bad(`${d}: 특성·드롭 데이터 없음`);
Object.values({...PEX,...PEX_FORM}).forEach(x=>{[...x.a,x.h].filter(Boolean).forEach(a=>{if(!ABIL[a]||/^\?/.test(ABIL[a][0]))bad(`특성 번역 없음: ${a}`)});(x.d||[]).forEach(r=>{if(/^\?/.test(r[0]))bad(`드롭 아이템 번역 없음: ${r[0]}`)});});
console.log(`아이템: ${ITEMS.length}개`);
console.log(err?`\n오류 ${err}개`:"\n검사 통과");process.exit(err?1:0);
