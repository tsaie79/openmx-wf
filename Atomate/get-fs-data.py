from atomate.openmx.database import openmxCalcDb
import os

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

OPENMX_DB = openmxCalcDb.from_db_file("/workspaces/openmx-wf/Atomate/setting/db.json", admin=True)


def get_fs_file(taskid, key, f_name, db=OPENMX_DB):
    out = db.get_openmx_output(taskid, key)
    with open(f"/workspaces/openmx-wf/{f_name}", "wb") as f:
        f.write(out)

def get_deeph_files(taskid, db=OPENMX_DB, objs=OBJ_NAMES):
    dir_path = "/workspaces/openmx-wf/deeph"
    os.mkdir(dir_path)
    # run the following loop in parallel
    import concurrent.futures

    def write_output(obj):
        out = db.get_openmx_output(taskid, obj)
        # define the file name by replace the last "_" with "." of obj
        obj = obj[::-1].replace("_", ".", 1)[::-1]
        with open(f"{dir_path}/{obj}", "wb") as f:
            f.write(out)

    # Use a ThreadPoolExecutor to run the loop in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(write_output, objs)


if __name__ == "__main__":
    get_deeph_files(1)