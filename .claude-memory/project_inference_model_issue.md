---
name: 推理引擎：超参数・prevalence問題（解決済み）
description: IDF+Coverage超参数はgrid search解決。prevalence実験3種は全てFATAL>0で不採用。flat 0.01が最適。
type: project
---

## 超参数問題（解決済み）
81パラメータ組のgrid searchで最適値特定: dp=0.5, ca=0.3
`python bn_inference.py --grid` で再最適化可能

## prevalence実験（全て不採用）
| 方案 | Top-1 | Top-3 | FATAL | 分支 |
|------|-------|-------|-------|------|
| flat 0.01(現行) | 62% | 94% | 0 | main |
| raw prevalence | 65% | 85% | 2 | exp/raw-prevalence |
| adaptive(1/n) | 60% | 88% | 3 | exp/adaptive-prevalence |
| pop-leak | 56% | 81% | 3 | exp/pop-leak |
| pop-leak+cov | 63% | 89% | 6 | exp/pop-leak-cov |
| MI weight | 49% | 76% | 5 | exp/mi-weight |

**結論**: IDF+CoverageがprevalenceのIDF+Coverageが prevalenceの役割を間接的に代替しており、prevalence追加は二重計上になる。flat 0.01が最適。
