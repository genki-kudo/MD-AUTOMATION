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


def separate(setting, reslist, temp_dir):
    hdir = os.getcwd()
    os.chdir(temp_dir)
    nums = setting['MD']['edit_trajectory']['necessary-snaps']
    outdir = './separate_file/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    confs = 'conformations.pdb'
    lines = sum([1 for _ in open(confs,'r')])
    perconf = int(lines/(nums+1))

    with open(confs)as f:
        ls = f.readlines()
        ls_rstrip = [l.rstrip("\n") for l in ls]

    order_scale = int(len(str(int(nums)))+1)
    for i in range(nums+1):
        with open(outdir+'/conf_'+str(i).zfill(order_scale)+'.pdb','w')as out:
            out.truncate(0)
        with open(outdir+'/conf_'+str(i).zfill(order_scale)+'.pdb', 'a')as out:
            for j in range(i*perconf, (i+1)*perconf):
                out.write("%s\n" % ls_rstrip[j])

    for i in range(nums+1):
        f_p = outdir+'/prot_'+str(i).zfill(order_scale)+'.pdb'
        f_l = outdir+'/lig_'+str(i).zfill(order_scale)+'.pdb'
        with open(f_p,'w')as out:
            out.truncate(0)
        with open(f_l,'w')as out:
            out.truncate(0)
        protlist = []
        liglist = []
        for j in open(outdir+'/conf_'+str(i).zfill(order_scale)+'.pdb'):
            if j[0:6]=='ATOM  ' or j[0:6]=='HETATM':
                if j[17:20].replace(' ','') in reslist:
                    protlist.append(j.rstrip("\n"))
                if j[17:20].replace(' ','')==str(setting['MD']['preparation']['ligand_resname']):
                    liglist.append(j.rstrip("\n"))
        with open(f_p,'a')as out:
            for j in protlist:
                out.write("%s\n" % j)
        with open(f_l,'a')as out:
            for j in liglist:
                out.write("%s\n" % j)
    os.chdir(hdir)
