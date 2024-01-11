#!/usr/bin/env python

from subprocess import run
import os
import yaml
import sys
from md_preparation.tleap import *
from md_preparation.input_check import *
from md_preparation.convert import *
from md_preparation.equilibration import *
from md_production.production import *
from md_production.trjconv import *
from md_production.separate import *
from md_production.outputs import *
bash=lambda x:run(x,shell=True)

###input args###
conditions = str(sys.argv[1]) # condition.yaml
input_dir = str(sys.argv[2]) # ./
temp_dir = str(sys.argv[3]) # Tsukuba_workflow/MD/
out_dir = str(sys.argv[4]) # Tsukuba_workflow/P2C_SINCHO/ out/yyyymmdd/sincho_out/

###load and preparation###
with open(conditions,'r')as f:
    setting = yaml.safe_load(f)
for i in range(2,5):
    if not os.path.exists(str(sys.argv[i])):
        os.makedirs(str(sys.argv[i]))
reslist = input_check(setting, input_dir, temp_dir)
tleap_exec(setting, temp_dir)
convert(temp_dir)

###equilibration###
equilibration(setting,temp_dir)

###prodiction###
production(setting, temp_dir)

###post-MD
trjconv(setting, temp_dir)
separate(setting, reslist, temp_dir)
outputs(setting, temp_dir, out_dir)






















