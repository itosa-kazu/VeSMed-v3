---
name: VeSMedプロジェクト鉄則（6原則）
description: テスト案例は実症例のみ、CPT変更は文献必須、Evidence変数IDはstep1確認必須、三件套同期、辺+CPT同時追加、新疾患追加時は必ずreal case検索
type: feedback
---

## VeSMed 6大鉄則

### 1. テスト案例鉄則: 真実症例のみ
テストスイート(real_case_test_suite.json)に入れる案例は、PMC/NEJM/BMJ等の文献に基づく実症例のみ使用可。
Synthetic（合成）症例や国試問題は使用禁止。

**Why:** 実臨床データでなければモデルの真の性能を評価できない。LLM生成や国試は分布が偏る。
**How to apply:** 案例追加時は必ずPMCIDまたはDOIを記載。出典が示せない案例は追加しない。

### 2. CPT修正鉄則: 既存CPT変更は文献エビデンス必須
既に書かれたCPT値を変更する場合、PMC/教科書/UpToDate等の文献裏付けが必要。
新規の辺+CPT追加は医学知識に基づいて可能だが、根拠を明記すること。

**Why:** CPTは一度書き込むと簡単に変えられない。根拠なき変更はモデル全体の信頼性を損なう（D24→L11バグの教訓）。
**How to apply:** CPT変更時は出典を明記。直感や推測での変更は禁止。

**教訓(2026-03-15):** D149 CO中毒のL53(トロポニン)CPTをFATAL修正のために文献確認なしで変更してしまった。結果的にFATALは解消したが、CPT値の根拠がない。新規CPTは医学知識で許容されるが、既存CPTの変更は必ず文献を先に確認すること。「FATALを消すため」という結果駆動のCPT変更は小細工と同質。

### 3. Evidence変数ID鉄則: step1で必ず確認
caseのevidence/risk_factorsに変数IDを入れる時、必ずstep1のID・name・statesを確認してから入れる。

**Why:** 存在しないIDや無効なstate名を入れると、推論エンジンが無視するかエラーになる（L11 "elevated"バグの教訓）。
**How to apply:** 案例作成時、各evidence項目について step1 JSON で ID存在・state名一致を検証する。

### 4. 三件套同期鉄則: 節点・辺・CPTは三位一体
step1(節点) / step2(辺) / step3(CPT) は完全一体。一つ変えたら他も必ず查缺補漏：
- 辺追加 → CPT(parent_effects)も同時追加 + step1のstates確認
- 節点states変更 → 辺とCPTも同期更新
- CPT変更 → 辺の存在を確認

**Why:** 不整合があるとbuild_model時にデフォルト値(0.001)が使われ推論を破壊する。
**How to apply:** 編集は常にstep2 + step3をセットで。validate_bn.pyで検証。

### 5. 辺+CPT同時追加鉄則
step2に辺を追加したら、必ずstep3のparent_effectsも同時追加。辺だけ足してCPTなしは禁止。

**Why:** CPTなし辺は推論エンジンに使われない。validate_bn.pyのEDGE_NO_CPTで検出可能。
**How to apply:** 辺追加作業は常にstep2 + step3のペア編集。

### 6. 新疾患追加時テスト案例必須鉄則
新疾患をモデルに追加したら、必ずPMC等からreal caseを検索してテスト案例を作成する。疾患追加だけでテスト無しは禁止。

**Why:** テスト案例なしでは新疾患の推論精度が検証できない。回帰テストだけでは新疾患の動作確認にならない。
**How to apply:** 疾患追加スクリプト実行後、WebSearchでPMC case reportを検索→evidence抽出→real_case_test_suite.jsonに追加→推論テスト実行。

### 7. テスト案例は発熱案例に限定しない
モデルに収録されている疾患であれば、無熱の案例でもテストに使用可能。システムは発熱鑑別に特化しているが、発熱以外の所見のみでも動作する汎用的な鑑別診断システムである。

**Why:** 心筋炎等は先行感染の発熱が治まった後に発症することが多く、来院時無熱でも臨床的に重要な鑑別対象。無熱案例を排除するとモデルの評価が不完全になる。
**How to apply:** 案例検索時に「fever」で絞り込みすぎない。疾患がモデルにあれば使用OK。
