import sys
from util import adopt, processcsv
from settings import default_csv_file

csv_file_path = ""

def main():
    try:
        processcsv(csv_file_path, adopt)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__=='__main__':
    csv_file_path = default_csv_file if len(sys.argv) < 2 else sys.argv[1]
    main()
