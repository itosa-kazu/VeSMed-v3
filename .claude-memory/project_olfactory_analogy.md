---
name: 嗅覚組合符号化とVeSMedの同型性 — 侧抑制=explaining away=水流
description: 嗅覚系統の処理鏈とVeSMedの対応関係。侧抑制(lateral inhibition)=Bayesian explaining away=水流入盆地。VeSMedに欠けている核心拼図。
type: project
---

## 嗅覚系統とVeSMedの同型対応

| 嗅覚系統 | VeSMed | 状態 |
|---------|--------|------|
| 400種OR（受容体） | 900変量 | ✓ 已有 |
| 組合激活模式 | evidence模式 | ✓ 已有 |
| 模式補完（部分情報識別） | 部分evidence推論 | ✓ 已有 |
| 模式分離（相似模式の区別） | 反証推奨（falsification test） | ✓ 已有 |
| 自頂向下期待 | R→D prior | ✓ 已有 |
| **侧抑制（lateral inhibition）** | **???** | **❌ 欠缺** |
| 嗅覚適応（背景消除） | 快照間差分 | 計画v3.2 |

## 核心発見: 三概念同一

```
嗅覚侧抑制 = Bayesian explaining away = 水流入盆地
```

全て同一操作: **強者先占、弱者分余。**

### Noisy-ORの欠陥
Noisy-ORは各疾患を独立評分。同一所見が複数疾患に同等の信用を与える（競争なし）。

### explaining awayの実装構想（v3.3）
```
1. Noisy-OR評分（現行、不変）
2. 最強疾患が最特異所見を「認領」
3. 残余疾患が未認領所見で再評分
4. 収束まで繰返し
```

出力: 排名表ではなく「疾患組合 + 各疾患が説明する所見セット」

**Why:** 嗅覚の組合符号化から着想。VeSMedは嗅覚系統の処理鏈の大部分を既に持つが、侧抑制（explaining away）だけが欠けている。これが「匹配→解釈」の跨越の鍵。

**How to apply:** v3.3で侧抑制/explaining awayを実装。v3.0-v3.2はNoisy-OR維持。因果図の拓撲変更は不要（推論引擎の升級のみ）。

## 核心実装決定: Soft Lateral Inhibition

8つの対抗的攻撃テスト(→ project_v33_adversarial_bio_design.md)の結果、嗅覚侧抑制の正確な模倣が確定:
- **対比増強であり消灭ではない** — 視覚侧抑制はエッジを鋭化するが暗部を消さない
- **確率加重soft claiming** — hard winner-take-all禁止。生物は全層面(遺伝子→免疫→神経→進化)でsoft抑制
- **叠加型所見(fever等)はexplaining away対象外** — 生物信号の天然属性に従う

## 推論引擎の進化路線

```
v3.0: Noisy-OR（独立評分、競争なし）
v3.2: + D→D伝播（疾患間因果）— 標準BN恢復、新数学不要
v3.3: + explaining away（soft lateral inhibition）
      + unexplained residual検出器（先天免疫）
      → 匹配から解釈への完全移行
```
