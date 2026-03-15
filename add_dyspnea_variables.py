#!/usr/bin/env python3
"""Add 6 new variables for dyspnea differential expansion.

L51: BNP/NT-proBNP — 心不全マーカー
S49: 起座呼吸(orthopnea) — 心不全に特異的
E36: 下腿浮腫(lower extremity edema) — 心不全/DVT
E37: 頸静脈怒張(JVD) — 心不全/心タンポナーデ/緊張性気胸
R44: 心疾患既往 — 心不全リスク
R45: 喫煙歴 — COPD/肺癌リスク

step1のみ変更。辺とCPTは各疾患追加時に同時追加(三位一体)。
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)

new_vars = [
    {
        "id": "L51", "name": "BNP_NTproBNP", "name_ja": "BNP/NT-proBNP",
        "category": "lab",
        "states": ["not_done", "normal", "mildly_elevated", "very_high"],
        "note": "心不全マーカー。正常<100pg/mL, 軽度100-400, 著高>400。"
               "心不全で著高、肺疾患では正常~軽度。PE/腎不全でも軽度上昇"
    },
    {
        "id": "S49", "name": "orthopnea", "name_ja": "起座呼吸",
        "category": "symptom",
        "states": ["absent", "present"],
        "note": "臥位で呼吸困難が増悪し、座位で改善。心不全に特異的(感度50-60%, 特異度90%+)"
    },
    {
        "id": "E36", "name": "lower_extremity_edema", "name_ja": "下腿浮腫",
        "category": "sign",
        "states": ["absent", "unilateral", "bilateral"],
        "note": "片側: DVT。両側: 心不全/腎不全/肝硬変。"
    },
    {
        "id": "E37", "name": "JVD", "name_ja": "頸静脈怒張(JVD)",
        "category": "sign",
        "states": ["absent", "present"],
        "note": "右心不全/心タンポナーデ/緊張性気胸で陽性。心不全の感度40-50%"
    },
    {
        "id": "R44", "name": "cardiac_history", "name_ja": "心疾患既往(心不全/虚血性心疾患)",
        "category": "risk_factor",
        "states": ["no", "yes"],
        "note": "心不全/虚血性心疾患の既往。心不全増悪のリスク"
    },
    {
        "id": "R45", "name": "smoking_history", "name_ja": "喫煙歴",
        "category": "risk_factor",
        "states": ["never", "former", "current"],
        "note": "COPD/肺癌/虚血性心疾患のリスク。pack-years不問(あり/なし/現在)"
    },
]

for v in new_vars:
    s1["variables"].append(v)
    print(f"Added {v['id']} {v['name_ja']}")

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "w", encoding="utf-8") as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)

print(f"\nTotal variables: {len(s1['variables'])}")
