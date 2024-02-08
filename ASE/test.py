from ase.calculators.openmx import OpenMX
from ase import Atoms

from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.inputs import Structure

import os

from pymatgen.io.openmx.sets import ScfInputSet


os.chdir(os.path.dirname(__file__))

class CalculationSetup:
    def __init__(self, structure, magnetic_moments=None):
        self.input_file = input_file

        # load structure from file
        self.st = Structure.from_file(self.input_file)

        atom_adaptor = AseAtomsAdaptor()
        self.atoms = atom_adaptor.get_atoms(self.st)

        # set magnetic moments
        if magnetic_moments:
            self.atoms.set_initial_magnetic_moments(magnetic_moments)

    def setup_calculation(self, inputs):
        # add environment variables
        os.environ["OPENMX_DFT_DATA_PATH"] = "/workspaces/openmx-wf/ASE/DFT_DATA19"
        os.environ["ASE_OPENMX_COMMAND"] = "openmx"


        calc = OpenMX(label=f"{self.st.formula}_openmx", **inputs)
        calc.write_input(self.atoms, properties=["magmoms", "forces", "stress"])

def main():
    os.environ["OPENMX_DFT_DATA_PATH"] = "/workspaces/openmx-wf/ASE/DFT_DATA19"
    os.environ["ASE_OPENMX_COMMAND"] = "openmx"

    input_file = "GaAs.vasp"
    st = Structure.from_file(input_file)
    print(f"st: {st}")
    vis = ScfInputSet(structure=st)
    print(f"vis: {vis.as_dict()}")
    inputs = vis.as_dict()

    atoms = AseAtomsAdaptor().get_atoms(st)
    calc = OpenMX(label="test", **inputs)

    calc.write_input(atoms, properties=["magmoms", "forces", "stress"])

    


if __name__ == "__main__":
    main()