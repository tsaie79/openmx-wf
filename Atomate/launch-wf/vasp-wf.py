from atomate.openmx.fireworks.core import StaticFW
from pymatgen.io.vasp.inputs import Structure
from fireworks import LaunchPad
from fireworks import Workflow

structure = Structure.from_file("/workspaces/openmx-wf/Atomate/launch-wf/C.cif")


fw = StaticFW(structure=structure, name="C", vasp_input_set="MPRelaxSet", vasp_cmd="openmx")

wf = Workflow([fw], name="C")

lp = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")

lp.add_wf(wf)
