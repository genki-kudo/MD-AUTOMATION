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


def outputs(setting, temp_dir, out_dir):


    nums = setting['edit_trajectory']['necessary-snaps']
    outdir = setting['edit_trajectory']['output_dir']
    for i in range(nums+1):
        if not os.path.exists(out_dir+"trajectory_"+str(i).zfill(3)):
            os.makedirs(out_dir+"trajectory_"+str(i).zfill(3))
        f_p = temp_dir+outdir+'/prot_'+str(i).zfill(3)+'.pdb'
        f_l = temp_dir+outdir+'/lig_'+str(i).zfill(3)+'.pdb'
    
        #bash("cp "+f_p+" "+out_dir+"trajectory_"+str(i).zfill(3)+"/prot_"+str(i).zfill(3)+".pdb")
        #bash("cp "+f_l+" "+out_dir+"trajectory_"+str(i).zfill(3)+"/lig_"+str(i).zfill(3)+".pdb")
        bash('obabel -ipdb '+f_p+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(3)+'/prot_'+str(i).zfill(3)+'.pdb')
        bash('obabel -ipdb '+f_l+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(3)+'/lig_'+str(i).zfill(3)+'.pdb')
