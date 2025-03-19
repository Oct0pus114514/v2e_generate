import event_utils as eu
import numpy as np

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

if __name__=='__main__':
    ts, x, y, p = extract_data('eall/seq0/0.txt')
    xs,ys,ps=np.array(x),np.array(y),np.array(p)
    image=eu.events_to_image(xs,ys,ps,sensor_size=(288,512))
    eu.save_image(image,save_path='eall/new/0.jpg')
    print(type(image))