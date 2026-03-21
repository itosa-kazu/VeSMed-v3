import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

var_name_map = {v['id']: v['name'] for v in s1['variables']}

# === Step 1: Disease definition ===
s1['variables'].append({
    "id":"D404","name":"duchenne_muscular_dystrophy",
    "name_ja":"Duchenne型筋ジストロフィー(DMD)",
    "category":"disease","category_sub":"neurology",
    "states":["absent","present"],"severity":"high",
    "note":"X連鎖劣性。1/5,000男児出生。2-5歳発症。近位筋力低下+Gower徴候+腓腹筋仮性肥大+CK著明高値(10-200xULN)+動揺性歩行。12歳までに歩行不能。心筋症70-100%。鑑別:Becker型/脊髄性筋萎縮症/先天性ミオパチー/多発筋炎"
})

# === Step 2: Edges ===
FROM="D404"; FROM_NAME="duchenne_muscular_dystrophy"
d404_edges = [
    ("S48","DMD: 近位筋力低下~100%(StatPearls NBK482346)。下肢>上肢。2-5歳で顕在化。Gower徴候陽性"),
    ("L17","DMD: CK著明高値(10-200xULN, >10,000IU/L)(StatPearls)。診断時ほぼ全例。年齢とともに低下"),
    ("S106","DMD: 歩行障害~90%。動揺性(Trendelenburg)歩行。尖足歩行。12歳までに歩行不能"),
    ("S137","DMD: 動揺性歩行(waddling gait)~90%。骨盤帯筋力低下→Trendelenburg徴候"),
    ("E53","DMD: 深部腱反射低下(PMC7752564)。筋線維脱落→反射弱化。膝蓋腱反射早期消失"),
    ("E81","DMD: 筋緊張低下(flaccid)。下位運動ニューロン型パターン。乳児期の筋緊張低下"),
    ("S04","DMD: 呼吸困難30-50%(進行期)。呼吸筋力低下→拘束性換気障害。FVC低下"),
    ("S07","DMD: 倦怠感。慢性筋力低下+心筋症+呼吸機能低下"),
    ("E01","DMD: 通常無熱。発熱→肺炎合併(誤嚥性/拘束性)を示唆"),
    ("T01","DMD: 慢性(年単位)。発症から診断まで2-3年のことが多い"),
    ("T02","DMD: 慢性(先天性)。緩徐進行。数年単位で筋力低下が進行"),
]

for to_id, reason in d404_edges:
    s2['edges'].append({"from":FROM,"to":to_id,"from_name":FROM_NAME,
        "to_name":var_name_map.get(to_id,to_id),"reason":reason})
s2['total_edges'] = len(s2['edges'])

# === Step 3: CPTs ===
# Male only (X-linked), 1_5 and 6_12 peak
s3['root_priors']['D404'] = {
    "parents":["R02","R01"],
    "description":"DMD。男児のみ(X連鎖)。2-5歳発症。1/5,000男児出生",
    "cpt":{
        "male|18_39":0.0001,"male|40_64":0.00002,"male|65_plus":0.0,
        "female|18_39":0.0,"female|40_64":0.0,"female|65_plus":0.0
    }
}
s3['full_cpts']['D404'] = {
    "R01":{"description":"DMD年齢。1-12歳が主。成人は稀(Becker型との混同)","cpt":{
        "0_1":0.10,"1_5":0.35,"6_12":0.35,"13_17":0.10,
        "18_39":0.08,"40_64":0.02,"65_plus":0.0}},
    "R02":{"description":"DMD性別。男児のみ(X連鎖劣性)","cpt":{"male":1.0,"female":0.0}}
}

d404_cpts = {
    "S48":{"absent":0.02,"present":0.98},               # proximal weakness ~100%
    "L17":{"normal":0.02,"elevated":0.08,"very_high":0.90},  # CK 10-200x ULN
    "S106":{"absent":0.10,"present":0.90},               # gait disturbance ~90%
    "S137":{"ataxic":0.02,"shuffling":0.02,"steppage":0.05,"spastic":0.01,
            "waddling":0.85,"antalgic":0.05},             # waddling dominant
    "E53":{"normal":0.15,"areflexia":0.25,"hyporeflexia":0.55,"hyperreflexia":0.05},
    "E81":{"normal":0.15,"flaccid":0.75,"spastic":0.05,"rigid":0.02,"paratonia":0.03},
    "S04":{"absent":0.55,"on_exertion":0.30,"at_rest":0.15},  # respiratory 30-50%
    "S07":{"absent":0.25,"mild":0.40,"severe":0.35},
    "E01":{"hypothermia_under_35":0.005,"under_37.5":0.96,"37.5_38.0":0.025,
           "38.0_39.0":0.007,"39.0_40.0":0.002,"over_40.0":0.001},
    "T01":{"under_3d":0.01,"3d_to_1w":0.01,"1w_to_3w":0.03,"over_3w":0.95},
    "T02":{"sudden":0.01,"acute":0.02,"subacute":0.05,"chronic":0.92},
}

ok=True
for v,c in d404_cpts.items():
    s=sum(c.values())
    if abs(s-1)>0.002: print(f"ERR {v} {s}"); ok=False
    if v in s3['noisy_or_params']:
        s3['noisy_or_params'][v]['parent_effects']['D404'] = c
    else:
        print(f"WARN {v} no NOP — need activation")
if ok: print("All CPT sums OK")

# Save
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f: json.dump(s1,f,ensure_ascii=False,indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f: json.dump(s2,f,ensure_ascii=False,indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f: json.dump(s3,f,ensure_ascii=False,indent=2)

print(f"\nD404: {len(d404_edges)} edges. Total: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['id'].startswith('D')])} diseases")
