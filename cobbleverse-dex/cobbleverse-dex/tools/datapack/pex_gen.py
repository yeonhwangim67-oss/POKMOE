# 특성·드롭 데이터: 코블몬 1.7.3 종족 데이터 + Mega Showdown 1.8.4 덮어쓰기 -> src/poke_extra.js
import json,glob,zipfile,re,sys,collections
dex={}
for f in glob.glob('species/1.7.3/*.json'):
    d=json.load(open(f)); dex[d['nationalPokedexNumber']]=d
z=zipfile.ZipFile('mrpack/jars/mega_showdown-fabric-1.8.4+1.7.3+1.21.1.jar')
over=[]
for x in z.namelist():
    if x.startswith('data/cobblemon/species/') and x.endswith('.json'):
        d=json.loads(z.read(x)); dex[d['nationalPokedexNumber']]=d; over.append(d['nationalPokedexNumber'])
addn=[]
for x in z.namelist():
    if x.startswith('data/cobblemon/species_additions/') and x.endswith('.json'):
        a=json.loads(z.read(x))
        if 'drops' in a:
            tgt=a['target'].split(':')[-1]
            for d in dex.values():
                if d['name'].lower().replace(' ','')==tgt.replace('_','') or re.sub(r'[^a-z]','',d['name'].lower())==re.sub(r'[^a-z]','',tgt):
                    d['drops']=a['drops'];addn.append(d['nationalPokedexNumber'])
# COBBLEVERSE 데이터팩(COBBLEVERSE-DP-v31)이 덮어쓴 종족·드롭 (Mega Showdown보다 우선)
dpz=zipfile.ZipFile('mrpack/x/overrides/datapacks/COBBLEVERSE-DP-v31.zip')
dpover=[];dpadd=[]
for x in dpz.namelist():
    if x.startswith('data/cobblemon/species/') and x.endswith('.json'):
        d=json.loads(dpz.read(x)); dex[d['nationalPokedexNumber']]=d; dpover.append(d['nationalPokedexNumber'])
for x in dpz.namelist():
    if x.startswith('data/cobblemon/species_additions/') and x.endswith('.json'):
        a=json.loads(dpz.read(x))
        if 'drops' not in a and 'abilities' not in a: continue
        tgt=a['target'].split(':')[-1]
        for d in dex.values():
            if re.sub(r'[^a-z]','',d['name'].lower())==re.sub(r'[^a-z]','',tgt):
                for k in ('drops','abilities'):
                    if k in a: d[k]=a[k]
                dpadd.append(d['nationalPokedexNumber'])
LANG={}
for p in ['cw/mc_ko.json','cw/ko_kr.json','msd/ko.json']: LANG.update(json.load(open(p)))
miss=collections.Counter()
def item_ko(i):
    ns,iid=i.split(':')
    for k in (f'item.{ns}.{iid}',f'block.{ns}.{iid}'):
        if k in LANG: return LANG[k]
    BADID={'cobblemon:sacred_ash':'성스러운분말 (게임에 없는 아이템 ID)','minecraft:eye_of_ender':'엔더의 눈 (잘못된 아이템 ID)','minecraft:raw_cod':'생대구 (게임에 없는 아이템 ID)'}
    if i in BADID: return BADID[i]
    for ns2 in ('cobblemon','minecraft'):
        for k in (f'item.{ns2}.{iid}',f'block.{ns2}.{iid}'):
            if k in LANG: return LANG[k]+' (게임에 없는 아이템 ID)'
    miss[i]+=1; return '?'+i
abil=set()
def pack(d):
    a=[x for x in d.get('abilities',[]) if not x.startswith('h:')]
    h=[x[2:] for x in d.get('abilities',[]) if x.startswith('h:')]
    for x in a+h: abil.add(x)
    o={'a':list(dict.fromkeys(a))}
    if h: o['h']=h[0]
    dr=d.get('drops')
    if dr and dr.get('entries'):
        o['d']=[[item_ko(e['item']),e.get('percentage',100),e.get('quantityRange','')] for e in dr['entries']]
        if dr.get('amount'): o['n']=int(dr['amount'])
    return o
