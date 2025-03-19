# event frame is just draw events on a figure. 

import numpy as np
from matplotlib import pyplot as plt
import glob
import lowpass_filter as lf
import os

def extract_data(filename):
    infile = open(filename, 'r')
    ts, x, y, p = [], [], [], []
    for line in infile:
        words = line.split()
        ts.append(float(words[0]))
        x.append(int(words[1]))
        y.append(int(words[2]))
        p.append(int(words[3]))
    infile.close()
    return ts, x, y, p

def density_filter(events, time_window=0.01, density_threshold=3):
    events_sorted = sorted(events, key=lambda e: e.t)
    filtered_events = []
    current_time = events_sorted[0].t
    while current_time <= events_sorted[-1].t:
        window_events = [e for e in events_sorted if current_time <= e.t < current_time + time_window]
        # 统计每个 (x,y) 的事件数
        coord_counts = {}
        for e in window_events:
            key = (e.x, e.y)
            coord_counts[key] = coord_counts.get(key, 0) + 1
        # 保留计数超过阈值的坐标事件
        for e in window_events:
            if coord_counts[(e.x, e.y)] >= density_threshold:
                filtered_events.append(e)
        current_time += time_window
    return filtered_events


if __name__ == '__main__':
    filter = lf.LowpassFilter(tau=0.02)
    for k in range(10):
        all_files=glob.glob(f'./eall/seq{k}/*.txt')
        for file_idx in range(len(all_files)):
            ts, x, y, p = extract_data(f'./eall/seq{k}/{file_idx}.txt')
            for i in range(len(ts)):
                filter.process_event([x[i], y[i], p[i], ts[i]])
            xmax,ymax=max(x),max(y)
            img_size = (ymax,xmax)
            num_events = len(x)
            img = np.zeros(shape=img_size, dtype=int)

            for i in range(num_events):
                if y[i]<img.shape[0] and x[i]<img.shape[1]:
                    img[y[i], x[i]] = (2*p[i]-1)
    
            # draw image
            fig = plt.figure()
            fig.suptitle('Event Frame')
            plt.imshow(img, cmap='gray')
            plt.xlabel("x [pixels]")
            plt.ylabel("y [pixels]")
            plt.colorbar()
            plt.axis('off')
            if not os.path.exists(f'eall/ev_fr/seq{k}'):
                os.mkdir(f'eall/ev_fr/seq{k}')
            plt.savefig(f'eall/ev_fr/seq{k}/{file_idx}.jpg')
            plt.close()
    # plt.show()
