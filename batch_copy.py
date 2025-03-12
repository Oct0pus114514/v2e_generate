import glob
import os

if not os.path.exists('rpg_vid2e/input'):
    os.mkdir('rpg_vid2e/input')
source_file=sorted(glob.glob(os.path.join('DL3DV_videos/DL3DV_points_50/1K','*')))
i=0
for dir_name in source_file:
    # print(dir_name)
    file_route=sorted(glob.glob(os.path.join(dir_name,'*.mp4')))
    for video in file_route:
        length_of_name=len(video)-len(dir_name)-1
        if length_of_name==8 or length_of_name==9:
            print(video)
            os.mkdir(f'rpg_vid2e/input/seq{i}')
            os.system(f'cp {video} rpg_vid2e/input/seq{i}/video{i}.mp4')
            i=i+1
            if i==10:
                exit()