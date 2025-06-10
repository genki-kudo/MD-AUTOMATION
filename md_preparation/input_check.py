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
from pymol import cmd

bash=lambda x:run(x,shell=True)

def file_exist(file):
    if os.path.isfile(file):
        print(file, 'exists')
    else:
        print('FATAL!', file, 'does not existed!')
        exit()
    return

def pdb_res_check(file, hit, otherres, temp_dir):
    resname = ['GLY','ALA','VAL','LEU','ILE','ASN','ASP','GLN','PRO',
               'GLU','MET','ARG','LYS','PHE','TRP','TYR','THR','SER',
               'CYS','CYX','HIS','HIE','HID','HIP']
    resname.append(hit)
    reslist = []
    ligfile = ''
    #->同じ化合物が2個以上入っている場合に未対応。(2024/01/10)
    if otherres:
        for j in otherres:
            resname.append(j)
            othfile = ''
            for i in open(file,'r'):
                if i[0:6]=='ATOM  'or i[0:6]=='HETATM':
                    if i[17:20]==j:
                        othfile+=(i)
            with open(os.path.join(temp_dir, j+'.pdb'),'w')as out:
                out.write(othfile)
    #<-同じ化合物が2個以上入っている場合に未対応。(2024/01/10)

    for i in open(file,'r'):
        if i[0:6]=='ATOM  'or i[0:6]=='HETATM':
            if i[17:20] not in resname and i[17:20] not in ["HOH", "WAT"]:
                print('WARNING! this residue is irregular.')
                print(i)
            if i[17:20]=='HIS':
                print('WARNING! Histidine should be specified HIE/HID/HIP')
                print(i)
            if i[17:20]=='CYS':
                print('CHECK this Cysteine does not form SS-bond?')
            if i[17:20]==hit:
                ligfile+=(i)
            if i[17:20].replace(' ','') not in reslist:
                reslist.append(i[17:20].replace(' ',''))

    with open(os.path.join(temp_dir, hit+'.pdb'),'w')as f:
        f.write(ligfile)
    
    if 'HOH' in reslist:
        reslist.remove('HOH')
    if 'WAT' in reslist:
        reslist.remove('WAT')
    reslist.remove(hit)

    return ligfile, reslist


def antechamber(setting, resname,temp_dir):
    hdir = os.getcwd()
    os.chdir(temp_dir)
    pdb = resname+'.pdb'
    prep = resname+'.prep'
    frcmod = resname+'.frcmod'

    mol = Chem.MolFromPDBFile(pdb)
    netc = Chem.rdmolops.GetFormalCharge(mol)
    bash('antechamber -i '+pdb+' -fi pdb -o '+prep+' -fo prepi -c '+setting['MD']['preparation']['charge_method']+' -at '+setting['MD']['tleap']['ff_ligand']+' -nc '+str(netc))
    bash('parmchk2 -i '+prep+' -o '+frcmod+' -f prepi -s gaff')

    if os.path.isfile(prep) and os.path.isfile(frcmod):
        pass
    else:
        print(resname+" ANTECHAMBER FAILED.")
        exit()
    os.chdir(hdir)


def input_check(setting, temp_dir):
    os.makedirs(temp_dir,exist_ok=True)
    pdb = setting['MD']['preparation']['complex_name']
    hit = str(setting['MD']['preparation']['ligand_resname'])
    otherres = setting['MD']['preparation']['other_necessary_residue']

    file_exist(pdb)
    bash("cp "+setting['MD']['preparation']['complex_name']+" "+temp_dir+"/")
    ligfile, reslist = pdb_res_check(pdb, hit, otherres, temp_dir)
    ###ligand parameter###
    if os.path.isfile(hit+'.prep')==False or os.path.isfile(hit+'.frcmod')==False:
        antechamber(setting, hit, temp_dir)
    else:
        bash("cp "+hit+".prep"+" "+temp_dir+"/"+hit+".prep")
        bash("cp "+hit+".frcmod"+" "+temp_dir+"/"+hit+".frcmod")
    ###ligand parameter###
    if otherres:
        for j in otherres:
            print(j)
            if os.path.isfile(j+'.prep')==False or os.path.isfile(j+'.frcmod')==False:
                antechamber(setting, j, temp_dir)
            else:
                bash("cp "+j+".prep"+" "+temp_dir+"/"+j+".prep")
                bash("cp "+j+".frcmod"+" "+temp_dir+"/"+j+".frcmod")
    
    return reslist

