---
name: 大清洗pipeline — 致密モデル化設計
description: 全430疾患を1つずつ致密化。UpToDate主軸+PMC補完、hot-swap構成、1ヶ月集中作業。
type: project
---

## 目標

全430疾患 × 全evidence変量のペアを審査し、因果関係のあるペアに文献根拠付きの辺+CPTを設定する。
完了後は真の致密モデル（dense model）となり、変量追加以外の辺修正は不要になる。

## データソース戦略（2026-04-05確定）

### 主軸: UpToDate（1ヶ月集中、~$50/月）

- ユーザーがUpToDate月額アクセスを取得
- 各疾患の「Clinical manifestations」章節をコピー → `raw/D{xxx}.txt`
- ユーザーの作業: **1疾患5分 × 430疾患 ≈ 36時間（1日14疾患 × 30日）**
- Claudeの作業: raw txtから頻度抽出 → VeSMed変量マッピング → JSON生成

### 補助: Consensus MCP（無料） + PMC API（無料）

- Consensus: PMID検索、引用文献追跡
- PMC API: OA論文の全文XML取得 → 表格データ構造化解析
- Bronze案件（UpToDateが定性のみ）のn/N補完に使用

### 待定ツール（将来導入の可能性あり）

- **Elicit**（$49/月）: 全文データ提取(Extract Data)、跨論文比較、カスタム列。機構権限があれば全文アクセス可。SR内テーブルからの頻度抽出に有用
- **Consensus**（Pro $8.99/月 or MCP無料）: 2.2億論文検索、Medical Mode(800万医学論文)。PMID検索・引用追跡に有用。MCP経由でClaude Code直接統合可
- **Undermind**: 深層検索+successive search。稀少疾患のSR/NR発見に有用
- **PubMed.ai**: PubMed特化AI検索。MeSH最適化
- 導入判断はUpToDate主軸の実運用結果を見てから

### CPT値の分級策略（確定）

| グレード | 条件 | 処理 |
|---------|------|------|
| **Gold** | UpToDateが百分率/n/Nを直接提示 | そのまま使用 |
| **Silver** | UpToDateが範囲(30-50%)を提示 | 中央値採用、sourceに範囲記録 |
| **Bronze** | UpToDateが定性のみ("common") | Claude がUpToDateの引用PMIDをPMC APIで追跡し原始n/Nを取得 |
| **要人工** | 引用論文がPMC外 | ユーザーがUpToDate引用元から数値を補完 |

### 多state分配問題

- UpToDateが「dyspnea 40%」→ absent=0.60, present(全陽性state合計)=0.40
- 陽性state間の分配(on_exertion vs at_rest)は:
  - 追加文献があれば使用
  - なければ臨床判断で推定し `"quality": "estimated"` で標記
  - 将来的には主変量+衛星変量分離で解消

## 核心設計

### 1. 情報源の鉄則

- **全ての辺に文献根拠必須（PMID + source type + excerpt）**
- 情報源優先順位: **SR > NR > TB(UpToDate) > CS**
- **降級した情報源は必ず明示的にtypeで標記** → 全環節貫通の鉄律
- 1疾患につきUpToDate記事を基盤 + 引用文献で補完
- **UpToDateに記載なし = 無辺**（UpToDateが臨床所見を漏らすことはない）

### 1.1 辺の根拠とCPT値の根拠は分離記録

- **source_edge**: 辺の存在根拠（UpToDate記載 or SR/NR）
- **source_cpt**: CPT値の根拠（頻度データ n/N を含む原始研究）

### 1.2 CPT値は実数カウント(n/N)が理想

- Gold/Silver: UpToDateの数値を直接使用
- Bronze: 引用文献を追ってn/Nを取得
- 要人工: ユーザーが引用元から補完
- 全グレードをJSONに記録し、将来のアップグレードパスを確保

### 1.3 データ提取

- ユーザーがUpToDate本文をコピペ → `raw/D{xxx}.txt`
- Claude が txt を解析 → 変量マッピング → JSON生成
- Bronze案件のPMID追跡はClaude がPMC APIで自動実行
- 原始テキストはraw/に永久保存（ground truth）

### 2. アーキテクチャ: hot-swap方式

- 旧step2/step3は一切変更しない
- `dense_audit/` ディレクトリに疾患別JSONを配置
- 推論エンジン(bn_inference.py)にoverlay層を追加:
  - dense_audit/D058.json が存在 → 旧D58辺を全除去し新辺で置換
  - dense_audit/D058.json を削除 → 旧辺に自動復帰
- **即挿即用、抜けば原状復帰**

### 3. 疾患別JSONスキーマ

```json
{
  "disease_id": "D58",
  "name_ja": "成人Still病",
  "processed_date": "2026-04-04",
  "source": {
    "primary": "UpToDate: 'Clinical manifestations of AOSD'",
    "accessed": "2026-04-XX"
  },
  "edges": [
    {
      "to": "E12",
      "to_name": "skin_rash",
      "cpt": {"absent": 0.24, "maculopapular_rash": 0.76},
      "quality": "gold",
      "reason": "Evanescent salmon-colored rash during fever spikes",
      "source_edge": {"source": "UpToDate", "type": "TB"},
      "source_cpt": {"pmid": "28765432", "type": "CS", "excerpt": "rash in 45/59 (76%)"}
    }
  ],
  "regression_snapshot": {
    "top1": 988,
    "top3": 1177,
    "fatal": 0,
    "total": 1262
  }
}
```

- edgesに含まれない変量 = 審査済みで無辺と判定
- quality: gold/silver/bronze/estimated
- regression_snapshotは記録のみ、途中の退化は追究しない（完成後に評価）

### 4. ID幻覚防止: テンプレート生成

- `generate_template.py D58` で全変量のID+name+statesを事前生成
- Claude Codeはテンプレートから**選択**するだけ、手打ち禁止

### 5. 進捗管理

- `ls dense_audit/ | wc -l` = 完了疾患数
- 430 - 完了数 = 残数
- ファイルの存在自体が進捗

### 6. 想定外事象の報告義務

実行中に設計時の想定外の事象が発生した場合は、**必ず作業を停止してユーザーに報告**する。

## 作業スケジュール概算

- ユーザー: 1日14疾患 × 5分 = 70分/日 + 抽検30分 ≈ 1.5-2時間/日
- Claude: raw txt解析 + JSON生成 + Bronze PMID追跡 + 回帰テスト
- 目標: 30日で430疾患完了
