import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D405","name":"breast_cancer",
    "name_ja":"乳癌",
    "category":"disease","category_sub":"gynecology",
    "states":["absent","present"],"severity":"high",
    "note":"女性癌1位。無痛性乳房腫瘤(80%)が主訴。腋窩リンパ節転移40-50%。乳頭分泌(血性5-10%)。転移:骨>肺>肝>脳。50-70歳ピーク。BRCA1/2。M:F≈1:100。鑑別:線維腺腫/乳腺症/乳腺炎/乳管内乳頭腫/葉状腫瘍"
})

# === Step 2: Edges ===
FROM="D405"; FROM_NAME="breast_cancer"
d405_edges = [
    ("S143","乳癌: 無痛性乳房腫瘤80%(StatPearls)。最多初発症状。硬く不整形"),
    ("E13","乳癌: 腋窩リンパ節腫脹40-50%(Harrison's)。同側腋窩が最多"),
    ("E46","乳癌: 腋窩リンパ節(Harrison's)。鎖骨上は進行例"),
    ("S144","乳癌: 乳頭分泌5-10%。血性が悪性示唆"),
    ("S148","乳癌: 血性乳頭分泌。乳管内乳頭腫との鑑別"),
    ("S129","乳癌: 乳房痛5-15%。通常無痛性だが炎症性乳癌では疼痛あり"),
    ("S17","乳癌: 体重減少20-30%(進行例)。悪性cachexia"),
    ("L63","乳癌: 転移(進行例40%): 骨>肺>肝>脳。骨転移最多"),
    ("L104","乳癌: ALP上昇(骨転移)。溶骨性+造骨性混合型"),
    ("S07","乳癌: 倦怠感。悪性腫瘍+化学療法"),
    ("E01","乳癌: 通常無熱。発熱→炎症性乳癌/膿瘍/好中球減少性発熱"),
    ("T01","乳癌: 慢性(数ヶ月~)。緩徐増大する腫瘤"),
    ("T02","乳癌: 慢性発症。数ヶ月~年で発見"),
]

for to_id, reason in d405_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Female predominant (M:F=1:100), 50-70歳ピーク
s3['root_priors']['D405'] = {
    "parents":["R02","R01"],
    "description":"乳癌。女性が99%。50-70歳ピーク。BRCA家族歴",
    "cpt":{
        "male|18_39":0.0,"male|40_64":0.00005,"male|65_plus":0.00005,
        "female|18_39":0.001,"female|40_64":0.004,"female|65_plus":0.003
    }
}
s3['full_cpts']['D405'] = {
    "R01":{"description":"乳癌年齢。50-70歳ピーク","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.001,
        "18_39":0.10,"40_64":0.50,"65_plus":0.399}},
    "R02":{"description":"乳癌性別。F>>M(Harrison's)","cpt":{"male":0.01,"female":0.99}}
}

d405_cpts = {
    "S143":{"absent":0.15,"present":0.85},              # breast mass 80%+
    "E13":{"absent":0.50,"present":0.50},               # axillary LAD 40-50%
    "E46":{"cervical":0.02,"axillary":0.80,"inguinal":0.01,
           "supraclavicular":0.10,"mediastinal":0.02,"generalized":0.05},
    "S144":{"absent":0.90,"present":0.10},              # nipple discharge 5-10%
    "S148":{"milky":0.05,"bloody":0.70,"serous":0.25},  # bloody dominant in cancer
    "S129":{"absent":0.85,"present":0.15},              # breast pain 5-15%
    "S17":{"absent":0.70,"present":0.30},               # weight loss 20-30%
    "L63":{"absent":0.55,"lung":0.05,"bone":0.20,"liver":0.08,
           "brain":0.02,"multiple":0.10},               # bone most common metastasis
    "L104":{"normal":0.60,"mild_elevated":0.25,"moderate_elevated":0.10,"markedly_elevated":0.05},
    "S07":{"absent":0.45,"mild":0.35,"severe":0.20},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,
           "38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.05,"over_3w":0.90},
    "T02":{"sudden":0.02,"acute":0.03,"subacute":0.10,"chronic":0.85},
}

