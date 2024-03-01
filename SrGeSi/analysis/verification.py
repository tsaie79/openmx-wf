from pymatgen.core.units import Ha_to_eV, bohr_to_ang

from atomate.openmx.database import openmxCalcDb

import os

import numpy as np

# chdir to the current file
os.chdir(os.path.dirname(os.path.realpath(__file__)))

db = openmxCalcDb.from_db_file("/workspaces/openmx-wf/Atomate/setting/db.json")



def check_force(taskid, plot=True):
    print(f"Checking forces for taskid: {taskid}")
    doc = db.collection.find_one({"task_id": taskid})

    calc_forces = doc["ase_calc"]["forces"]    
    calc_forces = np.array(calc_forces) * Ha_to_eV / bohr_to_ang

    if taskid != 1:
        prev_calc_force = doc["prev_calc"]["force"]
    else:
        prev_calc_force = doc["force"]
    prev_calc_force = np.array(prev_calc_force)

    # calculate the difference between the two forces
    diff = calc_forces - prev_calc_force

    # take abosulte value of the difference
    diff = np.abs(diff)

    # get a heatmap of the difference between the two forces
    print(f"max diff (ev/ang): {np.max(diff).round(4)}")
    print(f"min diff (ev/ang): {np.min(diff).round(4)}")
    print(f"mean diff (ev/ang): {np.mean(diff).round(4)}")
    print(f"std diff (ev/ang): {np.std(diff).round(4)}")


    def get_heatmap(diff):
        # plot a heat map of the difference
        import matplotlib.pyplot as plt

        # get a new diff that only has two values, 0 and 1 where if the value is 0, it is less than 0.05, and if it is 1, it is greater than 0.05

        diff = np.where(diff <= 0.05, 0, 1)

        plt.imshow(diff.transpose())

        plt.yticks([])

        # figure has large part of white space, so remove it
        plt.tight_layout()

        # add title to the plot
        plt.title("Difference between the two forces (ev/ang)\nwhite if <= 0.05, black if > 0.05")
        
        # save the plot
        plt.savefig(f"diff_{taskid}.png")

    if plot:
        get_heatmap(diff)



if __name__ == "__main__":
    check_force(4)