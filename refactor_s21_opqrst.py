#!/usr/bin/env python3
"""Refactor S21 chest pain into OPQRST decomposition.

S21 (quality): absent / burning / sharp / pressure / tearing
S50 (provocation): not_applicable / none / exertion / breathing / position / meals
S51 (radiation): not_applicable / none / left_arm_jaw / back

Old mapping:
  pleuritic = sharp + breathing
  constant  = context-dependent (pressure/burning/tearing + context)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# === Step1: Update S21 states, add S50/S51 ===
for v in s1["variables"]:
    if v["id"] == "S21":
        v["states"] = ["absent", "burning", "sharp", "pressure", "tearing"]
        v["note"] = "胸痛の性質(Quality)。burning=GERD, sharp=胸膜性/心膜炎, pressure=ACS, tearing=解離"
        break

s1["variables"].append({
    "id": "S50", "name": "chest_pain_provocation", "name_ja": "胸痛の誘発因子",
    "category": "symptom",
    "states": ["not_applicable", "none", "exertion", "breathing", "position", "meals"],
    "note": "胸痛のProvocation。exertion=ACS, breathing=胸膜性, position=心膜炎(前傾改善), meals=GERD"
})
s1["variables"].append({
    "id": "S51", "name": "chest_pain_radiation", "name_ja": "胸痛の放散",
    "category": "symptom",
    "states": ["not_applicable", "none", "left_arm_jaw", "back"],
    "note": "胸痛のRadiation。left_arm_jaw=ACS, back=大動脈解離"
})

# === Step2: Add edges for S50/S51 from all chest-pain diseases ===
chest_diseases = list(n["S21"]["parent_effects"].keys())
for did in chest_diseases:
    s2["edges"].append({"from": did, "to": "S50", "from_name": did, "to_name": "S50", "reason": f"{did}→胸痛誘発因子"})
    s2["edges"].append({"from": did, "to": "S51", "from_name": did, "to_name": "S51", "reason": f"{did}→胸痛放散"})

# === Step3: Update S21 CPTs + add S50/S51 CPTs ===
# S21 leak
n["S21"]["leak"] = {"absent": 0.85, "burning": 0.05, "sharp": 0.05, "pressure": 0.03, "tearing": 0.02}

# S50/S51 new entries
n["S50"] = {
    "description": "胸痛の誘発因子(Provocation)",
    "leak": {"not_applicable": 0.85, "none": 0.08, "exertion": 0.03, "breathing": 0.02, "position": 0.01, "meals": 0.01},
    "parent_effects": {}
}
n["S51"] = {
    "description": "胸痛の放散(Radiation)",
    "leak": {"not_applicable": 0.85, "none": 0.10, "left_arm_jaw": 0.03, "back": 0.02},
    "parent_effects": {}
}

# Per-disease CPT mapping
disease_cpts = {
    # (S21 quality, S50 provocation, S51 radiation)
    "D05":  ({"absent":0.55,"burning":0.03,"sharp":0.35,"pressure":0.05,"tearing":0.02},
             {"not_applicable":0.55,"none":0.15,"exertion":0.05,"breathing":0.20,"position":0.03,"meals":0.02},
             {"not_applicable":0.55,"none":0.40,"left_arm_jaw":0.02,"back":0.03}),
    "D36":  ({"absent":0.30,"burning":0.03,"sharp":0.55,"pressure":0.10,"tearing":0.02},
             {"not_applicable":0.30,"none":0.15,"exertion":0.05,"breathing":0.45,"position":0.03,"meals":0.02},
             {"not_applicable":0.30,"none":0.65,"left_arm_jaw":0.02,"back":0.03}),
    "D66":  ({"absent":0.35,"burning":0.05,"sharp":0.45,"pressure":0.10,"tearing":0.05},
             {"not_applicable":0.35,"none":0.40,"exertion":0.05,"breathing":0.15,"position":0.03,"meals":0.02},
             {"not_applicable":0.35,"none":0.60,"left_arm_jaw":0.02,"back":0.03}),
    "D77":  ({"absent":0.30,"burning":0.03,"sharp":0.55,"pressure":0.10,"tearing":0.02},
             {"not_applicable":0.30,"none":0.15,"exertion":0.05,"breathing":0.45,"position":0.03,"meals":0.02},
             {"not_applicable":0.30,"none":0.65,"left_arm_jaw":0.02,"back":0.03}),
    "D03":  ({"absent":0.70,"burning":0.03,"sharp":0.20,"pressure":0.05,"tearing":0.02},
             {"not_applicable":0.70,"none":0.10,"exertion":0.03,"breathing":0.13,"position":0.02,"meals":0.02},
             {"not_applicable":0.70,"none":0.27,"left_arm_jaw":0.01,"back":0.02}),
    "D103": ({"absent":0.70,"burning":0.03,"sharp":0.20,"pressure":0.05,"tearing":0.02},
             {"not_applicable":0.70,"none":0.10,"exertion":0.03,"breathing":0.13,"position":0.02,"meals":0.02},
             {"not_applicable":0.70,"none":0.27,"left_arm_jaw":0.01,"back":0.02}),
    "D73":  ({"absent":0.40,"burning":0.05,"sharp":0.10,"pressure":0.40,"tearing":0.05},
             {"not_applicable":0.40,"none":0.35,"exertion":0.15,"breathing":0.05,"position":0.03,"meals":0.02},
             {"not_applicable":0.40,"none":0.50,"left_arm_jaw":0.05,"back":0.05}),
    "D116": ({"absent":0.05,"burning":0.05,"sharp":0.55,"pressure":0.30,"tearing":0.05},
             {"not_applicable":0.05,"none":0.15,"exertion":0.15,"breathing":0.15,"position":0.45,"meals":0.05},
             {"not_applicable":0.05,"none":0.80,"left_arm_jaw":0.10,"back":0.05}),
    "D123": ({"absent":0.05,"burning":0.02,"sharp":0.80,"pressure":0.10,"tearing":0.03},
             {"not_applicable":0.05,"none":0.10,"exertion":0.05,"breathing":0.75,"position":0.03,"meals":0.02},
             {"not_applicable":0.05,"none":0.85,"left_arm_jaw":0.02,"back":0.08}),
    "D124": ({"absent":0.45,"burning":0.03,"sharp":0.15,"pressure":0.30,"tearing":0.07},
             {"not_applicable":0.45,"none":0.30,"exertion":0.05,"breathing":0.10,"position":0.08,"meals":0.02},
             {"not_applicable":0.45,"none":0.45,"left_arm_jaw":0.05,"back":0.05}),
    "D125": ({"absent":0.55,"burning":0.03,"sharp":0.10,"pressure":0.25,"tearing":0.07},
             {"not_applicable":0.55,"none":0.30,"exertion":0.08,"breathing":0.03,"position":0.02,"meals":0.02},
             {"not_applicable":0.55,"none":0.40,"left_arm_jaw":0.03,"back":0.02}),
    "D127": ({"absent":0.50,"burning":0.03,"sharp":0.35,"pressure":0.10,"tearing":0.02},
             {"not_applicable":0.50,"none":0.15,"exertion":0.05,"breathing":0.25,"position":0.03,"meals":0.02},
             {"not_applicable":0.50,"none":0.45,"left_arm_jaw":0.02,"back":0.03}),
    "D129": ({"absent":0.40,"burning":0.05,"sharp":0.10,"pressure":0.40,"tearing":0.05},
             {"not_applicable":0.40,"none":0.40,"exertion":0.05,"breathing":0.05,"position":0.05,"meals":0.05},
             {"not_applicable":0.40,"none":0.55,"left_arm_jaw":0.03,"back":0.02}),
    "D131": ({"absent":0.05,"burning":0.03,"sharp":0.05,"pressure":0.80,"tearing":0.07},
             {"not_applicable":0.05,"none":0.20,"exertion":0.55,"breathing":0.05,"position":0.03,"meals":0.12},
             {"not_applicable":0.05,"none":0.25,"left_arm_jaw":0.60,"back":0.10}),
    "D132": ({"absent":0.05,"burning":0.03,"sharp":0.07,"pressure":0.15,"tearing":0.70},
             {"not_applicable":0.05,"none":0.80,"exertion":0.03,"breathing":0.05,"position":0.02,"meals":0.05},
             {"not_applicable":0.05,"none":0.20,"left_arm_jaw":0.05,"back":0.70}),
    "D21":  ({"absent":0.55,"burning":0.20,"sharp":0.20,"pressure":0.03,"tearing":0.02},
             {"not_applicable":0.55,"none":0.20,"exertion":0.03,"breathing":0.15,"position":0.05,"meals":0.02},
             {"not_applicable":0.55,"none":0.42,"left_arm_jaw":0.01,"back":0.02}),
    "D133": ({"absent":0.10,"burning":0.75,"sharp":0.05,"pressure":0.08,"tearing":0.02},
             {"not_applicable":0.10,"none":0.20,"exertion":0.05,"breathing":0.05,"position":0.10,"meals":0.50},
             {"not_applicable":0.10,"none":0.85,"left_arm_jaw":0.03,"back":0.02}),
    "D134": ({"absent":0.05,"burning":0.03,"sharp":0.70,"pressure":0.15,"tearing":0.07},
             {"not_applicable":0.05,"none":0.10,"exertion":0.05,"breathing":0.20,"position":0.55,"meals":0.05},
             {"not_applicable":0.05,"none":0.80,"left_arm_jaw":0.05,"back":0.10}),
    "D135": ({"absent":0.03,"burning":0.05,"sharp":0.60,"pressure":0.25,"tearing":0.07},
             {"not_applicable":0.03,"none":0.15,"exertion":0.10,"breathing":0.50,"position":0.05,"meals":0.17},
             {"not_applicable":0.03,"none":0.90,"left_arm_jaw":0.03,"back":0.04}),
}

for did, (s21_cpt, s50_cpt, s51_cpt) in disease_cpts.items():
    n["S21"]["parent_effects"][did] = s21_cpt
    n["S50"]["parent_effects"][did] = s50_cpt
    n["S51"]["parent_effects"][did] = s51_cpt

# === Update test cases ===
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# Mapping: case_id -> (new S21, S50, S51)
case_updates = {
    "R11":  ("sharp", "breathing", None),         # COVID pleuritic
    "R29":  ("sharp", "breathing", None),         # rheumatic fever
    "R50":  ("sharp", "breathing", None),         # sarcoidosis
    "R118": ("pressure", "none", None),           # pheochromocytoma
    "R144": ("sharp", "breathing", None),         # lung abscess
    "R196": ("sharp", "position", None),          # myocarditis (worsened lying, improved sitting)
    "R197": ("sharp", "none", None),              # myocarditis
    "R207": ("sharp", "breathing", None),         # pneumothorax
    "R214": ("sharp", "breathing", None),         # pleural effusion
    "R220": ("sharp", "breathing", None),         # tension pneumothorax
    "R228": ("pressure", "none", None),           # hyperventilation
    "R234": ("pressure", "exertion", None),       # dissection mimicking ACS
    "R235": ("pressure", "none", None),           # dissection (oppressive)
    "R236": ("tearing", "none", "back"),          # Type B dissection
    "R237": ("pressure", "none", "left_arm_jaw"), # STEMI (neck/shoulders)
    "R238": ("pressure", "none", "left_arm_jaw"), # STEMI (jaw/arm)
    "R239": ("pressure", "none", None),           # NSTEMI
    "R244": ("burning", "none", None),            # GERD
    "R245": ("burning", "exertion", None),        # GERD (exercise-triggered)
    "R246": ("burning", "breathing", None),       # GERD (burning + worsened by breathing)
}

for c in suite["cases"]:
    if c["id"] in case_updates:
        new_s21, new_s50, new_s51 = case_updates[c["id"]]
        c["evidence"]["S21"] = new_s21
        if new_s50:
            c["evidence"]["S50"] = new_s50
        if new_s51:
            c["evidence"]["S51"] = new_s51

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"S21 refactored: 5 states (was 3)")
print(f"S50 added: 6 states, {len(chest_diseases)} parents")
print(f"S51 added: 4 states, {len(chest_diseases)} parents")
print(f"Updated {len(case_updates)} test cases")
print(f"Total edges: {s2['total_edges']}")
