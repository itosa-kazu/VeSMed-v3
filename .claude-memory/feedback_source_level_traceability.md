---
name: 情報源レベル追跡の鉄律
description: 全ての辺にPMID+情報源レベル(SR/NR/TB)+原文excerptを必須記録。降級源は明示的に標記。全環節貫通。
type: feedback
---

## 鉄律

**全ての辺(edge)に以下を必須記録する:**

1. **pmid** — 文献のPMID（定位可能）
2. **type** — 情報源レベル: `SR`(Systematic Review) / `NR`(Narrative Review) / `TB`(Textbook)
3. **excerpt** — CPT値の根拠となる原文摘録（例: "fever 95% (95%CI 92-97%, n=1203)"）

## 優先順位

**SR > NR > TB**

- Systematic Reviewを最優先で探す
- 見つからない場合はNRまたはTBに降級 → **typeフィールドで明示**
- 降級した辺は将来の優先審査対象

## 根拠

- 情報源は「宁愿多不能少」（多すぎて困ることはない）
- CPT値の信頼度は情報源の質に直結する
- 降級源の辺は将来SRが出版された時に優先的にアップデートできる
- 全環節貫通: 大清洗だけでなく、今後の全ての辺追加作業にも適用
