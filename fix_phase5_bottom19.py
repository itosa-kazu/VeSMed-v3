#!/usr/bin/env python3
"""
Phase 5: Add missing edges + CPTs for diseases with <=7 edges (19 diseases)
Each disease gets edges to its key distinguishing features.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
s2 = json.load(open(os.path.join(BASE, 'step2_fever_edges_v4.json')))
s3 = json.load(open(os.path.join(BASE, 'step3_fever_cpts_v2.json')))

name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}
existing_edges = {(e['from'], e['to']) for e in s2['edges']}

added_edges = 0
added_cpts = 0

def add_edge(disease_id, var_id, reason, cpt_values):
    """Add edge + CPT. cpt_values = dict of {state: probability}"""
    global added_edges, added_cpts
    
    if (disease_id, var_id) in existing_edges:
        return  # Skip if already exists
    
    # Add edge
    s2['edges'].append({
        'from': disease_id,
        'to': var_id,
        'from_name': name_map.get(disease_id, ''),
        'to_name': name_map.get(var_id, ''),
        'reason': reason,
        'onset_day_range': None
    })
    existing_edges.add((disease_id, var_id))
    added_edges += 1
    
    # Add CPT (noisy-OR parent_effects)
    if var_id in s3['noisy_or_params']:
        s3['noisy_or_params'][var_id]['parent_effects'][disease_id] = cpt_values
        added_cpts += 1


# ============================================================
# D241 腎血管性高血圧 (6→target 15)
# Key: 治療抵抗性高血圧, 腹部血管雑音, 腎機能低下, 低K血症
# ============================================================
add_edge('D241', 'E33', '腹部血管雑音(腎動脈狭窄)',
    {'absent': 0.55, 'present': 0.45})
add_edge('D241', 'L44', '低K血症(二次性アルドステロン症)',
    {'normal': 0.60, 'hyponatremia': 0.05, 'hyperkalemia': 0.02, 'other': 0.33})
add_edge('D241', 'S35', '動悸(高血圧関連)',
    {'absent': 0.65, 'present': 0.35})
add_edge('D241', 'L78', '蛋白尿(腎障害)',
    {'not_done': 0.05, 'normal': 0.40, 'mild_proteinuria': 0.45, 'nephrotic_range': 0.10})
add_edge('D241', 'S122', '急性視力低下(高血圧性網膜症)',
    {'absent': 0.85, 'unilateral': 0.10, 'bilateral': 0.05})
add_edge('D241', 'R01', '年齢(若年or高齢)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.01,'18_39':0.25,'40_64':0.40,'65_plus':0.34})
add_edge('D241', 'L71', 'BUN上昇(腎機能)',
    {'normal': 0.45, 'elevated': 0.40, 'very_high': 0.15})
add_edge('D241', 'E36', '下腿浮腫(心不全合併)',
    {'absent': 0.70, 'present': 0.30})

# ============================================================
# D244 マロリー・ワイス症候群 (6→target 14)
# Key: 嘔吐後の吐血, アルコール歴, 上腹部痛
# ============================================================
add_edge('D244', 'S66', '嘔吐(先行する嘔吐が特徴)',
    {'absent': 0.10, 'present': 0.90})
add_edge('D244', 'S67', '嘔吐性状(吐血)',
    {'bilious': 0.10, 'bloody': 0.70, 'feculent': 0.01, 'projectile': 0.04, 'food_content': 0.15})
add_edge('D244', 'R16', '大量飲酒(主要リスク)',
    {'no': 0.40, 'yes': 0.60})
add_edge('D244', 'S135', '黒色便(下部消化管出血)',
    {'absent': 0.55, 'present': 0.45})
add_edge('D244', 'L93', 'Hb低下(出血)',
    {'very_low_under_7':0.05,'low_7_10':0.20,'mild_low_10_12':0.35,'normal':0.35,'high':0.05})
add_edge('D244', 'E03', '低血圧(出血性ショック)',
    {'normal_over_90': 0.75, 'hypotension_under_90': 0.25})
add_edge('D244', 'E02', '頻脈(出血)',
    {'under_100': 0.50, '100_120': 0.35, 'over_120': 0.15})
add_edge('D244', 'R01', '年齢',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.02,'18_39':0.30,'40_64':0.45,'65_plus':0.23})

# ============================================================
# D245 急性胃粘膜病変(AGML) (6→target 14)
# Key: ストレス/NSAIDs, 上腹部痛, 吐血, 黒色便
# ============================================================
add_edge('D245', 'S66', '嘔吐/吐血',
    {'absent': 0.30, 'present': 0.70})
add_edge('D245', 'S67', '吐血',
    {'bilious': 0.10, 'bloody': 0.60, 'feculent': 0.01, 'projectile': 0.04, 'food_content': 0.25})
add_edge('D245', 'S135', '黒色便',
    {'absent': 0.45, 'present': 0.55})
add_edge('D245', 'R08', 'NSAIDs/薬剤',
    {'no': 0.40, 'yes': 0.60})
add_edge('D245', 'R21', '最近の手術/ストレス',
    {'no': 0.50, 'yes': 0.50})
add_edge('D245', 'L93', 'Hb低下',
    {'very_low_under_7':0.05,'low_7_10':0.25,'mild_low_10_12':0.35,'normal':0.30,'high':0.05})
add_edge('D245', 'S61', '腹痛性状(灼烧)',
    {'colicky':0.05,'burning_gnawing':0.60,'sharp_stabbing':0.15,'dull_aching':0.15,'tearing':0.05})
add_edge('D245', 'R16', '飲酒',
    {'no': 0.50, 'yes': 0.50})

# ============================================================
# D248 食道癌 (6→target 15)
# Key: 嚥下困難(進行性,固形→液体), 体重減少, 嗄声, 胸痛
# ============================================================
add_edge('D248', 'S25', '嚥下困難(最重要症状)',
    {'absent': 0.10, 'present': 0.90})
add_edge('D248', 'S101', '嚥下困難種類(固形のみ→両方へ進行)',
    {'solids_only': 0.60, 'solids_and_liquids': 0.30, 'liquids_worse': 0.10})
add_edge('D248', 'S17', '体重減少',
    {'absent': 0.15, 'present': 0.85})
add_edge('D248', 'S183', '体重減少速度(急速)',
    {'rapid_weeks': 0.65, 'gradual_months': 0.35})
add_edge('D248', 'S55', '嗄声(反回神経浸潤)',
    {'absent': 0.75, 'present': 0.25})
add_edge('D248', 'S78', '嚥下痛',
    {'absent': 0.40, 'present': 0.60})
add_edge('D248', 'S46', '食欲不振',
    {'absent': 0.25, 'present': 0.75})
add_edge('D248', 'R03', '喫煙',
    {'never': 0.25, 'former': 0.30, 'current': 0.45})
add_edge('D248', 'R16', '飲酒',
    {'no': 0.30, 'yes': 0.70})

# ============================================================
# D293 BPPV (6→target 14)
# Key: 体位変換時の短時間回転性めまい, 聴力正常, 眼振
# ============================================================
add_edge('D293', 'S92', 'めまい性状(体位性短時間)',
    {'positional_brief': 0.90, 'continuous_rotatory': 0.05, 'episodic_with_hearing': 0.02, 'non_rotatory_disequilibrium': 0.03})
add_edge('D293', 'E62', '眼振(回旋性)',
    {'absent': 0.15, 'horizontal': 0.15, 'vertical': 0.05, 'rotatory': 0.65})
add_edge('D293', 'S66', '嘔吐(めまい随伴)',
    {'absent': 0.45, 'present': 0.55})
add_edge('D293', 'S124', '難聴なし(BPPVでは聴力正常)',
    {'absent': 0.95, 'present': 0.05})
add_edge('D293', 'S125', '耳鳴なし',
    {'absent': 0.92, 'present': 0.08})
add_edge('D293', 'R01', '年齢(中高年に多い)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.01,'13_17':0.02,'18_39':0.15,'40_64':0.42,'65_plus':0.40})
add_edge('D293', 'E06', '項部硬直なし',
    {'absent': 0.99, 'present': 0.01})
add_edge('D293', 'E16', '意識正常',
    {'normal': 0.99, 'confused': 0.005, 'obtunded': 0.005})

# ============================================================
# D296 緊張型頭痛 (6→target 14)
# Key: 両側性圧迫感, 光音過敏なし, 活動で増悪しない
# ============================================================
add_edge('D296', 'S70', '光音過敏(なし)',
    {'photophobia_only': 0.05, 'phonophobia_only': 0.05, 'both': 0.05, 'neither': 0.85})
add_edge('D296', 'S69', '頭痛パターン(反復/慢性)',
    {'single_acute': 0.05, 'episodic_recurrent': 0.55, 'chronic_progressive': 0.05, 'chronic_stable': 0.35})
add_edge('D296', 'S68', '頭痛増悪因子(ストレス)',
    {'valsalva_cough': 0.02, 'exertional': 0.05, 'positional_upright': 0.03, 'positional_supine': 0.02, 'none_identified': 0.88})
add_edge('D296', 'E06', '項部硬直なし',
    {'absent': 0.99, 'present': 0.01})
add_edge('D296', 'S13', '悪心(軽度あり)',
    {'absent': 0.80, 'present': 0.20})
add_edge('D296', 'R02', '性別(女性やや多い)',
    {'male': 0.42, 'female': 0.58})
add_edge('D296', 'S114', '不安/ストレス(関連)',
    {'absent': 0.40, 'present': 0.60})
add_edge('D296', 'S116', '不眠(関連)',
    {'absent': 0.50, 'present': 0.50})

# ============================================================
# D297 三叉神経痛 (6→target 13)
# Key: 電撃様疼痛, トリガーゾーン, 片側性, 秒単位
# ============================================================
add_edge('D297', 'S20', '顔面痛(三叉神経領域)',
    {'absent': 0.02, 'present': 0.98})
add_edge('D297', 'S69', '頭痛パターン(反復性)',
    {'single_acute': 0.02, 'episodic_recurrent': 0.90, 'chronic_progressive': 0.03, 'chronic_stable': 0.05})
add_edge('D297', 'R01', '年齢(50歳以上に多い)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.01,'18_39':0.10,'40_64':0.40,'65_plus':0.49})
add_edge('D297', 'R02', '性別(女性やや多い)',
    {'male': 0.38, 'female': 0.62})
add_edge('D297', 'S24', '開口障害(食事/会話でトリガー)',
    {'absent': 0.60, 'present': 0.40})
add_edge('D297', 'E06', '項部硬直なし',
    {'absent': 0.99, 'present': 0.01})
add_edge('D297', 'E16', '意識正常',
    {'normal': 0.99, 'confused': 0.005, 'obtunded': 0.005})

# ============================================================
# D339 網膜剥離 (6→target 14)
# Key: 飛蚊症急増, 光視症, カーテン様視野欠損, 無痛
# ============================================================
add_edge('D339', 'S168', '光視症(網膜牽引)',
    {'absent': 0.20, 'present': 0.80})
add_edge('D339', 'S122', '急性視力低下(片側)',
    {'absent': 0.30, 'unilateral': 0.65, 'bilateral': 0.05})
add_edge('D339', 'S95', '視野障害種類(hemianopia様)',
    {'hemianopia': 0.50, 'central_scotoma': 0.10, 'visual_loss': 0.40})
add_edge('D339', 'S123', '眼痛(なし=網膜剥離の特徴)',
    {'absent': 0.90, 'present': 0.10})
add_edge('D339', 'R01', '年齢(40-70歳にピーク)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.01,'13_17':0.02,'18_39':0.15,'40_64':0.50,'65_plus':0.32})
add_edge('D339', 'E63', '瞳孔異常(RAPD可能)',
    {'normal': 0.60, 'mydriasis': 0.05, 'miosis': 0.02, 'anisocoria': 0.05, 'RAPD': 0.28})
add_edge('D339', 'E16', '意識正常',
    {'normal': 0.99, 'confused': 0.005, 'obtunded': 0.005})
add_edge('D339', 'S69', '頭痛パターン(単回)',
    {'single_acute': 0.75, 'episodic_recurrent': 0.15, 'chronic_progressive': 0.05, 'chronic_stable': 0.05})

# ============================================================
# D226 真性多血症(PV) (7→target 15)
# Key: 赤ら顔, 掻痒(入浴後), 脾腫, Hb高値, 血栓症
# ============================================================
add_edge('D226', 'S96', '掻痒感(入浴後特徴的)',
    {'absent': 0.30, 'localized': 0.10, 'generalized': 0.60})
add_edge('D226', 'E14', '脾腫',
    {'absent': 0.25, 'present': 0.75})
add_edge('D226', 'L93', 'Hb高値',
    {'very_low_under_7':0.01,'low_7_10':0.01,'mild_low_10_12':0.03,'normal':0.10,'high':0.85})
add_edge('D226', 'L01', '白血球増多',
    {'low_under_4000':0.02,'normal_4000_10000':0.30,'high_10000_20000':0.50,'very_high_over_20000':0.18})
add_edge('D226', 'L100', '血小板増多',
    {'very_low_under_50k':0.01,'low_50k_150k':0.04,'normal':0.25,'high_over_400k':0.55,'very_high_over_1000k':0.15})
add_edge('D226', 'S35', '動悸',
    {'absent': 0.55, 'present': 0.45})
add_edge('D226', 'R01', '年齢(60歳以上)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.01,'18_39':0.05,'40_64':0.35,'65_plus':0.59})
add_edge('D226', 'S39', 'DVT/血栓症',
    {'absent': 0.75, 'present': 0.25})

# ============================================================
# D227 胸腺腫 (7→target 14)
# Key: 前縦隔腫瘤, 重症筋無力症合併, 咳嗽/呼吸困難
# ============================================================
add_edge('D227', 'S48', '近位筋力低下(MG合併30-50%)',
    {'absent': 0.55, 'present': 0.45})
add_edge('D227', 'S108', '眼瞼下垂(MG)',
    {'absent': 0.60, 'unilateral': 0.15, 'bilateral': 0.25})
add_edge('D227', 'S107', '複視(MG)',
    {'absent': 0.65, 'binocular': 0.30, 'monocular': 0.05})
add_edge('D227', 'S17', '体重減少',
    {'absent': 0.55, 'present': 0.45})
add_edge('D227', 'L35', '胸部CT(前縦隔腫瘤)',
    {'not_done':0.05,'normal':0.02,'consolidation':0.02,'GGO':0.01,'cavity':0.01,'halo_sign':0.01,'BHL':0.03,'pleural_effusion':0.05})
add_edge('D227', 'R01', '年齢(40-60歳)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.02,'18_39':0.15,'40_64':0.55,'65_plus':0.28})
add_edge('D227', 'S25', '嚥下困難(縦隔圧迫)',
    {'absent': 0.70, 'present': 0.30})

# ============================================================
# D235 CLL (7→target 15)
# Key: リンパ球増多, リンパ節腫脹, 脾腫, 高齢
# ============================================================
add_edge('D235', 'E13', 'リンパ節腫脹(全身性)',
    {'absent': 0.15, 'present': 0.85})
add_edge('D235', 'E46', 'リンパ節部位(全身性)',
    {'cervical':0.25,'axillary':0.20,'inguinal':0.15,'supraclavicular':0.10,'mediastinal':0.10,'generalized':0.20})
add_edge('D235', 'E14', '脾腫',
    {'absent': 0.40, 'present': 0.60})
add_edge('D235', 'E34', '肝腫大',
    {'absent': 0.55, 'present': 0.45})
add_edge('D235', 'S16', '盗汗',
    {'absent': 0.55, 'present': 0.45})
add_edge('D235', 'S17', '体重減少',
    {'absent': 0.50, 'present': 0.50})
add_edge('D235', 'R01', '年齢(70歳以上)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.0,'18_39':0.03,'40_64':0.22,'65_plus':0.75})
add_edge('D235', 'L100', '血小板(減少可能)',
    {'very_low_under_50k':0.10,'low_50k_150k':0.25,'normal':0.50,'high_over_400k':0.10,'very_high_over_1000k':0.05})

# ============================================================
# D236 多発性硬化症(MS) (7→target 16)
# Key: 視神経炎, 感覚障害, 歩行障害, 反復寛解増悪, 若年女性
# ============================================================
add_edge('D236', 'S122', '急性視力低下(視神経炎)',
    {'absent': 0.50, 'unilateral': 0.45, 'bilateral': 0.05})
add_edge('D236', 'S123', '眼痛(眼球運動時痛)',
    {'absent': 0.55, 'present': 0.45})
add_edge('D236', 'S76', '感覚障害パターン',
    {'stocking_glove':0.10,'ascending':0.10,'dermatomal':0.40,'hemisensory':0.30,'saddle':0.10})
add_edge('D236', 'S106', '歩行障害',
    {'absent': 0.40, 'present': 0.60})
add_edge('D236', 'S137', '歩行パターン(痙性/失調)',
    {'ataxic':0.35,'shuffling':0.05,'steppage':0.05,'spastic':0.40,'waddling':0.05,'antalgic':0.10})
add_edge('D236', 'S110', '排尿障害',
    {'absent': 0.40, 'present': 0.60})
add_edge('D236', 'R01', '年齢(20-40歳)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.02,'13_17':0.05,'18_39':0.55,'40_64':0.30,'65_plus':0.08})
add_edge('D236', 'R02', '性別(女性2-3倍)',
    {'male': 0.33, 'female': 0.67})
add_edge('D236', 'E74', 'Babinski陽性(UMN)',
    {'absent': 0.35, 'present': 0.65})

# ============================================================
# D237 腸重積(成人) (7→target 14)
# Key: 間欠的腹痛(周期的), 血便(いちごジャム様), 腹部腫瘤
# ============================================================
add_edge('D237', 'S26', '血便',
    {'absent': 0.40, 'present': 0.60})
add_edge('D237', 'S65', '腹痛パターン(間欠的)',
    {'constant':0.15,'intermittent_colicky':0.70,'progressive':0.10,'migratory':0.05})
add_edge('D237', 'E44', '腹部膨満',
    {'absent': 0.35, 'mild': 0.40, 'severe': 0.25})
add_edge('D237', 'S66', '嘔吐',
    {'absent': 0.25, 'present': 0.75})
add_edge('D237', 'E58', '腹部腫瘤(ソーセージ様)',
    {'absent': 0.45, 'present': 0.55})
add_edge('D237', 'S73', '排便停止(後期)',
    {'absent': 0.40, 'present': 0.60})
add_edge('D237', 'E52', '腸蠕動音亢進',
    {'normal':0.15,'hyperactive_high_pitched':0.65,'hypoactive':0.15,'absent':0.05})

# ============================================================
# D242 消化性潰瘍(非穿孔性) (7→target 15)
# Key: 心窩部痛, 食事との関連, NSAIDs/H.pylori, 吐血/黒色便
# ============================================================
add_edge('D242', 'S61', '腹痛性状(灼烧/啃咬)',
    {'colicky':0.05,'burning_gnawing':0.70,'sharp_stabbing':0.10,'dull_aching':0.10,'tearing':0.05})
add_edge('D242', 'S62', '食事関連(十二指腸=改善,胃=悪化)',
    {'none_identified':0.20,'postprandial':0.30,'relieved_by_food':0.30,'worse_with_movement':0.05,'relieved_by_leaning_forward':0.15})
add_edge('D242', 'S135', '黒色便',
    {'absent': 0.60, 'present': 0.40})
add_edge('D242', 'R08', 'NSAIDs使用',
    {'no': 0.45, 'yes': 0.55})
add_edge('D242', 'S66', '嘔吐',
    {'absent': 0.55, 'present': 0.45})
add_edge('D242', 'L93', 'Hb(慢性出血で低下)',
    {'very_low_under_7':0.03,'low_7_10':0.15,'mild_low_10_12':0.30,'normal':0.47,'high':0.05})
add_edge('D242', 'S102', '胸焼け',
    {'absent': 0.50, 'present': 0.50})
add_edge('D242', 'S89', '腹痛部位(心窩部)',
    {'epigastric':0.70,'RUQ':0.10,'RLQ':0.02,'LLQ':0.02,'suprapubic':0.01,'diffuse':0.15})

# ============================================================
# D262 伝染性膿痂疹(とびひ) (7→target 12)
# Key: 小児, 黄色痂皮, 水疱, 限局性
# ============================================================
add_edge('D262', 'R01', '年齢(小児)',
    {'0_1':0.10,'1_5':0.35,'6_12':0.35,'13_17':0.10,'18_39':0.07,'40_64':0.02,'65_plus':0.01})
add_edge('D262', 'S96', '掻痒感',
    {'absent': 0.20, 'localized': 0.70, 'generalized': 0.10})
add_edge('D262', 'S75', '皮疹分布(顔面/四肢限局)',
    {'trunk_centripetal':0.10,'extremities_centrifugal':0.45,'acral':0.05,'mucosal':0.01,'generalized':0.39})
add_edge('D262', 'E46', 'リンパ節(所属リンパ節)',
    {'cervical':0.45,'axillary':0.15,'inguinal':0.20,'supraclavicular':0.02,'mediastinal':0.01,'generalized':0.17})
add_edge('D262', 'R14', '皮膚外傷',
    {'no': 0.50, 'yes': 0.50})

# ============================================================
# D271 好酸球性食道炎(EoE) (7→target 14)
# Key: 若年男性, 嚥下困難(固形), アレルギー歴, 好酸球増多
# ============================================================
add_edge('D271', 'S101', '嚥下困難種類(固形のみ)',
    {'solids_only': 0.75, 'solids_and_liquids': 0.20, 'liquids_worse': 0.05})
add_edge('D271', 'S78', '嚥下痛',
    {'absent': 0.50, 'present': 0.50})
add_edge('D271', 'R01', '年齢(20-40歳)',
    {'0_1':0.01,'1_5':0.03,'6_12':0.08,'13_17':0.10,'18_39':0.50,'40_64':0.23,'65_plus':0.05})
add_edge('D271', 'R02', '性別(男性3倍)',
    {'male': 0.75, 'female': 0.25})
add_edge('D271', 'S102', '胸焼け',
    {'absent': 0.45, 'present': 0.55})
add_edge('D271', 'S46', '食欲不振',
    {'absent': 0.55, 'present': 0.45})
add_edge('D271', 'S89', '腹痛部位(心窩部)',
    {'epigastric':0.55,'RUQ':0.05,'RLQ':0.02,'LLQ':0.02,'suprapubic':0.01,'diffuse':0.35})

# ============================================================
# D298 Bell麻痺 (7→target 15)
# Key: 急性片側顔面麻痺(上下), 耳後部痛, 味覚障害, 涙液減少
# ============================================================
add_edge('D298', 'S109', '顔面麻痺(上下=末梢性)',
    {'absent': 0.02, 'upper_and_lower': 0.95, 'lower_only': 0.03})
add_edge('D298', 'S79', '耳後部痛',
    {'absent': 0.40, 'present': 0.60})
add_edge('D298', 'S19', '味覚障害(鼓索神経)',
    {'absent': 0.45, 'present': 0.55})
add_edge('D298', 'S164', '眼乾燥(涙液分泌低下)',
    {'absent': 0.50, 'present': 0.50})
add_edge('D298', 'S124', '聴覚過敏(アブミ骨筋)',
    {'absent': 0.65, 'present': 0.35})
add_edge('D298', 'R01', '年齢(15-45歳)',
    {'0_1':0.01,'1_5':0.02,'6_12':0.05,'13_17':0.10,'18_39':0.45,'40_64':0.27,'65_plus':0.10})
add_edge('D298', 'E16', '意識正常',
    {'normal': 0.99, 'confused': 0.005, 'obtunded': 0.005})
add_edge('D298', 'E06', '項部硬直なし',
    {'absent': 0.99, 'present': 0.01})

# ============================================================
# D299 Ramsay Hunt症候群 (7→target 15)
# Key: 顔面麻痺+耳介水疱+耳痛, VZV再活性化
# ============================================================
add_edge('D299', 'S109', '顔面麻痺(末梢性)',
    {'absent': 0.05, 'upper_and_lower': 0.90, 'lower_only': 0.05})
add_edge('D299', 'S79', '耳痛(強い)',
    {'absent': 0.08, 'present': 0.92})
add_edge('D299', 'S124', '難聴(感音性)',
    {'absent': 0.40, 'present': 0.60})
add_edge('D299', 'S140', '難聴種類',
    {'conductive':0.05,'sensorineural':0.85,'mixed':0.10})
add_edge('D299', 'S59', 'めまい(前庭神経障害)',
    {'absent': 0.45, 'present': 0.55})
add_edge('D299', 'S19', '味覚障害',
    {'absent': 0.40, 'present': 0.60})
add_edge('D299', 'S87', '皮膚症状種類(水疱)',
    {'localized_pain_redness':0.15,'rash_widespread':0.85})
add_edge('D299', 'R01', '年齢(高齢)',
    {'0_1':0.01,'1_5':0.01,'6_12':0.02,'13_17':0.03,'18_39':0.10,'40_64':0.33,'65_plus':0.50})

# ============================================================
# D302 PSP (7→target 15)
# Key: 垂直性眼球運動障害, 後方転倒, 筋強剛(体幹), 認知低下
# ============================================================
add_edge('D302', 'E64', '眼球運動障害(垂直方向)',
    {'absent': 0.10, 'present': 0.90})
add_edge('D302', 'E83', '眼球運動障害詳細(gaze palsy)',
    {'CN3_palsy':0.02,'CN4_palsy':0.01,'CN6_palsy':0.02,'INO':0.05,'gaze_palsy':0.90})
add_edge('D302', 'S106', '歩行障害(転倒)',
    {'absent': 0.10, 'present': 0.90})
add_edge('D302', 'S137', '歩行パターン',
    {'ataxic':0.20,'shuffling':0.40,'steppage':0.02,'spastic':0.25,'waddling':0.03,'antalgic':0.10})
add_edge('D302', 'S37', '筋強剛(体幹優位)',
    {'absent': 0.15, 'present': 0.85})
add_edge('D302', 'S104', '記憶障害',
    {'absent': 0.40, 'present': 0.60})
add_edge('D302', 'S150', '認知機能低下(前頭葉型)',
    {'absent': 0.30, 'present': 0.70})
add_edge('D302', 'R01', '年齢(60歳以上)',
    {'0_1':0.0,'1_5':0.0,'6_12':0.0,'13_17':0.0,'18_39':0.02,'40_64':0.28,'65_plus':0.70})

# ============================================================
# Save all
# ============================================================
json.dump(s2, open(os.path.join(BASE, 'step2_fever_edges_v4.json'), 'w'), ensure_ascii=False, indent=2)
json.dump(s3, open(os.path.join(BASE, 'step3_fever_cpts_v2.json'), 'w'), ensure_ascii=False, indent=2)

print(f'Added {added_edges} edges, {added_cpts} CPTs')
print(f'Total edges: {len(s2["edges"])}')
