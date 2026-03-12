import os
import re

def fix_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find markdown links [text](path.md) or [text](path.mdx)
    # Excluding external URLs
    pattern = r'\[([^\]]+)\]\(([^)]+\.mdx?)\)'
    
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)
        
        # Handle relative paths and anchors
        parts = path.split('#')
        base_path = parts[0]
        anchor = '#' + parts[1] if len(parts) > 1 else ''
        
        if base_path.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return match.group(0)
            
        ext_index = base_path.rfind('.md')
        if ext_index != -1:
            zh_path = base_path[:ext_index] + '_zh_TW' + base_path[ext_index:]
            
            # Check if the zh_TW file exists relative to the current file
            dir_path = os.path.dirname(file_path)
            full_zh_path = os.path.join(dir_path, zh_path)
            
            if os.path.exists(full_zh_path):
                return f'[{text}]({zh_path}{anchor})'
        
        return match.group(0)

    new_content = re.sub(pattern, replace_link, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('_zh_TW.md') or file.endswith('_zh_TW.mdx'):
                file_path = os.path.join(root, file)
                if fix_links_in_file(file_path):
                    print(f"Fixed links in: {file_path}")

if __name__ == "__main__":
    main()
