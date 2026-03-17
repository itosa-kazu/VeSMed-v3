---
name: 辺監査は必ずskillで実施
description: 辺監査は毎回/edge-auditスキルを使って実施すること。手動で雑にやらない。
type: feedback
---

辺監査は**必ず `/edge-audit` スキルのワークフローに従って**実施すること。

**Why:** 2026-03-16に3轮辺監査を手動で68辺追加したが、skill流程の「優先度分類(rank別)」「過拟合チェック(案例がなくてもこの辺を追加するか？)」が不十分だった。雑な辺追加は過拟合リスクを増大させる。

**How to apply:**
1. `/edge-audit` を呼び出す
2. Step 1: 漏れ辺検出（rank>=2の全案例）
3. Step 2: 優先度分類（rank 2-3 = Top-1直結、rank 4-5 = Top-3直結、6+ = 低優先）
4. Step 3: **各ペアで臨床判断** — 「この案例がなくても追加するか？」をYes/Noで判定
5. Step 4: 三位一体確認（EDGE_NO_CPT / CPT_NO_EDGE = 0）
6. Step 5: 回帰テスト + commit

手動で雑にやると過拟合する。skillで統制する。
