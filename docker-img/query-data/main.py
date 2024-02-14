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


class GetData:
    def __init__(self, db_file):
        self.db = openmxCalcDb.from_db_file(db_file, admin=True)

    def get_dict(self, taskid, key):
        """
        Get the file from the database and write it to the file system
        Args:
            taskid (int): The task id of the calculation
            key (str): The key of the file to get
        """
        pass