ok=True
for v,c in d405_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D405'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate S143 (breast_mass) NOP ===
if 'S143' not in s3['noisy_or_params']:
    print("Activating S143 (breast_mass) NOP...")
    s3['noisy_or_params']['S143'] = {
        "leak":{"absent":0.97,"present":0.03},
        "parent_effects":{}
    }
    s3['noisy_or_params']['S143']['parent_effects']['D405'] = d405_cpts['S143']
    # IDF: breast mass is highly specific. Only breast cancer in our model.
    # Add edge from D67 (NHL) → breast mass (rare but documented lymphoma presentation)
    s2['edges'].append({"from":"D67","to":"S143","from_name":"non_hodgkin_lymphoma",
        "to_name":"breast_mass","reason":"NHL: 乳房原発リンパ腫(稀, <1%)。乳腺腫瘤として発見"})
    s3['noisy_or_params']['S143']['parent_effects']['D67'] = {"absent":0.98,"present":0.02}
    # Add edge from D354 (HL) → very rare
    s2['edges'].append({"from":"D354","to":"S143","from_name":"hodgkin_lymphoma",
        "to_name":"breast_mass","reason":"HL: 乳房浸潤(極稀)。若年女性HL後のRT-induced乳癌リスク"})
    s3['noisy_or_params']['S143']['parent_effects']['D354'] = {"absent":0.99,"present":0.01}
    s2['total_edges'] = len(s2['edges'])
    n = len(s3['noisy_or_params']['S143']['parent_effects'])
    print(f"  S143 activated with {n} parents")

# === Activate S144 (nipple_discharge) NOP ===
if 'S144' not in s3['noisy_or_params']:
    print("Activating S144 (nipple_discharge) NOP...")
    s3['noisy_or_params']['S144'] = {
        "leak":{"absent":0.97,"present":0.03},
        "parent_effects":{}
    }
    s3['noisy_or_params']['S144']['parent_effects']['D405'] = d405_cpts['S144']
    # Check existing S144 parents
    s144_parents = set(e['from'] for e in s2['edges'] if e['to']=='S144' and e['from']!='D405')
    for pid in s144_parents:
        if pid == 'D345':  # Sheehan syndrome → galactorrhea/agalactia
            s3['noisy_or_params']['S144']['parent_effects']['D345'] = {"absent":0.70,"present":0.30}
    # Add prolactinoma-related discharge
    # D380 (pituitary adenoma/prolactinoma) → milky discharge
    if 'D380' in [v['id'] for v in s1['variables']]:
        s2['edges'].append({"from":"D380","to":"S144","from_name":"pituitary_adenoma",
            "to_name":"nipple_discharge","reason":"プロラクチノーマ: 乳汁漏出(galactorrhea)50-80%。高プロラクチン"})
        s3['noisy_or_params']['S144']['parent_effects']['D380'] = {"absent":0.30,"present":0.70}
    s2['total_edges'] = len(s2['edges'])
    n = len(s3['noisy_or_params']['S144']['parent_effects'])
    print(f"  S144 activated with {n} parents")

# === Activate S148 (nipple_discharge_type) NOP ===
if 'S148' not in s3['noisy_or_params']:
    print("Activating S148 (nipple_discharge_type) NOP...")
    s3['noisy_or_params']['S148'] = {
        "leak":{"milky":0.40,"bloody":0.20,"serous":0.40},
        "parent_effects":{}
    }
    s3['noisy_or_params']['S148']['parent_effects']['D405'] = d405_cpts['S148']
    if 'D380' in [v['id'] for v in s1['variables']]:
        s2['edges'].append({"from":"D380","to":"S148","from_name":"pituitary_adenoma",
            "to_name":"nipple_discharge_type","reason":"プロラクチノーマ: 乳汁性(milky)が特徴的"})
        s3['noisy_or_params']['S148']['parent_effects']['D380'] = {"milky":0.90,"bloody":0.02,"serous":0.08}
    s2['total_edges'] = len(s2['edges'])
    n = len(s3['noisy_or_params']['S148']['parent_effects'])
    print(f"  S148 activated with {n} parents")

# === Activate S129 (breast_pain) NOP ===
if 'S129' not in s3['noisy_or_params']:
    print("Activating S129 (breast_pain) NOP...")
    s3['noisy_or_params']['S129'] = {
        "leak":{"absent":0.95,"present":0.05},
        "parent_effects":{}
    }
    s3['noisy_or_params']['S129']['parent_effects']['D405'] = d405_cpts['S129']
    # Check existing S129 parents
    s129_parents = set(e['from'] for e in s2['edges'] if e['to']=='S129' and e['from']!='D405')
    for pid in s129_parents:
        s3['noisy_or_params']['S129']['parent_effects'][pid] = {"absent":0.40,"present":0.60}
    s2['total_edges'] = len(s2['edges'])
    n = len(s3['noisy_or_params']['S129']['parent_effects'])
    print(f"  S129 activated with {n} parents")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD405: {len(d405_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
