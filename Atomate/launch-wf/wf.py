from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.openmx.powerups import add_additional_fields_to_taskdocs, set_execution_options

from pymatgen.io.vasp.inputs import Structure
from fireworks import LaunchPad
from fireworks import Workflow


from monty.serialization import loadfn

def calc1(): 
    lp = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")

    st_dict = loadfn('/workspaces/openmx-wf/SrGeSi/initial-train.json')

    for i in st_dict:
        st_ase_dict = st_dict[i]
        print(st_ase_dict)
        st = st_ase_dict['st_vasp_dict']
        # remove the st_vasp_dict key 
        st_ase_dict.pop('st_vasp_dict')
        st_ase_dict['file_from'] = '20230805-training_data/initial-train.xyz'

        fw = OpenmxScfFW(structure=st, run_deeph_preprocess=True, override_default_openmx_params={"kppa": 8000})
        wf = Workflow([fw], name=f"{st.formula}")
        wf = add_additional_fields_to_taskdocs(wf, {"prev_calc": st_ase_dict})
        wf = set_execution_options(wf, category="20230805-training_data")

        lp.add_wf(wf)

        break


if __name__ == '__main__':
    calc1()
