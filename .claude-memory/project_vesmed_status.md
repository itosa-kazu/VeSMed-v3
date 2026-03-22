---
name: VeSMed V3.1 項目状態
description: 414疾患、7949辺、1101案例、Top-1 78%、Top-3 93%、FATAL 0
type: project
---

- 414疾患(D01~D419)、794+変量、7949条因果边
- 推理引擎: bn_inference.py V3.1 (Noisy-OR log-LR + IDF dp=0.3 + CF ca=2.0 + PP=0.5)
- 测试: 1101案例 (1095 in-scope, 6 OOS)
- 当前成绩: Top-1 853/1095(78%), Top-3 1021/1095(93%), FATAL 0
- R→D Prior: 全414疾患に年齢/性別prior設定済み
- 国試Priority A+B+C: 全完了(高K/低Kは疾患でなくL108で対応済み)
- 今回追加: D416大腿骨頸部骨折/D417結核性腹膜炎/D418線維筋痛症/D419コクシジオイデス症
- 新変量: E94(圧痛点)のNOP新規作成
- GitHub: https://github.com/itosa-kazu/VeSMed-v3.git
