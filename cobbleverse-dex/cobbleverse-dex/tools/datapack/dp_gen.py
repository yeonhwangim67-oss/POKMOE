# dpwork/cards.json -> src/data_gen1..9.js
import json,re,collections,sys,glob
SRC=sys.argv[1]
cards=json.load(open('dpwork/cards.json')); core=json.load(open('dpwork/core_consts.json'))
ref=json.load(open('ref.json')); cur=json.load(open('cur_wiki.json'))
WIKI_S={}
for p in cur['P']:
    if not p['form'] and p['entries'] and 's' in p['entries'][0]: WIKI_S.setdefault(p['d'],p['entries'][0]['s'])
FALLBACK=[]
# 출현 풀 밖에서 얻는 방법(되살리기 머신, 엔드 포털 받침대)은 위키 카드를 그대로 덧붙인다
WIKI_EXTRA=[(p['d'],p['form'],en) for p in cur['P'] for en in p['entries'] if set(en.get('s',[]))&{'Resurrection Machine','End Podium'}]
KINV={v:k for k,v in cur['K'].items()}
EN={}
for p in cur['P']:
    EN.setdefault(p['d'],p['en'])
for f in glob.glob('species/1.7.3/*.json'):
    d=json.load(open(f)); EN.setdefault(d['nationalPokedexNumber'],d['name'])
SNAKE={'classic':'클래식 무늬','legacy':'레거시 무늬','attack':'어택 무늬','speed':'스피드 무늬','elusive':'일루시브 무늬','sound':'사운드 무늬','dark':'어두운 무늬'}
def fixform(c):
    f=c['form']
    if f and f.startswith('@snake_pattern='): return SNAKE[f.split('=')[1]]
    if f and f.startswith('@special_spots='): return '특수 무늬'
    if f and f.startswith('@'): raise SystemExit('form? %r'%f)
    return f
GEN=[(1,151),(152,251),(252,386),(387,493),(494,649),(650,721),(722,809),(810,905),(906,1025)]
def gen_of(d): return next(i+1 for i,(a,b) in enumerate(GEN) if a<=d<=b)
sig=lambda c:json.dumps({k:c.get(k) for k in('r','lv','c','b','s','all','ex')},sort_keys=True,ensure_ascii=False)
# 묶기: (dex, form) 순서 유지
groups=collections.OrderedDict()
unown=collections.OrderedDict()
for c in cards:
    if c['unown']:
        unown.setdefault(sig(c),[]).append(c); continue
    f=fixform(c)
    if not any(k in c for k in('b','s','all')):
        if c['dex'] in WIKI_S: c['s']=WIKI_S[c['dex']]
        else: c['c']=['breed']+c['c']
        FALLBACK.append((c['dex'],c.get('s','breed')))
    lst=groups.setdefault((c['dex'],f),[])
    if any(sig(x)==sig(c) for x in lst): continue  # 화면에 똑같이 보이는 항목(얼루기 무늬 1~4, 바닐라·추가 모드 마을 등)은 한 줄
    lst.append(c)
for d,f,en in WIKI_EXTRA:
    groups.setdefault((d,f),[]).append({'r':en['r'],'lv':en['lv'],'c':[KINV[x] for x in en['c']],'s':en['s']})
# 안농: 같은 조건의 글자들을 한 줄로
ALPHA='abcdefghijklmnopqrstuvwxyz'
bylab=collections.OrderedDict()
for sg,lst in unown.items():
    ls=[x['unown'] for x in lst]
    parts=[]
    if all(a in ls for a in ALPHA): parts.append('A~Z'); ls=[x for x in ls if x not in ALPHA]
    parts+= [x.upper() for x in ls]
    bylab.setdefault(', '.join(parts),[]).append(lst[0])
for lab,lst in bylab.items(): groups[(201,lab)]=lst
keys=sorted(groups,key=lambda k:(k[0],list(groups).index(k)))
exist={}
for n,v in core.items():
    if len(set(v))==len(v): exist.setdefault(frozenset(v),n)
RES=set(core)|{'P','K','B','S','OW','NETH','END','e','add','UNLOCK','U_','CATS','STRUCT_KO','STAT_RAW','BASE','FORM_STATS','MEGA','sv','OM','ITEMS','ABIL','PEX','PEX_FORM','SPECIES'}
used_names=set()
J=lambda x:json.dumps(x,ensure_ascii=False,separators=(",",":"))
def write(g):
    ks=[k for k in keys if gen_of(k[0])==g]
    use=collections.Counter(); first={}
    for k in ks:
        for c in groups[k]:
            for f in ('b','s'):
                if f in c:
                    fs=frozenset(c[f])
                    if fs in exist: continue
                    use[fs]+=1; first.setdefault(fs,(EN[k[0]],c[f]))
    newc={};order=[]
    for fs,n in use.items():
        if n<2 or len(fs)<3: continue
        base=re.sub(r'[^A-Z0-9]','',first[fs][0].upper()) or 'L'
        if base[0].isdigit(): base='P'+base
        name=base;i=2
        while name in RES or name in used_names: name=f'{base}{i}';i+=1
        used_names.add(name); newc[fs]=name; order.append(fs)
    def rl(lst):
        fs=frozenset(lst)
        if fs in exist and len(lst)==len(fs): return exist[fs]
        if fs in newc: return newc[fs]
        return J(lst)
    def loc(c):
        if 'all' in c:
            ex=c.get('ex',[])
            if 's' in c: return '{all:"%s",ex:%s,s:%s}'%(c['all'],J(ex),rl(c['s']))
            if c['all']=='ow': return 'OW(%s)'%(J(ex) if ex else '')
            if not ex: return {'nether':'NETH','end':'END'}[c['all']]
            return '{all:"%s",ex:%s}'%(c['all'],J(ex))
        if 'b' in c and 's' in c: return '{b:%s,s:%s}'%(rl(c['b']),rl(c['s']))
        if 'b' in c: return 'B(%s)'%rl(c['b'])
        if 's' in c: return 'S(%s)'%rl(c['s'])
        if 'breed' in c['c']: return '{}'
        raise SystemExit('no loc %r'%c)
    out=[f'// ---- {g}세대 (COBBLEVERSE 모드팩 1.7.42 데이터팩 COBBLEVERSE-DP-v31 기준) ----']
    for fs in order: out.append(f'const {newc[fs]}={J(first[fs][1])};')
    out.append('')
    for k in ks:
        d,f=k
        ents=','.join('e("%s","%s",%s,%s)'%(c['r'],c['lv'],J(c['c']),loc(c)) for c in groups[k])
        out.append('add(%d,%s,%s,%s,[%s]);'%(d,J(ref['ko'][str(d)]),J(EN[d]),J(f) if f else 'null',ents))
    old=open(f'{SRC}/data_gen{g}.js',encoding='utf-8').read()
    keep=[l for l in old.split('\n') if 'UNLOCK' in l or l.startswith('// 출현 시점')]
    if keep: out+=['',*keep]
    open(f'{SRC}/data_gen{g}.js','w',encoding='utf-8').write('\n'.join(out)+'\n')
    return len({k[0] for k in ks}),len(ks),sum(len(groups[k]) for k in ks)
for g in range(1,10): print(g,write(g))
print('fallback',FALLBACK)
