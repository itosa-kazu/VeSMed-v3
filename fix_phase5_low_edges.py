#!/usr/bin/env python3
"""
Phase 5: Add missing edges + CPTs for diseases with <10 edges.
Each disease gets edges to its key distinguishing clinical features.
"""
import json, os
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

def load():
    s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
    s2 = json.load(open(os.path.join(BASE, 'step2_fever_edges_v4.json')))
    s3 = json.load(open(os.path.join(BASE, 'step3_fever_cpts_v2.json')))
    return s1, s2, s3

# ============================================================
# Disease → required edges mapping
# Format: disease_id: [(target_var, cpt_dict, reason), ...]
# cpt_dict: {state: probability} for noisy-OR
# ============================================================

# Helper: common CPT patterns
def binary_high(p=0.8):
    return {'absent': 1-p, 'present': p}
def binary_mod(p=0.5):
    return {'absent': 1-p, 'present': p}
def binary_low(p=0.3):
    return {'absent': 1-p, 'present': p}

DISEASE_EDGES = {
    # ============================================================
    # 6-edge diseases
    # ============================================================
    'D241': [  # 腎血管性高血圧
        ('E33', binary_mod(0.4), '腎動脈狭窄→血管雑音'),
        ('L55', {'normal':0.3,'mild_elevated':0.4,'high_AKI':0.3}, '腎虚血→腎機能障害'),
        ('S35', binary_low(0.3), '高血圧→動悸'),
        ('E36', {'absent':0.6,'present':0.4}, '腎性高血圧→浮腫'),  # binary now
        ('R01', None, '高齢者に多い'),
    ],
    'D244': [  # マロリー・ワイス症候群
        ('S66', binary_high(0.9), '嘔吐後の吐血が典型'),
        ('S67', {'bilious':0.1,'bloody':0.8,'feculent':0.01,'projectile':0.01,'food_content':0.08}, '吐血'),
        ('S26', binary_mod(0.3), '黒色便/血便'),
        ('R16', {'no':0.3,'yes':0.7}, '大量飲酒→嘔吐→裂傷'),
        ('E03', {'normal_over_90':0.7,'hypotension_under_90':0.3}, '大量出血→低血圧'),
    ],
    'D245': [  # 急性胃粘膜病変(AGML)
        ('S66', binary_high(0.7), '嘔吐(吐血)'),
        ('S67', {'bilious':0.1,'bloody':0.7,'feculent':0.01,'projectile':0.01,'food_content':0.18}, '吐血'),
        ('S26', binary_mod(0.5), '上部消化管出血→黒色便'),
        ('R16', {'no':0.5,'yes':0.5}, 'アルコール/NSAIDs/ストレス'),
        ('L93', {'very_low_under_7':0.2,'low_7_10':0.3,'mild_low_10_12':0.3,'normal':0.15,'high':0.05}, '出血→貧血'),
    ],
    'D248': [  # 食道癌
        ('S25', binary_high(0.85), '嚥下困難が主症状'),
        ('S101', {'solids_only':0.6,'solids_and_liquids':0.3,'liquids_worse':0.1}, '固形物嚥下困難から進行'),
        ('S17', binary_high(0.7), '体重減少'),
        ('S55', binary_mod(0.3), '嗄声(反回神経浸潤)'),
        ('S78', binary_mod(0.4), '嚥下痛'),
        ('E13', binary_mod(0.3), '鎖骨上リンパ節腫脹'),
    ],
    'D293': [  # BPPV
        ('S92', {'positional_brief':0.9,'continuous_rotatory':0.05,'episodic_with_hearing':0.02,'non_rotatory_disequilibrium':0.03}, '体位変換で誘発される短時間の回転性めまい'),
        ('E62', {'absent':0.1,'horizontal':0.3,'vertical':0.1,'rotatory':0.5}, '眼振(方向固定性/回旋性)'),
        ('S125', binary_low(0.1), '耳鳴は通常なし(メニエールとの鑑別)'),
        ('S124', binary_low(0.05), '難聴は通常なし'),
        ('E60', {'absent':0.9,'present':0.1}, 'Romberg陰性(末梢前庭)'),
    ],
    'D296': [  # 緊張型頭痛
        ('S69', {'single_acute':0.05,'episodic_recurrent':0.6,'chronic_progressive':0.05,'chronic_stable':0.3}, '反復性/慢性'),
        ('S70', {'photophobia_only':0.05,'phonophobia_only':0.05,'both':0.02,'neither':0.88}, '光音過敏は通常なし'),
        ('S71', binary_low(0.02), '自律神経症状なし'),
        ('S68', {'valsalva_cough':0.02,'exertional':0.02,'positional_upright':0.02,'positional_supine':0.02,'none_identified':0.92}, '特定の増悪因子なし'),
        ('S114', binary_mod(0.4), 'ストレス/不安が関連'),
    ],
    'D297': [  # 三叉神経痛
        ('S69', {'single_acute':0.02,'episodic_recurrent':0.95,'chronic_progressive':0.01,'chronic_stable':0.02}, '反復性発作'),
        ('S20', binary_high(0.9), '顔面痛(三叉神経分布)'),
        ('S68', {'valsalva_cough':0.1,'exertional':0.05,'positional_upright':0.01,'positional_supine':0.01,'none_identified':0.83}, '触覚刺激で誘発'),
        ('R01', None, '50歳以上に多い'),
    ],
    'D339': [  # 網膜剥離
        ('S122', {'absent':0.1,'unilateral':0.85,'bilateral':0.05}, '急性片側視力低下'),
        ('S168', binary_high(0.7), '光視症(網膜牽引)'),
        ('S123', binary_low(0.2), '眼痛は通常軽度'),
        ('R01', None, '中高年/強度近視'),
    ],

    # ============================================================
    # 7-edge diseases
    # ============================================================
    'D226': [  # 真性多血症(PV)
        ('L93', {'very_low_under_7':0.01,'low_7_10':0.01,'mild_low_10_12':0.02,'normal':0.16,'high':0.8}, 'Hb高値'),
        ('L100', {'very_low_under_50k':0.02,'low_50k_150k':0.03,'normal':0.25,'high_over_400k':0.5,'very_high_over_1000k':0.2}, '血小板増加'),
        ('E14', binary_mod(0.4), '脾腫'),
        ('S96', {'absent':0.4,'localized':0.1,'generalized':0.5}, '水浴後掻痒(aquagenic pruritus)'),
        ('S42', binary_low(0.15), '血栓→痙攣'),
        ('E12', {'normal':0.7,'localized_erythema_warmth_swelling':0.05,'petechiae_purpura':0.05,'maculopapular_rash':0.1,'vesicular_dermatomal':0.01,'diffuse_erythroderma':0.08,'purpura':0.01,'vesicle_bulla':0.0,'skin_necrosis':0.0}, '顔面紅潮/赤ら顔'),
    ],
    'D227': [  # 胸腺腫
        ('S48', binary_mod(0.4), '重症筋無力症合併(30-50%)→近位筋力低下'),
        ('S108', {'absent':0.6,'unilateral':0.1,'bilateral':0.3}, '眼瞼下垂(MG)'),
        ('S107', {'absent':0.6,'binocular':0.35,'monocular':0.05}, '複視(MG)'),
        ('S25', binary_mod(0.3), '嚥下困難(MG/腫瘍圧迫)'),
        ('L35', {'normal':0.2,'consolidation':0.05,'GGO':0.05,'cavity':0.0,'halo_sign':0.0,'BHL':0.0,'pleural_effusion':0.1}, '前縦隔腫瘤'),
    ],
    'D235': [  # CLL
        ('E13', binary_high(0.7), 'リンパ節腫脹(全身性)'),
        ('E14', binary_mod(0.5), '脾腫'),
        ('L93', {'very_low_under_7':0.1,'low_7_10':0.2,'mild_low_10_12':0.3,'normal':0.35,'high':0.05}, '貧血'),
        ('S17', binary_mod(0.4), '体重減少(B症状)'),
        ('S16', binary_mod(0.3), '盗汗'),
        ('R01', None, '高齢者に多い(70歳代)'),
    ],
    'D236': [  # 多発性硬化症(MS)
        ('S54', binary_mod(0.4), '視神経炎→視力低下/視野障害'),
        ('S122', {'absent':0.6,'unilateral':0.35,'bilateral':0.05}, '視神経炎(片側)'),
        ('S76', {'stocking_glove':0.1,'ascending':0.1,'dermatomal':0.3,'hemisensory':0.4,'saddle':0.1}, '感覚障害'),
        ('S106', {'absent':0.4,'ataxic':0.35,'shuffling':0.01,'steppage':0.05,'spastic':0.15,'waddling':0.01,'antalgic':0.03}, '歩行障害(小脳性/痙性)'),
        ('E61', binary_mod(0.35), '小脳徴候'),
        ('S110', binary_mod(0.3), '尿閉/排尿障害'),
        ('E62', {'absent':0.4,'horizontal':0.2,'vertical':0.2,'rotatory':0.2}, '眼振'),
        ('L46', {'normal':0.2,'temporal_lobe_lesion':0.1,'diffuse_abnormal':0.6,'other':0.1}, '脱髄斑(periventricular)'),
    ],
    'D237': [  # 腸重積症(成人)
        ('S66', binary_high(0.7), '嘔吐'),
        ('E44', {'absent':0.2,'mild':0.4,'severe':0.4}, '腹部膨満'),
        ('S73', binary_mod(0.5), '排便停止'),
        ('S26', binary_mod(0.4), '粘血便(イチゴゼリー状)'),
        ('E52', {'normal':0.1,'hyperactive_high_pitched':0.7,'hypoactive':0.1,'absent':0.1}, '腸蠕動音亢進'),
    ],
    'D242': [  # 消化性潰瘍(非穿孔性)
        ('S61', {'colicky':0.1,'burning_gnawing':0.6,'sharp_stabbing':0.15,'dull_aching':0.1,'tearing':0.05}, '灼烧感/空腹時痛'),
        ('S62', {'none_identified':0.1,'postprandial':0.2,'relieved_by_food':0.4,'worse_with_movement':0.05,'relieved_by_leaning_forward':0.25}, '食事で改善(DU)/食後増悪(GU)'),
        ('S66', binary_mod(0.4), '嘔吐'),
        ('S26', binary_mod(0.3), '上部消化管出血→黒色便'),
        ('S102', binary_mod(0.4), '胸焼け'),
        ('S89', {'epigastric':0.7,'RUQ':0.15,'RLQ':0.02,'LLQ':0.02,'suprapubic':0.01,'diffuse':0.1}, '心窩部痛'),
    ],
    'D262': [  # 伝染性膿痂疹(とびひ)
        ('E12', {'normal':0.02,'localized_erythema_warmth_swelling':0.15,'petechiae_purpura':0.01,'maculopapular_rash':0.1,'vesicular_dermatomal':0.02,'diffuse_erythroderma':0.0,'purpura':0.0,'vesicle_bulla':0.6,'skin_necrosis':0.1}, '水疱/痂皮'),
        ('S96', {'absent':0.3,'localized':0.6,'generalized':0.1}, '掻痒感'),
        ('E01', {'hypothermia_under_35':0.0,'under_37.5':0.5,'37.5_38.0':0.3,'38.0_39.0':0.15,'39.0_40.0':0.04,'over_40.0':0.01}, '微熱'),
        ('R01', None, '小児に多い'),
        ('E13', binary_low(0.2), '所属リンパ節腫脹'),
    ],
    'D271': [  # 好酸球性食道炎(EoE)
        ('S25', binary_high(0.8), '嚥下困難(主症状)'),
        ('S101', {'solids_only':0.7,'solids_and_liquids':0.2,'liquids_worse':0.1}, '固形物嚥下困難'),
        ('S78', binary_mod(0.5), '嚥下痛'),
        ('S102', binary_mod(0.4), '胸焼け'),
        ('L14', {'normal':0.3,'left_shift':0.01,'atypical_lymphocytes':0.01,'thrombocytopenia':0.01,'eosinophilia':0.65,'lymphocyte_predominant':0.02}, '末梢血好酸球増加'),
    ],
    'D298': [  # Bell麻痺
        ('S109', {'absent':0.02,'upper_and_lower':0.95,'lower_only':0.03}, '末梢性顔面麻痺(上下)'),
        ('S79', binary_mod(0.5), '耳痛(発症前後)'),
        ('S124', binary_low(0.2), '患側の聴覚過敏'),
        ('S19', binary_mod(0.3), '患側の味覚障害(鼓索神経)'),
        ('S31', binary_mod(0.3), '患側の眼乾燥(涙腺障害)'),
    ],
    'D299': [  # Ramsay Hunt症候群
        ('S109', {'absent':0.02,'upper_and_lower':0.9,'lower_only':0.08}, '末梢性顔面麻痺'),
        ('S79', binary_high(0.8), '激しい耳痛'),
        ('E12', {'normal':0.05,'localized_erythema_warmth_swelling':0.05,'petechiae_purpura':0.0,'maculopapular_rash':0.05,'vesicular_dermatomal':0.8,'diffuse_erythroderma':0.0,'purpura':0.0,'vesicle_bulla':0.05,'skin_necrosis':0.0}, '耳介/外耳道の帯状疱疹'),
        ('S124', binary_mod(0.5), '感音性難聴'),
        ('S59', binary_mod(0.5), 'めまい(前庭神経障害)'),
        ('S125', binary_mod(0.4), '耳鳴'),
    ],
    'D302': [  # 進行性核上性麻痺(PSP)
        ('S106', {'absent':0.05,'ataxic':0.1,'shuffling':0.6,'steppage':0.02,'spastic':0.05,'waddling':0.03,'antalgic':0.15}, '易転倒性(後方転倒)'),
        ('E64', binary_high(0.8), '垂直性核上性注視麻痺(下方注視障害)'),
        ('S53', binary_mod(0.4), '構音障害'),
        ('S25', binary_mod(0.3), '嚥下困難'),
        ('S104', binary_mod(0.5), '記憶障害(前頭葉性)'),
        ('S150', binary_high(0.7), '認知機能低下(遂行機能障害)'),
        ('E53', {'normal':0.1,'areflexia':0.05,'hyporeflexia':0.05,'hyperreflexia':0.8}, '深部腱反射亢進'),
    ],
}

