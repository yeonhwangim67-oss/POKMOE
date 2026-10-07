# COBBLEVERSE 데이터팩 출현 -> 카드(정규화) 목록
import json,re,glob,collections,sys
sys.path.insert(0,'tools')
from dp_common import entries,TG,live
TAGS=TG['tags']
mc_en=json.load(open('cw/mc_en.json'))
SPID={}
for f in glob.glob('species/1.7.3/*.json'):
    d=json.load(open(f)); SPID[f.split('/')[-1][:-5]]=d['nationalPokedexNumber']
NS_OK=('minecraft:','terralith:','cobblemon:','cobbleverse:')
def btag(ref,seen=None):
    seen=seen if seen is not None else set()
    if ref.startswith('#'):
        k=ref[1:]
        if k in seen: return []
        seen.add(k);out=[]
        for v in TAGS['worldgen/biome'].get(k,[]): out+=btag(v,seen)
        return out
    return [ref] if ref.startswith(NS_OK) else []
# Terralith 데이터팩이 더한 태그 값은 쓰지 않는다(기존 위키와 같은 방식)
def load_tags_without_terralith():
    import zipfile
    M='mrpack/';tg=collections.defaultdict(list)
    srcs=[M+'jars/mc-client-1.21.1.jar',M+'jars/fabric-convention-tags-v1-0.116.14.jar',M+'jars/fabric-convention-tags-v2-0.116.14.jar',M+'jars/Cobblemon-fabric-1.7.3+1.21.1.jar']+[j for j in glob.glob(M+'jars/*.jar') if 'mc-client' not in j and 'convention' not in j and 'Cobblemon-fabric' not in j]+[M+'x/overrides/datapacks/COBBLEVERSE-DP-v31.zip']+glob.glob(M+'x/overrides/datapacks/extra/COBBLEVERSE-*.zip')
    for j in srcs:
        z=zipfile.ZipFile(j)
        for n in z.namelist():
            m=re.match(r'data/([^/]+)/tags/worldgen/biome/(.+)\.json$',n)
            if m:
                d=json.loads(z.read(n));key=f'{m.group(1)}:{m.group(2)}'
                if d.get('replace'): tg[key]=[]
                tg[key]+=[v if isinstance(v,str) else v['id'] for v in d.get('values',[])]
    return tg
TAGS['worldgen/biome']=load_tags_without_terralith()
def bname(b):
    ns,p=b.split(':',1)
    if ns=='minecraft' and f'biome.minecraft.{p}' in mc_en: return mc_en[f'biome.minecraft.{p}']
    return ' '.join(w.capitalize() for w in p.split('/')[-1].split('_'))
STRUCT={'#minecraft:village':['Village (All Types)'],'minecraft:mansion':['Woodland Mansion'],'minecraft:woodland_mansion':['Woodland Mansion'],
'cobblemon:shipwreck_coves/lush_shipwreck_cove':['Lush Shipwreck Cove'],'cobblemon:shipwreck_coves/submerged_shipwreck_cove':['Submerged Shipwreck Cove'],'#cobblemon:shipwreck_cove':['Shipwreck Cove (All Types)'],
'minecraft:trail_ruins':['Trail Ruins'],'#cobblemon:ruin':['Cobblemon Ruins (All Types)'],'#cobblemon:ruins/arch':['Crumbling Arch Ruins','Rooted Arch Ruins'],'minecraft:jungle_pyramid':['Jungle Pyramid'],
'minecraft:desert_pyramid':['Desert Pyramid'],'minecraft:swamp_hut':['Swamp Hut'],'bca:village/witch_hut':['Swamp Hut'],'minecraft:pillager_outpost':['Pillager Outpost'],'#minecraft:ocean_ruin':['Cold Ocean Ruins','Warm Ocean Ruins'],
'minecraft:monument':['Ocean Monument'],'minecraft:ocean_monument':['Ocean Monument'],'#minecraft:ruined_portal':['Ruined Portal'],'minecraft:ancient_city':['Ancient City'],'minecraft:end_city':['End City'],
'cobbleverse:dyna_tree':['Dyna Tree (Hoenn)'],'cobbleverse:burned_tower':['Burned Tower (Johto)'],'minecraft:stronghold':['Stronghold'],'minecraft:igloo':['Igloo'],'minecraft:nether_fossil':['Nether Fossil'],
'minecraft:bastion_remnant':['Bastion Remnant'],'minecraft:fortress':['Nether Fortress'],'#minecraft:shipwreck':['Shipwreck'],'cobbleverse:crown_cemetery':['Crown Cemetery'],'cobbleverse:crown_spire':['Crown Spire'],
'cobblemon:ruins/luna_henge_ruins':['Luna Henge Ruins'],'cobblemon:ruins/sol_henge_ruins':['Sol Henge Ruins'],'cobblemon:ruins/stonjourner_henge_ruins':['Stonjourner Henge Ruins'],'minecraft:desert_well':['Desert Well'],
'cobbleverse:dawn_tower':['Dawn Tower (End)'],'cobbleverse:dusk_tower':['Dusk Tower (End)']}
for t in ['fighting','dark','default']:
    for sz in ['small','mid','large']: STRUCT[f'bca:village/{t}_{sz}']=['Village (All Types)']
