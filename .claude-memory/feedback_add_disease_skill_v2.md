---
name: add-diseases skill V2起点
description: 文献検証必須の新add-diseases skillはD370(再生不良性貧血)から適用。D368/D369は旧skillで追加後に遡及修正。
type: feedback
---

add-diseases skill V2(Step 0文献調査+競合検証+辺出典強制)の適用起点:
- **D370以降**: 新skill適用（最初からStep 0で文献調査してからモデル作成）
- **D368(急性HCV), D369(HEV)**: 旧skillで追加→遡及的に文献検証してCPT修正済み
- **D367以前**: 旧skillで追加。CPTはLLM印象値の可能性あり、未検証

**Why:** 旧skillではLLM印象でCPT値を設定していた。HCV検証でCRP正常(重大発見)、HEV肝腫大10%なのに40%設定等の重大エラーを発見。

**How to apply:** D367以前の疾患のCPTを修正する際は、文献検証を優先的に実施すべき。特に辺監査で触る疾患は同時にCPT値も文献照合する。