def run():
    s1, s2, s3 = load()
    name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}
    
    # Existing edges set
    existing_edges = set()
    for e in s2['edges']:
        existing_edges.add((e['from'], e['to']))
    
    added_edges = 0
    added_cpts = 0
    
    for did, edge_list in DISEASE_EDGES.items():
        disease_name = name_map.get(did, '?')
        
        for target_id, cpt_dict, reason in edge_list:
            if target_id not in name_map:
                print(f'  WARNING: {target_id} not found, skipping')
                continue
            
            # Skip R variables (risk factors have different edge direction)
            if target_id.startswith('R'):
                # For risk factors, edge goes R → D (already handled differently)
                # Skip for now — these need separate handling
                continue
            
            if (did, target_id) in existing_edges:
                continue  # Already exists
            
            # Add edge
            s2['edges'].append({
                'from': did,
                'to': target_id,
                'from_name': name_map.get(did, ''),
                'to_name': name_map.get(target_id, ''),
                'reason': reason,
                'onset_day_range': None
            })
            existing_edges.add((did, target_id))
            added_edges += 1
            
            # Add CPT entry
            if cpt_dict and target_id in s3['noisy_or_params']:
                params = s3['noisy_or_params'][target_id]
                if 'parent_effects' not in params:
                    params['parent_effects'] = {}
                if did not in params['parent_effects']:
                    params['parent_effects'][did] = cpt_dict
                    added_cpts += 1
    
    # Save
    json.dump(s2, open(os.path.join(BASE, 'step2_fever_edges_v4.json'), 'w'), ensure_ascii=False, indent=2)
    json.dump(s3, open(os.path.join(BASE, 'step3_fever_cpts_v2.json'), 'w'), ensure_ascii=False, indent=2)
    
    print(f'Added {added_edges} edges, {added_cpts} CPT entries')
    print(f'Total edges: {len(s2["edges"])}')
    
    # Show updated edge counts
    edge_count = Counter(e['from'] for e in s2['edges'] if e['from'].startswith('D'))
    for did in sorted(DISEASE_EDGES.keys(), key=lambda x: int(x[1:])):
        print(f'  {did}: {name_map.get(did,"")[:30]:30s} {edge_count[did]:3d} edges')

if __name__ == '__main__':
    run()
