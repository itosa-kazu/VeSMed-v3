---
name: add-diseases
description: VeSMed疾患追加の完全ワークフロー。5疾患ずつ追加→案例検索→テスト→辺監査→commit pushの完全サイクル。
---

# 疾患追加ワークフロー

$ARGUMENTS に疾患名リスト（日本語）が渡される。なければ疾患リスト.txtから次の候補を選ぶ。

## 完全サイクル（省略禁止）

### Step 1: 疾患モデル作成
- step1に変数定義（id, name, name_ja, category, states, severity, note）
- step2に辺（disease→所見変数）を追加。**最低10辺以上**
- step3にCPT（leak + parent_effects）を追加。full_cptにR01/R02を含める（性差/年齢差がある場合）
- **三位一体**: step1/step2/step3は必ず同時更新

### Step 2: 回帰テスト
- `python bn_inference.py` で全案例テスト
- Top-1/Top-3/FATALを確認
- **Top-3が前回より2%以上低下したら辺監査（Step 5）を先に実施**

### Step 3: 案例検索（**絶対省略禁止**）
- 各疾患ごとにPMCからreal case reportを**3件以上**検索
- Agent toolでバックグラウンド検索を並列実行
- **案例検索を飛ばして次の疾患に進むことは絶対禁止**
- 見つかった案例は全て使う（3件以上あれば全部追加）

### Step 4: 案例追加+テスト
- real_case_test_suite.jsonに追加
- `python validate_cases.py` でERROR 0を確認
- `python bn_inference.py --case R*** R*** ...` で新案例テスト
- FATALがあれば辺追加で解消（OOS逃避禁止）

### Step 5: 辺監査
- rank 2以上の全案例で漏れ辺を検出:
```python
missing = set(ev.keys()) - edge_map.get(expected, set())
```
- 臨床的に妥当な辺のみ追加（過拟合禁止）
- EDGE_NO_CPT / CPT_NO_EDGE が0であることを確認

### Step 6: commit push
- git add + commit + push
- commitメッセージに: 疾患数、辺数、案例数、Top-1、Top-3、FATAL

### Step 7: 欠失変量の記録
- FATALが辺追加で解決できない場合、鑑別に必要な変量が欠けている可能性
- 発見したら `memory/project_missing_variables.md` に記録
- 変量追加が可能な場合はその場で追加（L56 β-hCGのように）

## 鉄則チェックリスト
- [ ] step1/step2/step3 三位一体
- [ ] full_cptにR01/R02（性差/年齢差がある場合）
- [ ] 案例検索agent起動済み
- [ ] validate_cases.py ERROR 0
- [ ] EDGE_NO_CPT = 0, CPT_NO_EDGE = 0
- [ ] 回帰テストでFATAL 0
- [ ] 欠失変量があればmemory記録
- [ ] commit push済み
