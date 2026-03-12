import sys
import os

def mark_done(file_path):
    progress_file = 'PROGRESS.md'
    if not os.path.exists(progress_file):
        return
    
    with open(progress_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    ext = file_path.split('.')[-1]
    base = file_path[:-(len(ext)+1)]
    zh_file = f"{base}_zh_TW.{ext}"
    
    new_lines = []
    for line in lines:
        if f"- [ ] {file_path}" in line:
            new_lines.append(f"- [x] {file_path} (已翻譯成 {zh_file})\n")
        else:
            new_lines.append(line)
            
    with open(progress_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mark_done(sys.argv[1])
