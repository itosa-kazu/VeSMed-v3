---
name: CPT state名とstep1 state定義の一致性チェック必須
description: step3のCPT state名がstep1のstate定義と不一致だと推理引擎がCPTを無視する。全変量で定期チェック必要
type: feedback
---

step3(noisy_or_params)のCPT内のstate名は、step1の変数定義のstates配列と**完全一致**でなければならない。一文字でも違うと推理引擎がそのCPT値を無視し、leak値にフォールバックする。

**Why:** R715(GPA)がFATALだった根本原因。L11のCPTに`mildly_elevated`と書いたがstep1では`mild_elevated`。E12のCPTに`localized_erythema`と書いたがstep1では`localized_erythema_warmth_swelling`。数十の疾患CPTが無効化されていた。

**How to apply:**
1. 辺/CPT追加後は必ずstep1のstatesと照合するバリデーションを実施
2. 外部AIが生成したCPTは特に注意（state名を勝手に短縮/変更している可能性大）
3. 定期的に全変量のstate名一致性チェックを実施するスクリプトを使う
