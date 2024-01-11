# MD-AUTOMATION

## Setup
```
#set PATH.
echo "export PATH=\$PATH:`pwd`/bin" >> ~/.bashrc
source ~/.bashrc
```

## input file
* complex.pdb
* conditions.yaml

## Running
```
md_perform.py conditions.yaml ./ Tsukuba_workflow/MD/ Tsukuba_workflow/P2C_SINCHO/

p2c_sincho_parallel.py conditions.yaml Tsukuba_workflow/P2C_SINCHO
```
## additional
```
yamlout conditions.yaml Tsukuba_workflow/P2C_SINCHO/ out/yyyymmdd/sincho_out/
```
