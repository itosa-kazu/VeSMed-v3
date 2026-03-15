---
name: VeSMed V3.1 项目状态
description: 发热鉴别诊断BN系统当前状态：116疾病、~1896边、196cases、Top-1 66%、Top-3 92%、FATAL 0
type: project
---

- 116疾病(D01~D116)、292変量(L48-L50, L14更新)、~1896条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.5 + CF ca=0.3)
- 反証推奨: next_best_falsification_test() 実装済み(エントロピー増大方向)
- 测试: 196案例 (193 in-scope, 3 OOS)
- 当前成绩: Top-1 128/193(66%), Top-3 178/193(92%), FATAL 0
- ナビゲーションテスト: 4件実施(R193 AOSD, R194/R195 DGI, R196 心筋炎)
- 今回追加疾患: D110-D116(トキソプラズマ/SJS-TEN/PAN/ヒストプラズマ/骨髄腫/DGI/心筋炎)
- 今回追加変量: L48 SPEP, L49 骨X線, L50 血清総蛋白, L14+lymphocyte_predominant
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
