from atomate.openmx.database import openmxCalcDb


DB_PATH = "/workspaces/openmx-wf/Atomate/setting/db.json"

# def get_fs_data():
#     db = openmxCalcDb.from_db_file(DB_PATH, admin=True)
#     fs_d
#     return fs_data

if __name__ == "__main__":
    db = openmxCalcDb.from_db_file(DB_PATH, admin=True)
    out = db.get_openmx_scfout(1)

    with open("/workspaces/openmx-wf/openmx.scfout", "wb") as f:
        f.write(out)