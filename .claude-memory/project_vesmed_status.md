---
name: VeSMed V3.1 项目状态
description: 鉴别诊断BN系统当前状态：135疾病、~2247边、245cases、Top-1 71%、Top-3 91%、FATAL 0
type: project
---

- 135疾病(D01~D135)、313変量、~2247条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み(max H_after降順, 閾値なし)
- OPQRST分解: S21胸痛→quality(S21)+provocation(S50)+radiation(S51)に分解済み
- 测试: 245案例 (241 in-scope, 4 OOS)
- 当前成绩: Top-1 170/241(71%), Top-3 220/241(91%), FATAL 0
- ナビゲーションテスト: 10件(最終版関数で検証済み)
- 呼吸困難Phase 1完了, 胸痛Phase 2完了
- 案例0件の疾患: D124タンポナーデ, D134心膜炎, D135肋軟骨炎(検索中)
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
