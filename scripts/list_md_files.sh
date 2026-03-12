#!/bin/bash
find . -type f \( -name "*.md" -o -name "*.mdx" \) \
    ! -path "*/node_modules/*" \
    ! -path "*/.*/*" \
    ! -name "PROGRESS.md" \
    ! -name "*_zh_TW.md" \
    ! -name "*_zh_TW.mdx" \
    ! -path "./dist/*" \
    ! -path "./build/*" | sed 's|^\./||' | sort
