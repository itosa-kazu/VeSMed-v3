---
name: edge-audit
description: VeSMed辺監査。全案例のrank2+で漏れ辺を検出し、臨床的に妥当な辺を一括追加。Top-1/Top-3改善の最強手法。
---

# 辺監査ワークフロー

## Step 1: 漏れ辺検出

全in-scope案例でrankを計算し、rank>=2の案例について:
- expected_diseaseのedge集合とevidence変数集合を比較
- evidenceにあるのにedgeがない(disease, variable)ペアを全て列挙

```python
missing = set(ev.keys()) - edge_map.get(expected, set())
```

## Step 2: 優先度分類

| 優先度 | rank | 影響 |
|--------|------|------|
| 最高 | 4-5 | Top-3に直結 |
| 高 | 2-3 | Top-1に直結 |
| 中 | 6-10 | MISS改善 |
| 低 | 11+ | 深層改善 |

## Step 3: 臨床判断で追加

各(disease, variable)ペアについて:
1. 「この疾患はこの所見を本当に引き起こすか？」→ Yes/No
2. 「頻度は？」→ CPT値設定
3. 「この案例がなくてもこの辺を追加するか？」→ 過拟合チェック

**追加禁止のパターン:**
- T01/T02が案例データの入力ミスで欠けている場合 → 案例修正が正解
- L09=negative/L10=negative → 他の類似疾患にも同じ辺を追加すること（公平性）
- 特殊変量(E15心雑音/E22口蓋垂偏位等) → 本当に必要か慎重判断

## Step 4: 三位一体確認

```python
# EDGE_NO_CPT と CPT_NO_EDGE が両方0であること
```

## Step 5: 回帰テスト + commit

$ARGUMENTS が指定されれば、そのrankのみ対象。指定なければ全rank。
