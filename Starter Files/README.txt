Group Number: 8
Student IDs:
- Name: Abdullah Al Mahmud Sagor, ID: 22201081


Compilation Commands:
gcc -Wall -Wextra -std=c11 simplefs_builder.c -o simplefs_builder
gcc -Wall -Wextra -std=c11 simplefs_adder.c -o simplefs_adder

Execution Examples:
# Create a new empty image
./simplefs_builder --image disk.img

# Add a file to the image
./simplefs_adder --input disk.img --file test1.txt

# Verify contents
xxd disk.img

Brief Description:
This project implements a simplified file system named SimpleFS using C. 
The implementation consists of two programs:
1. simplefs_builder: Initializes a 256 KiB file-system image containing a superblock, inode bitmap, data bitmap, inode table, and data region. It creates the root directory with '.' and '..' entries.
2. simplefs_adder: Adds a regular file to an existing SimpleFS image. It uses first-fit allocation for both inodes and data blocks. It safely handles errors such as oversized files, missing images, insufficient blocks, and duplicate filenames.

Contributions:
- Abdullah Al Mahmud Sagor: Contributed to implementing the SimpleFS builder and adder functions.
                            Also Contributed to testing, debugging, and file system block allocations.

Known Limitations or Problems:
- No known problems. The implementation follows the specified constraints correctly.
