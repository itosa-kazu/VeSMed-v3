import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D399","name":"pharyngeal_cancer",
    "name_ja":"咽頭癌(中咽頭/下咽頭)",
    "category":"disease","category_sub":"ENT",
    "states":["absent","present"],"severity":"high",
    "note":"嚥下困難/嚥下痛(主訴)+咽頭痛+頸部腫瘤(50%)+嗄声+耳痛(関連痛)+体重減少。M:F=3-5:1、55-65歳。喫煙+飲酒+HPVがリスク。鑑別:喉頭癌/扁桃周囲膿瘍/食道癌/甲状腺癌/リンパ腫/上咽頭癌"
})

# === Step 2: Edges ===
FROM="D399"; FROM_NAME="pharyngeal_cancer"
d399_edges = [
    ("S25","咽頭癌: 嚥下困難60-80%。腫瘍による機械的閉塞。進行に伴い固形→液体"),
    ("S78","咽頭癌: 嚥下痛(odynophagia)50-70%。腫瘍浸潤による粘膜痛"),
    ("S02","咽頭癌: 咽頭痛40-60%。持続性。抗菌薬無効が鑑別の鍵"),
    ("S55","咽頭癌: 嗄声30-40%。下咽頭→反回神経浸潤。喉頭癌との鑑別"),
    ("E13","咽頭癌: 頸部リンパ節腫脹50%。初発症状として頸部腫瘤のみの場合あり"),
    ("E46","咽頭癌: 頸部リンパ節(cervical)。jugulodigastric/jugulo-omohyoid"),
    ("S79","咽頭癌: 耳痛(関連痛)20-30%。Arnold nerve/glossopharyngeal nerve経由"),
    ("S17","咽頭癌: 体重減少30-50%。嚥下困難→栄養障害+悪性cachexia"),
    ("S24","咽頭癌: 開口障害。翼突筋浸潤(進行例)"),
    ("S07","咽頭癌: 倦怠感。悪性腫瘍+栄養障害"),
    ("S101","咽頭癌: 固形物のみの嚥下困難→両方(進行時)。機械的閉塞パターン"),
    ("E01","咽頭癌: 無熱(定義的)。発熱→感染合併/リンパ腫除外"),
    ("T01","咽頭癌: 慢性(数ヶ月~)。初期は非特異的症状で診断遅延"),
    ("T02","咽頭癌: 亜急性~慢性発症。数週~数ヶ月で進行"),
]

for to_id, reason in d399_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# M:F=4:1, 55-65歳ピーク
s3['root_priors']['D399'] = {
    "parents":["R02","R01"],
    "description":"咽頭癌。M:F=4:1。55-65歳ピーク",
    "cpt":{
        "male|18_39":0.0002,"male|40_64":0.002,"male|65_plus":0.003,
        "female|18_39":0.00005,"female|40_64":0.0005,"female|65_plus":0.0008
    }
}
s3['full_cpts']['D399'] = {
    "R01":{"description":"咽頭癌年齢。55-65歳ピーク","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.001,"13_17":0.005,
        "18_39":0.05,"40_64":0.45,"65_plus":0.494}},
    "R02":{"description":"咽頭癌性別。M:F=4:1","cpt":{"male":0.80,"female":0.20}}
}

d399_cpts = {
    "S25":{"absent":0.25,"present":0.75},             # dysphagia 60-80%
    "S78":{"absent":0.35,"present":0.65},              # odynophagia 50-70%
    "S02":{"absent":0.45,"present":0.55},              # sore throat 40-60%
    "S55":{"absent":0.65,"present":0.35},              # hoarseness 30-40%
    "E13":{"absent":0.50,"present":0.50},              # LAD 50%
    "E46":{"cervical":0.90,"axillary":0.02,"inguinal":0.01,"supraclavicular":0.05,"mediastinal":0.01,"generalized":0.01},
    "S79":{"absent":0.75,"present":0.25},              # otalgia (referred) 20-30%
    "S17":{"absent":0.60,"present":0.40},              # weight loss 30-50%
    "S24":{"absent":0.80,"present":0.20},              # trismus (advanced)
    "S07":{"absent":0.40,"mild":0.35,"severe":0.25},   # fatigue
    "S101":{"solids_only":0.60,"solids_and_liquids":0.35,"liquids_worse":0.05},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.05,"over_3w":0.90},
    "T02":{"sudden":0.02,"acute":0.03,"subacute":0.20,"chronic":0.75},
}

ok=True
for v,c in d399_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D399'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate S78 (odynophagia) NOP ===
if 'S78' not in s3['noisy_or_params']:
    print("Activating S78 (odynophagia) NOP...")
    s3['noisy_or_params']['S78'] = {
        "leak":{"absent":0.97,"present":0.03},
        "parent_effects":{}
    }
    # Add existing parents
    s78_parents = set(e['from'] for e in s2['edges'] if e['to']=='S78' and e['from']!='D399')
    for pid in s78_parents:
        if pid == 'D320':  # laryngeal cancer
            s3['noisy_or_params']['S78']['parent_effects']['D320'] = {"absent":0.60,"present":0.40}
        elif pid == 'D33':  # peritonsillar abscess
            s3['noisy_or_params']['S78']['parent_effects']['D33'] = {"absent":0.10,"present":0.90}
        elif pid == 'D04':  # acute pharyngotonsillitis
            s3['noisy_or_params']['S78']['parent_effects']['D04'] = {"absent":0.30,"present":0.70}
        else:
            # Generic: mild odynophagia
            s3['noisy_or_params']['S78']['parent_effects'][pid] = {"absent":0.50,"present":0.50}
    s3['noisy_or_params']['S78']['parent_effects']['D399'] = d399_cpts['S78']
    print(f"  S78 activated with {len(s3['noisy_or_params']['S78']['parent_effects'])} parents")

# === Activate S101 (dysphagia_type) NOP ===
if 'S101' not in s3['noisy_or_params']:
    print("Activating S101 (dysphagia_type) NOP...")
    s3['noisy_or_params']['S101'] = {
        "leak":{"solids_only":0.50,"solids_and_liquids":0.30,"liquids_worse":0.20},
        "parent_effects":{}
    }
    s101_parents = set(e['from'] for e in s2['edges'] if e['to']=='S101' and e['from']!='D399')
    for pid in s101_parents:
        if pid == 'D320':  # laryngeal cancer
            s3['noisy_or_params']['S101']['parent_effects']['D320'] = {"solids_only":0.55,"solids_and_liquids":0.40,"liquids_worse":0.05}
        elif pid == 'D247':  # gastric cancer → esophageal obstruction
            s3['noisy_or_params']['S101']['parent_effects'][pid] = {"solids_only":0.60,"solids_and_liquids":0.35,"liquids_worse":0.05}
        else:
            s3['noisy_or_params']['S101']['parent_effects'][pid] = {"solids_only":0.50,"solids_and_liquids":0.35,"liquids_worse":0.15}
    s3['noisy_or_params']['S101']['parent_effects']['D399'] = d399_cpts['S101']
    print(f"  S101 activated with {len(s3['noisy_or_params']['S101']['parent_effects'])} parents")

# IDF check
for var_id in ['S78','S101']:
    if var_id in s3['noisy_or_params']:
        n = len(s3['noisy_or_params'][var_id]['parent_effects'])
        print(f"  {var_id}: {n} parents {'OK' if n >= 3 else 'NEED MORE'}")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD399: {len(d399_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
