---
name: 統一推奨（Rank Fusion）実装計画
description: 確認推奨(IG)と反証推奨(max H_after)をBorda count rank fusionで統合する。Top-5一致数を診断成熟度信号として表示。
type: project
---

## 背景
- 確認推奨: IG = H_now - E[H|v] → 期待値最適（理論的に最適な単一指標）
- 反証推奨: max_s(H_after(v=s)) → 最悪ケース最適（minimax視角）
- 両者が一致する検査 = 情報論的最強（確認でも反証でもトップ）

## 実験結果 (2026-03-18)
| 場景 | H(bits) | Top-5一致 | 統一Top-1 | 意味 |
|------|---------|-----------|-----------|------|
| R01 Still病 (9 ev) | 0.55 | 2件 | L15 フェリチン (確認#1, 反証#1) ★ | 一発で決まる |
| PMC11706331 HLH (12 ev) | 2.58 | 0件 | L04 胸部X線 (確認#7, 反証#5) | 鑑別散在 |
| PMC11706331 HLH early (6 ev) | 6.26 | 0件 | L16 LDH (確認#7, 反証#1) | まだ序盤 |

## 核心発見
1. **Top-5一致数は診断成熟度信号**: 一致多→決定的検査あり、一致少→鉴別散在
2. **Rank Fusion（Borda count: rank_ig + rank_fals）が最もバランス良い**
3. **IG単独は既にEIG（理論最適）だが、反証の尾部リスク情報を捕捉しない**

## 実装方針
- 主ランキング: Rank Fusion (確認rank + 反証rank の和、小さい方が上位)
- 各検査に確認方向(best_state)と反証方向(disruptive_state)を併記
- Top-5両方一致の検査に★マーク
- 一致度をUI上に「診断成熟度」として表示
- プロトタイプ: `test_unified_recommendation.py` (コミット済み)

## PMCテスト案例
- PMC11706331: 78F HLH caused by DLBCL
  - evidence: E01=38.0_39.0, T01=over_3w, T02=chronic, S07=severe, E14=present, E36=present, L01=normal_4000_10000, L02=moderate_3_10, L15=very_high_over_1000, L16=elevated, L28=elevated, L100=low_50k_150k
  - risk: R01=65_plus, R02=female
  - expected: D107 (rank 4, 10.9%)

## TODO
- [ ] `bn_inference.py` に `unified_recommendation()` を正式統合
- [ ] `app.py` のAPI `/api/next_best_test` に統一ランキング追加
- [ ] UI（index.html）を統一ビューに改修
- [ ] PMC11706331案例をreal_case_test_suiteに正式追加
