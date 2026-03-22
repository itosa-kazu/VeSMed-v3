"""D434 裂肛 + D435 痔瘻 + D436 便秘症 + S190 肛門痛 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1: 変数追加
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)
variables = s1['variables']

# S190: 肛門痛
s190 = {
    "id": "S190",
    "name": "anal_pain",
    "name_ja": "肛門痛",
    "category": "symptom",
    "states": ["absent", "present"],
    "note": "排便時/排便後の肛門痛。裂肛(90%)、肛門周囲膿瘍、痔瘻に特徴的"
}
# Insert after S189
s189_idx = next(i for i, v in enumerate(variables) if v['id'] == 'S189')
variables.insert(s189_idx + 1, s190)

# D434: 裂肛
d434 = {
    "id": "D434",
    "name": "anal_fissure",
    "name_ja": "裂肛",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "mild",
    "note": "排便時の激痛(90%)+鮮血(71%)。硬便/便秘が原因。後方正中が90%。男女同等。20-40歳に多い"
}

# D435: 痔瘻
d435 = {
    "id": "D435",
    "name": "anal_fistula",
    "name_ja": "痔瘻",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "moderate",
    "note": "肛門周囲膿瘍の後遺。持続性排膿+肛門痛。M:F≈2:1。30-50歳に多い。瘻孔触知"
}

# D436: 便秘症(機能性)
d436 = {
    "id": "D436",
    "name": "functional_constipation",
    "name_ja": "便秘症(機能性)",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "mild",
    "note": "Rome IV: 排便困難/硬便/排便回数減少が3ヶ月以上。有病率10-15%。女性2-3倍。高齢で増加"
}

# Insert diseases after D433
d433_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D433')
for i, d in enumerate([d434, d435, d436]):
    variables.insert(d433_idx + 1 + i, d)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
print("Step 1: S190 + D434/D435/D436 added")

# ============================================================
# Step 2: 辺追加
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)
edges = s2['edges']

# === D434 裂肛 ===
d434_edges = [
    {"from": "D434", "to": "S190", "from_name": "裂肛", "to_name": "anal_pain",
     "reason": "裂肛: 排便時肛門痛90.8%(PMC3048443, 876例review)", "onset_day_range": None},
    {"from": "D434", "to": "S26", "from_name": "裂肛", "to_name": "bloody_stool",
     "reason": "裂肛: 鮮血71.4%(PMC3048443, 紙付着/便に線状)", "onset_day_range": None},
    {"from": "D434", "to": "S72", "from_name": "裂肛", "to_name": "constipation",
     "reason": "裂肛: 便秘が主因(硬便による裂傷, StatPearls)", "onset_day_range": None},
    {"from": "D434", "to": "E91", "from_name": "裂肛", "to_name": "perianal_finding",
     "reason": "裂肛: 視診でfissure確認(後方正中90%, StatPearls)", "onset_day_range": None},
    {"from": "D434", "to": "E82", "from_name": "裂肛", "to_name": "rectal_exam",
     "reason": "裂肛: 直腸診でfissure触知(StatPearls)", "onset_day_range": None},
    {"from": "D434", "to": "E01", "from_name": "裂肛", "to_name": "temperature",
     "reason": "裂肛: 発熱なし(局所病変)", "onset_day_range": None},
    {"from": "D434", "to": "T02", "from_name": "裂肛", "to_name": "onset_speed",
     "reason": "裂肛: 急性(排便時に発症)〜慢性(再発性, StatPearls)", "onset_day_range": None},
    {"from": "D434", "to": "T01", "from_name": "裂肛", "to_name": "symptom_duration",
     "reason": "裂肛: 急性<6週、慢性>6週(StatPearls)", "onset_day_range": None},
    {"from": "D434", "to": "L01", "from_name": "裂肛", "to_name": "WBC",
     "reason": "裂肛: WBC正常(局所病変、感染なし)", "onset_day_range": None},
    {"from": "D434", "to": "L02", "from_name": "裂肛", "to_name": "CRP",
     "reason": "裂肛: CRP正常(局所病変)", "onset_day_range": None},
]

# === D435 痔瘻 ===
d435_edges = [
    {"from": "D435", "to": "S190", "from_name": "痔瘻", "to_name": "anal_pain",
     "reason": "痔瘻: 肛門痛(持続性、膿瘍期は激烈, StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "E91", "from_name": "痔瘻", "to_name": "perianal_finding",
     "reason": "痔瘻: 肛門周囲に外瘻孔(排膿, Cleveland Clinic)", "onset_day_range": None},
    {"from": "D435", "to": "E01", "from_name": "痔瘻", "to_name": "temperature",
     "reason": "痔瘻: 膿瘍合併時に発熱21%(StatPearls perianal abscess)", "onset_day_range": None},
    {"from": "D435", "to": "S26", "from_name": "痔瘻", "to_name": "bloody_stool",
     "reason": "痔瘻: 膿性/血性排膿25%(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "E82", "from_name": "痔瘻", "to_name": "rectal_exam",
     "reason": "痔瘻: 直腸診で瘻管触知(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "T02", "from_name": "痔瘻", "to_name": "onset_speed",
     "reason": "痔瘻: 膿瘍後の亜急性〜慢性経過(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "T01", "from_name": "痔瘻", "to_name": "symptom_duration",
     "reason": "痔瘻: 週〜月単位の慢性経過(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "L01", "from_name": "痔瘻", "to_name": "WBC",
     "reason": "痔瘻: 膿瘍合併時にWBC上昇、慢性期は正常(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "L02", "from_name": "痔瘻", "to_name": "CRP",
     "reason": "痔瘻: 膿瘍合併時にCRP上昇(StatPearls)", "onset_day_range": None},
    {"from": "D435", "to": "S09", "from_name": "痔瘻", "to_name": "rigors",
     "reason": "痔瘻: 膿瘍合併時に悪寒21%(StatPearls perianal abscess)", "onset_day_range": None},
]

# === D436 便秘症 ===
d436_edges = [
    {"from": "D436", "to": "S72", "from_name": "便秘症(機能性)", "to_name": "constipation",
     "reason": "便秘症: 便秘は定義症状100%(Rome IV criteria)", "onset_day_range": None},
    {"from": "D436", "to": "E44", "from_name": "便秘症(機能性)", "to_name": "abdominal_distention",
     "reason": "便秘症: 腹部膨満50-60%(Rome IV supportive, PMC6326211)", "onset_day_range": None},
    {"from": "D436", "to": "S12", "from_name": "便秘症(機能性)", "to_name": "abdominal_pain",
     "reason": "便秘症: 腹痛(mild)30-40%(Rome IV 'mild pain may be present')", "onset_day_range": None},
    {"from": "D436", "to": "S13", "from_name": "便秘症(機能性)", "to_name": "nausea",
     "reason": "便秘症: 悪心15-20%(重度便秘時)", "onset_day_range": None},
    {"from": "D436", "to": "T01", "from_name": "便秘症(機能性)", "to_name": "symptom_duration",
     "reason": "便秘症: Rome IV 3ヶ月以上、慢性(Rome IV criteria)", "onset_day_range": None},
    {"from": "D436", "to": "T02", "from_name": "便秘症(機能性)", "to_name": "onset_speed",
     "reason": "便秘症: 慢性(Rome IV 6ヶ月以上の経過)", "onset_day_range": None},
    {"from": "D436", "to": "E01", "from_name": "便秘症(機能性)", "to_name": "temperature",
     "reason": "便秘症: 発熱なし(機能性、器質的疾患除外)", "onset_day_range": None},
    {"from": "D436", "to": "L01", "from_name": "便秘症(機能性)", "to_name": "WBC",
     "reason": "便秘症: WBC正常(機能性)", "onset_day_range": None},
    {"from": "D436", "to": "L02", "from_name": "便秘症(機能性)", "to_name": "CRP",
     "reason": "便秘症: CRP正常(機能性)", "onset_day_range": None},
    {"from": "D436", "to": "S89", "from_name": "便秘症(機能性)", "to_name": "abdominal_pain_region",
     "reason": "便秘症: 左下腹部/びまん性腹痛(S状結腸停滞)", "onset_day_range": None},
]

# Also add D39(肛門周囲膿瘍) -> S190 edge
d39_s190 = {"from": "D39", "to": "S190", "from_name": "肛門周囲膿瘍", "to_name": "anal_pain",
     "reason": "肛門周囲膿瘍: 肛門痛が主症状(StatPearls 'anal pain, dull/sharp/aching/throbbing')", "onset_day_range": None}

edges.extend(d434_edges)
edges.extend(d435_edges)
edges.extend(d436_edges)
edges.append(d39_s190)
s2['total_edges'] = len(edges)

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
print(f"Step 2: {len(d434_edges)+len(d435_edges)+len(d436_edges)+1} edges added, total {len(edges)}")

# ============================================================
# Step 3: CPT追加
# ============================================================
with open('step3_fever_cpts_v2.json', 'r', encoding='utf-8') as f:
    s3 = json.load(f)
cpts = s3['full_cpts']
nop = s3['noisy_or_params']

# === D434 裂肛 CPT ===
cpts['D434'] = {
    "parents": [],
    "description": "裂肛。便秘/硬便が主因。有病率~1%",
    "cpt": {"no": 0.99, "yes": 0.01},
    "R01": {"0_1": 0.001, "1_5": 0.002, "6_12": 0.003, "13_17": 0.005,
            "18_39": 0.008, "40_64": 0.006, "65_plus": 0.004},
    "R02": {"male": 0.5, "female": 0.5}
}

# === D435 痔瘻 CPT ===
cpts['D435'] = {
    "parents": [],
    "description": "痔瘻。肛門周囲膿瘍の後遺。M:F≈2:1",
    "cpt": {"no": 0.995, "yes": 0.005},
    "R01": {"0_1": 0.0, "1_5": 0.001, "6_12": 0.001, "13_17": 0.002,
            "18_39": 0.005, "40_64": 0.006, "65_plus": 0.003},
    "R02": {"male": 0.67, "female": 0.33}
}

# === D436 便秘症 CPT ===
cpts['D436'] = {
    "parents": [],
    "description": "機能性便秘。有病率10-15%。女性2-3倍",
    "cpt": {"no": 0.97, "yes": 0.03},
    "R01": {"0_1": 0.001, "1_5": 0.002, "6_12": 0.003, "13_17": 0.005,
            "18_39": 0.006, "40_64": 0.007, "65_plus": 0.01},
    "R02": {"male": 0.33, "female": 0.67}
}

# === S190 noisy_or (肛門痛) ===
nop['S190'] = {
    "description": "肛門痛。3親",
    "states": ["absent", "present"],
    "leak": {"absent": 0.97, "present": 0.03},
    "parent_effects": {
        "D434": {"absent": 0.09, "present": 0.91},   # 裂肛 90.8%
        "D435": {"absent": 0.3, "present": 0.7},      # 痔瘻 70%
        "D39": {"absent": 0.1, "present": 0.9}        # 肛門周囲膿瘍 90%
    }
}

# === E91 noisy_or (肛門周囲所見) ===
nop['E91'] = {
    "description": "肛門周囲所見。3親",
    "states": ["normal", "fissure", "fistula", "abscess", "hemorrhoid", "skin_tag"],
    "leak": {"normal": 0.7, "fissure": 0.05, "fistula": 0.02, "abscess": 0.03, "hemorrhoid": 0.15, "skin_tag": 0.05},
    "parent_effects": {
        "D434": {"normal": 0.05, "fissure": 0.85, "fistula": 0.01, "abscess": 0.01, "hemorrhoid": 0.03, "skin_tag": 0.05},
        "D435": {"normal": 0.05, "fissure": 0.02, "fistula": 0.8, "abscess": 0.1, "hemorrhoid": 0.02, "skin_tag": 0.01},
        "D39": {"normal": 0.02, "fissure": 0.01, "fistula": 0.05, "abscess": 0.85, "hemorrhoid": 0.02, "skin_tag": 0.05}
    }
}

# === E82 noisy_or (直腸診) ===
nop['E82'] = {
    "description": "直腸診所見。3親",
    "states": ["normal", "mass", "blood", "fissure", "prostate_enlargement"],
    "leak": {"normal": 0.7, "mass": 0.05, "blood": 0.1, "fissure": 0.05, "prostate_enlargement": 0.1},
    "parent_effects": {
        "D434": {"normal": 0.1, "mass": 0.01, "blood": 0.2, "fissure": 0.68, "prostate_enlargement": 0.01},
        "D435": {"normal": 0.2, "mass": 0.1, "blood": 0.3, "fissure": 0.05, "prostate_enlargement": 0.35}
    }
}

# D434 -> child CPTs
nop['S26']['parent_effects']['D434'] = 0.71  # bloody stool 71.4%
nop['S72']['parent_effects']['D434'] = 0.7   # constipation as cause
nop['E01']['parent_effects']['D434'] = {
    "under_37.5": 0.95, "37.5_38.0": 0.04, "38.0_39.0": 0.008,
    "39.0_40.0": 0.001, "over_40.0": 0.0005, "hypothermia_under_35": 0.0005}
nop['T02']['parent_effects']['D434'] = {
    "sudden": 0.15, "acute": 0.4, "subacute": 0.25, "chronic": 0.2}
nop['T01']['parent_effects']['D434'] = {
    "under_3d": 0.25, "3d_to_1w": 0.25, "1w_to_3w": 0.2, "over_3w": 0.3}
nop['L01']['parent_effects']['D434'] = {
    "low_under_4000": 0.02, "normal_4000_10000": 0.92, "high_10000_20000": 0.05, "very_high_over_20000": 0.01}
nop['L02']['parent_effects']['D434'] = {
    "normal_under_0.3": 0.9, "mild_0.3_3": 0.08, "moderate_3_10": 0.015, "high_over_10": 0.005}

# D435 -> child CPTs
nop['S26']['parent_effects']['D435'] = 0.25  # bloody discharge 25%
nop['E01']['parent_effects']['D435'] = {
    "under_37.5": 0.65, "37.5_38.0": 0.15, "38.0_39.0": 0.12,
    "39.0_40.0": 0.06, "over_40.0": 0.015, "hypothermia_under_35": 0.005}
nop['T02']['parent_effects']['D435'] = {
    "sudden": 0.05, "acute": 0.2, "subacute": 0.4, "chronic": 0.35}
nop['T01']['parent_effects']['D435'] = {
    "under_3d": 0.1, "3d_to_1w": 0.2, "1w_to_3w": 0.35, "over_3w": 0.35}
nop['L01']['parent_effects']['D435'] = {
    "low_under_4000": 0.02, "normal_4000_10000": 0.6, "high_10000_20000": 0.3, "very_high_over_20000": 0.08}
nop['L02']['parent_effects']['D435'] = {
    "normal_under_0.3": 0.35, "mild_0.3_3": 0.3, "moderate_3_10": 0.25, "high_over_10": 0.1}
# S09 rigors 21%
s09_nop = nop.get('S09', {})
if s09_nop and 'parent_effects' in s09_nop:
    s09_nop['parent_effects']['D435'] = 0.21

# D436 -> child CPTs
nop['S72']['parent_effects']['D436'] = 0.95  # constipation 100% by definition
nop['S12']['parent_effects']['D436'] = 0.35  # mild abdominal pain
nop['S13']['parent_effects']['D436'] = 0.18  # nausea
nop['E01']['parent_effects']['D436'] = {
    "under_37.5": 0.96, "37.5_38.0": 0.03, "38.0_39.0": 0.008,
    "39.0_40.0": 0.001, "over_40.0": 0.0005, "hypothermia_under_35": 0.0005}
nop['T02']['parent_effects']['D436'] = {
    "sudden": 0.01, "acute": 0.04, "subacute": 0.15, "chronic": 0.8}
nop['T01']['parent_effects']['D436'] = {
    "under_3d": 0.01, "3d_to_1w": 0.02, "1w_to_3w": 0.07, "over_3w": 0.9}
nop['L01']['parent_effects']['D436'] = {
    "low_under_4000": 0.03, "normal_4000_10000": 0.92, "high_10000_20000": 0.04, "very_high_over_20000": 0.01}
nop['L02']['parent_effects']['D436'] = {
    "normal_under_0.3": 0.9, "mild_0.3_3": 0.08, "moderate_3_10": 0.015, "high_over_10": 0.005}
nop['S89']['parent_effects']['D436'] = {
    "epigastric": 0.1, "RUQ": 0.05, "RLQ": 0.1, "LLQ": 0.4,
    "suprapubic": 0.1, "diffuse": 0.25}
if 'E44' in nop and 'parent_effects' in nop['E44']:
    nop['E44']['parent_effects']['D436'] = {"absent": 0.4, "mild": 0.45, "severe": 0.15}

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D434/D435/D436 CPTs added")
print("Done!")
