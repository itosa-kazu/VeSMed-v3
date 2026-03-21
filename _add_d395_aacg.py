import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D395","name":"acute_angle_closure_glaucoma",
    "name_ja":"急性閉塞隅角緑内障",
    "category":"disease","category_sub":"ophthalmology",
    "states":["absent","present"],"severity":"high",
    "note":"急性眼圧上昇(50-80mmHg)。眼痛47-83%/視力低下82-86%/角膜浮腫80%/充血23-75%/散瞳固定/頭痛34%/悪心嘔吐24-44%。F:M=2-4:1、55-65歳。遠視/浅前房がリスク。鑑別:片頭痛/群発頭痛/ぶどう膜炎/CRAO/角膜炎/急性副鼻腔炎"
})

# === Step 2: Edges ===
FROM="D395"; FROM_NAME="acute_angle_closure_glaucoma"
d395_edges = [
    ("S123","AACG: 眼痛47-83%(PMC8841641)。急性眼圧上昇による激痛"),
    ("S122","AACG: 急性視力低下82-86%(PMC8841641)。角膜浮腫+視神経障害"),
    ("E25","AACG: 充血23-75%(PMC8841641)。毛様充血/結膜充血"),
    ("E63","AACG: 散瞳固定(mid-dilated, 14-100%, PMC8841641)。瞳孔反応消失"),
    ("S05","AACG: 頭痛34%(PMC8841641)。三叉神経分布の放散痛。片頭痛/SAHと誤診多い"),
    ("S13","AACG: 悪心/嘔吐24-44%(PMC8841641)。迷走神経反射。腹部疾患と誤診あり"),
    ("S59","AACG: めまい/眩暈。眼圧上昇に伴う自律神経症状"),
    ("E01","AACG: 無熱(定義的)。発熱は眼窩蜂窩織炎/ぶどう膜炎を示唆"),
    ("T01","AACG: 急性(時間~日)。未治療では24-72時間で不可逆的視神経障害"),
    ("T02","AACG: 突然発症(分~時間)。暗所/散瞳薬が誘因"),
]

for to_id, reason in d395_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Root priors: F:M=2-4:1, 55-65歳ピーク, prevalence 2-12/100,000
s3['root_priors']['D395'] = {
    "parents":["R02","R01"],
    "description":"AACG。F:M=3:1。55-65歳ピーク。有病率4/100,000/年",
    "cpt":{
        "male|18_39":0.0001,"male|40_64":0.0005,"male|65_plus":0.0008,
        "female|18_39":0.0003,"female|40_64":0.0015,"female|65_plus":0.0025
    }
}
s3['full_cpts']['D395'] = {
    "R01":{"description":"AACG年齢。55-65歳ピーク。40歳以上で急増","cpt":{
        "0_1":0.001,"1_5":0.001,"6_12":0.005,"13_17":0.01,
        "18_39":0.05,"40_64":0.40,"65_plus":0.533}},
    "R02":{"description":"AACG性別。F:M=3:1","cpt":{"male":0.25,"female":0.75}}
}

d395_cpts = {
    "S123":{"absent":0.15,"present":0.85},          # eye pain 47-83%, use 85% (acute attack)
    "S122":{"absent":0.15,"unilateral":0.83,"bilateral":0.02},  # visual loss 82-86%, unilateral
    "E25":{"absent":0.25,"present":0.75},            # conjunctival injection 23-75%
    "E63":{"normal":0.10,"mydriasis":0.85,"miosis":0.01,"anisocoria":0.03,"RAPD":0.01},  # mid-dilated fixed pupil
    "S05":{"absent":0.55,"mild":0.20,"severe":0.25}, # headache 34%, often severe
    "S13":{"absent":0.60,"present":0.40},            # nausea/vomiting 24-44%
    "S59":{"absent":0.70,"present":0.30},            # dizziness
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.70,"3d_to_1w":0.20,"1w_to_3w":0.08,"over_3w":0.02},
    "T02":{"sudden":0.65,"acute":0.30,"subacute":0.04,"chronic":0.01},
}

# Validate CPTs
ok=True
for v,c in d395_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D395'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate S123 (eye_pain) NOP ===
if 'S123' not in s3['noisy_or_params']:
    print("Activating S123 (eye_pain) NOP...")
    s123_var = next(v for v in s1['variables'] if v['id']=='S123')
    # leak: most people have no eye pain
    s3['noisy_or_params']['S123'] = {
        "leak":{"absent":0.97,"present":0.03},
        "parent_effects":{}
    }
    # Add existing parents from edges
    s123_parents = [e['from'] for e in s2['edges'] if e['to']=='S123' and e['from']!='D395']
    for pid in s123_parents:
        # D339 (retinal detachment): eye pain is less common (stretching not pain typically)
        if pid == 'D339':
            s3['noisy_or_params']['S123']['parent_effects']['D339'] = {"absent":0.70,"present":0.30}
    # Add D395
    s3['noisy_or_params']['S123']['parent_effects']['D395'] = d395_cpts['S123']
    print(f"  S123 activated with {len(s3['noisy_or_params']['S123']['parent_effects'])} parents")

# === Activate E63 (pupil_abnormality) NOP ===
if 'E63' not in s3['noisy_or_params']:
    print("Activating E63 (pupil_abnormality) NOP...")
    s3['noisy_or_params']['E63'] = {
        "leak":{"normal":0.95,"mydriasis":0.02,"miosis":0.01,"anisocoria":0.01,"RAPD":0.01},
        "parent_effects":{}
    }
    # D211 (brain herniation): mydriasis/anisocoria
    e63_parents = [e['from'] for e in s2['edges'] if e['to']=='E63' and e['from']!='D395']
    for pid in e63_parents:
        if pid == 'D211':
            s3['noisy_or_params']['E63']['parent_effects']['D211'] = {
                "normal":0.15,"mydriasis":0.50,"miosis":0.05,"anisocoria":0.25,"RAPD":0.05
            }
        elif pid == 'D339':
            # Retinal detachment: RAPD can occur
            s3['noisy_or_params']['E63']['parent_effects']['D339'] = {
                "normal":0.60,"mydriasis":0.05,"miosis":0.05,"anisocoria":0.10,"RAPD":0.20
            }
    # Add D395
    s3['noisy_or_params']['E63']['parent_effects']['D395'] = d395_cpts['E63']
    print(f"  E63 activated with {len(s3['noisy_or_params']['E63']['parent_effects'])} parents")

# IDF check: S123 and E63 need >=3 parents
for var_id in ['S123','E63']:
    n_parents = len(s3['noisy_or_params'][var_id]['parent_effects'])
    print(f"  {var_id}: {n_parents} parents {'OK' if n_parents >= 3 else 'NEED MORE'}")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD395: {len(d395_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
