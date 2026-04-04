---
name: 大清洗pipeline — 致密モデル化設計
description: 全430疾患を1つずつ致密化。SR文献ベース、hot-swap構成、テンプレート生成でID幻覚防止。
type: project
---

## 目標

全430疾患 × 全evidence変量のペアを審査し、因果関係のあるペアに文献根拠付きの辺+CPTを設定する。
完了後は真の致密モデル（dense model）となり、変量追加以外の辺修正は不要になる。

## 核心設計（2026-04-04確定）

### 1. 情報源の鉄則

- **全ての辺にPMID + source type + excerpt必須**
- 情報源優先順位: **Systematic Review (SR) > Narrative Review (NR) > Textbook (TB)**
- **降級した情報源は必ず明示的にtypeで標記** → 全環節貫通の鉄律
- 1疾患につき1篇の高品質綜述を基盤とする
- **綜述に記載なし = 無辺**（良質な綜述が臨床所見を漏らすことはない）

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
    "pmid": "32345678",
    "type": "SR",
    "title": "Clinical features of AOSD: a systematic review",
    "year": 2021
  },
  "edges": [
    {
      "to": "E12",
      "to_name": "skin_rash",
      "cpt": {"absent": 0.24, "maculopapular_rash": 0.70, ...},
      "reason": "Evanescent salmon-colored rash during fever spikes",
      "excerpt": "skin rash 76% (95%CI 70-81%, n=1203)"
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
- regression_snapshotは記録のみ、途中の退化は追究しない（完成後に評価）

### 4. ID幻覚防止: テンプレート生成

- `generate_template.py D58` で全変量のID+name+statesを事前生成
- Claude Codeはテンプレートから**選択**するだけ、手打ち禁止
- 生成後に検証スクリプトでID/state合法性を自動チェック

### 5. 案例は別pipeline

案例検索・追加は大清洗pipelineとは分離。1 pipeline = 1問題。

### 6. 進捗管理

- `ls dense_audit/ | wc -l` = 完了疾患数
- 430 - 完了数 = 残数
- ファイルの存在自体が進捗

## 既存の稠密モデル実験との関係

project_dense_model_plan.mdの実験で「leak auto-fillは無効」と確認済み。
本pipelineはその教訓を踏まえ、全辺を文献ベースの臨床CPTで設定する正攻法。
