from subprocess import run
import os
import glob
import yaml
import math
import shutil
import sys
import numpy as np
import pandas as pd
import argparse
import datetime
from rdkit import Chem
from rdkit.Chem import AllChem


import json

bash=lambda x:run(x,shell=True)

base = os.path.dirname(os.path.abspath(__file__))
name = os.path.normpath(os.path.join(base, './equi_template/'))
mdplist = ['min1','min2','nvt','npt1','npt2','npt3','npt4','npt5','npt6','npt7','npt8']

def equilibration(setting, temp_dir):
    hdir = os.getcwd()
    os.chdir(temp_dir)
    gro = 'complex_wat.gro'
    top = 'complex_wat.top'
    cpu = setting['preparation']['number_of_cpus']

    for f in mdplist:
        mdpfile = name+'/'+f+'.mdp'
        bash('gmx_mpi grompp -maxwarn 1 -f '+mdpfile+' -c '+gro+' -p '+top+
             ' -o '+f+'.tpr -r '+gro+' -n index.ndx')
        bash('gmx_mpi mdrun -deffnm '+f+' -ntomp '+str(cpu))
        gro = f+'.gro'
    
    if os.path.isfile("npt8.gro"):
        pass
    else:
        print("EQUILIBRATION FAILED.")
        exit()
    os.chdir(hdir)
    return