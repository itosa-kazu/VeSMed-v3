# Memory Index

## 鉄則・フィードバック
- [feedback_project_principles.md](feedback_project_principles.md) — VeSMed 6大鉄則：実症例のみ/CPT文献必須/変数ID確認/三件套同期/辺+CPT同時/新疾患追加時real case必須
- [feedback_regression_report_format.md](feedback_regression_report_format.md) — 回帰テスト報告は総案例数+百分率を必ず含める
- [feedback_speak_chinese.md](feedback_speak_chinese.md) — 用中文交流
- [feedback_japanese_ui.md](feedback_japanese_ui.md) — 最終成果物は日本語、UI/病名/変数名は日本語で記述
- [feedback_kill_flask_only.md](feedback_kill_flask_only.md) — 重启Flask只杀5000端口进程，不要杀全部python.exe
- [feedback_trinity_audit.md](feedback_trinity_audit.md) — 新変数追加時は9項目の三位一体監査を必ず実施
- [feedback_no_definitive_test_in_eval.md](feedback_no_definitive_test_in_eval.md) — 確定診断検査(活検等)の結果はテスト案例に入れない
- [feedback_never_replace_cases.md](feedback_never_replace_cases.md) — テスト案例は置換禁止、常に追加。全文献案例は貴重
- [feedback_memory_sync.md](feedback_memory_sync.md) — push前にsync_memory.shでmemoryをrepoに同期
- [feedback_dual_test.md](feedback_dual_test.md) — 新案例は伝統Top-3テスト+ナビゲーションテスト(反証推奨)の2種を必ず実施

## ユーザー
- [user_profile.md](user_profile.md) — 用户背景：VeSMed项目负责人，熟悉BN和医学诊断

## プロジェクト状況
- [project_vesmed_status.md](project_vesmed_status.md) — 当前状态：1750辺, 180cases, Top-1 65%, Top-3 93%, FATAL 0
- [project_papers_plan.md](project_papers_plan.md) — 3篇论文计划：NO EDGE(85%), エントロピー(70%), 情報幾何(75%)
- [project_ideas_backlog.md](project_ideas_backlog.md) — 7个未实现点子：timeline/surprise/embedding等
- [project_inference_model_issue.md](project_inference_model_issue.md) — 解決済：超参数grid search + prevalence実験6種全て不採用
- [project_m02_hemodynamic.md](project_m02_hemodynamic.md) — M02血行動態異常：並列sign変数として実装完了
- [project_missing_diseases.md](project_missing_diseases.md) — 未追加の発熱疾患候補(ヒストプラズマ/骨髄腫以降)
- [project_navigation_test.md](project_navigation_test.md) — 新評価軸：推奨検査ナビでTop-1到達+維持できるか（手動テスト、論文ネタ）
- [project_violation_mechanism.md](project_violation_mechanism.md) — 違和感メカニズム：尤度比で対抗仮説を検出→鑑別検査推奨。骨髄腫で検証、未解決課題あり

## 解決済み（今回）
- ~~推奨検査に期待所見表示~~ → 実装済み（best_state + state_details API）
- ~~WebUI state日本語化~~ → 実装済み（160+項目の日本語マッピング）
- ~~超参数問題~~ → grid search解決(dp=0.5, ca=0.3)
- ~~prevalence問題~~ → 6実験で検証、flat 0.01が最適と確認
- ~~見逃し防止~~ → dont_miss機能実装(severity分類+タブ表示)
- ~~M02ショック~~ → 並列sign変数として実装+13案例
- ~~新疾患5種~~ → D105パルボ/D106 DM-PM/D107 HLH/D108 HepB/D109クリプト

## アーカイブ（統合済み）
- [feedback_three_file_sync.md](feedback_three_file_sync.md) — → feedback_project_principles.md に統合
- [feedback_edge_cpt_sync.md](feedback_edge_cpt_sync.md) — → feedback_project_principles.md に統合
- [feedback_cpt_literature.md](feedback_cpt_literature.md) — → feedback_project_principles.md に統合
