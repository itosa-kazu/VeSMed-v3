---
name: Evidence追加前に辺の整備を確認
description: 案例にevidenceを追加する前に、期待疾患がその変量への辺を持っているか確認必須。辺なしのevidenceはleak値で不利になる。
type: feedback
---

**案例にevidenceを追加する前に、期待疾患がその変量への辺+適切なCPTを持っているか必ず確認。**

**Why:** 2026-03-16にD252+の案例に112件のevidenceを一括自動追加したところ、Top-1が501→496(-5)に悪化。原因: 追加したevidence変量(L11等)に対して期待疾患の辺がないかCPTが弱く、競合疾患に負けた。

**例:** R669(横紋筋融解D330)にL11=very_high(AST上昇)を追加→D330→L11のCPTよりD108(B型肝炎)→L11のCPTが強い→D108が浮上してD330がrank1から脱落。

**How to apply:**
1. evidence追加前に `disease_children[expected_id]` にその変量があるか確認
2. 辺があっても、CPT値が競合疾患より弱くないか確認
3. 辺がなければ先に辺を追加してからevidenceを追加
4. 一括自動追加ではなく、1変量ずつ慎重に
