#!/usr/bin/env python3
"""Phase 5 Batch 2: Add edges for diseases with 8-9 edges"""
import json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))

def b(p=0.8): return {'absent': round(1-p,2), 'present': round(p,2)}

EDGES = {
    'D76': [('S07',b(0.6),'倦怠感'),('S04',b(0.3),'呼吸困難(TRALI)'),('E03',{'normal_over_90':0.7,'hypotension_under_90':0.3},'低血圧'),('S18',b(0.3),'蕁麻疹')],
    'D147': [('S38',b(0.95),'陰嚢腫脹'),('S169',b(0.95),'陰嚢疼痛'),('S66',b(0.6),'嘔吐'),('E12',{'normal':0.3,'localized_erythema_warmth_swelling':0.65,'petechiae_purpura':0.0,'maculopapular_rash':0.0,'vesicular_dermatomal':0.0,'diffuse_erythroderma':0.0,'purpura':0.0,'vesicle_bulla':0.0,'skin_necrosis':0.05},'患側発赤'),('S12',b(0.4),'下腹部痛')],
    'D180': [('E44',{'absent':0.05,'mild':0.25,'severe':0.7},'著明な腹部膨満'),('S66',b(0.6),'嘔吐'),('S73',b(0.8),'排便停止'),('S74',b(0.7),'排ガス停止'),('E52',{'normal':0.1,'hyperactive_high_pitched':0.3,'hypoactive':0.3,'absent':0.3},'腸蠕動音異常')],
    'D184': [('S111',b(0.9),'腰痛(炎症性)'),('S22',b(0.5),'背部痛'),('S90',{'monoarticular':0.1,'oligoarticular':0.5,'polyarticular_symmetric':0.05,'polyarticular_asymmetric':0.3,'migratory':0.05},'末梢関節'),('E35',b(0.3),'虹彩炎'),('L28',{'normal':0.2,'elevated':0.6,'very_high_over_100':0.2},'ESR上昇'),('S145',{'under_30min':0.05,'30min_to_1hr':0.15,'over_1hr':0.8},'朝こわばり>1h')],
    'D187': [('S15',b(0.8),'左側腹部痛'),('S89',{'epigastric':0.1,'RUQ':0.05,'RLQ':0.05,'LLQ':0.6,'suprapubic':0.0,'diffuse':0.2},'LLQ痛'),('E14',b(0.4),'脾腫'),('S04',b(0.3),'呼吸困難'),('L31',{'not_done':0.3,'normal':0.1,'abscess':0.1,'mass':0.0,'other_abnormal':0.5},'脾楔状')],
    'D190': [('L92',{'normal':0.05,'low':0.9,'high':0.05},'血清浸透圧低下'),('L91',{'dilute':0.05,'normal':0.15,'concentrated':0.8},'尿浸透圧高'),('S82',{'normal':0.6,'oliguria':0.3,'anuria':0.1},'尿量減少'),('S66',b(0.3),'嘔吐')],
    'D200': [('S106',{'absent':0.05,'ataxic':0.1,'shuffling':0.65,'steppage':0.02,'spastic':0.05,'waddling':0.05,'antalgic':0.08},'歩行障害'),('S104',b(0.8),'記憶障害'),('S150',b(0.8),'認知機能低下'),('S99',{'absent':0.2,'stress':0.1,'urge':0.6,'overflow':0.05,'functional':0.05},'尿失禁'),('S110',b(0.3),'排尿障害')],
    'D211': [('E63',{'normal':0.2,'miosis':0.1,'mydriasis':0.65,'anisocoria':0.05},'散瞳'),('E40',{'not_done':0.1,'normal':0.05,'atrial_fibrillation':0.05,'ST_elevation':0.05,'ST_depression':0.1,'RBBB_LBBB':0.3,'wide_QRS':0.3,'other_arrhythmia':0.05},'QRS延長'),('L68',{'not_done':0.2,'normal':0.1,'metabolic_acidosis':0.6,'metabolic_alkalosis':0.0,'respiratory_acidosis':0.05,'respiratory_alkalosis':0.0,'lactic_acidosis':0.05},'アシドーシス'),('E54',{'absent':0.5,'mild':0.3,'severe':0.2},'脱水')],
    'D212': [('E10',{'normal':0.2,'elevated':0.7,'markedly_elevated':0.1},'JVD'),('E73',b(0.8),'gallop'),('E39',{'not_done':0.2,'normal':0.05,'wall_motion_abnormal':0.2,'valvular_abnormal':0.1,'pericardial_effusion':0.05,'LVH':0.2,'dilated_chamber':0.2},'心エコー異常'),('S49',b(0.6),'起座呼吸'),('E36',b(0.7),'下腿浮腫')],
    'D217': [('S52',b(0.6),'末梢麻痺'),('E33',b(0.8),'動脈拍動消失'),('E41',{'not_done':0.2,'normal_over_0.9':0.05,'low_under_0.9':0.75},'ABI低下'),('S06',b(0.5),'患肢痛'),('E69',{'normal':0.1,'delayed_3s':0.3,'very_delayed_5s':0.6},'CRT延長')],
    'D218': [('S36',b(0.6),'振戦'),('S115',b(0.4),'抑うつ'),('S117',b(0.2),'精神症状'),('L87',{'normal':0.2,'indirect_dominant':0.1,'direct_dominant':0.5,'both_elevated':0.2},'ビリルビン'),('L93',{'very_low_under_7':0.1,'low_7_10':0.2,'mild_low_10_12':0.3,'normal':0.35,'high':0.05},'溶血性貧血')],
    'D225': [('L93',{'very_low_under_7':0.3,'low_7_10':0.3,'mild_low_10_12':0.25,'normal':0.1,'high':0.05},'貧血'),('L100',{'very_low_under_50k':0.3,'low_50k_150k':0.35,'normal':0.3,'high_over_400k':0.03,'very_high_over_1000k':0.02},'血小板減少'),('L22',b(0.5),'汎血球減少'),('E14',b(0.2),'脾腫'),('L94',{'microcytic':0.05,'normocytic':0.3,'macrocytic':0.65},'大球性')],
    'D228': [('L93',{'very_low_under_7':0.2,'low_7_10':0.3,'mild_low_10_12':0.3,'normal':0.15,'high':0.05},'溶血性貧血'),('L98',{'normal':0.05,'low':0.4,'absent':0.55},'ハプトグロビン低下'),('L72',{'not_done':0.2,'normal':0.1,'elevated':0.7},'網赤血球増加'),('S100',{'normal':0.3,'abnormal':0.7},'暗色尿'),('L100',{'very_low_under_50k':0.15,'low_50k_150k':0.35,'normal':0.4,'high_over_400k':0.08,'very_high_over_1000k':0.02},'血小板減少')],
    'D229': [('L37',{'not_done':0.2,'normal':0.1,'elevated':0.7},'IgG4高値'),('L36',{'normal':0.3,'elevated':0.5,'very_high':0.2},'膵酵素上昇'),('S17',b(0.5),'体重減少'),('L31',{'not_done':0.2,'normal':0.1,'abscess':0.0,'mass':0.4,'other_abnormal':0.3},'膵腫大')],
    'D238': [('S26',b(0.5),'血便'),('S72',b(0.4),'便秘'),('S17',b(0.6),'体重減少'),('L93',{'very_low_under_7':0.1,'low_7_10':0.2,'mild_low_10_12':0.3,'normal':0.35,'high':0.05},'貧血'),('L79',{'not_done':0.3,'negative':0.1,'positive':0.6},'便潜血'),('E58',b(0.3),'腹部腫瘤'),('L94',{'microcytic':0.5,'normocytic':0.35,'macrocytic':0.15},'小球性貧血')],
    'D239': [('S33',b(0.8),'血尿'),('L78',{'not_done':0.3,'negative':0.2,'trace':0.2,'positive':0.3},'尿蛋白'),('L75',{'not_done':0.2,'normal':0.3,'low_C3':0.4,'low_C4':0.05,'low_both':0.05},'補体C3低下')],
    'D243': [('S66',b(0.9),'大量吐血'),('S67',{'bilious':0.02,'bloody':0.9,'feculent':0.0,'projectile':0.0,'food_content':0.08},'鮮血'),('S26',b(0.4),'黒色便'),('E14',b(0.6),'脾腫'),('E65',b(0.4),'腹壁静脈怒張'),('L69',{'normal':0.3,'mildly_prolonged':0.4,'very_prolonged':0.3},'PT延長')],
    'D247': [('S25',b(0.3),'嚥下困難'),('S17',b(0.7),'体重減少'),('S131',b(0.5),'早期満腹感'),('L93',{'very_low_under_7':0.1,'low_7_10':0.2,'mild_low_10_12':0.3,'normal':0.35,'high':0.05},'貧血'),('E46',{'cervical':0.1,'axillary':0.05,'inguinal':0.02,'supraclavicular':0.6,'mediastinal':0.03,'generalized':0.2},'Virchow LN'),('L79',{'not_done':0.3,'negative':0.2,'positive':0.5},'便潜血')],
    'D268': [('S66',b(0.8),'嘔吐'),('E54',{'absent':0.3,'mild':0.4,'severe':0.3},'脱水'),('S86',{'watery':0.8,'bloody':0.02,'mucoid':0.08,'fatty':0.0,'rice_water':0.1},'水様性下痢')],
    'D272': [('S101',{'solids_only':0.3,'solids_and_liquids':0.6,'liquids_worse':0.1},'固液嚥下困難'),('S17',b(0.5),'体重減少'),('S102',b(0.3),'胸焼け'),('S66',b(0.4),'嘔吐')],
    'D300': [('S104',b(0.9),'急速進行性認知症'),('S150',b(0.9),'認知機能低下'),('S105',b(0.7),'ミオクローヌス'),('S106',{'absent':0.1,'ataxic':0.6,'shuffling':0.1,'steppage':0.02,'spastic':0.05,'waddling':0.02,'antalgic':0.1},'歩行障害'),('E61',b(0.5),'小脳徴候'),('S54',b(0.3),'視覚障害'),('S141',{'acute':0.3,'subacute':0.6,'chronic_progressive':0.1},'亜急性進行')],
    'D307': [('S48',b(0.7),'対麻痺'),('S76',{'stocking_glove':0.1,'ascending':0.3,'dermatomal':0.4,'hemisensory':0.1,'saddle':0.1},'感覚レベル'),('S110',b(0.7),'尿閉'),('S99',{'absent':0.3,'stress':0.05,'urge':0.1,'overflow':0.5,'functional':0.05},'溢流性尿失禁'),('E74',b(0.6),'Babinski'),('L80',{'not_done':0.2,'normal':0.05,'degenerative':0.05,'compression_fracture':0.02,'epidural_abscess':0.03,'canal_stenosis':0.02,'cord_signal_change':0.6,'other':0.03},'脊髄MRI')],
    'D308': [('S111',b(0.8),'腰痛'),('S110',b(0.8),'尿閉'),('S76',{'stocking_glove':0.1,'ascending':0.1,'dermatomal':0.2,'hemisensory':0.05,'saddle':0.55},'鞍部感覚障害'),('E53',{'normal':0.2,'areflexia':0.4,'hyporeflexia':0.35,'hyperreflexia':0.05},'反射低下'),('S99',{'absent':0.2,'stress':0.05,'urge':0.05,'overflow':0.6,'functional':0.1},'溢流性尿失禁'),('E82',{'not_done':0.3,'normal':0.1,'decreased_tone':0.5,'mass':0.05,'bloody':0.05},'肛門括約筋低下')],
    'D06': [('S84',{'dry':0.4,'productive_clear':0.3,'productive_purulent':0.2,'hemoptysis':0.05,'barking':0.05},'乾→湿'),('S03',b(0.5),'鼻汁'),('S47',{'acute_under_3w':0.7,'subacute_3w_8w':0.25,'chronic_over_8w':0.05},'急性'),('S09',b(0.3),'悪寒'),('S04',b(0.2),'軽度呼吸困難')],
    'D39': [('E54',{'absent':0.6,'mild':0.3,'severe':0.1},'局所腫脹'),('L09',{'not_done_or_pending':0.5,'negative':0.2,'gram_positive':0.2,'gram_negative':0.1},'混合菌')],
    'D41': [('S09',b(0.5),'悪寒'),('L09',{'not_done_or_pending':0.3,'negative':0.1,'gram_positive':0.4,'gram_negative':0.2},'創培養')],
    'D189': [('S122',{'absent':0.2,'unilateral':0.1,'bilateral':0.7},'視力障害'),('L68',{'not_done':0.1,'normal':0.02,'metabolic_acidosis':0.8,'metabolic_alkalosis':0.0,'respiratory_acidosis':0.0,'respiratory_alkalosis':0.0,'lactic_acidosis':0.08},'AG開大アシドーシス'),('S66',b(0.6),'嘔吐'),('E57',b(0.3),'乳頭浮腫'),('L92',{'normal':0.05,'low':0.05,'high':0.9},'浸透圧ギャップ')],
    'D191': [('S33',b(0.8),'血尿'),('S100',{'normal':0.2,'abnormal':0.8},'コーラ色尿'),('L75',{'not_done':0.2,'normal':0.1,'low_C3':0.6,'low_C4':0.05,'low_both':0.05},'C3低下'),('L78',{'not_done':0.2,'negative':0.1,'trace':0.2,'positive':0.5},'尿蛋白')],
    'D203': [('S119',b(0.8),'レイノー'),('S31',b(0.4),'口腔乾燥'),('S25',b(0.5),'嚥下困難'),('S102',b(0.5),'GERD'),('L18',{'not_done':0.1,'negative':0.1,'positive':0.8},'ANA'),('S96',{'absent':0.4,'localized':0.4,'generalized':0.2},'掻痒')],
    'D204': [('S25',b(0.3),'嚥下困難'),('S76',{'stocking_glove':0.6,'ascending':0.1,'dermatomal':0.1,'hemisensory':0.05,'saddle':0.15},'末梢神経障害'),('S14',b(0.3),'下痢'),('E12',{'normal':0.5,'localized_erythema_warmth_swelling':0.05,'petechiae_purpura':0.3,'maculopapular_rash':0.05,'vesicular_dermatomal':0.0,'diffuse_erythroderma':0.0,'purpura':0.1,'vesicle_bulla':0.0,'skin_necrosis':0.0},'紫斑'),('L78',{'not_done':0.2,'negative':0.1,'trace':0.2,'positive':0.5},'尿蛋白'),('S17',b(0.5),'体重減少')],
    'D214': [('S97',b(0.3),'労作時失神'),('S35',b(0.4),'動悸'),('E10',{'normal':0.3,'elevated':0.5,'markedly_elevated':0.2},'JVD'),('E73',b(0.5),'II音亢進'),('E39',{'not_done':0.2,'normal':0.1,'wall_motion_abnormal':0.2,'valvular_abnormal':0.1,'pericardial_effusion':0.05,'LVH':0.05,'dilated_chamber':0.3},'右室拡大')],
    'D216': [('E15',{'absent':0.02,'systolic':0.85,'diastolic':0.05,'both':0.08},'汎収縮期雑音'),('S49',b(0.7),'起座呼吸'),('E39',{'not_done':0.1,'normal':0.05,'wall_motion_abnormal':0.2,'valvular_abnormal':0.5,'pericardial_effusion':0.05,'LVH':0.05,'dilated_chamber':0.05},'弁膜異常'),('E10',{'normal':0.3,'elevated':0.5,'markedly_elevated':0.2},'JVD')],
    'D222': [('S23',b(0.7),'関節腫脹'),('E21',b(0.6),'関節炎症'),('S90',{'monoarticular':0.05,'oligoarticular':0.1,'polyarticular_symmetric':0.75,'polyarticular_asymmetric':0.05,'migratory':0.05},'対称性多関節'),('L76',{'not_done':0.2,'negative':0.15,'positive':0.65},'抗CCP'),('L88',{'not_done':0.2,'negative':0.15,'positive':0.65},'RF'),('S145',{'under_30min':0.05,'30min_to_1hr':0.15,'over_1hr':0.8},'朝こわばり>1h')],
    'D223': [('S119',b(0.8),'レイノー'),('L18',{'not_done':0.1,'negative':0.05,'positive':0.85},'ANA'),('S23',b(0.5),'関節腫脹'),('S48',b(0.3),'近位筋力低下')],
    'D224': [('E13',b(0.7),'リンパ節腫脹'),('E14',b(0.5),'脾腫'),('S18',b(0.5),'皮膚浸潤'),('L84',{'not_done':0.2,'low':0.05,'normal':0.1,'high':0.65},'高Ca'),('S17',b(0.4),'体重減少')],
    'D240': [('S18',b(0.4),'皮疹'),('S96',{'absent':0.4,'localized':0.3,'generalized':0.3},'掻痒'),('S82',{'normal':0.3,'oliguria':0.5,'anuria':0.2},'乏尿')],
    'D250': [('S96',{'absent':0.1,'localized':0.2,'generalized':0.7},'全身掻痒'),('S17',b(0.3),'体重減少'),('L18',{'not_done':0.1,'negative':0.1,'positive':0.8},'AMA/ANA'),('S31',b(0.4),'口腔乾燥')],
    'D260': [('S29',b(0.9),'口腔内水疱'),('S46',b(0.5),'食欲不振'),('S78',b(0.6),'嚥下痛')],
    'D269': [('S66',b(0.7),'嘔吐'),('S86',{'watery':0.85,'bloody':0.02,'mucoid':0.05,'fatty':0.0,'rice_water':0.08},'水様性下痢'),('E54',{'absent':0.2,'mild':0.4,'severe':0.4},'脱水')],
    'D270': [('S81',{'stridor':0.05,'wheezing':0.8,'air_hunger_kussmaul':0.05,'paroxysmal_nocturnal':0.1},'wheezing'),('S126',b(0.6),'鼻ポリープ')],
    'D288': [('S169',b(0.3),'陰嚢鈍痛'),('S17',b(0.3),'体重減少'),('E13',b(0.3),'後腹膜LN')],
    'D295': [('S71',b(0.9),'自律神経症状'),('S153',{'left_only':0.5,'right_only':0.5},'片側性'),('S69',{'single_acute':0.05,'episodic_recurrent':0.85,'chronic_progressive':0.05,'chronic_stable':0.05},'群発期反復'),('S70',{'photophobia_only':0.1,'phonophobia_only':0.05,'both':0.15,'neither':0.7},'光音過敏軽度')],
    'D303': [('E81',{'normal':0.05,'rigidity':0.8,'hypotonia':0.05,'spasticity':0.1},'筋強剛'),('S106',{'absent':0.05,'ataxic':0.05,'shuffling':0.75,'steppage':0.02,'spastic':0.03,'waddling':0.02,'antalgic':0.08},'すくみ足'),('S163',b(0.5),'嗅覚障害'),('S116',b(0.5),'不眠'),('S150',b(0.4),'認知機能低下'),('S115',b(0.4),'抑うつ')],
    'D304': [('S117',b(0.8),'幻覚'),('S138',{'visual':0.85,'auditory':0.1,'tactile':0.05},'視覚性幻覚'),('S104',b(0.9),'記憶障害'),('S150',b(0.9),'認知機能低下'),('E81',{'normal':0.1,'rigidity':0.7,'hypotonia':0.05,'spasticity':0.15},'パーキンソニズム'),('S106',{'absent':0.1,'ataxic':0.05,'shuffling':0.65,'steppage':0.02,'spastic':0.05,'waddling':0.03,'antalgic':0.1},'すくみ足')],
    'D309': [('S34',b(0.3),'喀血'),('E33',b(0.3),'血管雑音'),('S175',{'hyperacute_seconds':0.6,'acute_hours':0.2,'subacute_days_weeks':0.15,'chronic_progressive':0.05},'超急性発症')],
    'D310': [('S175',{'hyperacute_seconds':0.8,'acute_hours':0.15,'subacute_days_weeks':0.04,'chronic_progressive':0.01},'超急性→24h消失'),('S54',b(0.3),'一過性黒内障'),('E33',b(0.3),'頸動脈雑音')],
    'D317': [('L35',{'not_done':0.2,'normal':0.05,'consolidation':0.1,'GGO':0.5,'cavity':0.0,'halo_sign':0.0,'BHL':0.0,'pleural_effusion':0.05},'GGO'),('S84',{'dry':0.6,'productive_clear':0.2,'productive_purulent':0.05,'hemoptysis':0.1,'barking':0.05},'乾性咳嗽'),('S17',b(0.3),'体重減少')],
    'D320': [('S17',b(0.5),'体重減少'),('E13',b(0.4),'頸部LN'),('S79',b(0.3),'耳痛'),('E46',{'cervical':0.7,'axillary':0.02,'inguinal':0.01,'supraclavicular':0.2,'mediastinal':0.02,'generalized':0.05},'頸部LN部位')],
    'D338': [('S12',b(0.9),'間欠的腹痛'),('E09',{'normal':0.3,'tenderness_no_guarding':0.3,'guarding':0.2,'rigidity_rebound':0.1,'mass':0.1},'腹部腫瘤'),('E52',{'normal':0.2,'hyperactive_high_pitched':0.5,'hypoactive':0.2,'absent':0.1},'腸蠕動音')],
    'D342': [('S97',b(0.5),'失神'),('S35',b(0.4),'動悸'),('S175',{'hyperacute_seconds':0.7,'acute_hours':0.2,'subacute_days_weeks':0.08,'chronic_progressive':0.02},'急性発症')],
}

