import csv
import os
import shutil
import sys
import platform
import subprocess

# Set default CSV file path
default_csv_file = 'deploy-destinations.csv'

# Use default CSV file or get from command-line argument
csv_file_path = default_csv_file if len(sys.argv) < 2 else sys.argv[1]

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    print(f"Error: CSV file not found: {csv_file_path}")
    sys.exit(1)

# Read the CSV file
with open(csv_file_path, 'r') as csvfile:
    destinations = csv.reader(csvfile)
    next(destinations)  # Skip header if present

    # Loop through each row in the CSV file
    for row in destinations:
        local_file = row[0].strip()
        dest_file = os.path.join(os.path.expanduser('~'), row[1].strip())

        # Check if the destination file exists
        if not os.path.exists(dest_file):
            print(f"Warning: Destination file not found: {dest_file}")
            print(dest_file)
            continue
        # Perform the copy operation
        try:
            shutil.copy2(dest_file, local_file)
            print(f"Copied '{dest_file}' to '{local_file}'")
        except Exception as e:
            print(f"Initial copy failed: {str(e)}")
            if platform.system() == "Windows":
                try:
                    full_local_path = os.path.join(os.getcwd(), local_file)
                    powershell_command = f'Copy-Item -LiteralPath "{dest_file}" -Destination "{full_local_path}" -Force'
                    subprocess.run(["powershell", "-Command", powershell_command], check=True, capture_output=True, text=True)
                    print(f"Forcefully copied '{dest_file}' to '{full_local_path}' using PowerShell")
                except subprocess.CalledProcessError as pe:
                    print(f"Error: Failed to copy using PowerShell: {str(pe)}")
                    if pe.stdout:
                        print(f"PowerShell stdout: {pe.stdout}")
                    if pe.stderr:
                        print(f"PowerShell stderr: {pe.stderr}")
            else:
                print(f"Error: Failed to copy '{dest_file}' to '{local_file}'")