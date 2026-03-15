---
name: CPT修正は文献必須+辺追加時CPT同期
description: 既存CPTの変更は文献エビデンス必須。辺追加時は必ずCPTも同時追加。鉄則。
type: feedback
---

1. 既に書かれたCPTを変更する場合、必ず文献（PMC case series, CDC criteria, systematic review等）の裏付けが必要。直感や推測で変更してはならない。
2. step2に辺を追加したら、必ずstep3にもCPTを同時追加する。辺だけ追加してCPTなしは禁止。

**Why:** CPTは一度書き込むと簡単に変えられない。根拠なき変更はモデル全体の信頼性を損なう。辺とCPTの不整合はbuild_model時にデフォルト値(0.001)が使われ、推論を破壊する（D24→L11バグの教訓）。

**How to apply:** 辺追加作業では常に step2 + step3 をセットで編集。CPT値は文献の頻度データから導出し、出典を明記する。
