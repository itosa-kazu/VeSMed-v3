---
name: 疾患ID名前衝突問題（未解決）
description: step2辺ファイルに同一疾患IDで異なる疾患の辺が混在している重大なデータ品質問題
type: project
---

## 問題

step2_fever_edges_v4.jsonで、同一の疾患ID（例: D75）に対して**異なる疾患名**の辺が存在する。

### 確認済み重大衝突（25件）

| ID | 主疾患 | 混入疾患 | 混入辺数 |
|----|--------|----------|----------|
| D08 | 膀胱炎 | 胆管炎 | 6 |
| D75 | セロトニン症候群 | DVT/PE | 4 |
| D114 | 多発性骨髄腫 | ヒストプラズマ症 | 4 |
| D04 | 急性咽頭扁桃炎 | 扁桃周囲膿瘍 | 6 |
| D78 | 熱中症 | 蜂窩織炎 | 6 |
| D196 | ジフテリア | 褐色細胞腫 | 2 |
| ... | (他20件) | | |

### validate_edges.py出力
- 923 NAME CONFLICT errors
- 72 ORPHAN CPT warnings

### Root Cause（推定）
1. 辺追加時にfrom_nameフィールドが不正確（別疾患のコピペ）
2. Claude Code辺監査skillが疾患名をreasonから推定してIDを間違える
3. step2の疾患ID→疾患名の正規マッピングが存在しない

### 修復方針
- 923件の一括修正は危険（D75の例のように逆に退化する場合がある）
- 1件ずつ手動で確認して修正が必要
- validate_edges.pyを毎回実行して新規混入を防ぐ

### 既に修正済み
- D147→L05（精巣捻転に尿路感染のCPT）
- D105→L18（パルボB19に薬剤性ループスのANA CPT）

### 防止策
1. validate_edges.pyをcommit前に実行
2. 辺追加時にfrom_nameを疾患IDマスタから引く（手動入力禁止）
3. step1にdisease master listを追加（ID→正式名の1:1マッピング）
