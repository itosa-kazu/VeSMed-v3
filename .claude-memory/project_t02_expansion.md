---
name: T02 4state化計画
description: T02(発症速さ)を2state→4stateに拡張する計画。自動マッピングは失敗、手動CPT設定が必要。
type: project
---

## 計画
T02を2state(sudden_hours/gradual_days)→4stateに拡張:
- sudden_minutes: 超急性(秒~分) — SAH/大動脈解離/心停止/PE
- acute_hours: 急性(時間~1-2日) — 感染症/中毒/急性腹症
- subacute_weeks: 亜急性(数日~数週) — 結核/自己免疫/亜急性感染
- chronic_months: 慢性(数週~数月) — 腫瘍/変性疾患

## 実験結果（2026-03-16）
- T01のCPTを参考に自動マッピング → Top-1 519→511(-8), Top-3 625→621(-4), FATAL 2
- **自動マッピングは精度不足で失敗**
- 290疾患のCPTを手動で4値に設定する必要がある

## 必要な作業
1. step1: T02 states変更
2. step3: 290疾患のT02 CPTを手動で4値設定（臨床判断必須）
3. 案例: 597件のT02 evidenceを手動でリマップ（vignetteを読んで判断）
4. leak値の再設定

## スクリプト
- expand_t02_4states.py（自動版、失敗→参考用に残す）
