---
name: VeSMed V3.1 項目状態
description: 419疾患、8047辺、1149案例、Top-1 78%、Top-3 93%、FATAL 0
type: project
---

- 419疾患(D01~D424)、794+変量、8047条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1149案例 (1143 in-scope, 6 OOS)
- 当前成绩: Top-1 893/1143(78%), Top-3 1066/1143(93%), FATAL 0
- R→D Prior: 全419疾患に年齢/性別prior設定済み
- D421-D424全案例追加済み(D421卵巣癌6/D422子宮頸癌5/D423黒色腫5/D424甲状腺癌6)
- Prior p_obs=0 bug: 性別exclusive疾患(前立腺癌等)でp_obs=0がneutralに処理される問題あり
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
