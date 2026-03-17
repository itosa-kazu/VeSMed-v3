---
name: 大規模CPT変更は並列Agentで分割実行
description: 変量のCPT手動設計が大量にある場合、複数Agentに分割して並列実行する。1Agent=1変量。
type: feedback
---

## 鉄則：大規模CPT作業は並列Agent分割

### やり方

1. 変量ごとに1つのAgentを起動（最大5並列）
2. 各Agentに現在のCPT（leak + 全parent_effects）と臨床コンテキストを渡す
3. Agentが臨床根拠に基づいて新CPTをJSON形式で返す
4. 結果を収集して一括適用 → 回帰テスト

### Agentへの指示テンプレート

- 変量名・states・各stateの臨床的意味を明記
- 全parent疾患の現在CPTを提示
- 「比例正規化等の機械的変換は禁止、臨床的に考えろ」と明記
- 出力形式はJSON only（markdownや説明不要）

### 工数が大きい変量の扱い

- parent_effectsが多い変量（例: L04胸部X線の79親）は1Agent丸ごと担当
- 変量数が多い場合（例: 76変量のnot_done清理）は5変量ずつバッチ処理
- 各バッチ後に回帰テストして退化がないか確認

### 回帰テストのタイミング

- 5変量を適用するごとに `python bn_inference.py` で全案例テスト
- 退化があれば該当変量のCPTを個別調整
- 全バッチ完了後に最終回帰テスト

**Why:** 76変量のnot_done一括削除で機械的変換を3回試みて全て退化。1変量ずつ手動設計が正解だが、逐次では遅すぎる。並列Agentなら5変量を同時に臨床設計できる。
**How to apply:** CPT手動設計が5変量以上必要な場合、Agent toolで並列起動。各Agentに1変量を担当させる。
