---
name: 検査値変量の臨床的分級方法論
description: 検査値を新変量として追加する際、まずその変量固有の黄金分級を文献検索。専用分級がなければCTCAE v5.0ベースの4-stateをfallbackとする。
type: feedback
---

## 鉄則：検査値変量のstate設計は「因材施教」— 変量固有の黄金分級を優先

### 基本フロー

1. **文献検索**: 新検査値変量を追加する際、まずその変量の**専用臨床分級**をPMC/教科書で検索
2. **黄金分級があれば採用**: 学会ガイドライン等の確立された分級があればそれを使う
3. **なければCTCAE fallback**: 専用分級がない場合のみ、以下のCTCAE準拠4-stateを使う

### CTCAE fallback（専用分級がない検査値のデフォルト）

| State | 定義 | CTCAE対応 |
|-------|------|-----------|
| `normal` | ≤ULN | — |
| `mild_elevated` | >ULN ~ 3x ULN | G1相当 |
| `moderate_elevated` | 3x ~ 10x ULN | G2-G3相当 |
| `markedly_elevated` | >10x ULN | G3-G4相当 |

### 黄金分級の例

| 変量 | 黄金分級 | 出典 |
|------|----------|------|
| BNP | <100/100-400/>400 pg/mL | 心不全ガイドライン |
| PT-INR | 凝固能ベース（正常/延長/著明延長） | 凝固学 |
| CRP | <3/3-10/>10 mg/dL | 感染症分級 |
| トロポニン | 99th percentile基準 | ACS診断基準 |
| HbA1c | <5.7/5.7-6.4/≥6.5% | ADA糖尿病診断基準 |

### CTCAE fallback適用の変量

| 変量 | states | ULN参考値 |
|------|--------|-----------|
| γ-GTP | normal / mild / moderate / markedly_elevated | 男≤55, 女≤30 IU/L |
| ALP | normal / mild / moderate / markedly_elevated | 40-130 IU/L |
| AST/ALT | 同上 | AST: 10-40, ALT: 7-56 IU/L |
| LDH | 同上 | 120-246 IU/L |

### WebUI表示：具体的数値範囲を併記

state選択時にユーザーが迷わないよう、STATE_JAに具体的な数値範囲を併記する：
- 例: `軽度上昇 (55-165 IU/L)` ではなく、STATE_JA自体は `軽度上昇` のまま
- **app.pyのSTATE_JAにtooltip/補足情報を追加**して、WebUI上でホバーまたは括弧内に数値を表示

### PMC文献ソース

- PMC8735790: GGT特性 in different liver diseases
- PMC9972602: GGT in PBC (>3.2x ULN prognostic cutoff)
- PMC8637680: Abnormal liver enzymes review
- PMC7110573: Evaluation of elevated liver enzymes (ALP grading)
- PMC5719197: Elevated liver enzymes in asymptomatic patients
- CTCAE v5.0: NCI official grading

**Why:** 検査値ごとに臨床で確立された分級体系が異なる。一律CTCAEでは不適切な場合がある（例: BNPをxULNで分級しても臨床的に無意味）。各変量の黄金分級を優先することで、case reportからのマッピング精度が上がる。
**How to apply:** 新検査値変量追加時、①PMCで専用分級を検索 ②あればそれを採用 ③なければCTCAE 4-state fallback。