def run():
    s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
    s2 = json.load(open(os.path.join(BASE, 'step2_fever_edges_v4.json')))
    s3 = json.load(open(os.path.join(BASE, 'step3_fever_cpts_v2.json')))
    name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}
    existing = set((e['from'], e['to']) for e in s2['edges'])
    added_e, added_c = 0, 0
    for did, elist in EDGES.items():
        for target, cpt, reason in elist:
            if target not in name_map:
                print(f'  WARN: {target} not found'); continue
            if target.startswith('R'): continue
            if (did, target) in existing: continue
            s2['edges'].append({'from':did,'to':target,'from_name':name_map.get(did,''),'to_name':name_map.get(target,''),'reason':reason,'onset_day_range':None})
            existing.add((did, target)); added_e += 1
            if cpt and target in s3['noisy_or_params']:
                p = s3['noisy_or_params'][target]
                if 'parent_effects' not in p: p['parent_effects'] = {}
                if did not in p['parent_effects']:
                    p['parent_effects'][did] = cpt; added_c += 1
    json.dump(s2, open(os.path.join(BASE, 'step2_fever_edges_v4.json'), 'w'), ensure_ascii=False, indent=2)
    json.dump(s3, open(os.path.join(BASE, 'step3_fever_cpts_v2.json'), 'w'), ensure_ascii=False, indent=2)
    print(f'Batch 2: Added {added_e} edges, {added_c} CPTs')
    print(f'Total edges: {len(s2["edges"])}')
    ec = Counter(e['from'] for e in s2['edges'] if e['from'].startswith('D'))
    under10 = sum(1 for c in ec.values() if c < 10)
    print(f'Diseases <10 edges: {under10}')

if __name__ == '__main__': run()
