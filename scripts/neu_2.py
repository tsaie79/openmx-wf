import numpy as np
from pymatgen.core.structure import Structure
import os
import subprocess

np_cores = 56
pot_path = "/home/p.cui/Downloads/openmx/openmx3.9/DFT_DATA19"

inter_layer = 3.35
structure = Structure.from_file('input/Graphene.cif')
N_ATOM = len(structure)
np.random.seed(42)

for index_shift in range(30):
    displace_x = np.random.rand() - 0.5  # -0.5 ~ 0.5
    displace_y = np.random.rand() - 0.5  # -0.5 ~ 0.5

    frac_coords = structure.frac_coords
    lattice = structure.lattice.matrix
    print(lattice)
    frac_coords = np.concatenate([frac_coords, frac_coords, frac_coords])
    frac_coords += np.concatenate([np.array([0] * N_ATOM + [displace_x] * N_ATOM + [0] * N_ATOM).reshape(N_ATOM * 3, 1),
                                   np.array([0] * N_ATOM + [displace_y] * N_ATOM + [0] * N_ATOM).reshape(N_ATOM * 3, 1),
                                   np.array([0.4] * N_ATOM + [0.4 + inter_layer / lattice[2, 2]] * N_ATOM + [
                                       0.4 + 2 * inter_layer / lattice[2, 2]] * N_ATOM).reshape(
                                       N_ATOM * 3, 1)], axis=-1)

    structure_shift = Structure(lattice, ['C'] * N_ATOM * 3,
                                frac_coords,
                                coords_are_cartesian=False,
                                to_unit_cell=True)

    structure_shift.make_supercell([[4, 0, 0], [0, 4, 0], [0, 0, 1]])
    N_supercell = len(structure_shift)

    for index_perturb in range(20):
        cart_coords = structure_shift.cart_coords
        lattice = structure_shift.lattice.matrix

        disorder_x = (np.random.rand(N_supercell, 1) - 0.5) * 0.1  # -0.05 ~ 0.05
        disorder_y = (np.random.rand(N_supercell, 1) - 0.5) * 0.1  # -0.05 ~ 0.05
        disorder_z = (np.random.rand(N_supercell, 1) - 0.5) * 0.4  # -0.2 ~ 0.2

        cart_coords += np.concatenate([disorder_x, disorder_y, disorder_z], axis=-1)

        structure_shift_perturb = Structure(lattice, ['C'] * N_supercell,
                                            cart_coords,
                                            coords_are_cartesian=True,
                                            to_unit_cell=True)

        frac_coords = structure_shift_perturb.frac_coords
        frac_coords_str = ''
        for i in range(len(structure_shift)):
            frac_coords_str += f' {i + 1} C {frac_coords[i, 0]} {frac_coords[i, 1]} {frac_coords[i, 2]} 2.0  2.0'
            if i != len(structure_shift) - 1:
                frac_coords_str += '\n'

        lattice_vector_str = str(structure_shift_perturb.lattice.matrix).replace("[", "").replace("]", "")

        # print(frac_coords_str)
        # print("\n\n\n")

        openmx_input = f"""System.Name                       openmx
    DATA.PATH                         {pot_path}
    HS.fileout                        on

    Species.Number                    1
    <Definition.of.Atomic.Species
      C    C6.0-s2p2d1          C_PBE19
    Definition.of.Atomic.Species>
    Atoms.Number                      96
    Atoms.SpeciesAndCoordinates.Unit  FRAC
    <Atoms.SpeciesAndCoordinates
{frac_coords_str}
    Atoms.SpeciesAndCoordinates>

    Atoms.UnitVectors.Unit            Ang
    <Atoms.UnitVectors
{lattice_vector_str}
    Atoms.UnitVectors>

    scf.XcType                        GGA-PBE   # LDA/LSDA-CA/LSDA-PW/GGA-PBE
    scf.ElectronicTemperature         300.0     # default=300 (K) SIGMA in VASP ???
    scf.energycutoff                  300       # default=150 (Ry = 13.6eV) ???
    scf.maxIter                       2000
    scf.EigenvalueSolver              Band      # DC/DC-LNO/Krylov/ON2/Cluster/Band
    scf.Kgrid                         10  10  1 ??? 
    scf.criterion                     4e-08     # (Hartree = 27.21eV)
    scf.partialCoreCorrection         on

    scf.SpinPolarization              off
    scf.SpinOrbit.Coupling            off

    scf.Mixing.Type                   simple
    # 1DFFT.NumGridK                    900
    # 1DFFT.NumGridR                    900
    # 1DFFT.EnergyCutoff                3600.0

    scf.ProExpn.VNA                   off

    MD.Type                           Nomd      # Nomd (SCF) / NVT_NH (MD)
    ### END ###"""
        slurm_openmx_submit_script = """#!/bin/bash
#SBATCH --job-name=TBG_data
#SBATCH --output=tbg.out
#SBATCH --constraint=cascadelake
#SBATCH --error=tbg.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node={np_cores}
#SBATCH --exclusive 
#SBATCH --time=24:00:00
#SBATCH --mem=100G
#SBATCH --partition=short


export PATH=/home/p.cui/Downloads/openmx/openmx3.9_neu/source:$PATH
module load intel-oneapi/2021.1_u9
source /shared/centos7/intel/oneapi/2021.1_u9-base/setvars.sh
mpiexec -np {np_cores} openmx openmx_in.dat""".format(np_cores=np_cores)
        os.makedirs(f'./dataset/raw/{index_shift}_{index_perturb}', exist_ok=True)
        with open(f'./dataset/raw/{index_shift}_{index_perturb}/openmx_in.dat', 'w') as save_f:
            save_f.write(openmx_input)

        with open(f'./dataset/raw/{index_shift}_{index_perturb}/openmx_neu.slurm', 'w') as save_f:
            save_f.write(slurm_openmx_submit_script)

        cmd_output = subprocess.run(["sbatch", "openmx_neu.slurm"], capture_output=True, text=True,
                                    cwd=f'./dataset/raw/{index_shift}_{index_perturb}')
        print(cmd_output.stdout)
