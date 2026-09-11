# CSE321 Final Project - SimpleFS

This project implements a simplified file system named **SimpleFS** using C. The implementation consists of two primary programs:

1. **`simplefs_builder`**: Initializes a 256 KiB file-system image containing a superblock, inode bitmap, data bitmap, inode table, and data region. It creates the root directory with `.` and `..` entries.
2. **`simplefs_adder`**: Adds a regular file to an existing SimpleFS image. It uses first-fit allocation for both inodes and data blocks. It safely handles errors such as oversized files, missing images, insufficient blocks, and duplicate filenames.

## Project Details
- **Group Number:** 8
- **Contributor:** Abdullah Al Mahmud Sagor (ID: 22201081)
- **Contributions:** Contributed to implementing the SimpleFS builder and adder functions. Also contributed to testing, debugging, and file system block allocations.
- **Known Limitations or Problems:** No known problems. The implementation follows the specified constraints correctly.

## Compilation Commands

To compile the C source files into executable binaries, run the following commands:

```bash
gcc -Wall -Wextra -std=c11 simplefs_builder.c -o simplefs_builder
gcc -Wall -Wextra -std=c11 simplefs_adder.c -o simplefs_adder
```

## Execution Examples

### 1. Create a new empty image
```bash
./simplefs_builder --image disk.img
```

### 2. Add a file to the image
```bash
./simplefs_adder --input disk.img --file test1.txt
```

### 3. Verify contents
```bash
xxd disk.img
```
