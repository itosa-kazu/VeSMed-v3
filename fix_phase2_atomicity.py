#!/usr/bin/env python3
"""Phase 2 Atomicity fixes — split merged concepts, rename, expand states"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
existing_ids = {v['id'] for v in s1['variables']}
max_s = max(int(v['id'][1:]) for v in s1['variables'] if v['id'].startswith('S') and v['id'][1:].isdigit())
max_l = max(int(v['id'][1:]) for v in s1['variables'] if v['id'].startswith('L') and v['id'][1:].isdigit())
max_r = max(int(v['id'][1:]) for v in s1['variables'] if v['id'].startswith('R') and v['id'][1:].isdigit())
sid, lid, rid = max_s + 1, max_l + 1, max_r + 1

var_map = {v['id']: v for v in s1['variables']}
added = []

# ============================================================
# SPLITS — truly independent clinical concepts
# ============================================================

# 1. S19 味覚・嗅覚障害 → 味覚障害 + 嗅覚障害
var_map['S19']['name_ja'] = '味覚障害'
var_map['S19']['name'] = 'taste_disorder'
var_map['S19']['note'] = '亜鉛欠乏/薬剤性/口腔内感染/頭部外傷/放射線治療後。嗅覚障害(S{})とは独立'.format(sid)
added.append({'id':f'S{sid}','name':'anosmia_hyposmia','name_ja':'嗅覚障害',
    'category':'symptom','states':['absent','present'],
    'note':'COVID-19(急性)/パーキンソン(早期)/前頭葉病変/副鼻腔炎/頭部外傷。味覚障害(S19)とは独立'})
print(f'S19 → 味覚障害 + S{sid} 嗅覚障害')
sid += 1

# 2. S31 乾燥症状（口腔/眼）→ 口腔乾燥 + 眼乾燥
var_map['S31']['name_ja'] = '口腔乾燥'
var_map['S31']['name'] = 'dry_mouth'
var_map['S31']['note'] = 'シェーグレン/薬剤性(抗コリン)/放射線/脱水/糖尿病。眼乾燥(S{})とは独立'.format(sid)
added.append({'id':f'S{sid}','name':'dry_eyes','name_ja':'眼乾燥',
    'category':'symptom','states':['absent','present'],
    'note':'シェーグレン/加齢/VDT作業/薬剤性/マイボーム腺機能不全。口腔乾燥(S31)とは独立'})
print(f'S31 → 口腔乾燥 + S{sid} 眼乾燥')
sid += 1

# 3. S57 無月経/乳汁分泌不全 → 無月経 + 乳汁分泌不全
var_map['S57']['name_ja'] = '無月経'
var_map['S57']['name'] = 'amenorrhea'
var_map['S57']['note'] = '原発性/続発性。PCOS/視床下部性/高プロラクチン/早発卵巣不全/Sheehan/甲状腺/妊娠'
added.append({'id':f'S{sid}','name':'agalactia','name_ja':'乳汁分泌不全',
    'category':'symptom','states':['absent','present'],
    'note':'産褥期に乳汁が出ない。Sheehan症候群の特徴的所見。下垂体壊死/高プロラクチン(逆に乳汁漏出→S144)'})
print(f'S57 → 無月経 + S{sid} 乳汁分泌不全')
sid += 1

# 4. S121 多飲/多尿 → 多飲 + 多尿
var_map['S121']['name_ja'] = '多飲'
var_map['S121']['name'] = 'polydipsia'
var_map['S121']['note'] = 'DM/尿崩症(代償性)/心因性多飲/高Ca血症。多尿(S{})とは独立(心因性多飲→多尿は二次的)'.format(sid)
added.append({'id':f'S{sid}','name':'polyuria','name_ja':'多尿',
    'category':'symptom','states':['absent','present'],
    'note':'DM(浸透圧利尿)/尿崩症(中枢性/腎性)/高Ca/リチウム/利尿薬。多飲(S121)なしの多尿=尿崩症を強く示唆'})
print(f'S121 → 多飲 + S{sid} 多尿')
sid += 1

# 5. S114 不安/焦燥 → 不安 + 焦燥
var_map['S114']['name_ja'] = '不安'
var_map['S114']['name'] = 'anxiety'
var_map['S114']['note'] = '主観的不安感。甲状腺機能亢進/褐色細胞腫/パニック障害/PE/低血糖/離脱症状'
added.append({'id':f'S{sid}','name':'agitation','name_ja':'焦燥・興奮',
    'category':'symptom','states':['absent','present'],
    'note':'客観的な運動性不穏。せん妄/アルコール離脱/甲状腺クリーゼ/抗NMDA受容体脳炎/低血糖/中毒。不安(S114)なしの焦燥=せん妄を示唆'})
print(f'S114 → 不安 + S{sid} 焦燥・興奮')
sid += 1

# 6. S58 飛蚊症/光視症 → 飛蚊症 + 光視症
var_map['S58']['name_ja'] = '飛蚊症'
var_map['S58']['name'] = 'floaters'
var_map['S58']['note'] = '硝子体混濁/後部硝子体剥離/網膜裂孔(急性増加=emergency)/ぶどう膜炎'
added.append({'id':f'S{sid}','name':'photopsia','name_ja':'光視症',
    'category':'symptom','states':['absent','present'],
    'note':'実際にない光が見える。網膜牽引(網膜剥離前駆)/片頭痛前兆/後頭葉病変。飛蚊症(S58)とは独立のメカニズム'})
print(f'S58 → 飛蚊症 + S{sid} 光視症')
sid += 1

# 7. S38 陰嚢腫脹・疼痛 → 陰嚢腫脹 + 陰嚢疼痛
var_map['S38']['name_ja'] = '陰嚢腫脹'
var_map['S38']['name'] = 'scrotal_swelling'
var_map['S38']['note'] = '水瘤/精索静脈瘤/精巣腫瘍(無痛性!)/鼠径ヘルニア。疼痛(S{})の有無で鑑別が変わる'.format(sid)
added.append({'id':f'S{sid}','name':'scrotal_pain','name_ja':'陰嚢疼痛',
    'category':'symptom','states':['absent','present'],
    'note':'精巣捻転(急性激痛=emergency)/精巣上体炎/精索静脈瘤(鈍痛)。腫脹(S38)なしの疼痛=捻転早期/関連痛'})
print(f'S38 → 陰嚢腫脹 + S{sid} 陰嚢疼痛')
sid += 1

# 8. L34 便培養/CDトキシン → 便培養 + CDトキシン
var_map['L34']['name_ja'] = '便培養'
var_map['L34']['name'] = 'stool_culture'
var_map['L34']['states'] = ['not_done', 'normal', 'pathogen_detected']
var_map['L34']['note'] = 'Salmonella/Campylobacter/Shigella/EHEC等。CDトキシンはL{}で別検査'.format(lid)
added.append({'id':f'L{lid}','name':'cd_toxin','name_ja':'CDトキシン検査',
    'category':'lab','states':['not_done','negative','positive'],
    'note':'Clostridioides difficile感染症の確定検査。抗菌薬使用後の下痢で検査。便培養(L34)とは別'})
print(f'L34 → 便培養 + L{lid} CDトキシン')
lid += 1

# 9. S44 出血傾向 → 粘膜出血に限定rename (S126鼻出血, E12紫斑は既に別にある)
var_map['S44']['name_ja'] = '粘膜出血(歯肉出血等)'
var_map['S44']['name'] = 'mucosal_bleeding'
var_map['S44']['note'] = '歯肉出血/口腔内出血/消化管出血前駆。S126(鼻出血), E12(紫斑/点状出血)とは独立。血小板減少/DIC/凝固障害/VitK欠乏/肝不全'
print(f'S44 → 粘膜出血(歯肉出血等) (S126鼻出血, E12紫斑は既存)')

# ============================================================
# RENAMES — name cleanup only
# ============================================================

# S15: 側腹部痛・腰背部痛 → 側腹部痛 (S111 腰痛 already exists)
var_map['S15']['name_ja'] = '側腹部痛'
var_map['S15']['name'] = 'flank_pain'
var_map['S15']['note'] = '腎結石/腎盂腎炎/腎梗塞/AAA/後腹膜病変。腰痛(S111)とは区別: 側腹部=腎/尿管由来が多い'
print(f'S15 → 側腹部痛 (S111腰痛は既存)')

# S53: already binary+satellite. Name just descriptive
var_map['S53']['name_ja'] = '言語障害'
var_map['S53']['name'] = 'speech_language_disorder'
var_map['S53']['note'] = '構音障害/失語を含む。種類はS94 satelliteで記録。脳梗塞/脳出血/脳腫瘍/ALS/MS'
print(f'S53 → 言語障害')

# R10: redundant with R28/R42/R56 → rename to other devices
var_map['R10']['name_ja'] = 'その他の体内デバイス(ステント/人工血管/シャント等)'
var_map['R10']['name'] = 'other_implanted_device'
var_map['R10']['note'] = '人工弁(R28)/人工関節(R42)/ペースメーカー(R56)以外の体内デバイス。冠動脈ステント/人工血管/VPシャント/透析シャント'
print(f'R10 → その他の体内デバイス')

# E33: 脈拍左右差/血管雑音 — both vascular exam findings, keep together
# but add note clarifying
var_map['E33']['note'] = '脈拍左右差=大動脈解離/鎖骨下動脈狭窄/大動脈縮窄, 血管雑音=頸動脈狭窄/腎動脈狭窄/AVM。両方とも血管診察所見'
print(f'E33 → note updated (統合OK)')

# ============================================================
# STATE EXPANSIONS
# ============================================================

# R25 HIV陽性/AIDS → expand states
var_map['R25']['name_ja'] = 'HIV感染状態'
var_map['R25']['name'] = 'hiv_status'
var_map['R25']['states'] = ['negative', 'hiv_positive_controlled', 'hiv_positive_uncontrolled', 'aids']
var_map['R25']['note'] = 'controlled=ART中でウイルス抑制, uncontrolled=未治療/治療失敗, AIDS=CD4<200。日和見感染リスクが段階的に異なる'
print(f'R25 → HIV感染状態 (4 states)')

# R40 悪性腫瘍の既往/治療中 → expand states
var_map['R40']['name_ja'] = '悪性腫瘍の状態'
var_map['R40']['name'] = 'malignancy_status'
var_map['R40']['states'] = ['no', 'history_remission', 'active_on_treatment', 'active_untreated']
var_map['R40']['note'] = '既往寛解=再発リスク, 治療中=免疫抑制/腫瘍崩壊リスク, 未治療活動性=paraneoplastic/圧迫/浸潤'
print(f'R40 → 悪性腫瘍の状態 (4 states)')

# R44 心疾患既往 → split into HF and IHD
var_map['R44']['name_ja'] = '心不全の既往'
var_map['R44']['name'] = 'history_heart_failure'
var_map['R44']['note'] = 'うっ血性心不全の既往。容量負荷/肺うっ血/浮腫リスク。虚血性心疾患(R{})とは独立'.format(rid)
added.append({'id':f'R{rid}','name':'history_IHD','name_ja':'虚血性心疾患の既往',
    'category':'risk','states':['no','yes'],
    'note':'心筋梗塞/狭心症の既往。ACS再発リスク/抗血小板薬使用中。心不全(R44)とは独立'})
print(f'R44 → 心不全既往 + R{rid} 虚血性心疾患既往')
rid += 1

# ============================================================
# Save
# ============================================================
for a in added:
    a.setdefault('severity', 'medium')
    if a['id'] not in existing_ids:
        s1['variables'].append(a)
        existing_ids.add(a['id'])

json.dump(s1, open(os.path.join(BASE, 'step1_fever_v2.7.json'), 'w'), ensure_ascii=False, indent=2)

# Check
ids = [v['id'] for v in s1['variables']]
dupes = set(x for x in ids if ids.count(x) > 1)
print(f'\nAdded: {len(added)} new variables')
print(f'Total: {len(s1["variables"])}')
print(f'Duplicates: {dupes if dupes else "None"}')
