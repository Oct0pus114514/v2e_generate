import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def read_data(file_path):
    file=np.load(file_path)
    t,x,y,p=file['t'],file['x'],file['y'],file['p']
    return t,x,y,p

def plot_and_save(x,y,p,path):
    xmax,ymax=max(x),max(y)
    img_size = (ymax,xmax)
    num_events = len(x)
    img = np.zeros(shape=img_size, dtype=int)

    positions = [0.0, 0.5, 1.0]
    colors = ['blue', 'white', 'red']
    cmap = mcolors.LinearSegmentedColormap.from_list('blue_white_red', list(zip(positions, colors)))

    for i in range(num_events):
        if y[i]<img.shape[0] and x[i]<img.shape[1]:
            img[y[i], x[i]] = p[i]

    # draw image
    fig = plt.figure()
    fig.suptitle('Event Frame')
    plt.imshow(img, cmap=cmap,vmin=-1,vmax=1)
    plt.colorbar()
    plt.savefig(path)
    plt.close()

def sort_list_by_ts(lists):
    combined=list(zip(*lists))
    sorted_combined=sorted(combined,key=lambda x:x[0].mean())
    sorted_lists = list(zip(*sorted_combined))
    return [list(lst) for lst in sorted_lists]

if __name__=='__main__':
    
    for i in range(10):
        ts,xs,ys,ps=[],[],[],[]
        all_files=glob.glob(f'events/seq{i}/*.npz')
        if not os.path.exists(f'eall/seq{i}'):
            os.makedirs(f'eall/seq{i}')
        for file in all_files:
            t,x,y,p=read_data(file)
            t=t/1e9
            ts.append(t)
            xs.append(x)
            ys.append(y)
            ps.append(p)
        sorted_lists=sort_list_by_ts([ts,xs,ys,ps])
        ts,xs,ys,ps=sorted_lists
        for j in range(len(ts)-10):
            plot_and_save(np.concatenate(xs[j:j+10]),
                          np.concatenate(ys[j:j+10]),
                          np.concatenate(ps[j:j+10]),
                          f'eall/seq{i}/frame{j}.png')
    # print(ts)