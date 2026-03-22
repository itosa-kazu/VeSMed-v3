---
name: VeSMed V3.1 項目状態
description: 415疾患、7967辺、1118案例、Top-1 77%、Top-3 93%、FATAL 0
type: project
---

- 415疾患(D01~D420)、794+変量、7967条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1118案例 (1112 in-scope, 6 OOS)
- 当前成绩: Top-1 860/1112(77%), Top-3 1033/1112(93%), FATAL 0
- R→D Prior: 全415疾患に年齢/性別prior設定済み
- 今回変更: D05軟削除/D420 HFpEF追加/D215案例5件/D356案例7件追加
- D215急性AR: 10辺, 5案例(1 Top-1, 2 Top-3, 2 MISS) → edge-audit推奨
- D356 SVT/WPW: 23辺, 8案例(7 Top-1, 1 Top-3)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
