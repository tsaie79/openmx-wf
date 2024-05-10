#https://github.com/materialsproject/api/blob/main/mp_api/client/routes/materials/summary.py

from mp_api.client import MPRester
from mp_api.client.routes.materials.summary import SummaryRester
from monty.serialization import loadfn, dumpfn
import pandas as pd


def get_data():
    mpi_key = "wInAbIyH5mtLChHmXDzHgjBunoC03q2R"

    req_fields = ["material_id", "formula_pretty", "nsites", "nelements", "energy_above_hull", "band_gap", "is_magnetic"]
    with SummaryRester(api_key=mpi_key) as mpr:
        data = mpr.search(total_magnetization=(None, None), fields=req_fields)

    table = {}
    for field in req_fields:
        print(f"Field: {field}")
        table[field] = [d.__getattribute__(field) for d in data]

    dumpfn(table, "mp_data.json", indent=4)

def get_table():
    # get csv
    table = loadfn("mp_data.json")
    df = pd.DataFrame(table)
    # find those with the field "is_magentic" is True
    df = df[df["is_magnetic"] == False].sort_values(["energy_above_hull", "band_gap"], ascending=[True, False])
    df.to_csv("mp_data.csv", index=False)

if __name__ == "__main__":
    # get_data()
    get_table()