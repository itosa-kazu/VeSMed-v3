---
name: 未实现的好点子（7个）
description: VeSMed待实现功能：timeline/surprise/embedding/中間変数/除外診断/MIMIC/死亡向量
type: project
---

## 1. Per-disease timeline（每个病按自己的时间轴切）
- 虫垂炎=小时级，結核=周级。输入"発病第X天"自动调整各所見出現確率
- onset_day_range数据已在每条辺上，metadata已生成
- temporal penaltyのprototype engine跑过，虫垂炎Day0→Day1和IE Day3→Day21效果漂亮
- **未做：** 正式统合到主引擎，per-disease切分（非uniform 4-stage）

## 2. Surprise Detector（背景意外度検出）
- 系统说"淋巴腫99%"但βDグルカン陽性——对淋巴腫很意外
- 专门检测"如果top-1正确，有没有不该出現的所見"，捕捉自信误诊的安全网
- surprise_v2_blindspot.py 有初步实现
- **未做：** 和主引擎统合，real case验证

## 3. VeSMed v2 嵌入向量系统（Qwen3-Embedding）
- Qwen3-Embedding-8B给386疾患+329検査项做embedding，构建similarity matrix
- 解决"BN只覆盖102疾患，剩余怎么办"
- Binary matrix处理negation blindspot。"Part B: Critical Hit"用max操作做致命疾患排除
- **未做：** 实际训练和测试。是VeSMed从"手工BN"扩展到"386疾患全覆盖"的关键

## 4. 中間変数の系統的導入
- SAH(M01)成功了。同样思路可用于：
  - DIC（多疾患→DIC→出血/血小板低下）
  - ARDS（多疾患→ARDS→低酸素）
  - HLH（多疾患→HLH→汎血球減少+フェリチン爆上げ）
- **已做：** M01(SAH)
- **未做：** DIC, ARDS, HLH等

## 5. 「全検査陰性」を正の証拠として扱う
- 薬剤熱/腫瘍熱は除外診断——全感染症検査陰性才考虑
- 目前BN不区分"没做检查"和"做了但陰性"
- 需要让"血培陰性+ANA陰性+各種培養陰性"成为薬剤熱/腫瘍熱の正の証拠
- **未做：** 实现

## 6. MIMIC-IV / DPC 大規模検証
- MIMIC-IV(MIT ICU数据) + DPC(日本診断群分類) 做几千～几万例验证
- **制约：** MIMIC-IV需CITI训练+PhysioNet申请+DUA签署。DUA禁止发送数据到LLM API，只能本地Python处理。DPC需机构申请

## 7. 「死亡ベクトル」と「治療ベクトル」
- 最早期概念：疾患=推患者向"死亡向量"的力，治療=推离的力
- VeSMed的哲学性framing起点
- **未做：** formalize成数学
