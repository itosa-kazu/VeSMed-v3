---
name: δMed鑑別力指標: max|logLR|
description: δMedの変量ランキングをTVDからmax|logLR|に変更。LR≥2有用/LR<1.5陷阱。Oxford CEBM準拠。
type: project
---

## 指標変更 (2026-04-03)
- **旧**: TVD (Total Variation Distance) — 全state差異の合計。臨床直感と乖離
- **新**: max|log(LR)| — 各stateの尤度比の最大値。臨床医の思考と一致

## 閾値 (Oxford CEBM準拠)
- **有用**: max|logLR| ≥ 0.7 (LR ≥ 2.0) — "有一定鑑別価値"の下限
- **陷阱**: max|logLR| < 0.4 (LR < 1.5) — "ほぼ無用"
- 根拠: Oxford CEBM + McGee JAMA Rational Clinical Examination

## CEBM LR分級
| LR | 臨床意義 |
|---|---|
| >10 | rule in級 |
| 5-10 | 中等度有用 |
| 2-5 | 一定の価値 |
| 1-2 | ほぼ無用 |
| <0.1 | rule out級 |

## 臨床的思考との対応
- 「この所見を見たら、AとBの判断がどれだけ変わるか？」= LR
- TVDは全stateを平等に扱い、「1つの決定的state」を評価できない
- max|logLR|は「最も鑑別力の高いstate」に注目 — 臨床直感と一致

**Why:** VeSMed推理引擎(Noisy-OR + log-LR)と同じ思想でδMedの学習指標を統一
**How to apply:** vesmed_export.pyのextract_differential_featuresでmax|logLR|を計算。divergenceフィールドに格納
