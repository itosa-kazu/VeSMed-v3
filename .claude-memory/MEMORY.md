# Memory Index

## 鉄則・フィードバック
- [feedback_source_level_traceability.md](feedback_source_level_traceability.md) — **全辺にPMID+情報源レベル(SR/NR/TB)+excerpt必須。降級源は明示的標記。全環節貫通の鉄律**
- [feedback_structure_follows_invariants.md](feedback_structure_follows_invariants.md) — **架構三鉄律(通用)**: 結構はDomain Invariantsに従う/演進は加法のみ/補丁は架構bugの症状。Plato "carving at joints"
- [feedback_project_principles.md](feedback_project_principles.md) — VeSMed 6大鉄則：実症例のみ/CPT文献必須/変数ID確認/三件套同期/辺+CPT同時/新疾患追加時real case必須
- [feedback_regression_report_format.md](feedback_regression_report_format.md) — 回帰テスト報告は総案例数+百分率を必ず含める
- [feedback_speak_chinese.md](feedback_speak_chinese.md) — 用中文交流
- [feedback_japanese_ui.md](feedback_japanese_ui.md) — 最終成果物は日本語、UI/病名/変数名は日本語で記述
- [feedback_disease_names_japanese.md](feedback_disease_names_japanese.md) — 疾患名はユーザーとの会話で必ず日本語表記
- [feedback_kill_flask_only.md](feedback_kill_flask_only.md) — 重启Flask只杀5000端口进程，不要杀全部python.exe
- [feedback_trinity_audit.md](feedback_trinity_audit.md) — 新変数追加時は9項目の三位一体監査を必ず実施
- [feedback_no_definitive_test_in_eval.md](feedback_no_definitive_test_in_eval.md) — 確定診断検査(活検等)の結果はテスト案例に入れない
- [feedback_atomicity_principle.md](feedback_atomicity_principle.md) — **変量原子化原則**: 1変量=1臨床観察単位。異なる検体/手技/感度は別変量(喀痰≠BAL)
- [feedback_variable_state_design.md](feedback_variable_state_design.md) — **変量State設計鉄律(対抗検証済)**: 三層構造(Finding=absent/present, Measurement=cutoff区間, Satellite=陽性分岐のみ)。absent+severity混合禁止。5攻撃全却下
- [feedback_variable_granularity.md](feedback_variable_granularity.md) — **変量粒度原則(6攻撃検証済)**: 臨床観察のみ/機制不要。診断評分≠臨床測量尺。治療反応=秒分Finding/時間週D→D。粗細二重計上禁止
- [feedback_not_fever_only.md](feedback_not_fever_only.md) — **最重要: VeSMedは発熱限定ではない**。全疾患対象の包括的システム。「scope外」と判断しない

