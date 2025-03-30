import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse
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
    
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--input_folder',type=str,required=True,help='输入事件数据文件夹路径')
    parser.add_argument('-o','--output_folder',type=str,required=True,help='输出图片文件夹路径')
    input_dir=parser.parse_args().input_folder
    output_dir=parser.parse_args().output_folder
    all_files=sorted(glob.glob(os.path.join(input_dir,'*.npz')))

    ts,xs,ys,ps=[],[],[],[]
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
                        f'{output_dir}/frame{j}.png')
    # print(ts)