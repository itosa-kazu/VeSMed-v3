---
name: 辺追加時はCPTも必ず同期
description: step2に辺を追加したら必ずstep3のparent_effectsも同時に追加すること。辺だけ足してCPTなしは推論に反映されない。
type: feedback
---

辺(step2)を追加する際は、必ずstep3のnoisy_or_params内の対応するparent_effectsも同時に追加すること。
辺だけあってCPTがないと、推論エンジン(bn_inference.py)はその辺を使えない。
validate_bn.pyのEDGE_NO_CPTチェックで検出可能。
