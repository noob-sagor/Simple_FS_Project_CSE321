import re

def patch_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    
    pattern = r"/\* TODO: STUDENT CODE START \*/.*?/\* TODO: STUDENT CODE END \*/"
    
    def repl_func(match):
        if not patch_file.replacements:
            return match.group(0)
        replacement = patch_file.replacements.pop(0)
        return "/* TODO: STUDENT CODE START */\n" + replacement + "\n    /* TODO: STUDENT CODE END */"

    patch_file.replacements = replacements.copy()
    content = re.sub(pattern, repl_func, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)

