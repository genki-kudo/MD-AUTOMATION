from subprocess import run
import os

bash=lambda x:run(x,shell=True)

base = os.path.dirname(os.path.abspath(__file__))


def outputs(setting, temp_dir):
    bef_dir = os.path.join(temp_dir, 'separate_file')
    aft_dir = os.path.join(setting['OUTPUT']['directory'], setting['SINCHO']['working_directory'])

    nums = setting['MD']['edit_trajectory']['necessary-snaps']
    order_scale = int(len(str(int(nums)))+1)

    for i in range(nums+1):
        n = str(i).zfill(order_scale)
        bdir = bef_dir
        adir = os.path.join(aft_dir, 'trajectory_'+n)
        if not os.path.exists(adir):
            os.makedirs(adir)
        f_p = os.path.join(aft_dir, 'trajectory_'+n, 'prot_'+n+'.pdb')
        f_l = os.path.join(aft_dir, 'trajectory_'+n, 'lig_'+n+'.pdb')
        
        b_prot = os.path.join(bdir, 'prot_'+n+'.pdb')
        a_prot = os.path.join(adir, 'prot_'+n+'.pdb')
        b_lig  = os.path.join(bdir, 'lig_'+n+'.pdb')
        a_lig  = os.path.join(adir, 'lig_'+n+'.pdb')
        
        print(os.getcwd())
        print(f'obabel -ipdb {b_prot} -opdb -O {a_prot}')
        
        bash(f'obabel -ipdb {b_prot} -opdb -O {a_prot}')
        bash(f'obabel -ipdb {b_lig} -opdb -O {a_lig}')
        
