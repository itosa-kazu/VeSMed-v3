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

## その他の鉄則
- **テスト案例は置換禁止、常に追加** — 全文献案例は貴重
- **確定診断検査の結果はテスト案例に入れない** — 活検等
- **新変数追加時は9項目の三位一体監査** — IDF健全性チェック含む
- **回帰テスト報告は総案例数+百分率を含める**
- **Flask再起動は5000番ポートのみkill** — 全python.exeをkillしない
- **検査値変量のstate設計は因材施教** — まず変量固有の黄金分級を文献検索、なければCTCAE準拠4-state(xULN基準)をfallback
- **辺追加後は `python3 validate_edges.py` 必須** — 疾患IDの名前衝突・孤立CPT・重複辺を検出
- **辺のfrom_nameは疾患IDマスタから引く** — 手動入力禁止、step2のfrom既存辺から正規名を取得

## 現在の状態
- 345疾患(D01-D350)、792変量、6111辺、105疾患にR→D prior
- 712案例(708 in-scope + 4 OOS)
- Top-1: 562/708(79%), Top-3: 662/708(94%), FATAL: 0
- 反証推奨(falsification test)実装済み

## 重要な研究方向
- **反証推奨** — エントロピー増大方向の検査推奨（波普尔証伪の初の計算実装、論文化予定）
- **ナビゲーションテスト** — 推奨検査を追ってTop-1到達+維持できるか
- **違和感メカニズム** — 尤度比で対抗仮説を検出
