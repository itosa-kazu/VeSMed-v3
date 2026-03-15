---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：137疾病、~2296边、259cases、Top-1 71%、Top-3 94%、FATAL 0
type: project
---

- 137疾病(D01~D137)、314変量、~2296条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み
- OPQRST分解: S21胸痛→quality(S21)+provocation(S50)+radiation(S51)
- 测试: 259案例 (255 in-scope, 4 OOS)
- 当前成绩: Top-1 181/255(71%), Top-3 239/255(94%), FATAL 0
- ナビゲーションテスト: 10件
- Phase完了: 発熱(D01-D119), 呼吸困難(D120-D130), 胸痛(D131-D135), 腹痛開始(D136-D137)
- 残り非Top-3: 16件(証拠不足/類似疾患鑑別困難/非典型 = モデル限界)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
