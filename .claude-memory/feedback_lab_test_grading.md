---
name: 検査値変量の臨床的分級方法論
description: 検査値（γ-GTP, ALP等）を新変量として追加する際、state設計はCTCAE v5.0ベースの4-state分級を採用する。文献根拠あり。
type: feedback
---

## 鉄則：検査値変量のstate設計はCTCAE準拠の臨床分級を使う

新しい検査値変量を追加する際、stateは以下の4段階分級を基本とする：

| State | 定義 | CTCAE対応 |
|-------|------|-----------|
| `normal` | ≤ULN | — |
| `mild_elevated` | >ULN ~ 3x ULN | G1相当 |
| `moderate_elevated` | 3x ~ 10x ULN | G2-G3相当 |
| `markedly_elevated` | >10x ULN | G3-G4相当 |

### 根拠

- **CTCAE v5.0**（NCI公式）は4段階: G1(>ULN~2.5x), G2(>2.5~5x), G3(>5~20x), G4(>20x)
- 臨床肝臓学では簡化3段階: 軽度(<3x), 中等度(3-10x), 重度(>10x)が慣用
- Case reportでG3(5-20x)とG4(>20x)を区別できる記載は稀 → 合併して>10xが実用的
- VeSMedでは `normal` を加えた**4-state**を標準とする

### 適用済み・適用予定の変量

| 変量 | states | ULN参考値 |
|------|--------|-----------|
| γ-GTP | normal / mild / moderate / markedly_elevated | 男≤55, 女≤30 IU/L |
| ALP | normal / mild / moderate / markedly_elevated | 40-130 IU/L |
| (将来) AST/ALT | 同上 | AST: 10-40, ALT: 7-56 IU/L |
| (将来) LDH | 同上 | 120-246 IU/L |

### 例外ケース

- **低値が臨床的に重要な検査**: ALP低下（低フォスファターゼ症）等は `decreased` stateを追加
- **質的検査（陽性/陰性）**: この分級は不適用。ANCA, 抗GBM抗体等は `not_done/negative/positive` 等
- **特殊な閾値がある検査**: トロポニン（正常/borderline/elevated）等は疾患特異的に設計

### PMC文献ソース

- PMC8735790: GGT特性 in different liver diseases
- PMC9972602: GGT in PBC (>3.2x ULN prognostic cutoff)
- PMC8637680: Abnormal liver enzymes review
- PMC7110573: Evaluation of elevated liver enzymes (ALP grading)
- PMC5719197: Elevated liver enzymes in asymptomatic patients
- CTCAE v5.0: NCI official grading (GGT/ALP both use same xULN scale)

**Why:** Case reportから検査値をstateにマッピングする際、統一基準がないと一貫性を欠く。CTCAE v5.0は最も標準化された分級であり、臨床論文でも広く使われている。
**How to apply:** 新検査値変量追加時、まずこの4-state分級が適用可能か確認。適用可能なら統一フォーマットを使用。
