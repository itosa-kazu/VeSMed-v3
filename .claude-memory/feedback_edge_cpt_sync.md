---
name: 辺追加時はCPTも必ず同期
description: step2に辺を追加したら必ずstep3のparent_effectsも同時に追加すること。辺だけ足してCPTなしは推論に反映されない。
type: feedback
---

辺(step2)を追加する際は、必ずstep3のnoisy_or_params内の対応するparent_effectsも同時に追加すること。
辺だけあってCPTがないと、推論エンジン(bn_inference.py)はその辺を使えない。
validate_bn.pyのEDGE_NO_CPTチェックで検出可能。

## 辺追加時の追加ルール
1. **from_nameは既存辺から取得**: 同一disease IDの既存辺のfrom_nameをコピーする。手動入力禁止。
   - 理由: D147(精巣捻転)にD145(尿管結石)のfrom_nameが混入した事故の教訓
2. **辺追加後は `python3 validate_edges.py` 必須**: 名前衝突・孤立CPT・重複辺を検出
   - エラー数が増加していないことを確認してからcommit
