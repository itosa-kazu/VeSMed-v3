---
name: VeSMed V3.1 项目状态
description: 发热鉴别诊断BN系统当前状态：114疾病、~1864边、191cases、Top-1 66%、Top-3 93%、FATAL 0
type: project
---

- 114疾病(D01~D114)、289変量(L48-L50新規)、~1864条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3, grid search最適化済)
- Prior策略: flat BASE=0.01 + RF相対比率。prevalence実験6種全て不採用。
- 中間変数: M01(SAH), M02(血行動態異常/ショック徴候=並列sign変数)
- 新機能: 見逃し防止(dont_miss), 推奨検査(期待所見付き), tab式UI, state日本語化160+項目
- 测试: 191案例 (188 in-scope, 3 OOS)
- 当前成绩 (2026-03-14): Top-1 125/188(66%), Top-3 174/188(93%), FATAL 0
- 今回追加疾患(D110-D114): トキソプラズマ, SJS/TEN, PAN, 播種性ヒストプラズマ, 多発性骨髄腫
- 今回追加変量: L48 SPEP/免疫固定, L49 骨X線, L50 血清総蛋白
- 未実装研究課題: 違和感メカニズム(反証検査), ナビゲーションテスト評価軸
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
