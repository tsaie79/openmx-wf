#https://github.com/materialsproject/api/blob/main/mp_api/client/routes/materials/summary.py

from mp_api.client import MPRester
from mp_api.client.routes.materials.summary import SummaryRester
from monty.serialization import loadfn, dumpfn
import pandas as pd

MPI_KEY = "wInAbIyH5mtLChHmXDzHgjBunoC03q2R"

def get_data():

    req_fields = ["material_id", "formula_pretty", "nsites", "nelements", "energy_above_hull", "band_gap", "is_magnetic"]
    with SummaryRester(api_key=MPI_KEY) as mpr:
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


def get_first_column(file_path):
    df = pd.read_csv(file_path, header=None)
    return df[0].tolist()[1:]


def get_mp_structure():
    mp_ids = get_first_column("/mp/05142024_is_magnetic_false.csv")
    print(f"Number of materials: {len(mp_ids)}, first 5: {mp_ids[:5]}")
    req_fields = ["material_id", "formula_pretty", "structure"]
    with SummaryRester(api_key=MPI_KEY) as mpr:
        # every 500 materials generate a json file
        for i in range(0, len(mp_ids), 500):
            data = mpr.search(material_ids=mp_ids[i:i+500], fields=req_fields)
            table = {}
            for field in req_fields:
                print(f"Field: {field}")
                table[field] = [d.__getattribute__(field) for d in data]
            dumpfn(table, f"/mp/out/mp_structure_{i}-{i+500}.json", indent=4)

if __name__ == "__main__":
    # get_data()
    # get_table()
    get_mp_structure()