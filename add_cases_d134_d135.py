#!/usr/bin/env python3
"""Add pericarditis (D134) x2 + costochondritis (D135) x3 cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D134 Pericarditis x2 (Case 1 PMC10783203 = R196 duplicate, skip)
suite["cases"].append({
    "id": "R250", "source": "CMAJ 2014", "pmcid": "PMC4203603",
    "vignette": "28M 胸骨後部痛(左腕放散, 吸気時増悪, 前傾改善)+発汗. 摩擦音なし. トロポニン正常, CK正常, CRP上昇, ESR上昇. ECG: びまん性ST上昇. Echo: 少量心嚢液, 心収縮正常. ASA 800mg+コルヒチンで1週間で改善",
    "final_diagnosis": "急性特発性心膜炎",
    "expected_id": "D134", "in_scope": True,
    "evidence": {
        "S21": "sharp", "S50": "position", "E01": "under_37.5",
        "L53": "normal", "L02": "moderate_3_10", "L28": "elevated",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "典型的心膜炎. トロポニン正常(心筋炎との鑑別). 前傾改善が鍵"
})

suite["cases"].append({
    "id": "R251", "source": "Eur Heart J Case Rep 2021", "pmcid": "PMC7882268",
    "vignette": "63M 1週間の発熱38.4+乾性咳嗽+倦怠感→胸骨下圧迫痛(中等度~重度). HR 100, BP 96/62, RR 14, SpO2 99%. トロポニン正常, CRP 5mg/dL, ESR 11. ECG: びまん性凹面上ST上昇+PR低下. Echo: 小量心嚢液(7mm). 冠動脈造影正常. SARS-CoV-2陽性",
    "final_diagnosis": "ウイルス性心膜炎(SARS-CoV-2)",
    "expected_id": "D134", "in_scope": True,
    "evidence": {
        "S21": "pressure", "S50": "none", "S01": "dry", "S07": "severe",
        "E02": "100_120", "E01": "38.0_39.0",
        "L53": "normal", "L02": "moderate_3_10",
        "L01": "normal_4000_10000",
        "T01": "3d_to_1w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "COVID心膜炎. 発熱38.4+低血圧96/62. トロポニン正常→心筋炎除外"
})

# D135 Costochondritis x3
suite["cases"].append({
    "id": "R252", "source": "Case Rep Orthop 2019", "pmcid": "PMC6340818",
    "vignette": "41M 健康/喫煙者. 急性の前胸部刺痛(刺すような激痛). T 36.4, BP 134/73, HR 78, SpO2 99%. 第3肋軟骨接合部の腫脹+圧痛(再現性あり). トロポニン正常, WBC正常, ECG正常, CXR正常. CT: 左第2肋軟骨接合部軽度肥大. NSAIDで改善",
    "final_diagnosis": "Tietze症候群(肋軟骨炎)",
    "expected_id": "D135", "in_scope": True,
    "evidence": {
        "S21": "sharp", "S50": "breathing", "E01": "under_37.5",
        "L53": "normal", "L01": "normal_4000_10000",
        "L04": "normal", "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "Tietze症候群. 圧痛再現性+全検査正常が鍵"
})

suite["cases"].append({
    "id": "R253", "source": "Cureus 2023", "pmcid": "PMC10170415",
    "vignette": "38M COVID-19後6週. 左胸骨傍の持続性胸痛(深吸気で増悪). HR 76, BP 130/80, 無熱. 第4胸肋接合部に腫脹+圧痛. hs-トロポニン正常, CRP正常, CBC正常, ECG正常, Echo正常. エコー: 接合部に16mm低エコー域. イブプロフェン600mg TIDで24時間改善",
    "final_diagnosis": "Tietze症候群(COVID後)",
    "expected_id": "D135", "in_scope": True,
    "evidence": {
        "S21": "sharp", "S50": "breathing", "E01": "under_37.5",
        "L53": "normal", "L02": "normal_under_0.3",
        "L04": "normal", "T01": "1w_to_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "COVID後Tietze. 全検査正常. エコーで確認"
})

suite["cases"].append({
    "id": "R254", "source": "J Am Osteopath Assoc 2020", "pmcid": "PMC7645301",
    "vignette": "24M 海兵隊. 8ヶ月の左胸骨痛(水泳/腕立てで増悪)+呼吸困難+左腕痛+指しびれ+めまい. BP 131/64, HR 68, RR 18, SpO2 100%, T 36.7. 胸骨左縁遠位圧痛(再現性あり). トロポニン<0.010, ECG正常, CXR正常, 冠動脈CT正常",
    "final_diagnosis": "肋骨由来非心臓性胸痛",
    "expected_id": "D135", "in_scope": True,
    "evidence": {
        "S21": "sharp", "S50": "exertion", "S04": "on_exertion",
        "S05": "mild", "E01": "under_37.5",
        "L53": "normal", "L04": "normal",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "8ヶ月の慢性胸痛. 労作時増悪→ACS除外必要. 全検査正常"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R250-R254. Total: {len(suite['cases'])}")
