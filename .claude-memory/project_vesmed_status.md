---
name: VeSMed V3.1 项目状态
description: 发热鉴别诊断BN系统当前状态：117疾病、~1910边、198cases、Top-1 67%、Top-3 92%、FATAL 0
type: project
---

- 117疾病(D01~D117)、292変量、~1910条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み(エントロピー増大方向)
- 测试: 198案例 (195 in-scope, 3 OOS)
- 当前成绩: Top-1 130/195(67%), Top-3 179/195(92%), FATAL 0
- ナビゲーションテスト: 5件(R193 AOSD, R194/R195 DGI, R196 心筋炎, R198 硬膜外膿瘍)
- 今回追加疾患: D110-D117
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
