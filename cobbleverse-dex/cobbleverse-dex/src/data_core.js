// 공통 도우미, 바이옴 묶음, 조건 사전. 데이터 출처: cobbleverse.wiki (COBBLEVERSE 공식 위키)
const JUNGLE=["Jungle","Sparse Jungle","Bamboo Jungle","Underground Jungle"];
const MOUNT=["Windswept Forest","Windswept Gravelly Hills","Windswept Hills","Windswept Savanna","Meadow","Alpine Grove","Alpine Highlands","Blooming Valley","Forested Highlands","Snowy Slopes","Lavender Valley","Lush Valley","Arid Highlands","Savanna Slopes","Moonlight Valley","Sakura Valley","Temperate Highlands","Blooming Plateau","Yosemite Lowlands","Caldera","Volcanic Crater"];
const MOUNTV=[...MOUNT,"Volcanic Peaks"];
const GEO=[...MOUNTV,"Yosemite Cliffs"];
const TEMPERATE=["River","Swamp","Mangrove Swamp","Orchid Swamp","Beach","Plains","Sunflower Plains","Cherry Grove","Forest","Flower Forest","Meadow","Birch Forest","Old Growth Birch Forest","Brushland","Shrubland","Steppe","Valley Clearing","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Alpine Highlands","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands","Arid Highlands","Blooming Plateau"];
const VAPO=TEMPERATE.filter(b=>b!=="Beach");
const FOREST=["Forest","Cherry Grove","Flower Forest","Birch Forest","Old Growth Birch Forest","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands"];
const FOREST_D=["Forest","Cherry Grove","Flower Forest","Birch Forest","Dark Forest","Old Growth Birch Forest","Pale Garden","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands"];
const FOREST_G=["Forest","Cherry Grove","Flower Forest","Birch Forest","Grove","Old Growth Birch Forest","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands"];
const FOREST_ALL=["Forest","Cherry Grove","Flower Forest","Birch Forest","Dark Forest","Grove","Old Growth Birch Forest","Pale Garden","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands"];
const PLAINS=["Plains","Sunflower Plains","Meadow","Brushland","Shrubland","Steppe","Alpine Highlands","Arid Highlands","Blooming Plateau","Valley Clearing"];
const PIDGEY=["Plains","Sunflower Plains","Cherry Grove","Forest","Flower Forest","Meadow","Birch Forest","Grove","Old Growth Birch Forest","Brushland","Shrubland","Steppe","Valley Clearing","Blooming Valley","Forested Highlands","Lavender Forest","Lavender Valley","Alpine Highlands","Mirage Isles","Sakura Grove","Sakura Valley","Temperate Highlands","Arid Highlands","Blooming Plateau"];
const BUTTER=["Plains","Forest","Birch Forest","Old Growth Birch Forest","Brushland","Shrubland","Steppe","Valley Clearing","Forested Highlands","Alpine Highlands","Mirage Isles","Temperate Highlands","Arid Highlands"];
const FLOWER=["Cherry Grove","Flower Forest","Meadow","Sunflower Plains","Blooming Plateau","Blooming Valley","Cloud Forest","Lavender Forest","Lavender Valley","Sakura Grove","Sakura Valley"];
const PLAINS3=["Plains","Brushland","Shrubland","Steppe","Alpine Highlands","Arid Highlands","Valley Clearing"];
const PLAINS2=["Plains","Sunflower Plains","Brushland","Shrubland","Steppe","Valley Clearing"];
const SAVX=["Savanna","Savanna Plateau","Arid Highlands","Ashen Savanna","Desert Oasis","Hot Shrubland","Red Oasis","Savanna Slopes","Windswept Savanna"];
const RAT=[...PLAINS2,...SAVX];
const SAVANNA=["Savanna","Savanna Plateau","Windswept Savanna","Arid Highlands","Ashen Savanna","Brushland","Desert Oasis","Hot Shrubland","Red Oasis","Savanna Slopes","Shrubland"];
const BADLANDS=["Badlands","Wooded Badlands","Eroded Badlands","Ashen Savanna","Red Oasis"];
const BADL=[...BADLANDS,"Savanna","Savanna Plateau","Windswept Savanna","Arid Highlands","Brushland","Desert Oasis","Hot Shrubland","Savanna Slopes","Shrubland"];
const DESERT=["Desert","Ancient Sands","Desert Canyon","Desert Oasis","Lush Desert","Sandstone Valley"];
const SAND=["Desert","Ancient Sands","Desert Canyon","Desert Oasis","Lush Desert","Red Oasis","Sandstone Valley"];
const EKANS=[...BADLANDS,...DESERT,"Savanna","Savanna Plateau","Arid Highlands","Brushland","Shrubland","Hot Shrubland","Savanna Slopes"];
const FREEZE=["Grove","Frozen River","Jagged Peaks","Snowy Beach","Snowy Plains","Snowy Slopes","Snowy Taiga","Snowy Badlands","Alpine Grove","Frozen Peaks","Ice Spikes","Glacial Chasm","Siberian Taiga","Ice Marsh","Siberian Grove","Snowy Cherry Grove","Cold Shrubland","Snowy Shield","Wintry Forest","Wintry Lowlands","Frozen Ocean","Deep Frozen Ocean"];
const MEOWA=[...EKANS,...FREEZE];
const MEOWG=[...FREEZE,"Taiga","Old Growth Pine Taiga","Old Growth Spruce Taiga","Bryce Canyon","Cloud Forest","Moonlight Grove","Moonlight Valley","Shield","Yosemite Lowlands"];
const SNOWSAND=["Frozen Peaks","Ice Spikes","Glacial Chasm","Siberian Taiga","Siberian Grove","Ice Marsh","Alpine Grove","Snowy Cherry Grove","Snowy Shield","Cold Shrubland","Wintry Forest","Wintry Lowlands"];
const AVULPIX=["Ice Marsh","Siberian Grove","Snowy Cherry Grove","Grove","Snowy Taiga","Alpine Grove","Cold Shrubland","Snowy Shield","Wintry Forest","Wintry Lowlands"];
const SWAMP=["Mangrove Swamp","Swamp","Ice Marsh","Orchid Swamp"];
const SWAMP3=["Mangrove Swamp","Swamp","Orchid Swamp"];
const DARK=["Dark Forest","Pale Garden","Deep Dark"];
const MYST=["Dark Forest","Amethyst Canyon","Amethyst Rainforest","Mirage Isles","Moonlight Grove","Moonlight Valley"];
const POLI=["River",...JUNGLE,...MYST,"Mushroom Fields","Fungal Caves"];
const LUSHC=["Lush Caves","Fungal Caves","Underground Jungle"];
const OCEAN=["Ocean","Warm Ocean","Lukewarm Ocean","Cold Ocean","Frozen Ocean","Deep Ocean","Deep Cold Ocean","Deep Warm Ocean"];
const SHORE=["Beach","Snowy Beach","Stony Shore","White Cliffs"];
const COLDO=["Cold Ocean","Deep Cold Ocean","Deep Frozen Ocean","Frozen Ocean"];
const WARMO=["Ocean","Warm Ocean","Lukewarm Ocean","Deep Ocean","Deep Warm Ocean"];
const RIVERS=["River","Warm River","Frozen River"];
const KARP=["River","Frozen River","Swamp","Mangrove Swamp","Ice Marsh","Orchid Swamp",...OCEAN];
const HORSEA=["Deep Lukewarm Ocean","Lukewarm Ocean","Warm Ocean"];
const SEEL=["Deep Frozen Ocean","Frozen Ocean"];
const HGROW=["Jagged Peaks","Snowy Slopes","Stony Peaks","Rocky Mountains","Volcanic Peaks"];
const ABRA=[...MOUNT.filter(b=>b!=="Moonlight Valley"),"Plains","Sunflower Plains","Cherry Grove","Forest","Flower Forest","Birch Forest","Grove","Old Growth Birch Forest","Pale Garden","Brushland","Shrubland","Steppe","Valley Clearing","Lavender Forest","Sakura Grove"];
const RHY=["Meadow","Windswept Forest","Windswept Gravelly Hills","Windswept Hills","Windswept Savanna","Alpine Grove","Alpine Highlands","Blooming Valley","Forested Highlands","Lavender Valley","Lush Valley","Arid Highlands","Savanna Slopes","Sakura Valley","Temperate Highlands","Blooming Plateau","Caldera","Volcanic Crater","Volcanic Peaks","Yosemite Cliffs","Savanna","Savanna Plateau","Ashen Savanna","Brushland","Desert Oasis","Hot Shrubland","Red Oasis","Shrubland"];
const SCY_M=["Windswept Forest","Windswept Gravelly Hills","Windswept Hills","Windswept Savanna","Meadow","Alpine Highlands","Lush Valley","Arid Highlands","Savanna Slopes","Moonlight Valley","Blooming Plateau","Yosemite Lowlands","Caldera","Volcanic Crater"];
const SNORLAX=["Ice Marsh","Siberian Grove","Snowy Cherry Grove",...FOREST_ALL,"Windswept Forest","Windswept Gravelly Hills","Windswept Hills","Windswept Savanna","Meadow","Alpine Grove","Alpine Highlands","Snowy Slopes","Lush Valley","Arid Highlands","Savanna Slopes","Moonlight Valley","Blooming Plateau","Yosemite Lowlands","Caldera","Volcanic Crater"];
const TAUROS=["Plains","Sunflower Plains","Brushland","Shrubland","Steppe","Valley Clearing","Savanna","Savanna Plateau","Ashen Savanna","Desert Oasis","Hot Shrubland","Red Oasis"];
const PALDEA_T=["Meadow","Alpine Highlands","Arid Highlands","Blooming Plateau"];
const JOLT=[...PLAINS2,...SAVX,"Meadow","Windswept Forest","Windswept Gravelly Hills","Windswept Hills","Alpine Grove","Alpine Highlands","Blooming Valley","Forested Highlands","Snowy Slopes","Lavender Valley","Lush Valley","Moonlight Valley","Sakura Valley","Temperate Highlands","Blooming Plateau","Yosemite Lowlands","Caldera","Volcanic Crater","Volcanic Peaks","Yosemite Cliffs"];
const CLEF1=["Dripstone Caves","Amethyst Canyon","Amethyst Rainforest","Mirage Isles","Moonlight Grove","Moonlight Valley"];
const PARAS2=["Dark Forest","Mushroom Fields","Fungal Caves","Mirage Isles","Crimson Forest"];
const VIL4=["Village (Plains)","Village (Taiga)","Village (Snowy)","Village (Savanna)"];
const VILD=["Village (Plains)","Village (Desert)","Village (Taiga)","Village (Savanna)"];
const VILGR=["Village (Desert)","Village (Taiga)","Village (Snowy)","Village (Savanna)"];
const VILALL=["Village (All Types)"];
const MANSION=["Woodland Mansion"];
const RUINS=["Cold Ocean Ruins","Warm Ocean Ruins"];
const LSC=["Lush Shipwreck Cove"], SSC=["Submerged Shipwreck Cove"];

