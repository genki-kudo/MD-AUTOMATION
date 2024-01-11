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
name = os.path.normpath(os.path.join(base, './conv_amb_grom/groconvert.sh'))

def convert(setting):
    temp_dir = setting['MD']['working_directory']
    hdir = os.getcwd()
    os.chdir(temp_dir)
    file_name = 'complex_wat'

    bash('cp '+file_name+'.prmtop leap.parm7')
    bash('cp '+file_name+'.inpcrd leap.rst7')
    bash(name+' -i leap -o '+file_name+' -r')
    bash('gmx_mpi make_ndx -f '+file_name+'.gro <<EOF\n q\n EOF')
    
    if os.path.isfile("complex_wat.top")and os.path.isfile("complex_wat.gro")and os.path.isfile("index.ndx"):
        pass
    else:
        print("TOPOLOGY CONVERT FAILED.")
        exit()
    os.chdir(hdir)
    return