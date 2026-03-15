#!/usr/bin/env python3
"""Add D123 Pneumothorax (気胸) + E07/L04 state追加.

E07 肺聴診: +decreased_absent (呼吸音減弱/消失) — 気胸/大量胸水
L04 胸部X線: +pneumothorax (気胸像) — 胸膜線/肺虚脱

Clinical basis:
  突然の胸膜性胸痛+呼吸困難。若年痩身男性(原発性)、COPD(続発性)。
  呼吸音減弱(患側), CXRで気胸確認。
  緊張性気胸: 低血圧+JVD+気管偏位 → 緊急脱気
  References: MacDuff A et al. BTS guideline 2010
"""
import json, os, math
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# === E07: add 'decreased_absent' state ===
for v in s1["variables"]:
    if v["id"] == "E07":
        v["states"].append("decreased_absent")
        print(f"E07 states: {v['states']}")
        break

n = s3["noisy_or_params"]

# Update E07 leak
old_leak = n["E07"]["leak"]
n["E07"]["leak"] = {"clear": 0.88, "crackles": 0.05, "wheezes": 0.04, "decreased_absent": 0.03}

# Update all E07 parent_effects
for d_id, cpt in n["E07"]["parent_effects"].items():
    old_sum = sum(cpt.values())
    # Most diseases: low probability of decreased_absent
    da_prob = 0.03
    if d_id in ["D36"]:  # 膿胸 → 呼吸音減弱 30%
        da_prob = 0.25
    elif d_id in ["D77"]:  # 大量PE → 減弱 10%
        da_prob = 0.08
    scale = (old_sum - da_prob) / old_sum
    for s in list(cpt.keys()):
        cpt[s] *= scale
    cpt["decreased_absent"] = da_prob

print(f"E07: updated {len(n['E07']['parent_effects'])} parent CPTs + leak")

# === L04: add 'pneumothorax' state ===
for v in s1["variables"]:
    if v["id"] == "L04":
        v["states"].append("pneumothorax")
        print(f"L04 states: {v['states']}")
        break

old_leak_l04 = n["L04"]["leak"]
total_l = sum(old_leak_l04.values())
# Redistribute: take from normal
n["L04"]["leak"]["pneumothorax"] = 0.01
n["L04"]["leak"]["normal"] = old_leak_l04["normal"] - 0.01

for d_id, cpt in n["L04"]["parent_effects"].items():
    old_sum = sum(cpt.values())
    pnx_prob = 0.01  # Default: very low
    scale = (old_sum - pnx_prob) / old_sum
    for s in list(cpt.keys()):
        cpt[s] *= scale
    cpt["pneumothorax"] = pnx_prob

print(f"L04: updated {len(n['L04']['parent_effects'])} parent CPTs + leak")

# === D123 Pneumothorax ===
s1["variables"].append({
    "id": "D123", "name": "pneumothorax", "name_ja": "気胸",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の胸膜性胸痛+呼吸困難。若年痩身男性(原発性)/COPD(続発性)。"
           "呼吸音減弱(患側)、CXRで確定。緊張性気胸は緊急脱気"
})

d_edges = [
    ("S21",  "気胸: 胸痛(90%+, 胸膜性/突然発症)"),
    ("S04",  "気胸: 呼吸困難(80-90%)"),
    ("E07",  "気胸: 肺聴診 — 患側呼吸音減弱/消失(80%+)"),
    ("L04",  "気胸: CXR — 気胸像(胸膜線+肺虚脱)"),
    ("E02",  "気胸: 頻脈(50-60%)"),
    ("E04",  "気胸: 頻呼吸(50-60%)"),
    ("E05",  "気胸: 低酸素(中等度以上で)"),
    ("E03",  "気胸: 低血圧(緊張性気胸5-10%)"),
    ("E37",  "気胸: JVD(緊張性気胸で)"),
    ("E01",  "気胸: 通常無熱"),
    ("L01",  "気胸: WBC通常正常"),
    ("L02",  "気胸: CRP通常正常"),
    ("T01",  "気胸: 超急性(数分~数時間)"),
    ("T02",  "気胸: 突然発症"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D123", "to": to_id, "from_name": "pneumothorax", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n["S21"]["parent_effects"]["D123"] = {"absent": 0.05, "pleuritic": 0.80, "constant": 0.15}
n["S04"]["parent_effects"]["D123"] = {"absent": 0.10, "on_exertion": 0.30, "at_rest": 0.60}
n["E07"]["parent_effects"]["D123"] = {"clear": 0.05, "crackles": 0.02, "wheezes": 0.03, "decreased_absent": 0.90}
n["L04"]["parent_effects"]["D123"] = {"normal": 0.05, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.02, "BHL": 0.01, "pleural_effusion": 0.05, "pneumothorax": 0.85}
n["E02"]["parent_effects"]["D123"] = {"under_100": 0.35, "100_120": 0.45, "over_120": 0.20}
n["E04"]["parent_effects"]["D123"] = {"normal_under_20": 0.30, "tachypnea_20_30": 0.50, "severe_over_30": 0.20}
n["E05"]["parent_effects"]["D123"] = {"normal_over_96": 0.40, "mild_hypoxia_93_96": 0.35, "severe_hypoxia_under_93": 0.25}
n["E03"]["parent_effects"]["D123"] = {"normal_over_90": 0.88, "hypotension_under_90": 0.12}
n["E37"]["parent_effects"]["D123"] = {"absent": 0.85, "present": 0.15}
n["E01"]["parent_effects"]["D123"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D123"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.75, "high_10000_20000": 0.18, "very_high_over_20000": 0.04}
n["L02"]["parent_effects"]["D123"] = {"normal_under_0.3": 0.60, "mild_0.3_3": 0.30, "moderate_3_10": 0.08, "high_over_10": 0.02}
n["T01"]["parent_effects"]["D123"] = {"under_3d": 0.80, "3d_to_1w": 0.15, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D123"] = {"sudden_hours": 0.85, "gradual_days": 0.15}

s3["full_cpts"]["D123"] = {
    "parents": ["R01"],
    "description": "気胸。若年男性(原発性)、高齢+COPD(続発性)",
    "cpt": {"18_39": 0.005, "40_64": 0.003, "65_plus": 0.003}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nD123: {len(d_edges)} edges. Total: {s2['total_edges']}")
