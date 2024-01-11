# MD-AUTOMATION

## Setup
```
#set PATH.
echo "export PATH=\$PATH:`pwd`/bin" >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:$(pwd)/bin' >> ~/.bashrc
source ~/.bashrc
```

## input file
* parameters/complex.pdb
* conditions.yaml

## Running（MD-＞P2C-＞SINCHO）
```
md_perform.py conditions.yaml

p2c_sincho_parallel.py conditions.yaml

yamlout.py conditions.yaml
```
