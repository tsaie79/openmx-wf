from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.vasp.powerups import set_execution_options

from pymatgen.io.vasp.inputs import Structure
from fireworks import LaunchPad
from fireworks import Workflow

structure = Structure.from_file("/workspaces/openmx-wf/Atomate/launch-wf/GaAs.vasp")

fw = OpenmxScfFW(structure=structure, run_deeph_preprocess=True)

wf = Workflow([fw], name=f"{structure.formula}")

wf = set_execution_options(wf, category="test")

lp = LaunchPad.from_file("/workspaces/openmx-wf/Atomate/setting/my_launchpad.yaml")

lp.add_wf(wf)