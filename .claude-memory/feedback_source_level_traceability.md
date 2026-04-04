---
name: 情報源レベル追跡の鉄律
description: 全辺に文献根拠必須。辺根拠(source_edge)とCPT根拠(source_cpt)を分離記録。降級源は明示標記。CPT値は実数カウント(n/N)必須。
type: feedback
---

## 鉄律

**全ての辺(edge)に以下の2層の文献根拠を記録する:**

### source_edge（辺の存在根拠）
- **pmid** — 文献のPMID
- **type** — `SR`(Systematic Review) / `NR`(Narrative Review) / `TB`(Textbook) / `CS`(Case Series)

### source_cpt（CPT値の根拠）
- **pmid** — 頻度データの出典（source_edgeと同一文献の場合もある）
- **type** — 同上
- **excerpt** — **実数カウントを含む原文摘録**（例: "rash in 45/59 (76%)"）

辺の存在根拠とCPT値の根拠は別の文献から来ることがある。両方を個別に記録する。

## 情報源優先順位

**SR > NR > TB > CS**

- Systematic Reviewを最優先で探す
- 見つからない場合は降級 → **typeフィールドで明示**
- 降級した辺は将来の優先審査対象

## CPT値は実数カウント(n/N)必須

- 定性描述（"common", "rare", "frequent"等）からの主観的変換は**禁止**
- SRに頻度なし → SRの引用文献を追い、頻度データのある原始研究を探す
- SRもNRもない稀少疾患 → 最大サンプルのcase seriesから頻度を取得
- excerptには必ず n/N または百分率+サンプルサイズを含めること

## 根拠

- 情報源は「宁愿多不能少」（多すぎて困ることはない）
- CPT値の信頼度は情報源の質に直結する
- 降級源の辺は将来SRが出版された時に優先的にアップデートできる
- 全環節貫通: 大清洗だけでなく、今後の全ての辺追加作業にも適用
