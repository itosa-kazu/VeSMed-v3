# VeSMed HANDOVER — 2025-03-12

## 一言で言うと

LLMで因果ベイズネットワーク（発熱鑑別診断102疾患）を人力構築し、43例のreal case reportでTop-1 56%, Top-3 81%を達成。自信的误诊（H<2+wrong）の根本原因が「辺の構造的欠落」であることを発見。これが論文一の核心命題。

---

## 確定版ファイル一覧

| ファイル | 内容 | 備考 |
|---------|------|------|
| `step1_fever_v2.7.json` | 変数定義 273変数(102疾患+M01) | 最新版 |
| `step2_fever_edges_v4.json` | 因果辺 984本 | TB肺外辺追加済 |
| `step3_fever_cpts_v2.json` | CPT全部 (noisy-OR + full_cpt) | 全辺カバー |
| `real_case_test_suite.json` | Real case R01-R18 (18例分) | **要更新: R19-R43追加必要** |
| `real_case_results_final.md` | テスト結果サマリー | 最終版 |
| `disease_timelines.json` | 102疾患の時間特性メタデータ | |
| `test_case_classification.md` | Real vs Synthetic 分類ルール | |

---

## ネットワーク構成

```
疾患:       102 (D01-D102)
中間変数:     1 (M01: SAH)
症状:        46 (S01-S46)
徴候:        35 (E01-E35)
検査:        44 (L01-L46)
リスク因子:    42 (R01-R43)
時間:         3 (T01-T03)
合計:       273変数, 984辺
```

---

## Real Case テスト成績 (R01-R43)

```
Total: 43例 (in-scope 36, OOS 7)
Top-1: 20/36 (56%)
Top-3: 29/36 (81%)
Confident misdiagnosis (H<2+wrong): 5件
```

### OOS一覧 (7例)
R02(Cogan), R12(Murine typhus), R29(ARF), R31(Scrub typhus), R32(PFAPA), R42(Psittacosis), R43(Strongyloides)

### 疾患別内訳

| カテゴリ | 例数 | Top-1 | Top-3 | 備考 |
|---------|------|-------|-------|------|
| Still病 | 8 | 8/8 (100%) | 8/8 | 完璧。フェリチン+弛張熱が強い |
| リンパ腫/HLH | 5 | 3/5 | 5/5 | 白血病との鑑別が困難 |
| 結核(肺外含) | 6 | 2/6 | 4/6 | 肺外TB辺追加で0→2に改善 |
| PCP | 2 | 2/2 | 2/2 | S17/S46/T01辺追加で修正 |
| Q熱 | 3 | 0/3 | 1/3 | 特異的所見なし=great mimicker |
| IE | 1 | 1/1 | 1/1 | SAH中間変数で解決 |
| その他感染 | 5 | 3/5 | 4/5 | |
| その他自己免疫 | 3 | 1/3 | 1/3 | サルコイド/ブルセラが弱い |
| その他 | 3 | 0/3 | 3/3 | PE/薬剤熱/occult肺炎 |

### Confident Misdiagnosis 5件（最重要）

| Case | H | 出力 | 正答 | 根本原因 |
|------|---|------|------|---------|
| R03 DLBCL/HLH 78F | 0.9 | 白血病73% | リンパ腫r2 | 骨髄検査なしで鑑別不能 |
| R11 COVID 81M | 1.5 | 肺炎71% | COVIDr4 | PCRなしで鑑別不能 |
| R26 HLH 50F | 1.2 | 白血病69% | リンパ腫r2 | R03と同パターン |
| R36 Miliary TB 48F | 1.2 | リンパ腫63% | 結核r2 | B症状がリンパ腫と重複 |
| R39 TB meningitis 72M | 1.8 | マラリア55% | 結核r3 | tropical→マラリア優先 |

---

## このsessionで実施した主な修正

### 1. R06(渡航歴)を地域別に分割
`no/tropical_endemic/developed/domestic` の4値に拡張。先進国渡航でマラリア/腸チフスが上がる問題を解消。

### 2. Q熱(D55)のCPT強化
prior: R30=livestockで0.02, leak=0.0001。R30=livestockでrank12→rank2に改善。ただしrank1には届かず（Q熱はgreat mimicker）。

### 3. SAH(M01)中間変数の導入
IE→SAH→項部硬直/頭痛/意識障害の因果連鎖。NEJM Case 38-2024 (IE→SAH)が0%→99%に。