CUSTOM={'secret_garden':'Secret Garden (Hoenn)','split_decision_temple':'Split Decision Temple (Sinnoh)','articuno_tower':'Articuno Tower (Kanto)','zapdos_tower':'Zapdos Tower (Kanto)','moltres_tower':'Moltres Tower (Nether)',
'team_rocket_radio':'Team Rocket Radio Tower (Johto)','origin_temple':'Origin Temple (Kanto)','whirl_island':'Whirl Island (Johto)','bell_tower':'Bell Tower (Johto)','ilex_shrine':'Ilex Shrine (Johto)',
'regirock_temple':'Regirock Temple (Hoenn)','regice_temple':'Regice Temple (Hoenn)','registeel_temple':'Registeel Temple (Hoenn)','kyogre_temple':'Kyogre Dome (Hoenn)','groudon_vulcano':'Groudon Volcano (Hoenn)',
'sky_pillar':'Sky Pillar (Hoenn)','jirachi_structure':'Wish Cave (Hoenn)','deoxys_meteorite':'Deoxys Meteorite (Hoenn)','newmoon_island':'Newmoon Island','flower_paradise':'Flower Paradise (Sinnoh)',
'sinnoh_temple':'Temple of Sinnoh','eternatus_cocoon':'Eternatus Cocoon (End)','crown_spire':'Crown Spire','crown_cemetery':'Crown Cemetery','grasswither_shrine':'Grasswither Shrine','icerend_shrine':'Icerend Shrine',
'groundblight_shrine':'Groundblight Shrine','firescoruge_shrine':'Firescourge Shrine'}
GROUP={'is_freezing':'얼음 계열','is_spooky':'으스스한 계열','is_arid':'건조 계열','is_lush':'무성한 계열','is_swamp':'늪 계열','is_volcanic':'화산 계열','is_sandy':'모래 계열','is_magical':'마법 계열','is_tundra':'툰드라 계열',
'is_thermal':'온열 계열','is_desert':'사막 계열','is_ocean':'바다 계열','is_badlands':'악지 계열','is_cherry_blossom':'벚꽃 계열','is_jungle':'정글 계열','is_bamboo':'대나무 계열','is_island':'섬 계열','has_block/mud':'진흙 계열',
'is_taiga':'타이가 계열','is_mountain':'산 계열','is_floral':'꽃 계열','is_frozen_ocean':'얼어붙은 바다 계열','is_beach':'해변 계열','is_hills':'언덕 계열','is_forest':'숲 계열','is_dripstone':'점적석 계열','is_cold_ocean':'차가운 바다 계열',
'is_plains':'평원 계열','is_cold':'추운 계열','is_warm_ocean':'따뜻한 바다 계열','is_savanna':'사바나 계열','is_mushroom':'버섯 계열','is_peak':'봉우리 계열','is_sky':'하늘 계열','is_temperate':'온대 계열','is_deep_ocean':'깊은 바다 계열',
'is_lukewarm_ocean':'미지근한 바다 계열','is_temperate_ocean':'온대 바다 계열','is_tropical_island':'열대 섬 계열','nether/is_warped':'네더 뒤틀린 계열','nether/is_frozen':'네더 얼음 계열','nether/is_desert':'네더 사막 계열',
'nether/is_quartz':'네더 석영 계열','nether/is_toxic':'네더 독 계열','is_snowy':'눈 계열','is_grassland':'초원 계열','is_coast':'해안 계열','is_river':'강 계열','is_freshwater':'민물 계열','is_glacial':'빙하 계열'}
def exname(ref):
    if ref.startswith('#'):
        ex=list(dict.fromkeys(btag(ref)))
        if len(ex)==1: return bname(ex[0])
        k=ref.split(':',1)[1]
        return GROUP.get(k,'?'+ref)
    return bname(ref)
