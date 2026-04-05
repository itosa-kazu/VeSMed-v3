---
name: VeSMed バージョン時間軸
description: v3.0(現行)とv3.1(大清洗後)の状態・計画。原則はバージョン不変、データのみ刷新。
type: project
---

## v3.0（現行 〜2026-04-05）

- 430疾患(D01~D436、D05廃止)、901変量、8201辺
- 推理引擎: bn_inference.py (Noisy-OR log-LR + IDF dp=0.7 + CF ca=2.5 + PP=0.3)
- 1268案例 (1262 in-scope, 6 OOS)
- Top-1 988/1262(78%), Top-3 1177/1262(93%), FATAL 0
- R→D Prior: 全430疾患に年齢/性別prior設定済み
- 変量state設計: **混在あり**（absent+severity混合、absent+type混合が歴史的に存在）
- δMed連携: vesmed_export.py → Supabase → δMed PWA
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git

## v3.1（大清洗後 — 計画段階）

### Phase 0: 変量再設計
- 三層構造(Finding/Measurement/Satellite)で全変量を統一的に再設計
- Finding = absent/present のみ
- Measurement = 標準cutoff区間（absentなし）
- Satellite = 親Finding=present時のみ、分類or分級（absentなし）
- UI連動: Satellite設定時は親Findingを自動present化

### Phase 1-430: 逐疾患データ刷新
- UpToDate主軸 + PMC補完
- hot-swap overlay方式（dense_audit/D{xxx}.json）
- 全辺にsource_edge + source_cpt + PMID + excerpt
- CPT分級: Gold(直接%)/Silver(範囲→中央値)/Bronze(定性→引用追跡)

### バージョン間の関係
- **原則(feedback/鉄則)**: v3.0で確立したもの全てv3.1に継承。原則はバージョン不変
- **データ(辺/CPT/変量state)**: v3.1で全面刷新。旧データはhot-swapで段階的に置換
- **架構(推論エンジン)**: 変更なし（ユーザー承認なしに変更禁止）
