with open('simplefs_adder.c', 'r') as f:
    content = f.read()

content = content.replace('    dirent_t entry;\n    fseek(image, ROOT_DATA_BLOCK * BLOCK_SIZE, SEEK_SET);', '    fseek(image, ROOT_DATA_BLOCK * BLOCK_SIZE, SEEK_SET);')
content = content.replace('int i = 0; i < BLOCK_SIZE / sizeof(dirent_t); i++', 'unsigned int i = 0; i < BLOCK_SIZE / sizeof(dirent_t); i++')

with open('simplefs_adder.c', 'w') as f:
    f.write(content)
