---
name: 新変数追加時の三位一体監査チェックリスト
description: 新変数追加後に必ず7項目の整合性チェックを実施する。M02追加時にWebUI STATE_JA漏れを発見した教訓。
type: feedback
---

新変数を追加したら、以下7項目を必ず監査すること：

1. **step1**: 変数定義（id, name, name_ja, category, states）
2. **step2**: 関連辺（disease→変数）が全て存在
3. **step3**: CPT（leak + parent_effects）がstep2の辺と一致
4. **bn_inference.py**: 特殊prefix（M-prefix等）の処理対応
5. **test cases**: 該当案例に証拠が追加されている
6. **WebUI STATE_JA**: 全stateの日本語ラベルが登録されている
7. **app.py**: パラメータ・import等が最新

8. **IDF健全化（強制）**: 新変量追加後、parent数が3未満ならIDF≈1.0で特定疾患を偏袒する。**必ず**臨床的に合理的な既存疾患からの辺を追加してparent≧3にする。辺の追加理由は文献的に妥当でなければならない（IDF調整のためだけの無根拠な辺は禁止）。L51/S49/E36/E37で全てIDF=1.0→0.6-0.7に修正した教訓(2026-03-15)

9. **回帰テスト**: 全案例を再実行し、MISSリストを前回と比較。新たにMISSになった案例があれば原因分析

**Why:** M02追加時にSTATE_JAへの登録を漏らした。S48追加時にparent1本でIDF=1.0のBUG的挙動が発生。D107/D109追加時に4件の回帰バグ発見(うち1件はexpected_id誤り)。新変数は上流変更なので下流全てに波及する。
**How to apply:** 新変数・新疾患追加のcommit前に、上記9項目をチェック。特に回帰テストは毎回必須。
