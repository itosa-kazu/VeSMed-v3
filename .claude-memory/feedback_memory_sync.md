---
name: Memory同步到GitHub的流程
description: push前にbash sync_memory.shでmemoryをrepoにコピーし、新PCではCLAUDE.mdの手順で復元
type: feedback
---

Memoryファイルは2箇所に存在する：
- **作業用(本体):** `~/.claude/projects/.../memory/` ← 普段はここに自動保存
- **GitHub用(バックアップ):** プロジェクト内 `.claude-memory/` ← push前に同期

**同期手順:**
1. 普段の作業: memory は Claude Code デフォルトパスに自動保存（何もしなくてOK）
2. GitHub push前: `bash sync_memory.sh` で最新memoryを `.claude-memory/` にコピー
3. `git add .claude-memory/ && git commit`
4. 新PCでclone後: `CLAUDE.md` に記載の復元コマンドを実行

**Why:** memoryはマシン固有パスに保存されるため、別PCでは自動的に引き継がれない。GitHub経由でバックアップ・復元する仕組みが必要。
**How to apply:** commitやpush作業時に `sync_memory.sh` の実行をユーザーに提案する。
