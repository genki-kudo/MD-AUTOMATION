from subprocess import run
import os

bash=lambda x:run(x,shell=True)

base = os.path.dirname(os.path.abspath(__file__))


def outputs(setting, temp_dir):
    out_dir = os.path.join(setting['OUTPUT']['directory'], setting['SINCHO']['working_directory']

    nums = setting['MD']['edit_trajectory']['necessary-snaps']
    order_scale = int(len(str(int(nums)))+1)
    outdir = './separate_file/'
    for i in range(nums+1):
        if not os.path.exists(out_dir+"trajectory_"+str(i).zfill(order_scale)):
            os.makedirs(out_dir+"trajectory_"+str(i).zfill(order_scale))
        f_p = temp_dir+outdir+'/prot_'+str(i).zfill(order_scale)+'.pdb'
        f_l = temp_dir+outdir+'/lig_'+str(i).zfill(order_scale)+'.pdb'
    
        #bash("cp "+f_p+" "+out_dir+"trajectory_"+str(i).zfill(order_scale)+"/prot_"+str(i).zfill(order_scale)+".pdb")
        #bash("cp "+f_l+" "+out_dir+"trajectory_"+str(i).zfill(order_scale)+"/lig_"+str(i).zfill(order_scale)+".pdb")
        bash('obabel -ipdb '+f_p+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(order_scale)+'/prot_'+str(i).zfill(order_scale)+'.pdb')
        bash('obabel -ipdb '+f_l+' -opdb -O '+out_dir+'trajectory_'+str(i).zfill(order_scale)+'/lig_'+str(i).zfill(order_scale)+'.pdb')
