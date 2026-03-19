---
name: add-diseases
description: VeSMed疾患追加の完全ワークフロー。文献根拠必須・競合検証必須。宁慢勿错。
---

# 疾患追加ワークフロー

$ARGUMENTS に疾患名リスト（日本語）が渡される。なければ疾患リスト.txtから次の候補を選ぶ。

## 原則: 宁慢勿错

**速度よりも臨床的正確性を最優先する。** 辺1本のCPTが間違うと、その疾患の全案例に永続的に影響する。LLMの印象で書いたCPTは必ず文献で検証してから投入する。

## 完全サイクル（省略禁止）

### Step 0: 臨床プロファイル調査（**新設・最重要**）

**疾患モデルを作る前に、まず文献でその疾患の臨床像を把握する。**

1. **WebSearchでreview article/教科書を検索**:
   - `"{disease} clinical features frequency"` or `"{disease} clinical manifestations review"`
   - UpToDate/Harrison's/Mandell's等の教科書記載も可
2. **原文をWebFetchで取得**し、以下を抽出:
   - 主要症状と**各症状の出現頻度(%)**
   - 主要検査所見と**異常値の頻度(%)**
   - 年齢・性別分布（疫学）
   - 鑑別診断リスト
3. **抽出結果を一覧表にまとめてからStep 1に進む**

```
例: 急性C型肝炎
| 所見 | 頻度 | 出典 |
|------|------|------|
| ALT >10xULN | 95% | Harrison's Ch.340 |
| 黄疸 | 20-30% | PMC3794154 |
| 倦怠感 | 60-80% | Mandell's |
| 発熱 | 20-30% | UpToDate |
```

**この表が辺リスト+CPT値の根拠になる。表なしでStep 1に進むことは禁止。**

### Step 1: 疾患モデル作成（文献ベース）

- **重複チェック（必須）**: 既存疾患と同名/類似名がないか確認
- step1に変数定義（id, name, name_ja, category, states, severity, note）
- step2に辺を追加。**各辺のreason欄に出典と頻度を記載**:
  - 良い例: `"急性HCV: 黄疸(20-30%, Harrison's Ch.340)"`
  - 悪い例: `"急性HCV: 黄疸"`
- **最低10辺以上**。鑑別力のある辺を優先（正常値辺は不要）
- **辺のfrom_nameは同一disease IDの既存辺からコピー**（手動入力禁止）
- step3にCPT（leak + parent_effects）を追加
  - **CPT値はStep 0の頻度表から直接設定**。LLMの印象値は禁止
  - **full_cptにR01(年齢)とR02(性別)を必ず追加（必須・省略禁止）**
  - **CPTの機械的一括変換は禁止**。各CPTは臨床根拠に基づき手動設計
- **検査値変量にnot_doneステートは禁止**
- **三位一体**: step1/step2/step3は必ず同時更新

### Step 1.5: 競合疾患検証（**新設**）

新疾患追加後、**最も混淆しやすい既存疾患3-5件**を特定し、鑑別力を検証する。

1. **競合疾患の特定**: 同じ主訴(発熱+黄疸等)を共有する既存疾患をリストアップ
2. **辺の差分比較**: 新疾患 vs 各競合で、辺集合の差分を確認
   - 差分が2辺以下 → 鑑別力不足。新疾患の特異的辺を追加するか、競合にも辺を追加
3. **CPT値の差分確認**: 共通辺のCPT値が区別可能か（例: HCV黄疸28% vs HAV黄疸70%）
4. **Prior公平性**: 新疾患と競合のR01/R02 priorが適切か確認

### Step 1.7: 新変量追加時の全疾患照合（新変量がある場合のみ）

- 新変量を追加した場合、**全疾患リストと手動照合**して辺の漏れを確認
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
- `python bn_inference.py` で新案例テスト
- FATALがあれば辺追加で解消（OOS逃避禁止）

### Step 5: 辺監査
- rank 2以上の全案例で漏れ辺を検出:
```python
missing = {v for v in (set(ev.keys()) - edge_map.get(expected, set()))
           if not v.startswith("R")}
```
- 臨床的に妥当な辺のみ追加（過拟合禁止）
- **追加する辺にもWebSearch文献根拠が必要**（edge-audit skillと同じ基準）
- EDGE_NO_CPT / CPT_NO_EDGE が0であることを確認

### Step 6: commit push
- git add + commit + push
- commitメッセージに: 疾患数、辺数、案例数、Top-1、Top-3、FATAL

### Step 7: 欠失変量の記録
- FATALが辺追加で解決できない場合、鑑別に必要な変量が欠けている可能性
- 発見したら `memory/project_missing_variables.md` に記録
- 変量追加が可能な場合はその場で追加

## 疾患混在禁止ルール
- **1つのIDに臨床的に異なる疾患を同居させない**
- 疫学(年齢/性別分布)、主要症状、治療法が異なるなら別IDに分割
- 例: DVT/PEは別疾患、IBDはクローン/UCに分割
- umbrella疾患を見つけたら分割を検討
- 分割時はPrior分割: P(combined) ≈ P(sub1) + P(sub2)

## 鉄則チェックリスト
- [ ] **Step 0の臨床プロファイル表を作成済み（文献出典あり）**
- [ ] step1/step2/step3 三位一体
- [ ] **全辺のreason欄に出典+頻度が記載されている**
- [ ] **full_cptにR01(年齢7区分)とR02(性別)を必ず追加（必須）**
- [ ] **競合疾患3-5件との鑑別力を検証済み**
- [ ] 案例検索agent起動済み
- [ ] validate_cases.py ERROR 0
- [ ] EDGE_NO_CPT = 0, CPT_NO_EDGE = 0
- [ ] `python3 validate_edges.py` のエラー数が増加していないこと
- [ ] 回帰テストでFATAL 0
- [ ] 欠失変量があればmemory記録
- [ ] commit push済み
