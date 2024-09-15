import csv
import os
import shutil
import platform
import subprocess
from typing import NoReturn, List, Callable
import difflib

def diff(file_list: List[str]) -> None:
    local_file = os.path.join(os.getcwd(), file_list[0].strip())
    dest_file = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    
    try:
        with open(local_file, 'r') as file1, open(dest_file, 'r') as file2:
            diff = difflib.unified_diff(
                file1.readlines(),
                file2.readlines(),
                fromfile=local_file,
                tofile=dest_file,
            )
            
            diff_output = ''.join(diff)
            if diff_output:
                print(f"Differences between '{local_file}' and '{dest_file}':")
                print(diff_output)
            else:
                print(f"No differences found between '{local_file}' and '{dest_file}'")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error comparing files: {str(e)}")

def adopt(file_list: List[str]) -> None:
    local_file = os.path.join(os.getcwd(), file_list[0].strip())
    dest_file = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    try:
        forcecopy(local_file, dest_file)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error copying file: {str(e)}")

def deploy(file_list: List[str]) -> None:
    local_file = os.path.join(os.getcwd(), file_list[0].strip())
    dest_file = os.path.join(os.path.expanduser('~'), file_list[1].strip())
    try:
        forcecopy(dest_file, local_file)
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

def forcecopy(origin: str, destination: str) -> NoReturn:
    if not os.path.exists(destination):
        print(f"Warning: Destination file not found: {destination}")
        print(destination)
        raise FileNotFoundError(f"Destination file not found: {destination}")
    try:
        shutil.copy2(destination, origin)
        print(f"Copied '{destination}' to '{origin}'")
    except Exception as e:
        print(f"Initial copy failed: {str(e)}")
        if platform.system() == "Windows":
            try:
                powershell_command = f'Copy-Item -LiteralPath "{destination}" -Destination "{origin}" -Force'
                subprocess.run(["powershell", "-Command", powershell_command], check=True, capture_output=True, text=True)
                print(f"Forcefully copied '{destination}' to '{origin}' using PowerShell")
            except subprocess.CalledProcessError as pe:
                print(f"Error: Failed to copy using PowerShell: {str(pe)}")
                if pe.stdout:
                    print(f"PowerShell stdout: {pe.stdout}")
                if pe.stderr:
                    print(f"PowerShell stderr: {pe.stderr}")
                raise pe
        else:
            print(f"Error: Failed to copy '{destination}' to '{origin}'")
            raise e