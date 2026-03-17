---
name: 変量審計パイプライン実験
description: 外部AI生成の227新変量+fix脚本の導入。CPT_NO_EDGE同期問題の発見と修正
type: project
---

## 変量審計パイプライン (experiment/variable-audit-pipeline)

**日付**: 2026-03-17

### 導入内容
- 外部AIとの対話で生成された変量審計パイプライン（5フェーズ）
- Phase 2: 8複合変量を原子化分割（味覚/嗅覚、多飲/多尿等）
- Phase 5: 辺数最少の70+疾患にbatch辺追加
- 結果: 565→792変量(+227), 5025→5462辺(+437)

### 発見された問題: CPT_NO_EDGE不同期
- fix脚本がstep3にCPTを書いたがstep2に辺を書き忘れた
- 507条のCPT_NO_EDGE（卫星変量S83-S94, E46-E50等）
- 一括同期で修正 → Top-1 +7

### 未使用の新変量
- 93個の非疾患変量（14 lab + 25 sign + 54 symptom）が零辺+零CPT
- テスト案例に1つも使われていないため、現時点では性能に影響なし
- 将来的にevidenceで使い始めたら辺+CPTが必要

**Why:** 外部AIツールとの連携時はstep2/step3の同期を必ず検証する必要がある
**How to apply:** 新変量/辺の一括導入後は`CPT_NO_EDGE`と`EDGE_NO_CPT`の両方向チェックを実施
