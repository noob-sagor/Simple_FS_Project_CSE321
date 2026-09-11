#!/bin/bash
echo "Compiling..."
gcc -Wall -Wextra -std=c11 simplefs_builder.c -o simplefs_builder
gcc -Wall -Wextra -std=c11 simplefs_adder.c -o simplefs_adder

if [ $? -ne 0 ]; then
  echo "Compilation failed!"
  exit 1
fi

echo "Compilation successful."
echo "----------------------------------------"

echo "Test Case 1 - Empty File System"
rm -f disk.img
./simplefs_builder --image disk.img
ls -l disk.img | awk '{print "Size: " $5}'

echo "Test Case 2 - Superblock"
xxd -l 128 disk.img | head -n 4

echo "Test Case 3 - Initial Inode Bitmap"
xxd -s 4096 -l 16 disk.img

echo "Test Case 4 - Initial Data Bitmap"
xxd -s 8192 -l 16 disk.img

echo "Test Case 5 - Root Directory"
xxd -s 16384 -l 128 disk.img

echo "Test Case 6 - Add a Small File"
echo "Operating Systems Lab" > test1.txt
rm -f disk.img
./simplefs_builder --image disk.img
./simplefs_adder --input disk.img --file test1.txt

echo "Test Case 7 - Inode Allocation After One File"
xxd -s 4096 -l 8 disk.img

echo "Test Case 8 - Data Allocation After One Small File"
xxd -s 8192 -l 8 disk.img

echo "Test Case 9 - Verify File Contents"
xxd -s 20480 -l 100 disk.img

echo "Test Case 10 - Two-Block File"
dd if=/dev/zero of=test2.txt bs=1 count=5000 2>/dev/null
rm -f disk.img
./simplefs_builder --image disk.img
./simplefs_adder --input disk.img --file test2.txt
xxd -s 8192 -l 8 disk.img

echo "Test Case 11 - Maximum File Size"
dd if=/dev/zero of=maxfile.dat bs=1 count=12288 2>/dev/null
dd if=/dev/zero of=too_big.dat bs=1 count=12289 2>/dev/null
./simplefs_adder --input disk.img --file maxfile.dat
./simplefs_adder --input disk.img --file too_big.dat

echo "Test Case 12 - Multiple Files"
rm -f disk.img
./simplefs_builder --image disk.img
./simplefs_adder --input disk.img --file test1.txt
./simplefs_adder --input disk.img --file test2.txt
echo "test3" > test3.txt
./simplefs_adder --input disk.img --file test3.txt
xxd -s 4096 -l 8 disk.img

echo "Test Case 13 - Duplicate File"
./simplefs_adder --input disk.img --file test1.txt

echo "Test Case 14 - Missing Source File"
./simplefs_adder --input disk.img --file abc123.txt

echo "Test Case 15 - Missing Image"
./simplefs_adder --input nothing.img --file test1.txt

echo "----------------------------------------"
echo "Done."
