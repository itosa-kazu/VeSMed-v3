# VeSMed V3 — Claude Code プロジェクト指示

## 言語
- 用中文交流
- 最終成果物（UI/病名/変数名）は日本語

## Memory
このプロジェクトのメモリファイルは `.claude-memory/` に格納されています。
新しいマシンでセットアップする場合は、以下を実行してください：
```bash
# .claude-memory/ の内容をローカルのメモリディレクトリにコピー
mkdir -p ~/.claude/projects/$(pwd | tr '/' '-' | sed 's/^-//')/memory
cp .claude-memory/*.md ~/.claude/projects/$(pwd | tr '/' '-' | sed 's/^-//')/memory/
```

## 6大鉄則
1. **テスト案例は実症例のみ** — PMC/NEJM/BMJ等の文献、Synthetic禁止
2. **CPT変更は文献必須** — 既存CPT変更にはPMC/教科書の裏付け必要
3. **Evidence変数IDはstep1で確認** — ID存在・state名一致を検証
4. **三件套同期** — step1/step2/step3は完全一体で同時変更
5. **辺+CPT同時追加** — 辺だけ足してCPTなしは禁止
6. **新疾患追加時はreal case必須** — WebSearchでPMC case report検索→テスト案例追加

7. **CPT補0禁止** — 欠落stateに0%を機械的に補填禁止（LR虚高の原因）。必ず文献検索して正確な値を設定

## 情報源追跡の鉄律（全環節貫通）
- **全辺に文献根拠必須** — source_edge(辺の存在根拠) + source_cpt(CPT値の根拠)を分離記録
- **情報源レベル明示** — SR(Systematic Review) > NR(Narrative Review) > TB(Textbook) > CS(Case Series)。降級は必ずtypeで標記
- **CPT値は実数カウント(n/N)必須** — 定性描述("common","rare"等)からの主観的変換は禁止。SRに頻度なし→引用元の原始研究を追う
- **SR選定は全候補記録** — 複数SR存在時は最新+最大N+PRISMA準拠を選定。全候補と選定理由をJSONに記録
- **データ提取はプログラム化必須** — Claude WebFetchで論文データを直接提取しない。PMC API+Python解析 or OCR APIで構造化データを取得し、Claudeは構造化データから選択するだけ
- **想定外事象は即停止・報告** — 設計時の想定外が発生したら自己判断で回避せず必ずユーザーに報告

## その他の鉄則
- **テスト案例は置換禁止、常に追加** — 全文献案例は貴重
- **確定診断検査の結果はテスト案例に入れない** — 活検等
- **新変数追加時は9項目の三位一体監査** — IDF健全性チェック含む
- **回帰テスト報告は総案例数+百分率を含める**
- **Flask再起動は5000番ポートのみkill** — 全python.exeをkillしない
- **変量State設計鉄律** — 三層構造: Finding(absent/presentのみ) / Measurement(cutoff区間、absentなし) / Satellite(親Finding=present時のみ、分類or分級、absentなし)。異なる臨床問題は別変量。absent+severity混合禁止。Satellite設定時は親Findingを自動present化
- **辺追加後は `python3 validate_edges.py` 必須** — 疾患IDの名前衝突・孤立CPT・重複辺を検出
- **辺のfrom_nameは疾患IDマスタから引く** — 手動入力禁止、step2のfrom既存辺から正規名を取得
- **新疾患追加/疾患分割時はR01+R02必須** — full_cptsにR01(年齢7区分)とR02(性別)を必ず追加。per-R個別フォーマット使用
- **revert禁止** — 回帰テストが悪化してもrevertにはユーザ承認が必要

## バージョン時間軸

### v3.0（現行 〜2026-04-05）
- 430疾患(D01–D436)、901変量、8201辺、R01/R02全430疾患Prior完備
- 1268案例(1262 in-scope + 6 OOS)
- Top-1: 988/1262(78%), Top-3: 1177/1262(93%), FATAL: 0
- 変量state設計: 混在あり（absent+severity等）、歴史的経緯で非統一
- 反証推奨(falsification test)実装済み
- T01泛化済み: fever_duration→symptom_duration（非発熱疾患にも適用）
- A群+B群+C群+D群疾患分割完了

### v3.1（大清洗後 — 計画中）
- **変量再設計**: 三層構造(Finding/Measurement/Satellite)で全変量統一
- **辺+CPT全面刷新**: UpToDate主軸+PMC補完、hot-swap overlay方式
- **情報源完全追跡**: 全辺にsource_edge+source_cpt+PMID+excerpt
- v3.0の鉄則・feedback は全てv3.1に継承（データが変わるだけ、原則は不変）

### 共通（v3.0/v3.1両方）
- δMed S3連携: vesmed_export.py → Supabase → δMed PWA
- δMed公開URL: https://itosa-kazu.github.io/deltamed/
- δMed鑑別力指標: max|logLR|（Oxford CEBM準拠、LR≥2有用/LR<1.5陷阱）
- δMed配対: confusion≥2回の33対（真の臨床混淆のみ）

## δMed更新パイプライン（CPT/辺/疾患変更後は必ず実行）
```bash
# 1. VeSMedからエクスポート
PYTHONIOENCODING=utf-8 python3 vesmed_export.py --output deltamed_export --with-confusion
# 2. Supabaseへアップロード（confusion≥2フィルタ内蔵）
python3 upload_to_supabase.py
# 3. deltamed/src/lib/db.ts の DATA_VERSION を +1
# 4. δMedビルド+デプロイ
cd ~/Desktop/deltamed && npm run build && cp dist/index.html dist/404.html && npx gh-pages -d dist
```

## 未実施の疾患分割
- **D02(細菌性髄膜炎)** — 肺炎球菌/髄膜炎菌/GBS等に分割が必要

## 重要な研究方向
- **反証推奨** — エントロピー増大方向の検査推奨（波普尔証伪の初の計算実装、論文化予定）
- **ナビゲーションテスト** — 推奨検査を追ってTop-1到達+維持できるか
- **違和感メカニズム** — 尤度比で対抗仮説を検出
