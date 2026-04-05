---
name: Jaccard非対称辺監査法
description: 高Jaccard疾患ペアの非対称辺から漏れ辺を体系的に検出する新手法
type: feedback
---

**高Jaccard疾患ペアの「のみ」辺 = 辺漏れ候補**。Jaccard > 0.7の類似疾患ペアで、一方にあって他方にない辺は、臨床的に追加すべき辺である可能性が高い。

**Why:** 講義教材生成時に鑑別困難ペアを分析したところ、「サルモネラのみ: 食欲不振, 心拍数」のような不整合が大量に発見された。従来のrank2+案例ベース監査と異なり、案例に依存せず全疾患を体系的にスキャンできる。

**How to apply:** `/edge-audit`や辺整備の際に、Jaccardベースの非対称辺リストを補助ツールとして使う。ただし「のみ」が全て漏れとは限らない（急性B肝の関節痛=serum sickness等、疾患特異的な差異もある）ので、臨床的妥当性の判断は必須。lecture APIの`/api/lecture`で`differential_pairs`→`unique_to_d1/d2`として自動出力される。
