import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D406","name":"allergic_bronchopulmonary_aspergillosis",
    "name_ja":"アレルギー性気管支肺アスペルギルス症(ABPA)",
    "category":"disease","category_sub":"respiratory",
    "states":["absent","present"],"severity":"moderate",
    "note":"喘息患者の1-2%(専門施設13%)。Aspergillus fumigatusに対する過敏反応。産生性咳嗽(茶色粘液栓)+喘鳴+好酸球増多+IgE>1000+中枢性気管支拡張症。20-40歳。鑑別:好酸球性肺炎/過敏性肺炎/肺結核/EGPA/肺アスペルギルス症(侵襲性)"
})

# === Step 2: Edges ===
FROM="D406"; FROM_NAME="allergic_bronchopulmonary_aspergillosis"
d406_edges = [
    ("S01","ABPA: 咳嗽80-95%(Agarwal 2013)。産生性。茶色/金色粘液栓の喀出30-70%"),
    ("S84","ABPA: 産生性咳嗽が主(PMC4921692)。粘稠な粘液栓"),
    ("S04","ABPA: 呼吸困難60-80%(Agarwal 2013)。気道閉塞+気管支拡張"),
    ("E07","ABPA: 聴診: 喘鳴(wheezes)70-90%。基礎疾患の喘息+気道炎症"),
    ("S34","ABPA: 喀血15-30%。中枢性気管支拡張症から。軽度~中等度"),
    ("L14","ABPA: 好酸球増多80-95%(Agarwal 2013)。>500/μL、しばしば>1000/μL"),
    ("L04","ABPA: CXR: 移動性浸潤影50-80%。上葉優位。中枢性気管支拡張"),
    ("E01","ABPA: 微熱25-50%。急性増悪時。高熱→侵襲性アスペルギルス症を除外"),
    ("S07","ABPA: 倦怠感。慢性炎症+ステロイド依存性喘息"),
    ("S17","ABPA: 体重減少10-25%(進行例)"),
    ("L28","ABPA: ESR上昇40-60%。急性増悪時。非特異的"),
    ("E04","ABPA: 頻呼吸(急性増悪時)。気道閉塞による"),
    ("T01","ABPA: 慢性経過(数週~数ヶ月の増悪を繰り返す)"),
    ("T02","ABPA: 亜急性~慢性。増悪は急性だが全体経過は慢性"),
]

for to_id, reason in d406_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# M:F≈1.2:1, 20-40歳ピーク
s3['root_priors']['D406'] = {
    "parents":["R02","R01"],
    "description":"ABPA。20-40歳。M:F≈1.2:1。喘息患者背景",
    "cpt":{
        "male|18_39":0.0005,"male|40_64":0.0003,"male|65_plus":0.0001,
        "female|18_39":0.0004,"female|40_64":0.0002,"female|65_plus":0.0001
    }
}
s3['full_cpts']['D406'] = {
    "R01":{"description":"ABPA年齢。20-40歳ピーク","cpt":{
        "0_1":0.01,"1_5":0.02,"6_12":0.05,"13_17":0.08,
        "18_39":0.45,"40_64":0.30,"65_plus":0.09}},
    "R02":{"description":"ABPA性別。M:F≈1.2:1","cpt":{"male":0.55,"female":0.45}}
}

d406_cpts = {
    "S01":{"absent":0.10,"present":0.90},               # cough 80-95%
    "S84":{"dry":0.15,"productive":0.85},                # productive dominant
    "S04":{"absent":0.25,"on_exertion":0.45,"at_rest":0.30},  # dyspnea 60-80%
    "E07":{"clear":0.10,"crackles":0.10,"wheezes":0.75,"decreased_absent":0.05},  # wheezes 70-90%
    "S34":{"absent":0.75,"present":0.25},                # hemoptysis 15-30%
    "L14":{"normal":0.10,"left_shift":0.02,"atypical_lymphocytes":0.01,
           "thrombocytopenia":0.01,"eosinophilia":0.85,"lymphocyte_predominant":0.01},
    "L04":{"normal":0.15,"lobar_infiltrate":0.40,"bilateral_infiltrate":0.30,
           "BHL":0.05,"pleural_effusion":0.05,"pneumothorax":0.05},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.60,"37.5_38.0":0.25,
           "38.0_39.0":0.10,"39.0_40.0":0.03,"over_40.0":0.005},
    "S07":{"absent":0.40,"mild":0.40,"severe":0.20},
    "S17":{"absent":0.80,"present":0.20},                # weight loss 10-25%
    "L28":{"normal":0.45,"elevated":0.45,"very_high_over_100":0.10},
    "E04":{"normal_under_20":0.50,"tachypnea_20_30":0.40,"severe_over_30":0.10},
    "T01":{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.25,"over_3w":0.60},
    "T02":{"sudden":0.05,"acute":0.15,"subacute":0.40,"chronic":0.40},
}

ok=True
for v,c in d406_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D406'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD406: {len(d406_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
