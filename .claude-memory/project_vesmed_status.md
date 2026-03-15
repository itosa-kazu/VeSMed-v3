---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：148疾病、~2433边、292cases、Top-1 72%、Top-3 92%、FATAL 0
type: project
---

- 148疾病(D01~D148)、318変量、~2433条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み
- OPQRST分解: S21→quality+provocation(S50)+radiation(S51)
- 测试: 292案例 (288 in-scope, 4 OOS)
- 当前成绩: Top-1 207/288(72%), Top-3 266/288(92%), FATAL 0
- ナビテスト: batch全228件実行済み(67%到達)
- Phase完了: 発熱/呼吸困難/胸痛/腹痛/意識障害 + 誤嚥性肺炎/GBS/尿管結石/高血圧緊急症/精巣捻転/Boerhaave
- マスター疾患リスト: 疾患リスト.txt(670疾患)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
