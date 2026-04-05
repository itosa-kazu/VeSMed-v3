---
name: 変量State設計鉄律 — 一変量=一臨床問題（対抗検証済み）
description: 変量state設計の根本原則。三層構造(Finding/Measurement/Satellite)。absent+severity混合禁止。5つの攻撃に耐えた確定版。
type: feedback
---

## 根本原則: 一変量 = 一臨床問題、States = その問題の全回答

変量のstateが「同じ問題の異なる回答」になっていなければ設計が間違っている。
stateに**層級関係**(absent→present→mild→severe)があったら2つの問題が混在している証拠。

**Why:** 大清洗Phase 0で確立。旧設計で absent/mild/severe を1変量に混在→absentは「有無」の問題、mild/severeは「程度」の問題。異なる臨床問題を1変量に押し込むとCPT設計が不自然になり、将来の構造変更を誘発する。

**How to apply:** 新変量設計時に必ず以下の三層構造と判定規則を適用。

---

## 変量三層構造（確定版）

| 層 | 臨床問題 | States規則 | 例 |
|----|---------|-----------|-----|
| **Finding** | 有没有？ | absent / present のみ | 皮疹、肝腫大、心雑音 |
| **Measurement** | 数値/等級は？ | 標準cutoff区間（absentなし） | 体温、WBC、GCS、血圧 |
| **Satellite** | 何型？何程度？ | 分類 or 分級（absentなし） | 皮疹形態、水腫分級、雑音時相 |

### Finding（発見）
- 定義: 臨床所見を探して、あったかなかったか
- States: **absent / present のみ。永遠にこの2つだけ**
- 例: Koplik斑, Janeway lesion, 腹膜刺激徴, 皮疹, リンパ節腫大

### Measurement（測定）
- 定義: 検査/測定を行い、数値または分級を得る
- States: 連続値の離散化区間 or 公認分級の各等級
- **absentなし** — 測定すれば必ず値がある。未測定=evidenceを設定しない
- 区間境界 = 医学標準cutoff（教科書/ガイドライン）= Domain Invariant
- 例: 体温(<35/35-37.4/37.5-38/38-39/39-40/>40), WBC(<4k/4-10k/10-20k/>20k), GCS(15/13-14/9-12/3-8)

### Satellite（衛星）
- 定義: 親Findingが present の時にのみ意味を持つ追加観察
- States: 分類（形態/類型）or 分級（程度/等級）。**absentなし**
- 本質: absentのないMeasurement（測定対象が「所見の特徴」）
- Noisy-ORでは親変量と完全独立に計算（変量間依存なし）
- 例: 皮疹形態(maculopapular/vesicular/petechial), 水腫分級(1+/2+/3+/4+), 心雑音時相(systolic/diastolic)

### 衛星変量のevidence設定規則
- 皮疹なし → rash=absent, rash_morphologyは**未設定**（evidenceを入れない）
- 水疱疹あり → rash=present, rash_morphology=vesicular
- 皮疹あり、型不明 → rash=present, rash_morphologyは**未設定**

### 衛星変量の方向性: **陽性分岐のみ**
- 衛星は Finding=present の場合のみ展開
- Finding=absent のとき追加記述は不要 — **absent就是absent、没有细节可追问**
- 理由: 情報は陽性所見からのみ流出する。陰性は「探して見つからなかった」で終了

### N層嵌套: 框架は任意深度を支持

観察の階層は2層に限らない。GCSの例:

```
Layer 1 (Finding):         consciousness_impairment: absent / present
Layer 2 (Satellite):       gcs_score: 13-14 / 9-12 / 3-8  (GCS=15 = parent absent)
Layer 3 (Sub-measurement): gcs_eye: 1/2/3/4
                           gcs_verbal: 1/2/3/4/5
                           gcs_motor: 1/2/3/4/5/6
```

皮疹の例:
```
Layer 1 (Finding):         rash: absent / present
Layer 2 (Satellite):       rash_morphology: macular / vesicular / petechial / ...
Layer 3 (Sub-satellite):   vesicle_pattern: dermatomal / diffuse / ...（鑑別に必要な場合のみ）
```

**規則は2条のみ、全層に再帰適用:**
1. **parent=absent → 全子孫禁用**（Finding→Satellite規則の再帰版）
2. **同層の粗細は互斥**（粗観察 OR 細観察、両方設定は二重計上）

| 文献報告 | Layer 1 | Layer 2 | Layer 3 |
|---------|---------|---------|---------|
| "意識清楚" | absent | 禁用 | 禁用 |
| "意識障害あり" | present | 未設定 | 未設定 |
| "GCS 8" | present(自動) | 3-8 | 未設定 |
| "E2V2M4" | present(自動) | **未設定** | eye=2,verbal=2,motor=4 |

実践上ほぼ3層を超えない。Layer 3は**組分に独立鑑別意義がある場合のみ**追加（GCS motorが特に低い→脳幹病変等）。

---

## 合併 vs 分離の判定基準

### 合併可（1変量にしてよい）
states間に**層級関係がなく、同じ問題の異なる回答**である場合:
- 数値区間: WBC <4k/4-10k/10-20k/>20k ✓
- 分類型: 旅行先 tropical/developed/domestic ✓

### 分離必須（別変量にすべき）
states間に**層級関係**がある、または**異なる臨床問題が混在**する場合:
- absent+severity: absent/mild/severe ✗ →「有無」+「程度」が混在
- absent+type: absent/dry/productive ✗ →「有無」+「何型」が混在

