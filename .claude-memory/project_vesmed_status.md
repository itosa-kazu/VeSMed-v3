---
name: VeSMed V3.1 項目状態
description: 415疾患、7967辺、1106案例、Top-1 78%、Top-3 93%、FATAL 0
type: project
---

- 415疾患(D01~D420)、794+変量、7967条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1106案例 (1100 in-scope, 6 OOS)
- 当前成绩: Top-1 853/1100(78%), Top-3 1023/1100(93%), FATAL 0
- R→D Prior: 全415疾患に年齢/性別prior設定済み
- 今回変更: D05軟削除(deprecated)+D420 HFpEF追加+D120からR204再マッピング
- D05: R18→D266, R33→D263に再マッピング。病原体別ID7個で代替
- D420: HFpEF 18辺, 6案例(2 Top-1, 3 Top-3, 1 MISS)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
