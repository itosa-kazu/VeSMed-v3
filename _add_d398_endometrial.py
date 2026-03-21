import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D398","name":"endometrial_cancer",
    "name_ja":"子宮体癌(子宮内膜癌)",
    "category":"disease","category_sub":"gynecology",
    "states":["absent","present"],"severity":"high",
    "note":"不正性器出血90%+(最多症状)。閉経後出血の9%が子宮体癌。肥満(BMI>30→2.6倍)が最強リスク。60歳ピーク。骨盤US:子宮内膜肥厚。鑑別:子宮筋腫/子宮頸癌/異所性妊娠/DUB/凝固障害"
})

# === Step 2: Edges ===
FROM="D398"; FROM_NAME="endometrial_cancer"
d398_edges = [
    ("S127","EC: 不正性器出血90%+(StatPearls NBK525981)。最多の初発症状。閉経後出血が典型"),
    ("S12","EC: 腹痛/骨盤痛。進行例で30-40%。子宮壁浸潤/腹膜播種"),
    ("S07","EC: 倦怠感。悪性腫瘍に伴う全身症状+慢性出血による貧血"),
    ("S17","EC: 体重減少。進行例で20%。悪性腫瘍に伴うcachexia"),
    ("S128","EC: 帯下(水様/血性)。閉経後の異常分泌物"),
    ("L62","EC: 骨盤US: 子宮内膜肥厚>4mm(閉経後)→生検適応"),
    ("E85","EC: 結膜蒼白(貧血)。慢性性器出血による鉄欠乏性貧血"),
    ("E01","EC: 無熱(定義的)。発熱→感染合併を示唆"),
    ("T01","EC: 慢性(数ヶ月~)。緩徐進行"),
    ("T02","EC: 慢性発症。数ヶ月かけて出血量増加"),
]

for to_id, reason in d398_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Female only, 55-65歳ピーク
s3['root_priors']['D398'] = {
    "parents":["R02","R01"],
    "description":"EC。女性のみ。55-65歳ピーク",
    "cpt":{
        "male|18_39":0.0,"male|40_64":0.0,"male|65_plus":0.0,
        "female|18_39":0.0005,"female|40_64":0.003,"female|65_plus":0.004
    }
}
s3['full_cpts']['D398'] = {
    "R01":{"description":"EC年齢。55-65歳ピーク","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.001,
        "18_39":0.05,"40_64":0.40,"65_plus":0.549}},
    "R02":{"description":"EC性別。女性のみ","cpt":{"male":0.0,"female":1.0}}
}

d398_cpts = {
    "S127":{"absent":0.08,"present":0.92},           # vaginal bleeding 90%+
    "S12":{"absent":0.65,"present":0.35},             # pelvic pain 30-40%
    "S07":{"absent":0.50,"mild":0.30,"severe":0.20},  # fatigue from anemia
    "S17":{"absent":0.80,"present":0.20},             # weight loss 20%
    "S128":{"absent":0.60,"present":0.40},            # vaginal discharge
    "L62":{"normal":0.10,"adnexal_mass":0.05,"free_fluid":0.05,"uterine_abnormal":0.80},
    "E85":{"absent":0.60,"present":0.40},             # conjunctival pallor (anemia)
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.05,"over_3w":0.90},
    "T02":{"sudden":0.03,"acute":0.05,"subacute":0.12,"chronic":0.80},
}

ok=True
for v,c in d398_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D398'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate S127 (abnormal_vaginal_bleeding) NOP ===
if 'S127' not in s3['noisy_or_params']:
    print("Activating S127 (abnormal_vaginal_bleeding) NOP...")
    s3['noisy_or_params']['S127'] = {
        "leak":{"absent":0.95,"present":0.05},
        "parent_effects":{}
    }
    # Add existing parent D276 (ovarian torsion)
    s3['noisy_or_params']['S127']['parent_effects']['D276'] = {"absent":0.70,"present":0.30}
    # Add D398
    s3['noisy_or_params']['S127']['parent_effects']['D398'] = d398_cpts['S127']
    # Add D291 (ectopic pregnancy) — vaginal bleeding is key symptom
    s2['edges'].append({"from":"D291","to":"S127","from_name":"ectopic_pregnancy",
        "to_name":"abnormal_vaginal_bleeding","reason":"異所性妊娠: 不正性器出血60-80%。腹痛+無月経+出血の三徴"})
    s3['noisy_or_params']['S127']['parent_effects']['D291'] = {"absent":0.25,"present":0.75}
    # Add D26 (PID) — can cause abnormal bleeding
    s2['edges'].append({"from":"D26","to":"S127","from_name":"pelvic_inflammatory_disease",
        "to_name":"abnormal_vaginal_bleeding","reason":"PID: 不正出血30-40%。子宮内膜炎に伴う"})
    s3['noisy_or_params']['S127']['parent_effects']['D26'] = {"absent":0.65,"present":0.35}
    s2['total_edges'] = len(s2['edges'])
    print(f"  S127 activated with {len(s3['noisy_or_params']['S127']['parent_effects'])} parents")

# === Activate S128 (vaginal_discharge) NOP ===
if 'S128' not in s3['noisy_or_params']:
    print("Activating S128 (vaginal_discharge) NOP...")
    s3['noisy_or_params']['S128'] = {
        "leak":{"absent":0.90,"present":0.10},
        "parent_effects":{}
    }
    # Check existing edges to S128
    s128_parents = set(e['from'] for e in s2['edges'] if e['to']=='S128')
    for pid in s128_parents:
        if pid == 'D26':  # PID
            s3['noisy_or_params']['S128']['parent_effects']['D26'] = {"absent":0.30,"present":0.70}
    # Add D398
    s3['noisy_or_params']['S128']['parent_effects']['D398'] = d398_cpts['S128']
    # Add D291 (ectopic) if not already
    if 'D291' not in s3['noisy_or_params']['S128']['parent_effects']:
        s2['edges'].append({"from":"D291","to":"S128","from_name":"ectopic_pregnancy",
            "to_name":"vaginal_discharge","reason":"異所性妊娠: 帯下(血性分泌物)"})
        s3['noisy_or_params']['S128']['parent_effects']['D291'] = {"absent":0.60,"present":0.40}
    s2['total_edges'] = len(s2['edges'])
    print(f"  S128 activated with {len(s3['noisy_or_params']['S128']['parent_effects'])} parents")

# IDF check
for var_id in ['S127','S128']:
    if var_id in s3['noisy_or_params']:
        n = len(s3['noisy_or_params'][var_id]['parent_effects'])
        print(f"  {var_id}: {n} parents {'OK' if n >= 3 else 'NEED MORE'}")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD398: {len(d398_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
