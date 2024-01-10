#!/usr/bin/env python

from subprocess import run
import os
import yaml
import sys
import numpy as np
import pandas as pd
import argparse
import datetime
from md_preparation.tleap import *
from md_preparation.input_check import *
from md_preparation.convert import *
from md_preparation.equilibration import *
from md_production.production import *
from md_production.trjconv import *
from md_production.separate import *
from md_production.outputs import *

import json

bash=lambda x:run(x,shell=True)

###input args###
conditions = str(sys.argv[1]) # condition.yaml
work_dir = str(sys.argv[2]) # Tsukuba_workflow/P2C_SINCHO/
hdir =os.getcwd()

###load and preparation###
with open(conditions,'r')as f:
    setting = yaml.safe_load(f)

nums = setting['edit_trajectory']['necessary-snaps']

for i in range(nums+1):
    os.chdir(hdir+"/"+work_dir+"/trajectory_"+str(i).zfill(3)+"/")
    bash('rm -r asphere_output/ p2c_output/ sincho*')
    bash('p2c -m LB -p prot_'+str(i).zfill(3)+'.pdb -l lig_'+str(i).zfill(3)+'.pdb -d 10.0')
    bash('sincho -p prot_'+str(i).zfill(3)+'.pdb -l lig_'+str(i).zfill(3)+'.pdb -n 20 ')
  
