from ase import io
from pymatgen.io.ase import AseAtomsAdaptor
import os 

# change the directory to the current file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_xyz(filename):
    return io.read(filename, index=':')

def tansform_xyz_to_st(st_ase):
    st = AseAtomsAdaptor.get_structure(st_ase)
    return st


def main():
    sts = read_xyz('20230805-training_data/initial-train.xyz')
    for i, st in enumerate(sts):
        st = tansform_xyz_to_st(st)
        st.to(f'20230805-training_data/train/{i}.vasp', "poscar")

if __name__ == '__main__':
    main()
    
