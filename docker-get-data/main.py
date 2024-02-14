import argparse
from get_fs_data import get_deeph_files  # replace 'your_module' with the actual module name

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Get deepH files.")

    # Add the arguments
    parser.add_argument('-d', '--db_file', type=str, required=True, help='The database file')
    parser.add_argument('-t', '--taskid', type=int, required=True, help='The task id of the calculation')
    parser.add_argument('-p', '--dir_path', type=str, required=True, help='The path to store the files')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    get_deeph_files(args.taskid, db=args.db_file, store_in=args.dir_path)


if __name__ == "__main__":
    main()