---
name: VeSMed V3.1 項目状態
description: 415疾患、8000辺、1122案例、Top-1 79%、Top-3 94%、FATAL 0
type: project
---

- 415疾患(D01~D420)、794+変量、8000条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1122案例 (1116 in-scope, 6 OOS)
- 当前成绩: Top-1 878/1116(79%), Top-3 1046/1116(94%), FATAL 0
- R→D Prior: 全415疾患に年齢/性別prior設定済み
- 辺監査2回実施: Top-1 +15, Top-3 +8。30辺追加+S113/S180 NOP新規
- D05軟削除(deprecated)/D420 HFpEF追加/D215案例9件/D356案例8件
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
