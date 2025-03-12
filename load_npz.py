import numpy as np
import glob
import os

if not os.path.exists('eall'):
    os.mkdir('eall')

all_files=sorted(glob.glob(os.path.join('events/seq0','*.npz')))
# print(all_files)
f=open('eall/1.txt','w')
cnt,j=0,0
# print(np.load(file)['t'].shape[0])
for file in all_files:
    np.load(file)
    if cnt%50==0:
        f=open('eall/'+str(j)+'.txt','w')
        print(f'file {j} created')
    if cnt%50>=0 and cnt%50<10:
        for i in range(np.load(file)['t'].shape[0]):
            f.write(str(np.load(file)['t'][i]/(10**9))+' '+str(np.load(file)['x'][i])+' '+
                str(np.load(file)['y'][i])+' '+str(np.load(file)['p'][i])+'\n')
        print(f'npz {cnt} done')
    cnt=cnt+1
    if cnt%50==10:
        f.close()
        j=j+1
    