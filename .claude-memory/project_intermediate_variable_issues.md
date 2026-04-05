---
name: 中間変量問題リスト
description: 間接因果を直接辺にできない問題の一覧。中間変量追加または新しいlab変量で対処が必要。
type: project
---

## 解決済み

### 転移巣 → L63 転移巣(CT/PET所見)
- **方式**: 中間層ではなく、観測可能なlab変量として実装
- **states**: not_done/absent/lung/bone/liver/brain/multiple
- **結果**: Top-1 +4, Top-3 +1（experiment/metastasis-variable分岐で検証）
- **教訓**: 間接因果は「観測可能な検査所見」に変換すればBNに組み込める

### ショック → M02 血行動態異常
- **方式**: 並列sign変量として実装済み
- **states**: stable/compensated/shock

## 未解決（要排査）

### DIC → L64 DICスコア(ISTH基準) ✅解決
- **方式**: 観測可能なlab変量(not_done/normal/pre_DIC/overt_DIC)
- **結果**: Top-3 +3。HELLP/胎盤早期剥離の鑑別改善
- **10辺**: DIC/HELLP/胎盤早期剥離/敗血症/APL/熱中症/マムシ/TTP/HUS/白血病

### 心不全 → L65 心不全グレード(臨床評価) ✅解決
- **方式**: 観測可能なlab変量(not_assessed/absent/mild_NYHA2/severe_NYHA3_4)
- **結果**: AS/収縮性心膜炎の改善。たこつぼ/MSはcf_alpha波及で悪化→evidence除外で対応
- **13辺**: ADHF/AS/MS/HCM/たこつぼ/収縮性心膜炎/心筋炎/心タンポナーデ/ACS/CTEPH/マルファン/心膜炎/不整脈

### 肝不全/肝うっ血 → L66 肝障害パターン ✅解決
- **方式**: 観測可能なlab変量(not_assessed/normal/hepatocellular/cholestatic/congestive)
- **20辺**: 肝細胞型(A肝/B肝/AIH等)+胆汁うっ滞型(CBD結石/胆管癌等)+うっ血型(肝硬変/心不全等)

### 腎前性AKI → L67 AKI原因分類 ✅解決
- **方式**: 観測可能なlab変量(not_assessed/no_AKI/prerenal/renal/postrenal)
- **13辺**: 腎前性(DKA/HHS/AAA等)+腎性(横紋筋融解/RPGN/TLS等)+腎後性(膀胱癌/前立腺癌)

### 骨髄浸潤/骨髄抑制
- **問題**: 癌の骨髄浸潤/化学療法→汎血球減少
- **影響疾患**: 前立腺癌, 白血病, 骨髄腫, 神経芽腫等
- **案**: L14/L22で部分対応中。将来的にL68等で対応検討

### 共通上流原因による併発所見（疑似直接辺）
- **問題**: D→V辺が存在するが、真の因果は「共通上流→D + 共通上流→V」
- **既知の例**:
  - **D177(虚血性腸炎)→L55(Cr/AKI)**: 動脈硬化/低灌流が共通上流。虚血性腸炎がAKIを起こすのではなく併発
  - 同様にD177→E03(低血圧)、D177→E38(高血圧crisis)も背景共有の可能性
- **影響**: 推論エンジンへの影響は軽微（他証拠と合算されるため）。講義資料の「確定所見」選出で不適切な結論が出る
- **暫定対応**: generate_lecture.pyにINDIRECT_EDGES除外リストを追加
- **将来案**: 全疾患で系統的に間接辺を監査。共通上流原因を持つ疾患-変量ペアを特定しフラグ付与

## 設計原則
- **間接因果に直接辺を張らない**（feedback_no_indirect_edges.md）
- **中間状態が観測可能なら lab/sign 変量として追加**（L63方式）
- **中間状態が観測困難なら M変量（並列sign）として追加**（M02方式）
