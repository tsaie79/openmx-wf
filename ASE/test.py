from ase.calculators.openmx import OpenMX
from ase import Atoms

from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.inputs import Structure

import os

from pymatgen.io.openmx.sets import ScfInputSet


os.chdir(os.path.dirname(__file__))

class CalculationSetup:
    def __init__(self, input_file, magnetic_moments=None):
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
    input_file = "GaAs.vasp"
    calc_setup = CalculationSetup(input_file, magnetic_moments=[2, 2, -1, -1, 0, 0, 0, 0])

    d = ScfInputSet().write_input(calc_setup.st)
    calc_setup.setup_calculation(d)
    


if __name__ == "__main__":
    main()