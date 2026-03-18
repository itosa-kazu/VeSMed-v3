---
name: fix-edge-conflicts
description: step2辺の疾患ID名前衝突を修復。validate_edges.pyで検出された923件のNAME CONFLICTを1疾患IDずつ安全に修正。
---

# 辺ID衝突修復ワークフロー

## 背景

step2_fever_edges_v4.jsonで同一の疾患ID（例: D75）に対して**異なる疾患名**の辺が混在している。
原因: 辺追加時にfrom_nameを手動入力し、別疾患のIDを誤って使用した。

**D75の教訓**: 一括修正は危険。「from_nameが間違い」でも「disease IDは正しい」ケースがある。
reason文字列が別疾患名を含んでいても、そのedge自体はID通りの疾患に臨床的に正当な場合がある。

## 衝突の2タイプ

| タイプ | 説明 | 修正方法 |
|--------|------|----------|
| **A: 名前だけ間違い** | from_nameが別疾患名だが、辺自体はdisease IDの疾患に臨床的に妥当 | from_nameを正しい名前に修正するだけ |
| **B: IDが間違い** | 辺自体が別の疾患のもの（reason文も別疾患の臨床理由） | fromを正しいdisease IDに変更 + step3 CPT移動 |

## ワークフロー

### Step 0: 現状把握

```bash
python3 validate_edges.py 2>&1 | grep "NAME CONFLICT" | wc -l
python3 bn_inference.py 2>&1 | grep SUMMARY
```
エラー数と回帰テストのベースラインを記録する。

### Step 1: 1疾患IDを選択

validate_edges.pyの出力から1つの疾患IDを選ぶ。**案例が多い疾患を優先**（影響が大きい）。

```python
# 該当IDの全辺を表示
for e in s2['edges']:
    if e['from'] == 'DXX':
        print(f"  → {e['to']} from_name={e.get('from_name','')} reason={e.get('reason','')[:60]}")
```

### Step 2: タイプ判定（最重要ステップ）

各衝突辺について**臨床的に判断**:

1. **reason文を読む**: 「PE: 頻呼吸」なら明らかにPEの辺
2. **disease IDの正体を確認**: step2の同IDの多数派from_nameから特定
3. **この辺はID通りの疾患に臨床的に妥当か？**:
   - YES → **タイプA**（名前だけ修正）
   - NO → **タイプB**（ID変更が必要）

**判断に迷ったらタイプA扱い**（保守的）。タイプBの誤判定はD75のような退化を起こす。

### Step 3: 修正実行

#### タイプA（名前修正のみ）:
```python
# from_nameを正しい名前に上書き
e['from_name'] = correct_canonical_name
# reasonはそのまま（臨床的に正しいため）
```

#### タイプB（ID変更）:
```python
# 1. step2: fromを正しいIDに変更
e['from'] = correct_disease_id
e['from_name'] = correct_disease_name

# 2. step3: CPTを移動（旧ID→新ID）
# ただし新IDに既にCPTがある場合はスキップ（既存を優先）
if old_did in nop[vid]['parent_effects']:
    if new_did not in nop[vid]['parent_effects']:
        nop[vid]['parent_effects'][new_did] = nop[vid]['parent_effects'][old_did]
    del nop[vid]['parent_effects'][old_did]
```

**タイプBの追加確認**:
- 正しいdisease IDが実在するか？
- 正しいdisease IDに既にその変量への辺があるか？（重複辺禁止）
- 旧IDからCPTを消した後、旧IDの残り辺は正常に動くか？

### Step 4: 検証

```bash
# 1. validate_edges.pyのエラー数が減少したこと
python3 validate_edges.py 2>&1 | grep "NAME CONFLICT" | wc -l

# 2. 回帰テストでゼロ劣化
python3 bn_inference.py 2>&1 | grep SUMMARY
```

**回帰テストが1案例でも悪化したら**:
1. 悪化案例を特定
2. 原因がこの修正に起因するなら**即revert** (`git checkout -- step2*.json step3*.json`)
3. タイプ判定をやり直す（AだったものがBだった、またはその逆）

### Step 5: commit + 次のIDへ

```bash
git add step2_fever_edges_v4.json step3_fever_cpts_v2.json
git commit -m "fix: resolve D?? edge name conflict (TYPE_A/B, N edges fixed)"
```

**バッチサイズ**:
- タイプA（名前修正のみ）: 5-10 ID分をまとめてcommit可能
- タイプB（ID変更）: 1 IDずつcommit（回帰テスト必須）

## 注意事項

### やってはいけないこと
- **全923件を一括修正**: D75の教訓。一度に大量修正すると退化の原因特定が不可能
- **from_nameだけ見てタイプ判定**: reason文と臨床的妥当性を必ず確認
- **CPTの値を変更**: ID移動のみ。CPT値は臨床設計済みなので触らない

### 進捗管理
- 修正したID数とvalidate_edges.pyのエラー数を毎回記録
- 目標: 923 → 0（数セッションに分けて段階的に）

### 優先順位
1. **テスト案例に影響するID** — 案例のexpected_idと衝突IDが一致するもの
2. **parent_effects数が多いID** — CPTへの影響が大きい
3. **from_name差が大きいID** — 完全に別疾患（D114 骨髄腫vsヒストプラズマ）

## タイプ判定のヒント集

| パターン | 判定 | 例 |
|----------|------|-----|
| reason文が別疾患名を含み、臨床的にも別疾患の所見 | **タイプB** | D75→E04 reason="PE: 頻呼吸" → PEの辺 |
| reason文が別疾患名を含むが、ID疾患にも臨床的に妥当 | **タイプA** | D75→E02 reason="セロトニン: 頻脈" → SSにも妥当 |
| from_nameが日本語で、多数派が英語（同一疾患） | **タイプA** | D05 "市中肺炎" vs "community_acquired_pneumonia" |
| from_nameが "CPT_NO_EDGE sync" を含む | 要確認 | 外部スクリプトが生成した辺。ID正否を個別確認 |
| from_nameが "FIXED_from_DXX" を含む | 修正済み | 前回の修正で既にID変更済み。スキップ |
