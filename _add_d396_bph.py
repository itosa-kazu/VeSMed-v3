import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Duplicate check ===
for v in s1['variables']:
    if v['id'].startswith('D') and ('prostat' in v.get('name','').lower() and 'hyper' in v.get('name','').lower()):
        print(f"DUPLICATE FOUND: {v['id']} {v['name']}")
        exit(1)

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D396","name":"benign_prostatic_hyperplasia",
    "name_ja":"前立腺肥大症(BPH)",
    "category":"disease","category_sub":"urology",
    "states":["absent","present"],"severity":"moderate",
    "note":"LUTS: 頻尿/夜間頻尿/尿勢低下/残尿感/尿閉。50歳以上男性50%+。DRE:平滑腫大前立腺。急性尿閉5%。鑑別:前立腺癌/膀胱癌/尿道狭窄/神経因性膀胱/前立腺炎/OAB"
})

# === Step 2: Edges ===
FROM="D396"; FROM_NAME="benign_prostatic_hyperplasia"
d396_edges = [
    ("S11","BPH: 頻尿。蓄尿症状の主要所見。56%のBPH患者で報告(StatPearls NBK558920)"),
    ("S10","BPH: 排尿時痛/不快感。尿路閉塞に伴う(合併UTI時に増強)"),
    ("S98","BPH: 残尿感。排尿症状の主要所見。IPSS評価項目"),
    ("S110","BPH: 尿閉。急性尿閉は重篤合併症(5%/年, StatPearls)。PVR>200mL"),
    ("S33","BPH: 血尿。前立腺血管怒張による。肉眼的血尿はBPH合併症"),
    ("S82","BPH: 尿量変化。慢性尿閉→溢流性尿失禁/乏尿→腎後性AKI"),
    ("L55","BPH: Cr上昇。閉塞性腎症→腎後性AKI(重症合併症)"),
    ("S05","BPH: 頭痛は稀(absent)。鑑別的:頭痛なし"),
    ("E01","BPH: 無熱。発熱→急性前立腺炎/UTI合併を示唆"),
    ("T01","BPH: 慢性(数ヶ月~数年かけて進行)"),
    ("T02","BPH: 慢性発症。緩徐進行性"),
]

for to_id, reason in d396_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Male only, 50歳以上で急増
s3['root_priors']['D396'] = {
    "parents":["R02","R01"],
    "description":"BPH。男性のみ。50歳以上50%+、70歳以上80%+",
    "cpt":{
        "male|18_39":0.001,"male|40_64":0.010,"male|65_plus":0.020,
        "female|18_39":0.0,"female|40_64":0.0,"female|65_plus":0.0
    }
}
s3['full_cpts']['D396'] = {
    "R01":{"description":"BPH年齢。50歳以上で急増","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.0,
        "18_39":0.02,"40_64":0.38,"65_plus":0.60}},
    "R02":{"description":"BPH性別。男性のみ","cpt":{"male":1.0,"female":0.0}}
}

d396_cpts = {
    "S11":{"absent":0.30,"present":0.70},            # urinary frequency 56-70%
    "S10":{"absent":0.75,"present":0.25},             # dysuria 25% (mild, from obstruction)
    "S98":{"absent":0.35,"present":0.65},             # residual feeling common
    "S110":{"absent":0.80,"present":0.20},            # retention 5-20% (acute crisis)
    "S33":{"absent":0.85,"present":0.15},             # hematuria (complication)
    "S82":{"normal":0.80,"oliguria":0.18,"anuria":0.02},  # urine output mostly normal
    "L55":{"normal":0.85,"mild_elevated":0.12,"high_AKI":0.03},  # Cr elevation rare
    "S05":{"absent":0.95,"mild":0.04,"severe":0.01}, # headache not typical
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.05,"3d_to_1w":0.05,"1w_to_3w":0.10,"over_3w":0.80},
    "T02":{"sudden":0.05,"acute":0.10,"subacute":0.15,"chronic":0.70},
}

