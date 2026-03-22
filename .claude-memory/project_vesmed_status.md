---
name: VeSMed V3.1 項目状態
description: 423疾患、8134辺、1213案例、Top-1 80%、Top-3 94%、FATAL 0
type: project
---

- 423疾患(D01~D428)、794+変量、8134条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1213案例 (1207 in-scope, 6 OOS)
- 当前成绩: Top-1 960/1207(80%), Top-3 1131/1207(94%), FATAL 0
- R→D Prior: 全423疾患に年齢/性別prior設定済み
- Prior p_obs=0 bug: 性別exclusive疾患(前立腺癌等)でp_obs=0がneutralに処理される問題あり
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
