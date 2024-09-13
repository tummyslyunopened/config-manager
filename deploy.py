import csv
import os
import shutil
import sys

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

        # Check if the local file exists
        if not os.path.exists(local_file):
            print(f"Warning: Local file not found: {local_file}")
            continue

        # Ensure the destination directory exists
        dest_dir = os.path.dirname(dest_file)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
                print(f"Created directory: {dest_dir}")
            except Exception as e:
                print(f"Error: Failed to create directory: {dest_dir}. Error: {str(e)}")
                continue

        # Perform the copy operation
        try:
            shutil.copy2(local_file, dest_file)
            print(f"Copied '{local_file}' to '{dest_file}'")
        except Exception as e:
            print(f"Error: Failed to copy '{local_file}' to '{dest_file}': {str(e)}")