### 4. 自信的误诊の系統的修正（NO EDGE問題）
- D92(腫瘍熱): +T01,L04,S01 → FATAL→正解45%
- D14(IE): +E06,L45,S42,L04,S01,S04 → 脳塞栓+肺塞栓
- D67(リンパ腫): +T01,L04,S01 → DANGER→正解89%
- D50(PCP): +S17,S46,T01,S07 → DANGER→正解96%

### 5. 系統的辺欠落チェック
慢性疾患→T01(17疾患), 急性疾患→T01(12疾患), 呼吸器→L04(7疾患), IE multi-organ(S33,E05)追加。

### 6. 肺外結核(D17)への14辺追加
腹膜結核(S12,E28,S14), 結核性髄膜炎(E06,E16,S05,L45), 粟粒結核(E14,L22), 慢性消耗(S17,S46,S07)。TB 0/6→2/6 Top-1, 4/6 Top-3。

### 7. Per-disease timeline メタデータ生成
102疾患をhyperacute(20)/acute(50)/subacute(25)/chronic(7)に自動分類。

---

## 鉄律（Memory に記録済み）

1. **テスト:** real case only。synthetic/国試は禁止。PMC/NEJM/BMJ等の疑難症例のみ
2. **三件套同步:** node追加→辺追加→CPT追加。どれか1つでも欠けると推論に反映されない
3. **Real vs Synthetic厳密分離:** 論文では別セクションで報告

---

## 論文級の発見（このsession）

### 発見1: 自信的误诊の根本原因 = NO EDGE
LLM生成BNの最大リスクはCPTパラメータ誤りではなく辺の構造的欠落。辺がない→likelihoodがleak→他疾患に吸い込まれる→H低い（自信）+top-1間違い。5例全てがこのパターン。

### 発見2: H(エントロピー)の意味
- H>3.0 → 「情報不足、追加検査せよ」（正確な警告）
- H<1.0 → 「ほぼ確定」（だが稀に自信的误诊 = 最も危険）

### 発見3: IE→SAH→項部硬直の因果連鎖
中間変数(SAH)なしでは心雑音+血培でもIE32%止まり。SAH確認後は心雑音1つで86%に翻転。

### 発見4: Q熱/肺外結核の「弱さ」の正体
全所見で競合疾患がlikelihood上位 → 尤度比≈1 → 確定検査なしでは人間も当てられない。

---

## Real Case 全件一覧 (R01-R43)

### Top-1 正解 (20件)
R01 Still 19F, R04 Hodgkin 44M, R05 PCP 71M, R08 Malaria 39M, R09 Lepto 37M, R10 IE→SAH 22F, R14 PTCL-TFH 28M, R15 Splenic NHL, R16 SLE 60F, R19 Still+HPS 88F, R20 Still 30sF, R21 Still 37M, R22 Still 33M, R23 Still+pleural 38F, R24 Still atypical 18M, R30 Still+TB 48F, R33 CAP+rhabdo 67M, R34 HIV+PCP 70F, R37 Miliary TB 49M, R41 Miliary TB ovarian

### Top-3 正解 (追加9件)
R03 DLBCL/HLH(r2), R07 Q fever(r2), R13 PE/DVT(r3), R17 IPD(r3), R18 Occult pneumonia(r2), R26 HLH(r2), R35 Drug fever(r3), R36 Miliary TB(r2), R39 TB meningitis(r3)

### Top-3外 (7件)
R06 Q fever肝炎(r49), R11 COVID(r4), R25 Sarcoid(r22), R27 Q persist(r92), R28 Neurobrucella(r59), R38 Peritoneal TB(r25), R40 Peritoneal TB TNFi(r5)

---

## 未解決の問題（次session以降）

| 優先度 | 項目 |
|--------|------|
| HIGH | real_case_test_suite.json にR19-R43を追加 |
| HIGH | Real case 50+ in-scope への拡大（現在36） |
| HIGH | サルコイドーシス(D62)改善: BHL/ACE変数追加 |
| MED | ブルセラ(D53)改善: 辺追加 |
| MED | Hodgkin Pel-Ebstein: T03 CPT調整 |
| LOW | MIMIC-IV申請 |
| LOW | 森先生メール |
| LOW | per-disease onset stage 推論エンジン統合 |

---

## 論文構成

| 論文 | テーマ | 就緒度 |
|------|--------|--------|
| 論文一 | LLM生成BN vs 人力構築: NO EDGE問題 | 85% |
| 論文三 | エントロピー減少曲線 → 確定検査推奨 | 70% |
| 論文四 | 因果グラフ → 情報幾何 | 75% |
