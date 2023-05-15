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

def pdb_res_check(file,hit,otherres):
    resname = ['GLY','ALA','VAL','LEU','ILE','ASN','ASP','GLN','PRO',
               'GLU','MET','ARG','LYS','PHE','TRP','TYR','THR','SER',
               'CYS','CYX','HIS','HIE','HID','HIP']
    resname.append(hit)
    reslist = []
    ligfile = ''
    if otherres:
        for j in otherres:
            othfile = ''
            for i in open(file,'r'):
                if i[0:6]=='ATOM  'or i[0:6]=='HETATM':
                    if i[17:20]==j:
                        othfile+=(i)
            with open(j+'.pdb','w')as out:
                out.write(othfile)



    for i in open(file,'r'):
        if i[0:6]=='ATOM  'or i[0:6]=='HETATM':
            if i[17:20] not in resname:
                print('WARNING! this residue is irregular.')
                print(i)
            if i[17:20]=='HIS':
                print('WARNING! Histidine should be specified HIE/HID/HIP')
                print(i)
            #if i[17:20]=='CYS':
                #print('CHECK this Cysteine does not form SS-bond?')
            if i[17:20]==hit:
                ligfile+=(i)
            if i[17:20].replace(' ','') not in reslist:
                reslist.append(i[17:20].replace(' ',''))

    with open(hit+'.pdb','w')as f:
        f.write(ligfile)
    
    if 'HOH' in reslist:
        reslist.remove('HOH')
    if 'WAT' in reslist:
        reslist.remove('WAT')
    reslist.remove(hit)

    return ligfile, reslist


def antechamber(setting, resname):
    pdb = resname+'.pdb'
    prep = resname+'.prep'
    frcmod = resname+'.frcmod'

    mol = Chem.MolFromPDBFile(pdb)
    netc = Chem.rdmolops.GetFormalCharge(mol)
    bash('antechamber -i '+pdb+' -fi pdb -o '+prep+' -fo prepi -c '+setting['preparation']['charge_method']+' -at '+setting['tleap']['ff_ligand']+' -nc '+str(netc))
    bash('parmchk2 -i '+prep+' -o '+frcmod+' -f prepi -s gaff')

    if os.path.isfile(prep) and os.path.isfile(frcmod):
        pass
    else:
        print(resname+" ANTECHAMBER FAILED.")
        exit()


def input_check(setting):
    pdb = setting['preparation']['complex_name']
    hit = setting['preparation']['ligand_resname']
    otherres = setting['preparation']['other_necessary_residue']
    file_exist(pdb)
    ligfile, reslist = pdb_res_check(pdb,hit, otherres)
    ###ligand parameter###
    if os.path.isfile(hit+'.prep')==False or os.path.isfile(hit+'.frcmod')==False:
        antechamber(setting, hit)
    ###ligand parameter###
    if otherres:
        for j in otherres:
            print(j)
            if os.path.isfile(j+'.prep')==False or os.path.isfile(j+'.frcmod')==False:
                antechamber(setting, j)
    
    return reslist

