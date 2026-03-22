---
name: VeSMed V3.1 項目状態
description: 431疾患、8233辺、1246案例、Top-1 79%、Top-3 94%、FATAL 0
type: project
---

- 431疾患(D01~D436)、795+変量、8233条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.7 + CF ca=2.5 + PP=0.3)
- 测试: 1246案例 (1240 in-scope, 6 OOS)
- 当前成绩: Top-1 979/1240(79%), Top-3 1160/1240(94%), FATAL 0
- R→D Prior: 全431疾患に年齢/性別prior設定済み
- 新追加(2026-03-22): D429アニサキス/D430 FD/D431食道カンジダ/D432自己免疫性胃炎/D433 Meckel/D434裂肛/D435痔瘻/D436便秘症
- 新変量: R67(生魚摂取歴), S190(肛門痛)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
