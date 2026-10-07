const RAR={C:{ko:"흔함",cls:"r-c"},U:{ko:"드묾",cls:"r-u"},R:{ko:"레어",cls:"r-r"},X:{ko:"울트라 레어",cls:"r-x"}};
const RORDER=["C","U","R","X"];
const BKO={},BCAT={};CATS.forEach(([c,o])=>Object.entries(o).forEach(([en,ko])=>{BKO[en]=ko;BCAT[en]=c;}));
const NETHER=new Set(Object.keys(CATS.find(c=>c[0]==="네더")[1]));
const ALLKO={ow:"오버월드 어디서나",nether:"네더 어디서나",end:"엔드 어디서나"};
const state={loc:null,rar:new Set(),q:"",gen:0};
const GENS=[[1,151,"관동"],[152,251,"성도"],[252,386,"호연"],[387,493,"신오"],[494,649,"하나"],[650,721,"칼로스"],[722,809,"알로라"],[810,905,"가라르"],[906,1025,"팔데아"]];
const genOf=d=>GENS.findIndex(g=>d>=g[0]&&d<=g[1])+1;
const REG={"Kanto":"관동","Johto":"성도","Hoenn":"호연","Sinnoh":"신오","Nether":"네더","End":"엔드"};
function notesFor(p){const n=[];if(UNLOCK[p.d])n.push(UNLOCK[p.d]);const regs=new Set();let sp=false;p.entries.forEach(e=>{if(e.c.includes("특수 조우"))sp=true;(e.s||[]).forEach(s=>{const m=s.match(/\((Kanto|Johto|Hoenn|Sinnoh|Nether|End)\)$/);if(m)regs.add(REG[m[1]]);});});regs.forEach(r=>n.push(r+" 전용 구조물"));if(sp)n.push("특수 조우");return n;}
const CHO="ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ";
const cho=s=>[...s].map(ch=>{const c=ch.charCodeAt(0)-44032;return c>=0&&c<11172?CHO[Math.floor(c/588)]:ch;}).join("");
const isCho=s=>/^[ㄱ-ㅎ\s]+$/.test(s);
P.sort((a,b)=>a.d-b.d||(a.form?1:0)-(b.form?1:0));
P.forEach((p,i)=>{p.i=i;p.notes=notesFor(p);p.key=(p.ko+(p.form||"")+p.en).toLowerCase();p.cho=cho(p.ko+(p.form||""));});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function locOK(e,loc){
 if(!loc)return true;
 if(loc.t==="b"){const n=loc.v;
  if(e.b&&e.b.includes(n))return true;
  if(e.all==="ow"&&!NETHER.has(n)&&!(e.ex||[]).includes(n))return true;
  if(e.all==="nether"&&NETHER.has(n))return true;
  return false;}
 if(loc.t==="s")return !!(e.s&&e.s.includes(loc.v));
 if(loc.t==="a")return e.all===loc.v;
 return true;}
function matchEntries(p,loc,rar){return p.entries.filter(e=>(rar.size===0||rar.has(e.r))&&locOK(e,loc));}
function searchOK(p,q){if(!q)return true;const s=q.toLowerCase().trim();if(!s)return true;
 if(/^\d+$/.test(s))return p.d===+s;
 if(isCho(s))return p.cho.includes(s.replace(/\s/g,""));
 return p.key.includes(s.replace(/\s/g,""))||p.key.replace(/\s/g,"").includes(s.replace(/\s/g,""));}

function placeHTML(e){
 const parts=[];
 if(e.all){let t=ALLKO[e.all];if(e.ex&&e.ex.length)t+=` <span class="ex">(제외: ${e.ex.map(x=>esc(BKO[x]||x)).join(", ")})</span>`;parts.push(`<span class="pl all">${t}</span>`);}
 (e.s||[]).forEach(s=>parts.push(`<span class="pl st">${esc(STRUCT_KO[s]||s)}</span>`));
 const b=(e.b||[]);
 if(b.length){const shown=b.slice(0,4).map(x=>`<span class="pl">${esc(BKO[x]||x)}</span>`).join("");
  if(b.length>4){parts.push(shown+`<details class="more"><summary>외 ${b.length-4}곳</summary>${b.slice(4).map(x=>`<span class="pl">${esc(BKO[x]||x)}</span>`).join("")}</details>`);}
  else parts.push(shown);}
 return parts.join("");}

