#!/usr/bin/env python

from subprocess import run
import os
import yaml
import sys

bash=lambda x:run(x,shell=True)

###input args###
conditions = str(sys.argv[1]) # condition.yaml
hdir =os.getcwd()

###load and preparation###
with open(conditions,'r')as f:
    setting = yaml.safe_load(f)

nums = setting['P2C_SINCHO']['num_of_parallel']
work_dir = setting['P2C_SINCHO']['working_directory']

for i in range(nums+1):
    n= str(i).zfill(3)
    os.chdir(hdir+"/"+work_dir+"/trajectory_"+n+"/")
    bash('rm -r asphere_output/ p2c_output/ sincho*')
    bash('p2c -m LB -p prot_'+n+'.pdb -l lig_'+n+'.pdb -d '+str(setting['P2C_SINCHO']['distance_range']))
    bash('sincho -p prot_'+n+'.pdb -l lig_'+n+'.pdb -n '+str(setting['P2C_SINCHO']['npairs_per_snap']))
  
