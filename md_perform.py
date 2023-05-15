#!/usr/bin/env python

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
from md_preparation.tleap import *
from md_preparation.input_check import *
from md_preparation.convert import *
from md_preparation.equilibration import *
from md_production.production import *
from md_production.trjconv import *
from md_production.separate import *

import json

bash=lambda x:run(x,shell=True)

###input args###
conditions = str(sys.argv[1])
with open(conditions,'r')as f:
    setting = yaml.safe_load(f)

###preparation###
reslist = input_check(setting)

tleap_exec(setting)
convert()

###equilibration###
equilibration(setting)

###prodiction###
production(setting)


trjconv(setting)


separate(setting, reslist)



