# Validate CPTs
ok=True
for v,c in d396_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D396'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# === Activate S98 (residual_feeling) NOP ===
if 'S98' not in s3['noisy_or_params']:
    print("Activating S98 (residual_feeling) NOP...")
    s3['noisy_or_params']['S98'] = {
        "leak":{"absent":0.95,"present":0.05},
        "parent_effects":{}
    }
    # Add D396
    s3['noisy_or_params']['S98']['parent_effects']['D396'] = d396_cpts['S98']
    # Add D289 (prostate cancer) — also causes residual feeling
    s2['edges'].append({"from":"D289","to":"S98","from_name":"prostate_cancer",
        "to_name":"urinary_retention_feeling","reason":"前立腺癌: 残尿感。前立腺腫大/浸潤による閉塞症状"})
    s3['noisy_or_params']['S98']['parent_effects']['D289'] = {"absent":0.40,"present":0.60}
    # Add D22 (acute prostatitis)
    s2['edges'].append({"from":"D22","to":"S98","from_name":"acute_prostatitis",
        "to_name":"urinary_retention_feeling","reason":"急性前立腺炎: 残尿感。前立腺腫脹による排尿障害"})
    s3['noisy_or_params']['S98']['parent_effects']['D22'] = {"absent":0.40,"present":0.60}
    # Add D308 (cauda equina) — neurogenic
    s2['edges'].append({"from":"D308","to":"S98","from_name":"cauda_equina",
        "to_name":"urinary_retention_feeling","reason":"馬尾症候群: 残尿感/尿閉。膀胱直腸障害"})
    s3['noisy_or_params']['S98']['parent_effects']['D308'] = {"absent":0.20,"present":0.80}
    s2['total_edges'] = len(s2['edges'])
    print(f"  S98 activated with {len(s3['noisy_or_params']['S98']['parent_effects'])} parents")

# === Activate S110 (urinary_retention) NOP if needed ===
if 'S110' not in s3['noisy_or_params']:
    print("Activating S110 (urinary_retention) NOP...")
    s3['noisy_or_params']['S110'] = {
        "leak":{"absent":0.98,"present":0.02},
        "parent_effects":{}
    }
    # Add existing parents from edges
    s110_parents = set(e['from'] for e in s2['edges'] if e['to']=='S110' and e['from']!='D396')
    for pid in s110_parents:
        if pid == 'D236':  # MS
            s3['noisy_or_params']['S110']['parent_effects']['D236'] = {"absent":0.70,"present":0.30}
        elif pid == 'D200':  # NPH
            s3['noisy_or_params']['S110']['parent_effects']['D200'] = {"absent":0.60,"present":0.40}
        elif pid == 'D307':  # transverse myelitis
            s3['noisy_or_params']['S110']['parent_effects']['D307'] = {"absent":0.30,"present":0.70}
        elif pid == 'D308':  # cauda equina
            s3['noisy_or_params']['S110']['parent_effects']['D308'] = {"absent":0.15,"present":0.85}
        elif pid == 'D289':  # prostate cancer
            s3['noisy_or_params']['S110']['parent_effects']['D289'] = {"absent":0.50,"present":0.50}
        elif pid == 'D301':  # NMOSD
            s3['noisy_or_params']['S110']['parent_effects']['D301'] = {"absent":0.50,"present":0.50}
    # Add D396
    s3['noisy_or_params']['S110']['parent_effects']['D396'] = d396_cpts['S110']
    print(f"  S110 activated with {len(s3['noisy_or_params']['S110']['parent_effects'])} parents")

# === Activate S82 (urine_output) NOP if needed ===
if 'S82' not in s3['noisy_or_params']:
    print("Activating S82 (urine_output) NOP...")
    s3['noisy_or_params']['S82'] = {
        "leak":{"normal":0.95,"oliguria":0.04,"anuria":0.01},
        "parent_effects":{}
    }
    s82_parents = set(e['from'] for e in s2['edges'] if e['to']=='S82' and e['from']!='D396')
    for pid in s82_parents:
        if pid == 'D190':  # SIADH
            s3['noisy_or_params']['S82']['parent_effects']['D190'] = {"normal":0.60,"oliguria":0.35,"anuria":0.05}
        elif pid == 'D211':  # TCA overdose
            s3['noisy_or_params']['S82']['parent_effects']['D211'] = {"normal":0.50,"oliguria":0.40,"anuria":0.10}
        elif pid == 'D191':  # PSGN
            s3['noisy_or_params']['S82']['parent_effects']['D191'] = {"normal":0.40,"oliguria":0.50,"anuria":0.10}
        elif pid == 'D240':  # AIN
            s3['noisy_or_params']['S82']['parent_effects']['D240'] = {"normal":0.50,"oliguria":0.40,"anuria":0.10}
        elif pid == 'D289':  # prostate cancer
            s3['noisy_or_params']['S82']['parent_effects']['D289'] = {"normal":0.70,"oliguria":0.25,"anuria":0.05}
        elif pid == 'D290':  # bladder cancer
            s3['noisy_or_params']['S82']['parent_effects']['D290'] = {"normal":0.75,"oliguria":0.20,"anuria":0.05}
    # Add D396
    s3['noisy_or_params']['S82']['parent_effects']['D396'] = d396_cpts['S82']
    print(f"  S82 activated with {len(s3['noisy_or_params']['S82']['parent_effects'])} parents")

# IDF check
for var_id in ['S98','S110','S82']:
    if var_id in s3['noisy_or_params']:
        n = len(s3['noisy_or_params'][var_id]['parent_effects'])
        print(f"  {var_id}: {n} parents {'OK' if n >= 3 else 'NEED MORE'}")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD396: {len(d396_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