function rowHTML(p,ents){
 const rs=RORDER.filter(r=>ents.some(e=>e.r===r));
 const lines=ents.map(e=>`<li class="ent"><span class="dot ${RAR[e.r].cls}" title="${RAR[e.r].ko}"></span><div class="ent-body"><div class="ent-top"><b>Lv ${esc(e.lv)}</b>${e.c.map(c=>`<span class="cond">${esc(c)}</span>`).join("")}</div><div class="places">${placeHTML(e)}</div></div></li>`).join("");
 return `<tr><td class="c-no">${String(p.d).padStart(4,"0")}</td><td class="c-name"><button type="button" class="nm" data-i="${p.i}"><span class="ko">${esc(p.ko)}</span>${p.form?`<span class="form">${esc(p.form)}</span>`:""}<span class="en">${esc(p.en)}</span></button>${p.notes.map(t=>`<span class="note">${esc(t)}</span>`).join("")}</td><td class="c-rar">${rs.map(r=>`<span class="badge ${RAR[r].cls}">${RAR[r].ko}</span>`).join("")}</td><td class="c-spawn"><ul>${lines}</ul></td></tr>`;}

const SPECIES=new Set(P.map(p=>p.d)).size;
document.querySelector(".brand p").textContent=`${SPECIES}종 수록, COBBLEVERSE 모드팩 데이터 기준`;
function render(){
 const tb=document.getElementById("rows");let n=0,html="";const sp=new Set();
 for(const p of P){if(state.gen&&genOf(p.d)!==state.gen)continue;if(!searchOK(p,state.q))continue;const ents=matchEntries(p,state.loc,state.rar);if(!ents.length)continue;n++;sp.add(p.d);html+=rowHTML(p,ents);}
 tb.innerHTML=html;
 const emp=document.getElementById("empty");emp.hidden=n>0;emp.textContent=(state.gen&&!P.some(p=>genOf(p.d)===state.gen))?`${state.gen}세대는 아직 추가하지 않았어요.`:"조건에 맞는 포켓몬이 없어요. 등급이나 바이옴 선택을 줄여 보세요.";
 const where=state.loc?(state.loc.t==="b"?BKO[state.loc.v]:state.loc.t==="s"?STRUCT_KO[state.loc.v]:ALLKO[state.loc.v]):"모든 장소";
 const rt=state.rar.size?RORDER.filter(r=>state.rar.has(r)).map(r=>RAR[r].ko).join(", "):"모든 등급";
 const gt=state.gen?`${state.gen}세대, `:"";document.getElementById("status").textContent=`${gt}${where}, ${rt}: ${sp.size}종 (${n}줄)`;
 document.getElementById("clearLoc").hidden=!state.loc;
 document.querySelectorAll(".loc").forEach(el=>{const on=state.loc&&el.dataset.t===state.loc.t&&el.dataset.v===state.loc.v;el.classList.toggle("on",!!on);el.setAttribute("aria-pressed",on?"true":"false");});
 document.querySelectorAll(".ore").forEach(el=>{const on=state.rar.has(el.dataset.r);el.classList.toggle("on",on);el.setAttribute("aria-pressed",on?"true":"false");});
 const pick=document.getElementById("pickLabel");if(pick)pick.textContent=state.loc?where:"바이옴 고르기";}

function countFor(loc){const s=new Set();P.forEach(p=>{if(p.entries.some(e=>locOK(e,loc)))s.add(p.d);});return s.size;}
function buildSide(){
 const side=document.getElementById("biomes");let h="";
 const filt=document.getElementById("bfilter").value.trim();
 const fm=(ko,en)=>!filt||ko.includes(filt)||en.toLowerCase().includes(filt.toLowerCase())||(isCho(filt)&&cho(ko).includes(filt.replace(/\s/g,"")));
 const btn=(t,v,ko,en)=>`<button type="button" class="loc" data-t="${t}" data-v="${esc(v)}"><span class="lk">${esc(ko)}</span><em>${countFor({t,v})}</em>${en?`<small>${esc(en)}</small>`:""}</button>`;
 const sp=[["a","ow",ALLKO.ow,""],["a","nether",ALLKO.nether,""],["a","end",ALLKO.end,""]].filter(x=>fm(x[2],x[3]));
 if(sp.length)h+=`<section><h3>어디서나</h3>${sp.map(x=>btn(...x)).join("")}</section>`;
 CATS.forEach(([c,o])=>{const items=Object.entries(o).filter(([en,ko])=>fm(ko,en)).sort((a,b)=>a[1].localeCompare(b[1],"ko"));if(items.length)h+=`<section><h3>${c}</h3>${items.map(([en,ko])=>btn("b",en,ko,en)).join("")}</section>`;});
 const st=Object.entries(STRUCT_KO).filter(([en,ko])=>fm(ko,en));if(st.length)h+=`<section><h3>구조물</h3>${st.map(([en,ko])=>btn("s",en,ko,en)).join("")}</section>`;
 side.innerHTML=h||`<p class="none">"${esc(filt)}"에 맞는 바이옴이 없어요.</p>`;render();}

