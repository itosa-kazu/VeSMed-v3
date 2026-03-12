# VeSMed Real Case Test Results
## Date: 2025-03-12
## Network: step1_v2.7 (273変数, 102疾患, 984辺)

## FINAL RESULTS (R01-R43, R44-R50除外)

| Metric | Value |
|--------|-------|
| Total cases | 43 |
| In-scope | 36 |
| OOS (out of scope) | 7 |
| **Top-1 accuracy** | **20/36 (56%)** |
| **Top-3 accuracy** | **29/36 (81%)** |
| Confident misdiagnosis (H<2+wrong) | 5 |

## Disease-specific breakdown

| Category | Cases | Top-1 | Top-3 |
|----------|-------|-------|-------|
| Still disease | 8 | 8/8 (100%) | 8/8 |
| Lymphoma/HLH | 5 | 3/5 (60%) | 5/5 |
| Tuberculosis | 6 | 2/6 (33%) | 4/6 |
| PCP | 2 | 2/2 (100%) | 2/2 |
| Q fever | 3 | 0/3 (0%) | 1/3 |
| IE | 1 | 1/1 | 1/1 |
| Other infections | 5 | 3/5 | 4/5 |
| Other autoimmune | 3 | 1/3 | 1/3 |
| Other | 3 | 0/3 | 3/3 |

## Confident Misdiagnosis (H<2 + wrong) — 最重要

| Case | H | Output | Correct | Root cause |
|------|---|--------|---------|------------|
| R03 DLBCL/HLH 78F | 0.9 | 白血病73% | リンパ腫r2 | 白血病vsリンパ腫は骨髄検査なしで鑑別不能 |
| R11 COVID 81M | 1.5 | 肺炎71% | COVIDr4 | COVID特異所見なし。PCR必須 |
| R26 HLH 50F | 1.2 | 白血病69% | リンパ腫r2 | R03と同パターン |
| R36 Miliary TB 48F | 1.2 | リンパ腫63% | 結核r2 | B症状がリンパ腫と完全に重なる |
| R39 TB meningitis 72M | 1.8 | マラリア55% | 結核r3 | R06=tropical→マラリア優先 |

## OOS cases (リスト外疾患)

| Case | H | Fallback | Clinical adequacy |
|------|---|----------|-------------------|
| R02 Cogan | 3.1 | Still 43% | まあまあ |
| R12 Murine typhus | 2.3 | CMV 62% | 発熱+肝脾腫としてはまあまあ |
| R29 ARF | 4.1 | 痛風 16% | H高い=不確定信号は正しい |
| R31 Scrub typhus | 1.5 | NMS 82% | 筋強剛→NMSは妥当だが危険 |
| R32 PFAPA | 2.2 | FMF 49% | 周期熱→FMFは臨床的に妥当 |
| R42 Psittacosis | 0.9 | 肺炎89% | 肺炎型なのでfallbackとして妥当 |
| R43 Strongyloides | 3.7 | IBD 29% | H高い=不確定信号は正しい |
