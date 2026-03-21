import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D401","name":"preeclampsia_eclampsia",
    "name_ja":"子癇前症/子癇(Preeclampsia/Eclampsia)",
    "category":"disease","category_sub":"obstetrics",
    "states":["absent","present"],"severity":"high",
    "note":"妊娠20週以降の高血圧+蛋白尿(or重症徴候)。頭痛66%+視覚障害25-50%+上腹部痛25%。子癇=痙攣(<3%)。HELLP移行3-20%。有病率4-5%。初産/肥満/35歳以上がリスク。鑑別:HELLP/TTP-HUS/高血圧緊急症/PRES/CVST"
})

# === Step 2: Edges ===
FROM="D401"; FROM_NAME="preeclampsia_eclampsia"
d401_edges = [
    ("E38","PE: 高血圧(≥140/90)は診断基準(ACOG)。重症25%(≥160/110, PMC9723483)"),
    ("L78","PE: 蛋白尿42-58%(PMC9723483)。≥0.3g/24h。2013以降必須ではないが高頻度"),
    ("S05","PE: 頭痛66%(子癇前兆, PMC3119563)。重症型で高頻度。子癇の最多前駆症状"),
    ("S54","PE: 視覚障害25-50%(NBK576389)。暗点/閃光/霧視。後頭葉血管性浮腫"),
    ("E36","PE: 下肢浮腫60%。蛋白尿に伴う低アルブミン→浮腫。非特異的だが急速増悪は警告"),
    ("E68","PE: 顔面浮腫(眼瞼)30%。全身性浮腫の一部。急速な体重増加を伴う"),
    ("S13","PE: 悪心30-40%。肝腫大/子宮内圧上昇。HELLP移行の警告"),
    ("S42","PE: 子癇(痙攣)<3%(PMC3119563)。40%は典型的PE所見なし。MgSO4で予防"),
    ("L11","PE: 肝酵素上昇10-54%(PMC4779350)。重症で高頻度。HELLP移行リスク"),
    ("L14","PE: 血小板減少25-30%(重症)。<100,000は重症基準。HELLP移行のサイン"),
    ("L55","PE: クレアチニン上昇(重症基準: >1.1mg/dL)。腎血管内皮障害"),
    ("L16","PE: LDH上昇45-50%。血管内皮障害+溶血反映。HELLP移行マーカー"),
    ("R15","PE: 妊娠が必須条件(定義的)。妊娠20週以降~産後48時間"),
    ("L56","PE: β-hCG陽性(妊娠中)。妊娠の確認"),
    ("S12","PE: 上腹部痛25-30%(PMC3119563)。肝被膜伸展。HELLP移行の警告"),
    ("S89","PE: 心窩部/右上腹部痛が主(肝腫大)。HELLP同様のパターン"),
    ("S120","PE: 体重増加55-60%。浮腫に伴う急速な体重増加(>2kg/週)"),
    ("S07","PE: 倦怠感。全身性浮腫+貧血+高血圧に伴う"),
    ("E01","PE: 通常無熱。発熱→感染/子宮内膜炎を除外"),
    ("T01","PE: 急性~亜急性(数日~1-2週)。急速進行で緊急分娩要する場合あり"),
    ("T02","PE: 急性~亜急性発症。数日で症状悪化"),
]

for to_id, reason in d401_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Female only, 18-39 peak (young primigravida), 40-64 also at risk
s3['root_priors']['D401'] = {
    "parents":["R02","R01"],
    "description":"子癇前症。女性のみ。妊娠可能年齢。初産/35歳以上リスク",
    "cpt":{
        "male|18_39":0.0,"male|40_64":0.0,"male|65_plus":0.0,
        "female|18_39":0.005,"female|40_64":0.002,"female|65_plus":0.0
    }
}
s3['full_cpts']['D401'] = {
    "R01":{"description":"PE年齢。18-39歳が主(妊娠可能年齢)","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.01,
        "18_39":0.65,"40_64":0.34,"65_plus":0.01}},
    "R02":{"description":"PE性別。女性のみ","cpt":{"male":0.0,"female":1.0}}
}

d401_cpts = {
    "E38":{"normal_under_140":0.10,"elevated_140_180":0.65,"crisis_over_180":0.25},
    "L78":{"normal":0.35,"mild_proteinuria":0.35,"nephrotic_range":0.30},
    "S05":{"absent":0.35,"mild":0.25,"severe":0.40},
    "S54":{"absent":0.60,"present":0.40},
    "E36":{"absent":0.40,"present":0.60},
    "E68":{"absent":0.70,"present":0.30},
    "S13":{"absent":0.65,"present":0.35},
    "S42":{"absent":0.97,"present":0.03},
    "L11":{"normal":0.50,"mild_elevated":0.35,"very_high":0.15},
    "L14":{"normal":0.60,"left_shift":0.05,"atypical_lymphocytes":0.02,
           "thrombocytopenia":0.28,"eosinophilia":0.02,"lymphocyte_predominant":0.03},
    "L55":{"normal":0.70,"mild_elevated":0.25,"high_AKI":0.05},
    "L16":{"normal":0.50,"elevated":0.50},
    "R15":{"no":0.01,"yes":0.99},
    "L56":{"negative":0.01,"positive":0.99},
    "S12":{"absent":0.70,"present":0.30},
    "S89":{"epigastric":0.45,"RUQ":0.40,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.02,"diffuse":0.09},
    "S120":{"absent":0.40,"present":0.60},
    "S07":{"absent":0.45,"mild":0.35,"severe":0.20},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.30,"3d_to_1w":0.40,"1w_to_3w":0.25,"over_3w":0.05},
    "T02":{"sudden":0.10,"acute":0.50,"subacute":0.35,"chronic":0.05},
}

ok=True
for v,c in d401_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D401'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD401: {len(d401_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
