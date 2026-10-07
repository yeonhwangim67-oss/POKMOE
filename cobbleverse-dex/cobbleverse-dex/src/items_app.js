// 아이템 도감 화면 (app.js 다음에 실행. app.js의 esc, cho, isCho, P, openDetail을 함께 씀)
const ICAT=[["held","지닌 물건"],["evo","진화 아이템"],["med","회복·성장"],["ball","몬스터볼·낚싯대"],["food","요리·음식"],["tm","기술머신·주얼"],["plant","작물·열매"],["etc","재료·기타"],["cv","코블버스 전용"],["leader","관장 소환"]];
const ICATKO=Object.fromEntries(ICAT);
const MLABEL={craft:"제작",cook:"요리",brew:"양조",smelt:"제련",smith:"대장장이 작업대",input:"기타",drop:"포켓몬 드롭",text:"획득 방법",table:"표"};
const MPLACE={craft:"작업대",cook:"모닥불 냄비",brew:"양조기",smelt:"화로",smith:"대장장이 작업대"};
const istate={cat:null,q:""};
const POKE_BY_DEX={};P.forEach(p=>{if(!p.form&&!POKE_BY_DEX[p.d])POKE_BY_DEX[p.d]=p;});
ITEMS.forEach((it,i)=>{it.i=i;
 const words=[it.ko,it.en,...it.subs.flatMap(s=>[s[0],s[1]])];
 it.how.forEach(h=>{if(h.out)words.push(h.out);(h.g||[]).forEach(x=>x&&words.push(x));(h.in||[]).forEach(x=>x&&words.push(x));(h.s||[]).forEach(x=>x&&words.push(x));});
 it.key=words.join(" ").toLowerCase().replace(/\s/g,"");it.cho=cho(words.filter(w=>/[가-힣]/.test(w)).join(""));});

function iSearchOK(it,q){const s=q.toLowerCase().replace(/\s/g,"");if(!s)return true;if(isCho(s))return it.cho.includes(s);return it.key.includes(s);}
function gridHTML(h){
 const names=[];const idx=x=>{if(!x)return "";let k=names.indexOf(x);if(k<0){names.push(x);k=names.length-1;}return k+1;};
 const cells=(h.g||[]).map(x=>{const n=idx(x);return `<span class="gc${n?" on":""}"${n?` title="${esc(x)}"`:""}>${n||""}</span>`;}).join("");
 const seas=h.s?`<div class="seas"><span class="sl2">양념</span>${h.s.map(x=>`<span class="gc${x?" on":""}"${x?` title="${esc(x)}"`:""}>${x?idx(x):""}</span>`).join("")}</div>`:"";
 const legend=names.map((n,i)=>`<li><b>${i+1}</b>${esc(n)}</li>`).join("");
 return `<div class="recipe"><div class="gridbox"><div class="grid3">${cells}</div>${seas}</div><span class="arrow" aria-hidden="true">→</span><span class="outp">${esc(h.out||"")}</span><ol class="legend">${legend}</ol>${h.free?`<p class="free">모양 상관없이 재료만 넣으면 돼요.</p>`:""}</div>`;}
