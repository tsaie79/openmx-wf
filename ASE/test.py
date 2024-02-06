from ase.calculators.openmx import OpenMX
from ase import Atoms

from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.inputs import Structure

import os

os.chdir(os.path.dirname(__file__))

# add environment variables, export OPENMX_DFT_DATA_PATH=/openmx/DFT_DATA13
os.environ["OPENMX_DFT_DATA_PATH"] = "/workspaces/openmx-wf/ASE/DFT_DATA19"
os.environ["ASE_OPENMX_COMMAND"] = "openmx"


st = Structure.from_file("C.cif")

atom_adaptor = AseAtomsAdaptor()

atoms = atom_adaptor.get_atoms(st)

calc = OpenMX(xc="PBE")

calc.write_input(atoms)


