# 바이옴·구조물 태그 수집과 바이옴 목록
import zipfile,json,glob,re,collections,os
M='mrpack/'
SRC=[M+'jars/mc-client-1.21.1.jar',M+'jars/fabric-convention-tags-v1-0.116.14.jar',M+'jars/fabric-convention-tags-v2-0.116.14.jar',M+'jars/Cobblemon-fabric-1.7.3+1.21.1.jar']
SRC+=[j for j in glob.glob(M+'jars/*.jar') if j not in SRC]
SRC+=[M+'x/overrides/datapacks/extra/Terralith-DP.zip',M+'x/overrides/datapacks/COBBLEVERSE-DP-v31.zip']+glob.glob(M+'x/overrides/datapacks/extra/COBBLEVERSE-*.zip')
tags={'worldgen/biome':collections.defaultdict(list),'worldgen/structure':collections.defaultdict(list)}
biomes=set();structures=set()
for j in SRC:
    z=zipfile.ZipFile(j)
    for n in z.namelist():
        m=re.match(r'data/([^/]+)/tags/(worldgen/(?:biome|structure))/(.+)\.json$',n)
        if m:
            d=json.loads(z.read(n)); key=f'{m.group(1)}:{m.group(3)}'
            vals=[v if isinstance(v,str) else (v['id'] if v.get('required',True) or True else None) for v in d.get('values',[])]
            if d.get('replace'): tags[m.group(2)][key]=[]
            tags[m.group(2)][key]+= [v for v in vals if v]
        m=re.match(r'data/([^/]+)/worldgen/biome/(.+)\.json$',n)
        if m: biomes.add(f'{m.group(1)}:{m.group(2)}')
        m=re.match(r'data/([^/]+)/worldgen/structure/(.+)\.json$',n)
        if m: structures.add(f'{m.group(1)}:{m.group(2)}')
def expand(kind,ref,seen=None,univ=None):
    seen=seen or set()
    if ref.startswith('#'):
        k=ref[1:]
        if k in seen: return []
        seen.add(k); out=[]
        for v in tags[kind].get(k,[]): out+=expand(kind,v,seen,univ)
        return out
    return [ref] if (univ is None or ref in univ) else []
if __name__=='__main__':
    print('biomes',len(biomes),'structures',len(structures),'biome tags',len(tags['worldgen/biome']),'structure tags',len(tags['worldgen/structure']))
    for t in ['#cobblemon:is_overworld','#cobblemon:is_jungle','#cobblemon:is_freezing','#minecraft:is_nether','#cobblemon:is_end','#cobblemon:is_sky']:
        e=list(dict.fromkeys(expand('worldgen/biome',t,univ=biomes))); print(t,len(e),e[:8])
    for t in ['#cobblemon:ruin','#minecraft:village','#minecraft:ruined_portal']:
        print(t,list(dict.fromkeys(expand('worldgen/structure',t,univ=structures)))[:12])
    json.dump({'biomes':sorted(biomes),'structures':sorted(structures),'tags':tags},open('dpwork/tags.json','w'))
