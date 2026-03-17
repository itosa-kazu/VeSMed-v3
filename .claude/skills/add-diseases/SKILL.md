---
name: add-diseases
description: VeSMed疾患追加の完全ワークフロー。5疾患ずつ追加→案例検索→テスト→辺監査→commit pushの完全サイクル。
---

# 疾患追加ワークフロー

$ARGUMENTS に疾患名リスト（日本語）が渡される。なければ疾患リスト.txtから次の候補を選ぶ。

## 完全サイクル（省略禁止）

### Step 1: 疾患モデル作成
- **重複チェック（必須）**: 既存疾患と同名/類似名がないか確認。5組重複で性能低下した教訓
- step1に変数定義（id, name, name_ja, category, states, severity, note）
- **検査値変量にnot_doneステートは禁止**（推理エンジンが未観測変量を辺縁化で処理するため冗余）
- 検査値変量のstate設計は因材施教: まず変量固有の黄金分級を文献検索、なければCTCAE準拠4-state(xULN基準)をfallback
- step2に辺（disease→所見変数）を追加。**最低10辺以上**。鑑別力のある辺を優先（正常値辺は不要）
- step3にCPT（leak + parent_effects）を追加。full_cptにR01/R02を含める（性差/年齢差がある場合）
- **三位一体**: step1/step2/step3は必ず同時更新

### Step 1.5: 新変量追加時の全疾患照合（新変量がある場合）
- 新変量を追加した場合、**全345疾患のリストと手動照合**して辺の漏れを確認
- 各疾患のnoteを読み「この疾患がこの変量の値を直接引き起こすか？」を判断
- YESなら辺+CPTを追加。parent≧3になるまで繰り返す
- **間接因果(転移/DIC/ショック経由)は直接辺にしない** → 中間変量(L63方式)を検討

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

## 疾患混在禁止ルール
- **1つのIDに臨床的に異なる疾患を同居させない**
- 疫学(年齢/性別分布)、主要症状、治療法が異なるなら別IDに分割
- 例: DVT/PEは別疾患（下肢腫脹 vs 呼吸困難）、IBDはクローン/UCに分割
- umbrella疾患を見つけたら分割を検討（辺/CPTが「平均」になり鑑別力低下の原因）
- 分割時はPrior分割: P(combined) ≈ P(sub1) + P(sub2)

## 鉄則チェックリスト
- [ ] step1/step2/step3 三位一体
- [ ] full_cptにR01/R02（性差/年齢差がある場合）
- [ ] 案例検索agent起動済み
- [ ] validate_cases.py ERROR 0
- [ ] EDGE_NO_CPT = 0, CPT_NO_EDGE = 0
- [ ] 回帰テストでFATAL 0
- [ ] 欠失変量があればmemory記録
- [ ] commit push済み
