import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D400","name":"frontotemporal_dementia",
    "name_ja":"前頭側頭型認知症(FTD/bvFTD)",
    "category":"disease","category_sub":"neurology",
    "states":["absent","present"],"severity":"high",
    "note":"行動変容型(bvFTD)が60%。脱抑制+無関心+共感喪失+常同行動+食行動変化+遂行機能障害。記憶は早期保持(AD鑑別)。45-65歳発症。M:F=1.3:1。30-50%家族性。鑑別:AD/DLB/PSP/CJD/うつ病/統合失調症"
})

# === Step 2: Edges ===
FROM="D400"; FROM_NAME="frontotemporal_dementia"
d400_edges = [
    ("S150","FTD: 遂行機能障害>90%(PMC5619539)。前頭葉萎縮→計画/判断/抽象思考の障害。core diagnostic criterion"),
    ("S104","FTD: 記憶は早期に保持(70-80%, PMC5619539)。AD(近時記憶障害90%)との最大の鑑別点"),
    ("S141","FTD: 慢性進行性(PMC5619539)。数年単位で緩徐進行。CJD(亜急性)との鑑別"),
    ("S115","FTD: 無関心/apathy>80%(PMC5619539, UCSF)。うつ病との誤診多い。しかし悲哀感なし"),
    ("S167","FTD: 脱抑制/焦燥60-70%(PMC5619539)。不適切な社会行動。AD(40%)より高頻度"),
    ("S149","FTD: 妄想10-20%(PMC5619539)。誇大妄想が特徴的。C9orf72変異例で40%"),
    ("S117","FTD: 幻覚<5%(PMC5619539)。稀。DLB(80%)との最大の鑑別点"),
    ("S53","FTD: 言語障害40-60%(PMC5619539)。svPPA(意味性)/nfvPPA(非流暢性)。bvFTDでも後期に"),
    ("S94","FTD: 失語(aphasia)優位(PMC5619539)。意味性失語/非流暢性失語。構音障害はPSP/MND"),
    ("S187","FTD: 言語障害は慢性進行性(PMC5619539)。月~年単位で進行"),
    ("S106","FTD: 歩行障害20-30%(late stage)。FTD-MND overlap/FTD-parkinsonism"),
    ("S25","FTD: 嚥下困難15-20%(late stage)。FTD-MND overlapで顕著"),
    ("S17","FTD: 体重減少30-40%。食行動変化(過食/偏食)+進行期のcachexia"),
    ("E01","FTD: 無熱(定義的)。発熱→感染/自己免疫性脳炎を除外"),
    ("T01","FTD: 慢性(数年単位)。初診時に数年の経過あることが多い"),
    ("T02","FTD: 慢性発症。数ヶ月~年で徐々に進行"),
]

for to_id, reason in d400_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# M:F=1.3:1, 45-65歳ピーク (younger than AD)
# Prevalence: 15-22/100,000 = ~0.0002
s3['root_priors']['D400'] = {
    "parents":["R02","R01"],
    "description":"FTD。M:F=1.3:1。45-65歳ピーク。AD(65+)より若年発症",
    "cpt":{
        "male|18_39":0.0002,"male|40_64":0.001,"male|65_plus":0.0008,
        "female|18_39":0.0001,"female|40_64":0.0007,"female|65_plus":0.0006
    }
}
s3['full_cpts']['D400'] = {
    "R01":{"description":"FTD年齢。45-65歳ピーク(PMC3932112)","cpt":{
        "0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.001,
        "18_39":0.03,"40_64":0.55,"65_plus":0.419}},
    "R02":{"description":"FTD性別。M:F=1.3:1(PMC3932112)","cpt":{"male":0.57,"female":0.43}}
}

d400_cpts = {
    "S150":{"absent":0.08,"present":0.92},              # executive dysfunction >90%
    "S104":{"absent":0.70,"present":0.30},               # memory PRESERVED early (70-80%)
    "S141":{"acute":0.02,"subacute":0.03,"chronic_progressive":0.95},  # chronic progressive
    "S115":{"absent":0.20,"present":0.80},               # apathy >80% (proxy for behavioral change)
    "S167":{"absent":0.35,"present":0.65},               # agitation/disinhibition 60-70%
    "S149":{"absent":0.85,"present":0.15},               # delusion 10-20%
    "S117":{"absent":0.95,"present":0.05},               # hallucination <5% (rare)
    "S53":{"absent":0.45,"present":0.55},                # speech disturbance 40-60%
    "S94":{"dysarthria":0.15,"aphasia":0.85},            # aphasia dominant
    "S187":{"hyperacute":0.01,"subacute":0.04,"chronic_progressive":0.95},  # chronic progressive
    "S106":{"absent":0.70,"present":0.30},               # gait disturbance 20-30% (late)
    "S25":{"absent":0.80,"present":0.20},                # dysphagia 15-20% (late)
    "S17":{"absent":0.65,"present":0.35},                # weight loss 30-40%
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,"38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.01,"3d_to_1w":0.01,"1w_to_3w":0.03,"over_3w":0.95},
    "T02":{"sudden":0.01,"acute":0.02,"subacute":0.07,"chronic":0.90},
}

ok=True
for v,c in d400_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D400'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD400: {len(d400_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
