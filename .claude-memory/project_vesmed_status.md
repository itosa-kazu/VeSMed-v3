---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：130疾病、~2121边、232cases、Top-1 69%、Top-3 92%、FATAL 0
type: project
---

- 130疾病(D01~D130)、309変量、~2121条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み(max H_after降順, 閾値なし)
- 测试: 232案例 (228 in-scope, 4 OOS)
- 当前成绩: Top-1 157/228(69%), Top-3 209/228(92%), FATAL 0
- ナビゲーションテスト: 10件(最終版関数で再検証済み)
- 呼吸困難Phase 1完了: D120心不全/D121COPD/D122喘息/D123気胸/D124タンポ/D125不整脈/D126アナフィラ/D127胸水/D128上気道/D129過換気/D130ILD
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
