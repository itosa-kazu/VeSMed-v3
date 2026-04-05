---
name: δMed部署パイプライン
description: VeSMed CPT変更後のδMed更新手順。export→Supabase→build→deploy の4ステップ固定フロー
type: feedback
---

VeSMedのstep1/step2/step3を変更した後、δMedにも反映する固定フロー:

```
1. PYTHONIOENCODING=utf-8 python3 vesmed_export.py --output deltamed_export --with-confusion
2. python3 upload_to_supabase.py  (deltamed_export/ → Supabase)
3. cd deltamed && npm run build && cp dist/index.html dist/404.html
4. npx gh-pages -d dist
```

**Why:** VeSMedとδMedは別リポだがデータは連動。CPT修正・辺追加・疾患追加の後にδMedを更新しないと古いデータで学習してしまう。

**How to apply:** step1/step2/step3に変更を加えた後、回帰テスト通過を確認してからこのパイプラインを実行する。特にCPT state名の修正はδMedの表示に直結するので必ず実行。

**デプロイ先:**
- GitHub Pages: https://itosa-kazu.github.io/deltamed/
- Supabase: liiiaegezuyejfifdhad.supabase.co (anon key はコード内にfallback)
- deltamed repo: https://github.com/itosa-kazu/deltamed (public)
