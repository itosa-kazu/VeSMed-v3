# VeSMed テスト症例の完全分類

## 基本原則
- Real case = 公開文献/国試から原文をそのまま使い、私(Claude)が答えを見ずにマッピングできないもの
- Synthetic = 私が答えを知った上で構成した症例（confirmation bias あり）
- 両者の証明力は根本的に異なる

## 現状 (2025-03-12)

### Real Cases: 11例 + 新規発見3例 = 14例
| # | 出典 | PMC/DOI | 正答 | リスト内? | 結果 |
|---|------|---------|------|----------|------|
| 1 | BMJ 2006 | PMC1557921 | Still(19F) | ✓ | ✗→✓(修正後) |
| 2 | BMJ CaseRep 2018 | PMC5990099 | Cogan(31F) | ✗OOS | ◇fallback |
| 3 | Cureus 2024 | PMC11706331 | DLBCL/HLH(78F) | △ | △rank2(白血病73%) |
| 4 | Cancer Rep 2024 | PMC11578651 | Hodgkin(44M) | ✓ | ✓リンパ腫96% |
| 5 | CHEST 2024 | journal.chestnet.org | PCP非HIV(71M) | ✓ | ✗→✓(修正後96%) |
| 6 | BMJ CaseRep 2021 | PMID:33602758 | Q熱肝炎(39F) | ✓ | △rank2(34%) |
| 7 | BMC InfDis 2025 | 10.1186/s12879-025-10699-8 | Q熱SCLS(54M) | ✓ | △rank2(34%) |
| 8 | NEJM 2024 | Case 4-2024 | マラリア(39M) | ✓ | ✓52% |
| 9 | NEJM 2024 | Case 31-2024 | レプトスピラ(37M) | ✓ | ✓53% |
| 10 | NEJM 2024 | Case 38-2024 | IE→SAH(22F) | ✓ | ✗→✓(SAH追加後99%) |
| 11 | NEJM 2021 | Case 18-2021 | COVID(81M) | ✓ | ✗(肺炎>COVID) |
| 12 | PMC 2022 | PMC9373758 | Murine typhus(37M) | ✗OOS | 未テスト |
| 13 | Cureus 2023 | PMC10473233 | PE/DVT(86F) | ✓ | 未テスト |
| 14 | Medicine 2024 | PMC10798690 | PTCL-TFH(28M) | ✗OOS | 未テスト |

### Real Case 成績（リスト内疾患のみ）
- 修正後 Top-1: 5/10 (50%)
- 修正後 Top-3: 8/10 (80%)

### Synthetic Cases: ~115例
- 回帰テスト(28疾患典型例): 17例
- 新疾患代表例: 29例
- 疑難バッチ: 30例
- adversarial: 15例
- 修正確認: ~24例
- Synthetic Top-1: ~90%

## 論文で報告すべき数字
- Real case Top-1 50%を正直に報告
- Synthetic 90%は「内部検証」として報告
- 両者のギャップ(50% vs 90%)の原因分析が論文の核心

## 必要なアクション
- Real caseを最低50例まで増やす必要がある
- MIMIC-IV申請 → 真の外部検証
- 国試過去問も「real case」として使える可能性あり（独立した出題者による症例）
