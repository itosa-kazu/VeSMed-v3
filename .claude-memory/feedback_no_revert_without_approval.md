# No Revert Without User Approval

- Even if regression test results get WORSE after a change, DO NOT revert without explicit user approval
- Always show the user the before/after comparison and let THEM decide whether to revert
- This applies to all architectural changes, CPT changes, inference algorithm changes, etc.