## 将来タスク
- [project_d05_cap_split.md](project_d05_cap_split.md) — **D05(市中肺炎)は分割/削除が必要**。病原体別ID(D266/D265/D263等)が既にあり冗長
- **L108(膿瘍穿刺液鏡検)** — 将来追加。R933(脳膿瘍ドレナージ)/R935(手術検体)のノカルジアCNS案例を解決する鍵。states: negative/gpc/gnr/afb/branching_filaments/fungal
- [feedback_never_replace_cases.md](feedback_never_replace_cases.md) — テスト案例は置換禁止、常に追加。全文献案例は貴重
- [feedback_max_cases.md](feedback_max_cases.md) — PMCで見つけた案例は全て使う（3件以上は全部追加）
- [feedback_use_all_found_cases.md](feedback_use_all_found_cases.md) — agentが見つけた案例は"次の機会"に残さず全て即追加
- [feedback_no_oos_escape.md](feedback_no_oos_escape.md) — OOS逃避禁止。FATALを正直に受け入れるか、変数追加で正面解決
- [feedback_systematic_edge_audit.md](feedback_systematic_edge_audit.md) — 体系的辺監査: rank2+の全案例で漏れ辺検出→Top-1+36,Top-3+12の劇的改善
- [feedback_no_architecture_change.md](feedback_no_architecture_change.md) — 架構変更禁止：IDF式/推論ロジック等はユーザー承認なしに変更不可
- [feedback_never_skip_cases.md](feedback_never_skip_cases.md) — **最重要**: 新疾患追加後のreal case検索は絶対省略禁止。D197-D251で55疾患分忘れた重大インシデント
- [feedback_no_overfitting.md](feedback_no_overfitting.md) — 辺監査の過拟合禁止：テスト案例のためだけの辺は追加不可。臨床的合理性が独立必要
- [feedback_no_evidence_manipulation.md](feedback_no_evidence_manipulation.md) — 排名改善のための証拠操作禁止。原文所見は全保留、臆測値は除外
- [feedback_disease_addition_methodology.md](feedback_disease_addition_methodology.md) — 疾患追加の標準方法論(6ステップ)。回帰テストはFATALだけでなくTop-1/Top-3推移も確認
- [feedback_memory_sync.md](feedback_memory_sync.md) — push前にsync_memory.shでmemoryをrepoに同期
- [feedback_dual_test.md](feedback_dual_test.md) — 新案例は伝統Top-3テスト+ナビゲーションテスト(反証推奨)の2種を必ず実施
- [feedback_edge_audit_must_use_skill.md](feedback_edge_audit_must_use_skill.md) — **辺監査は必ず/edge-auditスキルで実施**。手動で雑にやると過拟合リスク
- [feedback_no_regression_tolerance.md](feedback_no_regression_tolerance.md) — **ゼロ劣化原則**: 辺追加で1指標でも悪化したら必ず調査。「微減」で流さない
- [feedback_no_indirect_edges.md](feedback_no_indirect_edges.md) — **間接因果禁止**: 転移/DIC等を経由する間接症状に直接辺を張らない
- [feedback_check_duplicates.md](feedback_check_duplicates.md) — **新疾患追加前に重複チェック必須**。5組重複で性能低下した教訓
- [feedback_new_var_disease_list_check.md](feedback_new_var_disease_list_check.md) — **新変量追加後は全疾患リストと手動照合**。S59/S60で17疾患の漏れを発見
- [feedback_no_normal_value_edges.md](feedback_no_normal_value_edges.md) — 正常値辺(WBC正常等)は鑑別力ゼロで逆効果。疾患特異的辺のみ追加
- [feedback_bidirectional_edge_check.md](feedback_bidirectional_edge_check.md) — **辺チェックは双方向**: 変量→疾患 + 疾患→変量。rank最差から優先
- [project_dense_model_plan.md](project_dense_model_plan.md) — 稠密モデル実験結果: leak auto-fillは無効。臨床判断CPTによる漸進的稠密化が正解
- [project_dense_cleanup_pipeline.md](project_dense_cleanup_pipeline.md) — **大清洗pipeline**: UpToDate主軸+PMC補完、1ヶ月集中。CPT分級(Gold/Silver/Bronze)、hot-swap構成。ユーザー=コピペ、Claude=解析+JSON生成
- [project_t02_expansion.md](project_t02_expansion.md) — T02 4state化計画: sudden_minutes/acute_hours/subacute_weeks/chronic_months。自動マッピング失敗→手動CPT必要
- [feedback_keep_experiment_branches.md](feedback_keep_experiment_branches.md) — 実験分支は削除禁止。失敗も保存
- [feedback_evidence_needs_edges.md](feedback_evidence_needs_edges.md) — Evidence追加前に辺の整備を確認。辺なしevidenceはleak値で不利
- [feedback_rd_prior_fairness.md](feedback_rd_prior_fairness.md) — **R→D Prior公平性**: 競合疾患群を同時追加しないとFATAL/大量退化。カテゴリ単位で追加必須
- [feedback_edges_need_literature.md](feedback_edges_need_literature.md) — **新辺も文献必須**: D→変量の新辺はLLM印象ではなくPMC/教科書の根拠が必要
- [feedback_cpt_state_name_sync.md](feedback_cpt_state_name_sync.md) — **CPT state名一致性必須**: step3のstate名がstep1と1文字でも違うとCPT無効化。R715 FATAL原因
- [feedback_no_cherry_pick_edges.md](feedback_no_cherry_pick_edges.md) — **最重要: 臨床正確な辺の撤回禁止**。テスト退化は競合にも辺追加で解決。正しい辺を消すのは過拟合
- [feedback_no_auto_cpt.md](feedback_no_auto_cpt.md) — **CPT数値は人工設定必須**。プログラム自動生成禁止、導入のみ担当
- [feedback_no_umbrella_diseases.md](feedback_no_umbrella_diseases.md) — **疾患混在禁止**: 臨床的に異なる疾患を1IDに入れない。疫学/症状/治療が異なるなら別IDに分割
- [feedback_add_disease_skill_v2.md](feedback_add_disease_skill_v2.md) — **新skill起点**: D370以降は文献検証必須。D368/D369は遡及修正済み。D367以前は未検証
- [feedback_fatal_fix_workflow.md](feedback_fatal_fix_workflow.md) — **FATAL修復5ステップ**: 原文回帰→CPT比較→文献調査→競合回帰→修正。退化時も原文回帰で正面解決
- [feedback_no_rank_worship.md](feedback_no_rank_worship.md) — **排名唯一主義禁止**: rankは鏡であり目的ではない。原文所見は必ず追加、隠すのは過拟合。臨床的に正しい順位は受け入れる
- [feedback_verify_cpt_sources.md](feedback_verify_cpt_sources.md) — **CPT文献は原文fetch必須**: agentのweb search結果を鵜呑みにせず、原文をfetchして百分比を直接確認する
- [project_intermediate_variable_issues.md](project_intermediate_variable_issues.md) — 中間変量問題リスト: 転移(解決)/DIC/心不全/肝不全/腎前性AKI/骨髄浸潤(未解決)

