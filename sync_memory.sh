#!/bin/bash
# Sync Claude Code memory to repo for GitHub backup
# Usage: bash sync_memory.sh

MEMORY_DIR="$HOME/.claude/projects/$(pwd | tr '/' '-' | sed 's/^-//')/memory"
REPO_DIR=".claude-memory"

if [ ! -d "$MEMORY_DIR" ]; then
  echo "Memory directory not found: $MEMORY_DIR"
  echo "Trying Windows path..."
  MEMORY_DIR="$USERPROFILE/.claude/projects/C--Users-wangw-Desktop-VeSMed-v3/memory"
fi

if [ -d "$MEMORY_DIR" ]; then
  mkdir -p "$REPO_DIR"
  cp "$MEMORY_DIR"/*.md "$REPO_DIR/"
  echo "Synced $(ls "$REPO_DIR"/*.md | wc -l) memory files to $REPO_DIR/"
else
  echo "ERROR: Memory directory not found"
fi
