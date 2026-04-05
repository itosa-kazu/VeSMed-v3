---
name: δMed IndexedDB缓存问题
description: δMed更新Supabase后手機端不会自动刷新，需手动清除IndexedDB或加版本检查
type: feedback
---

Supabase数据更新后，手機浏览器上的δMed不会自动重新加载——isContentLoaded()检测到旧数据有dist_a字段就跳过DataLoader。

**临时解决:** 用户手动清除浏览器site data
**根本解决(TODO):** 加version stamp或content hash检查，Supabase变更后自动触发re-import

**Why:** IndexedDB是离线优先设计，一旦有数据就不再拉Supabase。但CPT修正后需要强制刷新。
**How to apply:** δMed更新パイプライン执行后，提醒用户清除浏览器缓存，或实装自动版本检查。
