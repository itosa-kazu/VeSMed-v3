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

- **全ての辺に文献根拠必須（PMID + source type + excerpt）**
- 情報源優先順位: **Systematic Review (SR) > Narrative Review (NR) > Textbook (TB) > Case Series (CS)**
- **降級した情報源は必ず明示的にtypeで標記** → 全環節貫通の鉄律
- 1疾患につき1篇の高品質綜述を基盤とする
- **綜述に記載なし = 無辺**（良質な綜述が臨床所見を漏らすことはない）

### 1.1 辺の根拠とCPT値の根拠は分離記録

辺の存在根拠（この疾患がこの所見を引き起こすか）とCPT値の根拠（頻度データ）は
別の文献から来ることがある。両方を個別に記録する:

- **source_edge**: 辺の存在根拠（通常はSR/NR — 臨床所見として記載あり）
- **source_cpt**: CPT値の根拠（頻度データ n/N を含む原始研究）

### 1.2 CPT値は実数カウント(n/N)必須

- CPT値は必ず実際の患者数カウント(n/N)から算出する
- 定性描述（"common", "rare", "frequent"等）からの主観的変換は禁止
- SRに頻度なし → SRの引用文献を追い、頻度データのある原始研究を探す
- SRもNRもない稀少疾患 → 最大サンプルのcase seriesから頻度を取得

### 1.3 SR選定基準

- 同一疾患に複数SRがある場合: **最新 + 最大pooled N + PRISMA準拠**を優先
- 選定したSRとともに**全候補SR**をJSONに記録（選定理由含む）
- 候補SR間で結論が矛盾する場合は記録して報告

### 1.4 データ提取: プログラム化必須（Claude WebFetch禁止）

Claudeの WebFetchは表格解読の信頼性が低いため、データ提取には使用しない。

- **PMC文献** → NCBI E-utilities APIでXML取得 → Pythonスクリプトで`<table>`を構造化解析
- **PDF文献** → ダウンロード → OCR API → テキスト化 → プログラム解析
- Claudeの役割は「構造化データからの選択」のみ（生データの解読はしない）
- **原始テーブルデータはground truthとして保存** → いつでも検証可能

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
      "cpt": {"absent": 0.24, "maculopapular_rash": 0.76},
      "reason": "Evanescent salmon-colored rash during fever spikes",
      "source_edge": {"pmid": "32345678", "type": "SR"},
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
- regression_snapshotは記録のみ、途中の退化は追究しない（完成後に評価）

### 4. ID幻覚防止: テンプレート生成

- `generate_template.py D58` で全変量のID+name+statesを事前生成
- Claude Codeはテンプレートから**選択**するだけ、手打ち禁止
- 生成後に検証スクリプトでID/state合法性を自動チェック

### 5. 変量設計: 主変量+衛星変量

多状態変量は主変量（有/無の二値）と衛星変量（亜型）に分離する:
- **主変量**: skin_rash_present [absent, present] → SRのn/Nが直接CPTになる
- **衛星変量**: skin_rash_morphology [maculopapular, petechial, vesicular, ...] → 皮疹を引き起こす疾患のみ
- これにより「SR頻度→CPT」の変換が一意になり、多状態分配問題が消滅する
- 変量も全面再設計（旧変量は旧step1/step2/step3に残す、新設計はdense_audit体系）

### 6. 案例は別pipeline

案例検索・追加は大清洗pipelineとは分離。1 pipeline = 1問題。

### 6. 進捗管理

- `ls dense_audit/ | wc -l` = 完了疾患数
- 430 - 完了数 = 残数
- ファイルの存在自体が進捗

### 8. 想定外事象の報告義務

実行中に設計時の想定外の事象が発生した場合は、**必ず作業を停止してユーザーに報告**する。
自己判断で回避策を取らない。

## 既存の稠密モデル実験との関係

project_dense_model_plan.mdの実験で「leak auto-fillは無効」と確認済み。
本pipelineはその教訓を踏まえ、全辺を文献ベースの臨床CPTで設定する正攻法。
