---
name: 新疾患追加前に重複チェック必須
description: 新疾患追加時に既存疾患と名前が重複していないか必ず確認。5組重複で性能低下した教訓。
type: feedback
---

**新疾患追加前に既存疾患との重複チェック必須。**

**Why:** 2026-03-16にD252-D350を一括追加した際、既存疾患と同名の疾患を5組重複追加してしまった（収縮性心膜炎/たこつぼ/IgG4/横紋筋融解/HCM）。同一疾患が2つのIDで存在すると互いに確率を奪い合い、両方のrankが悪化する。統合後Top-3が+3-6改善した。

**How to apply:**
```python
# 追加前に必ず実行
existing_names = {v['name_ja'] for v in s1['variables'] if v['category']=='disease'}
if new_name_ja in existing_names:
    print(f'DUPLICATE: {new_name_ja} already exists!')
```
add-diseases skillにもこのチェックを組み込むべき。
