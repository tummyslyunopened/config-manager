import csv
import os
import shutil
from typing import NoReturn, List, Callable
import difflib
import filecmp

def diff(file_list: List[str]) -> None:
    local_path = os.path.join(os.getcwd(), file_list[0].strip())
    dest_path = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    
    try:
        if os.path.isdir(local_path) and os.path.isdir(dest_path):
            diff_directories(local_path, dest_path)
        elif os.path.isfile(local_path) and os.path.isfile(dest_path):
            diff_files(local_path, dest_path)
        else:
            print(f"Error: Both paths must be either files or directories.")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error comparing paths: {str(e)}")

def diff_files(file1: str, file2: str) -> None:
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        diff = difflib.unified_diff(
            f1.readlines(),
            f2.readlines(),
            fromfile=file1,
            tofile=file2,
        )
        
        diff_output = ''.join(diff)
        if diff_output:
            print(f"Differences between '{file1}' and '{file2}':")
            print(diff_output)
        else:
            print(f"No differences found between '{file1}' and '{file2}'")

def diff_directories(dir1: str, dir2: str) -> None:
    dcmp = filecmp.dircmp(dir1, dir2)
    print_diff_results(dcmp)

def print_diff_results(dcmp: filecmp.dircmp) -> None:
    print(f"Comparing '{dcmp.left}' and '{dcmp.right}':")
    if dcmp.left_only:
        print(f"Files only in '{dcmp.left}': {dcmp.left_only}")
    if dcmp.right_only:
        print(f"Files only in '{dcmp.right}': {dcmp.right_only}")
    if dcmp.diff_files:
        print(f"Differing files: {dcmp.diff_files}")
        for file in dcmp.diff_files:
            file1 = os.path.join(dcmp.left, file)
            file2 = os.path.join(dcmp.right, file)
            diff_files(file1, file2)
    if dcmp.common_dirs:
        for common_dir in dcmp.common_dirs:
            print(f"\nSubdirectory '{common_dir}':")
            subdir1 = os.path.join(dcmp.left, common_dir)
            subdir2 = os.path.join(dcmp.right, common_dir)
            sub_dcmp = filecmp.dircmp(subdir1, subdir2)
            print_diff_results(sub_dcmp)

def adopt(file_list: List[str]) -> None:
    local_file = os.path.join(os.getcwd(), file_list[0].strip())
    dest_file = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    try:
        forcecopy(dest_file, local_file)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error copying file: {str(e)}")

def deploy(file_list: List[str]) -> None:
    local_file = os.path.join(os.getcwd(), file_list[0].strip())
    dest_file = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    try:
        forcecopy(local_file, dest_file)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error copying file: {str(e)}")


def processcsv(csv_file_path: str, process: Callable[[List[str]], None]) -> NoReturn:
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Error: CSV file not found: {csv_file_path}")
    with open(csv_file_path, 'r') as csvfile:
            destinations = csv.reader(csvfile)
            next(destinations)  
            for row in destinations:
                process(row)

def forcecopy(source: str, destination: str) -> NoReturn:
    if not os.path.exists(source):
        print(f"Error: Source path does not exist: {source}")
        raise FileNotFoundError(f"Source path not found: {source}")

    source_is_dir = os.path.isdir(source)
    dest_is_dir = os.path.isdir(destination)

    if source_is_dir != dest_is_dir:
        print(f"Error: Cannot copy {'directory' if source_is_dir else 'file'} to {'directory' if dest_is_dir else 'file'}")
        raise ValueError("Source and destination types do not match")

    if not os.path.exists(os.path.dirname(destination)):
        print(f"Error: Destination parent directory does not exist: {os.path.dirname(destination)}")
        raise FileNotFoundError(f"Destination parent directory not found: {os.path.dirname(destination)}")

    try:
        if source_is_dir:
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)
        print(f"Copied '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error: Failed to copy '{source}' to '{destination}'")
        print(f"Error details: {str(e)}")
        raise
