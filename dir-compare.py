from os import listdir, sys
from os.path import isfile, isdir, join, getsize
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
    entries = ((dir1, set(listdir(dir1))), (dir2, set(listdir(dir2))))

    # Get files/directories only in each dir:
    files = ()
    for entry in entries:
        files += (isolate_by_type(entry[1], lambda e: isfile(join(entry[0], e))), )

    subdirs = ()
    for entry in entries:
        subdirs += (isolate_by_type(entry[1], lambda e: isdir(join(entry[0], e))), )

    # Find common files:
    common_files = files[0].intersection(files[1])
    # Remove common files from both sets:
    distinct_files = ()
    for file_set in files:
        distinct_files += (file_set - common_files, )

    common_dirs = subdirs[0].intersection(subdirs[1])
    distinct_subdirs = ()
    for sub_dir_set in subdirs:
        distinct_subdirs += (sub_dir_set - common_dirs, )

    for distinct_file_set in distinct_files:
      if (distinct_file_set):
          for file in distinct_file_set:
              print(f"File '{join(dir1, file)}' is only in {dir1}")

    # Compare common files by size:
    for file in common_files:
        full_files = (join(dir1, file), join(dir2, file))
        size = (getsize(fullFile1), getsize(fullFile2))

        if size[0] != size[1]:
            print(f"File '{fullFile1}' diffeers in size ({size1}) from '{fullFile2}' ({size2})")

    for distinct_subdir_set in distinct_subdirs:
      if (distinct_subdir_set):
          for dir in distinct_subdir_set:
              print(f"Directory '{join(dir1, dir)}' is only in {dir1}")

    # Compare common directories:
    for dir in common_dirs:
        full_dirs = (join(dir1, dir), join(dir2, dir))
        compare_directories(full_dirs[0], full_dirs[1])

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
