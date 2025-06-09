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
name = os.path.normpath(os.path.join(base, './prod.mdp'))

def production(setting, temp_dir):
    hdir = os.getcwd()
    os.chdir(temp_dir)
    gro = 'npt8.gro'
    top = 'complex_wat.top'
    runtime = setting['MD']['production']['runtime']
    timestep = setting['MD']['production']['timestep']
    interval = setting['MD']['production']['output-interval']
    cpu = setting['MD']['preparation']['number_of_cpus']

    with open(name,'r')as f:
        data_lines = f.read()
        data_lines = data_lines.replace("nsteps          = flexible",
                                        "nsteps          = "+str(int(runtime/timestep)))
        data_lines = data_lines.replace("dt              = flexible",
                                        "dt              = "+str(timestep))
        data_lines = data_lines.replace("nstlog          = flexible",
                                        "nstlog          = "+str(int(interval/timestep)))
        data_lines = data_lines.replace("nstxout-compressed = flexible",
                                        "nstxout-compressed = "+str(int(interval/timestep)))

    with open('prod_out.mdp','w')as f:
        f.write(data_lines)
    bash('gmx_mpi grompp -maxwarn 1 -f prod_out.mdp -c '+gro+' -p '+top+
            ' -o prod.tpr -r '+gro+' -n index.ndx')
    bash('gmx_mpi mdrun -deffnm prod -ntomp '+str(cpu))
    gro = 'prod.gro'

    if os.path.isfile("prod.gro"):
        pass
    else:
        print("PRODUCTION RUN FAILED.")
        exit()
    os.chdir(hdir)
    return
