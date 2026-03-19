---
name: disease_split_plan
description: 疾患リスト分割計画 — A群+B群完了(12分割)。C群/D群は低優先。
type: project
---

# 疾患リスト分割計画

umbrella疾患を臨床的に独立したIDに分割。

**Why:** 1IDに異なる疾患を同居させると、辺/CPTが「平均」になり鑑別力が落ちる。分割すれば各疾患の特異的プロファイルが活きる。

**How to apply:** 分割時は以下を守る：
1. 元の疾患IDは維持（既存案例を壊さない）
2. 分割先の新IDにreal caseを検索して追加
3. 既存案例のexpected_idを適切に再マッピング
4. 辺/CPTは元から独立に再設計（コピーではなく疾患特異的に）
5. 競合疾患のprior公平性を確認
6. **noisy_or_params必須**: 新疾患にはedge targetのnoisy_or_params parent_effectsを必ず追加

## A群（完了）— 2026-03-17

| 元ID | 分割結果 | 新ID |
|------|---------|------|
| D77 | PE + DVT | D355 |
| D63 | クローン + UC | D353 |
| D67 | NHL + HL | D354 |
| D128 | 喉頭蓋炎 + 異物 | D358 |
| D37 | Campy + Salm + Shig | D351,D352 |
| D125 | AF + SVT + VT | D356,D357 |

## B群（完了）— 確認 2026-03-19

| 元ID | 分割結果 | 新ID |
|------|---------|------|
| D61 | PMR + GCA | D359 |
| D65 | 痛風 + CPPD | D360 |
| D106 | DM + PM | D361 |
| D29 | 細菌性 + アメーバ性肝膿瘍 | D362 |
| D108 | 急性HBV + 慢性HBV | D363 |
| D24 | 黄色ブ菌TSS + iGAS | D364 |

## C群（低優先度） / D群（広範カテゴリ）
省略（前回のまま）
