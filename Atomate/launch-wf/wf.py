from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.openmx.powerups import add_additional_fields_to_taskdocs, set_execution_options

from pymatgen.io.vasp.inputs import Structure, Kpoints
from fireworks import LaunchPad
from fireworks import Workflow

from monty.serialization import loadfn

from multiprocessing import Pool

class BatchRunner:
    def __init__(self, launchpad_file):
        self.lpad = LaunchPad.from_file(launchpad_file)

    def calc1(self, batch_id, kppa=2e3):
        st_dict = loadfn('/workspaces/openmx-wf/SrGeSi/initial-train.json')
        print(f"Batch {batch_id} started, Length of st_dict: {len(st_dict)}")
        for i in range((batch_id-1)*10, batch_id*10):
            print(f"Processing structure {i}")
            if i >= len(st_dict):
                break
            st_ase_dict = st_dict[str(i)]
            st = st_ase_dict['st_vasp_dict']
            # remove the st_vasp_dict key 
            st_ase_dict.pop('st_vasp_dict')
            st_ase_dict['file_from'] = '20230805-training_data/initial-train.xyz'

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

            wf = add_additional_fields_to_taskdocs(wf, {"prev_vasp_calc": st_ase_dict})
            
            wf = set_execution_options(wf, category="20230805-training_data")

            # self.lpad.add_wf(wf)

    def run_batch(self):
        # use parallel to run the function of calc1 from batch 73 to finish
        with Pool(1) as p:
            p.map(self.calc1, [72])
        # clean up the memory
        p.close()
        p.join()
        print("Batch finished")



if __name__ == "__main__":
    runner = BatchRunner("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")
    runner.run_batch()