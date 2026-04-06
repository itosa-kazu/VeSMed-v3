---
name: 嗅覚類比の総括 — 架構に有効、データに無効、IDF→explaining awayで消滅
description: 嗅覚系統とVeSMedの同型性。侧抑制=explaining away=水流。IDF=explaining awayの静的近似でv3.3で削除可能。
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
| **侧抑制（lateral inhibition）** | **soft claiming** | **v3.3で実装予定** |
| 嗅覚適応（背景消除） | 快照間差分 | 時系列(v4.x) |
| 浓度不変性 | 移植不可 | ❌ 入力空間の構造差 |

## 核心発見: 三概念同一

```
嗅覚侧抑制 = Bayesian explaining away = 水流入盆地
```

全て同一操作: **強者先占、弱者分余。**

## 推論引擎の進化路線

```
v3.0: Noisy-OR + IDF（独立評分、IDF外挂で共有症状を降重）
v3.2: + D→D伝播（疾患間因果）— 標準BN恢復
v3.3: + explaining away（soft lateral inhibition）
      + unexplained residual検出器
      - IDF削除（explaining awayが自然に代替）
      → 匹配から解釈への完全移行
```

## IDF = explaining awayの静的近似（v3.3で削除予定）

### IDFの問題
1. **静的** — 患者の証拠に関わらず固定重み
2. **全局的** — 全430疾患での出現頻度で計算。鑑別候補が2つに絞れても重みは不変
3. **確率基礎なし** — テキスト検索から借用した啓発的手法
4. **Noisy-ORの補丁** — 独立評分の欠陥を外付け重みで補正

### Explaining awayが天然にIDFを生む
```
発熱(300疾患接続): 300疾患が競争 → 各疾患の取得credit極小 → IDF低と同効果
盗汗(5疾患接続):   5疾患が競争 → 勝者が大部分を取得 → IDF高と同効果
```

| | IDF（v3.0） | Explaining away（v3.3） |
|--|-----------|----------------------|
| 静的/動的 | 静的（事前計算） | **動的**（証拠追加で変化） |
| 全局/局部 | 全局（全疾患対象） | **局部**（現在の鑑別候補間） |
| 確率基礎 | なし（啓発的） | **あり**（Bayes credit assignment） |

### 数学的対応
```
IDF ≈ 1/P(E) の粗糙な静的近似
Explaining away = P(E) の動的・条件付き精確計算

P(D|E) = P(E|D) × P(D) / P(E)
                              ↑ この分母をIDFが近似、explaining awayが精確計算
```

### 移行計画
- v3.3でexplaining away実装時にIDF重みを削除
- 性能比較: IDF有り/無し/explaining away → IDF無し+explaining awayが勝つはず
- **IDFはscaffolding、explaining awayがbuilding**

## 形状向量仮説（→ project_nmf_experiment.md）

- CPT矩陣の有効次元≈74、因子は器官系統に自動対応
- 補完には使えない（Netflix反論: 鑑別情報を破壊）
- 残差 = 鑑別情報 = IDFの精密版 → QCツール用

## 浓度不変性（移植不可）

- 嗅覚: 均質信号(全受体0-1連続値) + 単一スカラー浓度 → 総和で割り算
- VeSMed: 異質信号(二値/分類/連続混在) + 多次元重症度 → 統一歸一化不可
- log-LR + IDF(→explaining away) が「穷人版」として機能中
- A4(context-dependent CPT)は浓度不変性では解決不可、稀疏修飾層で個別対処

## 嗅覚類比の最終評価表

| 嗅覚機制 | VeSMed移植可? | 理由 |
|---------|-------------|------|
| 組合符号化 | ✓ 已有 | 設計原理 |
| 侧抑制/explaining away | ✓ v3.3 | 設計原理。**IDF削除の鍵** |
| 適応/背景消除 | ✓ 時系列 | 設計原理 |
| 受体最適化(変量選択) | ✓ 専門家代替 | 知的設計 |
| 物理免費CPT | ❌ | 対応する法則なし |
| 浓度不変性 | ❌ | 入力空間が異質 |

**嗅覚の贈り物 = 侧抑制(→IDF消滅) + 適応 + 組合符号化。**

**Why:** 嗅覚類比の全機制を系統的に評価。IDF=explaining awayの静的近似という発見。
**How to apply:** v3.3でexplaining away実装→IDF削除。浓度不変性はlog-LRで代替済み。A4は稀疏修飾層。
