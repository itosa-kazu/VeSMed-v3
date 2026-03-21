import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D397","name":"obstructive_sleep_apnea",
    "name_ja":"閉塞性睡眠時無呼吸症候群(OSAS)",
    "category":"disease","category_sub":"respiratory",
    "states":["absent","present"],"severity":"moderate",
    "note":"いびき95%/日中眠気64-80%/無呼吸目撃56%/朝頭痛/夜間頻尿。M:F=2-3:1、50代ピーク。肥満(BMI>30)が最強リスク。有病率M4%/F2%。鑑別:中枢性無呼吸/ナルコレプシー/甲状腺低下/うつ病/心不全"
})

# === Step 2: Edges ===
# Note: We don't have snoring or daytime sleepiness variables
# Use available variables: S07(fatigue), S05(headache), S116(insomnia), S11(nocturia), S35(palpitation), E05(SpO2), E02(HR)
FROM="D397"; FROM_NAME="obstructive_sleep_apnea"
d397_edges = [
    ("S07","OSAS: 倦怠感/日中眠気~80%(PMC10303057)。夜間断片化睡眠による"),
    ("S05","OSAS: 朝頭痛~30%(AJRCCM 2001)。夜間低酸素+高CO2による"),
    ("S116","OSAS: 不眠~50%。夜間覚醒多数+入眠困難"),
    ("S11","OSAS: 夜間頻尿~50%。ANP分泌増加+覚醒に伴う"),
    ("S35","OSAS: 動悸。夜間不整脈(AF 5x増)。OSA-AF関連"),
    ("E05","OSAS: SpO2低下。夜間反復性低酸素。重症AHI>30で持続性低下"),
    ("E02","OSAS: 頻脈/除脈反復。無呼吸中の自律神経変動"),
    ("E01","OSAS: 無熱(定義的)。発熱は合併感染/別疾患"),
    ("T01","OSAS: 慢性(数ヶ月~数年)。緩徐進行性"),
    ("T02","OSAS: 慢性発症。数ヶ月~数年で進行"),
]

for to_id, reason in d397_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# M:F=2-3:1, 40-65歳ピーク
s3['root_priors']['D397'] = {
    "parents":["R02","R01"],
    "description":"OSAS。M:F=2-3:1。40-65歳。有病率M4%/F2%",
    "cpt":{
        "male|18_39":0.003,"male|40_64":0.008,"male|65_plus":0.006,
        "female|18_39":0.001,"female|40_64":0.004,"female|65_plus":0.003
    }
}
s3['full_cpts']['D397'] = {
    "R01":{"description":"OSAS年齢。40-65歳ピーク","cpt":{
        "0_1":0.001,"1_5":0.005,"6_12":0.01,"13_17":0.02,
        "18_39":0.20,"40_64":0.45,"65_plus":0.314}},
    "R02":{"description":"OSAS性別。M:F=2.5:1","cpt":{"male":0.71,"female":0.29}}
}

d397_cpts = {
    "S07":{"absent":0.15,"mild":0.35,"severe":0.50},   # fatigue/sleepiness 64-80%
    "S05":{"absent":0.70,"mild":0.25,"severe":0.05},    # morning headache ~30%
    "S116":{"absent":0.50,"present":0.50},               # insomnia ~50%
    "S11":{"absent":0.50,"present":0.50},                 # nocturia ~50%
    "S35":{"absent":0.75,"present":0.25},                 # palpitation
    "E05":{"normal_over_96":0.50,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.15},
    "E02":{"under_100":0.70,"100_120":0.25,"over_120":0.05},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.05,"over_3w":0.90},
    "T02":{"sudden":0.02,"acute":0.03,"subacute":0.10,"chronic":0.85},
}

ok=True
for v,c in d397_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D397'] = c
    else:
        print(f"WARN {v} no NOP")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD397: {len(d397_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
