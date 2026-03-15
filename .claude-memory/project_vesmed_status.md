---
name: VeSMed V3.1 项目状态
description: 发热鉴别诊断BN系统当前状态：118疾病、~1925边、200cases、Top-1 67%、Top-3 92%、FATAL 0
type: project
---

- 118疾病(D01~D118)、292変量、~1925条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み
- 测试: 200案例 (197 in-scope, 3 OOS)
- 当前成绩: Top-1 132/197(67%), Top-3 181/197(92%), FATAL 0
- ナビゲーションテスト: 6件
- 今回追加疾患: D110-D118
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
