// 종족값 창에 특성·숨겨진 특성·드롭 아이템을 함께 보여 준다 (app.js, items_app.js 다음에 실행)
const iyeyo=w=>{const c=w.charCodeAt(w.length-1)-44032;return w+(c>=0&&c<11172&&c%28?"이에요":"예요");};
function extraOf(p){return PEX_FORM[p.d+"|"+p.form]||PEX[p.d];}
function renderExtra(p){
 const x=extraOf(p),box=document.getElementById("dExtra");
 if(!x){box.innerHTML="";return;}
 const ab=(id,hid)=>{const a=ABIL[id]||[id,""];return `<li><b>${esc(a[0])}</b>${hid?`<span class="hid">숨겨진 특성</span>`:""}${a[1]?`<span class="ad">${esc(a[1])}</span>`:""}</li>`;};
 const abil=x.a.map(id=>ab(id,false)).join("")+(x.h&&!x.a.includes(x.h)?ab(x.h,true):"");
 const same=x.h&&x.a.includes(x.h)?`<p class="dnote">숨겨진 특성도 ${esc(iyeyo((ABIL[x.h]||[x.h])[0]))}.</p>`:"";
 const drops=(x.d||[]).map(([it,pct,q])=>`<li><button type="button" class="ditem" data-item="${esc(it.replace(/ \(.*\)$/,""))}">${esc(it)}</button><span class="rate">${pct}%</span>${q?`<span class="qty">${esc(q)}개</span>`:""}</li>`).join("");
 box.innerHTML=`<div class="shead"><h3>특성</h3></div><ul class="abil">${abil}</ul>${same}`+
  `<div class="shead"><h3>잡거나 쓰러뜨리면 떨어지는 아이템</h3></div>`+(drops?`<ul class="dlist">${drops}</ul><p class="dnote">${x.n?`한 번에 최대 ${x.n}가지까지 떨어져요. `:""}100%는 개수 범위 안에서 항상 나온다는 뜻이에요(0개가 나올 수도 있어요). 아이템을 누르면 아이템 도감에서 찾아 줘요.</p>`:`<p class="dnote">떨어뜨리는 아이템이 없어요.</p>`);}
const _openDetail=openDetail;
openDetail=function(p){_openDetail(p);renderExtra(p);};
document.addEventListener("click",ev=>{const b=ev.target.closest(".ditem");if(!b)return;
 document.getElementById("dlg").close();setTab("items");istate.cat=null;istate.q=b.dataset.item;document.getElementById("iq").value=istate.q;renderItems();window.scrollTo(0,0);});
