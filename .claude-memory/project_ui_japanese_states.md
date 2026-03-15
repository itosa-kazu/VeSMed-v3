---
name: WebUI変数stateを日本語表示に変更
description: 現在absent/present等の英語表記を日本語に変換して表示する改善案
type: project
---

WebUI上のevidence変数のstate名が英語のまま(absent, present, mild, severe等)で分かりにくい。
日本語表示に変換する必要がある。

**Why:** ユーザーが英語stateを読みにくいと感じている
**How to apply:** step1のstatesに日本語名を追加するか、フロントエンドで英語→日本語マッピングテーブルを用意して表示時に変換
