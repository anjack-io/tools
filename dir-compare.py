import os
print("Hey, starting the comparison of two directories")

def compare_directories(dir1, dir2):
    """
    Compare two directories and print the differences.
    """

    # Get the list of files in directory 1
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))

    # Filter only files from the lists:
    files_only1 = {f for f in files1 if os.path.isfile(os.path.join(dir1, f))}
    files_only2 = {f for f in files2 if os.path.isfile(os.path.join(dir2, f))}

    # Find common files:
    common_files = files_only1.intersection(files_only2)
    # Remove common files from both sets:
    distinct_files_only1 = files_only1 - common_files
    distinct_files_only2 = files_only2 - common_files

    if (distinct_files_only1):
        for file in distinct_files_only1:
            print(f"File '{os.path.join(dir1, file)}' is only in {dir1}")
    if (distinct_files_only2):
        for file in distinct_files_only2:
            print(f"File '{os.path.join(dir2, file)}' is only in {dir2}")

    # Compare common files by size:
    for file in common_files:
        fullFile1 = os.path.join(dir1, file)
        fullFile2 = os.path.join(dir2, file)
        size1 = os.path.getsize(fullFile1)
        size2 = os.path.getsize(fullFile2)

        if size1 != size2:
            print(f"File '{fullFile1}' diffeers in size ({size1}) from '{fullFile2}' ({size2})")

    dirs_only1 = {d for d in files1 if os.path.isdir(os.path.join(dir1, d))}
    dirs_only2 = {d for d in files2 if os.path.isdir(os.path.join(dir2, d))}
    common_dirs = dirs_only1.intersection(dirs_only2)
    distinct_dirs_only1 = dirs_only1 - common_dirs
    distinct_dirs_only2 = dirs_only2 - common_dirs
    if (distinct_dirs_only1):
        for dir in distinct_dirs_only1:
            print(f"Directory '{os.path.join(dir1, dir)}' is only in {dir1}")
    if (distinct_dirs_only2):
        for dir in distinct_dirs_only2:
            print(f"Directory '{os.path.join(dir2, dir)}' is only in {dir2}")
    # Compare common directories:
    for dir in common_dirs:
        fullDir1 = os.path.join(dir1, dir)
        fullDir2 = os.path.join(dir2, dir)
        compare_directories(fullDir1, fullDir2)


# Check the arguments:

if __name__ == "__main__":
    if len(os.sys.argv) != 3:
        print("Usage: python dir-comparey.py <dir1> <dir2>")
        exit(1)

    dir1 = os.sys.argv[1]
    dir2 = os.sys.argv[2]

    if not os.path.isdir(dir1):
        print(f"Error: {dir1} is not a valid directory.")
        exit(1)

    if not os.path.isdir(dir2):
        print(f"Error: {dir2} is not a valid directory.")
        exit(1)

    compare_directories(dir1, dir2)
