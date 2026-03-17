#!/usr/bin/env python3
"""Phase 5 batch 3: Add edges for all 9-edge diseases still under 10"""
import json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))

def binary_high(p=0.8): return {'absent': 1-p, 'present': p}
def binary_mod(p=0.5): return {'absent': 1-p, 'present': p}
def binary_low(p=0.3): return {'absent': 1-p, 'present': p}

DISEASE_EDGES = {
    'D06': [  # 急性気管支炎
        ('S84', {'dry':0.3,'productive_purulent':0.3,'productive_clear':0.35,'barking':0.05}, '咳嗽(初期乾性→湿性)'),
        ('S04', binary_low(0.2), '軽度の呼吸困難'),
        ('S07', binary_mod(0.5), '全身倦怠感'),
        ('S21', binary_low(0.25), '咳嗽時胸痛'),
        ('S47', {'under_3weeks':0.6,'3_to_8_weeks':0.35,'over_8weeks':0.05}, '咳嗽3週間前後'),
    ],
    'D39': [  # 肛門周囲膿瘍
        ('S15', binary_mod(0.5), '肛門周囲痛(座位で増悪)'),
        ('S07', binary_mod(0.4), '全身倦怠感'),
        ('E01', {'hypothermia_under_35':0.0,'under_37.5':0.2,'37.5_38.0':0.3,'38.0_39.0':0.35,'39.0_40.0':0.12,'over_40.0':0.03}, '発熱'),
        ('S14', binary_low(0.2), '排便時痛/下痢'),
    ],
    'D41': [  # SSI
        ('S07', binary_mod(0.5), '全身倦怠感'),
        ('E01', {'hypothermia_under_35':0.0,'under_37.5':0.15,'37.5_38.0':0.25,'38.0_39.0':0.4,'39.0_40.0':0.15,'over_40.0':0.05}, '術後発熱(>48h)'),
        ('E12', {'normal':0.05,'localized_erythema_warmth_swelling':0.8,'petechiae_purpura':0.0,'maculopapular_rash':0.0,'vesicular_dermatomal':0.0,'diffuse_erythroderma':0.0,'purpura':0.0,'vesicle_bulla':0.05,'skin_necrosis':0.1}, '創部発赤/腫脹/膿'),
    ],
    'D189': [  # メタノール中毒
        ('S122', {'absent':0.2,'unilateral':0.1,'bilateral':0.7}, '両側視力低下'),
        ('S07', binary_high(0.7), '全身倦怠感'),
        ('L68', {'not_done':0.1,'normal':0.02,'metabolic_acidosis':0.85,'metabolic_alkalosis':0.0,'respiratory_acidosis':0.01,'respiratory_alkalosis':0.0,'lactic_acidosis':0.02}, '代謝性アシドーシス(AG開大)'),
        ('S66', binary_mod(0.5), '嘔吐'),
        ('L92', {'not_done':0.2,'low':0.05,'normal':0.1,'high':0.65}, '浸透圧gap上昇'),
    ],
    'D191': [  # PSGN
        ('S33', binary_high(0.7), '肉眼的血尿(コーラ色)'),
        ('E68', binary_high(0.6), '眼瞼浮腫(朝方)'),
        ('L75', {'not_done':0.2,'normal':0.05,'low_C3':0.65,'low_C4':0.05,'low_both':0.05}, '低補体(C3低下)'),
        ('S82', {'normal':0.3,'oliguria':0.55,'anuria':0.15}, '乏尿'),
    ],
    'D203': [  # 全身性強皮症
        ('S119', binary_high(0.8), 'レイノー現象(90%以上)'),
        ('S25', binary_mod(0.5), '嚥下困難(食道硬化)'),
        ('S102', binary_mod(0.5), '胸焼け(GERD)'),
        ('E55', {'normal':0.1,'splinter_hemorrhage':0.1,'clubbing':0.2,'janeway_osler':0.0}, '強指症/爪変化'),
        ('L18', {'not_done':0.2,'negative':0.1,'positive':0.7}, '抗核抗体陽性'),
    ],
    'D204': [  # アミロイドーシス
        ('S25', binary_mod(0.3), '嚥下困難(舌肥大/自律神経)'),
        ('S76', {'stocking_glove':0.6,'ascending':0.1,'dermatomal':0.05,'hemisensory':0.02,'saddle':0.23}, '末梢神経障害(stocking-glove)'),
        ('E73', {'absent':0.3,'S3':0.3,'S4':0.2,'both':0.2}, 'gallop(restrictive cardiomyopathy)'),
        ('E68', binary_mod(0.4), '眼窩周囲紫斑(pathognomonic)'),
        ('L78', {'not_done':0.2,'negative':0.1,'trace':0.1,'positive':0.6}, '尿蛋白(腎アミロイド)'),
    ],
    'D214': [  # PAH
        ('S49', binary_mod(0.5), '起座呼吸(右心不全進行期)'),
        ('E15', {'absent':0.3,'systolic':0.3,'diastolic':0.2,'both':0.2}, 'TR/PR雑音'),
        ('E73', {'absent':0.4,'S3':0.3,'S4':0.2,'both':0.1}, '右心gallop'),
        ('S97', binary_mod(0.3), '労作時失神'),
        ('E39', {'not_done':0.2,'normal':0.05,'wall_motion_abnormal':0.1,'valvular_abnormal':0.2,'pericardial_effusion':0.1,'LVH':0.05,'dilated_chamber':0.3}, '右心拡大'),
    ],
    'D216': [  # 急性僧帽弁閉鎖不全症
        ('E15', {'absent':0.05,'systolic':0.8,'diastolic':0.05,'both':0.1}, '新規収縮期雑音'),
        ('S49', binary_high(0.8), '急性起座呼吸'),
        ('E39', {'not_done':0.15,'normal':0.05,'wall_motion_abnormal':0.2,'valvular_abnormal':0.4,'pericardial_effusion':0.05,'LVH':0.05,'dilated_chamber':0.1}, '弁逆流(心エコー)'),
        ('E73', {'absent':0.2,'S3':0.5,'S4':0.1,'both':0.2}, 'S3 gallop'),
    ],
    'D222': [  # RA
        ('S23', binary_high(0.8), '関節腫脹'),
        ('E21', binary_high(0.7), '関節の発赤・熱感'),
        ('S90', {'monoarticular':0.05,'oligoarticular':0.15,'polyarticular_asymmetric':0.1,'polyarticular_symmetric':0.7}, '多関節対称性'),
        ('S27', binary_high(0.8), '朝のこわばり'),
        ('S145', {'under_30min':0.05,'30min_to_2h':0.25,'over_2h':0.7}, '朝のこわばり1h以上'),
        ('L88', {'not_done':0.2,'negative':0.2,'positive':0.6}, 'RF陽性'),
    ],
    'D223': [  # MCTD
        ('S119', binary_high(0.85), 'レイノー現象(ほぼ全例)'),
        ('S08', binary_high(0.7), '関節痛'),
        ('S48', binary_mod(0.4), '近位筋力低下(PM/DM要素)'),
        ('L18', {'not_done':0.1,'negative':0.02,'positive':0.88}, '抗核抗体陽性(anti-U1RNP)'),
        ('E36', {'absent':0.5,'present':0.5}, '浮腫(手指のソーセージ様腫脹)'),
    ],
    'D224': [  # ATLL
        ('E13', binary_high(0.7), 'リンパ節腫脹'),
        ('E14', binary_mod(0.5), '肝脾腫'),
        ('E12', {'normal':0.4,'localized_erythema_warmth_swelling':0.05,'petechiae_purpura':0.05,'maculopapular_rash':0.3,'vesicular_dermatomal':0.0,'diffuse_erythroderma':0.15,'purpura':0.0,'vesicle_bulla':0.05,'skin_necrosis':0.0}, '皮疹(多彩)'),
        ('L84', {'not_done':0.2,'low':0.02,'normal':0.18,'mildly_elevated':0.3,'very_high':0.3}, '高Ca血症'),
        ('S17', binary_mod(0.5), '体重減少'),
    ],
    'D240': [  # 急性間質性腎炎(AIN)
        ('S07', binary_mod(0.5), '全身倦怠感'),
        ('S96', {'absent':0.5,'localized':0.1,'generalized':0.4}, '薬剤アレルギー性の皮疹'),
        ('S82', {'normal':0.3,'oliguria':0.5,'anuria':0.2}, '乏尿/無尿'),
        ('L14', {'normal':0.3,'left_shift':0.05,'atypical_lymphocytes':0.05,'thrombocytopenia':0.05,'eosinophilia':0.5,'lymphocyte_predominant':0.05}, '末梢血好酸球増加'),
    ],
    'D250': [  # PBC
        ('S96', {'absent':0.2,'localized':0.1,'generalized':0.7}, '掻痒感(初発症状)'),
        ('S07', binary_high(0.7), '倦怠感'),
        ('E18', binary_mod(0.5), '黄疸(進行期)'),
        ('S31', binary_mod(0.4), '口腔乾燥(シェーグレン合併)'),
        ('S164', binary_mod(0.4), '眼乾燥(シェーグレン合併)'),
    ],
    'D260': [  # ヘルパンギーナ
        ('E08', {'normal':0.05,'erythema':0.15,'exudate_or_white_patch':0.8}, '口蓋弓/咽頭の水疱性口内炎'),
        ('S78', binary_high(0.7), '嚥下痛'),
        ('E01', {'hypothermia_under_35':0.0,'under_37.5':0.05,'37.5_38.0':0.1,'38.0_39.0':0.4,'39.0_40.0':0.35,'over_40.0':0.1}, '高熱(38-40度)'),
        ('S46', binary_mod(0.5), '食欲不振(嚥下痛による)'),
    ],
    'D269': [  # ロタウイルス胃腸炎
        ('S14', binary_high(0.85), '下痢'),
        ('S86', {'bloody':0.02,'watery':0.85,'mucoid':0.05,'fatty':0.01,'rice_water':0.07}, '水様性下痢(白色)'),
        ('S66', binary_high(0.7), '嘔吐'),
        ('E54', binary_mod(0.5), '脱水(小児で顕著)'),
        ('S173', {'acute_under_2w':0.95,'persistent_2w_4w':0.04,'chronic_over_4w':0.01}, '急性(3-8日)'),
    ],
    'D270': [  # アスピリン喘息(NSAIDs不耐症)
        ('S81', {'stridor':0.05,'wheezing':0.8,'air_hunger_kussmaul':0.05,'paroxysmal_nocturnal':0.1}, 'wheezing'),
        ('S03', binary_high(0.7), '鼻汁(鼻茸/副鼻腔炎)'),
        ('S04', binary_high(0.8), '呼吸困難(NSAID服用後)'),
        ('S96', {'absent':0.5,'localized':0.2,'generalized':0.3}, '蕁麻疹/血管性浮腫'),
    ],
    'D288': [  # 精巣腫瘍
        ('S38', binary_high(0.85), '陰嚢腫脹(無痛性が典型)'),
        ('S169', binary_low(0.2), '疼痛は通常軽度'),
        ('S17', binary_mod(0.3), '体重減少(進行期)'),
        ('E13', binary_mod(0.3), 'リンパ節腫脹(傍大動脈)'),
    ],
    'D295': [  # 群発頭痛
        ('S71', binary_high(0.85), '自律神経症状(流涙/結膜充血/鼻閉)'),
        ('S153', {'ipsilateral':0.95,'bilateral':0.05}, '同側性'),
        ('S60', {'tension_band':0.01,'thunderclap':0.01,'throbbing_pulsatile':0.15,'stabbing':0.6,'dull_pressure':0.03,'retro_orbital':0.2}, '眼窩後部の激痛'),
        ('S69', {'single_acute':0.05,'episodic_recurrent':0.85,'chronic_progressive':0.02,'chronic_stable':0.08}, '群発期に毎日反復'),
        ('E25', binary_mod(0.5), '結膜充血(同側)'),
    ],
    'D303': [  # パーキンソン病
        ('S105', binary_high(0.7), '不随意運動(安静時振戦)'),
        ('S106', {'absent':0.1,'ataxic':0.05,'shuffling':0.7,'steppage':0.02,'spastic':0.03,'waddling':0.05,'antalgic':0.05}, 'すくみ足/小刻み歩行'),
        ('S109', {'absent':0.5,'upper_and_lower':0.1,'lower_only':0.4}, '仮面様顔貌(表情筋)'),
        ('S25', binary_mod(0.3), '嚥下困難(進行期)'),
        ('S53', binary_mod(0.3), '小声/構音障害'),
    ],
    'D304': [  # レビー小体型認知症(DLB)
        ('S104', binary_high(0.8), '記憶障害(変動性)'),
        ('S150', binary_high(0.8), '認知機能低下(注意/遂行機能)'),
        ('S117', binary_high(0.7), '幻覚(詳細な幻視が特徴的)'),
        ('S138', {'visual':0.85,'auditory':0.1,'tactile':0.05}, '幻視'),
        ('S105', binary_mod(0.5), 'パーキンソニズム'),
        ('S116', binary_mod(0.4), '不眠/REM睡眠行動障害'),
    ],
    'D309': [  # 脳AVM
        ('S42', binary_mod(0.5), '痙攣(初発症状として多い)'),
        ('S175', {'hyperacute_seconds':0.7,'acute_hours':0.2,'subacute_days_weeks':0.08,'chronic_progressive':0.02}, '超急性発症(出血時)'),
        ('E67', binary_mod(0.3), '髄膜刺激徴候(出血時)'),
        ('S04', binary_low(0.2), '呼吸困難(大出血時)'),
    ],
    'D310': [  # TIA
        ('S175', {'hyperacute_seconds':0.8,'acute_hours':0.15,'subacute_days_weeks':0.04,'chronic_progressive':0.01}, '超急性発症'),
        ('S53', binary_mod(0.5), '一過性の言語障害'),
        ('S54', binary_mod(0.3), '一過性の視野障害(amaurosis fugax)'),
        ('E40', {'not_done':0.3,'normal':0.3,'ST_change':0.1,'arrhythmia':0.2,'conduction_block':0.1}, '心房細動(塞栓源)'),
    ],
    'D317': [  # PAP(肺胞蛋白症)
        ('S81', {'stridor':0.0,'wheezing':0.05,'air_hunger_kussmaul':0.1,'paroxysmal_nocturnal':0.0}, '進行性呼吸困難'),
        ('S07', binary_mod(0.5), '倦怠感'),
        ('S17', binary_low(0.2), '体重減少'),
        ('L35', {'normal':0.05,'consolidation':0.1,'GGO':0.7,'cavity':0.0,'halo_sign':0.0,'BHL':0.0,'pleural_effusion':0.15}, 'crazy paving pattern(CT)'),
    ],
    'D320': [  # 喉頭癌
        ('S55', binary_high(0.85), '嗄声(主症状)'),
        ('S78', binary_mod(0.4), '嚥下痛(進行期)'),
        ('S17', binary_mod(0.4), '体重減少'),
        ('E13', binary_mod(0.3), '頸部リンパ節腫脹'),
    ],
    'D338': [  # 腸重積症(小児向けだが成人も)
        ('S14', binary_mod(0.5), '下痢/粘血便'),
        ('E09', {'normal':0.2,'diffuse_tenderness':0.2,'RUQ_tenderness':0.1,'RLQ_tenderness':0.05,'LLQ_tenderness':0.05,'rebound_guarding':0.2,'murphy_positive':0.0,'CVA_tenderness':0.0,'suprapubic_tenderness':0.0,'mass_palpable':0.2}, '腹部腫瘤触知'),
        ('S12', binary_high(0.8), '間欠性腹痛'),
        ('S66', binary_high(0.7), '嘔吐'),
    ],
    'D342': [  # QT延長症候群
        ('S97', binary_high(0.7), '失神(TdP発作)'),
        ('S42', binary_mod(0.5), '痙攣(TdP)'),
        ('S35', binary_mod(0.5), '動悸'),
        ('E40', {'not_done':0.1,'normal':0.05,'ST_change':0.1,'arrhythmia':0.65,'conduction_block':0.1}, 'QT延長/TdP'),
    ],
}

