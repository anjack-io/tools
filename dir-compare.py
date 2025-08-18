from os import listdir, sys
from os.path import isfile, isdir, join
from typing import Callable

# TODO: This can be done with arrays for entries1/entries2, thus allowing for
#   more complex comparisons of N arguments. Of course, the logic will become
#   more complex. Additionally, the comparison will take more time, as we would
#   need to compare each entry with each other entry. Which can be tackled by
#   using separate threads for each pair comparison.
#
#   An important note is that the reading of the entire comparison result will
#   be hard for humans.
print("Starting the comparison of two directories")

def isolate_by_type(entries: list[str], isolator: Callable[[str], list[str]]):
    isolated_entries = {e for e in entries if isolator(e)}

    return isolated_entries

def compare_directories(dir1: str, dir2:str):
    """
    Compare two directories and print the differences.
    """

    # Get the list of entries in each dir:
    entries1 = set(listdir(dir1))
    entries2 = set(listdir(dir2))

    # Get files/directories only in each dir:
    files1 = isolate_by_type(entries1, lambda e: isfile(join(dir1, e)))
    files2 = isolate_by_type(entries2, lambda e: isfile(join(dir2, e)))

    subdirs1 = isolate_by_type(entries1, lambda e: isdir(join(dir1, e)))
    subdirs2 = isolate_by_type(entries2, lambda e: isdir(join(dir2, e)))

    # Find common files:
    common_files = files1.intersection(files2)
    # Remove common files from both sets:
    distinct_files1 = files1 - common_files
    distinct_files2 = files2 - common_files

    common_dirs = subdirs1.intersection(subdirs2)
    distinct_subdirs1 = subdirs1 - common_dirs
    distinct_subdirs2 = subdirs2 - common_dirs

    if (distinct_files1):
        for file in distinct_files1:
            print(f"File '{join(dir1, file)}' is only in {dir1}")
    if (distinct_files2):
        for file in distinct_files2:
            print(f"File '{join(dir2, file)}' is only in {dir2}")

    # Compare common files by size:
    for file in common_files:
        fullFile1 = join(dir1, file)
        fullFile2 = join(dir2, file)
        size1 = os.path.getsize(fullFile1)
        size2 = os.path.getsize(fullFile2)

        if size1 != size2:
            print(f"File '{fullFile1}' diffeers in size ({size1}) from '{fullFile2}' ({size2})")

    if (distinct_subdirs1):
        for dir in distinct_subdirs1:
            print(f"Directory '{join(dir1, dir)}' is only in {dir1}")
    if (distinct_subdirs2):
        for dir in distinct_subdirs2:
            print(f"Directory '{join(dir2, dir)}' is only in {dir2}")
    # Compare common directories:
    for dir in common_dirs:
        fullDir1 = join(dir1, dir)
        fullDir2 = join(dir2, dir)
        compare_directories(fullDir1, fullDir2)

# Check the arguments:

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dir-comparey.py <dir1> <dir2>")
        exit(1)

    dir1 = sys.argv[1]
    dir2 = sys.argv[2]

    if not isdir(dir1):
        print(f"Error: {dir1} is not a valid directory.")
        exit(1)

    if not isdir(dir2):
        print(f"Error: {dir2} is not a valid directory.")
        exit(1)

    compare_directories(dir1, dir2)