## ユーザー
- [user_profile.md](user_profile.md) — 用户背景：VeSMed项目负责人，熟悉BN和医学诊断

## プロジェクト状況
- [project_vesmed_status.md](project_vesmed_status.md) — **バージョン時間軸**: v3.0(現行430疾患/8201辺/1268案例) → v3.1(大清洗: 変量三層化+UpToDate全面刷新)
- [project_rd_prior_discovery.md](project_rd_prior_discovery.md) — **R→D Prior大発見**: 人口統計prior(年齢/性別)が史上最大の改善レバー。53/345疾患実装済み、全疾患展開が最優先
- [project_variable_audit_pipeline.md](project_variable_audit_pipeline.md) — 変量審計パイプライン: 227新変量導入、CPT_NO_EDGE同期問題の発見と修正
- [project_papers_plan.md](project_papers_plan.md) — 3篇论文计划：NO EDGE(85%), エントロピー(70%), 情報幾何(75%)
- [project_ideas_backlog.md](project_ideas_backlog.md) — 7个未实现点子：timeline/surprise/embedding等
- [project_inference_model_issue.md](project_inference_model_issue.md) — 解決済：超参数grid search + prevalence実験6種全て不採用
- [project_m02_hemodynamic.md](project_m02_hemodynamic.md) — M02血行動態異常：並列sign変数として実装完了
- [project_missing_diseases.md](project_missing_diseases.md) — 未追加の発熱疾患候補(ヒストプラズマ/骨髄腫以降)
- [project_expansion_plan.md](project_expansion_plan.md) — 全疾患展開計画: 呼吸困難→胸痛→腹痛→意識障害。Prior再調整が将来必要
- [project_navigation_test.md](project_navigation_test.md) — 新評価軸：推奨検査ナビでTop-1到達+維持できるか（手動テスト、論文ネタ）
- [project_violation_mechanism.md](project_violation_mechanism.md) — 違和感メカニズム：尤度比で対抗仮説を検出→鑑別検査推奨。骨髄腫で検証、未解決課題あり
- [project_navigation_test_results.md](project_navigation_test_results.md) — ナビテスト全案例結果: 153/228(67%)到達、75件未到達の分類
- [project_pending_splits.md](project_pending_splits.md) — 未実施の疾患分割・追加リスト(AML/ALL分割、MCD/MN/FSGS追加等)
- [project_disease_split_plan.md](project_disease_split_plan.md) — 疾患リスト分割計画: umbrella疾患18件をA/B/C/D群に分類、A群6件から着手
- [project_new_variables_needed.md](project_new_variables_needed.md) — 新変量追加候補: 肺クリプトコッカス等の構造的限界を解決する変量リスト
- [project_next_best_test_perf.md](project_next_best_test_perf.md) — next_best_test性能瓶颈(10-20秒)、預筛选/缓存/C扩展の最適化方向
- [project_causal_disease_overlap.md](project_causal_disease_overlap.md) — 因果疾患重複問題: D273(胆管結石)→D25(胆管炎)等、因果関係疾患が確率を食い合う
- [project_complication_limitation.md](project_complication_limitation.md) — 合併症表現の構造的限界: D→D因果連鎖が表現不可。将来hierarchical BN等で対処
- [project_kokushi_gap_analysis.md](project_kokushi_gap_analysis.md) — **国試×VeSMed缺口分析**: 精神科が最大Gap(うつ病116点+統合失調症104点)。覆盖率71%
- [project_d120_split_needed.md](project_d120_split_needed.md) — D120分割状況: HFpEF(D420)分離済み。残りはHFrEF/原因不明ADHF
- [project_cardiac_gap_analysis.md](project_cardiac_gap_analysis.md) — **心臓系缺口分析**: 18疾患で主要網羅。D215案例9件/D356案例8件追加済み
- [project_melanoma_limitation.md](project_melanoma_limitation.md) — **D423黒色腫の構造的限界**: 皮膚病変変量がなくTop-1 17%。皮膚所見変量追加が必要
- [project_disease_gap_2026_03.md](project_disease_gap_2026_03.md) — **疾患缺口分析**: 全137缺口(A27/B33/C50/D27)。最手薄: 産科/婦人科/眼科/皮膚科/整形
- [project_universal_medical_graph.md](project_universal_medical_graph.md) — **万有医学因果図**: 全医学=1枚のDAG。診断=位置推定、治療=ノード削弱、時間=快照列。合併症は自然消滅。D→D辺追加が鍵
- [project_olfactory_analogy.md](project_olfactory_analogy.md) — **嗅覚類比**: 侧抑制=explaining away=水流。VeSMedに欠ける核心拼図。v3.3で実装予定
- [project_biological_convergence.md](project_biological_convergence.md) — **生物収束進化**: 因果図=生命普遍架構。基因調控/免疫/神経/進化が全て同一解。表観遺伝=CPT修飾
- [project_unsolved_problems_audit.md](project_unsolved_problems_audit.md) — **未解決問題総監査**: 架構級(A1-A5)全解決、変量級(B1-B4)全解決。残りは数据/工程/人力のみ
- [project_v33_adversarial_bio_design.md](project_v33_adversarial_bio_design.md) — **v3.3対抗性テスト(8攻撃)**: 全て生物解法あり。核心: soft lateral inhibition + additive/exclusive所見属性 + unexplained residual検出器
- [project_immune_system_analogy.md](project_immune_system_analogy.md) — **免疫類比【未証実】**: V→V辺/上下文変量は未検証仮説。確定: 免疫=執行者,VeSMed=偵察兵
- [project_olfactory_time_series.md](project_olfactory_time_series.md) — **嗅覚×時間処理(v3.3内建)**: EA+記憶=侧抑制+適応。v4.x不要。未証実仮説は末尾に分離

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
