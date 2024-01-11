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


bash=lambda x:run(x,shell=True)
base = os.path.dirname(os.path.abspath(__file__))

def trjconv(setting):
    temp_dir = setting['MD']['working_directory']
    hdir = os.getcwd()
    os.chdir(temp_dir)

    runtime = setting['MD']['production']['runtime']
    timestep = setting['MD']['production']['timestep']
    interval = setting['MD']['production']['output-interval']

    bash('gmx_mpi trjconv -f prod.xtc -o prodnj1.xtc -s complex_wat.gro -n index.ndx -pbc nojump << EOF\n System\n EOF')
    bash('gmx_mpi trjconv -f prodnj1.xtc -o prodnj2.xtc -s complex_wat.gro -n index.ndx -center <<EOF\n Protein\n System\n EOF')
    bash('gmx_mpi trjconv -f prodnj2.xtc -o prodnj3.xtc -s complex_wat.gro -n index.ndx -ur rect -pbc mol <<EOF\n System\n EOF')
    bash('gmx_mpi trjconv -f prodnj3.xtc -o prodnj4.xtc -s complex_wat.gro -n index.ndx -fit rot+trans <<EOF\n C-alpha\n System\n EOF')

    b= setting['MD']['edit_trajectory']['start-range']
    e= setting['MD']['edit_trajectory']['end-range']
    steps = setting['MD']['edit_trajectory']['necessary-snaps']
    allsnaps = int(int(runtime/timestep)/int(interval/timestep))
    rate = (e-b)/runtime

    skip = int(allsnaps*rate/steps)

    bash('gmx_mpi trjconv -f prodnj4.xtc -s min1.tpr -n index.ndx -o conformations.pdb -b '+str(b)+' -e '+str(e)+' -skip '+str(skip)+' <<EOF\nnon-Water\n EOF')
    
    if os.path.isfile("conformations.pdb"):
        pass
    else:
        print("TRAJECTORY CONVERT FAILED.")
        exit()

    os.chdir(hdir)
    return
