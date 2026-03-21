---
name: VeSMed V3.1 項目状態
description: 407疾患、7864辺、1066案例、Top-1 78%、Top-3 93%、FATAL 0
type: project
---

- 407疾患(D01~D412)、792+変量、7864条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1066案例 (1060 in-scope, 6 OOS)
- 当前成绩: Top-1 825/1060(78%), Top-3 990/1060(93%), FATAL 0
- R→D Prior: 全407疾患に年齢/性別prior設定済み
- 国試Priority A+B: 全16疾患完了
- 国試Priority C: 6/11疾患完了(メニエール/突発性難聴/急性中耳炎/乾癬/丹毒/脊柱管狭窄症)
- NOP活性化: S124(5), S125(5), E62(5), S140(4) — 今回新規活性化
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
