---
name: VeSMed V3.1 項目状態
description: 鉴别诊断BN系统当前状态：353疾病、6559边、745cases、Top-1 79%、Top-3 94%、FATAL 0
type: project
---

- 353疾病(D01~D358, A群6疾患分割済み)、792+変量、6559条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 745案例 (740 in-scope, 5 OOS)
- 当前成绩: Top-1 584/740(79%), Top-3 692/740(94%), FATAL 0
- R→D Prior: 285+疾患に年齢/性別prior設定済み
- JAPAN_POP: R01/R02/R05/R06/R40の人口分布定義済み
- A群疾患分割完了: DVT/PE, CD/UC, NHL/HL, 喉頭蓋炎/異物, Campy/Salm/Shig, AF/SVT/VT
- E40にSVT/VT state追加済み
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
