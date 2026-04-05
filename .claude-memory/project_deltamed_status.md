---
name: δMed S3 開発状況
description: δMed S3(鑑別診断学習PWA)の実装状況。pair単位カード+max|logLR|+チェックボックス式FSRS。2026-04-03更新。
type: project
---

## 概要
- VeSMedのCPT差異から鑑別問題を自動生成するPWA学習アプリ
- GitHub: https://github.com/itosa-kazu/deltamed (public)
- 公開URL: https://itosa-kazu.github.io/deltamed/
- Stack: Vite 8 + React 19 + TypeScript + Tailwind 4 + Dexie.js + Supabase + ts-fsrs + framer-motion

## 現在の状態（2026-04-03）
- Supabase: 430疾患 / 471変量 / 33対(confusion≥2) / 282 features
- 鑑別力指標: max|logLR| (LR≥2有用, LR<1.5陷阱, Oxford CEBM準拠)
- カード単位: pair (1疾患対=1カード、全鑑別変量を一覧)
- 各conceptに最大LRのstate表示:「← 血小板減少: NHLに5.8倍」
- 評分: チェックボックス式4段階FSRS (正解率→Again/Hard/Good/Easy)
- 報告: 各concept右上に!ボタン → Supabase vesmed_feedbackへ即送信
- Anki式: 全dueカード復習 + 新カード10枚/日
- State名: 550+日本語mapping + 重症度降順ソート
- デプロイ: GitHub Pages (gh-pagesブランチ)
- DATA_VERSION: 5 (自動再ダウンロード機構)

## 配対フィルタ
- confusion≥2回: 229対→33対（真の臨床混淆のみ）
- confusion=1は偶然の可能性が高く教学価値が低い

## デプロイパイプライン
1. `PYTHONIOENCODING=utf-8 python3 vesmed_export.py --output deltamed_export --with-confusion`
2. `python3 upload_to_supabase.py` (confusion≥2フィルタ内蔵)
3. db.tsのDATA_VERSIONを+1
4. `cd deltamed && npm run build && cp dist/index.html dist/404.html && npx gh-pages -d dist`

## S3出題方式
- **学習単位**: pair — 疾患対の全鑑別体系を一括学習
- **題目**: 「A vs B — 鑑別に有用な所見をすべて挙げよ」
- **答え**: 全useful変量一覧（チェックボックス+最大LR state表示）+ butterfly chart + 陷阱情報
- **評分**: 想起できた変量をチェック → 正解率でFSRS自動評分
- **報告**: 各conceptの!ボタンでCPT問題を即報告
- **指標**: max|logLR| (臨床的尤度比ベース、Oxford CEBM準拠)

## 解決済み
- IndexedDB v1→v2互換 + orphaned FSRS cards
- CPT state名不一致: 21変量84疾患修正
- D76(輸血反応) S07 severe: 0%→5% (文献ベース)
- State日本語化 + 重症度降順ソート
- DATA_VERSION自動再ダウンロード機構
- TVD→max|logLR|移行
- 補0問題: 欠落stateに0%を入れるとLR虚高になる（要注意）

## 未実装
- Auth / Sync engine / PWA
- Level 2/3/4
- Browse/Stats改善
- 補0 stateの全面見直し（192箇所）
