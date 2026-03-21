import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D402","name":"small_cell_lung_cancer",
    "name_ja":"小細胞肺癌(SCLC)",
    "category":"disease","category_sub":"respiratory",
    "states":["absent","present"],"severity":"high",
    "note":"全肺癌の13-15%。中枢型(90%)。急速増殖(倍加時間54-132日)。60-70%が初診時extensive。SIADH(10-45%)/Cushing(2-5%)/Lambert-Eaton(3%)等paraneoplastic。喫煙95%。M:F≈1.5:1、60-70歳。鑑別:肺腺癌/肺扁平上皮癌/リンパ腫/胸腺腫/転移性肺腫瘍"
})

# === Step 2: Edges ===
FROM="D402"; FROM_NAME="small_cell_lung_cancer"
d402_edges = [
    ("S01","SCLC: 咳嗽70-75%(StatPearls NBK482458)。中枢型で気道刺激/閉塞"),
    ("S04","SCLC: 呼吸困難40-75%(Medscape)。腫瘤圧迫/胸水/SVC症候群"),
    ("S16","SCLC: 喀血20-30%(Medscape)。気道浸潤"),
    ("S17","SCLC: 体重減少60-80%(Medscape)。悪性cachexia+食欲不振"),
    ("S21","SCLC: 胸痛20-40%(Medscape)。胸壁浸潤/胸膜炎性"),
    ("S07","SCLC: 倦怠感60%。悪性腫瘍+paraneoplastic(SIADH/Cushing)"),
    ("S55","SCLC: 嗄声5-10%(Medscape)。反回神経麻痺(縦隔浸潤)"),
    ("S46","SCLC: 食欲不振50%。cachexia+SIADH関連の悪心"),
    ("S25","SCLC: 嚥下困難5-10%(Medscape)。食道圧迫"),
    ("L04","SCLC: 胸部X線。中枢型腫瘤90%→肺門腫大/縦隔拡大。胸水も"),
    ("L44","SCLC: 低Na血症(SIADH)10-45%(PMC7656388)。最多paraneoplastic"),
    ("L16","SCLC: LDH上昇44%(PMC8636211)。腫瘍量マーカー/予後因子"),
    ("E13","SCLC: リンパ節腫脹。縦隔/鎖骨上リンパ節。初診時66%縦隔浸潤"),
    ("E46","SCLC: 鎖骨上/縦隔リンパ節。N2/N3が多い"),
    ("L63","SCLC: 転移巣。60-70%がextensive(PMC8177722)。骨50-67%/脳10-20%/肝転移"),
    ("S84","SCLC: 咳嗽は乾性/湿性両方。気道閉塞パターン"),
    ("E01","SCLC: 通常無熱。発熱→閉塞性肺炎合併を示唆"),
    ("T01","SCLC: 8-12週の症状期間(StatPearls)。急速増殖だが受診まで数週"),
    ("T02","SCLC: 亜急性~慢性発症。数週~数ヶ月で進行"),
]

for to_id, reason in d402_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# M:F≈1.5:1, 60-70歳ピーク, 喫煙95%
s3['root_priors']['D402'] = {
    "parents":["R02","R01"],
    "description":"SCLC。M:F≈1.5:1。60-70歳ピーク。喫煙強く関連",
    "cpt":{
        "male|18_39":0.0001,"male|40_64":0.002,"male|65_plus":0.003,
        "female|18_39":0.00005,"female|40_64":0.001,"female|65_plus":0.002
    }
}
s3['full_cpts']['D402'] = {
    "R01":{"description":"SCLC年齢。60-70歳ピーク","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.001,
        "18_39":0.02,"40_64":0.40,"65_plus":0.579}},
    "R02":{"description":"SCLC性別。M:F≈1.5:1","cpt":{"male":0.60,"female":0.40}}
}

d402_cpts = {
    "S01":{"absent":0.25,"present":0.75},              # cough 70-75%
    "S04":{"absent":0.35,"present":0.65},              # dyspnea 40-75%
    "S16":{"absent":0.75,"present":0.25},              # hemoptysis 20-30%
    "S17":{"absent":0.30,"present":0.70},              # weight loss 60-80%
    "S21":{"absent":0.65,"present":0.35},              # chest pain 20-40%
    "S07":{"absent":0.35,"mild":0.35,"severe":0.30},   # fatigue ~60%
    "S55":{"absent":0.90,"present":0.10},              # hoarseness 5-10%
    "S46":{"absent":0.50,"present":0.50},              # anorexia ~50%
    "S25":{"absent":0.92,"present":0.08},              # dysphagia 5-10%
    "L04":{"normal":0.05,"lobar_infiltrate":0.20,"bilateral_infiltrate":0.05,
           "BHL":0.45,"pleural_effusion":0.20,"pneumothorax":0.05},  # central mass→BHL
    "L44":{"normal":0.60,"hyponatremia":0.35,"hyperkalemia":0.02,"other":0.03},  # SIADH 10-45%
    "L16":{"normal":0.55,"elevated":0.45},             # LDH elevated ~44%
    "E13":{"absent":0.25,"present":0.75},              # lymphadenopathy 66%+
    "E46":{"cervical":0.10,"axillary":0.02,"inguinal":0.01,
           "supraclavicular":0.45,"mediastinal":0.40,"generalized":0.02},
    "L63":{"absent":0.30,"lung":0.05,"bone":0.15,"liver":0.10,
           "brain":0.10,"multiple":0.30},              # 60-70% extensive
    "S84":{"dry":0.55,"productive":0.45},              # both patterns
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.90,"37.5_38.0":0.06,
           "38.0_39.0":0.025,"39.0_40.0":0.007,"over_40.0":0.003},  # mostly afebrile
    "T01":{"under_3d":0.02,"3d_to_1w":0.05,"1w_to_3w":0.20,"over_3w":0.73},
    "T02":{"sudden":0.02,"acute":0.08,"subacute":0.40,"chronic":0.50},
}

ok=True
for v,c in d402_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D402'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD402: {len(d402_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
