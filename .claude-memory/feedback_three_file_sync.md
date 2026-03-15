---
name: 三件套同步规则
description: step1(节点)、step2(边)、step3(CPT)必须作为一体同步修改，改边时必须同时检查节点和CPT
type: feedback
---

修改网络时，step1(节点) / step2(边) / step3(CPT) 是完全一体的三件套，必须同步更新：

- 加边 → 必须同时加CPT（parent_effects），并检查step1中节点的states是否需要调整
- 改节点states → 必须同步更新step2的边和step3的CPT/leak
- 改CPT → 检查是否需要新增/修改边

绝对不能只改其中一个文件。用户明确强调过这一点。
