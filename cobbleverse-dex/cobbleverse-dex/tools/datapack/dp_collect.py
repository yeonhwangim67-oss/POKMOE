import zipfile,json,collections,os
M='mrpack/'
dz=zipfile.ZipFile(M+'x/overrides/datapacks/COBBLEVERSE-DP-v31.zip')
cz=zipfile.ZipFile(M+'jars/Cobblemon-fabric-1.7.3+1.21.1.jar')
az=zipfile.ZipFile(M+'jars/cobblemon-additions-4.1.6.jar')
files={}
for z in (cz,az,dz):  # 뒤에 오는 것이 덮어씀
    for x in z.namelist():
        if 'spawn_pool_world' in x and x.endswith('.json'): files[x]=json.loads(z.read(x))
presets={}
for z in (cz,dz):
    for x in z.namelist():
        if 'spawn_detail_presets' in x and x.endswith('.json'): presets[os.path.basename(x)[:-5]]=json.loads(z.read(x))
json.dump({'files':files,'presets':presets},open('dpwork/spawns.json','w'))
C=collections.Counter
ck=C();ak=C();ctx=C();pre=C();tr=C();wm=C();aspect=C();btag=C();stag=C();keys=C()
for f,d in files.items():
    for s in d.get('spawns',[]):
        keys.update(s.keys())
        ck.update((s.get('condition') or {}).keys()); ak.update((s.get('anticondition') or {}).keys())
        ctx[s.get('context')]+=1; pre.update(s.get('presets',[]))
        tr[(s.get('condition') or {}).get('timeRange')]+=1
        for w in s.get('weightMultipliers',[]) or ([s['weightMultiplier']] if 'weightMultiplier' in s else []): wm[json.dumps(w.get('condition',{}),sort_keys=True)[:90]]+=1
        parts=s.get('pokemon','<'+str(s.get('type'))+'>').split()[1:]; aspect.update(parts)
        if 'pokemon' not in s: print('NOPOKEMON',f,json.dumps(s)[:200])
        for c in (s.get('condition') or {},s.get('anticondition') or {}):
            btag.update(c.get('biomes',[])); stag.update(c.get('structures',[]))
print('files',len(files),'entries',sum(len(d.get('spawns',[])) for d in files.values()))
print('KEYS',keys);print('COND',ck);print('ANTI',ak);print('CTX',ctx);print('PRESETS',pre);print('TIME',tr)
print('WM',wm.most_common(40));print('ASPECT',aspect.most_common(80));print('BIOMES',len(btag),btag.most_common(60));print('STRUCT',len(stag),stag.most_common(80))
print('preset names',list(presets))
