#!/usr/bin/env python3
"""Add D124 Cardiac Tamponade (心タンポナーデ).

Clinical basis:
  Beck's triad: 低血圧+JVD+心音減弱(30%のみ揃う)
  呼吸困難(80-90%), 胸痛(30-50%), 起座呼吸(40-50%)
  頻脈(90%+), 低血圧(50-70%), 奇脈(pulsus paradoxus)
  CXR: 心拡大(flask-shaped), 肺野clear
  Echo: 心嚢液貯留+右室虚脱(確定診断)
  原因: 悪性腫瘍(30%), 尿毒症(15%), 感染性心膜炎(15%), 特発性(15%), 外傷
  References: Spodick DH. NEJM 2003;349:684
              Adler Y et al. Eur Heart J 2015 (ESC pericardial guideline)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

s1["variables"].append({
    "id": "D124", "name": "cardiac_tamponade",
    "name_ja": "心タンポナーデ",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "Beck's triad(低血圧+JVD+心音減弱)。心嚢液による心臓圧迫。"
           "原因: 悪性腫瘍/心膜炎/尿毒症/外傷。Echo確定。緊急心嚢穿刺"
})

d_edges = [
    ("S04",  "タンポナーデ: 呼吸困難(80-90%)"),
    ("S49",  "タンポナーデ: 起座呼吸(40-50%)"),
    ("S21",  "タンポナーデ: 胸痛(30-50%, 定常性)"),
    ("E03",  "タンポナーデ: 低血圧(50-70%, Beck's triad)"),
    ("E37",  "タンポナーデ: JVD(70-80%, Beck's triad)"),
    ("E15",  "タンポナーデ: 心音減弱(30-40%, Beck's triad)"),
    ("E02",  "タンポナーデ: 頻脈(90%+, 代償性)"),
    ("E04",  "タンポナーデ: 頻呼吸(60-70%)"),
    ("E05",  "タンポナーデ: 低酸素(中等度で)"),
    ("E01",  "タンポナーデ: 発熱(感染性心膜炎なら30-40%, 他は無熱)"),
    ("L51",  "タンポナーデ: BNP軽度~中等度上昇"),
    ("L04",  "タンポナーデ: CXR — 心拡大(flask-shaped), 肺野clear"),
    ("L01",  "タンポナーデ: WBC — 原因による(感染なら上昇)"),
    ("L02",  "タンポナーデ: CRP — 感染性なら上昇"),
    ("S07",  "タンポナーデ: 倦怠感(50-60%)"),
    ("T01",  "タンポナーデ: 急性~亜急性(原因による)"),
    ("T02",  "タンポナーデ: 急性~亜急性"),
    ("E36",  "タンポナーデ: 下腿浮腫(右心不全で30-40%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D124", "to": to_id, "from_name": "cardiac_tamponade", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S04"]["parent_effects"]["D124"] = {"absent": 0.05, "on_exertion": 0.25, "at_rest": 0.70}
n["S49"]["parent_effects"]["D124"] = {"absent": 0.50, "present": 0.50}
n["S21"]["parent_effects"]["D124"] = {"absent": 0.45, "pleuritic": 0.15, "constant": 0.40}
n["E03"]["parent_effects"]["D124"] = {"normal_over_90": 0.35, "hypotension_under_90": 0.65}
n["E37"]["parent_effects"]["D124"] = {"absent": 0.20, "present": 0.80}
n["E15"]["parent_effects"]["D124"] = {"absent": 0.55, "pre_existing": 0.05, "new": 0.40}
n["E02"]["parent_effects"]["D124"] = {"under_100": 0.08, "100_120": 0.42, "over_120": 0.50}
n["E04"]["parent_effects"]["D124"] = {"normal_under_20": 0.20, "tachypnea_20_30": 0.50, "severe_over_30": 0.30}
n["E05"]["parent_effects"]["D124"] = {"normal_over_96": 0.35, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.25}
n["E01"]["parent_effects"]["D124"] = {"under_37.5": 0.55, "37.5_38.0": 0.20, "38.0_39.0": 0.15, "39.0_40.0": 0.08, "over_40.0": 0.02}
n["L51"]["parent_effects"]["D124"] = {"not_done": 0.25, "normal": 0.15, "mildly_elevated": 0.40, "very_high": 0.20}
# CXR: 心拡大 → normal相当(肺野clear), but enlarged heart silhouette
# L04にはheart-related stateがないので、normalに近い
n["L04"]["parent_effects"]["D124"] = {"normal": 0.30, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.05, "BHL": 0.02, "pleural_effusion": 0.55, "pneumothorax": 0.06}
n["L01"]["parent_effects"]["D124"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.50, "high_10000_20000": 0.35, "very_high_over_20000": 0.10}
n["L02"]["parent_effects"]["D124"] = {"normal_under_0.3": 0.25, "mild_0.3_3": 0.30, "moderate_3_10": 0.25, "high_over_10": 0.20}
n["S07"]["parent_effects"]["D124"] = {"absent": 0.20, "mild": 0.30, "severe": 0.50}
n["T01"]["parent_effects"]["D124"] = {"under_3d": 0.30, "3d_to_1w": 0.35, "1w_to_3w": 0.25, "over_3w": 0.10}
n["T02"]["parent_effects"]["D124"] = {"sudden_hours": 0.40, "gradual_days": 0.60}
n["E36"]["parent_effects"]["D124"] = {"absent": 0.55, "unilateral": 0.05, "bilateral": 0.40}

s3["full_cpts"]["D124"] = {
    "parents": [],
    "description": "心タンポナーデ。悪性腫瘍/心膜炎/尿毒症",
    "cpt": {"": 0.003}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D124: {len(d_edges)} edges. Total: {s2['total_edges']}")
