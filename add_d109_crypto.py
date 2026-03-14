#!/usr/bin/env python3
"""Add D109 Cryptococcosis (クリプトコッカス症)."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# step1
s1["variables"].append({
    "id": "D109",
    "name": "cryptococcosis",
    "name_ja": "クリプトコッカス症（髄膜炎/肺）",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "免疫不全(HIV CD4<100,臓器移植,ステロイド)で好発。髄膜炎型(70-80%):頭痛+発熱+意識障害。肺型:咳嗽+胸部異常影。墨汁染色/CrAg陽性で確定"
})
print("step1: Added D109 cryptococcosis")

# step2: edges
# クリプトコッカス症の臨床所見:
# 髄膜炎型(最多): 頭痛(80-90%), 発熱(60-80%), 意識障害(30-50%),
#   項部硬直(30-50%, HIV患者では少ない), 嘔気嘔吐(40-60%),
#   視力障害/乳頭浮腫(20-30%)
# 肺型: 咳嗽(30-50%), 胸部X線異常(結節影/浸潤影)
# 全身: 倦怠感, 体重減少, WBC正常~低下, CRP軽度~中等度
# リスク: HIV/免疫不全(R25)
# 検査: 髄液検査(L45), 墨汁染色/CrAg
# T01: 亜急性~慢性(数日~数週)
edges = [
    ("E01", "クリプト: 発熱(60-80%), 通常中等度"),
    ("S05", "クリプト髄膜炎: 頭痛(80-90%, 最多の症状)"),
    ("E16", "クリプト髄膜炎: 意識障害(30-50%)"),
    ("E06", "クリプト髄膜炎: 項部硬直(30-50%, HIV患者では少ない)"),
    ("S13", "クリプト髄膜炎: 嘔気嘔吐(40-60%)"),
    ("S01", "クリプト肺型: 咳嗽(30-50%)"),
    ("L04", "クリプト肺型: 胸部X線異常(結節影/浸潤影30-50%)"),
    ("S07", "クリプト: 倦怠感(70-80%)"),
    ("S17", "クリプト: 体重減少(30-50%)"),
    ("L01", "クリプト: WBC正常~低下(免疫不全背景)"),
    ("L02", "クリプト: CRP軽度~中等度上昇"),
    ("L45", "クリプト髄膜炎: 髄液異常(リンパ球優位, 蛋白↑, 糖↓)"),
    ("T01", "クリプト: 亜急性~慢性経過(数日~数週)"),
    ("T02", "クリプト: 緩徐発症"),
    ("L11", "クリプト: 肝酵素軽度上昇(播種性で20-30%)"),
    ("L28", "クリプト: ESR上昇(50-70%)"),
]
for to_id, reason in edges:
    s2["edges"].append({
        "from": "D109", "to": to_id,
        "from_name": "cryptococcosis", "to_name": to_id,
        "reason": reason
    })
print(f"step2: Added {len(edges)} edges")

# step3: CPTs
n = s3["noisy_or_params"]

# E01: 中等度発熱
n["E01"]["parent_effects"]["D109"] = {
    "under_37.5": 0.20, "37.5_38.0": 0.25, "38.0_39.0": 0.35,
    "39.0_40.0": 0.15, "over_40.0": 0.05
}
# S05: 頭痛(最多症状)
n["S05"]["parent_effects"]["D109"] = {"absent": 0.10, "mild": 0.25, "severe": 0.65}
# E16: 意識障害
n["E16"]["parent_effects"]["D109"] = {
    "alert": 0.50, "confused": 0.25, "obtunded": 0.20, "coma": 0.05
}
# E06: 項部硬直
n["E06"]["parent_effects"]["D109"] = {"absent": 0.55, "present": 0.45}
# S13: 嘔気嘔吐
n["S13"]["parent_effects"]["D109"] = {"absent": 0.45, "present": 0.55}
# S01: 咳嗽(肺型)
n["S01"]["parent_effects"]["D109"] = {"absent": 0.55, "dry": 0.30, "productive": 0.15}
# L04: 胸部X線
n["L04"]["parent_effects"]["D109"] = {
    "normal": 0.50, "lobar_infiltrate": 0.10, "bilateral_infiltrate": 0.15,
    "BHL": 0.05, "pleural_effusion": 0.05, "GGO": 0.10, "cavity": 0.05
}
# S07: 倦怠感
n["S07"]["parent_effects"]["D109"] = {"absent": 0.20, "mild": 0.35, "severe": 0.45}
# S17: 体重減少
n["S17"]["parent_effects"]["D109"] = {"absent": 0.55, "present": 0.45}
# L01: WBC
n["L01"]["parent_effects"]["D109"] = {
    "low_under_4000": 0.30, "normal_4000_10000": 0.50,
    "high_10000_20000": 0.15, "very_high_over_20000": 0.05
}
# L02: CRP
n["L02"]["parent_effects"]["D109"] = {
    "normal_under_0.3": 0.15, "mild_0.3_3": 0.35,
    "moderate_3_10": 0.35, "high_over_10": 0.15
}
# L45: 髄液(結核/真菌パターン: リンパ球優位, 蛋白↑, 糖↓)
n["L45"]["parent_effects"]["D109"] = {
    "not_done": 0.30, "normal": 0.05, "viral_pattern": 0.10,
    "bacterial_pattern": 0.05, "tb_fungal_pattern": 0.50
}
# T01: 亜急性~慢性
n["T01"]["parent_effects"]["D109"] = {
    "under_3d": 0.05, "3d_to_1w": 0.20, "1w_to_3w": 0.45, "over_3w": 0.30
}
# T02: 緩徐
n["T02"]["parent_effects"]["D109"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
# L11: 肝酵素
n["L11"]["parent_effects"]["D109"] = {"normal": 0.65, "mild_elevated": 0.25, "very_high": 0.10}
# L28: ESR
n["L28"]["parent_effects"]["D109"] = {"normal": 0.30, "elevated": 0.50, "very_high_over_100": 0.20}

print(f"step3: Added {len(edges)} CPTs")

# Save
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("All saved. 109 diseases.")