FORMS={'알로라':'Alola','가라르':'Galar','히스이':'Hisui','팔데아':'Paldea','알로라 계열':'Alola-Bias','가라르 계열':'Galar-Bias','히스이 계열':'Hisui-Bias','팔데아 컴뱃종':'Paldea-Combat','팔데아 블레이즈종':'Paldea-Blaze','팔데아 워터종':'Paldea-Aqua',
'붉은달':'Bloodmoon','메가':'Mega','진작폼':'Antique','위작폼':'Phony','한밤중의 모습':'Midnight','황혼의 모습':'Dusk','한낮의 모습':'Midday','도보폼':'Roaming','상자폼':'Chest','영원의 꽃':'Eternal','하양줄무늬의 모습':'White-Striped','파랑줄무늬의 모습':'Blue-Striped','빨강줄무늬의 모습':'Red-Striped'}
P=json.load(open('new.json'))['P']
PEX={};PF={}
for n,d in sorted(dex.items()):
    if n>1025: continue
    PEX[n]=pack(d)
for p in P:
    if not p['form']: continue
    fn=FORMS.get(p['form']); d=dex.get(p['d'])
    if not fn or not d: continue
    fm=next((f for f in d.get('forms',[]) if f.get('name','').lower()==fn.lower()),None)
    if not fm: continue
    o=pack({**{'abilities':d.get('abilities',[]),'drops':d.get('drops')},**{k:v for k,v in fm.items() if k in('abilities','drops')}})
    if o!=PEX[p['d']]: PF[f"{p['d']}|{p['form']}"]=o
# 출현 위치별 드롭: 데이터팩 출현 항목에 drops가 있으면 그 위치에서 나온 개체는 종족 드롭 대신 이 드롭을 쓴다
sys.path.insert(0,'tools')
from dp_common import entries
SPN={re.sub(r'[^a-z]','',d['name'].lower()):n for n,d in dex.items()}
mc_ko=json.load(open('cw/mc_ko.json'))
def where(c):
    b=c.get('biomes',[])
    if any('nether' in x for x in b): return '네더'
    if any(x.endswith('is_end') for x in b): return '엔드'
    if len(b)==1 and b[0].startswith('minecraft:'): return mc_ko.get('biome.minecraft.'+b[0].split(':')[1],b[0])
    return '특정 장소'
SD=collections.defaultdict(list)
for path,sp,c,a in entries():
    if not sp.get('drops'): continue
    n=SPN[re.sub(r'[^a-z]','',sp['pokemon'].split(' ')[0])]
    o=pack({'drops':sp['drops']})
    SD[n].append([where(c)+'에서 나온 개체',o['d'],o.get('n')])
for n,l in SD.items(): PEX[n]['sd']=l
ABIL={a:[LANG.get(f'cobblemon.ability.{a}','?'+a),LANG.get(f'cobblemon.ability.{a}.desc','')] for a in sorted(abil)}
if miss: print('MISSING ITEMS',miss); 
js='// 특성·드롭 아이템 (출처: 코블몬 1.7.3 종족 데이터, 코블버스에 들어 있는 Mega Showdown 1.8.4와 COBBLEVERSE-DP-v31 데이터팩이 덮어쓴 종족·출현별 드롭 포함 / 이름·설명: 코블몬·마인크래프트·Mega Showdown 게임 한국어 번역)\n'
js+='// PEX[도감번호]={a:[특성], h:숨겨진 특성, d:[[아이템, 확률%, 개수범위]], n:한 번에 떨어지는 최대 종류 수, sd:[[위치, 드롭, n]] 그 위치에서 나온 개체만의 드롭}, PEX_FORM["도감번호|폼"]: 폼이 다를 때\n'
js+='const ABIL='+json.dumps(ABIL,ensure_ascii=False,separators=(',',':'))+';\n'
js+='const PEX='+json.dumps(PEX,ensure_ascii=False,separators=(',',':'))+';\n'
js+='const PEX_FORM='+json.dumps(PF,ensure_ascii=False,separators=(',',':'))+';\n'
open(sys.argv[1],'w',encoding='utf-8').write(js)
print('DP overrides',dpover,'DP additions',dpadd,'spawn drops',dict((k,[x[0] for x in v]) for k,v in SD.items()))
print('species',len(PEX),'forms',len(PF),'abilities',len(ABIL),'MSD overrides',len(over),'additions',addn,'size',len(js))
