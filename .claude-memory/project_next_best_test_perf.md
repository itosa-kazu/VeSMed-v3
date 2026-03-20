---
name: next_best_test性能问题
description: 推荐检查API(next_best_test)需10-20秒，系统扩大后会更慢，需要优化
type: project
---

`/api/next_best_test` 是系统最大性能瓶颈。

**现状**: ~247未观测变量 × ~4 states × 370疾病 = ~1000+次完整推理，耗时10-20秒。

**已做**: Promise.all()拆开，诊断结果秒出，推荐检查异步加载。

**未来优化方向**:
1. **预筛选** — 只对有辺连接到Top-10疾病的变量算IG，跳过不相关变量
2. **缓存** — 相同evidence的prior只算一次（当前每次inference重算）
3. **C扩展** — 内层循环用Cython/NumPy向量化
4. **并行** — Python multiprocessing分摊hypothesis inference

**Why:** 系统从370疾病扩展到更多时，O(V×S×D×E)复杂度会进一步恶化。
**How to apply:** 作为技术债务跟踪，在系统扩展前需要解决。
