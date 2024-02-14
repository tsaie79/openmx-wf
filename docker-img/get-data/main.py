from atomate.openmx.database import openmxCalcDb
import argparse

collections = [
    "element_dat",
    "hamiltonians_h5",
    "lat_dat",
    "orbital_types_dat",
    "rc_h5",
    "rh_h5",
    "rlat_dat",
    "R_list_dat",
    "site_positions_dat",
]

OBJ_NAMES = tuple(coll for coll in collections)



def get_fs_file(taskid, key, f_name, db="db.json"):
    """
    Get the file from the database and write it to the file system
    Args:
        taskid (int): The task id of the calculation
        key (str): The key of the file to get
        f_name (str): The name of the file to write to
        db (openmxCalcDb): The database to get the file from
    """
    db = openmxCalcDb.from_db_file(db, admin=True)
    out = db.get_openmx_output(taskid, key)
    with open(f"{f_name}", "wb") as f:
        f.write(out)

def get_deeph_files(taskid, store_in, db="db.json", objs=OBJ_NAMES):
    """
    Get the files from the database and write them to the file system
    Args:
        taskid (int): The task id of the calculation
        db (openmxCalcDb): The database to get the files from
        objs (tuple): The names of the files to get
    """
    db = openmxCalcDb.from_db_file(db, admin=True)

    # run the following loop in parallel
    import concurrent.futures
    def write_output(obj):
        out = db.get_openmx_output(taskid, obj)
        # define the file name by replace the last "_" with "." of obj
        obj = obj[::-1].replace("_", ".", 1)[::-1]
        with open(f"{store_in}/{obj}", "wb") as f:
            f.write(out)

    # Use a ThreadPoolExecutor to run the loop in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(write_output, objs)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Get deepH files.")

    # Add the arguments
    parser.add_argument('-d', '--db_file', type=str, help='The path to the database file')
    parser.add_argument('-t', '--taskid', type=int, required=True, help='The task id of the calculation')
    parser.add_argument('-s', '--store_in', type=str, required=True, help='The directory to store the files in')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    get_deeph_files(args.taskid, store_in=args.store_in, db=args.db_file)

if __name__ == "__main__":
    main()  