NEAR={('minecraft:water',):['water'],('#minecraft:water',):['water'],('minecraft:water','minecraft:flowing_water'):['water','flow'],('minecraft:lily_pad',):['lily'],('#minecraft:iron_ores',):['iron'],
('#minecraft:redstone_ores','#cobblemon:redstone_blocks','#c:redstone_ores'):['redstone'],('minecraft:lightning_rod',):['rod'],('cobblemon:medicinal_leek',):['leek'],('#cobblemon:apricorns',):['apri'],
('minecraft:lava','minecraft:magma_block'):['lava'],('#cobblemon:saccharine_trees',):['sacch'],('minecraft:sunflower',):['sunflower'],('minecraft:lava',):['lavab'],('#minecraft:corals','#minecraft:coral_blocks'):['coral'],
('#cobblemon:dead_coral',):['deadcoral'],('#minecraft:coal_ores',):['coal'],('minecraft:coal_ore',):['coal'],('minecraft:bell',):['bell'],('#cobblemon:flowers','#cobblemon:saccharine_trees'):['flowersacch'],
('minecraft:magma_block',):['magma'],('#cobblemon:flowers',):['flowers'],('#cobblemon:red_flowers',):['redfl'],('#cobblemon:yellow_flowers',):['yellowfl'],('#cobblemon:orange_flowers',):['orangefl'],
('#cobblemon:blue_flowers',):['bluefl'],('#cobblemon:white_flowers',):['whitefl'],('#cobblemon:pink_flowers',):['pinkfl'],('minecraft:kelp_plant',):['kelp'],('#minecraft:diamond_ores',):['diamond'],
('minecraft:pumpkin','minecraft:carved_pumpkin'):['pumpkin'],('minecraft:iron_block',):['ironblock'],('minecraft:cake',):['cake'],('minecraft:sugar_cane',):['sugarcane'],('minecraft:kelp_plant','minecraft:seagrass'):['kelpsea'],
('#cobblemon:berries',):['berries'],('minecraft:amethyst_block','minecraft:budding_amethyst'):['amethyst'],('#minecraft:leaves','#c:leaves'):['leaves'],('#cobblemon:concrete_blocks',):['concrete'],
('#cobblemon:gemstones',):['gems'],('#cobblemon:red_flowers','#cobblemon:blue_flowers'):['redbluefl'],('minecraft:white_bed',):['whitebed'],
('minecraft:light_blue_wool','minecraft:blue_wool','minecraft:cyan_wool','minecraft:light_gray_wool','minecraft:gray_wool','minecraft:green_wool','minecraft:black_wool','minecraft:lime_wool','minecraft:orange_wool','minecraft:yellow_wool','minecraft:brown_wool','minecraft:yellow_carpet','minecraft:lime_carpet'):['wool'],
('minecraft:light_grey_carpet','minecraft:magenta_carpet','minecraft:white_carpet'):['carpet'],('minecraft:cobweb',):['cobweb'],
('minecraft:redstone_block','minecraft:repeater','minecraft:redstone_torch','minecraft:daylight_detector','minecraft:comparator','minecraft:redstone_ore','minecraft:redstone_lamp','minecraft:lightning_rod','cobblemon:pc','cobblemon:monitor','cobblemon:healing_machine','cobblemon:restoration_tank','cobblemon:fossil_analyzer'):['machine']}
HIDE_NEAR={'#cobblemon:mansion_blocks','#cobblemon:ocean_ruin_blocks','#cobblemon:trail_ruins_blocks','#cobblemon:ruined_portal_blocks','#cobblemon:pillager_outpost_blocks','#cobblemon:jungle_pyramid_blocks','#cobblemon:ancient_city_blocks',
'#cobblemon:desert_pyramid_blocks','#cobblemon:end_city_blocks','minecraft:bone_block','minecraft:cracked_stone_bricks','minecraft:mossy_stone_bricks','#cobblemon:nether_structure_blocks'}
WM={('night',0.25):'n025',('night',1.5):'n15',('thunder',5.0):'t5',('day',0.25):'d025',('night',5.0):'n5',('rain',1.5):'rain15',('rain',5.0):'rain5',('day',1.5):'d15',('twilight',2.5):'twi',
('bee',5.0):'bee5',('moon4',5.0):'newmoon5',('ship',10.0):'ship10',('dusk',5.0):'dusk5',('twilight',5.0):'twi5',('thunder',3.0):'t3',('dawn',5.0):'dawn5',('rain',3.0):'rain3',('moon0',5.0):'fullmoon5',
('night',1.8):'n18',('night',2.5):'n25',('thunder',2.0):'t2',('lava',5.0):'lava5',('water',5.0):'water5',('day',3.0):'d3',('day',5.0):'d5',('thunder',4.0):'t4',('thunder',2.5):'t25',('thunder',3.3):'storm33',('day',3.3):'day33',('rain',3.3):'rain33',('rain',2.0):'rain2'}
YK={(62,None):['minY62'],(48,None):['minY48'],(0,None):['minY0'],(-41,9):['shipY'],(-60,13):['subY'],(None,62):['maxY62'],(None,48):['maxY48'],(None,0):['maxY0'],(32,None):['minY32'],(None,32):['maxY32'],
(-37,10):['minYm37','maxY10'],(190,None):['minY190'],(32,62):['minY32','maxY62'],(None,60):['maxY60'],(-37,40):['minYm37','maxY40'],(-37,30):['minYm37','maxY30'],(None,75):['maxY75'],(None,40):['maxY40'],(None,30):['maxY30'],(None,10):['maxY10']}
RAR={'common':'C','uncommon':'U','rare':'R','ultra-rare':'X'}
ASP={'alolan':'알로라','galarian':'가라르','hisuian':'히스이','paldean':'팔데아','valencian':'발렌시아','region_bias=hisui':'히스이 계열','region_bias=alola':'알로라 계열','region_bias=galar':'가라르 계열',
'tea_authenticity=phony':'위작폼','tea_authenticity=antique':'진작폼','matcha_authenticity=counterfeit':'짝퉁폼','matcha_authenticity=artisan':'진품폼','matcha_authenticity=unremarkable':'범작폼','matcha_authenticity=masterpiece':'걸작폼',
'striped=blue':'파랑줄무늬의 모습','striped=red':'빨강줄무늬의 모습','striped=white':'하양줄무늬의 모습','maushold_family=four':'네 식구','maushold_family=three':'세 식구','bagworm_cloak=plant':'초목도롱','bagworm_cloak=sandy':'모래땅도롱','bagworm_cloak=trash':'슈레도롱',
'sea=east':'동쪽바다의 모습','sea=west':'서쪽바다의 모습','flower=red':'빨간꽃','flower=yellow':'노란꽃','flower=orange':'오렌지색꽃','flower=blue':'파란꽃','flower=white':'하얀꽃','flower=pink':'분홍꽃','flower=eternal':'영원의 꽃',
'roaming':'도보폼','chest':'상자폼','cosplay=belle':'옷갈아입기 마담','cosplay=libre':'옷갈아입기 마스크드','cosplay=phd':'옷갈아입기 닥터','cosplay=pop_star':'옷갈아입기 아이돌','cosplay=rock_star':'옷갈아입기 하드록','cosplay=cosplay':'옷갈아입기',
'bull_breed=combat':'팔데아 컴뱃종','bull_breed=blaze':'팔데아 블레이즈종','bull_breed=aqua':'팔데아 워터종','mooshtank=red':'빨간 무시탱크','mooshtank=brown':'갈색 무시탱크','forecast=rainy':'빗방울의 모습','forecast=snowy':'설운의 모습','forecast=sunny':'태양의 모습',
'blossom_form=overcast':'네거티브폼','blossom_form=sunshine':'포지티브폼','dance_style=baile':'이글이글스타일','dance_style=pom-pom':'파칙파칙스타일','dance_style=pau':'훌라훌라스타일','dance_style=sensu':'하늘하늘스타일',
'wolf_form=dusk':'황혼의 모습','wolf_form=midday':'한낮의 모습','wolf_form=midnight':'한밤중의 모습','core_color=red':'빨간색 코어','core_color=orange':'주황색 코어','core_color=yellow':'노란색 코어','core_color=green':'초록색 코어',
'core_color=blue':'파란색 코어','core_color=indigo':'남색 코어','core_color=violet':'보라색 코어','meteor_shield=meteor':'유성의 모습','paint_color=original':'500년 전의 색','bloodmoon':'붉은달','landsnake_form=two-segment':'두 마디폼','landsnake_form=three-segment':'세 마디폼',
'vivillon_wings=modern':'모던한 모양','vivillon_wings=high-plains':'황야의 모양','vivillon_wings=fancy':'팬시한 모양','vivillon_wings=ocean':'오션의 모양','vivillon_wings=sandstorm':'사진의 모양','vivillon_wings=meadow':'화원의 모양',
'vivillon_wings=garden':'정원의 모양','vivillon_wings=river':'대하의 모양','vivillon_wings=polar':'설국의 모양','vivillon_wings=tundra':'설원의 모양','vivillon_wings=jungle':'정글의 모양','vivillon_wings=monsoon':'스콜의 모양',
'vivillon_wings=archipelago':'군도의 모양','vivillon_wings=marine':'마린의 모양','vivillon_wings=continental':'대륙의 모양','vivillon_wings=savanna':'사바나의 모양','vivillon_wings=sun':'태양의 모양','vivillon_wings=elegant':'고아한 모양','vivillon_wings=icy-snow':'빙설의 모양',
'gender=female':'암컷','gender=male':'수컷','sword_form=ordinary':'평상시 모습','sword_form=resolute':'각오의 모습'}
IGN_ASP={'meteor_shield=core','percent_cells=core'}
miss=collections.Counter(); dead=[]
def conv_entry(path,s,c,a):
    keys=[]
    pt=s.get('spawnablePositionType')
    if pt=='fishing': keys.append('fish')
    if c.get('minLureLevel')==1: keys.append('lure1')
    if pt in ('submerged','surface','seafloor'): keys.append({'submerged':'sub','surface':'surf','seafloor':'floor'}[pt])
    if c.get('fluid')=='#minecraft:lava' or c.get('fluid')=='minecraft:lava': keys.append('inlava')
    if 'canSeeSky' in c: keys.append('seeSky' if c['canSeeSky'] else 'indoor')
    sl=(c.get('minSkyLight'),c.get('maxSkyLight'))
    if sl!=(None,None):
        k={(8,15):'sky',(0,7):'dim',(0,0):'sky0',(1,15):'sky115',(1,7):'sky17'}.get(sl)
        if k: keys.append(k)
        else: miss[('skylight',sl)]+=1;keys.append('?sl%s'%(sl,))
    if 'maxLight' in c:
        k={0:'light0',7:'light07'}.get(c['maxLight'])
        if k: keys.append(k)
        else: miss[('light',c['maxLight'])]+=1
    tr=c.get('timeRange')
    if tr:
        if tr in('day','night','dusk','dawn','twilight'): keys.append(tr if tr!='twilight' else 'twilightt')
        else: miss[('time',tr)]+=1
    if c.get('isRaining') is True: keys.append('rain')
    if c.get('isRaining') is False: keys.append('norain')
    if c.get('isThundering') is True: keys.append('storm')
    y=(c.get('minY'),c.get('maxY'))
    if y!=(None,None):
        if y in YK: keys+=YK[y]
        else: miss[('y',y)]+=1
    if 'moonPhase' in c:
        mp=str(c['moonPhase']);k={'0':'moon','0,4':'moon04','1,2,3':'moon13','5,6,7':'moon57','4':'newmoon'}.get(mp)
        if k: keys.append(k)
        else: miss[('moon',mp)]+=1
    if c.get('isSlimeChunk'): keys.append('slime')
    if 'minX' in c: keys.append('xpos')
    if 'maxX' in c: keys.append('xneg')
    nb=[x for x in c.get('neededNearbyBlocks',[]) if x not in HIDE_NEAR]
    if nb:
        k=NEAR.get(tuple(nb))
        if k: keys+=k
        else: miss[('near',tuple(nb))]+=1
    for bb in c.get('neededBaseBlocks',[]):
        if bb=='minecraft:quartz_block': keys.append('quartz')
        if bb=='minecraft:amethyst_block': keys.append('amethystbase')
        if bb=='#cobblemon:trees' and 'treetop' in (s.get('presets') or []): keys.append('treetop')
    anb=a.get('neededNearbyBlocks',[])
    if '#cobblemon:saccharine_trees' in anb: keys.append('nosacch')
    if 'minecraft:water' in anb or '#minecraft:water' in anb: keys.append('nowater')
    if a.get('isSlimeChunk'): keys.append('noslime')
    for w in (s.get('weightMultipliers') or ([s['weightMultiplier']] if s.get('weightMultiplier') else [])):
        cd=w.get('condition',{});m=float(w.get('multiplier'))
        if 'minLureLevel' in cd or 'maxLureLevel' in cd: continue
        kind=None
        if cd.get('timeRange'): kind=cd['timeRange']
        elif cd.get('isThundering'): kind='thunder'
        elif cd.get('isRaining'): kind='rain'
        elif 'moonPhase' in cd: kind='moon%s'%cd['moonPhase']
        elif cd.get('structures')==['#minecraft:shipwreck']: kind='ship'
        elif cd.get('neededNearbyBlocks')==['#minecraft:beehives']: kind='bee'
        elif cd.get('neededNearbyBlocks')==['#minecraft:lava']: kind='lava'
        elif cd.get('neededNearbyBlocks')==['#minecraft:water']: kind='water'
        k=WM.get((kind,m))
        if k: keys.append(k)
        else: miss[('wm',json.dumps(cd,sort_keys=True)[:80],m)]+=1; keys.append('?wm')
    # 장소
    loc={}
    bl=c.get('biomes',[]); special=False
    if 'cobbleverse:not_spawn' in bl: dead.append((path,s['id'],bl)); return None
    custom=[b for b in bl if 'custom_spawn' in b]
    structs=[]
    for b in custom:
        nm=b.split('custom_spawn/')[-1] if '/' in b.split(':')[1] else None
        if nm: 
            if nm in CUSTOM: structs.append(CUSTOM[nm])
            else: miss[('custom',nm)]+=1
        special=True
    bl=[b for b in bl if 'custom_spawn' not in b]
    for st in c.get('structures',[]):
        if st in STRUCT: structs+=STRUCT[st]
        else: miss[('struct',st)]+=1
    structs=list(dict.fromkeys(structs))
    antib=a.get('biomes',[])
    allk=None
    if '#cobblemon:is_overworld' in bl: allk='ow'; bl=[b for b in bl if b!='#cobblemon:is_overworld']
    elif '#minecraft:is_nether' in bl or '#cobblemon:is_nether' in bl: allk='nether'; bl=[b for b in bl if b not in('#minecraft:is_nether','#cobblemon:is_nether')]
    elif '#cobblemon:is_end' in bl or '#minecraft:is_end' in bl: allk='end'; bl=[b for b in bl if b not in('#cobblemon:is_end','#minecraft:is_end')]
    if allk:
        loc['all']=allk; loc['ex']=[exname(x) for x in antib]
        bl=[b for b in bl if not (allk in('ow','nether') and b in('#cobblemon:is_volcanic',))]
        if bl: miss[('mixed_all',tuple(bl))]+=1
        if structs and allk in('ow','nether','end') and not loc['ex']: loc={}
    else:
        ex=set()
        for x in antib: ex|=set(btag(x))
        names=[]
        for b in bl:
            for e in btag(b):
                if e not in ex: names.append(bname(e))
        names=list(dict.fromkeys(names))
        if names: loc['b']=names
        elif bl and not structs: dead.append((path,s['id'],bl)); return None
    if structs: loc['s']=structs
    if special: keys.append('special')
    # 폼
    asp=[x for x in s['pokemon'].split()[1:] if x not in IGN_ASP]
    form=None;unown=None
    if asp:
        if asp[0].startswith('character='): unown=asp[0].split('=')[1]
        elif asp[0].startswith(('snake_pattern=','face_spots','special_spots=','magikarp_jump=','tympole_pattern=','wooper_heart','whiscash_nero')): form='@'+' '.join(asp)
        else:
            if any(x.startswith('bull_breed=') for x in asp): asp=[x for x in asp if x!='paldean']
            fs=[ASP.get(x) for x in asp]
            if all(fs): form=' '.join(fs)
            else: miss[('aspect',tuple(asp))]+=1; form='?'+' '.join(asp)
    spid=s['pokemon'].split()[0]
    dex=SPID.get(spid)
    if not dex: miss[('species',spid)]+=1
    keys=list(dict.fromkeys(keys))
    return {'dex':dex,'form':form,'unown':unown,'r':RAR[s['bucket']],'lv':s['level'],'c':keys,**loc,'id':s['id'],'file':path}
if __name__=='__main__':
    cards=[c for c in (conv_entry(*x) for x in entries()) if c]
    json.dump(dead,open('dpwork/dead.json','w'))
    print('dead',dead)
    json.dump(cards,open('dpwork/cards.json','w'),ensure_ascii=False)
    print('cards',len(cards))
    for k,v in sorted(miss.items(),key=lambda kv:-kv[1]): print(v,k)
    print('special forms',collections.Counter(c['form'] for c in cards if c['form'] and c['form'].startswith('@')))
