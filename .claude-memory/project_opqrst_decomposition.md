---
name: OPQRST多維度症状建模
description: 症状(胸痛/頭痛/腹痛等)をOPQRSTの各次元に分解して独立変数にすべき。現在のS21は性質と誘発因子が混在。
type: project
---

## 問題
S21(胸痛)のstates(absent/pleuritic/constant)はQuality(性質)とProvocation(誘発因子)が混在。
実臨床ではburning+worsened_by_breathingが共存しうるが、現モデルでは1つしか選べない。

## 解決方針: OPQRST分解
各主要症状を独立次元に分解:
- **Quality(性質):** burning / sharp / pressure / tearing
- **Provocation(誘発因子):** exertion / breathing / position / meals / none
- **Radiation(放散):** none / left_arm_jaw / back / bilateral

### 疾患ごとの典型パターン
| 疾患 | Quality | Provocation | Radiation |
|------|---------|-------------|-----------|
| ACS | pressure | exertion | left_arm_jaw |
| 大動脈解離 | tearing | none(最初から最大) | back |
| GERD | burning | meals | none |
| 心膜炎 | sharp | position(前傾改善) | none |
| 肋軟骨炎 | sharp | breathing/movement | none |
| PE | sharp | breathing | none |
| 気胸 | sharp | breathing | none |

### 実装状況
- 胸痛(S21): 方案A実装済み → S21(quality) + S50(provocation) + S51(radiation)に分解
- 頭痛(S05): 未着手(将来)
- 腹痛(S12): 既にlocation分離済み(将来quality/provocation追加)
- 背部痛(S22): 未着手(将来)

### 原則
全ての主要症状は最終的にOPQRST分解すべき。ただし一度に全部やると影響大きいので段階的に。