document.addEventListener("click",ev=>{
 const l=ev.target.closest(".loc");if(l){const nl={t:l.dataset.t,v:l.dataset.v};state.loc=(state.loc&&state.loc.t===nl.t&&state.loc.v===nl.v)?null:nl;render();const d=document.getElementById("pick");if(d&&window.matchMedia("(max-width: 860px)").matches)d.open=false;return;}
 const o=ev.target.closest(".ore");if(o){const r=o.dataset.r;state.rar.has(r)?state.rar.delete(r):state.rar.add(r);render();return;}
 if(ev.target.closest("#clearLoc")){state.loc=null;render();}
 if(ev.target.closest("#clearAll")){state.loc=null;state.rar.clear();state.q="";state.gen=0;document.getElementById("q").value="";document.getElementById("gen").value="0";render();}
 const nm=ev.target.closest(".nm");if(nm){openDetail(P[+nm.dataset.i]);return;}
 if(ev.target.closest("#megaKey")){cycleMega();return;}
 if(ev.target.closest("#closeDlg")){document.getElementById("dlg").close();}});
document.getElementById("gen").addEventListener("change",e=>{state.gen=+e.target.value;render();});
document.getElementById("q").addEventListener("input",e=>{state.q=e.target.value;render();});
document.getElementById("bfilter").addEventListener("input",buildSide);
document.addEventListener("keydown",e=>{if(e.key==="/"&&document.activeElement.tagName!=="INPUT"){e.preventDefault();document.getElementById("q").focus();}});
if(window.matchMedia("(max-width: 860px)").matches)document.getElementById("pick").open=false;
buildSide();

const SLABEL=["체력","공격","방어","특수공격","특수방어","스피드"];
let cur=null,megaIdx=-1;
function baseOf(p){return FORM_STATS[p.d+"|"+p.form]||BASE[p.d];}
function megasOf(p){return p.form?[]:(MEGA[p.d]||[]);}
function drawStats(){
 const p=cur,base=baseOf(p),ms=megasOf(p),m=megaIdx>=0?ms[megaIdx]:null,st=m?m[1]:base;
 const box=document.getElementById("stats");
 box.classList.toggle("mega",!!m);
 box.innerHTML=SLABEL.map((l,i)=>{const v=st[i],d=v-base[i];return `<div class="srow"><span class="sl">${l}</span><span class="sv">${v}${m&&d?`<em class="${d>0?"up":"dn"}">${d>0?"+":""}${d}</em>`:""}</span><span class="track"><span class="fill" style="width:${Math.min(100,v/255*100).toFixed(1)}%"></span></span></div>`;}).join("")+`<div class="srow total"><span class="sl">합계</span><span class="sv">${st.reduce((a,b)=>a+b,0)}</span><span></span></div>`;
 const k=document.getElementById("megaKey"),kl=document.getElementById("megaLabel");
 k.disabled=!ms.length;k.setAttribute("aria-pressed",m?"true":"false");k.classList.toggle("on",!!m);
 kl.textContent=!ms.length?"메가진화 없음":m?m[0]:(ms.length>1?"메가진화 ("+ms.length+"가지)":"메가진화");
 document.getElementById("dTitle").textContent=m?m[0]:p.ko;
}
function cycleMega(){const ms=megasOf(cur);if(!ms.length)return;megaIdx=megaIdx+1>=ms.length?-1:megaIdx+1;drawStats();}
function openDetail(p){cur=p;megaIdx=-1;
 document.getElementById("dNo").textContent="No."+String(p.d).padStart(4,"0")+"  "+genOf(p.d)+"세대 "+GENS[genOf(p.d)-1][2];
 document.getElementById("dSub").innerHTML=(p.form?`<span class="form">${esc(p.form)}</span>`:"")+`<span class="en">${esc(p.en)}</span>`;
 const rs=RORDER.filter(r=>p.entries.some(e=>e.r===r));
 document.getElementById("dRar").innerHTML=rs.map(r=>`<span class="badge ${RAR[r].cls}">${RAR[r].ko}</span>`).join("")+p.notes.map(t=>`<span class="note">${esc(t)}</span>`).join("");
 drawStats();document.getElementById("dlg").showModal();}
