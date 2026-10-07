import json,re,collections,copy
D=json.load(open('dpwork/spawns.json')); TG=json.load(open('dpwork/tags.json'))
NOT_INSTALLED=('aether:','the_bumblezone:','biomesoplenty:','wythers:','blooming_biosphere:','clifftree:','byg:','regions_unexplored:','nullscape:','incendium:','promenade:','natures_spirit:','terrestria:','cinderscapes:','traverse:')
def live(ref): return not any(ref.lstrip('#').startswith(x) for x in NOT_INSTALLED)
FISH_ONLY={'feebas','milotic'}
LISTF=('biomes','structures','neededNearbyBlocks','neededBaseBlocks','dimensions')
def merge(a,b):
    out=dict(a or {})
    for k,v in (b or {}).items():
        if k not in out: out[k]=v
        elif k in LISTF: out[k]=list(dict.fromkeys(list(out[k])+list(v)))
    return out
def entries():
    for path,f in sorted(D['files'].items()):
        for s in f.get('spawns',[]):
            # 낚시는 빼되, 낚시로만 나오는 종(빈티나·밀로틱)은 넣는다
            if s.get('type')!='pokemon' or (s.get('spawnablePositionType')=='fishing' and s['pokemon'].split(' ')[0] not in FISH_ONLY): continue
            c=copy.deepcopy(s.get('condition') or {}); a=copy.deepcopy(s.get('anticondition') or {})
            for p in s.get('presets',[]) or []:
                pr=D['presets'].get(p.lower(),{})
                c=merge(c,pr.get('condition')); a=merge(a,pr.get('anticondition'))
            for k in ('canSeeSky','timeRange'):
                if k in s and k not in c: c[k]=s[k]
            refs=c.get('biomes',[])+c.get('structures',[])
            if refs and not [r for r in refs if live(r)]: continue
            c['biomes']=[b for b in c.get('biomes',[]) if live(b)]
            c['structures']=[b for b in c.get('structures',[]) if live(b)]
            if not c['biomes']: c.pop('biomes')
            if not c['structures']: c.pop('structures')
            if 'biomes' in a: a['biomes']=[b for b in a['biomes'] if live(b)]
            yield path,s,c,a
