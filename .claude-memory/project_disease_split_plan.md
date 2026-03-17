---
name: disease_split_plan
description: 疾患リスト分割計画 — umbrella疾患を臨床的に独立したIDに分割するプロジェクト。A群完了。
type: project
---

# 疾患リスト分割計画

345→353疾患。umbrella疾患を臨床的に独立したIDに分割。

**Why:** 1IDに異なる疾患を同居させると、辺/CPTが「平均」になり鑑別力が落ちる。分割すれば各疾患の特異的プロファイルが活きる。

**How to apply:** 分割時は以下を守る：
1. 元の疾患IDは維持（既存案例を壊さない）
2. 分割先の新IDにreal caseを検索して追加
3. 既存案例のexpected_idを適切に再マッピング
4. 辺/CPTは元から独立に再設計（コピーではなく疾患特異的に）
5. 競合疾患のprior公平性を確認
6. **noisy_or_params必須**: 新疾患にはedge targetのnoisy_or_params parent_effectsを必ず追加

## A群（完了）— 2026-03-17

| 元ID | 分割結果 | 新ID | 案例 | 結果 |
|------|---------|------|------|------|
| D77 | PE + DVT | D355 | +1 DVT | PE全4案例Top-1 |
| D63 | クローン + UC | D353 | +2 UC | R740 Top-1, R741 miss(FUO) |
| D67 | NHL + HL | D354 | +2 HL | R742 Top-1, R743 rank2 |
| D128 | 喉頭蓋炎 + 異物, R226→D185 | D358 | +2 epi | R745/R746 Top-1 |
| D37 | Campy + Salm + Shig | D351,D352 | — | 案例追加必要 |
| D125 | AF + SVT + VT | D356,D357 | — | R208/R209 Top-1 |

**教訓**: 新疾患は必ずnoisy_or_params parent_effectsが必要。edgeだけでは推論不能。

## B群（中優先度）— 未着手

| 元ID | 現在の名称 | 分割案 |
|------|-----------|--------|
| D61 | PMR/GCA | PMR + GCA |
| D65 | 痛風/偽痛風 | 痛風 + 偽痛風(CPPD) |
| D106 | DM/PM | 皮膚筋炎 + 多発性筋炎 |
| D29 | 肝膿瘍 | 細菌性 + アメーバ性 |
| D108 | B型肝炎 | 急性HBV + 慢性HBV増悪 |
| D24 | TSS/劇症型GAS | 黄色ブ菌TSS + 劇症型GAS |

## C群（低優先度） / D群（広範カテゴリ）
省略（前回のまま）
