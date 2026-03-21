import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D403","name":"tetralogy_of_fallot",
    "name_ja":"ファロー四徴症(TOF)",
    "category":"disease","category_sub":"cardiovascular",
    "states":["absent","present"],"severity":"high",
    "note":"最多チアノーゼ性先天性心疾患(5-7/10,000出生)。四徴:VSD+RVOTO+大動脈騎乗+右室肥大。70-80%チアノーゼ、20-30%はpink Tet。無修復生存:1歳66%、20歳11%。ばち指+多血症+低酸素。鑑別:大血管転位/総動脈幹/三尖弁閉鎖/Ebstein"
})

# === Step 2: Edges ===
FROM="D403"; FROM_NAME="tetralogy_of_fallot"
d403_edges = [
    ("E42","TOF: チアノーゼ70-80%(StatPearls NBK513288)。右左シャントによる動脈血酸素低下。pink Tet 20-30%"),
    ("E05","TOF: SpO2低下。無修復例でSpO2 55-89%(症例報告)。重度RVOTO→著明低酸素"),
    ("E15","TOF: 心雑音~100%。RVOT閉塞による粗い収縮期駆出性雑音。左胸骨縁上部"),
    ("E40","TOF: ECG: 右室肥大(RVH)~95%。右軸偏位。V1にqRまたはR波"),
    ("S04","TOF: 呼吸困難80-90%。労作時→安静時(重症)。RVOTO重症度に相関"),
    ("E95","TOF: 皮膚チアノーゼ70-80%。口唇/爪床/粘膜。慢性低酸素"),
    ("E55","TOF: ばち指60-80%(慢性チアノーゼ)。無修復例>2歳でほぼ全例。低酸素→微小血管増生"),
    ("S07","TOF: 倦怠感。慢性低酸素+多血症→運動耐容能低下"),
    ("E01","TOF: 通常無熱。発熱→IE合併/脳膿瘍(右左シャント→菌血症リスク)"),
    ("T01","TOF: 先天性。出生時~乳児期から症状(chronic)"),
    ("T02","TOF: 慢性(先天性)。出生時から存在するが症状は月~年単位で進行"),
]

for to_id, reason in d403_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Pediatric onset, slight male preponderance
s3['root_priors']['D403'] = {
    "parents":["R02","R01"],
    "description":"TOF。先天性心疾患。小児が主。M:F≈1.3:1",
    "cpt":{
        "male|18_39":0.0002,"male|40_64":0.0001,"male|65_plus":0.00005,
        "female|18_39":0.0001,"female|40_64":0.00005,"female|65_plus":0.00002
    }
}
s3['full_cpts']['D403'] = {
    "R01":{"description":"TOF年齢。先天性。乳幼児が主だが未修復成人も","cpt":{
        "0_1":0.35,"1_5":0.25,"6_12":0.15,"13_17":0.08,
        "18_39":0.10,"40_64":0.05,"65_plus":0.02}},
    "R02":{"description":"TOF性別。M:F≈1.3:1(StatPearls)","cpt":{"male":0.57,"female":0.43}}
}

d403_cpts = {
    "E42":{"normal":0.20,"pallor_cold":0.05,"cyanosis":0.70,"gangrene":0.05},  # cyanosis 70-80%
    "E05":{"normal_over_96":0.15,"mild_hypoxia_93_96":0.20,"severe_hypoxia_under_93":0.65},  # severe
    "E15":{"absent":0.02,"pre_existing":0.03,"new":0.95},  # murmur ~100%
    "E40":{"normal":0.03,"ST_elevation":0.01,"ST_depression":0.01,"AF":0.02,
           "QT_prolongation":0.01,"Brugada_pattern":0.01,"RVH_strain":0.85,
           "LVH_pattern":0.02,"SVT":0.02,"VT":0.02},  # RVH 95%
    "S04":{"absent":0.10,"on_exertion":0.55,"at_rest":0.35},  # dyspnea 80-90%
    "E95":{"normal":0.20,"pallor":0.05,"cyanosis":0.70,"flushing":0.01,
           "bronze":0.01,"hyperpigmentation":0.03},
    "E55":{"normal":0.25,"splinter_hemorrhage":0.02,"clubbing":0.70,"janeway_osler":0.03},
    "S07":{"absent":0.20,"mild":0.40,"severe":0.40},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,
           "38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.05,"3d_to_1w":0.05,"1w_to_3w":0.05,"over_3w":0.85},
    "T02":{"sudden":0.05,"acute":0.05,"subacute":0.10,"chronic":0.80},
}

ok=True
for v,c in d403_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D403'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate E55 (nail/digital findings) NOP ===
if 'E55' not in s3['noisy_or_params']:
    print("Activating E55 (nail_digital_findings) NOP...")
    s3['noisy_or_params']['E55'] = {
        "leak":{"normal":0.95,"splinter_hemorrhage":0.02,"clubbing":0.02,"janeway_osler":0.01},
        "parent_effects":{}
    }
    # Existing parent: D203 (scleroderma)
    e55_parents = set(e['from'] for e in s2['edges'] if e['to']=='E55' and e['from']!='D403')
    for pid in e55_parents:
        # D203 scleroderma → nail changes (digital ischemia)
        s3['noisy_or_params']['E55']['parent_effects'][pid] = {
            "normal":0.50,"splinter_hemorrhage":0.10,"clubbing":0.30,"janeway_osler":0.10}

    # Add D403
    s3['noisy_or_params']['E55']['parent_effects']['D403'] = d403_cpts['E55']

    # IDF strengthen: add D14 (IE) → E55 (Osler/Janeway/splinter)
    s2['edges'].append({"from":"D14","to":"E55","from_name":"infective_endocarditis",
        "to_name":"nail_digital_findings",
        "reason":"IE: Osler結節/Janeway病変/線状出血。subacute IEでばち指も。IE標識所見"})
    s3['noisy_or_params']['E55']['parent_effects']['D14'] = {
        "normal":0.50,"splinter_hemorrhage":0.25,"clubbing":0.05,"janeway_osler":0.20}

    # Add D130 (IPF) → E55 (clubbing)
    s2['edges'].append({"from":"D130","to":"E55","from_name":"interstitial_lung_disease",
        "to_name":"nail_digital_findings",
        "reason":"IPF: ばち指20-40%(Harrison's)。進行性線維化→慢性低酸素"})
    s3['noisy_or_params']['E55']['parent_effects']['D130'] = {
        "normal":0.60,"splinter_hemorrhage":0.02,"clubbing":0.35,"janeway_osler":0.03}

    # Add D277 (lung adenocarcinoma) → E55 (clubbing)
    s2['edges'].append({"from":"D277","to":"E55","from_name":"lung_adenocarcinoma",
        "to_name":"nail_digital_findings",
        "reason":"肺腺癌: ばち指5-15%(Harrison's)。肥大性骨関節症(HOA)"})
    s3['noisy_or_params']['E55']['parent_effects']['D277'] = {
        "normal":0.85,"splinter_hemorrhage":0.02,"clubbing":0.10,"janeway_osler":0.03}

    s2['total_edges'] = len(s2['edges'])
    n = len(s3['noisy_or_params']['E55']['parent_effects'])
    print(f"  E55 activated with {n} parents")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD403: {len(d403_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
