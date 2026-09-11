import re

def patch_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We find all blocks of /* TODO: STUDENT CODE START */ ... /* TODO: STUDENT CODE END */
    # and replace them one by one.
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

builder_replacements = [
"""    sb.magic = MAGIC_NUMBER;
    sb.block_size = BLOCK_SIZE;
    sb.total_blocks = TOTAL_BLOCKS;
    sb.inode_count = TOTAL_INODES;
    sb.inode_bitmap_block = INODE_BITMAP_BLOCK;
    sb.data_bitmap_block = DATA_BITMAP_BLOCK;
    sb.inode_table_block = INODE_TABLE_BLOCK;
    sb.data_region_block = DATA_REGION_BLOCK;
    sb.root_inode = ROOT_INODE;""",

"""    set_bit(inode_bitmap, 0);""",

"""    set_bit(data_bitmap, 0);""",

"""    root_inode.type = TYPE_DIRECTORY;
    root_inode.links = 2;
    root_inode.size = 128;
    root_inode.direct[0] = ROOT_DATA_BLOCK;
    root_inode.direct[1] = 0;
    root_inode.direct[2] = 0;""",

"""    dot.inode_no = ROOT_INODE;
    dot.type = TYPE_DIRECTORY;
    strcpy(dot.name, ".");""",

"""    dotdot.inode_no = ROOT_INODE;
    dotdot.type = TYPE_DIRECTORY;
    strcpy(dotdot.name, "..");"""
]

patch_file("simplefs_builder.c", builder_replacements)

adder_replacements = [
"""    for (int i = 1; i < TOTAL_INODES; i++) {
        if (!is_bit_set(bitmap, i)) {
            return i + 1;
        }
    }""",

"""    for (int i = 0; i < DATA_BLOCKS; i++) {
        if (!is_bit_set(bitmap, i)) {
            return DATA_REGION_BLOCK + i;
        }
    }""",

"""    dirent_t entry;
    fseek(image, ROOT_DATA_BLOCK * BLOCK_SIZE, SEEK_SET);
    for (int i = 0; i < BLOCK_SIZE / sizeof(dirent_t); i++) {
        if (fread(&entry, sizeof(entry), 1, image) != 1) break;
        if (entry.inode_no != 0 && strcmp(entry.name, filename) == 0) {
            return 1;
        }
    }""",

"""    fseek(image, ROOT_DATA_BLOCK * BLOCK_SIZE, SEEK_SET);
    for (int i = 0; i < BLOCK_SIZE / sizeof(dirent_t); i++) {
        if (fread(&entry, sizeof(entry), 1, image) != 1) break;
        if (i >= 2 && entry.inode_no == 0) {
            return i;
        }
    }""",

"""    if (file_size == 0) {
        required_blocks = 0;
    } else {
        required_blocks = (file_size + BLOCK_SIZE - 1) / BLOCK_SIZE;
    }""",

"""    int found_blocks = 0;
    for (int i = 0; i < DATA_BLOCKS && found_blocks < required_blocks; i++) {
        if (!is_bit_set(data_bitmap, i)) {
            allocated_blocks[found_blocks++] = DATA_REGION_BLOCK + i;
        }
    }
    if (found_blocks < required_blocks) {
        printf("Error: insufficient free data blocks.\\n");
        fclose(source); fclose(image); exit(1);
    }
    for (int i = 0; i < required_blocks; i++) {
        set_bit(data_bitmap, data_bitmap_index(allocated_blocks[i]));
    }""",

"""    long remaining = file_size;
    for (int i = 0; i < required_blocks; i++) {
        unsigned char buffer[BLOCK_SIZE] = {0};
        long to_read = remaining < BLOCK_SIZE ? remaining : BLOCK_SIZE;
        fread(buffer, 1, to_read, source);
        fseek(image, allocated_blocks[i] * BLOCK_SIZE, SEEK_SET);
        fwrite(buffer, 1, BLOCK_SIZE, image);
        remaining -= to_read;
    }""",

"""    new_inode.type = TYPE_FILE;
    new_inode.links = 1;
    new_inode.size = file_size;
    for (int i = 0; i < MAX_DIRECT_BLOCKS; i++) {
        if (i < required_blocks) {
            new_inode.direct[i] = allocated_blocks[i];
        } else {
            new_inode.direct[i] = 0;
        }
    }""",

"""    set_bit(inode_bitmap, free_inode - 1);""",

"""    new_entry.inode_no = free_inode;
    new_entry.type = TYPE_FILE;
    strncpy(new_entry.name, source_name, sizeof(new_entry.name) - 1);
    new_entry.name[sizeof(new_entry.name) - 1] = '\\0';""",

"""    root_inode.size += sizeof(dirent_t);"""
]

patch_file("simplefs_adder.c", adder_replacements)

