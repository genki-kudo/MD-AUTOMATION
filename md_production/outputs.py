from subprocess import run
import os

bash=lambda x:run(x,shell=True)

base = os.path.dirname(os.path.abspath(__file__))


def outputs(setting, temp_dir):
    out_dir = setting['P2C_SINCHO']['working_directory']

    nums = setting['MD']['edit_trajectory']['necessary-snaps']
    outdir = './separate_file/'
    for i in range(nums+1):
        if not os.path.exists(out_dir+"trajectory_"+str(i).zfill(3)):
            os.makedirs(out_dir+"trajectory_"+str(i).zfill(3))
        f_p = temp_dir+outdir+'/prot_'+str(i).zfill(3)+'.pdb'
        f_l = temp_dir+outdir+'/lig_'+str(i).zfill(3)+'.pdb'
    
        #bash("cp "+f_p+" "+out_dir+"trajectory_"+str(i).zfill(3)+"/prot_"+str(i).zfill(3)+".pdb")
        #bash("cp "+f_l+" "+out_dir+"trajectory_"+str(i).zfill(3)+"/lig_"+str(i).zfill(3)+".pdb")
        bash('obabel -ipdb '+f_p+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(3)+'/prot_'+str(i).zfill(3)+'.pdb')
        bash('obabel -ipdb '+f_l+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(3)+'/lig_'+str(i).zfill(3)+'.pdb')
