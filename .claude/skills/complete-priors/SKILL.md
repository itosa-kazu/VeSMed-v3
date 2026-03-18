---
name: complete-priors
description: R01(年齢)/R02(性別)のfull_cpts prior補完。未登録疾患に疫学データを基にCPTを追加。
---

# R01/R02 Prior補完ワークフロー

## 背景
R変数はstep2辺ではなくstep3 `full_cpts` 経由で動作する。
R01(年齢)は176/362疾患、R02(性別)は61/362疾患にしか登録されていない。
未登録 = 全年齢/全性別で等確率 → 臨床的に不正確。

## Step 1: 補完対象の特定

```python
import json
step1 = json.load(open("step1_fever_v2.7.json"))
step3 = json.load(open("step3_fever_cpts_v2.json"))
diseases = [v for v in step1["variables"] if v["category"] == "disease"]
fc = step3.get("full_cpts", {})

# R01未登録疾患
missing_r01 = []
missing_r02 = []
for d in diseases:
    did = d["id"]
    entry = fc.get(did, {})
    parents = entry.get("parents", []) if isinstance(entry, dict) else []
    if "R01" not in parents:
        missing_r01.append(did)
    if "R02" not in parents:
        missing_r02.append(did)
```

$ARGUMENTS で対象を指定:
- `R01` → R01未登録疾患のみ補完
- `R02` → R02未登録疾患のみ補完
- `D58 D67 D107` → 指定疾患のみ補完
- 引数なし → R01から順に全疾患補完

## Step 2: 疫学データ検索（10疾患ずつ）

各疾患について **WebSearch** で疫学データを取得:
- R01用: 「{disease_name} age distribution epidemiology incidence」
- R02用: 「{disease_name} sex ratio male female incidence」

**情報源の優先度:**
1. UpToDate / BMJ Best Practice の疫学セクション
2. PMC review articles
3. 教科書（Harrison's, Cecil等）
4. 各国の疫学統計

## Step 3: CPT値の設定

### R01(年齢) CPTテンプレート
```json
{
  "parents": ["R01"],
  "description": "{疾患名}。{疫学的特徴の要約}",
  "cpt": {
    "0_1": 0.001,
    "1_5": 0.001,
    "6_12": 0.001,
    "13_17": 0.001,
    "18_39": 0.01,
    "40_64": 0.02,
    "65_plus": 0.03
  }
}
```

### R02(性別) の追加方法
既にR01がある場合は `parents` に R02 を追加し、CPTを展開:
```json
{
  "parents": ["R01", "R02"],
  "cpt": {
    "18_39|male": 0.015,
    "18_39|female": 0.005,
    "40_64|male": 0.025,
    "40_64|female": 0.015,
    ...
  }
}
```

### CPT値の決め方
- **相対比が重要**（絶対値はBASE_PRIORとの比で自動調整される）
- 好発年齢層に高い値、稀な年齢層に低い値
- 性差が明確な場合のみR02追加（SLE→F:M=9:1、痛風→M:F=10:1等）
- **性差が不明確・軽微な疾患はR01のみでOK**（無理にR02を追加しない）

### セパレータの注意
- R01+R02の複合CPTキーは `|` セパレータ: `"18_39|male": 0.01`
- 小児年齢(0_1〜13_17)で性差が不要な場合は `,` セパレータ: `"0_1,male": 0.001`
- 既存CPTのセパレータ慣習に従うこと

## Step 4: step3への書き込み

`step3_fever_cpts_v2.json` の `full_cpts` セクションを編集:
- 既存エントリがある場合: `parents` にR01/R02を追加し、`cpt` を展開
- エントリがない場合: 新規作成
- **既存の他のR変数(R04等)を消さないこと**

## Step 5: 回帰テスト

```bash
python3 bn_inference.py
```

**確認項目:**
- Top-1, Top-3, FATAL の全指標
- **1件でも悪化したら原因調査** → CPT値の調整 or 撤回
- 回帰テスト報告は「総案例数 + 百分率 + 前回比」を含める

## Step 6: commit & push

10疾患ずつcommit:
```
prior: add R01/R02 priors for D58-D67 (10 diseases) → Top-1 XXX/801 (+N)
```

## 注意事項

- **R03〜R48は対象外** — 特徴的関連のみでOK、全疾患補完は不要
- **full_cptsのキー順序を保つ** — 既存の並び順を崩さない
- **descriptionフィールドは必須** — 疫学的根拠の要約を含める
- **年齢7区分すべてに値を設定** — 欠落するとget_priorでNone返却
- **BASE_PRIOR(0.01)との比で考える** — CPT値0.03なら3倍、0.003なら0.3倍
