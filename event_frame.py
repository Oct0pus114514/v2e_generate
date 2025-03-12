# event frame is just draw events on a figure. 

import numpy as np
from matplotlib import pyplot as plt
from types import SimpleNamespace

def extract_data(filename):
    infile = open(filename, 'r')
    ts, x, y, p, events = [], [], [], [], []
    for line in infile:
        words = line.split()
        ts.append(float(words[0]))
        x.append(int(words[1]))
        y.append(int(words[2]))
        p.append(int(words[3]))
    for i in range(len(ts)):
        events.append(SimpleNamespace(t=ts[i], x=x[i], y=y[i], p=p[i]))
    infile.close()
    return events

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

    for file_idx in range(22):
        events = extract_data(f'./eall/{file_idx}.txt')
        events=density_filter(events)
        x, y, p = events.x, events.y, events.p

        img_size = (288,512)
        num_events = len(x)
        img = np.zeros(shape=img_size, dtype=int)

        for i in range(num_events):
            img[y[i], x[i]] = (2*p[i]-1)

        # draw image
        fig = plt.figure()
        fig.suptitle('Event Frame')
        plt.imshow(img, cmap='gray')
        plt.xlabel("x [pixels]")
        plt.ylabel("y [pixels]")
        plt.colorbar()
        plt.axis('off')
        plt.savefig(f'eall/ev_fr/{file_idx}.jpg')
        plt.close()
    # plt.show()
