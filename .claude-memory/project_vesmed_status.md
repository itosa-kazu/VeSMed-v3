---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：345疾病、6025边、792変量、712cases、Top-1 79%、Top-3 94%、FATAL 0
type: project
---

- 345疾病(D01~D350, D213統合削除)、792変量、6025条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 712案例 (708 in-scope, 4 OOS)
- 当前成绩: Top-1 558/708(79%), Top-3 662/708(94%), FATAL 0
- R→D Prior: 53/345疾患に年齢/性別prior設定済み（残り292が最優先課題）
- 実験分支: experiment/variable-audit-pipeline
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
