from os import listdir, sys
from os.path import isfile, isdir, join, getsize, getmtime
from typing import Callable
from argparse import ArgumentParser

# TODO: This can be done with arrays for entries1/entries2, thus allowing for
#   more complex comparisons of N arguments. Of course, the logic will become
#   more complex. Additionally, the comparison will take more time, as we would
#   need to compare each entry with each other entry. Which can be tackled by
#   using separate threads for each pair comparison.
#
#   An important note is that the reading of the entire comparison result will
#   be hard for humans.
print("Starting the comparison of two directories")

def compare_files(files: (str, str), criteria: str) -> (bool, str):
    """
    Compares two files by specified criteria. It is assumed that the
    files already match by name
    """

    #Size:
    if ('s' in criteria):
        sizes = (getsize(files[0]), getsize(files[1]))

        if sizes[0] != sizes[1]:
            return (False, "Size")

    if ('m' in criteria):
        modified_times = (getmtime(files[0]), getmtime(files[1]))
        if modified_times[0] != modified_times[1]:
            return (False, "Modified Time")

    return (True, "")

def isolate_by_type(entries: list[str], isolator: Callable[[str], list[str]]):
    isolated_entries = {e for e in entries if isolator(e)}

    return isolated_entries

def compare_directories(dir1: str, dir2: str, criteria: str, show_equals=False) -> (bool, str):
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
        res = compare_files(full_files, criteria)

        if (not res[0]):
            print(f"Files {full_files[0]} and {full_files[1]} differ by {res[1]}")
        else:
            if show_equals:
                print(f"Files {full_files[0]} and {full_files[1]} are equal")

    for distinct_subdir_set in distinct_subdirs:
      if (distinct_subdir_set):
          for dir in distinct_subdir_set:
              print(f"Directory '{join(dir1, dir)}' is only in {dir1}")

    # Compare common directories:
    for dir in common_dirs:
        full_dirs = (join(dir1, dir), join(dir2, dir))
        compare_directories(full_dirs[0], full_dirs[1], criteria, show_equals)

# Check the arguments:

if __name__ == "__main__":

    arg_parser = ArgumentParser(
                        prog='dir-compare',
                        description='Compares two directories in depth by specified file attributes',
                        epilog='')

    arg_parser.add_argument('-s', '--source')
    arg_parser.add_argument('-t', '--target')
    arg_parser.add_argument('-e', '--show_equals', type = str)
    arg_parser.add_argument('-c', '--criteria', help = "Specifies the criteria to check upon: empty - filename only, s: size, m: modified time, can be combined, e.g. sm - both")
    args = arg_parser.parse_args()

    if not isdir(args.source):
        print(f"Error: {args.source} is not a valid directory.")
        exit(1)

    if not isdir(args.target):
        print(f"Error: {args.target} is not a valid directory.")
        exit(1)

    compare_directories(args.source, args.target, args.criteria, args.show_equals.lower() == "true")