const K={maxY48:"Y 48 이하",minY48:"Y 48 이상",inlava:"용암 속",cobweb:"거미줄 근처",sunflower:"해바라기 근처",coral:"산호 근처",deadcoral:"죽은 산호 근처",quartz:"석영 블록 위",wool:"양털/카펫 근처",twi5:"황혼 때 ×5",storm33:"뇌우 때 ×3.3",day33:"낮에 ×3.3",rain33:"비 올 때 ×3.3",sky:"하늘빛 8–15",dim:"하늘빛 0–7",sky0:"하늘빛 0",light0:"밝기 0",clear:"맑음",day:"낮",night:"밤",rain:"비",storm:"뇌우",water:"물 근처",flow:"흐르는 물 근처",sub:"물속",surf:"수면",floor:"해저",inwater:"물 안",seeSky:"하늘이 보여야 함",indoor:"실내/지하",minY0:"Y 0 이상",maxY0:"Y 0 이하",maxY32:"Y 32 이하",maxY62:"Y 62 이하",shipY:"Y -41~9",subY:"Y -60~13",t2:"뇌우 때 ×2",t25:"뇌우 때 ×2.5",t5:"뇌우 때 ×5",twi:"황혼 때 ×2.5",n15:"밤에 ×1.5",n025:"밤에 ×0.25",n5:"밤에 ×5",d15:"낮에 ×1.5",d025:"낮에 ×0.25",moon:"보름달",lily:"연잎 근처",redstone:"레드스톤 근처",rod:"피뢰침 근처",leek:"약용 파 근처",nowater:"물이 없는 곳",iron:"철광석 근처",lava:"용암/마그마 블록 근처",apri:"규토리 근처",sacch:"사카린 나무 근처",nosacch:"사카린 나무가 없는 곳",slime:"슬라임 청크",lava5:"용암 근처 ×5",water5:"물 근처 ×5",special:"특수 조우"};
// e(희귀도, 레벨, 조건키, 장소) — 장소: {b:[바이옴]} {s:[구조물]} {all:"ow"|"nether"|"end", ex:[제외]}
const e=(r,lv,c,w)=>({r,lv,c:c.map(k=>K[k]),...w});
const B=b=>({b}), S=s=>({s}), OW=(ex=[])=>({all:"ow",ex});
const P=[]; // [dex, ko, en, form(ko|null), entries]
function add(d,ko,en,form,entries){P.push({d,ko,en,form,entries});}


const UNLOCK={}; // 도감번호: 출현 시점 안내
const U_=a=>[...new Set(a)];
