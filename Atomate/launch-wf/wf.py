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

        fw = OpenmxScfFW(structure=st, run_deeph_preprocess=True)
        wf = Workflow([fw], name=f"{st.formula}")
        wf = add_additional_fields_to_taskdocs(wf, st_ase_dict)
        wf = set_execution_options(wf, category="20230805-training_data")

        lp.add_wf(wf)

        break


if __name__ == '__main__':
    st_dict = loadfn('/workspaces/openmx-wf/SrGeSi/initial-train.json')

    st_ase_dict = st_dict["0"]
    st = st_ase_dict['st_vasp_dict']
    st.to('poscar.vasp', "POSCAR")
    def ax(structure: Structure, kppvol: int, force_gamma: bool = False):
        """
        Returns an automatic Kpoint object based on a structure and a kpoint
        density per inverse Angstrom^3 of reciprocal cell.

        Algorithm:
            Same as automatic_density()

        Args:
            structure (Structure): Input structure
            kppvol (int): Grid density per Angstrom^(-3) of reciprocal cell
            force_gamma (bool): Force a gamma centered mesh

        Returns:
            Kpoints
        """
        from pymatgen.io.vasp.inputs import Kpoints
        vol = structure.lattice.reciprocal_lattice.volume
        kppa = kppvol * vol * len(structure)
        print(kppa)
        return Kpoints.automatic_density(structure, kppa, force_gamma=force_gamma)

    kpt = ax(st, 0.03)
