---
name: fix-fatal
description: FATAL/MISS案例の修復ワークフロー。原文回帰→CPT比較→文献調査→競合回帰→修正の5ステップ。
user_invocable: true
---

# FATAL/MISS修復ワークフロー

引数で案例ID（例: R751）を指定。指定なしの場合は全FATAL案例を対象。

## Step 1: 現状把握

```bash
PYTHONIOENCODING=utf-8 python3 bn_inference.py 2>&1 | grep -E "FATAL|SUMMARY"
```

対象案例のevidence、expected_id、現在のrankを確認。

## Step 2: 原文回帰（最重要）

対象案例のPMC論文を**必ずWebFetchで原文取得**して全文を読み直す。

チェック項目:
- [ ] vignette記載と原文の数値照合（転記ミス、数値入替がないか）
- [ ] 原文にあるのにevidenceに入っていない所見の洗い出し
- [ ] 特に基本所見: E13(LAD), E14(脾腫), E34(肝腫大), L01(WBC), L100(PLT), L02(CRP), L22(貧血)
- [ ] evidenceに入っているが原文に根拠がない所見がないか

**遗漏所見が見つかったら即座にevidenceに追加。**

## Step 3: 競合疾患CPT比較

正解疾患 vs Top-3競合疾患のCPTを全evidence変数で比較表を作成:

```python
# noisy_or_paramsから各疾患のCPTを抽出
for ev_id, obs_state in case_evidence.items():
    nop[ev_id]['parent_effects'][disease_id]  # 各疾患のCPT
```

**最大のCPT差を持つ変数を特定** → これが修正候補。

## Step 4: 文献調査（CPT修正には文献必須）

差が大きい変数について:
1. 正解疾患の文献頻度を調べる
2. 競合疾患の文献頻度も調べる（**競合のCPTが過大な可能性**も考慮）
3. 大規模コホート研究・系統的レビュー・教科書を優先
4. PMID/PMC IDを必ず記録

**文献なきCPT修正は禁止。**

## Step 5: 競合案例の回帰チェック

CPT変更対象の疾患について:
1. その疾患の**全テスト案例**を列挙
2. 変更するevidence変数を使っている案例を特定
3. 特にTop-1が僅差の案例は要注意

## Step 6: 修正実施

1. Evidence補完（原文遗漏）→ real_case_test_suite.json
2. CPT修正 → step3_fever_cpts_v2.json (noisy_or_params)
3. 新辺追加 → step2_fever_edges_v4.json + step3同時
4. 回帰テスト実行

## Step 7: 退化案例の修復

退化が発生したら:
1. **退化案例の原文もWebFetchで回帰検査**（Step 2と同じ手順）
2. 遗漏所見があれば追加
3. 遗漏所見で修復できない場合のみ、CPT微調整を検討

**鉄則: 正しいCPT修正を撤回して退化を隠すのは過拟合。退化は原文回帰で正面解決。**

**鉄則: 原文所見のrevert禁止。**
- 原文にある所見は**必ず追加**する。rankが下がっても所見を隠してはいけない（過拟合）
- rank低下 ≠ モデルの誤り。競合疾患が臨床的に上位なら低rankは正しい判断
- rankが不当に低い場合は**正解疾患に辺を追加**して解決（文献必須）。所見を隠すのではなくモデルの知識を補完する

## 成功判定

- [ ] 対象FATAL案例がTop-3以内に入った
- [ ] 全案例の回帰テストでTop-1/Top-3/FATALが悪化していない
- [ ] 全CPT修正に文献根拠がある
- [ ] validate_edges.py がエラー0