### 灰色地帯の解決法（肝腫大の例）
「肝腫大」は Finding にも Measurement にも見える。解決: **2変量に分離**
```
hepatomegaly:        absent / present          ← Finding（大きいか否か？）
hepatomegaly_degree: mild / moderate / marked   ← Satellite（どれくらい？）
```
normal/mild/severe を1変量にすると absent+severity 混合。分離すれば各変量が清潔。

---

## なぜ構造変更が永久不要か

- Finding = absent/present → **100年不変**
- Measurement cutoff = 医学標準 → **10年不変**
- Satellite = 所見の特徴記述 → 新カテゴリは**state追加（加法的）**
- 新しい検査 → 新変量追加（加法的）
- 変量数が臨床現実より多くなることはあり得ない（現実の観察数=正しい変量数）
- いかなる演変も既存変量のstate構造に影響しない

---

## 対抗検証の記録（2026-04-05）

5つの攻撃をかけて検証した結果:

| 攻撃 | 内容 | 判定 | 理由 |
|------|------|------|------|
| Categoricalは第3類型 | rash_morphologyはMでもFでもない | **却下** | Satelliteとして処理。本質はabsentなしのMeasurement |
| 子変量爆炸 | 1変量→4変量で総数が3-5倍 | **却下** | 臨床現実に観察が存在する以上、変量数は現実に合わせるべき。人為圧縮=Domain Invariant違反 |
| F vs Mの灰色地帯 | hepatomegalyはFかMか | **却下** | Finding+Satellite分離で灰色地帯消滅 |
| Step3の鶏卵問題 | 子分類の鑑別意義はPhase1データが必要 | **却下** | 教科書の臨床知識で判断可能。CPTデータ不要 |
| 穷挙不可能 | Phase0で全変量は列挙しきれない | **却下** | 加法的演進で対処。後から追加しても既存構造に影響なし |

**結論: フレームワーク成立。修正不要、Satellite層の明示追加のみ。**

---

## 衛星変量のUI/実装規則

### Evidence設定の連動ロジック（v3.1実装必須）

```
1. parent Finding = absent  → 全satellite禁用+クリア
2. parent Finding = present → satellite選択可能に
3. parent Finding = 未設定 + satellite設定 → parentを自動的にpresentに設定
```

規則3の理由: 案例報告に"vesicular lesions on trunk"とあれば、rash_morphology=vesicularを直接入力。
rash=presentは自明なので自動反推する。

### 「阴性の卫星」は不要（暗物質テスト済み 2026-04-05）

「absent」の更なる詳細化が必要な場面は一見存在するが、全て別の機制で捕獲済み:
- 治療による陰性化（退熱薬で解熱）→ **独立変量**（antipyretic_use等）
- 文脈依存的陰性（重度肝障害なのに黄疸なし）→ **Noisy-ORが自動処理**（CPTでP(jaundice|cirrhosis)高→absent observation→大幅降権）
- 時間的陰性（以前あったが消えた）→ **時間変量**（duration, onset）
- 検査限界による陰性（肥満で触診困難）→ **evidence未設定**（信頼できない観察はそもそも入力しない）

結論: absent = 観察連鎖の終端。これは「暗物質」ではなく、情報が既に別経路で流れている。

---

## 圧力テスト記録（8臨床案例 2026-04-05）

8つの刁鑽な臨床所見でフレームワークを検証:

| # | 所見 | 難点 | 処理方式 | 判定 |
|---|------|------|---------|------|
| 1 | 相対徐脈（発熱+正常HR） | 2変量の関係 | 各自独立Measurement、後験で組合涌現 | ✓ |
| 2 | 奇脈（吸気SBP>10mmHg低下） | 条件付き測定 | Finding(absent/present) or Measurement(cutoff区間) | ✓ |
| 3 | 遊走性環状紅斑 | 形態+動態+大きさ | rash=present + rash_morphology=erythema_migrans (Satellite) | ✓ |
| 4 | 非退色性点状出血 | 条件付き修飾 | rash_morphology=petechial + rash_blanching=non_blanching (2 Satellite) | ✓ |
| 5 | Kussmaul徴候 | 反常的生理 | kussmaul_sign: absent/present (Finding) | ✓ |
| 6 | 鉄錆色痰 | 多層修飾 | cough=present + sputum_appearance=rusty (Satellite) | ✓ |
| 7 | 移動性濁音 | 動態パターン | shifting_dullness: absent/present (Finding) | ✓ |
| 8 | 重度肝障害+黄疸欠如 | 文脈依存的陰性 | 各stigma=absent → Noisy-ORがCPT差で自動区分 | ✓ |

**8/8全通過。フレームワークの限界に達する案例は発見されなかった。**

---

## 落地Pipeline（Phase 0）

```
Step 1: 穷挙臨床観察
  来源: Harrison's ROS + 標準体検 + 常規検査 + 画像 + 危険因子
  各観察を標註: Measurement / Finding？

Step 2: States設定
  Measurement → 標準cutoff查詢（教科書/ガイドライン）
  Finding → absent / present（以上）

Step 3: Satellite識別
  判定: その発見の形態/類型/程度が鑑別に異なる意義を持つか？
  Yes → 独立のSatellite変量を作成（分類 or 分級、absentなし）
  No → Findingのままbinaryで十分

Step 4: 互斥完備性検証
  各変量のstates: 互斥か？完備か？層級混合なしか？
```
