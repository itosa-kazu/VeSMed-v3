#!/usr/bin/env python3
"""
辺監査 B群分割後: 漏れ辺の追加

臨床的に正当な辺のみ追加。R01/R02 prior漏れは別途対応。
"""
import json

def load_json(p):
    with open(p,'r',encoding='utf-8') as f: return json.load(f)
def save_json(p,d):
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

def add_edge(edges, frm, to, reason, **kw):
    edges.append({"from": frm, "to": to, "reason": reason, **kw})

def add_pe(nop, var_id, disease_id, effects):
    """Add parent_effects for a disease to a variable's noisy_or_params"""
    if var_id in nop:
        nop[var_id].setdefault('parent_effects', {})[disease_id] = effects

def main():
    s2 = load_json('step2_fever_edges_v4.json')
    s3 = load_json('step3_fever_cpts_v2.json')
    edges = s2['edges']
    nop = s3['noisy_or_params']

    added = 0

    # ================================================================
    # D359 GCA: T02漏れ (4案例で漏れ, rank2-43)
    # GCAは亜急性〜慢性発症
    # ================================================================
    add_edge(edges, "D359", "T02", "GCA: 亜急性〜慢性発症(週〜月単位)")
    add_pe(nop, "T02", "D359", {"sudden": 0.005, "acute": 0.02, "subacute": 0.3, "chronic": 0.675})
    added += 1

    # D359 GCA: S08 (関節痛, PMR overlap 40-60%)
    add_edge(edges, "D359", "S08", "GCA: 関節痛(PMR合併40-60%)")
    add_pe(nop, "S08", "D359", {"absent": 0.5, "present": 0.5})
    added += 1

    # ================================================================
    # D354 HL: L01白血球 (HL: 白血球増多/好酸球増多/リンパ球減少)
    # ================================================================
    add_edge(edges, "D354", "L01", "HL: 白血球増多(30-40%)、好酸球増多も")
    add_pe(nop, "L01", "D354", {"low_under_4000": 0.15, "normal_4000_10000": 0.45, "high_10000_20000": 0.3, "very_high_over_20000": 0.1})
    added += 1

    # D354 HL: L15 フェリチン (HL: フェリチン上昇は予後因子)
    add_edge(edges, "D354", "L15", "HL: フェリチン上昇(予後不良因子)")
    add_pe(nop, "L15", "D354", {"normal": 0.3, "mild_elevated": 0.4, "very_high_over_1000": 0.25, "extreme_over_10000": 0.05})
    added += 1

    # D354 HL: E34 肝腫大/脾腫 (HL stage III-IV)
    add_edge(edges, "D354", "E34", "HL: 肝脾腫(stage III-IV, 20-30%)")
    add_pe(nop, "E34", "D354", {"absent": 0.7, "present": 0.3})
    added += 1

    # D354 HL: L02 CRP (HL: B症状に伴うCRP上昇)
    add_edge(edges, "D354", "L02", "HL: CRP上昇(B症状時)")
    add_pe(nop, "L02", "D354", {"normal_under_0.3": 0.25, "mild_0.3_3": 0.3, "moderate_3_10": 0.3, "high_over_10": 0.15})
    added += 1

    # ================================================================
    # D364 iGAS: S13 悪心 (敗血症→GI症状, 2案例で漏れ)
    # ================================================================
    add_edge(edges, "D364", "S13", "iGAS: 敗血症に伴う悪心嘔吐(40-60%)")
    add_pe(nop, "S13", "D364", {"absent": 0.45, "present": 0.55})
    added += 1

    # D364 iGAS: S14 下痢 (敗血症→GI)
    add_edge(edges, "D364", "S14", "iGAS: 敗血症に伴う下痢(20-30%)")
    add_pe(nop, "S14", "D364", {"absent": 0.7, "present": 0.3})
    added += 1

    # ================================================================
    # D352 赤痢: T02発症速度 (3案例で漏れ, rank3-8)
    # 赤痢は急性発症
    # ================================================================
    add_edge(edges, "D352", "T02", "赤痢: 急性発症(1-3日で発症)")
    add_pe(nop, "T02", "D352", {"sudden": 0.1, "acute": 0.6, "subacute": 0.25, "chronic": 0.05})
    added += 1

    # D352 赤痢: E02心拍数 (発熱+脱水→頻脈)
    add_edge(edges, "D352", "E02", "赤痢: 発熱+脱水→頻脈")
    add_pe(nop, "E02", "D352", {"under_100": 0.35, "100_120": 0.45, "over_120": 0.2})
    added += 1

    # D352 赤痢: S46食欲不振
    add_edge(edges, "D352", "S46", "赤痢: 食欲不振(80%+)")
    add_pe(nop, "S46", "D352", {"absent": 0.2, "present": 0.8})
    added += 1

    # D352 赤痢: S06筋肉痛 (全身症状)
    add_edge(edges, "D352", "S06", "赤痢: 筋肉痛(全身症状, 30-50%)")
    add_pe(nop, "S06", "D352", {"absent": 0.55, "present": 0.45})
    added += 1

    # D352 赤痢: S05頭痛
    add_edge(edges, "D352", "S05", "赤痢: 頭痛(全身症状, 30-40%)")
    add_pe(nop, "S05", "D352", {"absent": 0.6, "mild": 0.3, "severe": 0.1})
    added += 1

    # D352 赤痢: E03低血圧 (重症脱水時)
    add_edge(edges, "D352", "E03", "赤痢: 重症脱水→低血圧(10-20%)")
    add_pe(nop, "E03", "D352", {"hypotension_under_90": 0.15, "normal_over_90": 0.85})
    added += 1

    # ================================================================
    # D351 サルモネラ: T02, E02 (漏れ)
    # ================================================================
    add_edge(edges, "D351", "T02", "サルモネラ腸炎: 急性発症")
    add_pe(nop, "T02", "D351", {"sudden": 0.1, "acute": 0.55, "subacute": 0.3, "chronic": 0.05})
    added += 1

    add_edge(edges, "D351", "E02", "サルモネラ腸炎: 発熱+脱水→頻脈")
    add_pe(nop, "E02", "D351", {"under_100": 0.35, "100_120": 0.45, "over_120": 0.2})
    added += 1

    # D351 サルモネラ: S46食欲不振
    add_edge(edges, "D351", "S46", "サルモネラ腸炎: 食欲不振")
    add_pe(nop, "S46", "D351", {"absent": 0.2, "present": 0.8})
    added += 1

    # ================================================================
    # D363 慢性HBV: E16意識レベル (肝性脳症, R787で漏れ)
    # ================================================================
    add_edge(edges, "D363", "E16", "慢性HBV増悪: 肝性脳症→意識障害(劇症化時)")
    add_pe(nop, "E16", "D363", {"normal": 0.7, "confused": 0.2, "obtunded": 0.1})
    added += 1

    # ================================================================
    # D353 UC: T02, S13, E03
    # ================================================================
    add_edge(edges, "D353", "T02", "UC: 亜急性〜慢性発症")
    add_pe(nop, "T02", "D353", {"sudden": 0.01, "acute": 0.05, "subacute": 0.4, "chronic": 0.54})
    added += 1

    add_edge(edges, "D353", "S13", "UC: 悪心(30-40%)")
    add_pe(nop, "S13", "D353", {"absent": 0.6, "present": 0.4})
    added += 1

    add_edge(edges, "D353", "E03", "UC: 重症時低血圧(大量出血/脱水)")
    add_pe(nop, "E03", "D353", {"hypotension_under_90": 0.1, "normal_over_90": 0.9})
    added += 1

    # ================================================================
    # D42 複雑性UTI: E03, E04, E05 (尿路敗血症時)
    # ================================================================
    add_edge(edges, "D42", "E03", "複雑性UTI: 尿路敗血症→低血圧(20-30%)")
    add_pe(nop, "E03", "D42", {"hypotension_under_90": 0.2, "normal_over_90": 0.8})
    added += 1

    add_edge(edges, "D42", "E04", "複雑性UTI: 敗血症→頻呼吸")
    add_pe(nop, "E04", "D42", {"normal_under_20": 0.5, "tachypnea_20_30": 0.35, "severe_over_30": 0.15})
    added += 1

    add_edge(edges, "D42", "E05", "複雑性UTI: 重症敗血症→低酸素")
    add_pe(nop, "E05", "D42", {"normal_over_96": 0.75, "mild_hypoxia_93_96": 0.2, "severe_hypoxia_under_93": 0.05})
    added += 1

    add_edge(edges, "D42", "L14", "複雑性UTI: 白血球左方移動")
    add_pe(nop, "L14", "D42", {"normal": 0.2, "left_shift": 0.55, "atypical_lymphocytes": 0.03, "thrombocytopenia": 0.12, "eosinophilia": 0.05, "lymphocyte_predominant": 0.05})
    added += 1

    # ================================================================
    # D220 EGPA: E13リンパ節, E46部位
    # ================================================================
    add_edge(edges, "D220", "E13", "EGPA: リンパ節腫脹(10-20%)")
    add_pe(nop, "E13", "D220", {"absent": 0.8, "localized": 0.15, "generalized": 0.05})
    added += 1

    add_edge(edges, "D220", "E46", "EGPA: リンパ節部位")
    add_pe(nop, "E46", "D220", {"cervical": 0.4, "axillary": 0.2, "inguinal": 0.1, "generalized": 0.3})
    added += 1

    # ================================================================
    # D354 HL: T02発症速度 (subacute/chronic)
    # Already has T03 but not T02
    # ================================================================
    add_edge(edges, "D354", "T02", "HL: 亜急性〜慢性経過")
    add_pe(nop, "T02", "D354", {"sudden": 0.005, "acute": 0.02, "subacute": 0.375, "chronic": 0.6})
    added += 1

    # ================================================================
    # D354 HL: S09悪寒 (B症状の一部)
    # ================================================================
    add_edge(edges, "D354", "S09", "HL: 悪寒(B症状時, 20-30%)")
    add_pe(nop, "S09", "D354", {"absent": 0.7, "present": 0.3})
    added += 1

    # Save
    s2['edges'] = edges
    s2['total_edges'] = len(edges)
    save_json('step2_fever_edges_v4.json', s2)
    save_json('step3_fever_cpts_v2.json', s3)
    print(f"Added {added} edges")
    print(f"Total edges: {len(edges)}")

if __name__ == '__main__':
    main()
