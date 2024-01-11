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

###load and preparation###
with open(conditions,'r')as f:
    setting = yaml.safe_load(f)

reslist = input_check(setting)
tleap_exec(setting)
convert(setting)

###equilibration###
equilibration(setting)

###prodiction###
production(setting)

###post-MD
trjconv(setting)
separate(setting, reslist)
outputs(setting)






















