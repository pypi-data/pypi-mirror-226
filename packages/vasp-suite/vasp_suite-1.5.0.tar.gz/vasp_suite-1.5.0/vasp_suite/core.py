'''
A programme which holds the core functions of vasp_suite.
'''

# Imports
import numpy as np
import os
from . import structure
from . import input
from . import submission
# Functions

def generate_input(filename: str, calculation: str) -> None:
    '''
    Generates Input files for VASP Calculations.
    '''
    input_files = input.InputFileGenerator(filename, calculation)
    input_files._INCAR()
    input_files._POTCAR()
    return None


def generate_job(title, cores, vasp_type):
    '''
    Generates a submission script for VASP calculations.
    '''
    job = submission.SubmissionWriter(title, cores, vasp_type)
    if job.hostname == 'csf3':
        job.submission_csf3()
    elif job.hostname == 'csf4':
        job.submission_csf4()
    else:
        exit()


def generate_supercell(expansion: np.ndarray) -> None:
    '''
    Generates a supercell from a given expansion matrix.
    '''
    _s = structure.Structure('POSCAR')
    _s.parse_vasp()
    _s.generate_supercell(expansion)
    _s.reorder_supercell()
    _s.write_poscar('POSCAR_supercell')
    return None


def dope_structure(filename: str, dopant: str, replace: str, instances: int) -> None:
    '''
    Dopes a structure with a given dopant and generates all possible structures.
    '''
    _d = structure.DOPE(filename, dopant, replace, instances)
    _d.Generate_structure()
    _d.write_poscars()
    return None


def generate_defect(filename: str, site: str, instances: int) -> None:
    '''
    Generates a defect structure from a given structure.
    '''
    _d = structure.DOPE(filename, 'D', site, instances)
    _d.Generate_structure()
    _d.Create_defect()
    _d.write_poscars()
    return None


def calculate_kpoints(filename: str) -> None:
    '''
    Calculates possible kpoint meshes for a given structure.
    '''
    _s = structure.Structure(filename) 
    _s.parse_vasp() 
    mesh, density = _s.calculate_mesh()
    for i in range(len(mesh)):
        print(f'Mesh: {mesh[i][0]} {mesh[i][1]} {mesh[i][2]} Density: {density[i]}')
    return None

def generate_kpoints(mesh: list) -> None:
    with open('KPOINTS', 'w') as f:
        f.write('Regular {}\t{}\t{} gamma centred mesh\n'.format(*mesh))
        f.write('0\nGamma\n')
        f.write('{}\t{}\t{}\n'.format(*mesh))
        f.write('0 0 0')

def convert_cif(filename: str) -> None:
    '''
    Converts a cif file to a POSCAR file.
    '''
    _s = structure.Structure(filename)
    _s.parse_cif()
    _s.write_poscar('POSCAR')


def molecule(filename: str, atom: str, bond_max: float):
    '''
    Finds a molecule in a structure.
    '''
    poscar = structure.Molecule(filename, atom, bond_max)
    poscar.find_molecule()


def create_input_configurations() -> None:
    '''
    Creates input configurations for VASP calculations.
    '''
    if not os.path.exists(os.path.expanduser('~/.vasp_suite_configs')):
        os.mkdir(os.path.expanduser('~/.vasp_suite_configs'))

    cwd = os.getcwd()
    os.chdir(os.path.expanduser('~/.vasp_suite_configs'))
    with open('relaxation.ini', 'w') as f:
        f.write('''[Relaxation]
prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.1
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = 2
nsw = 100
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    with open('scf.ini', 'w') as f:
        f.write('''[SCF] 
                prec = ACCURATE
lreal = .FALSE.
lasph = .TRUE.
ismear = 0
sigma = 0.1
nelm = 100
nelmin = 4
ncore = 4
ediff = 1e-08
ediffg = -0.01
ibrion = -1
isif = 4
potim = 0.5
lwave = .FALSE.
lcharg = .FALSE.
lorbit = 11
gga = PE
ivdw = 11
''')
    with open('phonon.ini', 'w') as f:
        f.write('''[Phonon]
ALGO = Normal
EDIFF = 1E-8
GGA = PE
ISIF = 2
ISMEAR = 0
LASPH = .TRUE.
LCHARG = .FALSE.
LREAL = .FLASE.
LWAVE = .FALSE.
NSW = 0
PREC = Accurate
SIGMA = 0.01
''')
    os.chdir(cwd)
