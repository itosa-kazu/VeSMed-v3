---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：142疾病、~2363边、271cases、Top-1 71%、Top-3 93%、FATAL 0
type: project
---

- 142疾病(D01~D142)、317変量、~2363条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み
- OPQRST分解: S21→quality+provocation(S50)+radiation(S51)
- 测试: 271案例 (267 in-scope, 4 OOS)
- 当前成绩: Top-1 190/267(71%), Top-3 249/267(93%), FATAL 0
- ナビテスト: batch全228件実行済み(67%到達, 平均0.40ステップ)
- Phase完了: 発熱(D01-D119), 呼吸困難(D120-D130), 胸痛(D131-D135), 腹痛(D136-D137), 意識障害(D138-D142)
- 待ち: D138脳梗塞の案例(agent実行中)
- マスター疾患リスト: 疾患リスト.txt(670疾患)との差分分析済み
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