function routeHTML(h){
 const m=h.m;
 if(m==="craft"||m==="cook")return gridHTML(h);
 if(m==="brew")return `<div class="flow"><span class="chip">${esc(h.in[0]||"")}</span><span class="plus">+</span><span class="chip">${esc(h.in[1]||"")}</span><span class="arrow">→</span><span class="outp">${esc(h.out||"")}</span></div><p class="sub2">아래 칸에 앞의 것, 위 칸에 뒤의 재료를 넣어요.</p>`;
 if(m==="smelt"||m==="input"||m==="smith")return `<div class="flow">${(h.in||[]).filter(Boolean).map(x=>`<span class="chip">${esc(x)}</span>`).join('<span class="plus">+</span>')}<span class="arrow">→</span><span class="outp">${esc(h.out||"")}</span></div>`;
 if(m==="drop")return `<ul class="drops">${h.rows.map(([d,f,rate,q])=>{const p=POKE_BY_DEX[d];const nm=p?p.ko:"No."+d;return `<li><button type="button" class="dp" data-d="${d}"><span class="no">${String(d).padStart(4,"0")}</span>${esc(nm)}${f?` <span class="form">${esc(f)}</span>`:""}</button><span class="rate">${esc(rate)}</span>${q?`<span class="qty">×${esc(q)}</span>`:""}</li>`;}).join("")}</ul>`;
 if(m==="text")return `<p class="ht">${esc(h.t)}</p>`;
 if(m==="table")return `<div class="tw"><table class="mini"><thead><tr>${h.hdr.map(x=>`<th>${esc(x)}</th>`).join("")}</tr></thead><tbody>${h.rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
 return "";}
function groupsOf(it){const g=[];it.how.forEach(h=>{const label=h.h||MLABEL[h.m];let last=g[g.length-1];if(!last||last.label!==label){last={label,place:MPLACE[h.m]&&!h.h?MPLACE[h.m]:(MPLACE[h.m]||""),list:[]};g.push(last);}last.list.push(h);});return g;}
function itemHTML(it,open){
 const q=istate.q.toLowerCase().replace(/\s/g,"");
 const hit=x=>JSON.stringify(x).toLowerCase().replace(/\s/g,"").includes(q);
 const narrow=q&&!isCho(q)&&!(it.ko+it.en).toLowerCase().replace(/\s/g,"").includes(q);
 const how=narrow?it.how.filter(h=>h.m!=="text"&&hit([h.out,h.g,h.in,h.s,h.h])):it.how;
 const hidden=it.how.length-how.length;
 const subsShown=narrow?it.subs.filter(x=>hit([x[0],x[1]])):it.subs;
 const gs=groupsOf({how});
 const methods=[...new Set(how.map(h=>h.h||MLABEL[h.m]))];
 const subs=it.subs.length>1||(it.subs[0]&&it.subs[0][1]!==it.ko)
  ?`<ul class="subs">${subsShown.map(s=>`<li><b>${esc(s[1])}</b>${s[2]?`<span>${esc(s[2])}</span>`:""}</li>`).join("")}</ul>`
  :(it.subs[0]&&it.subs[0][2]?`<p class="eff">${esc(it.subs[0][2])}</p>`:"");
 const body=gs.map(g=>`<section class="rg"><h4>${esc(g.label)}${g.place?`<small>${esc(g.place)}</small>`:""}</h4>${g.list.map(routeHTML).join("")}</section>`).join("");
 return `<article class="itm"><header><div class="ih"><h3>${esc(it.ko)}</h3><span class="en">${esc(it.en)}</span></div><div class="tags"><span class="tag">${esc(ICATKO[it.cat]||"")}</span>${it.mod?`<span class="tag src">${esc(it.mod)}</span>`:""}</div></header>${subs}
 <details class="routes"${open?" open":""}><summary><span class="sum-l">얻는 방법</span>${methods.map(m=>`<span class="mchip">${esc(m)}</span>`).join("")}</summary>${body||'<p class="ht">알려진 획득 방법이 없어요.</p>'}${hidden?`<p class="more2">검색어와 관계없는 경로 ${hidden}개는 숨겼어요. 검색어를 지우면 모두 보여요.</p>`:""}</details></article>`;}
function renderItems(){
 const list=ITEMS.filter(it=>(!istate.cat||it.cat===istate.cat)&&iSearchOK(it,istate.q));
 const open=list.length<=4;
 document.getElementById("itemList").innerHTML=list.map(it=>itemHTML(it,open)).join("")||`<p id="iempty">조건에 맞는 아이템이 없어요.</p>`;
 document.getElementById("istatus").textContent=`${istate.cat?ICATKO[istate.cat]:"모든 분류"}${istate.q?`, "${istate.q}" 검색`:""}: ${list.length}개`;
 document.querySelectorAll(".icat").forEach(b=>{const on=(b.dataset.c||null)===istate.cat;b.classList.toggle("on",on);b.setAttribute("aria-pressed",on?"true":"false");});}
function buildICats(){
 const n=c=>ITEMS.filter(it=>!c||it.cat===c).length;
 document.getElementById("icats").innerHTML=`<section><h3>분류</h3><button type="button" class="loc icat" data-c=""><span class="lk">전체</span><em>${n(null)}</em></button>${ICAT.map(([c,k])=>`<button type="button" class="loc icat" data-c="${c}"><span class="lk">${k}</span><em>${n(c)}</em></button>`).join("")}</section>`;}
function setTab(t){
 const items=t==="items";
 document.querySelectorAll(".tab").forEach(b=>{const on=b.dataset.tab===t;b.classList.toggle("on",on);b.setAttribute("aria-selected",on?"true":"false");});
 document.getElementById("pokeView").hidden=items;document.getElementById("itemView").hidden=!items;
 document.querySelector(".gen").hidden=items;document.querySelector(".search").hidden=items;
 document.querySelector(".brand p").textContent=items?`아이템 ${ITEMS.length}개 수록, 코블몬 공식 위키·LUMYVERSE 기준`:`${SPECIES}종 수록, COBBLEVERSE 공식 위키 기준`;
 try{localStorage.setItem("dexTab",t);}catch(e){}}
document.addEventListener("click",ev=>{
 const tb=ev.target.closest(".tab");if(tb){setTab(tb.dataset.tab);return;}
 const c=ev.target.closest(".icat");if(c){istate.cat=c.dataset.c||null;renderItems();const d=document.getElementById("ipick");if(d&&window.matchMedia("(max-width: 860px)").matches)d.open=false;return;}
 const dp=ev.target.closest(".dp");if(dp){const p=POKE_BY_DEX[+dp.dataset.d];if(p)openDetail(p);return;}
 if(ev.target.closest("#iclear")){istate.cat=null;istate.q="";document.getElementById("iq").value="";renderItems();}});
document.getElementById("iq").addEventListener("input",e=>{istate.q=e.target.value;renderItems();});
if(window.matchMedia("(max-width: 860px)").matches)document.getElementById("ipick").open=false;
buildICats();renderItems();
let _tab="poke";try{_tab=localStorage.getItem("dexTab")||"poke";}catch(e){}
setTab(_tab==="items"?"items":"poke");
