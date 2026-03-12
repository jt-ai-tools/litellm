#!/bin/bash
# 檢查是否所有 .md 和 .mdx 檔案都有對應的 _zh_TW 版本
# 排除 PROGRESS.md 和已翻譯檔案

MISSING_COUNT=0
./scripts/list_md_files.sh > .all_files

while read -r file; do
    ext="${file##*.}"
    base="${file%.*}"
    zh_file="${base}_zh_TW.${ext}"
    if [ ! -f "$zh_file" ]; then
        echo "缺失翻譯: $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done < .all_files

rm .all_files

if [ $MISSING_COUNT -eq 0 ]; then
    echo "所有檔案皆已完成翻譯！"
    exit 0
else
    echo "共有 $MISSING_COUNT 個檔案尚未翻譯。"
    exit 1
fi