def run():
    s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
    s2 = json.load(open(os.path.join(BASE, 'step2_fever_edges_v4.json')))
    s3 = json.load(open(os.path.join(BASE, 'step3_fever_cpts_v2.json')))
    name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}

    existing_edges = set((e['from'], e['to']) for e in s2['edges'])
    added_e, added_c = 0, 0

    for did, edge_list in DISEASE_EDGES.items():
        for target_id, cpt_dict, reason in edge_list:
            if target_id not in name_map:
                print(f'  WARNING: {target_id} not found')
                continue
            if target_id.startswith('R'):
                continue
            if (did, target_id) in existing_edges:
                continue
            s2['edges'].append({
                'from': did, 'to': target_id,
                'from_name': name_map.get(did,''), 'to_name': name_map.get(target_id,''),
                'reason': reason, 'onset_day_range': None
            })
            existing_edges.add((did, target_id))
            added_e += 1
            if cpt_dict and target_id in s3['noisy_or_params']:
                p = s3['noisy_or_params'][target_id]
                if 'parent_effects' not in p:
                    p['parent_effects'] = {}
                if did not in p['parent_effects']:
                    p['parent_effects'][did] = cpt_dict
                    added_c += 1

    json.dump(s2, open(os.path.join(BASE, 'step2_fever_edges_v4.json'), 'w'), ensure_ascii=False, indent=2)
    json.dump(s3, open(os.path.join(BASE, 'step3_fever_cpts_v2.json'), 'w'), ensure_ascii=False, indent=2)

    print(f'Added {added_e} edges, {added_c} CPTs')
    edge_count = Counter(e['from'] for e in s2['edges'] if e['from'].startswith('D'))
    for did in sorted(DISEASE_EDGES.keys(), key=lambda x: int(x[1:])):
        print(f'  {did}: {name_map.get(did,"")[:35]:35s} {edge_count[did]:3d} edges')
    
    under10 = sum(1 for d,c in edge_count.items() if c < 10)
    print(f'\nTotal edges: {len(s2["edges"])}')
    print(f'Diseases still <10 edges: {under10}')

if __name__ == '__main__':
    run()
