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

nums = setting['SINCHO']['num_of_parallel']
work_dir = os.path.join(setting['OUTPUT']['directory'], setting['SINCHO']['working_directory'])
order_scale = int(len(str(int(nums)))+1)

for i in range(nums+1):
    n= str(i).zfill(order_scale)
    os.chdir(hdir+"/"+work_dir+"/trajectory_"+n+"/")
    bash('rm -r asphere_output/ p2c_output/ sincho*')
    bash('p2c -m LB -p prot_'+n+'.pdb -l lig_'+n+'.pdb -d '+str(setting['SINCHO']['distance_range']))
    bash('sincho -p prot_'+n+'.pdb -l lig_'+n+'.pdb -n '+str(setting['SINCHO']['npairs_per_snap']))
  
