---
name: split-disease
description: VeSMed疾患分割。umbrella疾患を臨床的に独立したIDに分割する完全ワークフロー。step1/step2/step3/noisy_or_params/案例再マッピング/PMC案例検索を一体で実施。
---

# 疾患分割ワークフロー

$ARGUMENTS に分割元の疾患ID(D###)を指定。複数指定可。
引数なしの場合、`memory/project_disease_split_plan.md` から次の候補を選ぶ。

## 前提チェック（省略禁止）

```bash
# 現在のbaselineを確認・記録
python bn_inference.py  # Top-1/Top-3/FATAL を記録
```

---

## Phase 1: 分割設計（コード前）

### 1.1 分割案の決定

元疾患のstep1定義・step2辺・step3 CPT・test case全体を読み、以下を決定:

| 決定事項 | 内容 |
|---------|------|
| 新疾患ID | D351〜D358等（現在の最大ID+1から） |
| 新疾患名 | `name`(英語) + `name_ja`(日本語) |
| 案例再マッピング | 既存案例のexpected_idをどちら/どれに振るか |
| 差別化ポイント | 2疾患を分ける臨床的鍵（辺/CPTの差分） |
| Prior分割 | P(combined) ≈ P(sub1) + P(sub2) |

### 1.2 差別化ポイントの明文化

分割する意味＝**鑑別可能性**。以下を明記:
- 「変量Xで A=高, B=低」（例: S39下肢腫脹 DVT=0.90, PE=0.30）
- 最低2つの差別化変量がないと分割の意味なし

---

## Phase 2: 分割スクリプト作成・実行

`split_D{id}.py` を作成する。以下4セクションを含む。

### 2.1 step1: 変数定義

```python
# 1. 元疾患をrename（name, name_ja, icd10, key_features）
# 2. 新疾患を追加（disease list末尾に挿入）
# 3. 新state追加が必要なら既存変数のstates配列を拡張（例: E40にSVT/VT追加）
```

**新state追加時の注意**: 全既存noisy_or_params parent_effectsに新stateの確率0.0を追加必要。

### 2.2 step2: 辺の分割

```python
# 1. 元疾患の辺を全削除
# 2. 各子疾患用の辺を新規作成（コピーではなく疾患特異的に再設計）
# 3. 共通辺はそれぞれに作成（reason文を疾患固有に）
# 4. 差別化辺は片方のみ or CPT値を大きく変える
```

**辺数の目安**: 各子疾患に最低10辺。元の辺数と大きく変わらないこと。

### 2.3 step3: CPT分割（3箇所 + noisy_or_params）

```python
# === (A) root_priors ===
# 元のpriorを疫学に基づき分割
# P(combined) ≈ P(sub1) + P(sub2)

# === (B) full_cpts ===
# 元のflat/conditional priorを分割

# === (C) noisy_or_params（存在する場合） ===
# 元疾患が noisy_or_params に含まれていれば分割

# === (D) ★最重要★ noisy_or_params parent_effects ===
# 元疾患がparent_effectsに含まれている証拠変数を全て列挙
# 各証拠変数のparent_effectsに新疾患のエントリを追加
# コピー後、差別化ポイントに応じて値を調整
```

**致命的教訓**: (D)を忘れると新疾患は推論で完全に不可視になる（rank 330+）。
A群分割でHL/UC/DVTの3回この罠にはまった。**必ずチェック**:

```python
# 検証コード
nop = step3['noisy_or_params']
new_id = 'D355'
count = sum(1 for v in nop if new_id in nop[v].get('parent_effects', {}))
assert count > 0, f"{new_id} has 0 parent_effects — will be INVISIBLE!"
```

### 2.4 案例再マッピング

```python
# expected_id を適切な子疾患に変更
# evidence値の変更が必要な場合も対応（例: E40='AF' → E40='SVT'）
```

---

## Phase 3: 回帰テスト（ゼロ劣化確認）

```bash
python bn_inference.py  # 全案例
```

| チェック項目 | 許容範囲 |
|------------|---------|
| Top-1 | 前回と同じ or +1以上 |
| Top-3 | 前回と同じ or +1以上 |
| FATAL | 0 |
| EDGE_NO_CPT | 0 |
| CPT_NO_EDGE | 0 |

**1案例でも悪化したら原因調査**（ゼロ劣化原則）。
よくある原因:
- noisy_or_params parent_effects未追加 → Phase 2.3(D)
- Prior分割が不均衡 → full_cpts/root_priors調整
- 差別化辺のCPT値が極端 → 緩和

---

## Phase 4: PMC案例検索（絶対省略禁止）

各**新疾患**について:
1. Agent toolでバックグラウンドPMC検索（並列実行）
2. 各疾患3件以上、見つかれば全部追加
3. /find-cases スキルのStep 2-5に従う

**案例追加後の再テスト**:
```bash
python validate_cases.py    # ERROR 0
python bn_inference.py --case R### R### ...  # 新案例
python bn_inference.py       # 全案例回帰
```

---

## Phase 5: commit push

```bash
git add step1_fever_v2.7.json step2_fever_edges_v4.json step3_fever_cpts_v2.json \
        real_case_test_suite.json split_D*.py add_split_cases*.py fix_D*.py
git commit  # メッセージに: 分割内容、疾患数、辺数、案例数、Top-1、Top-3、FATAL
git push
```

---

## チェックリスト（全項目必須）

### 分割実行
- [ ] step1: 元疾患rename + 新疾患追加
- [ ] step2: 辺を疾患特異的に再設計（各10辺以上）
- [ ] step3 root_priors: Prior分割 P(A)+P(B)≈P(combined)
- [ ] step3 full_cpts: flat/conditional prior分割
- [ ] step3 noisy_or_params: 元疾患のエントリを分割（存在する場合）
- [ ] **step3 parent_effects: 新疾患を全関連証拠変数に追加（最重要）**
- [ ] 新state追加時: 全既存parent_effectsに0.0追加
- [ ] 案例expected_id再マッピング
- [ ] evidence値の更新（state名変更がある場合）

### テスト
- [ ] validate_cases.py ERROR 0
- [ ] bn_inference.py 全案例回帰: Top-1/Top-3 維持 or 改善
- [ ] FATAL 0
- [ ] 分割対象案例を個別テスト

### 案例
- [ ] 各新疾患のPMC案例検索agent起動
- [ ] 各新疾患3件以上追加
- [ ] 新案例validate + テスト

### 完了
- [ ] commit push
- [ ] memory/project_disease_split_plan.md 更新
- [ ] memory/project_vesmed_status.md 更新

---

## よくある失敗パターン

| 症状 | 原因 | 対処 |
|------|------|------|
| 新疾患がrank 300+ | parent_effects未追加 | Phase 2.3(D)を実行 |
| 元Top-1案例がTop-3に落ちた | 確率質量の分散（NHL/HL等） | 差別化辺のCPT強化、案例追加で回復 |
| 新案例がFATAL | 近縁疾患との競合 | 差別化変量の辺/CPT調整 |
| EDGE_NO_CPT > 0 | step2に辺追加、step3にCPTなし | 三位一体で同期 |
| 既存案例regression | Prior分割の不均衡 | full_cpts/root_priors微調整 |
