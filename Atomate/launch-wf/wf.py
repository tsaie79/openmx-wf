from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.openmx.powerups import add_additional_fields_to_taskdocs, set_execution_options

from pymatgen.io.vasp.inputs import Structure, Kpoints
from fireworks import LaunchPad
from fireworks import Workflow


from monty.serialization import loadfn

from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt


def calc1(batch_id, kppa=2e3):
    lpad = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")

    st_dict = loadfn('/workspaces/openmx-wf/SrGeSi/initial-train.json')

    for i in range((batch_id-1)*10, batch_id*10):
        if i >= len(st_dict):
            break
        st_ase_dict = st_dict[str(i)]
        st = st_ase_dict['st_vasp_dict']
        # remove the st_vasp_dict key 
        st_ase_dict.pop('st_vasp_dict')
        st_ase_dict['file_from'] = '20230805-training_data/initial-train.xyz'

        # User Precise VPS
        ## vps_option_dict = dict(zip(st.symbol_set, ["Precise"] * len(st.symbol_set)))
        ## fw = OpenmxScfFW(structure=st, run_deeph_preprocess=True, override_default_openmx_params={"kppa": kppa}, potcar_spec=vps_option_dict)
        
        fw = OpenmxScfFW(structure=st, run_deeph_preprocess=True, override_default_openmx_params={"kppa": kppa})
        wf = Workflow([fw], name=f"{st.formula}")

        def get_kpts(kppa, structure):
            kpoints = Kpoints.automatic_density(structure, kppa)
            # if kpt in one direction is even, make it odd
            kpoints.kpts[0][0] = kpoints.kpts[0][0] + 1 if kpoints.kpts[0][0] % 2 == 0 else kpoints.kpts[0][0]
            kpoints.kpts[0][1] = kpoints.kpts[0][1] + 1 if kpoints.kpts[0][1] % 2 == 0 else kpoints.kpts[0][1]
            kpoints.kpts[0][2] = kpoints.kpts[0][2] + 1 if kpoints.kpts[0][2] % 2 == 0 else kpoints.kpts[0][2]
            print(kpoints.kpts)
            return kpoints

        print(get_kpts(kppa, st).kpts[0][0])
        # wf = add_additional_fields_to_taskdocs(wf, {"prev_vasp_calc": st_ase_dict, 
        #                                             "test_target": {"vps_option_dict": vps_option_dict, 
        #                                                             "kppa": kppa,
        #                                                             "kgrids": get_kpts(kppa, st).kpts[0][0]}})

        wf = add_additional_fields_to_taskdocs(wf, {"prev_vasp_calc": st_ase_dict})
        
        wf = set_execution_options(wf, category="20230805-training_data")

        lpad.add_wf(wf)

def run_batch():
    # use parallel to run the function of calc1 from batch 37 to 40
    # from multiprocessing import Pool
    with Pool(4) as p:
        p.map(calc1, [37, 38, 39, 40])

def check_fw():
    lpad = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    total_num_fws = len(lpad.get_fw_ids({}))
    # print the number of fireworks that are COMPLETED
    num_completed_fws = len(lpad.get_fw_ids({"state": "COMPLETED"}))
    ## print number and percentage of completed fireworks
    print(f"Number of completed fireworks: {num_completed_fws} ({num_completed_fws/total_num_fws*100:.2f}%)")
    # print the number of fireworks that are FIZZLED
    num_fizzled_fws = len(lpad.get_fw_ids({"state": "FIZZLED"}))
    print(f"Number of fizzled fireworks: {num_fizzled_fws} ({num_fizzled_fws/total_num_fws*100:.2f}%)")
    # print RUNNING
    num_running_fws = len(lpad.get_fw_ids({"state": "RUNNING"}))
    print(f"Number of running fireworks: {num_running_fws} ({num_running_fws/total_num_fws*100:.2f}%)")
    # print pending
    num_pending_fws = len(lpad.get_fw_ids({"state": "PENDING"}))
    print(f"Number of pending fireworks: {num_pending_fws} ({num_pending_fws/total_num_fws*100:.2f}%)")
    # print the number of fireworks that are READY
    num_ready_fws = len(lpad.get_fw_ids({"state": "READY"}))
    print(f"Number of ready fireworks: {num_ready_fws} ({num_ready_fws/total_num_fws*100:.2f}%)")



# use parallel to get the runtime of each firework
def get_runtime(fw_id):
    lpad = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    try:
        launch = lpad.get_launch_by_id(fw_id)
        runtime = launch.runtime_secs
        # if type is not float, return 0
        if type(runtime) != float:
            return 0
        return runtime
    except:
        return 0
    

def eval_time_per_fw(plot=False):
    lpad = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    fws = lpad.get_fw_ids({"state": "COMPLETED"})

    with Pool(len(fws)) as p: # len(fws) means the number of parallel processes
        runtimes = p.map(get_runtime, fws)
        # get average runtime and standard deviation
    print(f"Total number of completed fireworks: {len(runtimes)}")
    runtimes = np.array(runtimes)
    # conver runtime from seconds to minutes
    runtimes = runtimes/60
    # remove the 0
    runtimes = runtimes[runtimes != 0]
    print(f"Average runtime: {runtimes.mean():.2f}min")
    print(f"Standard deviation: {runtimes.std():.2f}min")

    if plot:
        # plot a normal distribution of runtime
        plt.hist(runtimes, bins=100, edgecolor='black')
        plt.xlabel('Runtime (min)')
        plt.ylabel('Frequency')
        plt.title('Runtime Distribution')
        plt.show()




if __name__ == '__main__':
    # run_batch()
    eval_time_per_fw(plot=False)
    check_fw()


