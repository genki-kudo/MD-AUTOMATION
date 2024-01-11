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

def tleap_exec(setting):
    temp_dir = setting['MD']['working_directory']
    hdir = os.getcwd()
    os.chdir(temp_dir)

    # Load PDB file and parse structure
    pdb = Chem.MolFromPDBFile(str(setting['MD']['mv']['input_complex'][0].split("/")[-1]))
    # Convert to 3D coordinates and get list of atoms
    atoms = pdb.GetAtoms()
    # Calculate centroid coordinates
    centroid = [0.0, 0.0, 0.0]
    total = 0
    for atom in atoms:
        mass = atom.GetMass()
        coords = pdb.GetConformer().GetAtomPosition(atom.GetIdx())
        centroid[0] += coords.x
        centroid[1] += coords.y
        centroid[2] += coords.z
        total += 1
    centroid = [round(-(coord / total),3) for coord in centroid]

    with open('./leap.txt','w')as leap:
        print("",file=leap)
    with open('./leap.txt','a')as leap:
        print('source leaprc.protein.'+setting['MD']['tleap']['ff_protein'], file=leap)
        print('source leaprc.'+setting['MD']['tleap']['ff_ligand'], file=leap)
        print('source leaprc.water.'+setting['MD']['tleap']['ff_water'], file=leap)
        print('loadAmberPrep '+str(setting['MD']['preparation']['ligand_resname'])+'.prep', file=leap)
        print('loadamberparams '+str(setting['MD']['preparation']['ligand_resname'])+'.frcmod', file=leap)
        if setting['MD']['preparation']['other_necessary_residue']:
            for j in setting['MD']['preparation']['other_necessary_residue']:
                print('loadAmberPrep '+str(j)+'.prep', file=leap)
                print('loadamberparams '+str(j)+'.frcmod', file=leap)
        print('loadamberparams frcmod.ions1lm_1264_tip3p', file=leap)
        #print('loadamberparams frcmod.ions234lm_1264_tip3p', file=leap)
        
        print()
        
        print('mol = loadpdb '+str(setting['MD']['mv']['input_complex'][0].split("/")[-1]), file=leap)

        print('addions2 mol Na+ 0', file=leap)
        print('addions2 mol Cl- 0', file=leap)

        if setting['MD']['tleap']['translate_origin']==True:
            coordinates = str(centroid[0])+', '+str(centroid[1])+', '+str(centroid[2])
            print('translate mol {'+coordinates+' }', file=leap)
        
        if setting['MD']['tleap']['box']=='rectangular':
            print('solvatebox mol TIP3PBOX '+str(setting['MD']['tleap']['rect_around_box']), file=leap)
        elif setting['MD']['tleap']['box']=='cube':
            length = str(setting['MD']['tleap']['cube_size'])
            length = length+', '+length+', '+length+' '
            print('set mol box {'+length+'}', file=leap)
            print('solvatebox mol TIP3PBOX 0.1', file=leap)
        

        print('saveamberparm mol ./complex_wat.prmtop ./complex_wat.inpcrd',file=leap)
        print('savepdb mol complex_wat.pdb',file=leap)
        print('charge mol',file=leap)
        print('quit',file=leap)

    bash('tleap -f leap.txt')

    if os.path.isfile("complex_wat.inpcrd")and os.path.isfile("complex_wat.prmtop"):
        pass
    else:
        print("TLEAP FAILED.")
        exit()
    os.chdir(hdir)
    return