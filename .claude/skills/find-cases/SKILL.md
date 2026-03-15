---
name: find-cases
description: PMCからreal case reportを検索してtest suiteに追加。疾患IDまたは疾患名を引数で指定。
---

# 案例検索ワークフロー

$ARGUMENTS に疾患ID(D###)または疾患名を指定。

## Step 1: PMC検索

Agent toolでバックグラウンド検索:
- 各疾患3件以上、できれば5件
- 異なる臨床像（典型/非典型/合併症）を含む
- 成人症例のみ（小児は除外、ただし16歳以上は可）

検索URL: `https://www.ncbi.nlm.nih.gov/pmc/?term={disease}+case+report`

## Step 2: 案例データ抽出

各案例から必須項目:
- Source/PMCID（必須。出典なしは禁止）
- age/sex
- vital signs (T, HR, BP, RR, SpO2)
- key symptoms
- labs
- final diagnosis

## Step 3: Evidence変数マッピング

step1の変数定義を参照して:
- 各所見を変数ID+state値にマッピング
- **変数IDの存在とstate値の合法性をstep1で確認**（鉄則3）
- 確定診断検査の結果は入れない（鉄則: 活検/培養確定結果は除外）

## Step 4: validate + テスト

```bash
python validate_cases.py  # ERROR 0確認
python bn_inference.py --case R### R### ...  # 新案例テスト
```

FATALがあれば辺追加で解消。OOS逃避禁止。

## Step 5: 全案例全部追加

**見つかった案例は選別せず全て追加する。**「主要なものから」「ベスト3だけ」は禁止。
案例は多ければ多いほど良い。
