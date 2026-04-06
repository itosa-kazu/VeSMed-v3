---
name: 2026-04-06 嗅覚→v3.3設計→対抗攻撃 全討論交接
description: 2026-04-06の長時間セッション全体の交接摘要。嗅覚系統の生物学的メカニズムからv3.3アーキテクチャ設計、3轮21攻撃の対抗検証まで。
type: project
---

## セッション概要（2026-04-06）

嗅覚系統をVeSMedの設計青写真として深掘りし、v3.3の完全設計を確立。
3轮の対抗攻撃(計21攻撃)で検証。致命的欠陥なし。

## 討論の流れ（時間順）

### Phase 1: 嗅覚→VeSMed対応関係
- 嗅覚の400受体→パターン空間、明示的「匂いノード」なし
- CPT行列の低ランク構造発見: NMF実験でk≈74(90%分散)、因子は臓器系に自動対応
- Netflix式補完は失敗(r=0.24): 類似性補完は鑑別情報を破壊（anti-Netflix residual）
- **結論**: 形状は存在するが補完には使えない。データの近道なし

### Phase 2: 移植可能/不可能の分類
- **移植可能**: 侧抑制(EA)、適応(記憶)、組合せ符号(既存)
- **移植不可能**: 無料CPT(進化データ不足)、濃度不変性(異種入力空間)
- IDF = EAの静的近似と判明 → v3.3でIDF削除、EA導入

### Phase 3: 時間系列処理
- 核心発見: 侧抑制と適応は**同一操作**（顆粒細胞の二重機能）
- v4.x不要、v3.3+記憶で時間処理が可能
- 専門家推論との同構: 初心者=Noisy-OR、専門家=EA+記憶

### Phase 4: D→D設計（GRNから）
- D→Dは嗅覚ではなく遺伝子調控網絡(GRN)が対応
- 閾値はEAから湧現(Hill関数≈EA後の鋭化)、追加パラメータ不要
- Kd進化=代価-収益均衡。暴力調参禁止(1268案例で過拟合)
- EHRが「進化の無限データ」に相当

### Phase 5: v3.3完全設計確立
三層単一回路:
1. Noisy-OR原始信号
2. D→D伝播
3. EA+記憶（侧抑制+適応）

削除: IDF、独立スコアリング
湧現: unexplained residual、解釈出力

### Phase 6: 対抗攻撃3轮

**第1轮(8攻撃)** → project_v33_adversarial_bio_design.md
- 全解決。核心: soft claiming(概率加重認領)

**第2轮(7攻撃)** → project_v33_adversarial_round2.md
- 全解決。4つの核心設計原則:
  1. **Jacobi同期更新**: 全並列、順序依存なし（攻撃1,3）
  2. **信号級記憶**: "what I saw" only、解釈を記憶しない（攻撃2）
  3. **Bayes概率分配**: soft claiming=標準Bayes公式（攻撃4）
  4. **理論優先**: EA直接実装、灰度発布で誤魔化さない（攻撃7）

**第3轮(6攻撃)** → project_v33_adversarial_round3.md
- 架構vs現実世界の接口。攻撃8のみ方針確定。攻撃9-13未討論。
- 攻撃8: CPT質量→v3.1大清洗→直接EA。EHRで最終解
- **攻撃9-13は未討論、次セッションで継続**

### Phase 7: EHEC→HUS議論
- D→Dの真の適用範囲を厘清
- 物理痕跡(検査結果)が橋梁になる因果鏈はD→D不要
- D→Dは橋梁がない統計/病理関連のみ
- → project_dd_grn_design.md に記録

### Phase 8: 蒸留プロンプト
- prompts/disease_distillation_prompt.md + prompts/variable_list.txt 作成
- UpToDate Expert AIは外部データ生成を拒否
- 回避策: 臨床質問で頻度取得→別AIでJSON変換の二段階

## 未完了タスク
1. **第3轮攻撃9-13の討論** ← 最優先
   - 攻撃9: 封閉世界仮設（430外の疾患）
   - 攻撃10: 変量粒度不一致
   - 攻撃11: 時間情報の貧困
   - 攻撃12: EA奥卡姆仮設（多病老年患者）⭐⭐⭐⭐⭐
   - 攻撃13: 検査級聯
2. **蒸留プロンプトのUpToDate対応版**（臨床質問形式）

## 関連memoryファイル一覧
| ファイル | 内容 |
|---------|------|
| project_v33_adversarial_bio_design.md | 第1轮8攻撃+4設計原則 |
| project_v33_adversarial_round2.md | 第2轮7攻撃+4核心原則+EA先行研究+蒸留 |
| project_v33_adversarial_round3.md | 第3轮6攻撃(攻撃9-13未討論) |
| project_vesmed_v33_design.md | v3.3完全設計 |
| project_dd_grn_design.md | D→D設計+EHEC→HUS洞察 |
| project_olfactory_analogy.md | 嗅覚メカニズム移植可否一覧 |
| project_olfactory_time_series.md | EA+記憶=時間処理 |
| project_expert_reasoning_isomorphism.md | 専門家推論=嗅球処理 |
| project_nmf_experiment.md | NMF実験+Netflix批判 |

## 次セッションへの指示
「第3轮攻撃9-13を続けて」と言えば即座に再開可能。
全ての文脈は上記memoryファイルに格納済み。
